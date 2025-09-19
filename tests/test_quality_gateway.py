"""
Test suite to validate the local quality gateway implementation.
This test ensures that Ruff and Pre-commit are properly configured.
"""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml


def test_pyproject_toml_exists():
    """Test that pyproject.toml exists with Ruff configuration."""
    repo_root = Path(__file__).parent.parent
    pyproject_file = repo_root / "pyproject.toml"
    
    assert pyproject_file.exists(), "pyproject.toml must exist"
    
    content = pyproject_file.read_text()
    
    # Check for required Ruff configuration sections
    assert "[tool.ruff]" in content, "pyproject.toml must contain [tool.ruff] section"
    assert "[tool.ruff.lint]" in content, "pyproject.toml must contain [tool.ruff.lint] section"
    assert "[tool.ruff.format]" in content, "pyproject.toml must contain [tool.ruff.format] section"
    
    # Check for specific configuration values
    assert "line-length = 88" in content, "Ruff must be configured with line-length = 88"
    assert 'target-version = "py311"' in content, "Ruff must target Python 3.11"
    assert "preview = true" in content, "Ruff format must enable preview mode"


def test_pre_commit_config_exists():
    """Test that .pre-commit-config.yaml exists with proper configuration."""
    repo_root = Path(__file__).parent.parent
    config_file = repo_root / ".pre-commit-config.yaml"
    
    assert config_file.exists(), ".pre-commit-config.yaml must exist"
    
    content = config_file.read_text()
    
    # Check for required hooks
    assert "pre-commit/pre-commit-hooks" in content, "Must include standard pre-commit hooks"
    assert "astral-sh/ruff-pre-commit" in content, "Must include Ruff pre-commit hooks"
    
    # Check for specific hooks
    required_hooks = [
        "trailing-whitespace",
        "end-of-file-fixer", 
        "check-yaml",
        "check-toml",
        "ruff",
        "ruff-format"
    ]
    
    for hook in required_hooks:
        assert hook in content, f"Must include {hook} hook"
    
    # Check for Ruff arguments
    assert "--fix" in content, "Ruff hook must include --fix argument"
    assert "--exit-non-zero-on-fix" in content, "Ruff hook must include --exit-non-zero-on-fix argument"


def test_pre_commit_installation():
    """Test that pre-commit is properly installed."""
    repo_root = Path(__file__).parent.parent
    
    # Check that git hooks are installed
    hooks_file = repo_root / ".git" / "hooks" / "pre-commit"
    assert hooks_file.exists(), "Pre-commit git hooks must be installed"


def test_ruff_functionality():
    """Test that Ruff can detect and fix formatting issues."""
    # Create a temporary poorly formatted Python file
    poorly_formatted_code = '''
import sys,os
def test(  x,y  ):
 return x+y
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(poorly_formatted_code)
        temp_file = f.name
    
    try:
        repo_root = Path(__file__).parent.parent
        
        # Test that ruff check detects issues
        result = subprocess.run(
            ['ruff', 'check', temp_file],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        
        # Ruff should find issues in the poorly formatted code
        assert result.returncode != 0, "Ruff should detect formatting issues"
        assert "import" in result.stdout.lower() or "import" in result.stderr.lower(), "Should detect import issues"
        
        # Test that ruff format can fix formatting
        result = subprocess.run(
            ['ruff', 'format', temp_file],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, "Ruff format should succeed"
        
        # Read the formatted code
        with open(temp_file, 'r') as f:
            formatted_code = f.read()
        
        # Check that formatting was improved
        assert "import sys" in formatted_code, "Imports should be properly formatted"
        assert "def test(x, y):" in formatted_code, "Function signature should be properly formatted"
        
    finally:
        # Clean up
        os.unlink(temp_file)


def test_ruff_configuration_values():
    """Test that Ruff respects the configuration in pyproject.toml."""
    repo_root = Path(__file__).parent.parent
    
    # Create a test file with a simple long line to test our E501 ignore
    long_line_code = '''def test_function():
    # This is just a very long string literal that definitely exceeds our 88 character line limit but should not cause issues
    message = "This is a very long string that exceeds the 88 character limit set in pyproject.toml configuration"
    return message
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(long_line_code)
        temp_file = f.name
    
    try:
        # Test ruff format with our configuration
        result = subprocess.run(
            ['ruff', 'format', temp_file],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, "Ruff format should succeed"
        
        # Test that ruff check respects our configuration (without forcing E501)
        result = subprocess.run(
            ['ruff', 'check', temp_file],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        
        # Should pass because E501 (line too long) is ignored in our config
        # and there are no other linting issues
        assert result.returncode == 0, f"Ruff check should pass with our configuration. Output: {result.stdout}"
        
    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
