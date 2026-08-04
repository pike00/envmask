# drape

<!-- BEGIN PROJECT-KIT — generated, do not edit by hand -->
## Project-kit recipes

This repo is managed by project-kit (skill version: 0.2.0, last refreshed: 2026-08-04).
Project-kit-managed operations go through `just`.

### Execution context

Run `just context` before every host-dependent action.
Managed recipes enforce their checks automatically. Host roles are descriptive
rather than exclusive; the actual hostname and configured target determine where
an action runs.

### Quick reference

| Task | Command |
|---|---|
| Show execution context | `just context [target]` |
| Cut a release | `just release patch` |
| Update CHANGELOG | `just changelog` |
| Health check | `uv run .project-kit/scripts/doctor.py` |

### Subsystem status

- release: enabled

### Where things live

- Managed recipe imports: 2 (`_lib.just` plus 1 managed subsystem)
- `.project-kit/scripts/` — uv-scripts for non-trivial recipes
- `.project-kit/cliff.toml` — git-cliff config (centralized; passed via `--config`, no root copy)
- `justfile` (root) — imports 2 managed recipe files plus repo-specific recipes

### How to refresh

Re-run the project-kit wizard in chat: ask Claude to "refresh project-kit"
or "audit project-kit in this repo".
<!-- END PROJECT-KIT -->
