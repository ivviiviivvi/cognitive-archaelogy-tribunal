---
id: CAT-CONTRIB-001
title: "Contributing Guide"
version: 1.0.0
date: 2025-11-19
status: active
---

# Contributing to Cognitive Archaeology Tribunal

Thank you for your interest in contributing! This document provides guidelines for contributing code, documentation, datasets, and ideas.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Contributions](#code-contributions)
- [Dataset Contributions](#dataset-contributions)
- [Documentation Contributions](#documentation-contributions)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Style Guides](#style-guides)

---

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### 1. Code Contributions
- Fix bugs
- Implement new features
- Improve performance
- Add tests
- Enhance error handling

### 2. Dataset Contributions
- Publish your cognitive archaeology datasets
- Create example datasets
- Document use cases
- Share interesting findings

### 3. Documentation Contributions
- Improve existing docs
- Write tutorials
- Create video guides
- Translate documentation
- Fix typos

### 4. Community Contributions
- Answer questions in issues
- Help others in discussions
- Share your projects
- Write blog posts
- Give talks/presentations

---

## Development Setup

### Prerequisites

```bash
# Python 3.8+
python --version

# Git
git --version

# pip
pip --version
```

### Clone and Setup

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/cognitive-archaelogy-tribunal
cd cognitive-archaelogy-tribunal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # (if exists)

# Install pre-commit hooks (if configured)
pre-commit install
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cognitive_tribunal

# Run specific test file
pytest tests/test_ai_context_aggregator.py
```

---

## Code Contributions

### Workflow

1. **Create an Issue** (for significant changes)
   - Describe what you want to change
   - Discuss approach with maintainers
   - Get feedback before coding

2. **Fork & Branch**
   ```bash
   # Create a feature branch
   git checkout -b feature/your-feature-name

   # Or a bugfix branch
   git checkout -b fix/issue-123-description
   ```

3. **Write Code**
   - Follow style guides (see below)
   - Add/update tests
   - Update documentation
   - Add docstrings

4. **Test**
   ```bash
   # Run tests
   pytest

   # Check code style
   black cognitive_tribunal/
   flake8 cognitive_tribunal/

   # Type checking (if using mypy)
   mypy cognitive_tribunal/
   ```

5. **Commit**
   ```bash
   # Write clear commit messages
   git add .
   git commit -m "Add feature: brief description

   Longer explanation if needed.
   Fixes #123"
   ```

6. **Push & PR**
   ```bash
   # Push to your fork
   git push origin feature/your-feature-name

   # Create Pull Request on GitHub
   # Fill out the PR template
   ```

### Pull Request Requirements

- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] No merge conflicts
- [ ] Linked to related issue

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code follows style guide

## Related Issues
Fixes #123
Related to #456
```

---

## Dataset Contributions

### Publishing a Dataset

1. **Prepare Data**
   ```bash
   # Add data to ingestion chambers
   cp your-data.json ingestion/ai-exports/

   # Run processing
   ./scripts/ingest_all.sh

   # Check for sensitive info
   ./scripts/sanitize_for_public.sh
   ```

2. **Add Metadata**
   - Create DATASET.md with description
   - Add LICENSE-DATASET
   - Create CONSENT.md
   - Include citation information

3. **Submit**
   - Fork repository
   - Add your dataset
   - Create pull request
   - Maintainers will review

### Dataset Requirements

- [ ] No sensitive/private information
- [ ] LICENSE-DATASET file present
- [ ] CONSENT.md documenting permissions
- [ ] DATASET.md with metadata
- [ ] Proper attribution
- [ ] Example queries/use cases

---

## Documentation Contributions

### Types of Documentation

- **User Guides**: How to use features
- **Tutorials**: Step-by-step walkthroughs
- **API Documentation**: Function/class docs
- **Examples**: Working code examples
- **Case Studies**: Real-world usage

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots/visualizations
- Test all code examples
- Follow markdown lint rules

### Building Docs Locally

```bash
# If using Sphinx or similar
cd docs
make html

# View in browser
open _build/html/index.html
```

---

## Reporting Bugs

### Before Submitting

- Check existing issues
- Try latest version
- Collect system info

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.11.2]
- Tool Version: [e.g., 0.2.0]

## Additional Context
Logs, screenshots, etc.
```

---

## Suggesting Enhancements

### Enhancement Template

```markdown
## Feature Description
Brief description

## Use Case
Why is this needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches

## Additional Context
Mockups, examples, etc.
```

---

## Style Guides

### Python Code Style

**Formatter**: Black (line length 100)

```bash
black --line-length 100 cognitive_tribunal/
```

**Linter**: flake8

```bash
flake8 cognitive_tribunal/
```

**Key Points**:
- Use type hints
- Write docstrings (Google style)
- Follow PEP 8
- Keep functions focused
- Add comments for complex logic

**Example**:

```python
def analyze_conversations(
    export_path: str,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze AI conversation exports.

    Args:
        export_path: Path to conversation export file
        filters: Optional filters to apply

    Returns:
        Analysis results with stats and insights

    Raises:
        FileNotFoundError: If export_path doesn't exist
        ValueError: If export format is invalid
    """
    # Implementation
    pass
```

### Bash Script Style

**Linter**: shellcheck

```bash
shellcheck scripts/*.sh
```

**Key Points**:
- Use `set -e` for error handling
- Quote variables
- Add comments
- Include usage/help text
- Use meaningful variable names

### Markdown Style

**Linter**: markdownlint

**Key Points**:
- Use ATX-style headers (#)
- One sentence per line (optional)
- Code blocks with language tags
- Consistent list formatting

### Commit Message Style

**Format**:
```
type: brief description (50 chars max)

Longer explanation if needed (72 chars max per line).
Can include multiple paragraphs.

Fixes #123
Related to #456
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat: add browser tab analyzer module

Implements full BrowserTabAnalyzer class with tab group
analysis, temporal clustering, and domain categorization.

Fixes #42
```

```
fix: handle empty conversation files

Previously crashed on empty JSON files. Now returns
helpful error message.

Fixes #51
```

---

## Review Process

### What Happens After PR?

1. **Automated Checks** (if CI/CD configured)
   - Tests run
   - Linting checks
   - Coverage reports

2. **Maintainer Review**
   - Code quality
   - Test coverage
   - Documentation
   - Design decisions

3. **Feedback**
   - Requested changes
   - Questions
   - Suggestions

4. **Approval & Merge**
   - Once approved, will be merged
   - May be squashed into single commit

### Review Timeline

- Simple fixes: 1-2 days
- Features: 3-7 days
- Major changes: 1-2 weeks

---

## Getting Help

- **Questions**: Open a discussion
- **Bugs**: Open an issue
- **Chat**: (if Discord/Slack exists)
- **Email**: (if contact email exists)

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Thanked in release notes
- Credited in academic citations (for datasets)

---

## License

By contributing, you agree that your contributions will be licensed under the project's existing licenses:
- Code: MIT License
- Data: As specified in LICENSE-DATASET
- Documentation: CC-BY 4.0

---

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🙏

---

**Document ID**: CAT-CONTRIB-001
**Status**: Active
**Version**: 1.0.0
**Last Updated**: 2025-11-19

**See also**: [Code of Conduct](CODE_OF_CONDUCT.md) | [Governance](docs/GOVERNANCE.md) | [Roadmap](ROADMAP.md)
