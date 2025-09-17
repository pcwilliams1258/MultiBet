"""
Test suite to validate the repository structure and CI/CD pipeline requirements.
These tests ensure that the branch protection setup is working correctly.
"""

import sys
from pathlib import Path


def test_python_version():
    """Test that we're running on a supported Python version"""
    assert sys.version_info >= (3, 8), f"Python version {sys.version} is not supported"


def test_repository_structure():
    """Test that key directories and files exist"""
    repo_root = Path(__file__).parent.parent

    # Check for essential directories
    assert (repo_root / "src").exists(), "src directory must exist"
    assert (repo_root / ".github").exists(), ".github directory must exist"
    assert (
        repo_root / ".github" / "workflows"
    ).exists(), "workflows directory must exist"
    assert (repo_root / "docs").exists(), "docs directory must exist"

    # Check for essential files
    assert (repo_root / "requirements.txt").exists(), "requirements.txt must exist"
    assert (repo_root / ".gitignore").exists(), ".gitignore must exist"


def test_ci_workflow_exists():
    """Test that the CI workflow file exists and is properly configured"""
    repo_root = Path(__file__).parent.parent
    ci_workflow = repo_root / ".github" / "workflows" / "ci.yml"

    assert ci_workflow.exists(), "CI workflow file must exist"

    # Check that the workflow contains required job names
    workflow_content = ci_workflow.read_text()
    required_jobs = [
        "lint-and-format",
        "test",
        "security-scan",
        "dependency-check",
        "documentation-check",
        "build-validation",
        "integration-status",
    ]

    for job in required_jobs:
        assert (
            job in workflow_content
        ), f"Required job '{job}' not found in CI workflow"


def test_branch_protection_documentation():
    """Test that branch protection documentation exists"""
    repo_root = Path(__file__).parent.parent
    doc_file = repo_root / ".github" / "BRANCH_PROTECTION_SETUP.md"

    assert doc_file.exists(), "Branch protection documentation must exist"

    # Check that documentation contains required sections
    doc_content = doc_file.read_text()
    required_sections = [
        "Branch Protection Configuration Guide",
        "Require a Pull Request Before Merging",
        "Require Status Checks to Pass Before Merging",
        "Do Not Allow Bypassing the Above Settings",
        "Implementation Steps",
    ]

    for section in required_sections:
        assert (
            section in doc_content
        ), f"Required section '{section}' not found in documentation"


def test_requirements_file_format():
    """Test that requirements.txt is properly formatted"""
    repo_root = Path(__file__).parent.parent
    requirements_file = repo_root / "requirements.txt"

    assert requirements_file.exists(), "requirements.txt must exist"

    # Read and validate requirements format
    with open(requirements_file, "r") as f:
        lines = f.readlines()

    # Remove the numbered format and validate packages
    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            # Remove leading numbers if present
            if line[0].isdigit() and "." in line:
                package = line.split(".", 1)[1] if "." in line else line
            else:
                package = line
            packages.append(package.strip())

    # Check that essential packages are present
    essential_packages = ["flask", "pandas", "numpy", "pytest"]
    for package in essential_packages:
        package_found = any(package.lower() in pkg.lower() for pkg in packages)
        assert (
            package_found
        ), f"Essential package '{package}' not found in requirements"


def test_gitignore_includes_common_files():
    """Test that .gitignore includes common files that should be ignored"""
    repo_root = Path(__file__).parent.parent
    gitignore_file = repo_root / ".gitignore"

    assert gitignore_file.exists(), ".gitignore file must exist"

    gitignore_content = gitignore_file.read_text()

    # Check for common patterns that should be ignored
    common_patterns = ["__pycache__", ".env", ".venv"]
    for pattern in common_patterns:
        assert (
            pattern in gitignore_content
        ), f"Pattern '{pattern}' should be in .gitignore"

    # Check for Python byte-compiled files (can be *.pyc or *.py[cod])
    python_patterns = ["*.pyc", "*.py[cod]"]
    python_pattern_found = any(
        pattern in gitignore_content for pattern in python_patterns
    )
    assert (
        python_pattern_found
    ), "Python byte-compiled file patterns should be in .gitignore"


def test_documentation_completeness():
    """Test that project documentation is complete"""
    repo_root = Path(__file__).parent.parent
    docs_dir = repo_root / "docs"

    assert docs_dir.exists(), "docs directory must exist"

    # Check for essential documentation files
    essential_docs = ["PLAN.md", "technical_specification.md"]

    for doc in essential_docs:
        doc_path = docs_dir / doc
        assert doc_path.exists(), f"Essential documentation '{doc}' not found"

        # Check that files are not empty
        content = doc_path.read_text().strip()
        assert (
            len(content) > 100
        ), f"Documentation file '{doc}' appears to be too short or empty"


def test_workflow_trigger_configuration():
    """Test that workflows are triggered on appropriate events"""
    repo_root = Path(__file__).parent.parent
    ci_workflow = repo_root / ".github" / "workflows" / "ci.yml"

    assert ci_workflow.exists(), "CI workflow must exist"

    workflow_content = ci_workflow.read_text()

    # Check for proper trigger configuration
    assert "on:" in workflow_content, "Workflow must have trigger configuration"
    assert "pull_request:" in workflow_content, "Workflow must trigger on pull requests"
    assert (
        "branches: [ main ]" in workflow_content
    ), "Workflow must trigger on main branch"
