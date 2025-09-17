import pytest
from src.core_engine.base_model import BasePredictiveModel

def test_base_predictive_model_import():
    """
    Tests that the BasePredictiveModel can be imported successfully.
    """
    assert BasePredictiveModel is not None, "BasePredictiveModel should be importable"

def test_cannot_instantiate_base_model():
    """
    Tests that BasePredictiveModel cannot be instantiated directly,
    proving it is a proper abstract class.
    """
    with pytest.raises(TypeError, match="Can't instantiate abstract class BasePredictiveModel with abstract methods explain, predict"):
        BasePredictiveModel()
