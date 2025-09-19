"""
Test for GitHub Actions workflow validation.
"""

import os

import yaml


def test_ci_workflow_exists():
    """Test that the main CI workflow YAML is valid and exists."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "ci.yml",
    )

    assert os.path.exists(workflow_path), "The main ci.yml workflow file must exist"

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Basic workflow structure validation
    assert "name" in workflow_content
    assert "jobs" in workflow_content
    # YAML parses 'on:' as boolean True, so check for that
    assert True in workflow_content or "on" in workflow_content


def test_workflow_python_version():
    """Test that the main workflow uses the correct Python version."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "ci.yml",
    )

    with open(workflow_path, "r") as f:
        content = f.read()

    # Check that Python version is specified and supported
    assert "python-version:" in content
    assert "'3.11'" in content  # Should use Python 3.11 in quotes


def test_workflow_permissions():
    """Test that the security job has appropriate permissions."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "ci.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    job = workflow_content["jobs"]["security"]

    # Check permissions are set for the security job
    assert "permissions" in job
    permissions = job["permissions"]
    assert "contents" in permissions
    assert "security-events" in permissions

    # Check for reasonable permission values
    assert permissions["contents"] == "read"
    assert permissions["security-events"] == "write"
