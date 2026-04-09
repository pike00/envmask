"""Core masking logic for .env files."""

import sys
from pathlib import Path

from loguru import logger


def mask_value(value: str) -> str:
    """Mask a secret value to first 3 chars + ellipsis.

    Args:
        value: The secret value to mask

    Returns:
        Masked string (first 3 chars + "...") or empty string

    Examples:
        >>> mask_value("AKIAQU6D3H2I4SYVDHJP")
        'AKI...'
        >>> mask_value("")
        ''
    """
    if not value:
        return ""
    return value[:3] + "..."


def parse_env_file(filepath: Path) -> list[str]:
    """Parse .env file and return masked KEY=VALUE lines.

    Args:
        filepath: Path to .env file

    Returns:
        List of masked KEY=VALUE lines

    Raises:
        FileNotFoundError: If file does not exist

    Behavior:
        - Skips empty lines and comments (lines starting with #)
        - Splits on first = only (allows = in values)
        - Strips whitespace from keys and values
        - Masks all non-empty values to first 3 chars + "..."
    """
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")

    logger.debug(f"Parsing .env file: {filepath}")
    lines = []
    skipped_count = 0
    try:
        with open(filepath) as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip("\n")
                # Skip empty lines and comments
                if not line or line.lstrip().startswith("#"):
                    skipped_count += 1
                    continue

                # Split on first = only
                if "=" not in line:
                    skipped_count += 1
                    continue

                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()

                # Mask the value
                masked = mask_value(value) if value else ""
                lines.append(f"{key}={masked}")

        logger.debug(
            f"Successfully parsed {len(lines)} masked entries "
            f"(skipped {skipped_count} lines) from {filepath}"
        )
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
        raise

    return lines
