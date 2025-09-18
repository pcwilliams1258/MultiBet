---
name: Pull Request
about: Propose changes to the codebase
---

## Description
A brief description of the changes made in this PR and the problem it solves.

**Resolves:** #[issue_number]

---

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Chore (refactoring, dependency updates, etc.)

---

## ✅ PR Checklist

### 1. Task Completion
- [ ] **Issue Alignment**: This PR directly addresses all requirements in the linked issue.
- [ ] **Acceptance Criteria**: All acceptance criteria from the issue have been met and tested.

### 2. Quality Assurance
- [ ] **Local Checks**: I have run the `pre-commit` hooks locally and they pass. This ensures my code is formatted and linted correctly.
- [ ] **Unit Tests**: New and existing unit tests pass locally with my changes.
- [ ] **BDD Tests**: New Gherkin `.feature` files have been added and are passing.
- [ ] **Manual Validation**: I have manually verified that the changes work as expected.
- [ ] **CI/CD**: The CI pipeline is green.

### 3. Documentation
- [ ] **PLAN.md**: The status in `docs/PLAN.md` has been updated (e.g., from `📋 Planned` to `🔄 In Progress`).
- [ ] **Architectural Docs**: Any relevant architectural diagrams or documents have been updated.

### 4. AI-Assisted Development
- [ ] **Review**: I have reviewed all AI-generated code and take full responsibility for its correctness and quality.
- [ ] **Guidelines**: Changes are consistent with the best practices in `.github/copilot.md`.
- [ ] **Prompt Logging**: Key prompts and AI responses have been logged in an issue with the `documentation` label as per our process.

---

## Additional Notes
Add any other context, screenshots, or information about the pull request here.
