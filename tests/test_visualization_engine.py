"""
Unit tests for visualization_engine module.
"""

import pytest
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from visualization_engine import VisualizationEngine


class TestVisualizationEngine:
    """Tests for VisualizationEngine class."""

    @pytest.fixture
    def sample_kpi1_data(self):
        """Sample data for KPI 1."""
        return pd.DataFrame({
            "group": ["Male", "Female"],
            "average_score": [85.0, 88.0],
            "count": [50, 50]
        })
    
    @pytest.fixture
    def sample_kpi2_data(self):
        """Sample data for KPI 2."""
        return pd.DataFrame({
            "study_hours": [4.0, 5.0, 6.0, 7.0],
            "exam_score": [75.0, 80.0, 85.0, 90.0]
        })
    
    @pytest.fixture
    def sample_kpi3_data(self):
        """Sample data for KPI 3."""
        return pd.DataFrame({
            "attendance_range": [70.0, 80.0, 90.0],
            "average_score": [75.0, 82.0, 88.0],
            "count": [30, 40, 30]
        })
    
    @pytest.fixture
    def sample_kpi4_data(self):
        """Sample data for KPI 4."""
        return pd.DataFrame({
            "sleep_hours": [6.0, 7.0, 8.0, 9.0],
            "exam_score": [70.0, 80.0, 85.0, 88.0]
        })
    