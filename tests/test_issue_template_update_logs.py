"""
Test suite to validate the update_logs.md issue template.
This test ensures that the template file exists and contains the required content.
"""

from pathlib import Path


def test_update_logs_template_exists():
    """Test that the update_logs.md issue template file exists"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_logs.md"

    assert template_file.exists(), "update_logs.md issue template must exist"


def test_update_logs_template_has_correct_frontmatter():
    """Test that the template has the correct YAML frontmatter"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_logs.md"

    content = template_file.read_text()

    # Check for proper YAML frontmatter
    assert content.startswith("---"), "Template must start with YAML frontmatter"
    assert "name: ✍️ Update Logs & Docs" in content, "Template must have correct name"
    assert (
        "about: Use this template to log AI conversations and update key documents."
        in content
    ), "Template must have correct about description"
    assert (
        "title: 'LOG: [Brief description of changes]'" in content
    ), "Template must have correct default title"
    assert "labels: 'documentation'" in content, "Template must have correct labels"


def test_update_logs_template_has_required_sections():
    """Test that the template contains all required sections"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_logs.md"

    content = template_file.read_text()

    required_sections = [
        "## Instructions",
        "### 1. Prompt Log Content",
        "### 2. Technical Debt Log Updates",
        "### 3. Current Project State Updates",
    ]

    for section in required_sections:
        assert section in content, f"Template must contain section: {section}"


def test_update_logs_template_has_correct_instructions():
    """Test that the template contains the correct instructions"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_logs.md"

    content = template_file.read_text()

    # Check for key instruction elements
    assert (
        "development session with the AI" in content
    ), "Template must mention AI development sessions"
    assert (
        "documentation/prompt_log.md" in content
    ), "Template must reference documentation/prompt_log.md"
    assert (
        "documentation/technical_debt_log.md" in content
    ), "Template must reference documentation/technical_debt_log.md"
    assert (
        "current_project_state.md" in content
    ), "Template must reference current_project_state.md"
    assert (
        "(Paste AI conversation here)" in content
    ), "Template must have placeholder for AI conversation"
    assert (
        '(Paste any identified technical debt here, or "N/A" if none)' in content
    ), "Template must have placeholder for technical debt"
    assert (
        '(Paste new content for current_project_state.md here, or "N/A" if no architectural changes)'
        in content
    ), "Template must have placeholder for project state"


def test_update_logs_template_has_proper_code_blocks():
    """Test that the template contains proper code block formatting"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_logs.md"

    content = template_file.read_text()

    # Check for proper code block formatting
    assert "```text" in content, "Template must contain text code blocks"
    assert (
        "````markdown" in content
    ), "Template must contain markdown code blocks with 4 backticks"


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
