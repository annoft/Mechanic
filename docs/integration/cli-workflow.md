# CLI Workflow

Daily development commands and patterns for working with Mechanic.

---

## Daily Development

```bash
# Start your session
mech                          # Launch dashboard

# After making changes, reload in-game
# /reload

# Check for errors
mech addon.output             # Full snapshot (errors, tests, console)
mech addon.output --agent     # Compressed for AI assistants
```

---

## Code Quality

```bash
# Validate TOC
mech call addon.validate '{"addon": "MyAddon"}'

# Lint with Luacheck
mech call addon.lint '{"addon": "MyAddon"}'

# Format with StyLua
mech call addon.format '{"addon": "MyAddon"}'

# Run tests
mech call addon.test '{"addon": "MyAddon"}'

# Scan for deprecated APIs (Midnight prep)
mech call addon.deprecations '{"addon": "MyAddon"}'
```

---

## All-in-One Validation

```bash
# Run full quality suite before committing
mech call addon.lint '{"addon": "MyAddon"}' && \
mech call addon.test '{"addon": "MyAddon"}' && \
mech call addon.validate '{"addon": "MyAddon"}'
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start dashboard | `mech` |
| Reload WoW UI | Use `/reload` in-game |
| Get addon output | `mech addon.output` |
| Validate TOC | `mech call addon.validate '{"addon": "NAME"}'` |
| Lint code | `mech call addon.lint '{"addon": "NAME"}'` |
| Format code | `mech call addon.format '{"addon": "NAME"}'` |
| Run tests | `mech call addon.test '{"addon": "NAME"}'` |
| Check deprecations | `mech call addon.deprecations '{"addon": "NAME"}'` |
| Sync to clients | `mech call addon.sync '{"addon": "NAME"}'` |

---

## Environment Check

```bash
# Verify your setup
mech call env.status
```

This shows:
- WoW installation paths
- Active clients (_retail_, _beta_, _ptr_)
- Mechanic runtime installation status for `!Mechanic` and `Mechanic`

For downloaded/generated tool status, run:

```bash
mech call tools.status
mech call sandbox.status
```

---

## Related Guides

- [Release Automation](./release.md)
- [Troubleshooting](./troubleshooting.md)
- [CLI Reference](../cli-reference.md)
