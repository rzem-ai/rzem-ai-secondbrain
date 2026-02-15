# Code Style Guidelines

> Part of the [OpenClaw Second Brain CLAUDE.md](../CLAUDE.md) documentation

Coding standards for shell scripts, JavaScript, and configuration files in this project.

---

## Shell Scripts (Bash)

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

## JavaScript (Node.js Skills)

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

## Configuration Files (JSON)

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

**Related Documentation**:
- [Back to CLAUDE.md](../CLAUDE.md)
- [Testing Changes](./testing.md)
- [Git Workflow](./git-workflow.md)
