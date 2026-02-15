# rzem-ai-secondbrain

An AI-powered "Second Brain" built on [OpenClaw](https://github.com/openclaw/openclaw), securely self-hosted on Ubuntu.

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

See [PLAN.md](PLAN.md) for the full implementation plan covering installation, configuration, and operational maintenance.

## License

[MIT](LICENSE)