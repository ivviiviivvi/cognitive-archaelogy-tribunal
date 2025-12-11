#!/usr/bin/env bash
#
# License Chooser for Cognitive Archaeology Datasets
# Interactive tool to help select and apply appropriate license
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

echo -e "${BOLD}${BLUE}================================${NC}"
echo -e "${BOLD}${BLUE}License Chooser${NC}"
echo -e "${BOLD}${BLUE}================================${NC}"
echo ""
echo "Select a license for your dataset."
echo ""

# License options
echo "Available licenses:"
echo ""
echo "  1. CC0 1.0 Universal (Public Domain Dedication)"
echo "     - No rights reserved"
echo "     - No attribution required"
echo "     - Maximum freedom for reuse"
echo "     - ✓ Recommended for maximum impact"
echo ""
echo "  2. CC-BY 4.0 (Attribution)"
echo "     - Requires attribution"
echo "     - Allows commercial use"
echo "     - Allows modifications"
echo "     - ✓ Good for academic datasets"
echo ""
echo "  3. CC-BY-SA 4.0 (Attribution + ShareAlike)"
echo "     - Requires attribution"
echo "     - Derivatives must use same license"
echo "     - Allows commercial use"
echo ""
echo "  4. CC-BY-NC 4.0 (Attribution + Non-Commercial)"
echo "     - Requires attribution"
echo "     - Non-commercial use only"
echo "     - ⚠ Limits academic reuse"
echo ""
echo "  5. ODbL 1.0 (Open Database License)"
echo "     - For databases specifically"
echo "     - Requires attribution + ShareAlike"
echo ""
echo "  6. Custom License"
echo "     - Provide your own license text"
echo ""

read -p "Choose license (1-6): " choice

case $choice in
    1)
        LICENSE_NAME="CC0 1.0 Universal"
        LICENSE_SPDX="CC0-1.0"
        LICENSE_URL="https://creativecommons.org/publicdomain/zero/1.0/"
        ;;
    2)
        LICENSE_NAME="Creative Commons Attribution 4.0 International"
        LICENSE_SPDX="CC-BY-4.0"
        LICENSE_URL="https://creativecommons.org/licenses/by/4.0/"
        ;;
    3)
        LICENSE_NAME="Creative Commons Attribution-ShareAlike 4.0 International"
        LICENSE_SPDX="CC-BY-SA-4.0"
        LICENSE_URL="https://creativecommons.org/licenses/by-sa/4.0/"
        ;;
    4)
        LICENSE_NAME="Creative Commons Attribution-NonCommercial 4.0 International"
        LICENSE_SPDX="CC-BY-NC-4.0"
        LICENSE_URL="https://creativecommons.org/licenses/by-nc/4.0/"
        ;;
    5)
        LICENSE_NAME="Open Database License 1.0"
        LICENSE_SPDX="ODbL-1.0"
        LICENSE_URL="https://opendatacommons.org/licenses/odbl/1-0/"
        ;;
    6)
        read -p "Enter license name: " LICENSE_NAME
        read -p "Enter SPDX identifier (or 'custom'): " LICENSE_SPDX
        read -p "Enter license URL (optional): " LICENSE_URL
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Selected: $LICENSE_NAME"
echo "SPDX: $LICENSE_SPDX"
echo "URL: $LICENSE_URL"
echo ""

# Get dataset details
read -p "Dataset name: " DATASET_NAME
read -p "Your name (for attribution): " AUTHOR_NAME

# Create LICENSE file
echo ""
echo "Creating LICENSE file..."

cat > "$PROJECT_ROOT/LICENSE-DATASET" <<EOF
# License

**Dataset**: $DATASET_NAME
**License**: $LICENSE_NAME
**SPDX Identifier**: $LICENSE_SPDX
**License URL**: $LICENSE_URL

---

## Summary

EOF

# Add license-specific summary
case $choice in
    1)
        cat >> "$PROJECT_ROOT/LICENSE-DATASET" <<EOF
This dataset is dedicated to the public domain under CC0 1.0.

You are free to:
- Copy, modify, and distribute the dataset
- Use for commercial purposes
- Use without attribution (though appreciated)

No warranties or conditions apply.
EOF
        ;;
    2)
        cat >> "$PROJECT_ROOT/LICENSE-DATASET" <<EOF
This dataset is licensed under Creative Commons Attribution 4.0 International.

You are free to:
- Share: copy and redistribute
- Adapt: remix, transform, and build upon
- Use for commercial purposes

Under the following terms:
- Attribution: You must give appropriate credit and link to the license
EOF
        ;;
    3)
        cat >> "$PROJECT_ROOT/LICENSE-DATASET" <<EOF
This dataset is licensed under CC-BY-SA 4.0.

You are free to:
- Share: copy and redistribute
- Adapt: remix, transform, and build upon
- Use for commercial purposes

Under the following terms:
- Attribution: You must give appropriate credit
- ShareAlike: Derivatives must use the same license
EOF
        ;;
    4)
        cat >> "$PROJECT_ROOT/LICENSE-DATASET" <<EOF
This dataset is licensed under CC-BY-NC 4.0.

You are free to:
- Share: copy and redistribute
- Adapt: remix, transform, and build upon

Under the following terms:
- Attribution: You must give appropriate credit
- NonCommercial: You may not use for commercial purposes
EOF
        ;;
    5)
        cat >> "$PROJECT_ROOT/LICENSE-DATASET" <<EOF
This database is licensed under the Open Database License 1.0.

You are free to:
- Share: copy and redistribute
- Create: produce works from the database
- Adapt: modify, transform, and build upon

Under the following terms:
- Attribution: You must attribute the database
- Share-Alike: Derived databases must use ODbL
- Keep open: The database must remain open
EOF
        ;;
esac

cat >> "$PROJECT_ROOT/LICENSE-DATASET" <<EOF

---

## Attribution

If you use this dataset, please cite:

\`\`\`
$AUTHOR_NAME. ($DATASET_NAME). Licensed under $LICENSE_NAME ($LICENSE_SPDX).
$LICENSE_URL
\`\`\`

---

## Full License Text

For the complete license text, see: $LICENSE_URL

---

**SPDX-License-Identifier**: $LICENSE_SPDX
**Copyright**: $AUTHOR_NAME, 2025
EOF

echo ""
echo -e "${GREEN}LICENSE-DATASET file created!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review the LICENSE-DATASET file"
echo "  2. Create CONSENT.md to document permissions"
echo "  3. Add citation information to README"
echo "  4. Update dataset metadata with license info"
echo ""
echo "Commands:"
echo "  cat LICENSE-DATASET"
echo "  ./scripts/create_consent.sh"
echo ""
