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

```text
/
├── README.md                       # Project introduction and navigation
├── PLAN.md                         # Overview with platform comparison
├── PLAN_MACOS.md                   # Apple Silicon (M1/M2/M3) deployment
├── PLAN_UBUNTU.md                  # Ubuntu/Linux VPS deployment
├── SKILL_VETTING_GUIDE.md         # (Draft) Comprehensive skill review process
├── PROJECT_STATUS.md              # (Draft) Current state and decisions
│
├── docs/                           # Detailed guidelines for contributors
│   ├── working-with-project.md     # Workflows for updates and reviews
│   ├── common-tasks.md             # Step-by-step task instructions
│   ├── code-style.md               # Coding standards (Bash, JS, JSON)
│   ├── testing.md                  # Pre-commit checklists
│   ├── git-workflow.md             # Commit format and branching
│   ├── openclaw-context.md         # OpenClaw-specific guidance
│   ├── external-references.md      # Quick links to external docs
│   ├── troubleshooting.md          # Common problem solutions
│   ├── project-principles.md       # Core values and principles
│   └── questions-guide.md          # Quick decision guide
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

```text
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
2. **Code blocks**: Always specify language (```bash,```javascript, ```json)
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

See [docs/working-with-project.md](./docs/working-with-project.md) for detailed guidance on updating deployment plans, adding new skills, conducting security reviews, and understanding security review requirements.

## Common Tasks

See [docs/common-tasks.md](./docs/common-tasks.md) for step-by-step instructions for frequent operations like adding platform-specific tips, updating container runtime recommendations, adding skill vetting process steps, and fixing broken links.

## Code Style Guidelines

See [docs/code-style.md](./docs/code-style.md) for coding standards covering shell scripts (Bash), JavaScript (Node.js skills), and configuration files (JSON).

## Testing Changes

See [docs/testing.md](./docs/testing.md) for pre-commit checklists to ensure quality before committing documentation and code changes.

## Git Workflow

See [docs/git-workflow.md](./docs/git-workflow.md) for commit message format guidelines and branching strategy for this project.

## OpenClaw-Specific Context

See [docs/openclaw-context.md](./docs/openclaw-context.md) for details on OpenClaw's skill format, gateway configuration requirements, and security model principles.

## External References

See [docs/external-references.md](./docs/external-references.md) for quick links to OpenClaw documentation, YouTube API resources, and container runtime information.

## Troubleshooting Common Issues

See [docs/troubleshooting.md](./docs/troubleshooting.md) for solutions to common problems like skills section not updating, broken links, and code examples that fail.

## Project Principles

See [docs/project-principles.md](./docs/project-principles.md) for the core values guiding this project: Security First, Privacy Focused, User Empowerment, Documentation Quality, Platform-Specific approach, and Open & Transparent practices.

## Questions? Unsure?

See [docs/questions-guide.md](./docs/questions-guide.md) for a quick decision guide to help navigate common scenarios when working on this project.

---

**Last Updated**: 2026-02-15
**Project Status**: Ready for deployment, actively maintained
