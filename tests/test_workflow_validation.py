"""
Test for GitHub Actions workflow validation.
"""

import os

import yaml


def test_retrain_workflow_syntax():
    """Test that the retrain workflow YAML is valid."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    assert os.path.exists(workflow_path), "Retrain workflow file does not exist"

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Basic workflow structure validation
    assert "name" in workflow_content
    assert "jobs" in workflow_content

    # Handle YAML parsing quirk where 'on' becomes True
    trigger_key = True if True in workflow_content else "on"
    assert trigger_key in workflow_content

    # Check that the workflow has scheduled trigger
    assert "schedule" in workflow_content[trigger_key]
    assert isinstance(workflow_content[trigger_key]["schedule"], list)
    assert len(workflow_content[trigger_key]["schedule"]) > 0

    # Check manual trigger capability
    assert "workflow_dispatch" in workflow_content[trigger_key]

    # Check job structure
    jobs = workflow_content["jobs"]
    assert "retrain-models" in jobs

    job = jobs["retrain-models"]
    assert "runs-on" in job
    assert "steps" in job
    assert isinstance(job["steps"], list)

    # Validate key steps exist
    step_names = [step.get("name", "") for step in job["steps"]]
    required_steps = [
        "Checkout code",
        "Set up Python",
        "Install dependencies",
        "Execute model retraining pipeline",
    ]

    for required_step in required_steps:
        assert any(required_step in step_name for step_name in step_names), (
            f"Required step '{required_step}' not found in workflow"
        )


def test_workflow_python_version():
    """Test that workflow uses supported Python version."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    with open(workflow_path, "r") as f:
        content = f.read()

    # Check that Python version is specified and supported
    assert "python-version:" in content
    assert "3.11" in content  # Should use Python 3.11


def test_workflow_permissions():
    """Test that workflow has appropriate permissions."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    job = workflow_content["jobs"]["retrain-models"]

    # Check permissions are set
    assert "permissions" in job
    permissions = job["permissions"]
    assert "contents" in permissions
    assert "id-token" in permissions

    # Check for reasonable permission values
    assert permissions["contents"] == "read"
    assert permissions["id-token"] == "write"


def test_workflow_environment_variables():
    """Test that workflow uses environment variables correctly."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    with open(workflow_path, "r") as f:
        content = f.read()

    # Check for required environment variables
    required_env_vars = ["GCP_PROJECT_ID", "BIGQUERY_DATASET", "MODEL_REGISTRY_BUCKET"]

    for env_var in required_env_vars:
        assert env_var in content, (
            f"Environment variable {env_var} not found in workflow"
        )


def test_workflow_error_handling():
    """Test that workflow has proper error handling."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    with open(workflow_path, "r") as f:
        content = f.read()

    # Check for error handling features
    assert "continue-on-error" in content
    assert "if: failure()" in content
    assert "if: always()" in content
    assert "upload-artifact" in content


def test_workflow_schedule_format():
    """Test that the workflow schedule is properly formatted."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "retrain_pipeline.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Handle YAML parsing quirk where 'on' becomes True
    trigger_key = True if True in workflow_content else "on"
    schedule = workflow_content[trigger_key]["schedule"][0]
    cron_expr = schedule["cron"]

    # Basic cron format validation (5 fields)
    cron_parts = cron_expr.split()
    assert len(cron_parts) == 5, f"Invalid cron expression: {cron_expr}"

    # Check that it's scheduled for Sunday (0) at 3 AM UTC
    assert cron_parts[0] == "0", "Should run at minute 0"
    assert cron_parts[1] == "3", "Should run at hour 3 (3 AM UTC)"
    assert cron_parts[4] == "0", "Should run on Sunday (day 0)"
