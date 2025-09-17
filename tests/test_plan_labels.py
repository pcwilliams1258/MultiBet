"""
Test suite to validate that Labels column and Label Reference section have been added to docs/PLAN.md.
This test ensures compliance with issue #75 requirements.
"""

import re
from pathlib import Path


def test_labels_column_in_all_tables():
    """Test that all task tables in PLAN.md include a Labels column and Track column"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    assert plan_file.exists(), "docs/PLAN.md file should exist"
    
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all table headers that should have a Labels column and Track column
    table_headers = re.findall(r'\| Task ID \| User Story \| GitHub Issue \| Status \| Priority \| Assignee \|.*?\|.*?\|', content)
    
    # Should have 6 tables (5 phases + 1 epic + 1 infrastructure)
    assert len(table_headers) >= 6, f"Expected at least 6 task tables, found {len(table_headers)}"
    
    # Check that all tables have Labels column and Track column
    for header in table_headers:
        assert "Labels" in header, f"Table header should include Labels column: {header}"
        assert "Track" in header, f"Table header should include Track column: {header}"


def test_label_reference_section_exists():
    """Test that Label Reference section exists at the end of PLAN.md"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for Label Reference section
    assert "## Label Reference" in content, "Label Reference section should exist"
    
    # Check for subsections
    assert "### By Type of Work" in content, "By Type of Work subsection should exist"
    assert "### By Project Component" in content, "By Project Component subsection should exist"
    assert "### By Epic" in content, "By Epic subsection should exist"


def test_label_reference_content():
    """Test that Label Reference section contains expected labels"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Expected labels by category
    work_type_labels = ["enhancement", "bug", "documentation", "testing", "refactor", "project-management"]
    component_labels = ["core-engine", "quantitative-modeling", "data-pipeline", "architecture", "ml-models", "mle-ops", "ci-cd"]
    epic_labels = ["epic-1", "epic-2", "epic-3", "epic-4", "epic-5", "epic-6", "infra"]
    
    # Check that all expected labels are present
    for label in work_type_labels:
        assert f"`{label}`" in content, f"Work type label '{label}' should be present"
    
    for label in component_labels:
        assert f"`{label}`" in content, f"Component label '{label}' should be present"
    
    for label in epic_labels:
        assert f"`{label}`" in content, f"Epic label '{label}' should be present"


def test_existing_tasks_have_labels():
    """Test that existing tasks have been populated with appropriate labels and track information"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check that task rows have labels and track info (look for rows that have all table elements including track and labels)
    task_rows = re.findall(r'\| \d+\.\d+ \|.*?\|.*?\|.*?\|.*?\|.*?\| .+ \| .+ \|', content)
    task_rows.extend(re.findall(r'\| \d+\.\d+-\d+\.\d+ \|.*?\|.*?\|.*?\|.*?\|.*?\| .+ \| .+ \|', content))
    task_rows.extend(re.findall(r'\| INFRA-\d+ \|.*?\|.*?\|.*?\|.*?\|.*?\| .+ \| .+ \|', content))
    
    # Should have multiple tasks with labels and track info
    assert len(task_rows) >= 10, f"Expected at least 10 tasks with track and labels, found {len(task_rows)}"
    
    # Check that no task has empty labels or track (| |)
    for row in task_rows:
        parts = row.split("|")
        # Should have at least 8 parts (including empty strings at start/end)
        assert len(parts) >= 8, f"Task should have track and labels: {row}"


def test_track_assignments():
    """Test that track assignments match assignee expectations"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Tasks assigned to @pcwilliams1258 should be Glass Box
    pcwilliams_tasks = re.findall(r'\|.*?\| @pcwilliams1258 \| ([^|]+) \|.*?\|', content)
    for track in pcwilliams_tasks:
        assert "Glass Box" in track.strip(), f"@pcwilliams1258 tasks should be Glass Box track, found: {track}"
    
    # Tasks assigned to @copilot should be Delegated
    copilot_tasks = re.findall(r'\|.*?\| @copilot \| ([^|]+) \|.*?\|', content)
    for track in copilot_tasks:
        assert "Delegated" in track.strip(), f"@copilot tasks should be Delegated track, found: {track}"


def test_last_reviewed_date_updated():
    """Test that the Last Reviewed date has been updated"""
    plan_file = Path(__file__).parent.parent / "docs" / "PLAN.md"
    
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check that Last Reviewed date is present and recent
    assert "**Last Reviewed:" in content, "Last Reviewed date should be present"
    
    # Check that it's not the old date
    assert "2025-09-17" not in content or "2025-01-16" in content, "Last Reviewed date should be updated from 2025-09-17"


if __name__ == "__main__":
    import pytest
    
    pytest.main([__file__, "-v"])