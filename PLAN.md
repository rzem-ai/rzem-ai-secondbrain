# OpenClaw "Second Brain" — Deployment Plans

> **A personal AI knowledge management system that receives messages, extracts content, categorizes information, and delivers automated digests.**

---

## Choose Your Platform

Select the deployment guide for your environment:

### 🍎 [macOS Deployment](./PLAN_MACOS.md) (Recommended for Personal Use)

**Target**: Apple Silicon Macs (M1/M2/M3), residential/home deployment

**Ideal For**:
- Personal knowledge management
- Home/office use
- Privacy-first approach
- Maximum battery efficiency (laptops)

**Highlights**:
- Native Apple Silicon optimization
- OrbStack container runtime (lightweight, fast)
- macOS-specific integrations (Keychain, LaunchAgent, Shortcuts)
- Battery optimization tips
- Direct YouTube API integration (no third parties)

**Setup Time**: ~2-3 hours (including Google Cloud OAuth)

**👉 [View macOS Deployment Plan →](./PLAN_MACOS.md)**

---

### 🐧 [Ubuntu/Linux Deployment](./PLAN_UBUNTU.md) (VPS/Cloud Optimized)

**Target**: Ubuntu Server 22.04 LTS, VPS/cloud hosting, headless deployments

**Ideal For**:
- Always-on deployments
- Remote access scenarios
- Team/shared usage
- Cloud/VPS environments

**Highlights**:
- Rootless Podman security
- UFW firewall configuration
- SSH hardening & key-only authentication
- Tailscale mesh networking
- Systemd service management
- Remote access via SSH tunneling

**Setup Time**: ~3-4 hours (including security hardening)

**👉 [View Ubuntu Deployment Plan →](./PLAN_UBUNTU.md)**

---

## Quick Comparison

| Feature | macOS | Ubuntu/Linux |
|---------|-------|--------------|
| **Container Runtime** | OrbStack (recommended) | Rootless Podman |
| **Auto-Start** | LaunchAgent | Systemd service |
| **Secret Storage** | macOS Keychain | Pass/1Password CLI |
| **Remote Access** | Tailscale/local only | Tailscale/SSH tunnel |
| **Security Model** | User-level isolation | Rootless containers + UFW |
| **Battery Considerations** | Optimized for laptops | N/A (server) |
| **Network** | Residential IP-friendly | May need proxy for YouTube |
| **Best For** | Personal use, privacy | Always-on, remote access |

---

## What is "Second Brain"?

The OpenClaw Second Brain is an AI agent that acts as your personal knowledge management system:

### Core Functionality

```
Incoming Messages (WhatsApp/Telegram/Slack/etc.)
    ↓
OpenClaw Agent (localhost-bound)
    ↓
Content Extraction
├── Plain text → Categorize
├── YouTube links → Extract transcript → Summarize
├── Web links → Fetch content → Summarize
└── Store in memory with metadata
    ↓
Automated Email Digests
├── Morning digest (08:00)
├── Evening digest (20:00)
└── Weekly summary (Sunday 09:00)
```

### Features

- **Message Ingestion**: Receive from multiple channels
- **Content Extraction**: YouTube transcripts, web articles, link summaries
- **Intelligent Categorization**: Work, Personal, Learning, News, etc.
- **Memory Storage**: Markdown files compatible with Obsidian
- **Automated Digests**: Twice-daily summaries + weekly overview
- **Privacy-First**: Localhost-only deployment, no data leaves your control
- **Security Hardened**: Container isolation, vetted skills, prompt injection defenses

---

## Prerequisites (All Platforms)

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4 GB | 8 GB+ (16 GB for M3 Macs) |
| **Disk** | 20 GB free | 100 GB+ |
| **Node.js** | v22+ | Latest LTS |
| **Container Runtime** | Docker/Podman | Platform-specific (see guides) |
| **LLM API Key** | Any supported | Anthropic Claude Opus 4.6 |

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│              Messaging Channels                        │
│  (WhatsApp / Telegram / Slack / Signal / Discord)      │
└─────────────────────┬──────────────────────────────────┘
                      │ incoming messages
                      ▼
