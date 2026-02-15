# OpenClaw-Specific Context

> Part of the [OpenClaw Second Brain CLAUDE.md](../CLAUDE.md) documentation

Understanding OpenClaw's skill format, gateway configuration, and security model.

---

## Skill Format

OpenClaw skills use the Agent Skills format:

- **SKILL.md**: Main skill documentation with frontmatter
- **scripts/**: Executable scripts called by the agent
- **user-invocable: true**: Skill can be triggered directly by users

## Gateway Configuration

- Always bind to `127.0.0.1` (localhost only)
- Never expose to public internet without explicit user choice
- Remote access via Tailscale or SSH tunnel only

## Security Model

Defense in depth:

1. Network isolation (localhost binding)
2. Container isolation (read-only filesystems)
3. Skill vetting (source code review)
4. Secret management (keychain/pass)
5. Content sandboxing (untrusted external content)

---

**Related Documentation**:
- [Back to CLAUDE.md](../CLAUDE.md)
- [Working with This Project](./working-with-project.md)
- [External References](./external-references.md)
