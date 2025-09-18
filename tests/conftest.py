"""
Test fixtures for the MultiBet application.
This module provides reusable test components and mock data.
"""

import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

# Add project root to the Python path to allow imports from 'src' and 'config'
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_match_data():
    """Load sample match data from test_data directory."""
    test_data_path = Path(__file__).parent / "test_data" / "sample_matches.json"
    with open(test_data_path, "r") as f:
        return json.load(f)


@pytest.fixture
def mock_odds_api():
    """Mock odds API client for testing."""
    mock_api = Mock()
    mock_api.get_match_odds.return_value = {
        "home_win": 2.5,
        "draw": 3.2,
        "away_win": 2.8,
        "timestamp": "2024-01-01T12:00:00Z",
    }
    mock_api.get_closing_odds.return_value = {
        "home_win": 2.6,
        "draw": 3.1,
        "away_win": 2.7,
        "timestamp": "2024-01-01T14:00:00Z",
    }
    return mock_api


@pytest.fixture
def mock_prediction_model():
    """Mock prediction model for testing."""
    mock_model = Mock()
    mock_model.predict.return_value = {
        "home_win_prob": 0.42,
        "draw_prob": 0.28,
        "away_win_prob": 0.30,
        "confidence": 0.85,
        "model_version": "test_v1.0",
    }
    return mock_model


@pytest.fixture
def mock_database():
    """Mock database connection for testing."""
    mock_db = MagicMock()
    mock_db.store_prediction.return_value = True
    mock_db.get_historical_data.return_value = []
    mock_db.update_clv_metrics.return_value = True
    return mock_db


@pytest.fixture
def test_config():
    """Test configuration settings."""
    return {
        "DRY_RUN": True,
        "MODEL_THRESHOLD": 0.05,
        "MAX_STAKE_PERCENTAGE": 0.02,
        "MIN_ODDS": 1.1,
        "MAX_ODDS": 10.0,
        "CLV_THRESHOLD": 0.03,
        "DATABASE_URL": "sqlite:///:memory:",
        "LOG_LEVEL": "DEBUG",
    }


@pytest.fixture
def value_score_calculator():
    """Provide a value score calculator instance for testing."""

    class TestValueScoreCalculator:
        def __init__(self, config=None):
            self.config = config or {}

        def calculate(self, odds, probability):
            """Calculate value score: (probability * odds) - 1"""
            return (probability * odds) - 1

        def is_value_bet(self, value_score, threshold=0.0):
            """Determine if this is a value bet."""
            return value_score > threshold

        def calculate_kelly_stake(self, odds, probability, bankroll):
            """Calculate optimal Kelly criterion stake."""
            value_score = self.calculate(odds, probability)
            if value_score <= 0:
                return 0.0
            kelly_fraction = (probability * odds - 1) / (odds - 1)
            return max(
                0,
                min(
                    kelly_fraction * bankroll,
                    bankroll * self.config.get("MAX_STAKE_PERCENTAGE", 0.02),
                ),
            )

    return TestValueScoreCalculator


@pytest.fixture
def betting_simulation_data():
    """Provide data for betting simulation tests."""
    return {
        "initial_bankroll": 10000,
        "bet_history": [
            {"odds": 2.5, "stake": 200, "result": "win", "profit": 300},
            {"odds": 1.8, "stake": 150, "result": "loss", "profit": -150},
            {"odds": 3.2, "stake": 100, "result": "win", "profit": 220},
            {"odds": 2.1, "stake": 180, "result": "loss", "profit": -180},
        ],
        "expected_roi": 0.019,
        "expected_final_bankroll": 10190,
    }


@pytest.fixture
def clv_test_data():
    """Provide Closing Line Value test data."""
    return [
        {
            "opening_odds": 2.3,
            "closing_odds": 2.5,
            "bet_odds": 2.4,
            "expected_clv": 0.042,
        },
        {
            "opening_odds": 1.9,
            "closing_odds": 1.8,
            "bet_odds": 1.85,
            "expected_clv": -0.027,
        },
        {
            "opening_odds": 3.1,
            "closing_odds": 3.2,
            "bet_odds": 3.0,
            "expected_clv": -0.065,
        },
    ]


@pytest.fixture(scope="session")
def temp_test_directory(tmp_path_factory):
    """Create a temporary directory for test files."""
    return tmp_path_factory.mktemp("multibet_test_data")


@pytest.fixture
def mock_dry_run_logger():
    """Mock logger for dry run mode testing."""
    mock_logger = Mock()
    mock_logger.info = Mock()
    mock_logger.warning = Mock()
    mock_logger.debug = Mock()
    mock_logger.error = Mock()
    return mock_logger
    return mock_logger