┌─────────────────────┴──────────────────────────────────┐
│              OpenClaw Gateway                          │
│         (bound to 127.0.0.1 only)                      │
│                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Message      │→ │ Content      │→ │ Category &   │ │
│  │ Router       │  │ Extractor    │  │ Record Store │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                 │                   │        │
│         │                 ▼                   ▼        │
│         │          ┌──────────┐      ┌────────────┐   │
│         │          │ YouTube  │      │  Memory    │   │
│         │          │ Link     │      │ ~/.openclaw│   │
│         │          │ Reader   │      │  /memory/  │   │
│         │          └──────────┘      └────────────┘   │
│         │                 │                   │        │
│         │                 ▼                   ▼        │
│  ┌──────┴─────────────────┴───────────────────┴─────┐ │
│  │              Cron Scheduler                      │ │
│  │  • 08:00 — Morning summary email                │ │
│  │  • 20:00 — Evening summary email                │ │
│  │  • Sunday 09:00 — Weekly digest email           │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Skills & Components

### Required Skills

| Skill | Purpose | Installation |
|-------|---------|--------------|
| **youtube-direct** ⭐ | YouTube transcripts via official Google API | Custom (see platform guides) |
| **youtube-full** | Alternative: TranscriptAPI service | `npx clawhub@latest install youtube-full` |
| **summarize** | Summarize URLs, articles, files | `npx clawhub@latest install summarize` |
| **gog** or **gmail** | Email sending for digests | `npx clawhub@latest install gog` |

> **YouTube Skill Choice**: `youtube-direct` recommended for privacy and cost (free, 10k API units/day). `youtube-full` alternative for simpler setup or cloud/VPS IPs.
>
> **Security**: All skills vetted. See [`skills/SKILL_COMPARISON.md`](./skills/SKILL_COMPARISON.md) for detailed analysis.

### Memory Storage Structure

```
~/.openclaw/memory/
├── records/                    # Individual message records
│   ├── 2026-02-15_work_project-update.md
│   ├── 2026-02-15_learning_yt-ml-lecture.md
│   └── ...
├── categories/                 # Category indexes
│   ├── work.md
│   ├── learning.md
│   └── ...
├── transcripts/                # YouTube transcripts
│   └── 2026-02-15_yt_abc123.md
└── digests/                    # Email digest archives
    ├── 2026-02-15_morning.md
    ├── 2026-02-15_evening.md
    └── 2026-W07_weekly.md
```

**Obsidian Integration**: Point Obsidian to `~/.openclaw/memory/` for visual browsing and graph view.

---

## Security Model

### Defense in Depth

1. **Network Isolation**
   - Gateway bound to `127.0.0.1` only
   - No external ports exposed
   - Remote access via Tailscale or SSH tunnel

2. **Container Isolation**
   - Run in read-only containers
   - Resource limits (CPU, memory)
   - Separate container network

3. **Skill Vetting**
   - All skills reviewed before installation
   - Source code inspection
   - Dependency analysis
   - See [`SKILL_VETTING_GUIDE.md`](./SKILL_VETTING_GUIDE.md)

4. **Secret Management**
   - API keys in secure storage (Keychain/Pass)
   - Monthly rotation
   - Log redaction enabled

5. **Content Sandboxing**
   - All external content treated as untrusted
   - No code execution from fetched data
   - Prompt injection defenses

### Security Checklists

Each platform guide includes a comprehensive security checklist covering:
- ✅ File permissions and encryption
- ✅ Network configuration
- ✅ Authentication and secrets
- ✅ Container isolation
- ✅ Monitoring and logging
- ✅ Backup and recovery

---

## Deployment Phases (High-Level)

### Phase 1: Prerequisites & Base Setup
- Install OS-specific dependencies
- Configure container runtime
- Enable security features

### Phase 2: OpenClaw Installation
- Install OpenClaw globally
- Run setup wizard
- Configure LLM provider

