#!/usr/bin/env python3
"""Example: Using envguard as a library.

This example shows how to use envguard.masker in your own code.
"""

from pathlib import Path

from envguard import parse_env_file

# Parse and print masked env vars
env_file = Path(".env")
if env_file.exists():
    lines = parse_env_file(env_file)
    for line in lines:
        print(line)
else:
    print("No .env file found")
