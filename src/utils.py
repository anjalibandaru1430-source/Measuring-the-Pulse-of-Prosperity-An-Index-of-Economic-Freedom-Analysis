"""
Utility functions for the dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime


def format_number(num, decimals=2):
    """Format number with thousands separator"""
    if pd.isna(num):
        return "N/A"
    return f"{num:,.{decimals}f}"


def format_percentage(num, decimals=1):
    """Format as percentage"""
    if pd.isna(num):
        return "N/A"
    return f"{num:.{decimals}f}%"


def classify_score(score):
    """Classify freedom score"""
    if score >= 80:
        return 'Free'
    elif score >= 70:
        return 'Mostly Free'
    elif score >= 60:
        return 'Moderately Free'
    elif score >= 50:
        return 'Mostly Unfree'
    else:
        return 'Repressed'


def get_classification_color(classification):
    """Get color for classification"""
    colors = {
        'Free': '#2ecc71',
        'Mostly Free': '#f1c40f',
        'Moderately Free': '#e67e22',
        'Mostly Unfree': '#e74c3c',
        'Repressed': '#c0392b'
    }
    return colors.get(classification, '#95a5a6')


def safe_divide(numerator, denominator):
    """Safe division handling zero"""
    if denominator == 0:
        return 0
    return numerator / denominator


def round_smart(value, decimals=2):
    """Round value intelligently"""
    if pd.isna(value):
        return None
    if value == 0:
        return 0
    return round(value, decimals)