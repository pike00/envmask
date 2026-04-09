"""Command-line interface for envguard."""

import argparse
import sys
from pathlib import Path

from loguru import logger

from . import __version__
from .masker import parse_env_file

# Remove default handler and add stderr with INFO level
logger.remove()
logger.add(sys.stderr, level="INFO", format="<level>{message}</level>")


def main():
    """Parse command-line arguments and mask .env file."""
    parser = argparse.ArgumentParser(
        prog="envguard",
        description="Mask secrets in .env files for safe LLM inspection",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=".env",
        help="Path to .env file (default: .env)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()
    filepath = Path(args.file)

    try:
        lines = parse_env_file(filepath)
        for line in lines:
            print(line)
    except FileNotFoundError as e:
        logger.error(f"{e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
