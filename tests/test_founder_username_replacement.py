import re
from pathlib import Path

def test_no_founder_username_references():
    repo_root = Path(".")
    patterns = ["*.md", "*.py", "*.yml", "*.yaml", "*.txt"]
    exclude_dirs = {".git", "node_modules", "__pycache__", ".pytest_cache"}
    exclude_files = {"test_founder_username_replacement.py"}
    founder_username_files = []

    for pattern in patterns:
        for file_path in repo_root.rglob(pattern):
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue
            if file_path.name in exclude_files:
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "founder-username" in content:
                        lines = content.split("\n")
                        line_numbers = [
                            i + 1
                            for i, line in enumerate(lines)
                            if "founder-username" in line
                        ]
                        founder_username_files.append(
                            {
                                "file": str(file_path.relative_to(repo_root)),
                                "lines": line_numbers,
                            }
                        )
            except (UnicodeDecodeError, PermissionError):
                continue
    assert (
        len(founder_username_files) == 0
    ), f"Found founder-username references in files: {founder_username_files}"

def test_pcwilliams1258_references_present():
    plan_file = Path("docs/PLAN.md")
    assert plan_file.exists(), "docs/PLAN.md file should exist"
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    pcwilliams_count = content.count("@pcwilliams1258")
    assert (
        pcwilliams_count == 16
    ), f"Expected 16 @pcwilliams1258 references, found {pcwilliams_count}"

def test_assignee_tracks_section_updated():
    plan_file = Path("docs/PLAN.md")
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert (
        "- **@pcwilliams1258**: Glass Box track" in content
    ), "Assignee Tracks section should reference @pcwilliams1258"
    assignee_section_start = content.find("## Assignee Tracks")
    if assignee_section_start != -1:
        assignee_section = content[assignee_section_start:]
        assert (
            "founder-username" not in assignee_section
        ), "Assignee Tracks section should not contain founder-username"

def test_specific_task_assignments():
    plan_file = Path("docs/PLAN.md")
    with open(plan_file, "r", encoding="utf-8") as f:
        content = f.read()
    critical_tasks = [
        "initialize a clean project environment",
        "define a core engine architecture", 
        "implement foundational quantitative logic",
        "architect a two-layer Feature Store",
        "engineer high-alpha sports features",
        "implement a correlation engine",
        "implement dynamic Fractional Kelly staking",
        "automate logging and calculation of Closing Line Value",
        "integrate SHAP for model explainability",
    ]
    for task in critical_tasks:
        pattern = rf".*{re.escape(task)}.*@pcwilliams1258.*"
        assert re.search(
            pattern, content, re.IGNORECASE
        ), f"Task '{task}' should be assigned to @pcwilliams1258"
