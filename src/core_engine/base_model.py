from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePredictiveModel(ABC):
    """
    Abstract base class for all predictive models.
    Enforces a standard contract for model interaction.
    """

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a prediction based on input features.

        Args:
            features: A dictionary of feature names and their values.

        Returns:
            A dictionary containing the prediction, typically including
            outcome probabilities and a model confidence score.
        """
        pass

    @abstractmethod
    def explain(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides an explanation for a prediction using SHAP or a similar method.

        Args:
            features: A dictionary of feature names and their values.

        Returns:
            A dictionary detailing the contribution of each feature to the
            final prediction.
        """
        pass
