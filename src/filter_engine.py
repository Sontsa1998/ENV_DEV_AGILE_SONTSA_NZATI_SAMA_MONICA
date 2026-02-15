"""
Filter Engine module for dynamic data filtering.

This module provides functions to build and apply dynamic filters to SQL queries
and retrieve available filter options.
"""

from typing import Dict, List, Any, Optional, Tuple
from database_manager import DatabaseManager


class FilterEngine:
    """Manages dynamic filtering of data."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize Filter Engine with database manager.
        
        Args:
            db_manager: DatabaseManager instance for executing queries
        """
        self.db_manager = db_manager
    
    def build_filter_query(self, filters: Dict[str, Any]) -> str:
        """
        Build a WHERE clause from filter specifications.
        
        Args:
            filters: Dictionary of filter specifications
                    Example: {
                        "gender": ["Male", "Female"],
                        "age_range": (18, 25),
                        "attendance_range": (80.0, 100.0)
                    }
        
        Returns:
            WHERE clause string (without "WHERE" keyword)
        """
        if not filters:
            return ""
        
        conditions = []
        
        for key, value in filters.items():
            if value is None:
                continue
            
            if isinstance(value, list) and len(value) > 0:
                # Handle list of values (IN clause)
                values_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in value])
                conditions.append(f"{key} IN ({values_str})")
            
            elif isinstance(value, tuple) and len(value) == 2:
                # Handle range (BETWEEN clause)
                conditions.append(f"{key} BETWEEN {value[0]} AND {value[1]}")
            
            elif isinstance(value, str):
                # Handle single string value
                conditions.append(f"{key} = '{value}'")
            
            elif isinstance(value, (int, float)):
                # Handle single numeric value
                conditions.append(f"{key} = {value}")
            
            elif isinstance(value, bool):
                # Handle boolean value
                conditions.append(f"{key} = {value}")
        
        return " AND ".join(conditions) if conditions else ""
    