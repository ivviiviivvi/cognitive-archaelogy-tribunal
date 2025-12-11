#!/usr/bin/env bash
#
# AI Exports Ingestion Script
# Processes AI conversation exports from the ingestion chamber
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
INGESTION_DIR="$PROJECT_ROOT/ingestion/ai-exports"
OUTPUT_DIR="$PROJECT_ROOT/output/ai-context"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}AI Exports Ingestion${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if ingestion directory exists
if [ ! -d "$INGESTION_DIR" ]; then
    echo -e "${RED}Error: Ingestion directory not found: $INGESTION_DIR${NC}"
    exit 1
fi

# Check if there are any JSON files
JSON_COUNT=$(find "$INGESTION_DIR" -name "*.json" -type f | wc -l)
if [ "$JSON_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}Warning: No JSON files found in $INGESTION_DIR${NC}"
    echo ""
    echo "Please add AI conversation export files:"
    echo "  - ChatGPT: Export data from Settings → Data Controls"
    echo "  - Claude: Export conversation JSON files"
    echo "  - Other: Any JSON format conversation files"
    echo ""
    echo "See: ingestion/ai-exports/README.md for details"
    exit 1
fi

echo "📂 Ingestion chamber: $INGESTION_DIR"
echo "📊 Output directory: $OUTPUT_DIR"
echo "📄 JSON files found: $JSON_COUNT"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run the main script
echo -e "${GREEN}Running AI context aggregator...${NC}"
echo ""

cd "$PROJECT_ROOT"
python main.py \
    --ai-conversations "$INGESTION_DIR" \
    --output-dir "$OUTPUT_DIR" \
    --no-graph

# Check results
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✓ Ingestion Complete${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "Results saved to: $OUTPUT_DIR"
    echo ""

    if [ -f "$OUTPUT_DIR/triage_report.txt" ]; then
        echo "📋 Triage Report Preview:"
        echo "----------------------------------------"
        head -n 20 "$OUTPUT_DIR/triage_report.txt"
        echo "----------------------------------------"
        echo ""
        echo "Full report: $OUTPUT_DIR/triage_report.txt"
    fi

    echo ""
    echo "Generated files:"
    ls -lh "$OUTPUT_DIR" | grep -v "^d" | awk '{print "  - " $9 " (" $5 ")"}'
else
    echo ""
    echo -e "${RED}✗ Ingestion failed${NC}"
    echo "Check error messages above for details"
    exit 1
fi
