# Changelog

All notable changes to envmask will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-09

### Added

- Initial release of envmask
- Core masking utility: first 3 characters + ellipsis pattern
- Python CLI: `envmask` command-line tool
- Python API: `parse_env_file()` and `mask_value()` functions
- Claude Code integration: PreToolUse hook for automatic masking on `Read` calls
- Comprehensive test suite with 11+ tests
- Security threat model documentation
- Support for `.env` and `*.env` file patterns

### Features

- Parse `.env` files in KEY=VALUE format
- Mask secrets to 3 chars + "..." for safe LLM inspection
- Ignore comments and empty lines
- Handle whitespace gracefully
- Support values containing equals signs
- Package installable via pip

### Known Limitations

- Single-line values only (multiline JSON in values won't parse)
- No quote handling (outputs raw)
- KEY=VALUE format only (no YAML/JSON)
- Fixed masking pattern (not customizable yet)

## Future Releases

### [0.2.0] - Planned

- [ ] Support for `.env.local`, `.env.production`, etc. variants
- [ ] Custom masking patterns via configuration
- [ ] YAML and JSON format support
- [ ] Better error messages and logging
- [ ] On-demand unmasking with re-authentication

### [1.0.0] - Planned

- [ ] Stable API and CLI
- [ ] Full plugin support for Claude Code
- [ ] Integration with secret managers (1Password, Vault)
- [ ] Audit logging
