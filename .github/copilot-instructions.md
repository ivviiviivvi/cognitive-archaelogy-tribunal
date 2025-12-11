---
description: AI rules derived by SpecStory from the project AI interaction history
globs: *
---

## HEADERS

This file defines all project rules, coding standards, workflow guidelines, references, documentation structures, and best practices for the AI coding assistant. It is a living document, evolving with project needs and decisions.

## TECH STACK

*   Python 3.14.0 (as configured via Trunk)

## PROJECT DOCUMENTATION & CONTEXT SYSTEM

*   REPO_CLEANUP_PLAN.md

## CODING STANDARDS

*   **Markdown Linting:** Fenced code blocks should always have a language specified for syntax highlighting, accessibility, documentation quality, and CI/CD compliance. Use appropriate language identifiers like `bash`, `python`, `json`, `yaml`, `text`, or `markdown`. For directory structures, use `text`, `bash`, or `plaintext`.
*   **Python Imports:** Remove unused imports to keep code clean, improve performance, adhere to linting standards (PEP 8, flake8, pylint), and ease maintenance.
*   **Dot files/folders:** All config dot files/folders (`.venv`, `.trunk`, `.vscode`, `.github`, `.specstory`, `.history`) should be gitignored.

## DEBUGGING

*   **Markdown Linting:** When addressing markdown linting issues:
    *   Prioritize fixing missing code block languages.
    *   Address multiple blank lines.
    *   Correct spacing issues (lists, code blocks, list markers).
    *   Resolve heading issues (blank lines, duplicate content, top-level heading).
    *   Convert hard tabs to spaces.
*   **GitLens Launchpad:** If encountering issues, check GitHub authentication, pull request data, and extension settings. Try signing in to GitHub through GitLens, enabling the GitLens extension, or refreshing the connection.
*   **Local History Extension:** Local History should be disabled or configured with:
    *   Disabled
    *   0 days limit (no retention)
    *   0 save delay (no auto-save)
    *   Path to `` if it does activate
    If `` still regenerates, uninstall the extension entirely. Ensure `"local-history.enabled"` is set to `0` in VS Code settings to disable the extension.

## WORKFLOW & RELEASE RULES

## VS CODE SETTINGS

*   **files.exclude:** Use `files.exclude` in `settings.json` to hide configuration folders from view in the workspace explorer.

## GIT RULES

*   All configuration dot files/folders (`.venv`, `.trunk`, `.vscode`, `.github`, `.specstory`, `.history`) should be gitignored.