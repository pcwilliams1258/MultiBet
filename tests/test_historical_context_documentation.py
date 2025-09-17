"""
Test suite to validate the historical_context.md documentation file.
This test ensures that the file exists and contains the required template structure.
"""

from pathlib import Path


def test_historical_context_file_exists():
    """Test that the historical_context.md file exists in the documentation directory"""
    repo_root = Path(__file__).parent.parent
    historical_context_file = repo_root / "documentation" / "historical_context.md"
    
    assert historical_context_file.exists(), "documentation/historical_context.md must exist"


def test_historical_context_has_required_sections():
    """Test that the file contains all required sections"""
    repo_root = Path(__file__).parent.parent
    historical_context_file = repo_root / "documentation" / "historical_context.md"
    
    content = historical_context_file.read_text()
    
    required_sections = [
        "# Historical Context & Decision Log",
        "## Template for New Entry",
        "## Log Entries"
    ]
    
    for section in required_sections:
        assert section in content, f"File must contain section: {section}"


def test_historical_context_has_template_structure():
    """Test that the file contains the template structure"""
    repo_root = Path(__file__).parent.parent
    historical_context_file = repo_root / "documentation" / "historical_context.md"
    
    content = historical_context_file.read_text()
    
    # Check for key template elements
    template_elements = [
        "### **Topic:** [Brief, Descriptive Title of the Conversation]",
        "- **Date:** YYYY-MM-DD",
        "- **Participants/Source:**",
        "#### **Summary of Discussion:**",
        "#### **Key Decisions & Rationale:**",
        "#### **Resulting Action Items / Code Snippets:**"
    ]
    
    for element in template_elements:
        assert element in content, f"Template must contain element: {element}"


def test_historical_context_has_code_block_example():
    """Test that the file contains a code block example in the template"""
    repo_root = Path(__file__).parent.parent
    historical_context_file = repo_root / "documentation" / "historical_context.md"
    
    content = historical_context_file.read_text()
    
    # Check for code block example
    assert "```python" in content, "Template must contain Python code block example"
    assert "# Paste relevant code snippet here if applicable" in content, "Template must contain code snippet placeholder"


def test_historical_context_has_proper_structure():
    """Test that the file has proper markdown structure and placeholder for new entries"""
    repo_root = Path(__file__).parent.parent
    historical_context_file = repo_root / "documentation" / "historical_context.md"
    
    content = historical_context_file.read_text()
    
    # Check for placeholder text
    assert "*(New entries should be added below this line)*" in content, "File must have placeholder for new entries"
    
    # Check for template instruction
    assert "Copy and paste the template below to add a new entry" in content, "File must contain template usage instructions"


if __name__ == "__main__":
    import pytest
    
    pytest.main([__file__, "-v"])