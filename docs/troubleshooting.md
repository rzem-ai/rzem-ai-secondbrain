# Troubleshooting Common Issues

> Part of the [OpenClaw Second Brain CLAUDE.md](../CLAUDE.md) documentation

Solutions for common problems encountered when working with this project.

---

## "Skills section not updating"

- Check if both PLAN_MACOS.md and PLAN_UBUNTU.md were updated
- Verify section numbers match across files
- Search for skill name across all files to catch references

## "Link not working"

- Use relative links: `./PLAN_MACOS.md` not `/PLAN_MACOS.md`
- GitHub flavored markdown: `[Link Text](./file.md)` not `[Link Text](file.md)`
- Test links in GitHub preview

## "Code example fails"

- Test in relevant platform (macOS vs Ubuntu)
- Check environment variables are documented
- Verify paths are correct for platform
- Escape special characters properly

---

**Related Documentation**:
- [Back to CLAUDE.md](../CLAUDE.md)
- [Common Tasks](./common-tasks.md)
- [Testing Changes](./testing.md)
