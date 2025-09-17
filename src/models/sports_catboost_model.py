"""Sports CatBoost model for general sports betting predictions."""

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from typing import Dict, Any, List, Optional
import joblib

try:
    from ..core_engine.base_model import BaseModel
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core_engine.base_model import BaseModel


class SportsCatBoostModel(BaseModel):
    """CatBoost model optimized for sports betting predictions."""
    
    def __init__(self, 
                 iterations: int = 1000,
                 learning_rate: float = 0.1,
                 depth: int = 6):
        """Initialize the sports CatBoost model.
        
        Args:
            iterations: Number of boosting iterations
            learning_rate: Learning rate for training
            depth: Depth of trees
        """
        super().__init__()
        self.model = CatBoostClassifier(
            iterations=iterations,
            learning_rate=learning_rate,
            depth=depth,
            random_seed=42,
            verbose=False,
            eval_metric='Logloss'
        )
        self.categorical_features = []
        self.feature_names = []
        self.is_trained = False
    
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for training or prediction.
        
        Args:
            data: Input data DataFrame
            
        Returns:
            Prepared feature DataFrame
        """
        # Core sports betting features
        base_features = [
            'home_odds', 'away_odds', 'draw_odds',
            'home_form_score', 'away_form_score',
            'head_to_head_wins', 'head_to_head_draws',
            'home_advantage_score', 'league_strength',
            'season_progress', 'days_since_last_match'
        ]
        
        # Categorical features for CatBoost
        categorical_features = [
            'sport', 'league', 'home_team', 'away_team',
            'day_of_week', 'is_weekend'
        ]
        
        # Create features if they don't exist
        features = data.copy()
        
        for feature in base_features + categorical_features:
            if feature not in features.columns:
                if feature in categorical_features:
                    features[feature] = 'unknown'
                else:
                    features[feature] = 0.0
        
        # Encode categorical variables
        for feature in categorical_features:
            features[feature] = features[feature].astype(str)
        
        self.categorical_features = categorical_features
        
        # Select only the features we want
        all_features = base_features + categorical_features
        features = features[all_features]
        
        # Handle missing values
        for col in base_features:
            features[col] = features[col].fillna(features[col].mean())
        
        for col in categorical_features:
            features[col] = features[col].fillna('unknown')
        
        return features
    
    def train(self, training_data: pd.DataFrame):
        """Train the CatBoost model.
        
        Args:
            training_data: DataFrame containing training data with target column
        """
        if 'target' not in training_data.columns:
            raise ValueError("Training data must contain 'target' column")
        
        # Prepare features and target
        X = self._prepare_features(training_data)
        y = training_data['target'].values
        
        # Get categorical feature indices
        cat_feature_indices = [
            X.columns.get_loc(feature) 
            for feature in self.categorical_features 
            if feature in X.columns
        ]
        
        # Train model
        self.model.fit(
            X, y,
            cat_features=cat_feature_indices,
            verbose=False
        )
        
        self.feature_names = list(X.columns)
        self.is_trained = True
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Make predictions on sports data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Array of predicted probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare features
        X = self._prepare_features(data)
        
        # Make predictions
        probabilities = self.model.predict_proba(X)
        
        # Return probabilities for positive class
        return probabilities[:, 1] if probabilities.shape[1] > 1 else probabilities[:, 0]
    
    def predict_multiclass(self, data: pd.DataFrame) -> np.ndarray:
        """Make multiclass predictions (home/draw/away).
        
        Args:
            data: Input data for prediction
            
        Returns:
            Array of predicted probabilities for each class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare features
        X = self._prepare_features(data)
        
        # Make predictions
        return self.model.predict_proba(X)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the trained model.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        importance_scores = self.model.get_feature_importance()
        importance = dict(zip(self.feature_names, importance_scores))
        
        # Normalize to sum to 1
        total = sum(importance.values())
        if total > 0:
            importance = {k: v/total for k, v in importance.items()}
        
        return importance
    
    def save_model(self, filepath: str):
        """Save the trained model to disk.
        
        Args:
            filepath: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        self.model.save_model(filepath)
        
        # Save additional metadata
        metadata = {
            'feature_names': self.feature_names,
            'categorical_features': self.categorical_features,
            'is_trained': self.is_trained
        }
        
        joblib.dump(metadata, f"{filepath}.metadata")
    
    def load_model(self, filepath: str):
        """Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
        """
        self.model.load_model(filepath)
        
        # Load metadata
        metadata = joblib.load(f"{filepath}.metadata")
        self.feature_names = metadata['feature_names']
        self.categorical_features = metadata['categorical_features']
        self.is_trained = metadata['is_trained']