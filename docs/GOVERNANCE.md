---
id: GOV-FRAMEWORK-001
title: "Cognitive Archaeology Tribunal: Governance Framework"
version: 1.0.0
date: 2025-11-19
type: governance
status: active
license: CC-BY-4.0
tags: [governance, metadata, licensing, consent, standards]
---

# Governance Framework

**Effective Date**: 2025-11-19
**Version**: 1.0.0
**Status**: Active

This document defines the governance, standards, and policies for the Cognitive Archaeology Tribunal project and all datasets published using it.

---

## I. METADATA STANDARDS

### Required Metadata (All Outputs)

Every output JSON file MUST include:

```json
{
  "metadata": {
    "id": "uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "type": "ai-conversations|archives|bookmarks|browser-tabs|synthesis",
    "version": "1.0.0",
    "schema_version": "1.0.0",
    "created_at": "2025-11-19T12:00:00Z",
    "updated_at": "2025-11-19T12:00:00Z",
    "generator": {
      "tool": "cognitive-tribunal",
      "version": "0.2.0",
      "module": "AIContextAggregator"
    },
    "provenance": {
      "source_files": ["path/to/source1.json"],
      "processing_steps": ["load", "parse", "analyze"],
      "parameters": {}
    },
    "license": "CC0-1.0",
    "attribution": "Optional attribution text"
  },
  "data": {
    // Actual output data
  }
}
```

### Dublin Core Mapping

For academic compliance, include Dublin Core elements:

```json
{
  "dublin_core": {
    "dc:title": "Dataset Title",
    "dc:creator": "Author Name",
    "dc:subject": ["cognitive archaeology", "AI conversations"],
    "dc:description": "Description of the dataset",
    "dc:publisher": "Publisher Name",
    "dc:contributor": ["Contributor 1"],
    "dc:date": "2025-11-19",
    "dc:type": "Dataset",
    "dc:format": "application/json",
    "dc:identifier": "uuid:...",
    "dc:source": "https://github.com/...",
    "dc:language": "en",
    "dc:rights": "CC0-1.0",
    "dc:coverage": "Temporal: 2024-01 to 2025-11"
  }
}
```

### DataCite Schema (for DOI)

For DOI registration via Zenodo/figshare:

```json
{
  "datacite": {
    "identifier": "10.5281/zenodo.XXXXXXX",
    "identifierType": "DOI",
    "creators": [
      {"name": "Author, Name", "orcid": "0000-0000-0000-0000"}
    ],
    "titles": [
      {"title": "Dataset Title"}
    ],
    "publisher": "Zenodo",
    "publicationYear": "2025",
    "resourceType": "Dataset",
    "subjects": ["Cognitive Archaeology", "Digital Humanities"],
    "dates": [
      {"date": "2025-11-19", "dateType": "Created"}
    ],
    "version": "1.0.0",
    "rights": [
      {"rights": "CC0 1.0", "rightsURI": "https://creativecommons.org/publicdomain/zero/1.0/"}
    ]
  }
}
```

---

## II. UNIQUE IDENTIFIERS

### ID Format

All datasets, outputs, and snapshots MUST have UUIDs (RFC 4122):

**Format**: `uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Example**: `uuid:a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### ID Assignment

```python
import uuid
from datetime import datetime

def generate_id():
    return f"uuid:{uuid.uuid4()}"

def generate_metadata():
    return {
        "id": generate_id(),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "schema_version": "1.0.0"
    }
```

### ID Namespaces

- `CAT-DOC-XXX` - Documentation files
- `CAT-DATA-XXX` - Datasets
- `CAT-SNAP-XXX` - Snapshots
- `CAT-REL-XXX` - Releases
- `GOV-XXX` - Governance documents
- `ANALYSIS-XXX` - Analysis reports

---

## III. LICENSING

### Default License

**Default for Code**: MIT License
**Default for Data**: CC0 1.0 Universal (Public Domain)
**Default for Documentation**: CC-BY 4.0

### License Chooser Workflow

Before publishing, users MUST choose a license:

```bash
./scripts/choose_license.sh

# Options:
# 1. CC0 1.0 (Public Domain)
# 2. CC-BY 4.0 (Attribution Required)
# 3. CC-BY-SA 4.0 (Attribution + ShareAlike)
# 4. CC-BY-NC 4.0 (Attribution + Non-Commercial)
# 5. ODbL (Open Database License)
# 6. Custom
```

### License File Template

```markdown
# License

This dataset is released under [LICENSE NAME].

**License**: [SPDX Identifier]
**License URL**: [URL]

## Summary

[Human-readable summary of rights]

## Full Text

[Full license text or link]

## Attribution

If you use this dataset, please cite:

[Citation format]
```

### SPDX Headers

All code files should include:

```python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2025 Cognitive Archaeology Tribunal Contributors
```

---

## IV. CONSENT & PRIVACY

### Consent Manifest

Every public dataset MUST include `CONSENT.md`:

```markdown
# Consent Manifest

**Dataset ID**: uuid:...
**Dataset Name**: ...
**Publication Date**: 2025-11-19

## Data Sources

### AI Conversations
- [ ] All conversations are my own
- [ ] I have permission to publish shared conversations
- [ ] Sensitive information has been redacted

### Bookmarks
- [ ] All bookmarks are from my personal collection
- [ ] No proprietary/confidential URLs included
- [ ] Shared bookmark collections have permission

### Archives
- [ ] All files are my own or I have rights to publish
- [ ] No copyrighted materials without permission
- [ ] Personal information redacted

## Consent Statement

I, [NAME], affirm that:
1. I have the right to publish this data
2. I have obtained necessary permissions
3. I have redacted sensitive information
4. I release this data under [LICENSE]

**Signed**: [Name]
**Date**: 2025-11-19
```

