"""Claude Code PreToolUse hook for masking .env file reads.

Usage:
    python3 -m envguard.hook
    (reads tool input from stdin, outputs hook response to stdout)
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

from loguru import logger

from ..masker import parse_env_file


def _should_mask(filepath: str) -> bool:
    """Check if file should be masked based on naming pattern.

    Args:
        filepath: Full file path

    Returns:
        True if file matches .env patterns, False otherwise
    """
    basename = os.path.basename(filepath).lower()

    # Match: .env or *.env
    # Exclude: .env.sops, .env.example, .env.json, .env.yaml, .env.yml
    if basename == ".env":
        return True
    if basename.endswith(".env"):
        # Check for known non-.env extensions
        excluded_suffixes = (".sops", ".example", ".json", ".yaml", ".yml")
        return not any(basename.endswith(f".env{suffix}") for suffix in excluded_suffixes)
    return False


def main() -> None:
    """PreToolUse hook handler for Claude Code.

    Intercepts Read calls on .env files and returns masked content instead of
    exposing raw secrets in the LLM conversation.
    """
    # Suppress debug logs in hook context
    logger.remove()

    try:
        tool_input: dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError:
        logger.debug("Invalid JSON input, deferring to Claude")
        sys.exit(0)

    filepath: str = tool_input.get("tool_input", {}).get("file_path", "")
    if not filepath:
        logger.debug("No file_path in tool input")
        sys.exit(0)

    # Check if file should be masked
    if not _should_mask(filepath):
        logger.debug(f"File does not match .env pattern: {filepath}")
        sys.exit(0)

    if not os.path.isfile(filepath):
        logger.debug(f"File does not exist: {filepath}")
        sys.exit(0)  # let Read handle file-not-found

    try:
        masked_lines = parse_env_file(Path(filepath))
        masked_content = "\n".join(masked_lines)
        logger.debug(f"Successfully masked {len(masked_lines)} entries from {filepath}")
    except Exception as e:
        logger.debug(f"Error masking {filepath}: {e}, deferring to Claude")
        sys.exit(0)  # On error, let Claude try normally

    response: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"envguard: secrets masked for LLM safety.\n\n"
                f"# {filepath} (masked by envguard)\n{masked_content}"
            ),
        }
    }

    json.dump(response, sys.stdout)


if __name__ == "__main__":
    main()
