"""
Test suite to validate the update_prompt_log.md issue template.
This test ensures that the template file exists and contains the required content.
"""

from pathlib import Path


def test_update_prompt_log_template_exists():
    """Test that the update_prompt_log.md issue template file exists"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_prompt_log.md"
    
    assert template_file.exists(), "update_prompt_log.md issue template must exist"


def test_update_prompt_log_template_has_correct_frontmatter():
    """Test that the template has the correct YAML frontmatter"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_prompt_log.md"
    
    content = template_file.read_text()
    
    # Check for proper YAML frontmatter
    assert content.startswith("---"), "Template must start with YAML frontmatter"
    assert "name: ✍️ Update Prompt Log" in content, "Template must have correct name"
    assert "about: Use this template to add the AI-generated explanation summary to the prompt log." in content, "Template must have correct about description"
    assert "title: 'docs: Update prompt log with AI explanation'" in content, "Template must have correct default title"
    assert "labels: documentation, enhancement" in content, "Template must have correct labels"


def test_update_prompt_log_template_has_required_sections():
    """Test that the template contains all required sections"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_prompt_log.md"
    
    content = template_file.read_text()
    
    required_sections = [
        "### Instructions for Founder",
        "### 📋 AI Explanation Output",
        "### 🔗 Link to Log Entry",
        "### 🤖 Instructions for Coding Agent"
    ]
    
    for section in required_sections:
        assert section in content, f"Template must contain section: {section}"


def test_update_prompt_log_template_has_correct_instructions():
    """Test that the template contains the correct instructions"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_prompt_log.md"
    
    content = template_file.read_text()
    
    # Check for key instruction elements
    assert "/explain` command" in content, "Template must mention the /explain command"
    assert "PROMPT_LOG.md" in content, "Template must reference PROMPT_LOG.md"
    assert "(To be filled by founder...)" in content, "Template must reference the placeholder text to replace"
    assert "1-2 sentence summary" in content, "Template must specify summary length"
    assert "docs: Update prompt log with AI explanation" in content, "Template must specify PR title"


def test_update_prompt_log_template_links_to_correct_file():
    """Test that the template links to the correct PROMPT_LOG.md file"""
    repo_root = Path(__file__).parent.parent
    template_file = repo_root / ".github" / "ISSUE_TEMPLATE" / "update_prompt_log.md"
    
    content = template_file.read_text()
    
    # Check for correct GitHub link to PROMPT_LOG.md
    expected_link = "https://github.com/pcwilliams1258/MultiBet/blob/main/docs/PROMPT_LOG.md"
    assert expected_link in content, f"Template must link to {expected_link}"


if __name__ == "__main__":
    import pytest
    
    pytest.main([__file__, "-v"])