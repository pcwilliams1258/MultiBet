"""Data transformer for processing and cleaning betting data."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime


class DataTransformer:
    """Transforms and cleans raw betting data for model consumption."""
    
    def __init__(self):
        """Initialize the data transformer."""
        pass
    
    def transform_odds_data(self, raw_odds: Dict[str, Any]) -> Dict[str, float]:
        """Transform raw odds data into standardized format.
        
        Args:
            raw_odds: Raw odds data from API
            
        Returns:
            Standardized odds dictionary
        """
        transformed = {}
        
        # Ensure odds are in decimal format
        for key, value in raw_odds.items():
            if isinstance(value, (int, float)) and value > 0:
                transformed[key] = float(value)
            elif isinstance(value, str):
                try:
                    transformed[key] = float(value)
                except ValueError:
                    # Handle fractional odds or other formats
                    transformed[key] = self._convert_fractional_odds(value)
        
        return transformed
    
    def _convert_fractional_odds(self, fractional_odds: str) -> float:
        """Convert fractional odds to decimal odds.
        
        Args:
            fractional_odds: Odds in fractional format (e.g., "3/2")
            
        Returns:
            Decimal odds
        """
        try:
            if '/' in fractional_odds:
                numerator, denominator = fractional_odds.split('/')
                return (float(numerator) / float(denominator)) + 1.0
            else:
                return float(fractional_odds)
        except:
            return 1.0  # Default to even odds if conversion fails
    
    def create_features(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create features for model training/prediction.
        
        Args:
            match_data: Raw match data
            
        Returns:
            Feature dictionary
        """
        features = {}
        
        # Basic match features
        features['sport'] = match_data.get('sport', 'unknown')
        features['home_team'] = match_data.get('home_team', '')
        features['away_team'] = match_data.get('away_team', '')
        
        # Odds-based features
        if 'current_odds' in match_data:
            odds = match_data['current_odds']
            features['home_odds'] = odds.get('home_win', 1.0)
            features['draw_odds'] = odds.get('draw', 1.0)
            features['away_odds'] = odds.get('away_win', 1.0)
            
            # Implied probabilities
            total_prob = (1/features['home_odds'] + 
                         1/features.get('draw_odds', float('inf')) + 
                         1/features['away_odds'])
            features['market_margin'] = max(0, total_prob - 1.0)
        
        # Time-based features
        if 'match_date' in match_data:
            match_date = match_data['match_date']
            if isinstance(match_date, str):
                match_date = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
            
            features['day_of_week'] = match_date.weekday()
            features['hour_of_day'] = match_date.hour
            features['is_weekend'] = match_date.weekday() >= 5
        
        return features
    
    def clean_historical_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess historical data.
        
        Args:
            data: Raw historical data DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        cleaned = data.copy()
        
        # Remove duplicates
        cleaned = cleaned.drop_duplicates(subset=['match_id'], keep='last')
        
        # Handle missing values
        numeric_columns = cleaned.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
        
        # Remove invalid odds (less than 1.0)
        odds_columns = [col for col in cleaned.columns if 'odds' in col.lower()]
        for col in odds_columns:
            cleaned = cleaned[cleaned[col] >= 1.0]
        
        # Remove matches with missing essential data
        essential_columns = ['home_team', 'away_team', 'match_date']
        for col in essential_columns:
            if col in cleaned.columns:
                cleaned = cleaned.dropna(subset=[col])
        
        return cleaned