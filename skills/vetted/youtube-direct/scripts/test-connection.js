#!/usr/bin/env node

/**
 * Test YouTube API Connection
 *
 * Verifies that authentication is working correctly
 */

const { YouTubeClient } = require('../lib/youtube-client');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('Testing YouTube Direct API connection...\n');

  const client = new YouTubeClient();
  const credPath = path.join(client.configDir, 'credentials', 'client_secret.json');
  const tokenPath = path.join(client.configDir, 'credentials', 'tokens.json');

  // Check if credentials exist
  if (!fs.existsSync(credPath)) {
    console.error('✗ OAuth credentials not found');
    console.error('  Expected: ' + credPath);
    console.error('\nRun setup first:');
    console.error('  node scripts/setup-auth.js --credentials /path/to/client_secret.json\n');
    process.exit(1);
  } else {
    console.log('✓ OAuth credentials found');
  }

  // Check if tokens exist
  if (!fs.existsSync(tokenPath)) {
    console.error('✗ OAuth tokens not found');
    console.error('  Expected: ' + tokenPath);
    console.error('\nRun setup first:');
    console.error('  node scripts/setup-auth.js --credentials /path/to/client_secret.json\n');
    process.exit(1);
  } else {
    console.log('✓ OAuth tokens found');
  }

  try {
    // Initialize client
    await client.initWithOAuth(credPath);
    console.log('✓ OAuth client initialized');

    // Test API call - get details of a well-known video
    console.log('\nTesting API access...');
    const testVideoId = 'dQw4w9WgXcQ'; // Rick Astley - Never Gonna Give You Up
    const details = await client.getVideoDetails(testVideoId);

    console.log('✓ API call successful');
    console.log('\nTest video details:');
    console.log(`  Title: ${details.title}`);
    console.log(`  Channel: ${details.channel.title}`);
    console.log(`  Views: ${details.viewCount.toLocaleString()}`);

    // Test caption access
    console.log('\nTesting caption access...');
    try {
      const captions = await client.getAvailableCaptions(testVideoId);
      console.log(`✓ Caption access working (${captions.length} caption tracks available)`);
    } catch (captionError) {
      if (captionError.message.includes('disabled')) {
        console.log('✓ Caption API accessible (test video has captions disabled)');
      } else {
        throw captionError;
      }
    }

    console.log('\n✓ All tests passed!');
    console.log('\nYou can now use:');
    console.log('  node scripts/search.js --query "your search"');
    console.log('  node scripts/get-transcript.js --video VIDEO_ID\n');

  } catch (error) {
    console.error(`\n✗ Test failed: ${error.message}`);

    if (error.message.includes('invalid_grant')) {
      console.error('\nYour OAuth tokens have expired or been revoked.');
      console.error('Re-run setup:');
      console.error('  node scripts/setup-auth.js --credentials ' + credPath);
    } else if (error.message.includes('quotaExceeded')) {
      console.error('\nYour YouTube API quota has been exceeded.');
      console.error('Quota resets at midnight Pacific Time.');
    }

    console.error('');
    process.exit(1);
  }
}

main();
