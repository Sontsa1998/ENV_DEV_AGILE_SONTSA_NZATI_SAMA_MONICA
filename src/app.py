"""
Main Streamlit application for Student Performance Analyzer.

This module orchestrates the UI components and coordinates between modules
to provide an interactive interface for analyzing student performance data.
"""

import streamlit as st
import pandas as pd
from io import StringIO
from pathlib import Path

from file_manager import (
    validate_csv_structure, parse_csv_file, get_file_info,
    validate_csv_not_empty, handle_encoding_error, FileEncodingError
)
from database_manager import DatabaseManager, handle_duplicates
from filter_engine import FilterEngine
from kpi_calculator import KPICalculator
from visualization_engine import VisualizationEngine

# Configure Streamlit page
st.set_page_config(
    page_title="Analyse de Performance des Etudiants",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