### Phase 3: Skills Setup
- Install YouTube skill (youtube-direct or youtube-full)
- Install content summarizer
- Configure email integration

### Phase 4: Second Brain Configuration
- Define agent identity and behavior
- Set up memory structure
- Configure categorization rules

### Phase 5: Automated Digests
- Schedule cron jobs for email summaries
- Test digest delivery
- Configure email templates

### Phase 6: Security Hardening
- Container deployment
- Secret storage
- Log redaction
- Backup automation

### Phase 7: Monitoring & Maintenance
- Health checks
- Disk usage alerts
- Update procedures

**Detailed steps in platform-specific guides.**

---

## Estimated Costs

### Free Tier (Recommended for Personal Use)

- **OpenClaw**: Free (open source)
- **YouTube API**: Free (10,000 units/day ≈ 50 transcripts)
- **Claude API**: Pay-per-use (estimate $10-30/month for moderate usage)
- **Infrastructure**: $0 (local) or $5-10/month (VPS)

### Optional Paid Services

- **TranscriptAPI** (alternative): $5/month (1,000 credits)
- **VPS Hosting**: $5-20/month (Hetzner, DigitalOcean, etc.)
- **Domain Name**: $10-15/year (if hosting remotely)

---

## Success Criteria

The Second Brain is successfully deployed when:

- ✅ Messages arrive and are processed automatically
- ✅ YouTube transcripts extract correctly
- ✅ Web links fetch and summarize
- ✅ Content categorized and stored in memory
- ✅ Morning digest delivered daily at 08:00
- ✅ Evening digest delivered daily at 20:00
- ✅ Weekly digest delivered Sunday at 09:00
- ✅ System auto-starts after reboot
- ✅ All security checklist items completed
- ✅ Backups verified and restorable

---

## Documentation & Support

### Local Documentation

- **[macOS Deployment Guide](./PLAN_MACOS.md)** - Apple Silicon, personal use
- **[Ubuntu Deployment Guide](./PLAN_UBUNTU.md)** - Linux, VPS, cloud
- **[Skill Vetting Guide](./SKILL_VETTING_GUIDE.md)** - How to review skills
- **[Skill Comparison](./skills/SKILL_COMPARISON.md)** - YouTube options analysis
- **[YouTube Direct Skill](./skills/vetted/youtube-direct/README.md)** - Custom skill setup
- **[Project Status](./PROJECT_STATUS.md)** - Current state and decisions

### External Resources

- [OpenClaw Official Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [3-Tier Security Hardening](https://aimaker.substack.com/p/openclaw-security-hardening-guide)

### Community

- [OpenClaw Discord](https://discord.gg/openclaw)
- [OpenClaw Reddit](https://reddit.com/r/openclaw)
- [ClawHub Skills](https://clawhub.ai)

---

## Next Steps

1. **Choose your platform**: [macOS](./PLAN_MACOS.md) or [Ubuntu/Linux](./PLAN_UBUNTU.md)
2. **Review prerequisites** in the platform guide
3. **Follow the phase-by-phase deployment**
4. **Complete security checklist**
5. **Test all functionality**
6. **Set up monitoring**

---

## Troubleshooting

Common issues and solutions are documented in each platform guide:

- OAuth authentication failures
- YouTube API quota issues
- Container networking problems
- Email delivery failures
- Cron job reliability
- Disk space management

See the **Troubleshooting** section in your platform-specific guide.

---

## Contributing

Found an issue or have an improvement?

- **Security vulnerabilities**: Email privately or use GitHub Security Advisories
- **Bugs/improvements**: Open an issue in this repository
- **Documentation updates**: Submit a pull request
- **Share your setup**: Contribute your configuration to help others

---

## License

This project documentation is provided as-is for educational and deployment purposes. OpenClaw itself is governed by its own license (see [OpenClaw repository](https://github.com/openclaw/openclaw)).

---

**Ready to deploy?** Choose your platform:
- 🍎 **[macOS Deployment →](./PLAN_MACOS.md)**
- 🐧 **[Ubuntu Deployment →](./PLAN_UBUNTU.md)**
