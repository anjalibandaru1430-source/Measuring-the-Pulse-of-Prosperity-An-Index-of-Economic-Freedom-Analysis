"""
Economic Freedom Index Analysis Dashboard
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.data_processor import DataProcessor
from src.visualizations import Visualizations
from src.analysis import Analysis
from config import REGIONS, TOP_N, BOTTOM_N, FREEDOM_CATEGORIES, ECONOMIC_INDICATORS

# Configure page
st.set_page_config(
    page_title="Economic Freedom Index Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 0;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .highlight {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    @st.cache_resource
    def load_data():
        processor = DataProcessor()
        data = processor.load_data()
        data = processor.clean_data()
        return data
    
    st.session_state.data = load_data()

data = st.session_state.data

# Header
st.title("📊 Measuring the Pulse of Prosperity")
st.subheader("An Index of Economic Freedom Analysis Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")
    page = st.radio(
        "Select Page:",
        [
            "Overview",
            "Rankings",
            "Regional Analysis",
            "Factor Analysis",
            "Economic Indicators",
            "Comparisons",
            "Detailed Analysis"
        ]
    )
    
    st.markdown("---")
    st.header("📋 Filters")
    
    selected_region = st.multiselect(
        "Select Regions:",
        options=sorted(data['Region'].unique()),
        default=sorted(data['Region'].unique())
    )
    
    filtered_data = data[data['Region'].isin(selected_region)]
    
    st.markdown("---")
    st.markdown("**Dataset Info:**")
    st.info(f"""
    - **Countries:** {len(filtered_data)}
    - **Regions:** {len(selected_region)}
    - **Avg Score:** {filtered_data['2022 Score'].mean():.2f}
    - **Data Year:** 2022
    """)

# PAGE FUNCTIONS
def show_overview(filtered_data, full_data):
    """Overview page"""
    st.header("📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = filtered_data['2022 Score'].mean()
        st.metric(
            "Average Freedom Score",
            f"{avg_score:.2f}",
            delta=f"+{avg_score - full_data['2022 Score'].mean():.2f}"
        )
    
    with col2:
        countries = len(filtered_data)
        st.metric("Countries Analyzed", countries)
    
    with col3:
        total_gdp = filtered_data['GDP (Billions)'].sum()
        st.metric("Total GDP", f"${total_gdp:.1f}B")
    
    with col4:
        avg_gdp_pc = filtered_data['GDP per Capita (PPP)'].mean()
        st.metric("Avg GDP per Capita", f"${avg_gdp_pc:.0f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Countries")
        top_countries = Analysis.compare_countries(
            filtered_data, filtered_data.nlargest(10, '2022 Score')['Country Name'].tolist()
        )[['Country Name', 'Region', '2022 Score']]
        st.dataframe(top_countries, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📉 Bottom 10 Countries")
        bottom_countries = Analysis.compare_countries(
            filtered_data, filtered_data.nsmallest(10, '2022 Score')['Country Name'].tolist()
        )[['Country Name', 'Region', '2022 Score']]
        st.dataframe(bottom_countries, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Regional Comparison")
        Visualizations.plot_regional_comparison(filtered_data)
    
    with col2:
        st.subheader("📊 Score Distribution")
        Visualizations.plot_score_distribution(filtered_data)
    
    st.markdown("---")
    
    st.subheader("🎓 Freedom Classification")
    Visualizations.plot_score_classification(filtered_data)


def show_rankings(filtered_data):
    """Rankings page"""
    st.header("🏆 Country Rankings")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        ranking_count = st.slider("Number of Countries", 5, 30, 15)
    
    st.markdown("---")
    
    st.subheader(f"🥇 Top {ranking_count} Countries")
    Visualizations.plot_country_rankings(filtered_data, ranking_count)
    
    st.markdown("---")
    
    st.subheader("📋 Detailed Rankings Table")
    ranking_table = filtered_data.nlargest(ranking_count, '2022 Score')[
        ['World Rank', 'Country Name', 'Region', '2022 Score', 'GDP (Billions)', 'Population (Millions)']
    ].reset_index(drop=True)
    ranking_table.index = ranking_table.index + 1
    st.dataframe(ranking_table, use_container_width=True)


def show_regional_analysis(filtered_data):
    """Regional Analysis page"""
    st.header("🗺️ Regional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Regional Performance")
        Visualizations.plot_regional_comparison(filtered_data)
    
    with col2:
        st.subheader("Category Statistics")
        st.dataframe(Analysis.get_category_stats(filtered_data), use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📊 Regional Statistics")
    regional_stats = filtered_data.groupby('Region').agg({
        '2022 Score': ['mean', 'min', 'max'],
        'GDP (Billions)': 'sum',
        'Population (Millions)': 'sum'
    }).round(2)
    st.dataframe(regional_stats, use_container_width=True)


def show_factor_analysis(filtered_data):
    """Factor Analysis page"""
    st.header("🔍 Freedom Category Analysis")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        selected_country = st.selectbox(
            "Select Country:",
            options=sorted(filtered_data['Country Name'].tolist())
        )
    
    if selected_country:
        country_data = filtered_data[filtered_data['Country Name'] == selected_country].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Category Breakdown")
            Visualizations.plot_category_breakdown(country_data)
        
        with col2:
            st.subheader("Top Performing Categories")
            top_categories = Analysis.get_top_categories_by_country(filtered_data, selected_country)
            st.dataframe(top_categories, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("📊 Category Statistics")
    category_stats = Analysis.get_category_stats(filtered_data)
    st.dataframe(category_stats, use_container_width=True)


def show_economic_indicators(filtered_data):
    """Economic Indicators page"""
    st.header("💰 Economic Indicators Analysis")
    
    st.subheader("Correlation with Economic Freedom Score")
    correlations = Analysis.get_correlations_with_freedom(filtered_data)
    st.dataframe(correlations, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Freedom Score vs GDP")
        Visualizations.plot_gdp_vs_freedom(filtered_data)
    
    with col2:
        st.subheader("Freedom Score vs Unemployment")
        Visualizations.plot_unemployment_vs_freedom(filtered_data)
    
    st.markdown("---")
    
    st.subheader("Freedom Score vs Inflation")
    Visualizations.plot_inflation_vs_freedom(filtered_data)


def show_comparisons(filtered_data):
    """Comparisons page"""
    st.header("🔄 Country Comparisons")
    
    selected_countries = st.multiselect(
        "Select Countries to Compare:",
        options=sorted(filtered_data['Country Name'].tolist()),
        default=sorted(filtered_data['Country Name'].tolist())[:3]
    )
    
    if selected_countries:
        st.markdown("---")
        
        st.subheader("Detailed Comparison Table")
        comparison = Analysis.compare_countries(filtered_data, selected_countries)
        st.dataframe(comparison, use_container_width=True, hide_index=True)


def show_detailed_analysis(filtered_data):
    """Detailed Analysis page"""
    st.header("📊 Detailed Statistical Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Summary Stats", "Correlations", "Country Insights"])
    
    with tab1:
        st.subheader("Statistical Summary")
        summary_stats = Analysis.get_summary_statistics(filtered_data)
        st.dataframe(summary_stats, use_container_width=True)
    
    with tab2:
        st.subheader("Correlation Matrix")
        Visualizations.plot_heatmap_correlation(filtered_data)
    
    with tab3:
        selected_country = st.selectbox(
            "Select Country for Detailed Insights:",
            options=sorted(filtered_data['Country Name'].tolist()),
            key="insights_country"
        )
        
        if selected_country:
            country = filtered_data[filtered_data['Country Name'] == selected_country].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Overall Score", f"{country['2022 Score']:.2f}")
                st.metric("World Rank", int(country['World Rank']))
                st.metric("GDP (Billions)", f"${country['GDP (Billions)']:.1f}")
            
            with col2:
                st.metric("GDP per Capita", f"${country['GDP per Capita (PPP)']:.0f}")
                st.metric("Population", f"{country['Population (Millions)']:.1f}M")
                st.metric("Unemployment Rate", f"{country['Unemployment (%)']:.1f}%")
            
            st.markdown("---")
            st.subheader("Category Contribution")
            contribution = Analysis.calculate_category_contribution(filtered_data, selected_country)
            st.dataframe(contribution, use_container_width=True, hide_index=True)


# Page routing
if page == "Overview":
    show_overview(filtered_data, data)
elif page == "Rankings":
    show_rankings(filtered_data)
elif page == "Regional Analysis":
    show_regional_analysis(filtered_data)
elif page == "Factor Analysis":
    show_factor_analysis(filtered_data)
elif page == "Economic Indicators":
    show_economic_indicators(filtered_data)
elif page == "Comparisons":
    show_comparisons(filtered_data)
elif page == "Detailed Analysis":
    show_detailed_analysis(filtered_data)

# Footer
st.markdown("---")
st.markdown("""
<center>
📊 Economic Freedom Index Dashboard | Data: Heritage Foundation & World Bank | Last Updated: 2026-02-23
</center>
""", unsafe_allow_html=True)