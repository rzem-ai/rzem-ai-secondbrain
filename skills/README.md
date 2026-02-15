# OpenClaw Skills Directory

This directory contains vetted OpenClaw skills and their security reviews.

## Structure

```
skills/
├── README.md                          (this file)
├── vetted/                           (approved skills)
│   ├── youtube-summarizer/
│   │   ├── review.md                 (security review)
│   │   ├── skill.js                  (skill code)
│   │   └── package.json
│   └── ...
├── pending-review/                   (skills awaiting review)
│   └── ...
└── rejected/                         (rejected skills - for reference)
    └── ...
```

## Workflow

1. **Download skill** → Place in `pending-review/`
2. **Security review** → Follow [../SKILL_VETTING_GUIDE.md](../SKILL_VETTING_GUIDE.md)
3. **Approve/Reject** → Move to `vetted/` or `rejected/`
4. **Install** → Use the vetted version

## Currently Vetted Skills

None yet. Start by reviewing `youtube-summarizer`.

## Usage

### To add a skill for review:

```bash
cd /Users/alex/Dev/Work/ai/rzem-ai-secondbrain/skills/pending-review
mkdir youtube-summarizer
cd youtube-summarizer

# Download the skill (method depends on source)
# Option 1: From npm
npm pack youtube-summarizer
tar -xzf youtube-summarizer-*.tgz
mv package/* .
rmdir package

# Option 2: From GitHub
git clone https://github.com/[author]/youtube-summarizer.git .
```

### To review:

```bash
# Read the code
cat skill.js
cat package.json

# Check dependencies
npm install  # in a sandboxed environment
npm audit

# Run static analysis
npm run lint  # if available

# Complete security review using SKILL_VETTING_GUIDE.md
```

### To approve:

```bash
# Move to vetted
mv pending-review/youtube-summarizer vetted/

# Add review document
cd vetted/youtube-summarizer
# Create review.md with findings
```

### To install from vetted:

```bash
# Install from local vetted copy
cd vetted/youtube-summarizer
npm link

# Or install to OpenClaw directory
cp -r vetted/youtube-summarizer ~/.openclaw/skills/
```
