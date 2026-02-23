"""
Configuration settings for Economic Freedom Index Dashboard
"""

# File Paths
DATA_PATH = "data/index_of_economic_freedom.csv"

# Display Settings
CHART_HEIGHT = 500
CHART_WIDTH = 1000
PAGE_LAYOUT = "wide"

# Color Palettes
PRIMARY_COLORS = {
    'free': '#2ecc71',
    'mostly_free': '#f1c40f',
    'moderately_free': '#e67e22',
    'mostly_unfree': '#e74c3c',
    'repressed': '#c0392b'
}

CATEGORY_COLORS = {
    'Property Rights': '#3498db',
    'Judical Effectiveness': '#9b59b6',
    'Government Integrity': '#e74c3c',
    'Tax Burden': '#1abc9c',
    'Govt Spending': '#f39c12',
    'Fiscal Health': '#2ecc71',
    'Business Freedom': '#34495e',
    'Labor Freedom': '#16a085',
    'Monetary Freedom': '#8e44ad',
    'Trade Freedom': '#c0392b',
    'Investment Freedom ': '#27ae60',
    'Financial Freedom': '#2980b9'
}

REGION_COLORS = {
    'Asia-Pacific': '#3498db',
    'Europe': '#e74c3c',
    'Americas': '#f39c12',
    'Middle East and North Africa': '#9b59b6',
    'Sub-Saharan Africa': '#1abc9c'
}

# Score Classification
SCORE_CLASSIFICATION = {
    'Free': (80, 100),
    'Mostly Free': (70, 79.9),
    'Moderately Free': (60, 69.9),
    'Mostly Unfree': (50, 59.9),
    'Repressed': (0, 49.9)
}

# Category Settings
FREEDOM_CATEGORIES = [
    'Property Rights',
    'Judical Effectiveness',
    'Government Integrity',
    'Tax Burden',
    'Govt Spending',
    'Fiscal Health',
    'Business Freedom',
    'Labor Freedom',
    'Monetary Freedom',
    'Trade Freedom',
    'Investment Freedom ',
    'Financial Freedom'
]

ECONOMIC_INDICATORS = [
    'Population (Millions)',
    'GDP (Billions)',
    'GDP Growth Rate (%)',
    '5 Year GDP Growth Rate (%)',
    'GDP per Capita (PPP)',
    'Unemployment (%)',
    'Inflation (%)',
    'FDI Inflow (Millions)',
    'Public Debt (% of GDP)'
]

# Regional Settings
REGIONS = [
    'Asia-Pacific',
    'Europe',
    'Americas',
    'Middle East and North Africa',
    'Sub-Saharan Africa'
]

# Threshold Settings
TOP_N = 10
BOTTOM_N = 10

# Chart Settings
CHART_FONT_SIZE = 12
TITLE_FONT_SIZE = 16
COLORSCALE = 'RdYlGn'

# Statistical Settings
CORRELATION_THRESHOLD = 0.3
DECIMAL_PLACES = 2

# Dashboard Settings
SIDEBAR_WIDTH = 250
METRIC_COLUMNS = 4