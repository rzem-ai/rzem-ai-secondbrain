# YouTube Direct - Official API Integration

✅ **Security Reviewed & Approved** - No third-party services, direct Google API access

## Overview

This skill provides YouTube functionality using the official Google YouTube Data API v3. Unlike third-party services, all data flows directly between your machine and Google.

**What you get:**
- ✅ Video transcripts (captions/subtitles)
- ✅ Video metadata (titles, descriptions, stats)
- ✅ Search (videos, channels, playlists)
- ✅ Channel data and uploads
- ✅ Playlist extraction
- ✅ Complete privacy (no third parties)
- ✅ Free quota (10,000 units/day)

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/alex/Dev/Work/ai/rzem-ai-secondbrain/skills/vetted/youtube-direct
npm install
```

### 2. Get Google Cloud Credentials

**Option A: Step-by-step in Google Cloud Console**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable APIs:
   - Click "Enable APIs and Services"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create OAuth credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Configure Consent Screen"
     - User type: External
     - App name: "YouTube Direct Skill"
     - User support email: (your email)
     - Developer contact: (your email)
     - Click "Save and Continue"
     - Scopes: Skip (default is fine)
     - Test users: Add your email
     - Click "Save and Continue"
   - Back to "Credentials" tab
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "YouTube Direct CLI"
   - Click "Create"
   - Download JSON file

**Option B: Quick links**

- [Enable YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com)
- [Create OAuth Client](https://console.cloud.google.com/apis/credentials/oauthclient)

### 3. Authenticate

```bash
# Run the setup script with your downloaded credentials
node scripts/setup-auth.js --credentials ~/Downloads/client_secret_*.json

# This will:
# 1. Open your browser for Google sign-in
# 2. Request YouTube API permissions
# 3. Save authentication tokens securely
```

### 4. Test It Works

```bash
# Run the test suite
npm test

# Or manually test
node scripts/search.js --query "test" --limit 1
```

## Usage Examples

### Get Video Transcript

```bash
# By video ID
node scripts/get-transcript.js --video dQw4w9WgXcQ --format text

# By full URL
node scripts/get-transcript.js --video "https://youtube.com/watch?v=dQw4w9WgXcQ" --format json

# Specific language
node scripts/get-transcript.js --video dQw4w9WgXcQ --lang es
```

**Output (JSON)**:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up (Official Video)",
  "channel": "Rick Astley",
  "language": "en",
  "is_auto_generated": false,
  "transcript": [
    {
      "text": "We're no strangers to love",
      "start": 18.0,
      "duration": 2.5
    }
  ]
}
```

### Search Videos

```bash
# Search for videos
node scripts/search.js --query "python tutorial" --type video --limit 10

# Search for channels
node scripts/search.js --query "MIT OpenCourseWare" --type channel --limit 5
```

### From OpenClaw Agent

When using with OpenClaw, the agent can call these scripts directly:

```
User: "Get me the transcript of https://youtube.com/watch?v=dQw4w9WgXcQ"

Agent executes:
node ~/.openclaw/skills/youtube-direct/scripts/get-transcript.js \
  --video dQw4w9WgXcQ --format json
```

## API Quota Management

YouTube Data API v3 has a daily quota of **10,000 units**.

### Cost per operation:
- Search: 100 units (~100 searches/day)
- Get video details: 1 unit (~10,000/day)
- Download caption: 200 units (~50 transcripts/day)
- List playlist items: 1 unit (~10,000/day)

### Typical daily usage:
- 50 transcripts = 10,000 units ✓ Fits quota
- 100 searches = 10,000 units ✓ Fits quota
- 20 transcripts + 50 searches = 9,000 units ✓ Fits quota

### Request quota increase:
If you need more, request an increase (free):
1. Go to [Quotas page](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)
2. Click "Queries per day"
3. Click "Edit Quotas"
4. Request increase (usually approved within 24-48 hours)

## Security

**Credentials stored locally:**
```
~/.openclaw/skills/youtube-direct/credentials/
├── client_secret.json    (OAuth app credentials)
└── tokens.json           (Your personal access tokens)
```

**Permissions**: `0700` (directory), `0600` (files) - only you can read them.

**Refresh tokens**: Automatically refreshed when expired. No manual intervention needed.

**Revoke access**: [Google Account Permissions](https://myaccount.google.com/permissions)

## Troubleshooting

### "OAuth credentials not configured"

You need to run the setup first:
```bash
node scripts/setup-auth.js --credentials /path/to/client_secret.json
```

### "Captions require OAuth2 authentication"

API keys can't access captions. You must use OAuth (full setup).

### "quotaExceeded"

You've used your daily quota (10,000 units). Solutions:
1. Wait until midnight Pacific Time (quota resets)
2. Request quota increase (free, usually approved)
3. Optimize queries (cache results, reduce redundant calls)

### "redirect_uri_mismatch"

Your OAuth client needs redirect URI: `http://localhost:3000/oauth2callback`

Fix:
1. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
2. Click your OAuth client
3. Add `http://localhost:3000/oauth2callback` to "Authorized redirect URIs"
4. Save and re-run setup

### "Invalid grant" or "Token expired"

Your OAuth tokens have expired. Re-authenticate:
```bash
node scripts/setup-auth.js --credentials ~/.openclaw/skills/youtube-direct/credentials/client_secret.json
```

## Comparison: YouTube Direct vs. TranscriptAPI

| Feature | YouTube Direct (this) | TranscriptAPI |
|---------|----------------------|---------------|
| **Privacy** | ✓ Direct to Google | Via third-party |
| **Cost** | Free (10k/day quota) | $5/mo (1000 credits) |
| **Setup** | Medium (OAuth) | Easy (email + OTP) |
| **Dependencies** | Google only | TranscriptAPI.com |
| **Cloud IPs** | May be limited† | Always works |
| **Quota** | 10k units/day | 1000/month (paid) |
| **Control** | Full API access | Limited to service |

† YouTube may rate-limit some cloud/VPS IPs. Usually fine for personal/residential use.

## Files Structure

```
youtube-direct/
├── SKILL.md                 # Skill documentation (for OpenClaw)
├── README.md                # This file
├── package.json             # Dependencies
├── lib/
│   └── youtube-client.js    # Core API wrapper
├── scripts/
│   ├── setup-auth.js        # OAuth setup
│   ├── get-transcript.js    # Fetch transcripts
│   ├── search.js            # Search videos/channels
│   └── test-connection.js   # Test setup
└── credentials/             # OAuth credentials (auto-created)
    ├── client_secret.json
    └── tokens.json
```

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test

# Format code
npm run format  # (if configured)
```

## Support

**YouTube API Documentation**: https://developers.google.com/youtube/v3

**Google Cloud Console**: https://console.cloud.google.com/

**Report issues**: File an issue in this repository

## License

MIT License - See LICENSE file
