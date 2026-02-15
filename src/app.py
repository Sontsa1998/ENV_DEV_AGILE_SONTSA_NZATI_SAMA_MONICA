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


def render_upload_section():
    """Display file upload interface."""
    st.header("📁 Charger fichiers")
    st.markdown("Charger les fichiers contenant les données des performances Etudiants.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📌 Charger student_habits_performance.csv")
        habits_file = st.file_uploader(
            "Choose habits file",
            type="csv",
            key="habits_upload"
        )
    
    with col2:
        st.info("📌 Charger StudentPerformanceFactors.csv")
        factors_file = st.file_uploader(
            "Choose factors file",
            type="csv",
            key="factors_upload"
        )
    
    if habits_file or factors_file:
        try:
            if habits_file:
                # Read and parse habits file
                file_content = habits_file.read().decode("utf-8")
                df_habits = parse_csv_file(file_content)
                
                # Validate structure
                is_valid, error_msg = validate_csv_not_empty(df_habits)
                if not is_valid:
                    st.error(f"❌ Habits file error: {error_msg}")
                else:
                    # Remove duplicates
                    df_habits = handle_duplicates(df_habits, keep="first")
                    
                    # Import to database
                    st.session_state.db_manager.import_data(df_habits, "student_habits_performance")
                    st.success(f"✅ Habits file imported: {len(df_habits)} rows")
            
            if factors_file:
                # Read and parse factors file
                file_content = factors_file.read().decode("utf-8")
                df_factors = parse_csv_file(file_content)
                
                # Validate structure
                is_valid, error_msg = validate_csv_not_empty(df_factors)
                if not is_valid:
                    st.error(f"❌ Factors file error: {error_msg}")
                else:
                    # Remove duplicates
                    df_factors = handle_duplicates(df_factors, keep="first")
                    
                    # Import to database
                    st.session_state.db_manager.import_data(df_factors, "student_performance_factors")
                    st.success(f"✅ Factors file imported: {len(df_factors)} rows")
            
            st.session_state.data_loaded = True
        
        except FileEncodingError as e:
            st.error(f"❌ File encoding error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error processing files: {str(e)}")


