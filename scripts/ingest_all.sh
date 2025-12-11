#!/usr/bin/env bash
#
# Complete Ingestion Script
# Processes all data from all ingestion chambers
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BOLD}${BLUE}================================${NC}"
echo -e "${BOLD}${BLUE}COGNITIVE ARCHAEOLOGY TRIBUNAL${NC}"
echo -e "${BOLD}${BLUE}Complete Ingestion${NC}"
echo -e "${BOLD}${BLUE}================================${NC}"
echo ""

# Track what will be processed
CHAMBERS_TO_PROCESS=()

# Check each chamber
echo "Scanning ingestion chambers..."
echo ""

# AI Exports
AI_JSON_COUNT=$(find "$PROJECT_ROOT/ingestion/ai-exports" -name "*.json" -type f 2>/dev/null | wc -l)
if [ "$AI_JSON_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} AI Exports: $AI_JSON_COUNT JSON files"
    CHAMBERS_TO_PROCESS+=("ai")
else
    echo -e "${YELLOW}○${NC} AI Exports: No files"
fi

# Archives
if [ -f "$PROJECT_ROOT/ingestion/archives/locations.txt" ]; then
    LOC_COUNT=$(grep -v '^#' "$PROJECT_ROOT/ingestion/archives/locations.txt" | grep -v '^$' | wc -l)
    echo -e "${GREEN}✓${NC} Archives: $LOC_COUNT locations configured"
    CHAMBERS_TO_PROCESS+=("archives")
else
    echo -e "${YELLOW}○${NC} Archives: No locations.txt"
fi

# Bookmarks
BM_HTML_COUNT=$(find "$PROJECT_ROOT/ingestion/bookmarks" -name "*.html" -type f 2>/dev/null | wc -l)
if [ "$BM_HTML_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Bookmarks: $BM_HTML_COUNT HTML files"
    CHAMBERS_TO_PROCESS+=("bookmarks")
else
    echo -e "${YELLOW}○${NC} Bookmarks: No files"
fi

# Browser Tabs
TABS_COUNT=$(find "$PROJECT_ROOT/ingestion/browser-tabs" \( -name "*.txt" -o -name "*.json" \) -type f 2>/dev/null | wc -l)
if [ "$TABS_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Browser Tabs: $TABS_COUNT files"
    CHAMBERS_TO_PROCESS+=("tabs")
else
    echo -e "${YELLOW}○${NC} Browser Tabs: No files"
fi

echo ""

# Check if anything to process
if [ ${#CHAMBERS_TO_PROCESS[@]} -eq 0 ]; then
    echo -e "${RED}No data found in any ingestion chamber${NC}"
    echo ""
    echo "Please add data to at least one chamber:"
    echo "  - ingestion/ai-exports/"
    echo "  - ingestion/archives/"
    echo "  - ingestion/bookmarks/"
    echo "  - ingestion/browser-tabs/"
    echo ""
    echo "See: ingestion/README.md for details"
    exit 1
fi

# Confirmation
echo "Ready to process ${#CHAMBERS_TO_PROCESS[@]} chamber(s): ${CHAMBERS_TO_PROCESS[*]}"
echo ""
read -p "Continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Starting Ingestion${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Track results
SUCCESS_COUNT=0
FAIL_COUNT=0
START_TIME=$(date +%s)

# Process each chamber
for CHAMBER in "${CHAMBERS_TO_PROCESS[@]}"; do
    echo ""
    echo -e "${BOLD}Processing: $CHAMBER${NC}"
    echo "----------------------------------------"

    SCRIPT="$SCRIPT_DIR/ingest_${CHAMBER}.sh"

    if [ -f "$SCRIPT" ]; then
        if bash "$SCRIPT"; then
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            echo -e "${GREEN}✓ $CHAMBER complete${NC}"
        else
            FAIL_COUNT=$((FAIL_COUNT + 1))
            echo -e "${RED}✗ $CHAMBER failed${NC}"
        fi
    else
        echo -e "${YELLOW}Warning: Script not found: $SCRIPT${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi

    echo ""
done

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

# Final summary
echo ""
echo -e "${BOLD}${BLUE}================================${NC}"
echo -e "${BOLD}${BLUE}INGESTION COMPLETE${NC}"
echo -e "${BOLD}${BLUE}================================${NC}"
echo ""
echo "Chambers processed: ${#CHAMBERS_TO_PROCESS[@]}"
echo -e "${GREEN}Success: $SUCCESS_COUNT${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}Failed: $FAIL_COUNT${NC}"
fi
echo "Duration: ${MINUTES}m ${SECONDS}s"
echo ""

# Show output structure
echo "Results saved to:"
for CHAMBER in "${CHAMBERS_TO_PROCESS[@]}"; do
    OUTPUT_DIR="$PROJECT_ROOT/output"
    case $CHAMBER in
        "ai") OUTPUT_DIR="$OUTPUT_DIR/ai-context" ;;
        "archives") OUTPUT_DIR="$OUTPUT_DIR/archives" ;;
        "bookmarks") OUTPUT_DIR="$OUTPUT_DIR/bookmarks" ;;
        "tabs") OUTPUT_DIR="$OUTPUT_DIR/browser-tabs" ;;
    esac

    if [ -d "$OUTPUT_DIR" ]; then
        FILE_COUNT=$(find "$OUTPUT_DIR" -type f | wc -l)
        echo "  - $OUTPUT_DIR ($FILE_COUNT files)"
    fi
done

echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "  1. Review triage reports: cat output/*/triage_report.txt"
echo "  2. Explore results: ls -lh output/*/"
echo "  3. Generate unified analysis (coming soon)"
echo ""

# Check if we should generate unified report
if [ ${#CHAMBERS_TO_PROCESS[@]} -gt 1 ]; then
    echo -e "${YELLOW}Tip: You processed multiple data sources!${NC}"
    echo "Consider running a unified analysis to see cross-layer insights."
    echo ""
fi
