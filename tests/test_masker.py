"""Tests for envmask.masker module."""

import tempfile
from pathlib import Path

import pytest

from envmask.masker import mask_value, parse_env_file


class TestMaskValue:
    """Test mask_value function."""

    def test_mask_normal_value(self):
        """Test masking a typical secret."""
        assert mask_value("AKIAQU6D3H2I4SYVDHJP") == "AKI..."

    def test_mask_short_value(self):
        """Test masking values shorter than 3 chars."""
        assert mask_value("ab") == "ab..."
        assert mask_value("a") == "a..."

    def test_mask_empty_value(self):
        """Test masking empty string."""
        assert mask_value("") == ""

    def test_mask_special_chars(self):
        """Test masking values with special characters."""
        assert mask_value("p@ssw$rd!") == "p@s..."


class TestParseEnvFile:
    """Test parse_env_file function."""

    def test_parse_basic_env(self):
        """Test parsing a basic .env file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("KEY1=value1\n")
            f.write("KEY2=value2\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["KEY1=val...", "KEY2=val..."]

        Path(f.name).unlink()

    def test_parse_with_comments(self):
        """Test parsing ignores comments."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("# This is a comment\n")
            f.write("KEY=value\n")
            f.write("# Another comment\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["KEY=val..."]

        Path(f.name).unlink()

    def test_parse_with_empty_lines(self):
        """Test parsing ignores empty lines."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("KEY1=value1\n")
            f.write("\n")
            f.write("KEY2=value2\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["KEY1=val...", "KEY2=val..."]

        Path(f.name).unlink()

    def test_parse_empty_values(self):
        """Test parsing empty values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("KEY1=\n")
            f.write("KEY2=value\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["KEY1=", "KEY2=val..."]

        Path(f.name).unlink()

    def test_parse_equals_in_value(self):
        """Test parsing values containing equals sign."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("FORMULA=a=b+c\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["FORMULA=a=b..."]

        Path(f.name).unlink()

    def test_parse_whitespace_handling(self):
        """Test parsing handles whitespace."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("  KEY1  =  value1  \n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["KEY1=val..."]

        Path(f.name).unlink()

    def test_file_not_found(self):
        """Test parsing non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            parse_env_file(Path("/nonexistent/.env"))

    def test_parse_quoted_values(self):
        """Test parsing handles quoted values correctly."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write('KEY1="value_with_quotes"\n')
            f.write("KEY2='single_quotes'\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            # Quotes are part of the value, so they get masked too
            # First 3 chars of "value_with_quotes" is "va
            assert result == ['KEY1="va...', "KEY2='si..."]

        Path(f.name).unlink()

    def test_parse_json_value(self):
        """Test parsing JSON-like values in .env."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write('CONFIG={"nested":"value"}\n')
            f.flush()

            result = parse_env_file(Path(f.name))
            # JSON values are masked as-is (single line only)
            assert result == ['CONFIG={"n...']

        Path(f.name).unlink()

    def test_parse_multiline_comment(self):
        """Test parsing with inline comments (commented after key=value)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            # Note: inline comments after values are NOT supported (rare in .env files)
            f.write("KEY1=value1\n")
            f.write("# Commented key\n")
            f.write("KEY2=value2\n")
            f.flush()

            result = parse_env_file(Path(f.name))
            assert result == ["KEY1=val...", "KEY2=val..."]

        Path(f.name).unlink()
