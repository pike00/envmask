# envmask

[![PyPI](https://img.shields.io/pypi/v/envmask.svg)](https://pypi.org/project/envmask/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Hide secrets from LLMs when reading `.env` files.**

Envguard is a security tool for Claude Code and other AI agents. It automatically masks credentials in `.env` files so they never appear in LLM conversations, preventing accidental exposure of secrets in transcripts, provider logs, or shared sessions.

## Problem

When an LLM reads a plaintext `.env` file, all secrets are visible in the conversation:

```
POSTGRES_PASSWORD=wFwrTU8GN6WWNHuhw0ncydnxiAzopS83
AWS_SECRET_ACCESS_KEY=BD5w5gQ2mLPvBfgWBVgfi+OD3vzi441//QlruXrMo8oZ
```

This is a security risk — credentials could be logged in conversation transcripts, cached by the LLM provider, or exposed if the session is compromised.

## Solution

envmask masks secrets by showing only the first 3 characters + ellipsis:

```
POSTGRES_PASSWORD=wFw...
AWS_SECRET_ACCESS_KEY=BD5...
```

This retains enough information to identify a credential (which service, which key) while hiding the actual secret.

## Installation

```bash
pip install envmask
```

Or install from source:

```bash
git clone https://github.com/pike00/envmask.git
cd envmask
pip install .
```

## Usage

### Command Line

```bash
envmask .env
envmask config/.env.production
```

### Claude Code Integration (Primary Use Case)

envmask is designed to protect secrets when using Claude Code. Install the hook once, then claude automatically masks `.env` reads:

**Installation:**
```bash
pip install envmask
bash scripts/install-claude-hook.sh --project-dir /path/to/project
```

The installation script updates `.claude/settings.json` automatically. After restart, Claude sees masked values instead of raw secrets:

```
Claude asks: What's in .env?
Claude sees: 
  POSTGRES_PASSWORD=wFw...
  API_KEY=AKI...
```

Full secrets remain in your `.env` file (unmodified). The masking happens in-process on your machine before Claude sees anything.

**For detailed setup instructions, see [docs/SETUP.md](docs/SETUP.md) | [Publishing guide](docs/PUBLISHING.md)**

### Python API

```python
from pathlib import Path
from envmask import parse_env_file

lines = parse_env_file(Path(".env"))
for line in lines:
    print(line)
```

## Security Threat Model

**What envmask protects against:**
- Secrets appearing in LLM conversation transcripts
- Provider logging/caching of full secrets
- Accidental copy-paste of credentials into chat
- Third-party access to session history

**What envmask does NOT protect against:**
- Compromised local machine (if your `.env` is readable, keyloggers/malware can steal it)
- Compromised LLM account (someone with access to your account can request unmasked files)
- File permissions (envmask respects existing `chmod` rules)
- Multiline secrets (only processes single-line KEY=VALUE format)

**Threat scenario prevented:**
- Attacker gains read-only access to Claude conversation transcripts
- Masked content shows: `AWS_KEY=AKI...`
- Attacker cannot brute-force the full key (10^18 possibilities for 3-char prefix)
- Even with the pattern knowledge, only 3 chars visible

See [docs/architecture.md](docs/architecture.md) for detailed threat model and design rationale.
See [docs/ROADMAP.md](docs/ROADMAP.md) for planned features and version milestones.

## Configuration

### Masking Pattern

Currently fixed at first 3 characters + ellipsis. To customize, edit `src/envmask/masker.py`:

```python
def mask_value(value: str) -> str:
    return value[:3] + "..."  # Modify here
```

### File Patterns

By default, envmask masks files matching:
- `.env`
- `*.env` (e.g., `production.env`, `app.env`)

Does NOT mask:
- `.env.example`
- `.env.sops`
- `.env.json` (use dedicated parsers)

## Limitations

- **Single-line values only** — Multiline JSON in `.env` values won't parse correctly
- **No quote handling** — Outputs values as-is; quotes included in mask
- **No format detection** — Works with KEY=VALUE format only (not YAML, JSON, etc.)

Future versions may support:
- `.env.local`, `.env.staging`, `.env.production` variants
- YAML and JSON configuration files
- On-demand unmasking with re-authentication

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE)

## Contact

For security issues, email will@khanpikehome.com instead of opening a public issue.

## Related Work

- [direnv](https://direnv.net/) — Load .env files in shell
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Load .env in Python apps
- [SOPS](https://github.com/mozilla/sops) — Encrypt .env files at rest
