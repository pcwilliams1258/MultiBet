import pytest

from core_engine.base_model import BasePredictiveModel


def test_base_model_can_be_imported():
    """
    Validates that the BasePredictiveModel class can be imported
    without syntax or path errors.
    """
    assert BasePredictiveModel is not None


def test_base_model_is_abstract_and_cannot_be_instantiated():
    """
    Ensures that BasePredictiveModel is a true abstract class.

    This test is critical to enforce the architectural pattern that
    developers must create a concrete implementation (e.g., a specific
    sports model) rather than using the base class directly.
    """
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        BasePredictiveModel()
