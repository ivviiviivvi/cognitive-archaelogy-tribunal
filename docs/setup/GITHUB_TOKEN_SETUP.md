# GitHub Token Setup Guide

**Required for:** Repository analysis (Phases 2-5 of ingestion plan)

---

## Why You Need a GitHub Token

The Cognitive Archaeology Tribunal needs a GitHub Personal Access Token to:
- Analyze your personal repositories (4444JPP)
- Analyze organization repositories (ivi374forivi)
- Access private repository metadata
- Avoid rate limits (60 req/hr → 5000 req/hr)

Without a token, repository analysis modules **cannot function**.

---

## Quick Setup (5 minutes)

### Step 1: Create Token

1. **Go to GitHub Settings**
   - Direct link: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Click "Generate new token (classic)"**

3. **Configure Token**
   - **Note:** `Cognitive Archaeology Tribunal - Repo Analysis`
   - **Expiration:** Choose duration (30 days, 60 days, 90 days, or no expiration)

4. **Select Scopes**
   - ✅ **repo** (Full control of private repositories)
     - This includes: repo:status, repo_deployment, public_repo, repo:invite, security_events

   **Why these scopes:**
   - `repo`: Required to read repository metadata, commits, languages, etc.
   - This gives read access to analyze your repos, not modify them

5. **Generate Token**
   - Click "Generate token" at the bottom
   - **IMPORTANT:** Copy the token immediately (you won't see it again)
   - Token format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### Step 2: Set Environment Variable

**Linux/Mac (Current Session):**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

**Verify:**
```bash
echo "Token set: ${GITHUB_TOKEN:0:10}..."
```

**Linux/Mac (Permanent - Optional):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

**Windows (Command Prompt):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
```

---

### Step 3: Test Token

```bash
# Test if token is set
python -c "import os; print('✓ Token set' if os.getenv('GITHUB_TOKEN') else '✗ Token not set')"

# Test token with a simple repo query (optional)
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

---

## Using the Token with the Tool

### Method 1: Environment Variable (Recommended)
```bash
export GITHUB_TOKEN="ghp_xxx"

# Then run normally
python main.py --personal-repos 4444JPP --output-dir ./output/personal
```

### Method 2: Command Line Argument
```bash
python main.py \
  --personal-repos 4444JPP \
  --github-token "ghp_xxx" \
  --output-dir ./output/personal
```

### Method 3: Configuration File
```yaml
# config.yaml
github:
  token: "${GITHUB_TOKEN}"  # Reads from environment
  # OR
  token: "ghp_xxx"  # Direct (not recommended for security)
```

---

## Security Best Practices

### DO ✅
- ✅ Store token in environment variables
- ✅ Use token expiration (30-90 days)
- ✅ Regenerate tokens periodically
- ✅ Use minimal required scopes
- ✅ Keep token confidential

### DON'T ❌
- ❌ Commit tokens to git repositories
- ❌ Share tokens with others
- ❌ Use tokens in public URLs
- ❌ Store in plain text files
- ❌ Use same token for multiple purposes

### If Token is Compromised
1. Go to: https://github.com/settings/tokens
2. Find the compromised token
3. Click "Delete"
4. Generate a new token
5. Update your environment variable

---

## Troubleshooting

### "Bad credentials" error
- Token is invalid or expired
- Regenerate token at https://github.com/settings/tokens
- Ensure you copied the full token

### "API rate limit exceeded"
- Token not being used (check environment variable)
- Verify token is set: `echo $GITHUB_TOKEN`
- Token may lack required scopes

### "Not Found" for repositories
- Token lacks `repo` scope
- Regenerate with correct scopes
- Check you have access to the repos

### Token not persisting
- Environment variable only lasts current session
- Add to `.bashrc`/`.zshrc` for permanence
- Or re-export each session

---

## What Happens When You Run Analysis

With a valid token, the tool will:

1. **Authenticate with GitHub API**
   - Uses your token for all requests
   - Gets 5000 requests/hour instead of 60

2. **Analyze Personal Repos (4444JPP)**
   - Fetch all repositories
   - Classify forks vs. originals
   - Detect modifications in forks
   - Calculate activity metrics
   - Extract language statistics
   - Generate triage recommendations

3. **Analyze Org Repos (ivi374forivi)**
   - Fetch organization repositories
   - Calculate health scores
   - Detect stale/abandoned projects
   - Track dependencies
   - Map open issues
   - Create migration plans

4. **Generate Outputs**
   - `personal_repos.json` - Complete inventory
   - `org_repos.json` - Health reports
   - `inventory.json` - Unified catalog
   - `knowledge_graph.json` - Relationship map
   - `triage_report.txt` - Actionable recommendations

---

## Expected Analysis Time

With token:
- **Personal repos (35+):** ~30-60 seconds
- **Org repos (23):** ~20-40 seconds
- **Combined:** ~60-90 seconds

Without token:
- ❌ Will fail immediately due to authentication

---

## Commands Ready to Run

Once token is set:

```bash
# Verify token
echo "Token: ${GITHUB_TOKEN:0:10}..."

# Personal repos only
python main.py \
  --personal-repos 4444JPP \
  --output-dir ./output/personal-repos

# Org repos only
python main.py \
  --org-repos ivi374forivi \
  --output-dir ./output/org-repos

# Both together (recommended)
python main.py \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --output-dir ./output/complete-repo-audit

# Review results
cat ./output/complete-repo-audit/triage_report.txt
```

---

## Next Steps After Token Setup

1. ✅ Set token: `export GITHUB_TOKEN="ghp_xxx"`
2. ✅ Verify: `echo $GITHUB_TOKEN`
3. ✅ Run personal repo analysis
4. ✅ Run org repo analysis
5. ✅ Review triage reports
6. ✅ Act on recommendations

---

## Support

**GitHub Token Issues:**
- GitHub Help: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

**Tool Issues:**
- Check: `NEXT_STEPS.md` for troubleshooting
- Check: `USAGE.md` for detailed documentation

---

**Status:** Waiting for token setup to proceed with repository analysis

**Once token is set, you can immediately run:**
```bash
python main.py --personal-repos 4444JPP --org-repos ivi374forivi --output-dir ./output/repos
```
