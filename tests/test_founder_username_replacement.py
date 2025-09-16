"""
Test suite to validate that all founder-username references have been replaced with @pcwilliams1258.
This test ensures compliance with issue #48 requirements.
"""

import os
import re
from pathlib import Path


def test_no_founder_username_references():
    """Test that no founder-username references exist in repository files (excluding this test file)"""
    repo_root = Path(__file__).parent.parent
    
    # File patterns to check
    patterns = ["*.md", "*.py", "*.yml", "*.yaml", "*.txt"]
    
    # Directories to exclude from search
    exclude_dirs = {".git", "node_modules", "__pycache__", ".pytest_cache"}
    
    # Files to exclude (this test file itself)
    exclude_files = {"test_founder_username_replacement.py"}
    
    founder_username_files = []
    
    for pattern in patterns:
        for file_path in repo_root.rglob(pattern):
            # Skip excluded directories
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue
                
            # Skip excluded files
            if file_path.name in exclude_files:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "founder-username" in content:
                        # Find line numbers with founder-username
                        lines = content.split('\n')
                        line_numbers = [i + 1 for i, line in enumerate(lines) if "founder-username" in line]
                        founder_username_files.append({
                            'file': str(file_path.relative_to(repo_root)),
                            'lines': line_numbers
                        })
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files we can't read
                continue
    
    assert len(founder_username_files) == 0, f"Found founder-username references in files: {founder_username_files}"


def test_pcwilliams1258_references_present():
    """Test that @pcwilliams1258 references are present in docs/PLAN.md"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    assert plan_file.exists(), "docs/PLAN.md file should exist"
    
    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count @pcwilliams1258 references
    pcwilliams_count = content.count("@pcwilliams1258")
    
    # Should have exactly 14 references based on the original founder-username count
    assert pcwilliams_count == 14, f"Expected 14 @pcwilliams1258 references, found {pcwilliams_count}"


def test_assignee_tracks_section_updated():
    """Test that the Assignee Tracks section has been updated correctly"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that the Assignee Tracks section contains the correct reference
    assert "- **@pcwilliams1258**: Glass Box track" in content, \
        "Assignee Tracks section should reference @pcwilliams1258"
    
    # Ensure no founder-username in Assignee Tracks section
    assignee_section_start = content.find("## Assignee Tracks")
    if assignee_section_start != -1:
        assignee_section = content[assignee_section_start:]
        assert "founder-username" not in assignee_section, \
            "Assignee Tracks section should not contain founder-username"


def test_specific_task_assignments():
    """Test that specific high-priority tasks are assigned to @pcwilliams1258"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test some critical tasks are assigned to @pcwilliams1258
    critical_tasks = [
        "Implement quantitative correlation engine",
        "Implement dynamic Fractional Kelly staking", 
        "Automate Closing Line Value (CLV) Logging",
        "Integrate SHAP for Model Explainability"
    ]
    
    for task in critical_tasks:
        # Use regex to find task lines that should be assigned to @pcwilliams1258
        pattern = rf".*{re.escape(task)}.*@pcwilliams1258.*"
        assert re.search(pattern, content, re.IGNORECASE), \
            f"Task '{task}' should be assigned to @pcwilliams1258"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])