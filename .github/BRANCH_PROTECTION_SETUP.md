# Branch Protection Configuration Guide

This document provides step-by-step instructions for configuring branch protection rules for the `main` branch, aligned with the repository's CI/CD strategy.

## Overview

Branch protection rules ensure code quality and stability by enforcing a pull request-based workflow with required status checks. This prevents direct pushes to `main` and guarantees all code is vetted by our automated pipeline.

## Required Status Checks

The new CI/CD pipeline consolidates all checks into two primary jobs. **These are the only two checks that must be set as required**:

1.  `Quality Checks & Tests`
2.  `Security Audits`

---

## Implementation Steps

### Step 1: Access Repository Settings
1.  Navigate to the MultiBet repository on GitHub.
2.  Click on the **Settings** tab.
3.  Select **Branches** from the left sidebar.

### Step 2: Add or Edit the Branch Protection Rule
1.  Click **Add rule** (or **Edit** next to the existing `main` rule).
2.  Ensure "Branch name pattern" is set to `main`.

### Step 3: Configure Protection Rules
1.  ✅ Enable **Require a pull request before merging**.
    -   Optionally, set "Require approvals" to `1`.
2.  ✅ Enable **Require status checks to pass before merging**.
    -   ✅ Enable **Require branches to be up to date before merging**.
    -   In the status checks search bar, search for and select **`Quality Checks & Tests`**.
    -   Search again and select **`Security Audits`**.
3.  ✅ Enable **Require linear history**.
4.  ✅ Enable **Include administrators**. This ensures no one can bypass the established quality process.

### Step 4: Save Configuration
1.  Click **Create** or **Save changes**.

---
## Verification

After configuration, you can verify the rules by:
-   Attempting to push directly to `main` (it should be blocked).
-   Opening a pull request and confirming that the "Merge" button is disabled until both `Quality Checks & Tests` and `Security Audits` have passed.
