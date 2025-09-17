"""
Test suite to validate that GitHub templates contain proper documentation references.
This test ensures compliance with the issue template update requirements.
"""

from pathlib import Path


def test_development_task_template_has_documentation_section():
    """Test that development_task.md contains the Documentation section with required checkboxes"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "development_task.md"
    
    assert template_file.exists(), "development_task.md template must exist"
    
    content = template_file.read_text()
    
    # Check for Documentation section
    assert "## Documentation" in content, "Template must contain Documentation section"
    
    # Check for current_project_state.md reference
    assert "current_project_state.md" in content, "Template must reference current_project_state.md"
    assert "I have reviewed `current_project_state.md`" in content, "Template must have checkbox for reviewing current_project_state.md"
    
    # Check for technical_debt_log.md reference
    assert "documentation/technical_debt_log.md" in content, "Template must reference documentation/technical_debt_log.md"
    assert "I have checked `documentation/technical_debt_log.md`" in content, "Template must have checkbox for checking technical_debt_log.md"


def test_feature_request_template_has_current_project_state_checkbox():
    """Test that feature_request.md contains checkbox for reviewing current_project_state.md"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "feature_request.md"
    
    assert template_file.exists(), "feature_request.md template must exist"
    
    content = template_file.read_text()
    
    # Check for the new section
    assert "### Is your feature request related to a problem?" in content, "Template must contain the new subsection"
    
    # Check for current_project_state.md reference
    assert "current_project_state.md" in content, "Template must reference current_project_state.md"
    assert "I have reviewed `current_project_state.md`" in content, "Template must have checkbox for reviewing current_project_state.md"


def test_pull_request_template_has_ai_generated_content_section():
    """Test that pull_request_template.md contains AI-Generated Content section with copilot.md reference"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "pull_request_template.md"
    
    assert template_file.exists(), "pull_request_template.md must exist"
    
    content = template_file.read_text()
    
    # Check for AI-Generated Content section
    assert "## AI-Generated Content" in content, "Template must contain AI-Generated Content section"
    
    # Check for copilot.md reference
    assert ".github/copilot.md" in content, "Template must reference .github/copilot.md"
    assert "Changes are consistent with the guidelines in `.github/copilot.md`" in content, "Template must have checkbox for copilot guidelines"


def test_referenced_documentation_files_exist():
    """Test that all referenced documentation files actually exist"""
    repo_root = Path(__file__).parent.parent
    
    # Check that referenced files exist
    current_project_state = repo_root / "current_project_state.md"
    assert current_project_state.exists(), "current_project_state.md must exist"
    
    technical_debt_log = repo_root / "documentation" / "technical_debt_log.md"
    assert technical_debt_log.exists(), "documentation/technical_debt_log.md must exist"
    
    copilot_guidelines = repo_root / ".github" / "copilot.md"
    assert copilot_guidelines.exists(), ".github/copilot.md must exist"


if __name__ == "__main__":
    import pytest
    
    pytest.main([__file__, "-v"])