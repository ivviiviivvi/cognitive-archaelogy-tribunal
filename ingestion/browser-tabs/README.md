# Browser Tabs Ingestion Chamber

Drop browser tab/session exports here for analysis.

## Overview

This chamber processes open browser tabs and saved sessions to catalog and analyze your active browsing context.

**Status:** 🚧 **Experimental Feature**

The browser tab analyzer is a new module. Basic functionality works, but advanced features are in development.

## How to Export Tabs

### Method 1: OneTab Extension
**Recommended for simplicity**

1. Install OneTab extension
   - Chrome: [OneTab](https://chrome.google.com/webstore/detail/onetab/chphlpgkkbolifaimnlloiipkdnihall)
   - Firefox: [OneTab](https://addons.mozilla.org/en-US/firefox/addon/onetab/)

2. Click OneTab icon to save all tabs
3. Click "Export / Import URLs"
4. Copy to clipboard or download as text file
5. Save to this directory

**Output format (URL list):**
```
https://github.com/example/repo
https://stackoverflow.com/questions/12345
https://docs.python.org/3/
```

### Method 2: Session Buddy (Chrome)
1. Install [Session Buddy](https://chrome.google.com/webstore/detail/session-buddy/edacconmaakjimmfgnblocblbcdcpbko)
2. Open Session Buddy
3. Click "Export" for current session
4. Save JSON file to this directory

**Output format (JSON):**
```json
{
  "windows": [
    {
      "tabs": [
        {"url": "https://example.com", "title": "Example"}
      ]
    }
  ]
}
```

### Method 3: Tab Session Manager (Firefox)
1. Install [Tab Session Manager](https://addons.mozilla.org/en-US/firefox/addon/tab-session-manager/)
2. Open extension → Sessions
3. Right-click session → Export
4. Save JSON file to this directory

### Method 4: Manual Export
Create a simple text file with one URL per line:

```bash
cat > browser-tabs/my-tabs-2025-11-18.txt <<EOF
https://github.com/username/repo
https://docs.example.com
https://stackoverflow.com/questions/12345
EOF
```

## Supported Formats

### URL List (`.txt`)
```
https://example.com
https://github.com/user/repo
https://stackoverflow.com/questions/123
```

### JSON (`.json`)
```json
{
  "tabs": [
    {
      "url": "https://example.com",
      "title": "Example Site",
      "timestamp": "2025-11-18T12:00:00Z"
    }
  ]
}
```

### CSV (`.csv`)
```csv
url,title,timestamp
https://example.com,Example Site,2025-11-18
https://github.com/user/repo,GitHub Repo,2025-11-18
```

## What to Place Here

✅ **Do place:**
- OneTab exports (`.txt`)
- Session Buddy exports (`.json`)
- Tab Session Manager exports (`.json`)
- Manual URL lists (`.txt`)
- Tab group exports (`.json`)

❌ **Don't place:**
- Browser history files
- Browser cache
- Cookie files
- Profile directories

## Organization Tips

**Recommended structure:**
```
browser-tabs/
├── 2025-11-18-work-tabs.txt
├── 2025-11-18-research-tabs.txt
├── projects/
│   ├── project-a-tabs.json
│   └── project-b-tabs.json
└── archive/
    └── 2025-10-01-old-session.txt
```

## Processing

### Manual
```bash
# From project root
# Note: This feature requires the browser-tabs module (in development)
python main.py --browser-tabs ./ingestion/browser-tabs --output-dir ./output/browser-tabs
```

### Using Script
```bash
# From project root
./scripts/ingest_tabs.sh
```

## Output

Results saved to `output/browser-tabs/`:
- `browser_tabs.json` - Parsed tab data
- `inventory.json` - Unified inventory
- `knowledge_graph.json` - Domain relationships
- `triage_report.json` - Analysis and insights
- `triage_report.txt` - Human-readable report

## What Gets Analyzed

### Statistics
- Total tabs count
- Unique domains
- Domain frequency
- Tab groups (if available)

### Insights
- Most opened domains
- Domain categories (dev, docs, social, etc.)
- Tab age distribution
- Related tab clusters

### Recommendations
- Tabs to bookmark
- Tabs to close (duplicates)
- Tab organization suggestions
- Knowledge extraction opportunities

## Example Workflow

### 1. Export Tabs from OneTab
```bash
# OneTab → Export URLs → Copy
# Paste into file
pbpaste > ./ingestion/browser-tabs/tabs-2025-11-18.txt
```

### 2. Run Ingestion
```bash
./scripts/ingest_tabs.sh
```

### 3. Review Results
```bash
cat output/browser-tabs/triage_report.txt

# View domain frequency
jq '.stats.domain_frequency' output/browser-tabs/browser_tabs.json
```

## Use Cases

### 1. Research Session Capture
Save all tabs from a deep research session for later reference:
```bash
# Export tabs → save to ingestion/browser-tabs/research-topic-2025-11-18.txt
# Process to get organized list with metadata
```

### 2. Project Context Preservation
Capture all tabs related to a project:
```bash
# Save all tabs for Project X
# Creates permanent record of research context
# Can restore later or share with team
```

### 3. Tab Hoarding Analysis
Understand your tab usage patterns:
```bash
# Export all open tabs across all windows
# Analyze most common domains
# Identify tabs to bookmark vs. close
```

### 4. Knowledge Extraction
Extract valuable links from tab chaos:
```bash
# Export 100+ open tabs
# Analyze and categorize
# Convert to bookmarks or documentation
```

## Browser Extensions

### Recommended Tools

1. **OneTab** - Simple tab saving
   - Chrome/Firefox/Edge
   - Free
   - Export as URL list

2. **Session Buddy** - Advanced session management
   - Chrome
   - Free/Pro
   - JSON export

3. **Tab Session Manager** - Firefox session management
   - Firefox
   - Free
   - JSON export

4. **Toby** - Tab organization
   - Chrome
   - Free/Pro
   - Export capabilities

## Troubleshooting

**"No tabs found"**
- Verify file format (`.txt` or `.json`)
- Check file isn't empty
- Ensure valid URLs (start with `http://` or `https://`)

**"Invalid JSON"**
- Validate JSON syntax
- Check for trailing commas
- Verify file encoding (should be UTF-8)

**"Module not found"**
- Browser tabs module may still be in development
- Check if `cognitive_tribunal/modules/browser_tab_analyzer.py` exists
- Fall back to manual tab management

**"URLs not parsing"**
- Ensure one URL per line for `.txt` files
- Check for special characters or encoding issues
- Remove any headers or footers from export

## Privacy & Security

- 🔒 All processing is local
- 🔒 Tabs may contain sensitive URLs (work projects, personal accounts)
- 🔒 Output directory is gitignored
- 🔒 Be careful sharing tab exports

**Before sharing:**
- Review URLs for sensitive information
- Remove private/work-related URLs
- Consider domain-only anonymization

## Future Features

Planned enhancements:
- 🚧 Tab group preservation
- 🚧 Automatic categorization by domain type
- 🚧 Dead link detection
- 🚧 Duplicate tab identification
- 🚧 Tab age tracking
- 🚧 Browser history integration
- 🚧 Tab→Bookmark conversion

## Next Steps

After processing:
1. Review domain frequency analysis
2. Identify tabs to convert to bookmarks
3. Close duplicate or outdated tabs
4. Organize tabs into logical groups
5. Archive session for future reference

See [USAGE.md](../../USAGE.md) for advanced usage.

## Development Note

If you're a developer interested in contributing to the browser tabs module:
- Module location: `cognitive_tribunal/modules/browser_tab_analyzer.py` (to be created)
- Should follow pattern of other analyzers
- Support multiple input formats
- Extract meaningful insights from tab data

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.
