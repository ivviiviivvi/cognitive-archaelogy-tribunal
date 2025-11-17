# Cognitive Archaeology Tribunal

Comprehensive archaeological dig tool for multi-layer cognitive ecosystem. Audits previous chaos: all disparate sources: archives, AI conversations, personal repos, and org repos. Generates complete inventory, knowledge graph, and triage recommendations to transform scattered creative history into organized system foundation.

## 📚 Documentation

**New to this project?**
- 📖 **[Documentation Hub](docs/)** - Setup guides, user guides, and analysis reports
- 🎯 **[Quick Start](docs/guides/INTEGRATION_QUICK_START.md)** - Start integrating forks in 15 minutes
- 📋 **[Integration Queue](context/planning/INTEGRATION_QUEUE.md)** - Track 42 fork integrations
- 🔄 **[Current State](CONTEXTUAL_RELAY.md)** - Where we are and what's next

**Quick Links:**
- [Setup GitHub Token](docs/setup/GITHUB_TOKEN_SETUP.md)
- [Complete Ingestion Plan](context/planning/INGESTION_PLAN.md)
- [Repository Cleanup Plan](REPO_CLEANUP_PLAN.md)

## Features

### 🗂️ Module 1: Archive Scanner
- Scans iCloud, Dropbox, local drives, and network storage
- Intelligent file classification by type and purpose
- Advanced deduplication with hash-based detection
- Calculates potential space savings
- Identifies large, old, and unused files

### 🤖 Module 2: AI Context Aggregator
- Imports ChatGPT conversation exports
- Supports generic JSON conversation formats
- Extracts topics and conversation metadata
- Search and filter capabilities
- Timeline analysis of AI interactions

### 👤 Module 3: Personal Repo Analyzer
- Analyzes personal GitHub repositories
- Classifies forks vs. original repositories
- Tracks modifications in forked repos
- Identifies inactive and unmodified forks
- Activity and health metrics

### 🏢 Module 4: Org Repo Analyzer
- Analyzes organization repositories
- Status tracking (active, stale, abandoned, archived)
- Dependency detection and analysis
- Health scoring and recommendations
- Migration planning

## Outputs

The suite generates four comprehensive outputs:

1. **Unified Inventory (JSON)** - Complete catalog of all discovered assets
2. **Knowledge Graph** - Visual representation of relationships (JSON + Cytoscape format)
3. **Triage Report** - Prioritized action items with recommendations
4. **Migration Plans** - Strategic guidance for organization and cleanup

## Installation

```bash
# Clone the repository
git clone https://github.com/ivi374forivi/cognitive-archaelogy-tribunal.git
cd cognitive-archaelogy-tribunal

# Install dependencies
pip install -r requirements.txt

# Set up GitHub token (optional but recommended)
export GITHUB_TOKEN="your_github_token_here"
```

## Quick Start

### Run All Modules
```bash
python main.py \
  --scan-archives /path/to/archives \
  --ai-conversations /path/to/chatgpt/export \
  --personal-repos your-username \
  --org-repos your-org \
  --output-dir ./output
```

### Archive Scanner Only
```bash
python main.py --scan-archives /path/to/archives --output-dir ./output
```

### Personal Repos Only
```bash
python main.py --personal-repos your-username --output-dir ./output
```

### Organization Repos Only
```bash
python main.py --org-repos your-org --output-dir ./output
```

### AI Conversations Only
```bash
python main.py --ai-conversations /path/to/chatgpt/export --output-dir ./output
```

## Usage Examples

### Multiple Archive Locations
```bash
python main.py --scan-archives "/path/to/iCloud,/path/to/Dropbox,/path/to/local" --output-dir ./output
```

### With Custom GitHub Token
```bash
python main.py --personal-repos username --github-token ghp_yourtoken --output-dir ./output
```

### Skip Specific Outputs
```bash
python main.py --personal-repos username --no-graph --no-triage --output-dir ./output
```

## Output Files

After running, you'll find these files in your output directory:

- `inventory.json` - Unified inventory of all assets
- `knowledge_graph.json` - Knowledge graph data
- `knowledge_graph_cytoscape.json` - Graph in Cytoscape.js format
- `triage_report.json` - Structured triage recommendations
- `triage_report.txt` - Human-readable triage report
- `archives.json` - Detailed archive scan results
- `ai_conversations.json` - AI conversation analysis
- `personal_repos.json` - Personal repository analysis
- `org_repos.json` - Organization repository analysis

## Configuration

Copy `config.example.yaml` to `config.yaml` and customize:

```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

## API Usage

You can also use the modules programmatically:

```python
from cognitive_tribunal import (
    ArchiveScanner,
    AIContextAggregator,
    PersonalRepoAnalyzer,
    OrgRepoAnalyzer
)

# Scan archives
scanner = ArchiveScanner()
results = scanner.scan_directory('/path/to/archives')

# Analyze personal repos
analyzer = PersonalRepoAnalyzer(github_token='your_token')
repos = analyzer.analyze_user_repos('username')

# Get triage recommendations
triage = analyzer.generate_triage_report()
```

## Requirements

- Python 3.8+
- PyGithub (for GitHub API access)
- Other dependencies listed in `requirements.txt`

### Optional

- GitHub Personal Access Token for API access (higher rate limits)
- ChatGPT export data (for AI conversation analysis)

## ChatGPT Export Instructions

To export your ChatGPT conversations:

1. Go to ChatGPT settings
2. Navigate to "Data Controls"
3. Click "Export data"
4. Wait for the email with your data
5. Extract the ZIP file
6. Point the tool to the `conversations.json` file or directory

## Architecture

```
cognitive_tribunal/
├── modules/              # Core audit modules
│   ├── archive_scanner.py
│   ├── ai_context_aggregator.py
│   ├── personal_repo_analyzer.py
│   └── org_repo_analyzer.py
├── outputs/              # Output generators
│   ├── inventory.py
│   ├── knowledge_graph.py
│   └── triage_report.py
└── utils/                # Shared utilities
    ├── file_utils.py
    └── github_utils.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

Built for comprehensive digital archaeology and cognitive ecosystem organization.
