"""
Data processing and cleaning module for Economic Freedom Index data
"""

import pandas as pd
import numpy as np
from config import DATA_PATH, FREEDOM_CATEGORIES, ECONOMIC_INDICATORS


class DataProcessor:
    """Class for loading and processing economic freedom data"""
    
    def __init__(self, file_path=DATA_PATH):
        self.file_path = file_path
        self.data = None
        self.original_data = None
    
    def load_data(self):
        """Load data from CSV file"""
        try:
            self.data = pd.read_csv(self.file_path)
            self.original_data = self.data.copy()
            print(f"✓ Data loaded successfully: {len(self.data)} countries")
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def clean_data(self):
        """Clean and prepare data"""
        if self.data is None:
            self.load_data()
        
        # Remove duplicates
        self.data = self.data.drop_duplicates(subset=['Country_id'], keep='first')
        
        # Handle missing values
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if self.data[col].isnull().any():
                self.data[col] = self.data[col].fillna(self.data[col].mean())
        
        # Replace 0 values with NaN for certain columns (indicates missing data)
        columns_to_fix = FREEDOM_CATEGORIES + ['2022 Score']
        for col in columns_to_fix:
            if col in self.data.columns:
                self.data[col] = self.data[col].replace(0, np.nan)
        
        # Fill NaN with column mean
        self.data[columns_to_fix] = self.data[columns_to_fix].fillna(
            self.data[columns_to_fix].mean()
        )
        
        return self.data
    
    def get_data(self):
        """Get cleaned data"""
        if self.data is None:
            self.load_data()
            self.clean_data()
        return self.data
    
    def get_regions(self):
        """Get list of regions"""
        return sorted(self.data['Region'].unique())
    
    def get_countries_by_region(self, region):
        """Get countries in a specific region"""
        return sorted(self.data[self.data['Region'] == region]['Country Name'].tolist())
    
    def filter_by_region(self, region):
        """Filter data by region"""
        return self.data[self.data['Region'] == region]
    
    def filter_by_country(self, country):
        """Get data for a specific country"""
        filtered = self.data[self.data['Country Name'] == country]
        return filtered.iloc[0] if len(filtered) > 0 else None
    
    def get_top_countries(self, n=10):
        """Get top N countries by overall score"""
        return self.data.nlargest(n, '2022 Score')[['Country Name', 'Region', '2022 Score', 'World Rank']]
    
    def get_bottom_countries(self, n=10):
        """Get bottom N countries by overall score"""
        return self.data.nsmallest(n, '2022 Score')[['Country Name', 'Region', '2022 Score', 'World Rank']]
    
    def get_regional_stats(self):
        """Get statistics by region"""
        return self.data.groupby('Region').agg({
            '2022 Score': ['mean', 'min', 'max', 'std', 'count'],
            'GDP (Billions)': 'sum',
            'Population (Millions)': 'sum'
        }).round(2)
    
    def get_category_stats(self):
        """Get statistics for each freedom category"""
        stats = {}
        for category in FREEDOM_CATEGORIES:
            if category in self.data.columns:
                stats[category] = {
                    'Mean': self.data[category].mean(),
                    'Std': self.data[category].std(),
                    'Min': self.data[category].min(),
                    'Max': self.data[category].max()
                }
        return pd.DataFrame(stats).T.round(2)


def load_and_prepare_data():
    """Load and prepare data for dashboard"""
    processor = DataProcessor()
    data = processor.load_data()
    data = processor.clean_data()
    return data