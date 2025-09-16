# PROMPT_LOG.md

This document is the official log of all major development tasks completed using the "Glass Box" workflow with GitHub Copilot. It serves as a version-controlled history of the prompts used to generate features, as well as the validation steps taken.

---

## Template for New Entries

- **GitHub Issue:** (Link to the GitHub Issue, e.g., `https://github.com/your-org/your-repo/issues/123`)
- **Pull Request:** (Link to the Pull Request, e.g., `#145`)

**Final Prompt Chain:**
1. **Prompt 1:** (The initial prompt used to generate the core code for the feature.)
2. **Prompt 2 (Refinement):** (Any follow-up prompts used to refactor, add error handling, improve documentation, etc.)

**AI Explanation Summary:**  
(To be filled by founder after using `/explain` on the final code. A 1-2 sentence summary of the AI's explanation of the code's logic and purpose.)

**Validation Checklist:**
- [ ] Instructed Copilot to generate pytest unit tests based on the acceptance criteria in the issue.
- [ ] (Add specific test cases that were validated, e.g., Test case 1: Positive correlation.)
- [ ] Executed pytest in the terminal.
- [ ] All tests passed successfully before committing the code.

---

## Part 2: Scaffolding the Application and Core Engine

- **GitHub Issue:** (Link to Issue #1)
- **Pull Request:** (To be filled in upon creation)

**Final Prompt Chain:**
1. **Prompt 1 (Directory Structure):**  
   "Create a directory structure for a Python project. The root directory should contain a `src` directory. Inside `src`, create subdirectories: `core_engine`, `data_pipelines`, `models`, and `tests`. The root should also contain `config` and `data` directories."
2. **Prompt 2 (Version Control):**  
   "Initialize a new Git repository in the current root directory."
3. **Prompt 3 (Git Ignore):**  
   "Generate a standard `.gitignore` file suitable for a Python project."
4. **Prompt 4 (Dependencies):**  
   "Create a `requirements.txt` file in the root directory. Add: flask, pandas, numpy, redis, google-cloud-bigquery, scikit-learn, catboost, tensorflow, shap, requests, pydantic, pytest."

**AI Explanation Summary:**  
(N/A for file system setup)

**Validation Checklist:**
- [x] Verified that the `src`, `config`, and `data` directories were created correctly.
- [x] Verified that the subdirectories `core_engine`, `data_pipelines`, `models`, and `tests` exist inside `src`.
- [x] Confirmed that a `.gitignore` file was created with appropriate Python-related entries.
- [x] Confirmed that a `requirements.txt` file was created and contains all specified libraries.

---
