"""
Statistical analysis functions for Economic Freedom Index
"""

import pandas as pd
import numpy as np
from scipy import stats
from config import FREEDOM_CATEGORIES, ECONOMIC_INDICATORS


class Analysis:
    """Class for statistical analysis"""
    
    @staticmethod
    def get_summary_statistics(data):
        """Calculate summary statistics"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        summary = pd.DataFrame({
            'Mean': data[numeric_cols].mean(),
            'Median': data[numeric_cols].median(),
            'Std Dev': data[numeric_cols].std(),
            'Min': data[numeric_cols].min(),
            'Max': data[numeric_cols].max(),
            'Missing': data[numeric_cols].isnull().sum()
        }).round(2)
        
        return summary
    
    @staticmethod
    def get_category_stats(data):
        """Get statistics for each category"""
        category_stats = pd.DataFrame({
            'Mean': data[FREEDOM_CATEGORIES].mean(),
            'Std Dev': data[FREEDOM_CATEGORIES].std(),
            'Min': data[FREEDOM_CATEGORIES].min(),
            'Max': data[FREEDOM_CATEGORIES].max()
        }).round(2)
        
        return category_stats.sort_values('Mean', ascending=False)
    
    @staticmethod
    def correlate_with_freedom(data, column):
        """Calculate correlation of a variable with freedom score"""
        valid_data = data[[column, '2022 Score']].dropna()
        
        if len(valid_data) < 2:
            return None, None
        
        correlation = valid_data[column].corr(valid_data['2022 Score'])
        _, p_value = stats.pearsonr(valid_data[column], valid_data['2022 Score'])
        
        return correlation, p_value
    
    @staticmethod
    def get_correlations_with_freedom(data):
        """Get correlations of all indicators with freedom score"""
        correlations = {}
        
        for col in ECONOMIC_INDICATORS:
            if col in data.columns:
                corr, p_val = Analysis.correlate_with_freedom(data, col)
                if corr is not None:
                    correlations[col] = {
                        'Correlation': corr,
                        'P-Value': p_val,
                        'Significant': 'Yes' if p_val < 0.05 else 'No'
                    }
        
        return pd.DataFrame(correlations).T.round(4)
    
    @staticmethod
    def get_top_categories_by_country(data, country_name):
        """Get top performing categories for a country"""
        country = data[data['Country Name'] == country_name].iloc[0]
        
        category_scores = {cat: country[cat] for cat in FREEDOM_CATEGORIES if cat in country.index}
        
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        return pd.DataFrame(sorted_categories, columns=['Category', 'Score']).round(2)
    
    @staticmethod
    def compare_countries(data, countries):
        """Compare multiple countries"""
        filtered = data[data['Country Name'].isin(countries)][
            ['Country Name', '2022 Score', 'Region'] + FREEDOM_CATEGORIES
        ]
        
        return filtered.round(2)
    
    @staticmethod
    def calculate_category_contribution(data, country_name):
        """Calculate each category's contribution to overall score"""
        country = data[data['Country Name'] == country_name].iloc[0]
        overall_score = country['2022 Score']
        
        contributions = {}
        for category in FREEDOM_CATEGORIES:
            if category in country.index:
                score = country[category]
                contribution = (score / overall_score) * 100 if overall_score > 0 else 0
                contributions[category] = contribution
        
        contrib_df = pd.DataFrame(
            list(contributions.items()),
            columns=['Category', 'Contribution %']
        ).sort_values('Contribution %', ascending=False)
        
        return contrib_df.round(2)