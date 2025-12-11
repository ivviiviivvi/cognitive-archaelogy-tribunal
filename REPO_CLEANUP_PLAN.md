# Repository Cleanup Plan

**Date:** 2025-11-17
**Purpose:** Organize cognitive-archaelogy-tribunal repository structure

---

## Current Issues

### Root Directory Clutter (13+ markdown files)
- Planning docs mixed with operational docs
- Context preservation files in root
- Generated analysis files in root
- Naming inconsistencies (UPPERCASE.md, >symbols.MD)

### File Organization Needed
```
Current (cluttered):
├── README.md
├── USAGE.md
├── PROJECT_SUMMARY.md
├── INGESTION_PLAN.md
├── INTEGRATION_QUEUE.md
├── INTEGRATION_QUICK_START.md
├── NEXT_STEPS.md
├── GITHUB_TOKEN_SETUP.md
├── PHASE2_ANALYSIS_SUMMARY.md
├── PHASE2_REVISED_INTEGRATION_ANALYSIS.md
├── CHAOS>LOGOS-PATH_STEPXSTEP.MD
├── CHAOS>ORDER_LINEAR-PATH_STEPXSTEP.MD
├── GENESIS-CHAT-PRESERVATION
├── 4_ivi374_F0Rivi4_ CognitiveOperatingSystem.md
├── 4_ivi374_F0Rivi4_  CognitiveOperatingSystem.pdf (1.2MB)
└── ... (code files)
```

---

## Proposed Structure

```
cognitive-archaelogy-tribunal/
├── README.md                          # Main entry point
├── USAGE.md                          # How to use the tool
├── PROJECT_SUMMARY.md                # What this project does
├── requirements.txt                  # Dependencies
├── setup.py                         # Installation
├── main.py                          # CLI entry point
├── config.example.yaml              # Config template
│
├── cognitive_tribunal/              # Main package
│   ├── modules/
│   ├── outputs/
│   └── utils/
│
├── docs/                            # Documentation (NEW)
│   ├── README.md                    # Docs overview
│   ├── setup/                       # Setup guides
│   │   ├── github-token-setup.md
│   │   └── installation.md
│   ├── guides/                      # User guides
│   │   ├── integration-guide.md
│   │   └── quick-start.md
│   └── analysis/                    # Generated analysis docs
│       ├── phase1-self-analysis.md
│       ├── phase2-repo-analysis.md
│       └── phase2-integration-analysis.md
│
├── context/                         # Context preservation (NEW)
│   ├── README.md                    # Context docs overview
│   ├── planning/
│   │   ├── ingestion-plan.md
│   │   ├── integration-queue.md
│   │   └── next-steps.md
│   └── history/
│       ├── genesis-chat-preservation.md
│       ├── chaos-to-logos-path.md
│       ├── chaos-to-order-path.md
│       └── cognitive-os-master-plan.md
│
├── examples/                        # Example usage
├── tests/                          # Test files
└── output/                         # Generated outputs (gitignored)
```

---

## Cleanup Actions

### Phase 1: Create Directory Structure (5 min)

```bash
# Create new directories
mkdir -p docs/setup
mkdir -p docs/guides
mkdir -p docs/analysis
mkdir -p context/planning
mkdir -p context/history
```

### Phase 2: Move Files (10 min)

**Setup Documentation:**
```bash
mv GITHUB_TOKEN_SETUP.md docs/setup/github-token-setup.md
```

**User Guides:**
```bash
mv INTEGRATION_QUICK_START.md docs/guides/integration-quick-start.md
```

**Analysis Documents:**
```bash
mv PHASE2_ANALYSIS_SUMMARY.md docs/analysis/phase2-repo-analysis.md
mv PHASE2_REVISED_INTEGRATION_ANALYSIS.md docs/analysis/phase2-integration-analysis.md
```

**Planning Documents:**
```bash
mv INGESTION_PLAN.md context/planning/ingestion-plan.md
mv INTEGRATION_QUEUE.md context/planning/integration-queue.md
mv NEXT_STEPS.md context/planning/next-steps.md
```

**Context Preservation:**
```bash
mv "CHAOS>LOGOS-PATH_STEPXSTEP.MD" context/history/chaos-to-logos-path.md
mv "CHAOS>ORDER_LINEAR-PATH_STEPXSTEP.MD" context/history/chaos-to-order-path.md
mv GENESIS-CHAT-PRESERVATION context/history/genesis-chat-preservation.md
mv "4_ivi374_F0Rivi4_ CognitiveOperatingSystem.md" context/history/cognitive-os-master-plan.md
```

