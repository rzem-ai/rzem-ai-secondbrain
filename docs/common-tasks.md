# Common Tasks

> Part of the [OpenClaw Second Brain CLAUDE.md](../CLAUDE.md) documentation

Step-by-step instructions for frequent operations when maintaining this project.

---

## Add a New Platform-Specific Tip

1. Identify which guide(s) need the tip
2. Find appropriate section (usually troubleshooting or platform-specific tips)
3. Add with clear heading and example
4. Update table of contents if section is new

## Update Container Runtime Recommendations

1. Edit PLAN_MACOS.md section 4.4 (container runtime options)
2. Update pros/cons in the comparison table
3. Verify recommendation still matches in PLAN.md overview
4. Update PROJECT_STATUS.md decision matrix

## Add New Skill Vetting Process Step

1. Update SKILL_VETTING_GUIDE.md with new step
2. Apply to existing reviews in skills/pending-review/
3. Document rationale in PROJECT_STATUS.md

## Fix Broken Links

1. Search for the old link pattern: `grep -r "old-link" *.md`
2. Update in all locations
3. Test with markdown preview or link checker
4. Commit with clear message about link update

---

**Related Documentation**:
- [Back to CLAUDE.md](../CLAUDE.md)
- [Working with This Project](./working-with-project.md)
- [Testing Changes](./testing.md)
