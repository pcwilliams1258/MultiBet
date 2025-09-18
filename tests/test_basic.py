"""
Basic validation tests for the MultiBet repository.
"""

import os
import sys


def test_placeholder():
    """Placeholder test to ensure CI pipeline works"""
    assert True


def test_python_version():
    """Test that we're running on a supported Python version"""
    assert sys.version_info >= (3, 8)


def test_repository_structure():
    """Test that key directories exist"""
    assert os.path.exists("src")
    assert os.path.exists(".github")


def test_imports():
    """Test that basic Python imports work"""
    try:
        import datetime
        import json
        import pathlib

        # Use the imports to avoid linting errors
        assert json is not None
        assert datetime is not None
        assert pathlib is not None
    except ImportError as e:
        assert False, f"Failed to import basic modules: {e}"


def test_yaml_import():
    """Test that PyYAML is available (addresses issue #65)"""
    try:
        import yaml

        # Test basic yaml functionality
        test_data = {"test": "value", "number": 42}
        yaml_string = yaml.dump(test_data)
        parsed_data = yaml.safe_load(yaml_string)

        assert yaml is not None
        assert parsed_data["test"] == "value"
        assert parsed_data["number"] == 42
    except ImportError as e:
        assert (
            False
        ), f"Failed to import yaml module: {e}. This indicates PyYAML is not installed."