**Large Files (Optional):**
```bash
# Move PDF to context/history or consider removing if not needed in repo
mv "4_ivi374_F0Rivi4_  CognitiveOperatingSystem.pdf" context/history/
# Or add to .gitignore if too large
```

### Phase 3: Create README Files (15 min)

**docs/README.md:**
```markdown
# Documentation

## Setup Guides
- [GitHub Token Setup](setup/github-token-setup.md) - How to get a GitHub token
- [Installation](setup/installation.md) - Installing dependencies

## User Guides
- [Quick Start](guides/quick-start.md) - Get started in 15 minutes
- [Integration Guide](guides/integration-quick-start.md) - Fork → Org integration

## Analysis Reports
- [Phase 2: Repository Analysis](analysis/phase2-repo-analysis.md) - 85 repos analyzed
- [Phase 2: Integration Analysis](analysis/phase2-integration-analysis.md) - Integration strategy
```

**context/README.md:**
```markdown
# Context Preservation

This directory contains historical context and planning documents.

## Planning
Current plans and tracking:
- [Ingestion Plan](planning/ingestion-plan.md) - 5-phase ingestion strategy
- [Integration Queue](planning/integration-queue.md) - 42 fork integration tracking
- [Next Steps](planning/next-steps.md) - Immediate action items

## History
Historical context and evolution:
- [Genesis Chat Preservation](history/genesis-chat-preservation.md) - Original conversation
- [Chaos to Logos Path](history/chaos-to-logos-path.md) - Logical task order
- [Chaos to Order Path](history/chaos-to-order-path.md) - Linear task execution
- [Cognitive OS Master Plan](history/cognitive-os-master-plan.md) - System architecture vision
```

**context/planning/README.md:**
```markdown
# Current Planning Documents

- **[Integration Queue](integration-queue.md)** - Active tracking of 42 fork integrations
- **[Ingestion Plan](ingestion-plan.md)** - Complete 5-phase ingestion strategy
- **[Next Steps](next-steps.md)** - Immediate priority actions

## Quick Links
- Start integration: See [Integration Queue](integration-queue.md) Tier 1
- Run analysis: See [Ingestion Plan](ingestion-plan.md) Phase 2
- Get token: See [../../docs/setup/github-token-setup.md](../../docs/setup/github-token-setup.md)
```

### Phase 4: Update Cross-References (10 min)

Files that reference moved documents need updates:
- README.md - Update links to moved files
- Any docs referencing `INTEGRATION_QUEUE.md` → `context/planning/integration-queue.md`
- Any docs referencing other moved files

### Phase 5: Commit Changes (5 min)

```bash
git add .
git commit -m "Reorganize repository structure

- Create docs/ directory for documentation
- Create context/ directory for planning and history
- Move 13 root markdown files to organized locations
- Add README files for navigation
- Update cross-references

Improves:
- Discoverability (clear docs/ entry point)
- Navigation (organized by purpose)
- Maintainability (logical grouping)
- Professionalism (clean root directory)
"
git push
```

---

## Benefits

### Before (Cluttered)
- 13+ markdown files in root
- Hard to find specific docs
- Unclear which docs are current vs historical
- Mix of operational and context docs

### After (Organized)
- 3 markdown files in root (README, USAGE, PROJECT_SUMMARY)
- Clear navigation: docs/ for users, context/ for planning
- Organized by purpose (setup, guides, analysis, planning, history)
- Professional, maintainable structure

---

## Rollback Plan

If needed, restore original structure:
```bash
git revert [commit-hash]
# Or manually move files back
```

---

## Execution Checklist

- [ ] Create directory structure (docs/, context/)
- [ ] Move files to appropriate locations
- [ ] Create README.md files for navigation
- [ ] Update cross-references in existing docs
- [ ] Update main README.md with new structure
- [ ] Test all links work
- [ ] Commit and push changes
- [ ] Verify on GitHub web interface

---

**Estimated Time:** 45 minutes
**Complexity:** Low (simple file moves)
**Risk:** Low (git tracks all changes, easy to revert)
**Value:** High (much better organization)
