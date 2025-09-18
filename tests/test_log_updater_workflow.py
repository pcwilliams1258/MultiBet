"""
Test for GitHub Actions log updater workflow validation.
"""

import os

import yaml


def test_log_updater_workflow_exists():
    """Test that the log_updater workflow file exists."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "log_updater.yml",
    )

    assert os.path.exists(workflow_path), "Log updater workflow file does not exist"


def test_log_updater_workflow_syntax():
    """Test that the log updater workflow YAML is valid."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "log_updater.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Basic workflow structure validation
    assert "name" in workflow_content
    assert workflow_content["name"] == "Log Updater"
    assert "jobs" in workflow_content

    # Handle YAML parsing quirk where 'on' becomes True
    trigger_key = True if True in workflow_content else "on"
    assert trigger_key in workflow_content

    # Check that the workflow has pull_request trigger
    assert "pull_request" in workflow_content[trigger_key]
    assert "types" in workflow_content[trigger_key]["pull_request"]
    assert "opened" in workflow_content[trigger_key]["pull_request"]["types"]


def test_log_updater_job_structure():
    """Test that the log updater job has correct structure."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "log_updater.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    # Check job structure
    jobs = workflow_content["jobs"]
    assert "update-log" in jobs

    job = jobs["update-log"]
    assert "runs-on" in job
    assert job["runs-on"] == "ubuntu-latest"
    assert "name" in job
    assert job["name"] == "Update LOGS.md"
    assert "steps" in job
    assert isinstance(job["steps"], list)


def test_log_updater_workflow_steps():
    """Test that workflow has the required steps."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "log_updater.yml",
    )

    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)

    job = workflow_content["jobs"]["update-log"]
    step_names = [step.get("name", "") for step in job["steps"]]

    required_steps = [
        "Checkout code",
        "Extract issue number from PR body",
        "Check issue assignee",
        "Update LOGS.md",
        "Commit changes",
    ]

    for required_step in required_steps:
        assert any(required_step in step_name for step_name in step_names), (
            f"Required step '{required_step}' not found in workflow"
        )


def test_log_updater_references_logs_file():
    """Test that workflow references LOGS.md file instead of PROMPT_LOG.md."""
    workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "log_updater.yml",
    )

    with open(workflow_path, "r") as f:
        content = f.read()

    # Check that it references LOGS.md
    assert "docs/LOGS.md" in content
    assert "Auto-update LOGS.md" in content

    # Check that it doesn't reference old PROMPT_LOG.md
    assert "PROMPT_LOG.md" not in content


def test_logs_file_exists():
    """Test that the LOGS.md file exists."""
    logs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs",
        "LOGS.md",
    )

    assert os.path.exists(logs_path), "LOGS.md file does not exist"


def test_old_prompt_log_updater_workflow_removed():
    """Test that the old prompt_log_updater.yml workflow is removed."""
    old_workflow_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".github",
        "workflows",
        "prompt_log_updater.yml",
    )

    assert not os.path.exists(old_workflow_path), (
        "Old prompt_log_updater.yml workflow should be removed"
    )


def test_old_prompt_log_file_removed():
    """Test that the old PROMPT_LOG.md file is removed."""
    old_log_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs",
        "PROMPT_LOG.md",
    )

    assert not os.path.exists(old_log_path), "Old PROMPT_LOG.md file should be removed"
