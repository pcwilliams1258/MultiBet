---
name: Development Task
about: A standard template for new features or development tasks.
title: "[TASK]: "
labels: 'development'
assignees: ''

---

## 📝 Task Overview

**Plan Reference:** `[Task ID from PLAN.md]`
_Example: `1.3`_

**User Story:**
> As a [user type], I want [goal] so that [benefit].

**Description:**
A clear and concise description of what the task is and what its goals are.

---

## 🎯 Acceptance Criteria & BDD

**Acceptance Criteria:**
A list of specific, testable criteria that must be met for this task to be considered complete.
- [ ] Criterion 1
- [ ] Criterion 2

**Behavior-Driven Development (BDD) Scenarios:**
Provide Gherkin-style scenarios that describe the expected behavior. This will be used to create `.feature` files for testing.

```gherkin
Feature: [Feature Name]

  Scenario: [Scenario Name]
    Given [some precondition]
    When [I perform some action]
    Then [I should see some result]
```

---

## Technical Context

**Target Files & Modules:**
List the primary files, classes, or modules that are expected to be modified or created. This helps focus the AI's attention.
- `src/module_name/file_name.py`
- `tests/test_file.py`

**Architectural Notes:**
Provide any additional context, links, or notes that might be helpful. Reference `docs/PLAN.md` and other architectural documents.

## Documentation

Before starting development, ensure you have reviewed the relevant project documentation:

- [ ] I have reviewed `current_project_state.md` to understand the current architecture and state of the application
- [ ] I have checked `documentation/technical_debt_log.md` to understand any existing technical debt that may impact this task

---

## ✅ Definition of Done

- [ ] **Code Complete:** All development work is finished.
- [ ] **Testing:** Gherkin feature files and unit tests are implemented and passing.
- [ ] **CI/CD:** All checks in the CI pipeline are green.
- [ ] **Documentation:** `docs/PLAN.md` is updated, and any architectural changes are logged.
- [ ] **Dry Run Mode:** The feature supports a "Dry Run" mode where applicable.