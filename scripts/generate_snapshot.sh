#!/usr/bin/env bash
#
# Generate Cognitive Time Capsule Snapshot
# Creates a comprehensive snapshot of current cognitive state
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SNAPSHOT_DIR="$PROJECT_ROOT/snapshots"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SNAPSHOT_NAME="snapshot-$TIMESTAMP"
SNAPSHOT_PATH="$SNAPSHOT_DIR/$SNAPSHOT_NAME"

echo -e "${BOLD}${BLUE}================================${NC}"
echo -e "${BOLD}${BLUE}Cognitive Time Capsule${NC}"
echo -e "${BOLD}${BLUE}================================${NC}"
echo ""
echo "Creating snapshot: $SNAPSHOT_NAME"
echo ""

# Create snapshot directory
mkdir -p "$SNAPSHOT_PATH"

# 1. Copy current state
echo "📸 Capturing current state..."
echo ""

# Ingestion state
if [ -d "$PROJECT_ROOT/ingestion" ]; then
    echo "  ✓ Ingestion data"
    cp -r "$PROJECT_ROOT/ingestion" "$SNAPSHOT_PATH/"
fi

# Output state
if [ -d "$PROJECT_ROOT/output" ]; then
    echo "  ✓ Analysis outputs"
    cp -r "$PROJECT_ROOT/output" "$SNAPSHOT_PATH/"
fi

# 2. Generate summary statistics
echo ""
echo "📊 Generating statistics..."
echo ""

cat > "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
# Cognitive Time Capsule Snapshot

**Timestamp**: $(date +"%Y-%m-%d %H:%M:%S %Z")
**Snapshot ID**: $SNAPSHOT_NAME

---

## Overview

This snapshot captures the complete state of the cognitive archaeology system at a specific moment in time.

## Statistics

### AI Conversations
EOF

# AI stats
if [ -f "$SNAPSHOT_PATH/output/ai-context/ai_conversations.json" ]; then
    TOTAL_CONVS=$(jq '.stats.total_conversations // 0' "$SNAPSHOT_PATH/output/ai-context/ai_conversations.json")
    TOTAL_MSGS=$(jq '.stats.total_messages // 0' "$SNAPSHOT_PATH/output/ai-context/ai_conversations.json")

    cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
- **Total Conversations**: $TOTAL_CONVS
- **Total Messages**: $TOTAL_MSGS
- **Date Range**: $(jq -r '.stats.date_range.earliest // "N/A"' "$SNAPSHOT_PATH/output/ai-context/ai_conversations.json") to $(jq -r '.stats.date_range.latest // "N/A"' "$SNAPSHOT_PATH/output/ai-context/ai_conversations.json")

#### Top Topics
\`\`\`
$(jq -r '.conversations[].title' "$SNAPSHOT_PATH/output/ai-context/ai_conversations.json" 2>/dev/null | head -10 | nl || echo "No data")
\`\`\`
EOF
else
    cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
- No AI conversation data available
EOF
fi

# Bookmarks stats
cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF

### Bookmarks
EOF

BOOKMARK_FILES=$(find "$SNAPSHOT_PATH/output/bookmarks" -name "web_bookmarks.json" 2>/dev/null || true)
if [ ! -z "$BOOKMARK_FILES" ]; then
    TOTAL_BM=$(echo "$BOOKMARK_FILES" | xargs jq '.stats.total_bookmarks // 0' 2>/dev/null | awk '{sum+=$1} END {print sum}')
    cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
- **Total Bookmarks**: $TOTAL_BM

#### Top Domains
\`\`\`
$(echo "$BOOKMARK_FILES" | xargs jq -r '.bookmarks[].url' 2>/dev/null | sed 's|https\?://||' | cut -d/ -f1 | sort | uniq -c | sort -rn | head -10 || echo "No data")
\`\`\`
EOF
else
    cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
- No bookmark data available
EOF
fi

# Archive stats
cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF

### Archives
EOF

if [ -f "$SNAPSHOT_PATH/output/archives/archives.json" ]; then
    TOTAL_FILES=$(jq '.stats.total_files // 0' "$SNAPSHOT_PATH/output/archives/archives.json")
    TOTAL_SIZE=$(jq '.stats.total_size // 0' "$SNAPSHOT_PATH/output/archives/archives.json")
    TOTAL_SIZE_MB=$((TOTAL_SIZE / 1024 / 1024))

    cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
- **Total Files**: $TOTAL_FILES
- **Total Size**: ${TOTAL_SIZE_MB} MB

#### File Categories
\`\`\`
$(jq -r '.stats.by_category | to_entries[] | "\(.key): \(.value)"' "$SNAPSHOT_PATH/output/archives/archives.json" 2>/dev/null || echo "No data")
\`\`\`
EOF
else
    cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF
- No archive data available
EOF
fi

# 3. Add metadata
cat >> "$SNAPSHOT_PATH/SNAPSHOT.md" <<EOF

---

## Contents

\`\`\`
$(tree -L 2 "$SNAPSHOT_PATH" 2>/dev/null || find "$SNAPSHOT_PATH" -type d | head -20)
\`\`\`

---

## Manifest

\`\`\`
$(find "$SNAPSHOT_PATH" -type f | wc -l) total files
$(du -sh "$SNAPSHOT_PATH" | cut -f1) total size
\`\`\`

---

## Reflection Prompts

Use these prompts to reflect on this snapshot:

1. **Patterns**: What patterns do you notice in your conversations and bookmarks?
2. **Evolution**: How has your thinking evolved over the collection period?
3. **Surprises**: What unexpected connections or themes emerged?
4. **Gaps**: What areas are underrepresented in your digital archaeology?
5. **Future**: What would you like to explore or document next?

---

## Restoration

To restore this snapshot:

\`\`\`bash
# Copy snapshot back to main directories
cp -r $SNAPSHOT_NAME/ingestion/* ../ingestion/
cp -r $SNAPSHOT_NAME/output/* ../output/

# Or use as reference/comparison
diff -r $SNAPSHOT_NAME/output/ ../output/
\`\`\`

---

**Snapshot created**: $(date +%Y-%m-%d)
**Tool**: Cognitive Archaeology Tribunal
**Preservation format**: JSON, Markdown, Plain Text
EOF

# 4. Create archive
echo ""
echo "📦 Creating archive..."
cd "$SNAPSHOT_DIR"
tar -czf "${SNAPSHOT_NAME}.tar.gz" "$SNAPSHOT_NAME"
ARCHIVE_SIZE=$(du -h "${SNAPSHOT_NAME}.tar.gz" | cut -f1)
cd "$PROJECT_ROOT"

# 5. Summary
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Snapshot Complete${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Snapshot: $SNAPSHOT_PATH"
echo "Archive: $SNAPSHOT_DIR/${SNAPSHOT_NAME}.tar.gz ($ARCHIVE_SIZE)"
echo ""
echo "Contents:"
echo "  - SNAPSHOT.md (summary and statistics)"
echo "  - ingestion/ (source data)"
echo "  - output/ (analysis results)"
echo ""
echo "Next steps:"
echo "  1. Review SNAPSHOT.md"
echo "  2. Add personal reflections"
echo "  3. Archive for long-term preservation"
echo "  4. Compare with future snapshots"
echo ""
echo "View summary:"
echo "  cat $SNAPSHOT_PATH/SNAPSHOT.md"
echo ""
echo "Compare with current state:"
echo "  diff -r $SNAPSHOT_PATH/output/ output/"
echo ""
