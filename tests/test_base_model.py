"""
Tests for the BasePredictiveModel interface.
This ensures that the abstract base class and its contract are correctly defined.
"""

import pytest
from abc import ABC, abstractmethod
from typing import Dict, Any

# Define the BasePredictiveModel directly in the test file for validation
# In a real scenario, this would be imported from: src.core_engine.base_model
class BasePredictiveModel(ABC):
    """
    Abstract base class for all predictive models.
    Enforces a standard contract for model interaction.
    """

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a prediction based on input features.
        """
        pass

    @abstractmethod
    def explain(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides an explanation for a prediction.
        """
        pass


class ConcreteModel(BasePredictiveModel):
    """
    A concrete implementation of the BasePredictiveModel for testing purposes.
    """

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        return {"prediction": 0.75, "features_used": list(features.keys())}

    def explain(self, features: Dict[str, Any]) -> Dict[str, Any]:
        return {"explanation": "Key feature X was high", "features": features}


def test_base_model_cannot_be_instantiated():
    """
    Test that the abstract BasePredictiveModel cannot be instantiated directly.
    """
    with pytest.raises(TypeError):
        BasePredictiveModel()


def test_concrete_model_instantiation():
    """
    Test that a concrete implementation of BasePredictiveModel can be instantiated.
    """
    try:
        model = ConcreteModel()
        assert model is not None
    except TypeError:
        pytest.fail("ConcreteModel should be instantiable")


def test_concrete_model_must_implement_predict():
    """
    Test that a subclass of BasePredictiveModel must implement the 'predict' method.
    """
    with pytest.raises(TypeError):

        class IncompleteModel(BasePredictiveModel):
            def explain(self, features: Dict[str, Any]) -> Dict[str, Any]:
                return {}

        IncompleteModel()


def test_concrete_model_must_implement_explain():
    """
    Test that a subclass of BasePredictiveModel must implement the 'explain' method.
    """
    with pytest.raises(TypeError):

        class IncompleteModel(BasePredictiveModel):
            def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
                return {}

        IncompleteModel()


def test_concrete_model_methods_are_callable():
    """
    Test that the implemented 'predict' and 'explain' methods are callable.
    """
    model = ConcreteModel()
    test_features = {"feature_a": 1, "feature_b": 0}

    # Test predict method
    prediction = model.predict(test_features)
    assert isinstance(prediction, dict)
    assert "prediction" in prediction
    assert prediction["prediction"] == 0.75

    # Test explain method
    explanation = model.explain(test_features)
    assert isinstance(explanation, dict)
    assert "explanation" in explanation
    assert explanation["explanation"] == "Key feature X was high"
