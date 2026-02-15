#!/usr/bin/env node

/**
 * OAuth 2.0 Setup for YouTube Direct API
 *
 * This script helps you authenticate with YouTube Data API v3 using OAuth 2.0
 *
 * Prerequisites:
 *   1. Create a Google Cloud Project
 *   2. Enable YouTube Data API v3
 *   3. Create OAuth 2.0 credentials (Desktop app)
 *   4. Download the client_secret.json file
 *
 * Usage:
 *   node setup-auth.js --credentials /path/to/client_secret.json
 */

const { google } = require('googleapis');
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');
const os = require('os');

const SCOPES = [
  'https://www.googleapis.com/auth/youtube.readonly',
  'https://www.googleapis.com/auth/youtube.force-ssl'
];

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

function getConfigDir() {
  const home = os.homedir();
  const openclawDir = path.join(home, '.openclaw', 'skills', 'youtube-direct');
  const skillDir = path.join(__dirname, '..', 'credentials');

  return fs.existsSync(path.join(home, '.openclaw')) ? openclawDir : skillDir;
}

function ensureConfigDir(configDir) {
  const credDir = path.join(configDir, 'credentials');
  if (!fs.existsSync(credDir)) {
    fs.mkdirSync(credDir, { recursive: true, mode: 0o700 });
  }
  try {
    fs.chmodSync(credDir, 0o700);
  } catch (e) {
    console.warn(`Warning: Could not set permissions on ${credDir}`);
  }
}

async function authenticate(clientSecretPath, configDir) {
  // Read client secrets
  const credentials = JSON.parse(fs.readFileSync(clientSecretPath, 'utf8'));
  const { client_secret, client_id, redirect_uris } =
    credentials.installed || credentials.web;

  // Create OAuth2 client
  const oAuth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    redirect_uris[0] || 'http://localhost:3000/oauth2callback'
  );

  // Generate auth URL
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent' // Force consent screen to get refresh token
  });

  console.log('\n=== YouTube Direct API - OAuth Setup ===\n');
  console.log('Opening browser for Google sign-in...\n');
  console.log('If browser does not open automatically, visit this URL:');
  console.log(authUrl);
  console.log('\nWaiting for authentication...\n');

  // Open browser
  const opener = process.platform === 'darwin' ? 'open' :
                 process.platform === 'win32' ? 'start' : 'xdg-open';
  require('child_process').spawn(opener, [authUrl], { detached: true, stdio: 'ignore' });

  // Start local server to receive callback
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      try {
        if (req.url.indexOf('/oauth2callback') > -1) {
          const qs = new url.URL(req.url, 'http://localhost:3000').searchParams;
          const code = qs.get('code');

          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(`
            <html>
              <body style="font-family: sans-serif; padding: 40px; text-align: center;">
                <h1 style="color: #1a73e8;">✓ Authentication Successful</h1>
                <p>You can close this window and return to the terminal.</p>
              </body>
            </html>
          `);

          server.close();

          // Exchange code for tokens
          const { tokens } = await oAuth2Client.getToken(code);
          oAuth2Client.setCredentials(tokens);

          // Save tokens
          const tokenPath = path.join(configDir, 'credentials', 'tokens.json');
          fs.writeFileSync(tokenPath, JSON.stringify(tokens, null, 2), { mode: 0o600 });

          // Copy client_secret to config dir
          const destPath = path.join(configDir, 'credentials', 'client_secret.json');
          if (path.resolve(clientSecretPath) !== path.resolve(destPath)) {
            fs.copyFileSync(clientSecretPath, destPath);
            fs.chmodSync(destPath, 0o600);
          }

          resolve(tokens);
        }
      } catch (e) {
        reject(e);
      }
    }).listen(3000, () => {
      console.log('Listening on http://localhost:3000');
    });

    // Timeout after 5 minutes
    setTimeout(() => {
      server.close();
      reject(new Error('Authentication timeout - no response after 5 minutes'));
    }, 5 * 60 * 1000);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const credentialsPath = args.credentials || args.creds;

  if (!credentialsPath) {
    console.error('Error: --credentials parameter is required\n');
    console.error('Usage:');
    console.error('  node setup-auth.js --credentials /path/to/client_secret.json\n');
    console.error('Steps to get credentials:');
    console.error('  1. Go to https://console.cloud.google.com/');
    console.error('  2. Create a project (or select existing)');
    console.error('  3. Enable "YouTube Data API v3"');
    console.error('  4. Go to "APIs & Services" → "Credentials"');
    console.error('  5. Create "OAuth client ID" → Application type: "Desktop app"');
    console.error('  6. Download the JSON file\n');
    process.exit(1);
  }

  if (!fs.existsSync(credentialsPath)) {
    console.error(`Error: Credentials file not found: ${credentialsPath}`);
    process.exit(1);
  }

  try {
    const configDir = getConfigDir();
    ensureConfigDir(configDir);

    const tokens = await authenticate(credentialsPath, configDir);

    console.log('\n✓ Authentication successful!\n');
    console.log('Credentials saved to:');
    console.log(`  ${path.join(configDir, 'credentials', 'tokens.json')}\n`);
    console.log('You can now use the YouTube Direct skill.\n');
    console.log('Test with:');
    console.log('  node scripts/search.js --query "test" --limit 1');
    console.log('  node scripts/get-transcript.js --video dQw4w9WgXcQ --format text\n');

  } catch (error) {
    console.error(`\nError: ${error.message}`);

    if (error.message.includes('redirect_uri_mismatch')) {
      console.error('\nThe redirect URI in your OAuth credentials does not match.');
      console.error('Make sure your OAuth client is configured with redirect URI: http://localhost:3000/oauth2callback');
    }

    process.exit(1);
  }
}

main();
