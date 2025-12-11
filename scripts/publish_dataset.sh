#!/usr/bin/env bash
#
# Dataset Publishing Workflow
# Prepares data and outputs for public release
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RELEASE_DIR="$PROJECT_ROOT/releases"

echo -e "${BOLD}${BLUE}================================${NC}"
echo -e "${BOLD}${BLUE}Dataset Publishing Workflow${NC}"
echo -e "${BOLD}${BLUE}================================${NC}"
echo ""

# Get dataset name and version
read -p "Dataset name (e.g., 'my-cognitive-archaeology'): " DATASET_NAME
read -p "Version (e.g., '1.0', '2024-Q4'): " VERSION

if [ -z "$DATASET_NAME" ] || [ -z "$VERSION" ]; then
    echo -e "${YELLOW}Dataset name and version required${NC}"
    exit 1
fi

RELEASE_NAME="${DATASET_NAME}-v${VERSION}"
RELEASE_PATH="$RELEASE_DIR/$RELEASE_NAME"

echo ""
echo "Creating release: $RELEASE_NAME"
echo "Output: $RELEASE_PATH"
echo ""

# Create release directory
mkdir -p "$RELEASE_PATH"

# Copy structure
echo "Building release package..."
echo ""

# 1. Copy ingestion data
if [ -d "$PROJECT_ROOT/ingestion" ]; then
    echo "  ✓ Copying ingestion data..."
    cp -r "$PROJECT_ROOT/ingestion" "$RELEASE_PATH/"
fi

# 2. Copy outputs
if [ -d "$PROJECT_ROOT/output" ]; then
    echo "  ✓ Copying analysis outputs..."
    cp -r "$PROJECT_ROOT/output" "$RELEASE_PATH/"
fi

# 3. Copy documentation
echo "  ✓ Copying documentation..."
mkdir -p "$RELEASE_PATH/docs"
cp "$PROJECT_ROOT/README.md" "$RELEASE_PATH/" 2>/dev/null || true
cp "$PROJECT_ROOT/docs/PUBLIC_ARCHIVAL_GUIDE.md" "$RELEASE_PATH/docs/" 2>/dev/null || true
cp "$PROJECT_ROOT/docs/CREATIVE_ABSTRACTIONS.md" "$RELEASE_PATH/docs/" 2>/dev/null || true

# 4. Generate dataset metadata
echo "  ✓ Generating metadata..."
cat > "$RELEASE_PATH/DATASET.md" <<EOF
# Dataset: $DATASET_NAME

**Version**: $VERSION
**Release Date**: $(date +%Y-%m-%d)
**Tool**: Cognitive Archaeology Tribunal
**Repository**: https://github.com/ivi374forivi/cognitive-archaelogy-tribunal

## Overview

[Add description of this dataset]

## Contents

### Ingestion Data
\`\`\`
ingestion/
$(find "$RELEASE_PATH/ingestion" -type f 2>/dev/null | sed 's|'"$RELEASE_PATH"'/||' | head -20)
\`\`\`

### Analysis Outputs
\`\`\`
output/
$(find "$RELEASE_PATH/output" -type f 2>/dev/null | sed 's|'"$RELEASE_PATH"'/||' | head -20)
\`\`\`

## Statistics

- **AI Conversations**: $(jq '.stats.total_conversations // 0' "$RELEASE_PATH/output/ai-context/ai_conversations.json" 2>/dev/null || echo "N/A")
- **Bookmarks**: $(find "$RELEASE_PATH/output/bookmarks" -name "web_bookmarks.json" -exec jq '.stats.total_bookmarks // 0' {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}' || echo "N/A")
- **Archive Files**: $(jq '.stats.total_files // 0' "$RELEASE_PATH/output/archives/archives.json" 2>/dev/null || echo "N/A")

## Collection Period

- **Start**: [Add start date]
- **End**: [Add end date]

## Methodology

Data was collected and processed using the Cognitive Archaeology Tribunal:

1. **Ingestion**: Data placed in ingestion chambers
2. **Processing**: Automated analysis via ingestion scripts
3. **Curation**: [Add any manual curation steps]
4. **Publication**: Packaged for public release

## License

This dataset is released under [LICENSE NAME].

See LICENSE file for full terms.

## Citation

If you use this dataset, please cite:

\`\`\`bibtex
@dataset{${DATASET_NAME}_${VERSION},
  title = {${DATASET_NAME}},
  author = {[Your Name]},
  year = {$(date +%Y)},
  version = {$VERSION},
  url = {https://github.com/ivi374forivi/cognitive-archaelogy-tribunal/releases}
}
\`\`\`

## Contact

[Your contact information or repository issues link]

---

Generated: $(date +%Y-%m-%d) using Cognitive Archaeology Tribunal
EOF

# 5. Add license
if [ -f "$PROJECT_ROOT/LICENSE" ]; then
    echo "  ✓ Copying LICENSE..."
    cp "$PROJECT_ROOT/LICENSE" "$RELEASE_PATH/"
else
    echo "  ⚠ No LICENSE found - consider adding one"
fi

# 6. Create manifest
echo "  ✓ Creating manifest..."
cat > "$RELEASE_PATH/MANIFEST.txt" <<EOF
Cognitive Archaeology Dataset Release
======================================

Name: $DATASET_NAME
Version: $VERSION
Date: $(date +%Y-%m-%d)

Files included:
EOF

find "$RELEASE_PATH" -type f | sed 's|'"$RELEASE_PATH"'/||' | sort >> "$RELEASE_PATH/MANIFEST.txt"

# 7. Generate checksums
echo "  ✓ Generating checksums..."
cd "$RELEASE_PATH"
find . -type f -not -name "SHA256SUMS" -exec sha256sum {} \; > SHA256SUMS
cd "$PROJECT_ROOT"

# 8. Create archive
echo ""
echo "Creating archive..."
cd "$RELEASE_DIR"
tar -czf "${RELEASE_NAME}.tar.gz" "$RELEASE_NAME"
zip -r -q "${RELEASE_NAME}.zip" "$RELEASE_NAME"
cd "$PROJECT_ROOT"

# Calculate sizes
TAR_SIZE=$(du -h "$RELEASE_DIR/${RELEASE_NAME}.tar.gz" | cut -f1)
ZIP_SIZE=$(du -h "$RELEASE_DIR/${RELEASE_NAME}.zip" | cut -f1)

# Summary
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Release Package Complete${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Location: $RELEASE_PATH"
echo ""
echo "Archives:"
echo "  - ${RELEASE_NAME}.tar.gz ($TAR_SIZE)"
echo "  - ${RELEASE_NAME}.zip ($ZIP_SIZE)"
echo ""
echo "Next steps:"
echo "  1. Review DATASET.md and add details"
echo "  2. Verify data is sanitized (no private info)"
echo "  3. Test archive integrity"
echo "  4. Create git tag: git tag -a dataset-v$VERSION"
echo "  5. Push to GitHub and create release"
echo "  6. Upload archives to GitHub release"
echo "  7. Consider Zenodo for DOI"
echo ""
echo "Commands:"
echo "  # Tag and push"
echo "  git tag -a dataset-v$VERSION -m 'Dataset release $VERSION'"
echo "  git push --tags"
echo ""
echo "  # Verify checksums"
echo "  cd $RELEASE_PATH && sha256sum -c SHA256SUMS"
echo ""
