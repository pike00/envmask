"""envguard: Mask secrets in .env files for safe LLM inspection."""

__version__ = "0.1.0"
__author__ = "Will Pike"
__license__ = "MIT"

from .masker import mask_value, parse_env_file

__all__ = ["mask_value", "parse_env_file"]
