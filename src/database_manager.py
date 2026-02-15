"""
Database Manager module for DuckDB integration.

This module provides functions to manage DuckDB connections, create tables,
import data, and execute queries.
"""

from typing import List, Optional
import pandas as pd
import duckdb
from pathlib import Path