# Public Archival & Academic Expansion Guide

This guide is for researchers, archivists, and academics using the Cognitive Archaeology Tribunal for public knowledge preservation and expansion.

## Philosophy

This project treats digital artifacts as **archaeological evidence** worthy of preservation, study, and public access. All data and analyses can be:

- ✅ Published to version control
- ✅ Shared for academic research
- ✅ Archived for long-term preservation
- ✅ Extended and remixed by others
- ✅ Used for creative abstractions

## Public Data Workflow

### 1. Data Collection & Ingestion

```bash
# Place public data in ingestion chambers
cp my-public-conversations.json ingestion/ai-exports/
cp my-bookmarks.html ingestion/bookmarks/

# Process data
./scripts/ingest_all.sh

# Results go to output/
```

### 2. Review & Curate

```bash
# Review generated analyses
cat output/ai-context/triage_report.txt
jq '.stats' output/bookmarks/*/web_bookmarks.json

# Add annotations or metadata
# Edit JSON files to add research notes
```

### 3. Commit to Repository

```bash
# All ingestion data and outputs are now tracked by git
git add ingestion/ output/
git commit -m "Add public dataset: [description]"
git push
```

### 4. Publish & Share

```bash
# Tag for archival purposes
git tag -a v1.0-public-dataset -m "Public release of cognitive archaeology dataset"
git push --tags

# Create GitHub release for DOI integration
# Use Zenodo or figshare for academic citation
```

## Use Cases

### Academic Research

**Digital Humanities**
- Analyze conversation patterns across AI interactions
- Study knowledge formation in human-AI collaboration
- Track conceptual evolution over time

**Information Science**
- Bookmark classification and organization patterns
- Personal knowledge management strategies
- Digital archaeology methodologies

**Cognitive Science**
- External cognition through digital artifacts
- Distributed cognitive systems
- Memory and knowledge externalization

### Archival Science

**Digital Preservation**
- Long-term storage of AI conversation histories
- Maintaining context and metadata
- Version control as archival strategy

**Personal Digital Archives**
- Life documentation and memorialization
- Knowledge transfer across generations
- Institutional memory preservation

### Creative & Artistic

**Data Art**
- Knowledge graph visualizations
- Conversation pattern art
- Digital archaeology as creative practice

**Narrative Construction**
- Story extraction from digital traces
- Timeline reconstruction
- Thematic analysis and synthesis

## Data Formats

All outputs are in **open, documented formats**:

### JSON (Primary)
```json
{
  "stats": { ... },
  "conversations": [ ... ],
  "timestamp": "2025-11-18T12:00:00Z"
}
```

### Knowledge Graphs (Cytoscape.js)
```json
{
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

### Text Reports
```
=== TRIAGE REPORT ===
Generated: 2025-11-18

