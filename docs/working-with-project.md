# Working with This Project

> Part of the [OpenClaw Second Brain CLAUDE.md](../CLAUDE.md) documentation

This guide covers workflows for updating documentation, adding skills, and conducting security reviews.

---

## When Updating Deployment Plans

1. **Update ALL affected files**: If a change applies to both platforms, update both PLAN_MACOS.md and PLAN_UBUNTU.md
2. **Keep PLAN.md in sync**: Update the overview if adding major features
3. **Check cross-references**: Ensure all links between documents remain valid
4. **Update PROJECT_STATUS.md**: Reflect current state and decisions

## When Adding New Skills

1. **Place in pending-review/** initially
2. **Create security review document**: See `skills/pending-review/YOUTUBE_SKILLS_SECURITY_REVIEW.md` as template
3. **Document in SKILL_COMPARISON.md**: Add comparison with alternatives
4. **After vetting, move to vetted/**: Update references in deployment plans

## When Reviewing Third-Party Skills

Follow this process:

1. Clone skill repository to `skills/pending-review/[skill-name]/`
2. Create security review document
3. Check for:
   - Dangerous code patterns (dynamic code execution, shell injection)
   - Hardcoded secrets
   - Unexpected network calls
   - Supply chain risks (npm audit)
4. Document findings and recommendation
5. If approved, update deployment plans with installation instructions

## Security Review Requirements

**Critical checks**:

- [ ] No dynamic code execution with external data
- [ ] No hardcoded API keys or secrets
- [ ] Network calls only to documented endpoints
- [ ] Input validation present
- [ ] Dependencies scanned (npm audit)
- [ ] VirusTotal scan if binary/compiled code

**Red flags**:

- Obfuscated code
- Cryptocurrency mining
- Undocumented network requests
- Excessive permissions
- Supply chain concerns

---

**Related Documentation**:

- [Back to CLAUDE.md](../CLAUDE.md)
- [Common Tasks](./common-tasks.md)
- [OpenClaw-Specific Context](./openclaw-context.md)
