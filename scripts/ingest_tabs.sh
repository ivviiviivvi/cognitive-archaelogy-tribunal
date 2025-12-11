#!/usr/bin/env bash
#
# Browser Tabs Ingestion Script
# Processes browser tab exports from the ingestion chamber
#
# Note: This feature is experimental and may require additional module development
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Directories
INGESTION_DIR="$PROJECT_ROOT/ingestion/browser-tabs"
OUTPUT_DIR="$PROJECT_ROOT/output/browser-tabs"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Browser Tabs Ingestion${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo -e "${YELLOW}⚠️  Experimental Feature${NC}"
echo ""

# Check if ingestion directory exists
if [ ! -d "$INGESTION_DIR" ]; then
    echo -e "${RED}Error: Ingestion directory not found: $INGESTION_DIR${NC}"
    exit 1
fi

# Find supported files
TXT_COUNT=$(find "$INGESTION_DIR" -name "*.txt" -type f | wc -l)
JSON_COUNT=$(find "$INGESTION_DIR" -name "*.json" -type f | wc -l)
TOTAL_COUNT=$((TXT_COUNT + JSON_COUNT))

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}Warning: No tab export files found in $INGESTION_DIR${NC}"
    echo ""
    echo "Please add browser tab export files:"
    echo "  - OneTab: Export URLs (saves as .txt)"
    echo "  - Session Buddy: Export session (saves as .json)"
    echo "  - Manual: Create .txt file with one URL per line"
    echo ""
    echo "See: ingestion/browser-tabs/README.md for details"
    exit 1
fi

echo "📂 Ingestion chamber: $INGESTION_DIR"
echo "📄 Files found: $TOTAL_COUNT (.txt: $TXT_COUNT, .json: $JSON_COUNT)"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if browser tab analyzer module exists
MODULE_PATH="$PROJECT_ROOT/cognitive_tribunal/modules/browser_tab_analyzer.py"

if [ ! -f "$MODULE_PATH" ]; then
    echo -e "${YELLOW}================================${NC}"
    echo -e "${YELLOW}Module Not Yet Implemented${NC}"
    echo -e "${YELLOW}================================${NC}"
    echo ""
    echo "The browser tab analyzer module is still in development."
    echo ""
    echo "As a workaround, we'll create a basic analysis:"
    echo ""

    # Create basic analysis script
    cat > "$OUTPUT_DIR/analyze_tabs.py" <<'EOF'
#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse

def analyze_url_file(file_path):
    """Analyze a simple URL list file."""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('http'):
                urls.append(line)
    return urls

def analyze_json_file(file_path):
    """Analyze a JSON session export."""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Try to extract URLs from common formats
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'url' in item:
                    urls.append(item['url'])
        elif isinstance(data, dict):
            # Session Buddy format
            if 'windows' in data:
                for window in data['windows']:
                    for tab in window.get('tabs', []):
                        if 'url' in tab:
                            urls.append(tab['url'])
            # Simple tabs array
            elif 'tabs' in data:
                for tab in data['tabs']:
                    if isinstance(tab, dict) and 'url' in tab:
                        urls.append(tab['url'])
    return urls

def main():
    ingestion_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    all_urls = []

    # Process all files
    for file_path in ingestion_dir.glob('*.txt'):
        all_urls.extend(analyze_url_file(file_path))

    for file_path in ingestion_dir.glob('*.json'):
        try:
            all_urls.extend(analyze_json_file(file_path))
        except:
            pass

    # Analyze
    domains = [urlparse(url).netloc for url in all_urls]
    domain_counts = Counter(domains)

    # Results
    results = {
        'stats': {
            'total_tabs': len(all_urls),
            'unique_domains': len(domain_counts),
            'domain_frequency': dict(domain_counts.most_common(20))
        },
        'tabs': [{'url': url} for url in all_urls]
    }

    # Save
    output_file = output_dir / 'browser_tabs.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Report
    print(f"Total tabs: {len(all_urls)}")
    print(f"Unique domains: {len(domain_counts)}")
    print(f"\nTop domains:")
    for domain, count in domain_counts.most_common(10):
        print(f"  {domain}: {count}")

    print(f"\nResults saved to: {output_file}")

if __name__ == '__main__':
    main()
EOF

    # Run basic analysis
    python "$OUTPUT_DIR/analyze_tabs.py" "$INGESTION_DIR" "$OUTPUT_DIR"

    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✓ Basic Analysis Complete${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "Results saved to: $OUTPUT_DIR/browser_tabs.json"
    echo ""
    echo -e "${YELLOW}Note: For full functionality, the browser tab analyzer module needs to be implemented.${NC}"
    echo "See: cognitive_tribunal/modules/browser_tab_analyzer.py"

    exit 0
fi

# If module exists, run normal ingestion
echo -e "${GREEN}Running browser tab analyzer...${NC}"
echo ""

cd "$PROJECT_ROOT"
python main.py \
    --browser-tabs "$INGESTION_DIR" \
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
