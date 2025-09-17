---
name: ✍️ Update Logs & Docs
about: Use this template to log AI conversations and update key documents.
title: 'LOG: [Brief description of changes]'
labels: 'documentation'
assignees: ''
---

## Instructions

After a development session with the AI, paste the relevant outputs into the sections below. This issue will serve as the single source of truth for updating the repository's key operational documents.

---

### 1. Prompt Log Content

Paste the full, chronological transcript of the significant prompts and AI responses from your development session here. This will be appended to `documentation/prompt_log.md`.

```text
(Paste AI conversation here)
```

---

### 2. Technical Debt Log Updates

Paste any new technical debt identified during your AI interrogation. Clearly state the issue, the reason for the debt, and the recommended fix. This will be used to create new entries in `documentation/technical_debt_log.md`.

```text
(Paste any identified technical debt here, or "N/A" if none)
```

---

### 3. Current Project State Updates

Paste the AI-generated summary of the project's new state. This content will be used to **overwrite** the `current_project_state.md` file.

````markdown
(Paste new content for current_project_state.md here, or "N/A" if no architectural changes)
````