#!/usr/bin/env python3
"""
Script to update project knowledge log when a PR with assigned issue is opened.

This script:
1. Checks if the opened PR includes a linked GitHub Issue in its body
2. Verifies that the issue is assigned to the founder (pcwilliams1258)
3. If both conditions are met, appends a formatted entry to PROMPT_LOG.md
"""

import os
import sys
import re
from datetime import datetime, timezone
from github import Github, GithubException


def extract_issue_numbers(pr_body):
    """Extract issue numbers from PR body using common linking patterns."""
    if not pr_body:
        return []
    
    # Common patterns for linking issues:
    # - Fixes #123, closes #123, resolves #123
    # - #123 (simple reference)
    # - https://github.com/owner/repo/issues/123
    patterns = [
        r'(?:fixes|closes|resolves)\s+#(\d+)',
        r'(?:fix|close|resolve)\s+#(\d+)',
        r'(?:^|\s)#(\d+)(?:\s|$)',
        r'github\.com/[^/]+/[^/]+/issues/(\d+)'
    ]
    
    issue_numbers = set()
    for pattern in patterns:
        matches = re.finditer(pattern, pr_body, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            issue_numbers.add(int(match.group(1)))
    
    return list(issue_numbers)


def check_issue_assignment(github_client, repo_name, issue_number, founder_username):
    """Check if an issue is assigned to the founder."""
    try:
        repo = github_client.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        
        # Check if issue is assigned to founder
        assignees = [assignee.login for assignee in issue.assignees]
        return founder_username in assignees, issue
    except GithubException as e:
        print(f"Error fetching issue #{issue_number}: {e}")
        return False, None


def append_to_prompt_log(issue, pr_number, log_file_path):
    """Append formatted entry to the prompt log file."""
    current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    entry = f"""
## Glass Box Task

**Issue:** [{issue.title}]({issue.html_url})
**PR:** #{pr_number}
**Date:** {current_date}

"""
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"Successfully appended entry for issue #{issue.number} to {log_file_path}")
        return True
    except Exception as e:
        print(f"Error writing to {log_file_path}: {e}")
        return False


def main():
    """Main function to process PR and update log if conditions are met."""
    # Get environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')
    pr_body = os.getenv('PR_BODY', '')
    founder_username = 'pcwilliams1258'
    log_file_path = 'project_knowledge/PROMPT_LOG.md'
    
    if not all([github_token, repo_name, pr_number]):
        print("Error: Missing required environment variables")
        print(f"GITHUB_TOKEN: {'✓' if github_token else '✗'}")
        print(f"GITHUB_REPOSITORY: {'✓' if repo_name else '✗'}")
        print(f"PR_NUMBER: {'✓' if pr_number else '✗'}")
        sys.exit(1)
    
    print(f"Processing PR #{pr_number} in repository {repo_name}")
    print(f"PR Body length: {len(pr_body)} characters")
    
    # Initialize GitHub client
    try:
        github_client = Github(github_token)
    except Exception as e:
        print(f"Error initializing GitHub client: {e}")
        sys.exit(1)
    
    # Extract issue numbers from PR body
    issue_numbers = extract_issue_numbers(pr_body)
    print(f"Found issue references: {issue_numbers}")
    
    if not issue_numbers:
        print("No linked issues found in PR body. No action needed.")
        return
    
    # Check each issue for assignment to founder
    updated = False
    for issue_number in issue_numbers:
        print(f"Checking issue #{issue_number}...")
        is_assigned, issue = check_issue_assignment(
            github_client, repo_name, issue_number, founder_username
        )
        
        if is_assigned and issue:
            print(f"Issue #{issue_number} is assigned to {founder_username}")
            if append_to_prompt_log(issue, pr_number, log_file_path):
                updated = True
            else:
                print(f"Failed to update log for issue #{issue_number}")
        else:
            print(f"Issue #{issue_number} is not assigned to {founder_username}")
    
    if updated:
        print("Prompt log updated successfully!")
    else:
        print("No updates made to prompt log.")


if __name__ == '__main__':
    main()