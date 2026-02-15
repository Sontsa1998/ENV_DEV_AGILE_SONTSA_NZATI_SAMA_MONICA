"""
Database Manager module for DuckDB integration.

This module provides functions to manage DuckDB connections, create tables,
import data, and execute queries.
"""

from typing import List, Optional
import pandas as pd
import duckdb
from pathlib import Path

class DatabaseManager:
    """Manages DuckDB database connections and operations."""
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize DuckDB connection.
        
        Args:
            db_path: Path to DuckDB database file. Use ":memory:" for in-memory database.
        """
        self.db_path = db_path
        self.connection = None
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Initialize or reconnect to DuckDB database."""
        try:
            self.connection = duckdb.connect(self.db_path)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DuckDB connection: {str(e)}")
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def import_data(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> None:
        """
        Import a pandas DataFrame into a DuckDB table.
        
        Args:
            df: pandas DataFrame to import
            table_name: Name of the table to create/update
            if_exists: How to behave if table exists ('replace', 'append', 'fail')
        
        Raises:
            ValueError: If DataFrame is empty or table_name is invalid
            RuntimeError: If import operation fails
        """
        if df.empty:
            raise ValueError("Cannot import empty DataFrame")
        
        if not table_name or not table_name.replace("_", "").isalnum():
            raise ValueError(f"Invalid table name: {table_name}")
        
        try:
            if if_exists == "replace":
                self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            self.connection.register(table_name, df)
            self.connection.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}")
            self.connection.unregister(table_name)
        except Exception as e:
            raise RuntimeError(f"Failed to import data into table '{table_name}': {str(e)}")
     