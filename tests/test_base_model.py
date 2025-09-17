import pytest

from core_engine.base_model import BasePredictiveModel

def test_base_model_can_be_imported():
    """
    Test that the BasePredictiveModel can be imported without error.
    """
    assert BasePredictiveModel is not None

def test_base_model_is_abstract():
    """
    Test that BasePredictiveModel cannot be instantiated directly,
    proving it is an abstract class.
    """
    with pytest.raises(TypeError):
        BasePredictiveModel()
