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

# Add custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "db_manager" not in st.session_state:
    st.session_state.db_manager = DatabaseManager(":memory:")

if "filters" not in st.session_state:
    st.session_state.filters = {}

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False


def render_header():
    """Display application title and description."""
    st.title("📊 Student Performance Analyzer")
    st.subheader("MEMBRE DU GROUPE : SONTSA CHRISTIAN - NZATI STEPHANE - SAMA CAMELIA - MBOULA MONICA")
    st.markdown("""
    Bienvenue dans l’Analyseur de performance des étudiants ! Cette application aide les enseignants et les administrateurs à analyser les données de performance des étudiants grâce à des visualisations interactives et des filtres dynamiques.
    Fonctionnalités :
    <br/>- Importer et gérer les données de performance des étudiants
    <br/>- Appliquer des filtres dynamiques pour cibler des groupes d’étudiants spécifiques
    <br/>- Consulter quatre indicateurs clés de performance (KPI)
    <br/>- Explorer les relations entre les habitudes d’étude et les performances académiques
    """, unsafe_allow_html=True
)


