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

    