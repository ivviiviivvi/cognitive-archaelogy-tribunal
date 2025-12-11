#!/usr/bin/env bash
#
# Bookmarks Ingestion Script
# Processes browser bookmark exports from the ingestion chamber
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Directories
INGESTION_DIR="$PROJECT_ROOT/ingestion/bookmarks"
OUTPUT_BASE="$PROJECT_ROOT/output/bookmarks"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Bookmarks Ingestion${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if ingestion directory exists
if [ ! -d "$INGESTION_DIR" ]; then
    echo -e "${RED}Error: Ingestion directory not found: $INGESTION_DIR${NC}"
    exit 1
fi

# Find all HTML files
HTML_FILES=($(find "$INGESTION_DIR" -name "*.html" -type f))

if [ ${#HTML_FILES[@]} -eq 0 ]; then
    echo -e "${YELLOW}Warning: No HTML files found in $INGESTION_DIR${NC}"
    echo ""
    echo "Please add browser bookmark export files:"
    echo "  - Chrome: Bookmark Manager → ⋮ → Export bookmarks"
    echo "  - Firefox: Library → Import & Backup → Export"
    echo "  - Safari: File → Export Bookmarks"
    echo ""
    echo "See: ingestion/bookmarks/README.md for details"
    exit 1
fi

echo "📂 Ingestion chamber: $INGESTION_DIR"
echo "📄 HTML files found: ${#HTML_FILES[@]}"
echo ""

# Process each HTML file
SUCCESS_COUNT=0
FAIL_COUNT=0

for HTML_FILE in "${HTML_FILES[@]}"; do
    FILENAME=$(basename "$HTML_FILE" .html)
    OUTPUT_DIR="$OUTPUT_BASE/$FILENAME"

    echo "----------------------------------------"
    echo "Processing: $(basename "$HTML_FILE")"
    echo "----------------------------------------"

    # Create output directory
    mkdir -p "$OUTPUT_DIR"

    # Run the main script
    cd "$PROJECT_ROOT"
    if python main.py \
        --web-bookmarks "$HTML_FILE" \
        --output-dir "$OUTPUT_DIR" \
        --no-graph \
        --no-triage; then

        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo -e "${GREEN}✓ Success${NC}"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo -e "${RED}✗ Failed${NC}"
    fi
    echo ""
done

# Summary
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Ingestion Summary${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Processed: ${#HTML_FILES[@]} files"
echo -e "${GREEN}Success: $SUCCESS_COUNT${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}Failed: $FAIL_COUNT${NC}"
fi
echo ""
echo "Results saved to: $OUTPUT_BASE"
echo ""

# Show all output directories
echo "Generated outputs:"
ls -d "$OUTPUT_BASE"/*/ 2>/dev/null | while read -r dir; do
    DIRNAME=$(basename "$dir")
    FILE_COUNT=$(ls -1 "$dir" | wc -l)
    echo "  - $DIRNAME ($FILE_COUNT files)"
done

# Combine stats if multiple files processed
if [ ${#HTML_FILES[@]} -gt 1 ]; then
    echo ""
    echo -e "${YELLOW}Tip: View individual reports in each subdirectory${NC}"
    echo "Example: cat $OUTPUT_BASE/*/web_bookmarks.json | jq '.stats'"
fi
