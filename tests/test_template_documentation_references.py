from pathlib import Path

def test_development_task_template_has_documentation_section():
    template_file = Path(".github/ISSUE_TEMPLATE/development_task.md")
    assert template_file.exists(), "development_task.md template must exist"
    content = template_file.read_text()
    assert "## Documentation" in content, "Template must contain Documentation section"
    assert "current_project_state.md" in content, "Template must reference current_project_state.md"
    assert "I have reviewed `current_project_state.md`" in content, "Template must have checkbox for reviewing current_project_state.md"
    assert "documentation/technical_debt_log.md" in content, "Template must reference documentation/technical_debt_log.md"
    assert "I have checked `documentation/technical_debt_log.md`" in content, "Template must have checkbox for checking technical_debt_log.md"

def test_feature_request_template_has_current_project_state_checkbox():
    template_file = Path(".github/ISSUE_TEMPLATE/feature_request.md")
    assert template_file.exists(), "feature_request.md template must exist"
    content = template_file.read_text()
    assert "### Is your feature request related to a problem?" in content, "Template must contain the new subsection"
    assert "current_project_state.md" in content, "Template must reference current_project_state.md"
    assert "I have reviewed `current_project_state.md`" in content, "Template must have checkbox for reviewing current_project_state.md"

def test_pull_request_template_has_ai_generated_content_section():
    template_file = Path(".github/pull_request_template.md")
    assert template_file.exists(), "pull_request_template.md must exist"
    content = template_file.read_text()
    assert "## AI-Generated Content" in content, "Template must contain AI-Generated Content section"
    assert ".github/copilot.md" in content, "Template must reference .github/copilot.md"
    assert "Changes are consistent with the guidelines in `.github/copilot.md`" in content, "Template must have checkbox for copilot guidelines"

def test_referenced_documentation_files_exist():
    current_project_state = Path("current_project_state.md")
    assert current_project_state.exists(), "current_project_state.md must exist"
    technical_debt_log = Path("documentation/technical_debt_log.md")
    assert technical_debt_log.exists(), "documentation/technical_debt_log.md must exist"
    copilot_guidelines = Path(".github/copilot.md")
    assert copilot_guidelines.exists(), ".github/copilot.md must exist"