### Privacy Checklist

Before publishing, verify:

- [ ] Run `./scripts/sanitize_for_public.sh`
- [ ] Manual review of all outputs
- [ ] No API keys, tokens, passwords
- [ ] No private email addresses
- [ ] No private URLs (localhost, .internal, .corp)
- [ ] No sensitive personal information
- [ ] No confidential business information
- [ ] Consent obtained for shared data
- [ ] LICENSE file present
- [ ] CONSENT.md completed

---

## V. VERSIONING

### Semantic Versioning

Datasets use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible schema changes
- **MINOR**: New data added (backward compatible)
- **PATCH**: Bug fixes, corrections

**Examples**:
- `1.0.0` - Initial release
- `1.1.0` - Added more conversations
- `1.1.1` - Fixed typos in metadata
- `2.0.0` - Changed JSON schema structure

### Version Tags

```bash
# Tag dataset versions
git tag -a dataset-v1.0.0 -m "Initial public release"
git tag -a dataset-v1.1.0 -m "Added Q4 2024 conversations"

# Push tags
git push --tags
```

### Version Metadata

```json
{
  "version": "1.1.0",
  "version_history": [
    {
      "version": "1.0.0",
      "date": "2025-11-01",
      "changes": "Initial release"
    },
    {
      "version": "1.1.0",
      "date": "2025-11-19",
      "changes": "Added 50 new conversations from Nov 2025"
    }
  ]
}
```

---

## VI. CITATION STANDARDS

### BibTeX Template

```bibtex
@dataset{${DATASET_ID},
  author = {${AUTHOR_NAME}},
  title = {${DATASET_TITLE}},
  year = {${YEAR}},
  publisher = {GitHub/Zenodo},
  version = {${VERSION}},
  doi = {${DOI}},
  url = {${URL}}
}
```

### APA Style

```
Author, A. A. (Year). Title of dataset (Version X.X) [Data set]. Publisher. https://doi.org/XX.XXXX/XXXXX
```

### Chicago Style

```
Author, First. Year. "Title of Dataset." Version X.X. Publisher. https://doi.org/XX.XXXX/XXXXX.
```

### Automated Citation Generation

```bash
./scripts/generate_citation.sh --format bibtex
./scripts/generate_citation.sh --format apa
./scripts/generate_citation.sh --format chicago
```

---

## VII. CONTRIBUTION GUIDELINES

### Adding Data

1. Fork repository
2. Add data to ingestion chambers
3. Run processing scripts
4. Review outputs for sensitive data
5. Add LICENSE and CONSENT.md
6. Create pull request

### Code Contributions

1. Fork repository
2. Create feature branch
3. Write tests
4. Ensure tests pass
5. Add documentation
6. Submit pull request

### Pull Request Requirements

- [ ] Tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] License headers present
- [ ] No sensitive data

### Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## VIII. DECISION-MAKING PROCESS

### Roles

- **Maintainers**: Can merge PRs, create releases
- **Contributors**: Can submit PRs
- **Users**: Can use tool, report issues

### Decision Process

1. **Minor changes**: Maintainer decision
2. **Major changes**: Discussion + consensus
3. **Breaking changes**: RFC process

### RFC Process

For major changes:

1. Create RFC document in `rfcs/`
2. Open discussion issue
3. Collect feedback (2 weeks)
4. Vote (maintainers)
5. Accept/Reject
6. Implement if accepted

---

## IX. QUALITY STANDARDS

### Documentation

All modules MUST have:
- Docstrings (Google style)
- README with examples
- Type hints
- Usage examples

### Testing

All modules MUST have:
- Unit tests (80%+ coverage)
- Integration tests
- Example data tests

### Code Style

- **Python**: Black formatter, flake8 linter
- **Bash**: shellcheck
- **Markdown**: markdownlint

---

## X. PUBLICATION PROCESS

### Pre-Publication Checklist

- [ ] Run `./scripts/sanitize_for_public.sh`
- [ ] Add LICENSE file
- [ ] Create CONSENT.md
- [ ] Add DATASET.md with metadata
- [ ] Generate MANIFEST.txt
- [ ] Create SHA256 checksums
- [ ] Tag version
- [ ] Test archive integrity

### Publication Platforms

**Recommended**:
1. **GitHub Releases** - Hosting + version control
2. **Zenodo** - DOI + long-term archival
3. **Figshare** - Academic visibility
4. **OSF** - Research projects
5. **Institutional Repository** - University archives

### Post-Publication

1. Update README with DOI
2. Add to dataset registry (if exists)
3. Announce on relevant channels
4. Monitor citations
5. Respond to issues/questions

---

## XI. AMENDMENTS

This governance framework may be amended through:

1. RFC process (for major changes)
2. Pull request (for minor clarifications)
3. Maintainer decision (for typos/formatting)

**Version History**:
- `1.0.0` (2025-11-19) - Initial governance framework

---

## XII. CONTACT & QUESTIONS

**Issues**: https://github.com/ivi374forivi/cognitive-archaelogy-tribunal/issues
**Discussions**: https://github.com/ivi374forivi/cognitive-archaelogy-tribunal/discussions

---

**Document ID**: GOV-FRAMEWORK-001
**Status**: Active
**License**: CC-BY-4.0
**Last Updated**: 2025-11-19
