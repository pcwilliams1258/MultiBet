"""
Test suite for the local quality gateway configuration.

This suite validates that the pyproject.toml and .pre-commit-config.yaml files
are correctly configured to support the project's quality standards using Ruff
and pre-commit.
"""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml


def test_pyproject_toml_exists_and_is_valid():
    """Test that pyproject.toml exists and contains valid TOML."""
    repo_root = Path(__file__).parent.parent
    pyproject_path = repo_root / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml must exist in the project root"

    # This will raise an error if the TOML is invalid
    with open(pyproject_path, "r") as f:
        content = f.read()
    assert "[tool.ruff]" in content, "pyproject.toml must contain [tool.ruff] section"


def test_ruff_configuration_in_pyproject_toml():
    """Test that the ruff configuration in pyproject.toml is correct."""
    repo_root = Path(__file__).parent.parent
    pyproject_path = repo_root / "pyproject.toml"

    with open(pyproject_path, "r") as f:
        content = f.read()

    # Check for key configuration details
    assert 'line-length = 88' in content
    assert 'target-version = "py311"' in content
    assert 'select = ["E", "W", "F", "I"]' in content
    assert 'ignore = ["E501"]' in content
    assert "preview = true" in content


def test_pre_commit_config_exists_and_is_valid():
    """Test that .pre-commit-config.yaml exists and is valid YAML."""
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / ".pre-commit-config.yaml"
    assert config_path.exists(), ".pre-commit-config.yaml must exist"

    with open(config_path, "r") as f:
        # yaml.safe_load will raise an error on invalid YAML
        config = yaml.safe_load(f)
    assert "repos" in config, ".pre-commit-config.yaml must have a 'repos' key"


def test_pre_commit_config_contains_ruff_hooks():
    """Test that the pre-commit config contains the required ruff hooks."""
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / ".pre-commit-config.yaml"

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    ruff_repo_found = False
    for repo in config.get("repos", []):
        if "astral-sh/ruff-pre-commit" in repo.get("repo", ""):
            ruff_repo_found = True
            hook_ids = [hook["id"] for hook in repo.get("hooks", [])]
            assert "ruff" in hook_ids, "Ruff hook with id 'ruff' must be present"
            assert "ruff-format" in hook_ids, "Ruff hook with id 'ruff-format' must be present"
            break

    assert ruff_repo_found, "Repository 'astral-sh/ruff-pre-commit' not found in config"


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for testing pre-commit hooks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        subprocess.run(["git", "init"], cwd=repo_path, check=True)

        # Copy essential config files
        repo_root = Path(__file__).parent.parent
        for config_file in [".pre-commit-config.yaml", "pyproject.toml", "requirements.txt"]:
            (repo_path / config_file).write_text((repo_root / config_file).read_text())

        # Create a virtual environment and install dependencies
        venv_path = repo_path / ".venv"
        subprocess.run([f"python -m venv {venv_path}"], shell=True, cwd=repo_path, check=True)
        pip_executable = f"{venv_path / 'bin' / 'pip'}"
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"], cwd=repo_path, check=True)

        # Install pre-commit hooks
        pre_commit_executable = f"{venv_path / 'bin' / 'pre-commit'}"
        subprocess.run([pre_commit_executable, "install"], cwd=repo_path, check=True)

        yield repo_path


def test_pre_commit_hook_fixes_bad_file(temp_git_repo):
    """
    Simulate a commit of a poorly formatted file and check if pre-commit fixes it.
    """
    bad_code = "import os,sys\n\ndef my_func( ):\n    print('hello world'  )\n"
    test_file = temp_git_repo / "bad_file.py"
    test_file.write_text(bad_code)

    # Stage the file
    subprocess.run(["git", "add", test_file], cwd=temp_git_repo, check=True)

    # Attempt to commit (it should fail because of fixes)
    result = subprocess.run(
        ["git", "commit", "-m", "test commit"],
        cwd=temp_git_repo,
        capture_output=True,
        text=True
    )
    assert result.returncode != 0, "Commit should fail when files are modified by hooks"

    # Check that the file has been reformatted
    fixed_code = test_file.read_text()
    assert "import os" in fixed_code
    assert "import sys" in fixed_code
    assert "def my_func():" in fixed_code  # Check for corrected spacing
    assert "print('hello world')" in fixed_code  # Check for corrected spacing
