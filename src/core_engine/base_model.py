from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePredictiveModel(ABC):
    """
    Abstract base class for all predictive models.

    This class defines the standard contract that all models must follow
    to integrate with the core betting engine. It ensures a pluggable
    architecture where new models can be added with a consistent interface.
    """

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a prediction based on input features.

        Args:
            features: A dictionary of feature names and their values
                      required by the model.

        Returns:
            A dictionary containing the prediction results, which must
            conform to the standard prediction object schema. This includes
            outcome probabilities and a model confidence score.
        """
        pass

    @abstractmethod
    def explain(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides an explanation for a prediction, typically using SHAP.

        This method details the contribution of each feature to the final
        prediction, which is crucial for model transparency and the
        calculation of a Model Confidence Score (MCS).

        Args:
            features: A dictionary of feature names and their values.

        Returns:
            A dictionary detailing the feature contributions.
        """
        pass
