# AI Exports Ingestion Chamber

Drop your AI conversation exports here for processing.

## Supported Formats

### ChatGPT Export
**How to export:**
1. Go to ChatGPT settings (bottom left)
2. Navigate to "Data Controls"
3. Click "Export data"
4. Wait for email with download link
5. Download and extract ZIP file
6. Copy `conversations.json` here

**File structure:**
```json
[
  {
    "title": "Conversation Title",
    "create_time": 1234567890,
    "update_time": 1234567890,
    "mapping": {
      // Message tree structure
    }
  }
]
```

### Claude Export (Desktop/API)
**Format:** Individual JSON files or directory of JSON files

**Expected structure:**
```json
{
  "title": "Conversation Title",
  "messages": [
    {
      "role": "user",
      "content": "Message text"
    },
    {
      "role": "assistant",
      "content": "Response text"
    }
  ]
}
```

### Generic JSON Format
Any JSON file with conversations can be processed. Minimum required fields:
- `title` or conversation identifier
- `messages` array with message objects

## What to Place Here

✅ **Do place:**
- `conversations.json` from ChatGPT exports
- Individual conversation JSON files
- Directories containing multiple conversation JSON files
- Any `.json` file containing AI conversations

❌ **Don't place:**
- Non-JSON files
- Binary files
- Archive files (.zip, .tar.gz) - extract first
- Non-conversation data

## Organization Tips

**Recommended structure:**
```
ai-exports/
├── chatgpt-2025-11-18/
│   └── conversations.json
├── claude-conversations/
│   ├── conv-001.json
│   ├── conv-002.json
│   └── conv-003.json
└── other-ai/
    └── exported-chats.json
```

**Simple structure:**
```
ai-exports/
├── chatgpt-export-2025-11-18.json
├── claude-export-2025-11-18.json
└── gemini-conversations.json
```

## Processing

### Manual
```bash
# From project root
python main.py --ai-conversations ./ingestion/ai-exports --output-dir ./output/ai-context
```

### Using Script
```bash
# From project root
./scripts/ingest_ai.sh
```

## Output

Results are saved to `output/ai-context/`:
- `ai_conversations.json` - Full parsed data
- `inventory.json` - Unified inventory
- `knowledge_graph.json` - Relationship graph
- `triage_report.json` - Analysis and recommendations
- `triage_report.txt` - Human-readable report

## What Gets Analyzed

- **Statistics**: Total conversations, messages, date ranges
- **Topics**: Common themes extracted from titles
- **Timeline**: Conversation activity over time
- **Search**: Full-text search capabilities
- **Metadata**: Authors, timestamps, conversation lengths

## Example

### Place File
```bash
# After exporting from ChatGPT
cp ~/Downloads/chatgpt-export/conversations.json ./ingestion/ai-exports/
```

### Run Ingestion
```bash
./scripts/ingest_ai.sh
```

### View Results
```bash
cat output/ai-context/triage_report.txt
```

## Troubleshooting

**"No JSON files found"**
- Verify files have `.json` extension
- Check files aren't corrupted (open in text editor)
- Ensure you're in the right directory

**"Invalid JSON format"**
- ChatGPT exports should work out of the box
- For custom formats, ensure valid JSON syntax
- Check for BOM or encoding issues

**"Permission denied"**
- Ensure files are readable: `chmod 644 *.json`

## Privacy Note

- All processing is local - no data leaves your machine
- `output/` directory is gitignored
- Original export files are never modified
- Consider encrypting sensitive conversation data

## Next Steps

After processing:
1. Review `output/ai-context/triage_report.txt`
2. Search conversations for specific topics
3. Analyze conversation timeline
4. Extract knowledge into org systems

See [USAGE.md](../../USAGE.md) for advanced usage.
