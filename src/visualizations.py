"""
Visualization functions for Economic Freedom Index Dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from config import (
    CATEGORY_COLORS, REGION_COLORS, PRIMARY_COLORS, 
    COLORSCALE, FREEDOM_CATEGORIES
)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'


class Visualizations:
    """Class for creating visualizations"""
    
    @staticmethod
    def plot_country_rankings(data, top_n=15):
        """Create horizontal bar chart of top countries"""
        top_data = data.nlargest(top_n, '2022 Score')
        
        fig = px.bar(
            top_data.sort_values('2022 Score'),
            x='2022 Score',
            y='Country Name',
            orientation='h',
            color='2022 Score',
            color_continuous_scale=COLORSCALE,
            hover_data=['Region', 'World Rank'],
            title=f'Top {top_n} Countries by Economic Freedom Score',
            labels={'2022 Score': 'Economic Freedom Score', 'Country Name': 'Country'}
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_regional_comparison(data):
        """Create regional performance comparison"""
        regional_stats = data.groupby('Region').agg({
            '2022 Score': 'mean'
        }).reset_index().sort_values('2022 Score', ascending=False)
        
        fig = px.bar(
            regional_stats,
            x='Region',
            y='2022 Score',
            color='Region',
            color_discrete_map=REGION_COLORS,
            title='Average Economic Freedom Score by Region',
            labels={'2022 Score': 'Average Score'}
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_category_breakdown(country_data):
        """Create radar chart for country category breakdown"""
        categories = FREEDOM_CATEGORIES
        values = [country_data.get(cat, 0) for cat in categories]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=country_data.get('Country Name', 'Country'),
            marker=dict(color='#3498db')
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title=f"Economic Freedom Factors - {country_data.get('Country Name', 'Country')}",
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_score_distribution(data):
        """Create histogram of score distribution"""
        fig = px.histogram(
            data,
            x='2022 Score',
            nbins=20,
            title='Distribution of Economic Freedom Scores',
            labels={'2022 Score': 'Score', 'count': 'Number of Countries'},
            color_discrete_sequence=['#3498db'],
            marginal='box'
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_gdp_vs_freedom(data):
        """Scatter plot: GDP vs Freedom Score"""
        filtered = data[(data['GDP (Billions)'] > 0) & (data['2022 Score'] > 0)].copy()
        
        fig = px.scatter(
            filtered,
            x='2022 Score',
            y='GDP (Billions)',
            color='Region',
            color_discrete_map=REGION_COLORS,
            size='Population (Millions)',
            hover_data=['Country Name'],
            title='Economic Freedom Score vs GDP',
            labels={'GDP (Billions)': 'GDP (Billions)', '2022 Score': 'Freedom Score'},
            height=500,
            log_y=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_unemployment_vs_freedom(data):
        """Scatter plot: Unemployment vs Freedom Score"""
        filtered = data[(data['Unemployment (%)'] > 0) & (data['2022 Score'] > 0)].copy()
        
        fig = px.scatter(
            filtered,
            x='2022 Score',
            y='Unemployment (%)',
            color='Region',
            color_discrete_map=REGION_COLORS,
            hover_data=['Country Name'],
            title='Economic Freedom Score vs Unemployment Rate',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_inflation_vs_freedom(data):
        """Scatter plot: Inflation vs Freedom Score"""
        filtered = data[(data['Inflation (%)'].between(-50, 200)) & (data['2022 Score'] > 0)].copy()
        
        fig = px.scatter(
            filtered,
            x='2022 Score',
            y='Inflation (%)',
            color='Region',
            color_discrete_map=REGION_COLORS,
            hover_data=['Country Name'],
            title='Economic Freedom Score vs Inflation Rate',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_heatmap_correlation(data):
        """Create correlation heatmap"""
        numeric_data = data[FREEDOM_CATEGORIES].copy()
        numeric_data = numeric_data.fillna(numeric_data.mean())
        
        corr_matrix = numeric_data.corr()
        
        fig = px.imshow(
            corr_matrix,
            title='Correlation Matrix of Freedom Categories',
            color_continuous_scale='RdBu',
            zmin=-1,
            zmax=1,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_score_classification(data):
        """Plot countries by freedom classification"""
        def classify_score(score):
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
        
        data_copy = data.copy()
        data_copy['Classification'] = data_copy['2022 Score'].apply(classify_score)
        
        classification_counts = data_copy['Classification'].value_counts().reindex(
            ['Free', 'Mostly Free', 'Moderately Free', 'Mostly Unfree', 'Repressed']
        )
        
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b']
        
        fig = px.bar(
            x=classification_counts.index,
            y=classification_counts.values,
            color=classification_counts.index,
            color_discrete_sequence=colors,
            title='Countries by Freedom Classification',
            labels={'x': 'Classification', 'y': 'Number of Countries'},
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)