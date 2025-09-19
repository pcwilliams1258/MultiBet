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
    assert (repo_root / "src").exists(), "src directory must exist"
    assert (repo_root / ".github" / "workflows").exists(), "workflows directory must exist"
    assert (repo_root / "docs").exists(), "docs directory must exist"
    assert (repo_root / "requirements.txt").exists(), "requirements.txt must exist"
    assert (repo_root / ".gitignore").exists(), ".gitignore must exist"


def test_ci_workflow_exists_and_is_configured():
    """Test that the CI workflow file exists and is properly configured"""
    repo_root = Path(__file__).parent.parent
    ci_workflow = repo_root / ".github" / "workflows" / "ci.yml"
    assert ci_workflow.exists(), "CI workflow file must exist"

    # Check that the workflow contains the new, consolidated job names
    workflow_content = ci_workflow.read_text()
    required_jobs = [
        "quality-and-tests",
        "security",
    ]
    for job in required_jobs:
        assert job in workflow_content, f"Required job '{job}' not found in CI workflow"

    # Check for proper trigger configuration
    assert "on:" in workflow_content, "Workflow must have trigger configuration"
    assert "pull_request:" in workflow_content, "Workflow must trigger on pull requests"
    assert "branches:" in workflow_content, "Workflow must specify branches"
    assert "main" in workflow_content, "Workflow must trigger on main branch"


def test_branch_protection_documentation_is_aligned():
    """Test that branch protection documentation is aligned with the new strategy"""
    repo_root = Path(__file__).parent.parent
    doc_file = repo_root / ".github" / "BRANCH_PROTECTION_SETUP.md"
    assert doc_file.exists(), "Branch protection documentation must exist"

    # Check that the documentation contains the new required sections/jobs
    doc_content = doc_file.read_text()
    required_sections = [
        "Branch Protection Configuration Guide",
        "Required Status Checks",
        "Quality Checks & Tests",
        "Security Audits",
        "Implementation Steps",
    ]
    for section in required_sections:
        assert section in doc_content, f"Required section '{section}' not found in documentation"
