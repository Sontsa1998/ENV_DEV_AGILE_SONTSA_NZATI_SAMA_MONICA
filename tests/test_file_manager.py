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


