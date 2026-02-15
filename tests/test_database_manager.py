"""
Unit tests for database_manager module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_manager import DatabaseManager, handle_duplicates, remove_all_duplicates


class TestDatabaseManager:
    """Tests for DatabaseManager class."""
    
    @pytest.fixture
    def db_manager(self):
        """Create an in-memory database manager for testing."""
        return DatabaseManager(":memory:")

    @pytest.fixture
    def sample_df(self):
        """Create a sample DataFrame for testing."""
        return pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 28, 32],
            "score": [85, 90, 78, 92, 88]
        })
    
    def test_initialize_connection(self, db_manager):
        """Test that database connection is initialized."""
        assert db_manager.connection is not None
    
    def test_import_data_creates_table(self, db_manager, sample_df):
        """Test that importing data creates a table."""
        db_manager.import_data(sample_df, "test_table")
        tables = db_manager.get_available_tables()
        assert "test_table" in tables
    
    def test_import_empty_dataframe_raises_error(self, db_manager):
        """Test that importing empty DataFrame raises ValueError."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError):
            db_manager.import_data(empty_df, "test_table")
    
    def test_import_invalid_table_name_raises_error(self, db_manager, sample_df):
        """Test that invalid table name raises ValueError."""
        with pytest.raises(ValueError):
            db_manager.import_data(sample_df, "invalid-table-name!")
    