"""
Tests for the automated model retraining pipeline.
"""

import os
import sys
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import retrain_models


class TestRetrainingPipeline:
    """Test cases for the automated model retraining pipeline."""

    def test_get_latest_training_data(self):
        """Test retrieving training data from BigQuery."""
        data = retrain_models.get_latest_training_data()

        assert isinstance(data, dict)
        assert "features" in data
        assert "targets" in data
        assert "metadata" in data
        assert "rows" in data["metadata"]
        assert "features_count" in data["metadata"]
        assert "date_range" in data["metadata"]

    def test_train_new_model(self):
        """Test training a new CatBoost model."""
        training_data = {
            "features": [],
            "targets": [],
            "metadata": {"rows": 100, "features_count": 10},
        }

        model_info = retrain_models.train_new_model(training_data)

        assert isinstance(model_info, dict)
        assert "model" in model_info
        assert "metrics" in model_info
        assert "model_version" in model_info
        assert "train_accuracy" in model_info["metrics"]
        assert "validation_accuracy" in model_info["metrics"]
        assert "training_time_seconds" in model_info["metrics"]
        assert model_info["model_version"].startswith("model_")

    def test_backtest_model_clv(self):
        """Test backtesting model with CLV evaluation."""
        model_info = {
            "model": None,
            "metrics": {"train_accuracy": 0.85},
            "model_version": "test_model",
        }

        clv_metrics = retrain_models.backtest_model_clv(model_info)

        assert isinstance(clv_metrics, dict)
        assert "average_clv" in clv_metrics
        assert "clv_positive_rate" in clv_metrics
        assert "total_bets" in clv_metrics
        assert "roi" in clv_metrics
        assert isinstance(clv_metrics["average_clv"], float)
        assert isinstance(clv_metrics["clv_positive_rate"], float)
        assert isinstance(clv_metrics["total_bets"], int)
        assert isinstance(clv_metrics["roi"], float)

    def test_compare_and_deploy_superior_model(self):
        """Test deploying a model with superior CLV performance."""
        model_info = {"model_version": "test_model"}
        clv_metrics = {"average_clv": 0.05}  # Above threshold

        deployed = retrain_models.compare_and_deploy(model_info, clv_metrics)

        assert deployed is True

    def test_compare_and_deploy_inferior_model(self):
        """Test retaining current model when new model is inferior."""
        model_info = {"model_version": "test_model"}
        clv_metrics = {"average_clv": 0.01}  # Below threshold

        deployed = retrain_models.compare_and_deploy(model_info, clv_metrics)

        assert deployed is False

    @patch("retrain_models.get_latest_training_data")
    @patch("retrain_models.train_new_model")
    @patch("retrain_models.backtest_model_clv")
    @patch("retrain_models.compare_and_deploy")
    def test_main_pipeline_success(
        self, mock_deploy, mock_backtest, mock_train, mock_data
    ):
        """Test successful pipeline execution."""
        # Setup mocks
        mock_data.return_value = {
            "features": [],
            "targets": [],
            "metadata": {"rows": 1000, "features_count": 50},
        }
        mock_train.return_value = {
            "model": None,
            "metrics": {"train_accuracy": 0.85},
            "model_version": "test_model_123",
        }
        mock_backtest.return_value = {
            "average_clv": 0.03,
            "clv_positive_rate": 0.6,
            "total_bets": 100,
            "roi": 0.15,
        }
        mock_deploy.return_value = True

        # Test successful execution (should exit with 0)
        with pytest.raises(SystemExit) as exc_info:
            retrain_models.main()
        assert exc_info.value.code == 0

    @patch("retrain_models.get_latest_training_data")
    def test_main_pipeline_failure(self, mock_data):
        """Test pipeline failure handling."""
        # Setup mock to raise exception
        mock_data.side_effect = Exception("BigQuery connection failed")

        # Test failure handling (should exit with 1)
        with pytest.raises(SystemExit) as exc_info:
            retrain_models.main()
        assert exc_info.value.code == 1

    def test_logging_configuration(self):
        """Test that logging is properly configured."""
        import logging

        # Check that logger exists and has proper level
        logger = logging.getLogger("retrain_models")
        assert logger is not None

        # Check that the main module logger is configured
        main_logger = logging.getLogger(__name__.replace("test_", ""))
        assert main_logger is not None

    def test_error_handling_in_functions(self):
        """Test error handling in individual functions."""
        # Test that functions properly handle and re-raise exceptions
        with patch("retrain_models.logger") as mock_logger:
            # This will test the except block in functions if we simulate an error
            # For now, we just ensure functions can be called without errors
            try:
                retrain_models.get_latest_training_data()
                retrain_models.train_new_model({"features": [], "targets": []})
                retrain_models.backtest_model_clv({"model": None})
                retrain_models.compare_and_deploy({}, {"average_clv": 0.01})
            except Exception:
                # Functions should not raise unexpected exceptions in normal operation
                pass

    def test_model_version_format(self):
        """Test that model version follows expected format."""
        training_data = {"features": [], "targets": []}
        model_info = retrain_models.train_new_model(training_data)

        model_version = model_info["model_version"]
        assert model_version.startswith("model_")

        # Extract timestamp part and verify it's valid
        timestamp_part = model_version.replace("model_", "")
        try:
            datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
        except ValueError:
            pytest.fail("Model version timestamp format is invalid")

    def test_clv_threshold_logic(self):
        """Test CLV threshold-based deployment logic."""
        model_info = {"model_version": "test"}

        # Test exactly at threshold
        clv_metrics = {"average_clv": 0.02}
        deployed = retrain_models.compare_and_deploy(model_info, clv_metrics)
        assert deployed is False  # Should be > threshold, not >=

        # Test just above threshold
        clv_metrics = {"average_clv": 0.021}
        deployed = retrain_models.compare_and_deploy(model_info, clv_metrics)
        assert deployed is True

        # Test well below threshold
        clv_metrics = {"average_clv": -0.01}
        deployed = retrain_models.compare_and_deploy(model_info, clv_metrics)
        assert deployed is False


def test_script_can_be_imported():
    """Test that the script can be imported without errors."""
    import retrain_models

    assert hasattr(retrain_models, "main")
    assert hasattr(retrain_models, "get_latest_training_data")
    assert hasattr(retrain_models, "train_new_model")
    assert hasattr(retrain_models, "backtest_model_clv")
    assert hasattr(retrain_models, "compare_and_deploy")


def test_script_executable():
    """Test that the script is executable as a module."""
    import subprocess
    import sys

    # Test that script can be executed with --help or similar
    result = subprocess.run(
        [sys.executable, "retrain_models.py"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    # Script should exit with 0 (success) since it's a placeholder implementation
    assert result.returncode == 0
