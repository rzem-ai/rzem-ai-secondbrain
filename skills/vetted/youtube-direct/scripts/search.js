#!/usr/bin/env node

/**
 * Search YouTube Videos and Channels
 *
 * Usage:
 *   node search.js --query "search terms" [--type video|channel] [--limit N]
 */

const { YouTubeClient } = require('../lib/youtube-client');

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

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const query = args.query || args.q;
  const type = args.type || 'video';
  const limit = parseInt(args.limit || args.maxResults || '10');

  if (!query) {
    console.error('Error: --query parameter is required');
    console.error('\nUsage:');
    console.error('  node search.js --query "search terms" [--type video|channel] [--limit N]');
    console.error('\nExamples:');
    console.error('  node search.js --query "machine learning tutorial" --type video --limit 10');
    console.error('  node search.js --query "MIT OpenCourseWare" --type channel --limit 5');
    process.exit(1);
  }

  try {
    // Initialize client (can use API key for search)
    const client = new YouTubeClient();

    // Try OAuth first, fallback to API key
    const fs = require('fs');
    const path = require('path');
    const credPath = path.join(client.configDir, 'credentials', 'client_secret.json');

    if (fs.existsSync(credPath)) {
      await client.initWithOAuth(credPath);
    } else if (process.env.YOUTUBE_API_KEY) {
      client.initWithApiKey();
    } else {
      console.error('Error: No authentication configured.');
      console.error('\nOption 1 (OAuth): Run setup-auth.js');
      console.error('Option 2 (API Key): Set YOUTUBE_API_KEY environment variable');
      process.exit(1);
    }

    // Perform search
    console.error(`Searching for: ${query} (type: ${type}, limit: ${limit})`);
    const results = await client.search(query, { type, maxResults: limit });

    // Output results
    console.log(JSON.stringify(results, null, 2));

    // Summary
    console.error(`\nFound ${results.length} results`);

  } catch (error) {
    console.error(`Error: ${error.message}`);

    if (error.message.includes('quotaExceeded')) {
      console.error('\nYour YouTube API quota has been exceeded.');
      console.error('Quota resets at midnight Pacific Time.');
    }

    process.exit(1);
  }
}

main();
