"""
Test for GitHub Actions workflow validation.
"""

import os
import yaml

def test_ci_workflow_syntax():
    """Test that the main CI workflow YAML is valid."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "ci.yml",
    )

    assert os.path.exists(workflow_path), "Main CI workflow file (ci.yml) does not exist"

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Basic workflow structure validation
    assert "name" in workflow_content
    assert "on" in workflow_content
    assert "jobs" in workflow_content

    # Check for pull_request trigger
    assert "pull_request" in workflow_content["on"]
    assert "push" in workflow_content["on"]

def test_ci_workflow_job_structure():
    """Test that the CI workflow has the correct job structure."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "ci.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    jobs = workflow_content["jobs"]
    
    # Check for the main jobs
    expected_jobs = [
        "lint-and-format",
        "test",
        "security-scan",
        "dependency-check",
        "build-validation",
        "integration-status"
    ]
    
    for job_name in expected_jobs:
        assert job_name in jobs, f"Expected job '{job_name}' not found in ci.yml"
        assert "runs-on" in jobs[job_name]
        assert "steps" in jobs[job_name]

def test_retrain_workflow_exists_and_is_valid():
    """Test that the separate retrain workflow still exists and is valid."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    assert os.path.exists(workflow_path), "Retrain workflow file (retrain_pipeline.yml) does not exist"

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Validate basic structure
    assert "name" in workflow_content
    assert "on" in workflow_content
    assert "jobs" in workflow_content
    assert "retrain-models" in workflow_content["jobs"]
    
    # Validate triggers
    assert "schedule" in workflow_content["on"]
    assert "workflow_dispatch" in workflow_content["on"]