Statistics:
- Total items: 42
- Categories: 7
...
```

## Academic Citation

### Citing This Tool

```bibtex
@software{cognitive_archaeology_tribunal_2025,
  title = {Cognitive Archaeology Tribunal},
  author = {[Your Name/Organization]},
  year = {2025},
  url = {https://github.com/ivi374forivi/cognitive-archaelogy-tribunal},
  version = {1.0}
}
```

### Citing Datasets

When publishing processed datasets:

```bibtex
@dataset{my_cognitive_archaeology_2025,
  title = {Cognitive Archaeology Dataset: [Description]},
  author = {[Your Name]},
  year = {2025},
  publisher = {GitHub/Zenodo/Figshare},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://github.com/ivi374forivi/cognitive-archaelogy-tribunal}
}
```

## Reproducibility

### Document Your Process

Create a `DATASET.md` in your fork:

```markdown
# Dataset: [Name]

## Collection Period
- Start: 2024-01-01
- End: 2025-11-18

## Sources
- AI Conversations: ChatGPT exports (N=152)
- Bookmarks: Chrome export (N=3,241)
- Archives: iCloud Drive scan (N=15,432 files)

## Processing
- Tool: Cognitive Archaeology Tribunal v1.0
- Date: 2025-11-18
- Commands: See scripts/processing_log.sh

## Outputs
- output/ai-context/
- output/bookmarks/
- output/archives/

## Notes
[Any filtering, cleaning, or curation performed]
```

### Version Everything

```bash
# Tag datasets with versions
git tag -a dataset-v1.0 -m "Initial public release"
git tag -a dataset-v1.1 -m "Added 2025 Q1 conversations"

# Track processing scripts
git add scripts/
git commit -m "Processing pipeline v1.0"
```

## Privacy & Ethics

### Public vs. Private Data

Even for public datasets, consider:

1. **Consent**: Do you have rights to publish?
2. **Sensitive Info**: Remove PII, credentials, private URLs
3. **Context**: Provide context for interpretation
4. **Attribution**: Credit sources where appropriate

### Sanitization Scripts

```bash
# Create sanitization workflow
./scripts/sanitize_for_public.sh

# Example: Remove private domains
jq 'del(.conversations[] | select(.source_file | contains("private")))' \
  output/ai-context/ai_conversations.json > public.json
```

## Integration with Academic Infrastructure

### Zenodo Integration

1. Connect GitHub repo to Zenodo
2. Create release
3. Zenodo auto-archives and generates DOI
4. Cite with DOI in papers

### OSF (Open Science Framework)

```bash
# Create OSF project
# Link GitHub repo
# Add documentation, preregistration
# Generate OSF DOI
```

### Institutional Repositories

Many universities accept:
- GitHub repository exports
- Dataset documentation
- Research data packages

Check your institution's data repository guidelines.

## Extending & Remixing

### Fork for Your Research

```bash
git clone https://github.com/ivi374forivi/cognitive-archaelogy-tribunal
cd cognitive-archaelogy-tribunal

# Create research branch
git checkout -b research/my-study

# Add your modifications
# Commit and publish
```

### Contributing Back

```bash
# If you develop new analyzers or features
git checkout -b feature/new-analyzer

# Develop, test, commit
git push origin feature/new-analyzer

# Create pull request
# Share improvements with community
```

## Example Public Datasets

### Template Structure

```
my-cognitive-archaeology-dataset/
├── README.md                    # Dataset overview
├── DATASET.md                   # Collection methodology
├── LICENSE                      # CC0, CC-BY, or similar
├── ingestion/                   # Source data
│   ├── ai-exports/
│   ├── bookmarks/
│   └── archives/
├── output/                      # Processed results
│   ├── ai-context/
│   ├── bookmarks/
│   └── archives/
└── docs/
    ├── methodology.md
    └── analysis.md
```

### Licenses for Public Data

**Recommended:**
- **CC0**: Public domain dedication
- **CC-BY-4.0**: Attribution required
- **ODbL**: Open Database License

**Add LICENSE file:**
```markdown
# License

This dataset is released under [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication].

You are free to:
- Copy, modify, distribute
- Use for any purpose, commercial or non-commercial
- Without asking permission

Attribution appreciated but not required.
```

## Publishing Workflows

### GitHub Pages

```bash
# Generate static site from results
./scripts/generate_site.sh

# Enable GitHub Pages in repo settings
# Access at: https://[username].github.io/cognitive-archaelogy-tribunal
```

### Academic Preprints

1. Analyze your data using the tribunal
2. Write paper using findings
3. Publish preprint (arXiv, OSF Preprints)
4. Link to GitHub repo with data + code
5. Cite dataset DOI

### Peer-Reviewed Publication

- Submit to journals accepting data papers
- Examples: Journal of Open Archaeology Data, Scientific Data
- Include tribunal results as supplementary materials
- Provide reproduction scripts

## Community & Collaboration

### Sharing Your Work

1. **Tag releases** with descriptive versions
2. **Write documentation** for your specific use case
3. **Create issues** for discussions
4. **Star the repo** to show support
5. **Share examples** of your analyses

### Collaborative Research

```bash
# Set up collaborative repo
git clone [this-repo]
git remote add upstream https://github.com/ivi374forivi/cognitive-archaelogy-tribunal

# Create shared branch
git checkout -b collaboration/project-name

# Team members contribute
# Regular syncs with upstream
```

## Long-Term Preservation

### Archival Strategies

1. **Git-based**: GitHub (with Zenodo backup)
2. **Academic**: Institutional repositories
3. **Public**: Internet Archive, Zenodo, figshare
4. **Distributed**: IPFS for decentralized storage

### Format Longevity

All outputs use **preservation-friendly formats**:
- ✅ JSON (RFC 8259 standard)
- ✅ Plain text (UTF-8)
- ✅ Markdown (CommonMark)
- ✅ HTML5

Avoid:
- ❌ Proprietary formats
- ❌ Binary-only formats
- ❌ Closed databases

## Questions?

- **Documentation**: See `docs/`
- **Issues**: Open GitHub issue
- **Contributions**: Submit pull request
- **Academic collaboration**: Create discussion thread

---

**Remember**: Every digital artifact tells a story. By preserving and sharing yours, you contribute to the collective understanding of human-AI cognitive ecosystems.

**Happy excavating! 🏛️**
