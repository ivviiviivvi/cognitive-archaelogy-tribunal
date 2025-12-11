#!/usr/bin/env bash
#
# Sanitize Data for Public Release
# Helps remove private/sensitive information before publishing
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BOLD}${BLUE}================================${NC}"
echo -e "${BOLD}${BLUE}Data Sanitization Check${NC}"
echo -e "${BOLD}${BLUE}================================${NC}"
echo ""
echo -e "${YELLOW}This tool helps identify potentially sensitive data${NC}"
echo -e "${YELLOW}before public release. Review all findings carefully.${NC}"
echo ""

# Check patterns
echo "Scanning for potentially sensitive patterns..."
echo ""

# 1. Check for common credential patterns
echo "🔍 Checking for credentials..."
FOUND_CREDS=0

# API keys
if grep -r -i "api[_-]key\|apikey\|api_secret" ingestion/ output/ 2>/dev/null | grep -v ".git" | grep -v "example"; then
    echo -e "${RED}  ⚠ Found potential API keys${NC}"
    FOUND_CREDS=1
else
    echo -e "${GREEN}  ✓ No API keys found${NC}"
fi

# Tokens
if grep -r -i "token\|bearer\|authorization" ingestion/ output/ 2>/dev/null | grep -v ".git" | grep -v "github-token" | grep -v "example"; then
    echo -e "${RED}  ⚠ Found potential tokens${NC}"
    FOUND_CREDS=1
else
    echo -e "${GREEN}  ✓ No tokens found${NC}"
fi

# Passwords
if grep -r -i "password\|passwd" ingestion/ output/ 2>/dev/null | grep -v ".git" | grep -v "example"; then
    echo -e "${RED}  ⚠ Found password references${NC}"
    FOUND_CREDS=1
else
    echo -e "${GREEN}  ✓ No passwords found${NC}"
fi

echo ""

# 2. Check for personal information
echo "🔍 Checking for personal information..."
FOUND_PII=0

# Email addresses
EMAILS=$(grep -r -o -E "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" ingestion/ output/ 2>/dev/null | grep -v ".git" || true)
if [ ! -z "$EMAILS" ]; then
    EMAIL_COUNT=$(echo "$EMAILS" | wc -l)
    echo -e "${YELLOW}  ⚠ Found $EMAIL_COUNT email addresses${NC}"
    echo "    Review to ensure you want these public"
    FOUND_PII=1
else
    echo -e "${GREEN}  ✓ No email addresses found${NC}"
fi

# Phone numbers (basic US format)
PHONES=$(grep -r -o -E "\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}" ingestion/ output/ 2>/dev/null | grep -v ".git" || true)
if [ ! -z "$PHONES" ]; then
    PHONE_COUNT=$(echo "$PHONES" | wc -l)
    echo -e "${YELLOW}  ⚠ Found $PHONE_COUNT potential phone numbers${NC}"
    FOUND_PII=1
else
    echo -e "${GREEN}  ✓ No phone numbers found${NC}"
fi

# IP addresses
IPS=$(grep -r -o -E "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" ingestion/ output/ 2>/dev/null | grep -v ".git" | grep -v "0.0.0.0" | grep -v "127.0.0.1" || true)
if [ ! -z "$IPS" ]; then
    IP_COUNT=$(echo "$IPS" | wc -l)
    echo -e "${YELLOW}  ⚠ Found $IP_COUNT IP addresses${NC}"
    FOUND_PII=1
else
    echo -e "${GREEN}  ✓ No private IPs found${NC}"
fi

echo ""

# 3. Check for private URLs/domains
echo "🔍 Checking for private URLs..."

# Internal domains
PRIVATE_DOMAINS=$(grep -r -i "localhost\|127.0.0.1\|\.local\|\.internal\|\.corp" ingestion/ output/ 2>/dev/null | grep -v ".git" || true)
if [ ! -z "$PRIVATE_DOMAINS" ]; then
    echo -e "${YELLOW}  ⚠ Found references to internal domains${NC}"
else
    echo -e "${GREEN}  ✓ No internal domains found${NC}"
fi

echo ""

# 4. File size check
echo "🔍 Checking file sizes..."
LARGE_FILES=$(find ingestion/ output/ -type f -size +10M 2>/dev/null || true)
if [ ! -z "$LARGE_FILES" ]; then
    echo -e "${YELLOW}  ⚠ Large files found (>10MB):${NC}"
    echo "$LARGE_FILES" | while read file; do
        SIZE=$(du -h "$file" | cut -f1)
        echo "    - $file ($SIZE)"
    done
    echo "  Consider if these should be published"
else
    echo -e "${GREEN}  ✓ No excessively large files${NC}"
fi

echo ""

# 5. Summary and recommendations
echo "================================"
echo "Summary"
echo "================================"
echo ""

if [ $FOUND_CREDS -eq 1 ]; then
    echo -e "${RED}⚠ CREDENTIALS FOUND - DO NOT PUBLISH${NC}"
    echo "  Remove all API keys, tokens, and passwords before release"
    echo ""
fi

if [ $FOUND_PII -eq 1 ]; then
    echo -e "${YELLOW}⚠ Personal information found${NC}"
    echo "  Review and redact if necessary"
    echo ""
fi

echo "Recommendations:"
echo ""
echo "1. Manual Review:"
echo "   - Review all JSON files for sensitive data"
echo "   - Check conversation content for private information"
echo "   - Verify bookmark URLs don't expose private resources"
echo ""
echo "2. Redaction Options:"
echo "   # Remove specific files"
echo "   rm ingestion/ai-exports/private-conversation.json"
echo ""
echo "   # Filter JSON data"
echo "   jq 'del(.conversations[] | select(.title | contains(\"private\")))' \\"
echo "     output/ai-context/ai_conversations.json > public.json"
echo ""
echo "   # Replace sensitive values"
echo "   sed -i 's/my-api-key/REDACTED/g' file.json"
echo ""
echo "3. Create Clean Copy:"
echo "   # Copy only public-safe data to new directory"
echo "   mkdir -p public-release/"
echo "   # Manually copy verified-safe files"
echo ""
echo "4. Use .gitignore.local:"
echo "   # Keep private files out of git"
echo "   echo 'ingestion/private/*' >> .gitignore.local"
echo ""
echo "5. Final Check:"
echo "   # Run this script again on clean copy"
echo "   ./scripts/sanitize_for_public.sh"
echo ""
echo "6. Publish:"
echo "   # Only after thorough review"
echo "   git add ."
echo "   git commit -m 'Public dataset release'"
echo "   ./scripts/publish_dataset.sh"
echo ""

if [ $FOUND_CREDS -eq 0 ] && [ $FOUND_PII -eq 0 ]; then
    echo -e "${GREEN}✓ No obvious sensitive data found${NC}"
    echo -e "${YELLOW}  Still recommend manual review before publishing${NC}"
    echo ""
fi
