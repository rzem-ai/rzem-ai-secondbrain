#!/usr/bin/env node

/**
 * Get YouTube Video Transcript
 *
 * Usage:
 *   node get-transcript.js --video VIDEO_ID [--format json|text] [--lang LANG_CODE]
 */

const { YouTubeClient } = require('../lib/youtube-client');
const fs = require('fs');
const path = require('path');

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      result[key] = value;
      i++;
    }
  }
  return result;
}

function extractVideoId(input) {
  // Handle various YouTube URL formats
  if (!input) return null;

  // Already a video ID (11 characters)
  if (/^[a-zA-Z0-9_-]{11}$/.test(input)) {
    return input;
  }

  // youtube.com/watch?v=VIDEO_ID
  const watchMatch = input.match(/[?&]v=([a-zA-Z0-9_-]{11})/);
  if (watchMatch) return watchMatch[1];

  // youtu.be/VIDEO_ID
  const shortMatch = input.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
  if (shortMatch) return shortMatch[1];

  // youtube.com/embed/VIDEO_ID
  const embedMatch = input.match(/\/embed\/([a-zA-Z0-9_-]{11})/);
  if (embedMatch) return embedMatch[1];

  return null;
}

function formatAsText(transcript) {
  let text = '';

  text += `Title: ${transcript.title}\n`;
  text += `Channel: ${transcript.channel}\n`;
  text += `Language: ${transcript.language}\n`;
  text += `Auto-generated: ${transcript.is_auto_generated ? 'Yes' : 'No'}\n`;
  text += '\n--- Transcript ---\n\n';

  for (const entry of transcript.transcript) {
    const timestamp = formatTimestamp(entry.start);
    text += `[${timestamp}] ${entry.text}\n`;
  }

  return text;
}

function formatTimestamp(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const videoInput = args.video || args.v;
  const format = args.format || 'json';
  const language = args.lang || args.language || null;

  if (!videoInput) {
    console.error('Error: --video parameter is required');
    console.error('\nUsage:');
    console.error('  node get-transcript.js --video VIDEO_ID_OR_URL [--format json|text] [--lang LANG_CODE]');
    console.error('\nExamples:');
    console.error('  node get-transcript.js --video dQw4w9WgXcQ --format json');
    console.error('  node get-transcript.js --video https://youtube.com/watch?v=dQw4w9WgXcQ --format text');
    console.error('  node get-transcript.js --video dQw4w9WgXcQ --lang es');
    process.exit(1);
  }

  const videoId = extractVideoId(videoInput);
  if (!videoId) {
    console.error(`Error: Invalid video ID or URL: ${videoInput}`);
    process.exit(1);
  }

  try {
    // Initialize client with OAuth
    const client = new YouTubeClient();
    const credPath = path.join(client.configDir, 'credentials', 'client_secret.json');

    if (!fs.existsSync(credPath)) {
      console.error('Error: OAuth credentials not configured.');
      console.error('Run: node scripts/setup-auth.js --credentials /path/to/client_secret.json');
      process.exit(1);
    }

    await client.initWithOAuth(credPath);

    // Get transcript
    console.error('Fetching transcript...');
    const transcript = await client.getTranscript(videoId, { language });

    // Output in requested format
    if (format === 'text') {
      console.log(formatAsText(transcript));
    } else {
      console.log(JSON.stringify(transcript, null, 2));
    }

  } catch (error) {
    console.error(`Error: ${error.message}`);

    if (error.message.includes('OAuth2')) {
      console.error('\nHint: Captions require OAuth2 authentication.');
      console.error('Run: node scripts/setup-auth.js --credentials /path/to/client_secret.json');
    } else if (error.message.includes('quotaExceeded')) {
      console.error('\nYour YouTube API quota has been exceeded.');
      console.error('Quota resets at midnight Pacific Time.');
    } else if (error.message.includes('No captions available')) {
      console.error('\nThis video does not have captions/subtitles available.');
    }

    process.exit(1);
  }
}

main();
