import pytest
import sys
from pathlib import Path

# Add the project root to the Python path so we can import from 'src'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core_engine.base_model import BasePredictiveModel

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
