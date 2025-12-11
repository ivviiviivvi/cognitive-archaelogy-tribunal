# Bookmarks Ingestion Chamber

Drop browser bookmark export files here for analysis.

## How to Export Bookmarks

### Chrome / Chromium / Edge
1. Open Bookmark Manager (`Cmd+Shift+O` or `Ctrl+Shift+O`)
2. Click ⋮ (three dots) in top right
3. Select "Export bookmarks"
4. Save HTML file
5. Move to this directory

### Firefox
1. Open Library (`Cmd+Shift+B` or `Ctrl+Shift+B`)
2. Click "Import and Backup" → "Export Bookmarks to HTML"
3. Save file
4. Move to this directory

### Safari
1. Open Safari
2. File → Export Bookmarks
3. Save HTML file
4. Move to this directory

### Other Browsers
Most browsers support "Netscape Bookmark File Format" (HTML).
Check browser documentation for export options.

## Supported Formats

**Primary:** Netscape Bookmark File Format (`.html`)

This is the standard bookmark export format used by all major browsers.

**Format example:**
```html
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><A HREF="https://example.com/" ADD_DATE="1609459200">Example Site</A>
    <DT><A HREF="https://github.com/" ADD_DATE="1577836800">GitHub</A>
</DL>
```

## What to Place Here

✅ **Do place:**
- Browser bookmark export files (`.html`)
- Multiple export files from different browsers
- Historical bookmark exports for comparison

❌ **Don't place:**
- Browser profile directories
- Binary bookmark databases
- Non-HTML files

## Organization Tips

**Recommended structure:**
```
bookmarks/
├── chrome-bookmarks-2025-11-18.html
├── firefox-bookmarks-2025-11-18.html
├── safari-bookmarks-2025-11-18.html
└── archive/
    ├── chrome-bookmarks-2025-01-01.html
    └── firefox-bookmarks-2024-12-01.html
```

## Processing

### Manual
```bash
# From project root
python main.py --web-bookmarks ./ingestion/bookmarks --output-dir ./output/bookmarks
```

### Using Script
```bash
# From project root
./scripts/ingest_bookmarks.sh
```

The script will process all `.html` files in this directory.

## Output

Results saved to `output/bookmarks/`:
- `web_bookmarks.json` - Parsed bookmark data
- `inventory.json` - Unified inventory
- `triage_report.json` - Analysis and recommendations
- `triage_report.txt` - Human-readable report

## What Gets Analyzed

### Basic Stats
- Total bookmarks count
- Total folders count
- Creation date range
- Domain frequency

### Insights
- Most bookmarked domains
- Oldest bookmarks
- Recently added bookmarks
- Bookmark organization structure

### Recommendations
- Duplicate URL detection
- Dead link identification (future feature)
- Organization suggestions
- Cleanup opportunities

## Example Workflow

### 1. Export from Browser
```bash
# Chrome: Bookmark Manager → ⋮ → Export bookmarks
# Saves to Downloads as "bookmarks_MM_DD_YYYY.html"
```

### 2. Move to Ingestion Chamber
```bash
mv ~/Downloads/bookmarks_11_18_2025.html ./ingestion/bookmarks/
```

### 3. Run Ingestion
```bash
./scripts/ingest_bookmarks.sh
```

### 4. Review Results
```bash
cat output/bookmarks/triage_report.txt

# Or view JSON
jq '.stats' output/bookmarks/web_bookmarks.json
```

## Multiple Browser Analysis

Compare bookmarks across browsers:

```bash
# Export from each browser
mv ~/Downloads/chrome-bookmarks.html ./ingestion/bookmarks/
mv ~/Downloads/firefox-bookmarks.html ./ingestion/bookmarks/
mv ~/Downloads/safari-bookmarks.html ./ingestion/bookmarks/

# Process all
./scripts/ingest_bookmarks.sh

# Results will include all bookmarks from all files
```

## Advanced Usage

### Merge Bookmarks
The tool can help identify unique bookmarks across multiple exports:

1. Export from all browsers
2. Run ingestion
3. Review `web_bookmarks.json` for duplicates
4. Manually merge or use deduplication tools

### Bookmark Archaeology
Compare historical exports to see bookmark evolution:

```bash
bookmarks/
├── 2024-01-01-chrome.html
├── 2024-06-01-chrome.html
├── 2024-12-01-chrome.html
└── 2025-11-18-chrome.html
```

Process separately to see how your bookmarks changed over time.

## Troubleshooting

**"Not a valid Netscape Bookmark File"**
- Check file is actually HTML
- Open in text editor to verify format
- Re-export from browser if corrupted

**"No bookmarks found"**
- Verify HTML file contains `<A HREF=` tags
- Check file isn't empty
- Ensure export completed successfully

**"Encoding issues"**
- Most exports use UTF-8
- Try opening file and re-saving with UTF-8 encoding
- Check for special characters in bookmark names

**"Missing bookmarks"**
- Browser may export only specific folders
- Check browser export settings
- Verify all folders were selected during export

## Privacy Note

- All processing is local
- Original bookmark files are never modified
- `output/` directory is gitignored
- Consider removing sensitive URLs before sharing results

## Future Enhancements

Planned features:
- Dead link detection (HTTP check)
- Duplicate URL removal
- Bookmark similarity analysis
- Auto-categorization by domain type
- Tag extraction from titles
- Folder structure optimization

## Next Steps

After processing:
1. Review bookmark statistics
2. Identify duplicate URLs
3. Find most frequently bookmarked domains
4. Plan bookmark organization cleanup
5. Export curated lists for migration

See [USAGE.md](../../USAGE.md) for advanced usage.
