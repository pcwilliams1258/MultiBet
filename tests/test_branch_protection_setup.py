import sys
from pathlib import Path

def test_python_version():
    assert sys.version_info >= (3, 8), f"Python version {sys.version} is not supported"

def test_repository_structure():
    assert Path("src").exists(), "src directory must exist"
    assert Path(".github").exists(), ".github directory must exist"
    assert Path(".github/workflows").exists(), "workflows directory must exist"
    assert Path("docs").exists(), "docs directory must exist"
    assert Path("requirements.txt").exists(), "requirements.txt must exist"
    assert Path(".gitignore").exists(), ".gitignore must exist"

def test_ci_workflow_exists():
    ci_workflow = Path(".github/workflows/ci.yml")
    assert ci_workflow.exists(), "CI workflow file must exist"
    workflow_content = ci_workflow.read_text()
    required_jobs = [
        "lint-and-format",
        "test",
        "security-scan",
        "dependency-check",
        "documentation-check",
        "build-validation",
        "integration-status",
    ]
    for job in required_jobs:
        assert job in workflow_content, f"Required job '{job}' not found in CI workflow"

def test_branch_protection_documentation():
    doc_file = Path(".github/BRANCH_PROTECTION_SETUP.md")
    assert doc_file.exists(), "Branch protection documentation must exist"
    doc_content = doc_file.read_text()
    required_sections = [
        "Branch Protection Configuration Guide",
        "Require a Pull Request Before Merging",
        "Require Status Checks to Pass Before Merging",
        "Do Not Allow Bypassing the Above Settings",
        "Implementation Steps",
    ]
    for section in required_sections:
        assert section in doc_content, f"Required section '{section}' not found in documentation"

def test_requirements_file_format():
    requirements_file = Path("requirements.txt")
    assert requirements_file.exists(), "requirements.txt must exist"
    with open(requirements_file, "r") as f:
        lines = f.readlines()
    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            if line[0].isdigit() and "." in line:
                package = line.split(".", 1)[1] if "." in line else line
            else:
                package = line
            packages.append(package.strip())
    essential_packages = ["flask", "pandas", "numpy", "pytest"]
    for package in essential_packages:
        package_found = any(package.lower() in pkg.lower() for pkg in packages)
        assert package_found, f"Essential package '{package}' not found in requirements"

def test_src_directory_structure():
    src_dir = Path("src")
    assert src_dir.exists(), "src directory must exist"
    expected_dirs = ["core_engine", "data_pipelines", "models", "tests"]
    for expected_dir in expected_dirs:
        dir_path = src_dir / expected_dir
        assert dir_path.exists(), f"Expected directory '{expected_dir}' not found in src/"

def test_gitignore_includes_common_files():
    gitignore_file = Path(".gitignore")
    assert gitignore_file.exists(), ".gitignore file must exist"
    gitignore_content = gitignore_file.read_text()
    common_patterns = ["__pycache__", ".env", ".venv"]
    for pattern in common_patterns:
        assert pattern in gitignore_content, f"Pattern '{pattern}' should be in .gitignore"
    python_patterns = ["*.pyc", "*.py[cod]"]
    python_pattern_found = any(pattern in gitignore_content for pattern in python_patterns)
    assert python_pattern_found, "Python byte-compiled file patterns should be in .gitignore"

def test_documentation_completeness():
    docs_dir = Path("docs")
    assert docs_dir.exists(), "docs directory must exist"
    essential_docs = ["PLAN.md", "technical_specification.md"]
    for doc in essential_docs:
        doc_path = docs_dir / doc
        assert doc_path.exists(), f"Essential documentation '{doc}' not found"
        content = doc_path.read_text().strip()
        assert len(content) > 100, f"Documentation file '{doc}' appears to be too short or empty"

def test_workflow_trigger_configuration():
    ci_workflow = Path(".github/workflows/ci.yml")
    assert ci_workflow.exists(), "CI workflow must exist"
    workflow_content = ci_workflow.read_text()
    assert "on:" in workflow_content, "Workflow must have trigger configuration"
    assert "pull_request:" in workflow_content, "Workflow must trigger on pull requests"
    assert "branches: [ main ]" in workflow_content, "Workflow must trigger on main branch"
