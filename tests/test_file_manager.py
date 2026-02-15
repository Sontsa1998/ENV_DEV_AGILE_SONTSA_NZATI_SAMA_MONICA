"""
Unit tests for file_manager module.
"""

import pytest
import pandas as pd
from io import StringIO
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from file_manager import (
    validate_csv_structure, parse_csv_file, get_file_info,
    validate_csv_not_empty, validate_file_size, normalize_column_names,
    validate_data_types, FileValidationError, FileEncodingError
)


class TestValidateCSVStructure:
    """Tests for validate_csv_structure function."""
    
    def test_valid_csv_with_required_columns(self):
        """Test validation passes for CSV with all required columns."""
        csv_content = "name,age,score\nJohn,25,85\nJane,30,90"
        is_valid, error_msg = validate_csv_structure(csv_content, ["name", "age", "score"])
        assert is_valid is True
        assert error_msg == ""
    
    def test_csv_missing_required_columns(self):
        """Test validation fails when required columns are missing."""
        csv_content = "name,age\nJohn,25\nJane,30"
        is_valid, error_msg = validate_csv_structure(csv_content, ["name", "age", "score"])
        assert is_valid is False
        assert "score" in error_msg.lower()
    
    def test_csv_case_insensitive_column_matching(self):
        """Test that column matching is case-insensitive."""
        csv_content = "Name,Age,Score\nJohn,25,85"
        is_valid, error_msg = validate_csv_structure(csv_content, ["name", "age", "score"])
        assert is_valid is True
    
    def test_invalid_csv_format(self):
        """Test validation fails for invalid CSV format."""
        csv_content = "not a valid csv format"
        is_valid, error_msg = validate_csv_structure(csv_content, ["name"])
        assert is_valid is False


