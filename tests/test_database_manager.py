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