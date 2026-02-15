---
name: youtube-direct
description: Direct YouTube Data API v3 integration for transcripts, metadata, and search. No third-party services - uses official Google APIs. Requires Google Cloud project setup but provides full control and privacy.
homepage: https://developers.google.com/youtube/v3
user-invocable: true
---

# YouTube Direct (Official API)

Direct integration with YouTube Data API v3 and Caption API. No intermediary services.

## Features

- **Video Transcripts** - Fetch captions/subtitles directly from YouTube
- **Video Metadata** - Titles, descriptions, view counts, thumbnails
- **Search** - Search YouTube videos and channels
- **Channel Data** - Channel info, latest uploads, video lists
- **Playlist Data** - Extract all videos from playlists
- **Privacy** - All data flows directly between you and Google

## Setup

### Step 1: Create Google Cloud Project (One-time)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable APIs:
   - YouTube Data API v3
   - YouTube Analytics API (optional)
4. Create credentials:
   - Navigate to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app" or "Web application"
   - Download the JSON file

### Step 2: Configure Authentication

```bash
# Set up OAuth credentials
node ./scripts/setup-auth.js --credentials /path/to/client_secret.json

# This will:
# 1. Start a local server for OAuth callback
# 2. Open browser for Google sign-in
# 3. Save refresh token securely
```

Alternatively, use API key for read-only operations (search, metadata):

```bash
# API Key (simpler, but limited functionality - no captions)
export YOUTUBE_API_KEY="your-api-key-here"
```

### Step 3: Verify Setup

```bash
# Test the configuration
node ./scripts/test-connection.js
```

## Usage

### Get Video Transcript

```bash
# Full transcript with timestamps
node ./scripts/get-transcript.js --video dQw4w9WgXcQ --format json

# Plain text only
node ./scripts/get-transcript.js --video dQw4w9WgXcQ --format text

# Specify language (default: auto-detect)
node ./scripts/get-transcript.js --video dQw4w9WgXcQ --lang en
```

**Output**:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "language": "en",
  "transcript": [
    { "text": "Never gonna give you up", "start": 0.0, "duration": 2.5 },
    { "text": "Never gonna let you down", "start": 2.5, "duration": 2.8 }
  ]
}
```

### Search Videos

```bash
# Search for videos
node ./scripts/search.js --query "machine learning tutorial" --type video --limit 10

# Search for channels
node ./scripts/search.js --query "MIT OpenCourseWare" --type channel --limit 5
```

### Get Channel Videos

```bash
# Latest uploads from a channel
node ./scripts/channel-videos.js --channel UCBcRF18a7Qf58cCRy5xuWwQ --limit 20

# Or use channel handle
node ./scripts/channel-videos.js --handle @TED --limit 15
```

### Get Playlist Videos

```bash
# Extract all videos from a playlist
node ./scripts/playlist-videos.js --playlist PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
```

## API Quotas

YouTube Data API v3 has daily quotas:

| Operation | Cost (units) | Default Quota |
|-----------|--------------|---------------|
| Search | 100 | 10,000/day |
| Video details | 1 | 10,000/day |
| Caption download | 200 | 10,000/day |
| Channel details | 1 | 10,000/day |
| Playlist items | 1 | 10,000/day |

**Default quota**: 10,000 units/day (free)
**Calculation**: 50 captions + 100 searches + 500 video details = ~9,900 units

**Request quota increase**: [Google Cloud Console](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)

## Authentication Methods

### OAuth 2.0 (Recommended for Full Access)

**Required for**:
- Caption/transcript download
- Private video access
- User-specific data

**Setup**: Follow Step 2 above

### API Key (Limited)

**Allowed for**:
- Public video metadata
- Search
- Channel info (public)
- Playlist info (public)

**NOT allowed for**:
- Captions/transcripts
- Private videos

**Setup**:
```bash
export YOUTUBE_API_KEY="AIza..."
```

## Configuration Files

```
~/.openclaw/skills/youtube-direct/
├── credentials/
│   ├── client_secret.json    (OAuth credentials from Google)
│   └── tokens.json            (OAuth refresh tokens - auto-generated)
└── config.json                (Skill configuration)
```

**Security**: `credentials/` directory has `0700` permissions, files have `0600`.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `quotaExceeded` | Daily quota limit reached | Wait until quota resets (midnight PST), or request increase |
| `forbidden` | OAuth scope insufficient | Re-run setup-auth.js with correct scopes |
| `videoNotFound` | Invalid video ID | Check video exists and is not private/deleted |
| `captionsDisabled` | Video has no captions | Not all videos have captions available |
| `authError` | OAuth token expired | Refresh token automatically or re-authenticate |

## Privacy & Data

**Data flows**:
- Your machine ↔ Google YouTube API (direct)
- No intermediary services
- No data stored by third parties

**Credentials stored locally**:
- `~/.openclaw/skills/youtube-direct/credentials/`
- Only you have access

**Google's data usage**:
- Subject to [Google API Terms of Service](https://developers.google.com/terms)
- [YouTube API Services Terms](https://developers.google.com/youtube/terms/api-services-terms-of-service)

## Comparison to TranscriptAPI

| Feature | YouTube Direct (this) | TranscriptAPI |
|---------|----------------------|---------------|
| Third-party service | ❌ No | ✅ Yes |
| Cost | Free (10k quota/day) | $5/mo (1000 credits) |
| Setup complexity | Medium (OAuth) | Low (email + OTP) |
| Privacy | Direct to Google | Via TranscriptAPI.com |
| Reliability | Official API | High (specialized service) |
| Cloud IP support | May be limited | ✅ Always works |
| Quota limits | 10k units/day | 1000 transcripts/mo (paid) |

## Troubleshooting

### "Cannot download captions with API key"

**Cause**: API keys don't have permission for captions.
**Solution**: Use OAuth 2.0 instead (run `setup-auth.js`).

### "OAuth consent screen not configured"

**Cause**: Google Cloud project needs consent screen setup.
**Solution**:
1. Go to [Console](https://console.cloud.google.com/)
2. APIs & Services → OAuth consent screen
3. Configure (can use "Testing" mode for personal use)

### "Quota exceeded"

**Cause**: Used more than 10,000 units today.
**Solution**:
- Wait until midnight Pacific Time
- Request quota increase (free)
- Optimize queries (cache results)

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test

# Lint code
npm run lint
```

## References

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube Caption API](https://developers.google.com/youtube/v3/docs/captions)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [API Quotas](https://developers.google.com/youtube/v3/getting-started#quota)
