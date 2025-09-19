# Branch Protection Configuration Guide

This document provides step-by-step instructions for configuring branch protection rules for the main branch of the MultiBet repository.

## Overview

Branch protection rules ensure code quality and stability by preventing direct pushes to the main branch and enforcing a Pull Request-based workflow with required status checks.

## Required Branch Protection Rules

The following protection rules should be configured for the `main` branch:

### 1. Require a Pull Request Before Merging
- **Setting**: `Require a pull request before merging`
- **Purpose**: Prevents direct pushes to main branch
- **Configuration**: Enable this setting to ensure all changes go through the PR review process

### 2. Require Status Checks to Pass Before Merging
- **Setting**: `Require status checks to pass before merging`
- **Purpose**: Ensures all CI/CD checks pass before code can be merged
- **Required Status Checks**:
  - `Quality Checks & Tests`
  - `Security Audits`

### 3. Require Branches to be Up to Date Before Merging
- **Setting**: `Require branches to be up to date before merging`
- **Purpose**: Ensures PRs are based on the latest main branch code
- **Configuration**: Enable this setting to prevent integration issues

### 4. Do Not Allow Bypassing the Above Settings
- **Setting**: `Do not allow bypassing the above settings`
- **Purpose**: Enforces protection rules even for administrators
- **Configuration**: Enable this setting to ensure consistent enforcement

## Implementation Steps

### Step 1: Access Repository Settings
1. Navigate to the MultiBet repository on GitHub
2. Click on the "Settings" tab
3. Select "Branches" from the left sidebar

### Step 2: Add Branch Protection Rule
1. Click "Add rule" button
2. Enter `main` in the "Branch name pattern" field

### Step 3: Configure Protection Rules
1. Check "Require a pull request before merging"
   - Optionally set "Required number of reviews before merging" to 1 or more
   - Consider enabling "Dismiss stale PR approvals when new commits are pushed"

2. Check "Require status checks to pass before merging"
   - Check "Require branches to be up to date before merging"
   - In the status checks list, add the following required checks:
     - `Quality Checks & Tests`
     - `Security Audits`

3. Check "Restrict pushes that create files"
   - This prevents accidentally pushing large files or binaries

4. Check "Do not allow bypassing the above settings"
   - This ensures even administrators follow the protection rules

### Step 4: Save Configuration
1. Click "Create" to save the branch protection rule

## Verification

After implementing the branch protection rules, verify they work correctly by:

1. **Testing Direct Push Prevention**: Try to push directly to main (should be blocked)
2. **Testing PR Workflow**: Create a test PR and ensure all status checks run
3. **Testing Status Check Requirements**: Verify that PRs cannot be merged until all checks pass
4. **Testing Up-to-Date Requirement**: Verify that outdated branches cannot be merged

## Status Checks Overview

The CI/CD pipeline includes the following status checks:

| Status Check | Purpose | Failure Impact |
|-------------|---------|----------------|
| Quality Checks & Tests | Code quality validation with Ruff and automated testing with pytest | Blocks merge |
| Security Audits | Security vulnerability detection with Bandit and dependency vulnerability scanning with pip-audit | Blocks merge |

## Troubleshooting

### Common Issues

1. **Status checks not appearing**: Ensure the CI/CD workflow has run at least once on a PR
2. **Checks failing unexpectedly**: Review the GitHub Actions logs for detailed error information
3. **Unable to merge despite green checks**: Ensure the branch is up to date with main

### Contact

For issues with branch protection configuration, contact the repository administrator or create an issue in the repository.

## Maintenance

Review and update these protection rules periodically to ensure they continue to meet the project's security and quality requirements. Consider adding additional status checks as the project grows and new tools are introduced.