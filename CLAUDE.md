# Claude Instructions for OpenClaw Second Brain Project

This document provides context and guidelines for AI assistants working on this project.

## Project Overview

**OpenClaw "Second Brain"** is a comprehensive deployment guide for setting up an AI-powered personal knowledge management system using OpenClaw. The project includes:

- Platform-specific deployment guides (macOS and Ubuntu/Linux)
- Security-vetted skills for YouTube transcript extraction
- Container runtime comparisons and recommendations
- Complete skill vetting and security review processes

**Primary Goal**: Enable users to deploy a secure, privacy-first "Second Brain" that ingests messages, extracts content, categorizes information, and delivers automated email digests.

---

## Project Structure

```
/
├── README.md                       # Project introduction and navigation
├── PLAN.md                         # Overview with platform comparison
├── PLAN_MACOS.md                   # Apple Silicon (M1/M2/M3) deployment
├── PLAN_UBUNTU.md                  # Ubuntu/Linux VPS deployment
├── SKILL_VETTING_GUIDE.md         # (Draft) Comprehensive skill review process
├── PROJECT_STATUS.md              # (Draft) Current state and decisions
│
├── skills/                         # Skills directory (vetted and pending)
│   ├── README.md                   # Skills management guide
│   ├── SKILL_COMPARISON.md        # YouTube skill options analysis
│   │
│   ├── vetted/                     # Approved, ready-to-use skills
│   │   └── youtube-direct/         # Custom YouTube API integration
│   │       ├── README.md           # Setup and usage
│   │       ├── SKILL.md            # OpenClaw skill documentation
│   │       ├── package.json        # Dependencies
│   │       ├── lib/
│   │       │   └── youtube-client.js   # Core API wrapper
│   │       └── scripts/
│   │           ├── setup-auth.js       # OAuth configuration
│   │           ├── get-transcript.js   # Fetch transcripts
│   │           ├── search.js           # Search videos
│   │           └── test-connection.js  # Verify setup
│   │
│   └── pending-review/             # Skills under security review
│       ├── HOW_TO_REVIEW.md        # Review instructions
│       └── youtube-summarizer/     # TranscriptAPI (reviewed, approved)
│
└── .claude/                        # Claude Code configuration
    └── settings.local.json
```

---

## Key Concepts

### 1. Second Brain Architecture

The system follows this flow:
```
Messages (Telegram/WhatsApp/etc.)
    ↓
OpenClaw Gateway (localhost-only)
    ↓
Content Extraction (YouTube transcripts, web articles)
    ↓
Categorization & Memory Storage (~/.openclaw/memory/)
    ↓
Automated Email Digests (2x daily + weekly)
```

### 2. Platform-Specific Deployments

- **PLAN_MACOS.md**: For Apple Silicon Macs, personal use, OrbStack containers
- **PLAN_UBUNTU.md**: For VPS/cloud hosting, rootless Podman, always-on deployments
- **PLAN.md**: Entry point with comparison and overview

### 3. Security-First Approach

All third-party skills must be:
- Source code reviewed
- Dependency analyzed
- Network behavior verified
- Documented in security review files

### 4. YouTube Skill Options

Two vetted options:
- **youtube-direct** (recommended): Custom-built, uses official Google API, no third parties
- **youtube-full** (alternative): TranscriptAPI service, simpler setup, cloud-friendly

---

## Documentation Conventions

### Markdown Style

