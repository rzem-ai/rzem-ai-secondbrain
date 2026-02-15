# OpenClaw "Second Brain"

An AI-powered personal knowledge management system built on [OpenClaw](https://github.com/openclaw/openclaw). Deployable on macOS or Ubuntu/Linux with comprehensive security and privacy controls.

## What It Does

This project turns OpenClaw into a personal knowledge management system that:

- **Receives messages** from your preferred channels (Telegram, WhatsApp, Slack, etc.)
- **Reads and categorises** each message automatically — extracting topics, entities, and intent
- **Follows links** when a message contains a URL, fetching and summarising the content (articles, blog posts, YouTube transcripts, etc.)
- **Stores structured records** in Markdown (compatible with Obsidian) with timestamps, categories, summaries, and source material
- **Sends twice-daily email digests** (morning and evening) summarising everything captured in the last 12 hours
- **Sends a weekly digest** every Sunday with category breakdowns, top items, trends, and outstanding action items

## Architecture

```
Messages in (Telegram / WhatsApp / Slack / …)
        │
        ▼
   OpenClaw Gateway (localhost-only, containerised)
        │
        ├─ Plain text → Categorise → Store record
        └─ URL → Fetch content / extract transcript → Summarise → Categorise → Store record
        │
        ▼
   Cron scheduler → Email digests (2× daily + weekly)
```

## Security

The system is designed with security as a priority:

- Runs under a dedicated non-root user inside a rootless Podman container
- Gateway bound to `127.0.0.1` only — never exposed to the public internet
- Remote access via Tailscale or SSH tunnel only
- All skills source-code reviewed before installation
- API keys managed via a secret manager with monthly rotation
- External content treated as untrusted to guard against prompt injection

## Getting Started

Choose your deployment platform:

- **🍎 [macOS Deployment](./PLAN_MACOS.md)** - Optimized for Apple Silicon Macs (M1/M2/M3)
  - Best for: Personal use, privacy-first, laptop battery efficiency
  - Container: OrbStack (lightweight, native optimization)
  - Setup time: ~2-3 hours

- **🐧 [Ubuntu/Linux Deployment](./PLAN_UBUNTU.md)** - For VPS/cloud hosting
  - Best for: Always-on deployments, remote access, team usage
  - Container: Rootless Podman (maximum security)
  - Setup time: ~3-4 hours

**Start here**: [PLAN.md](./PLAN.md) - Overview and platform comparison

## Project Structure

```
├── PLAN.md                    # Overview and platform guide
├── PLAN_MACOS.md              # macOS deployment (M1/M2/M3)
├── PLAN_UBUNTU.md             # Ubuntu/Linux deployment
├── SKILL_VETTING_GUIDE.md     # How to review skills
├── skills/
│   ├── SKILL_COMPARISON.md    # YouTube skill options
│   ├── vetted/
│   │   └── youtube-direct/    # Custom YouTube API skill
│   └── pending-review/
│       └── youtube-summarizer/ # TranscriptAPI alternative
└── PROJECT_STATUS.md          # Current progress and decisions
```

## License

[MIT](LICENSE)