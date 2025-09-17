"""Racing logistic regression model for horse racing predictions."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
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


class RacingLogitModel(BaseModel):
    """Logistic regression model optimized for horse racing predictions."""
    
    def __init__(self, regularization: float = 1.0):
        """Initialize the racing logit model.
        
        Args:
            regularization: L2 regularization parameter
        """
        super().__init__()
        self.model = LogisticRegression(
            C=regularization,
            random_state=42,
            max_iter=1000
        )
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for training or prediction.
        
        Args:
            data: Input data DataFrame
            
        Returns:
            Prepared feature array
        """
        # Select relevant features for racing
        racing_features = [
            'horse_age', 'jockey_experience', 'trainer_wins',
            'recent_form_score', 'track_condition_score',
            'distance_suitability', 'weight_carried',
            'odds_implied_probability'
        ]
        
        # Create features if they don't exist
        for feature in racing_features:
            if feature not in data.columns:
                data[feature] = 0.0
        
        features = data[racing_features].copy()
        
        # Handle missing values
        features = features.fillna(features.mean())
        
        return features.values
    
    def train(self, training_data: pd.DataFrame):
        """Train the racing logit model.
        
        Args:
            training_data: DataFrame containing training data with target column
        """
        if 'target' not in training_data.columns:
            raise ValueError("Training data must contain 'target' column")
        
        # Prepare features and target
        X = self._prepare_features(training_data)
        y = training_data['target'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.feature_names = [col for col in training_data.columns if col != 'target']
        self.is_trained = True
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Make predictions on racing data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Array of predicted probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare features
        X = self._prepare_features(data)
        
        # Scale features using fitted scaler
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        probabilities = self.model.predict_proba(X_scaled)
        
        # Return probabilities for positive class
        return probabilities[:, 1] if probabilities.shape[1] > 1 else probabilities[:, 0]
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the trained model.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
        
        coefficients = self.model.coef_[0]
        importance = dict(zip(self.feature_names, abs(coefficients)))
        
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
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']