1. **Headings**: Use ATX-style (`#` headers)
2. **Code blocks**: Always specify language (```bash, ```javascript, ```json)
3. **Tables**: Use standard markdown tables with aligned columns
4. **Links**: Use relative links for internal docs, absolute for external
5. **Emojis**: Use sparingly for visual navigation (🍎, 🐧, ⭐, ✅, ⚠️)

### Structure Patterns

#### Deployment Guides (PLAN_*.md)

Standard sections:
1. Overview
2. Architecture
3. Prerequisites
4. Phase-by-phase deployment steps
5. Security hardening
6. Operational maintenance
7. Troubleshooting
8. References

#### Skill Documentation

Each skill should have:
- **README.md**: Setup, usage, troubleshooting
- **SKILL.md**: OpenClaw-specific skill definition
- **Security review document**: If third-party

### Command Examples

Always include:
- Clear descriptions of what commands do
- Expected output samples
- Error handling guidance
- Platform-specific variations when applicable

Example format:
```bash
# Install dependencies
npm install

# Expected output:
# added 47 packages, and audited 48 packages in 2s
```

---

## Working with This Project

### When Updating Deployment Plans

1. **Update ALL affected files**: If a change applies to both platforms, update both PLAN_MACOS.md and PLAN_UBUNTU.md
2. **Keep PLAN.md in sync**: Update the overview if adding major features
3. **Check cross-references**: Ensure all links between documents remain valid
4. **Update PROJECT_STATUS.md**: Reflect current state and decisions

### When Adding New Skills

1. **Place in pending-review/** initially
2. **Create security review document**: See `skills/pending-review/YOUTUBE_SKILLS_SECURITY_REVIEW.md` as template
3. **Document in SKILL_COMPARISON.md**: Add comparison with alternatives
4. **After vetting, move to vetted/**: Update references in deployment plans

### When Reviewing Third-Party Skills

Follow this process:
1. Clone skill repository to `skills/pending-review/[skill-name]/`
2. Create security review document
3. Check for:
   - Dangerous code patterns (dynamic code execution, shell injection)
   - Hardcoded secrets
   - Unexpected network calls
   - Supply chain risks (npm audit)
4. Document findings and recommendation
5. If approved, update deployment plans with installation instructions

### Security Review Requirements

**Critical checks**:
- [ ] No dynamic code execution with external data
- [ ] No hardcoded API keys or secrets
- [ ] Network calls only to documented endpoints
- [ ] Input validation present
- [ ] Dependencies scanned (npm audit)
- [ ] VirusTotal scan if binary/compiled code

**Red flags**:
- Obfuscated code
- Cryptocurrency mining
- Undocumented network requests
- Excessive permissions
- Supply chain concerns

---

## Common Tasks

### Add a New Platform-Specific Tip

1. Identify which guide(s) need the tip
2. Find appropriate section (usually troubleshooting or platform-specific tips)
3. Add with clear heading and example
4. Update table of contents if section is new

### Update Container Runtime Recommendations

1. Edit PLAN_MACOS.md section 4.4 (container runtime options)
2. Update pros/cons in the comparison table
3. Verify recommendation still matches in PLAN.md overview
4. Update PROJECT_STATUS.md decision matrix

### Add New Skill Vetting Process Step

1. Update SKILL_VETTING_GUIDE.md with new step
2. Apply to existing reviews in skills/pending-review/
3. Document rationale in PROJECT_STATUS.md

### Fix Broken Links

1. Search for the old link pattern: `grep -r "old-link" *.md`
2. Update in all locations
3. Test with markdown preview or link checker
4. Commit with clear message about link update

---

## Code Style Guidelines

### Shell Scripts (Bash)

```bash
# Use clear variable names
BACKUP_DIR="/path/to/backup"

# Quote variables to handle spaces
cd "$BACKUP_DIR"

# Use functions for reusability
function backup_config() {
    local config_file="$1"
    tar czf "backup-$(date +%F).tar.gz" "$config_file"
}

# Error handling
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backup directory not found" >&2
    exit 1
fi
```

### JavaScript (Node.js Skills)

```javascript
// Use modern async/await
async function fetchTranscript(videoId) {
    try {
        const response = await api.getTranscript(videoId);
        return response.data;
    } catch (error) {
        throw new Error(`Failed to fetch transcript: ${error.message}`);
    }
}

// Validate input
function validateVideoId(id) {
    if (!/^[a-zA-Z0-9_-]{11}$/.test(id)) {
        throw new Error('Invalid video ID format');
    }
    return id;
}

// Use descriptive error messages
if (!apiKey) {
    throw new Error('YouTube API key not found. Set YOUTUBE_API_KEY environment variable.');
}
```

### Configuration Files (JSON)

```json
{
    "skill_name": "youtube-direct",
    "version": "1.0.0",
    "description": "Brief, clear description",
    "dependencies": {
        "googleapis": "^140.0.0"
    }
}
```

---

## Testing Changes

### Before Committing Documentation

1. **Spellcheck**: Run through a spellchecker
2. **Link check**: Verify all relative links work
3. **Code examples**: Test commands in relevant environment
4. **Markdown rendering**: Preview in GitHub-compatible renderer
5. **Cross-references**: Check related documents are consistent

### Before Committing Code (Skills)

1. **Syntax check**: `node --check script.js`
2. **Dependency audit**: `npm audit`
3. **Local test**: Run in isolated environment
4. **Documentation**: Ensure README reflects changes

---

## Git Workflow

### Commit Message Format

```
Brief summary line (50 chars max)

- Bullet point for each major change
- Be specific about files and sections affected
- Include context for why, not just what

Co-Authored-By: Claude Sonnet 4.5 (1M context) <noreply@anthropic.com>
```

### When to Create Branches

This is primarily a documentation project, so main branch commits are acceptable for:
- Documentation updates
- Security reviews
- Skill additions to pending-review/

Consider branches for:
- Major restructuring
- Experimental skill implementations
- Large-scale content rewrites

---

## OpenClaw-Specific Context

### Skill Format

OpenClaw skills use the Agent Skills format:
- **SKILL.md**: Main skill documentation with frontmatter
- **scripts/**: Executable scripts called by the agent
- **user-invocable: true**: Skill can be triggered directly by users

### Gateway Configuration

- Always bind to `127.0.0.1` (localhost only)
- Never expose to public internet without explicit user choice
- Remote access via Tailscale or SSH tunnel only

### Security Model

Defense in depth:
1. Network isolation (localhost binding)
2. Container isolation (read-only filesystems)
3. Skill vetting (source code review)
4. Secret management (keychain/pass)
5. Content sandboxing (untrusted external content)

---

## External References

### OpenClaw Documentation

- [Official Docs](https://docs.openclaw.ai)
- [GitHub Repository](https://github.com/openclaw/openclaw)
- [Security Guide](https://docs.openclaw.ai/gateway/security)
- [ClawHub Skills](https://clawhub.ai)

### YouTube API

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Quotas](https://developers.google.com/youtube/v3/getting-started#quota)

### Container Runtimes

- [OrbStack](https://orbstack.dev) - macOS recommended
- [Docker Desktop](https://docker.com) - Cross-platform
- [Podman](https://podman.io) - Rootless, security-focused

---

## Troubleshooting Common Issues

### "Skills section not updating"

- Check if both PLAN_MACOS.md and PLAN_UBUNTU.md were updated
- Verify section numbers match across files
- Search for skill name across all files to catch references

### "Link not working"

- Use relative links: `./PLAN_MACOS.md` not `/PLAN_MACOS.md`
- GitHub flavored markdown: `[Link Text](./file.md)` not `[Link Text](file.md)`
- Test links in GitHub preview

### "Code example fails"

- Test in relevant platform (macOS vs Ubuntu)
- Check environment variables are documented
- Verify paths are correct for platform
- Escape special characters properly

---

## Project Principles

1. **Security First**: Vet all third-party code, default to paranoid
2. **Privacy Focused**: Prefer direct APIs over third-party services
3. **User Empowerment**: Give users choice with clear trade-offs
4. **Documentation Quality**: Clear, tested, maintainable instructions
5. **Platform-Specific**: Don't assume one size fits all
6. **Open & Transparent**: Document security reviews, share findings

---

## Questions? Unsure?

When working on this project:

- **Security concern?** → Default to more secure option, document trade-offs
- **Platform difference?** → Check both PLAN_MACOS.md and PLAN_UBUNTU.md
- **Third-party skill?** → Review code first, document findings
- **Breaking change?** → Update all affected files, test examples
- **Unclear instruction?** → Clarify in documentation, don't assume

This is a living document. Update it as patterns emerge and the project evolves.

---

**Last Updated**: 2026-02-15
**Project Status**: Ready for deployment, actively maintained
