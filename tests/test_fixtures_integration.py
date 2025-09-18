"""
Test to validate that fixtures are working properly.
"""

from pathlib import Path


def test_sample_match_data_fixture(sample_match_data):
    """Test that sample match data fixture loads correctly."""
    assert isinstance(sample_match_data, list)
    assert len(sample_match_data) == 3

    first_match = sample_match_data[0]
    assert first_match["match_id"] == "test_001"
    assert "closing_odds" in first_match
    assert "model_predictions" in first_match
    assert "clv_metrics" in first_match


def test_test_config_fixture(test_config):
    """Test that test config fixture provides proper configuration."""
    assert test_config["DRY_RUN"] is True
    assert "MODEL_THRESHOLD" in test_config
    assert "MAX_STAKE_PERCENTAGE" in test_config


def test_value_score_calculator_fixture(value_score_calculator):
    """Test that value score calculator fixture works."""
    calculator = value_score_calculator()

    # Test value score calculation
    value_score = calculator.calculate(2.5, 0.5)
    assert value_score == 0.25  # (0.5 * 2.5) - 1

    # Test value bet determination
    assert calculator.is_value_bet(0.25) is True
    assert calculator.is_value_bet(-0.1) is False


def test_mock_odds_api_fixture(mock_odds_api):
    """Test that mock odds API fixture works."""
    odds = mock_odds_api.get_match_odds()

    assert "home_win" in odds
    assert "draw" in odds
    assert "away_win" in odds
    assert "timestamp" in odds

    closing_odds = mock_odds_api.get_closing_odds()
    assert "home_win" in closing_odds


def test_mock_prediction_model_fixture(mock_prediction_model):
    """Test that mock prediction model fixture works."""
    prediction = mock_prediction_model.predict()

    assert "home_win_prob" in prediction
    assert "draw_prob" in prediction
    assert "away_win_prob" in prediction
    assert "confidence" in prediction
    assert "model_version" in prediction

    # Probabilities should sum to approximately 1
    total_prob = (
        prediction["home_win_prob"]
        + prediction["draw_prob"]
        + prediction["away_win_prob"]
    )
    assert abs(total_prob - 1.0) < 0.01


def test_betting_simulation_data_fixture(betting_simulation_data):
    """Test that betting simulation data fixture works."""
    assert "initial_bankroll" in betting_simulation_data
    assert "bet_history" in betting_simulation_data
    assert "expected_roi" in betting_simulation_data

    bet_history = betting_simulation_data["bet_history"]
    assert isinstance(bet_history, list)
    assert len(bet_history) > 0

    first_bet = bet_history[0]
    assert "odds" in first_bet
    assert "stake" in first_bet
    assert "result" in first_bet
    assert "profit" in first_bet


def test_clv_test_data_fixture(clv_test_data):
    """Test that CLV test data fixture works."""
    assert isinstance(clv_test_data, list)
    assert len(clv_test_data) > 0

    first_clv = clv_test_data[0]
    assert "opening_odds" in first_clv
    assert "closing_odds" in first_clv
    assert "bet_odds" in first_clv
    assert "expected_clv" in first_clv


def test_fixtures_directory_structure():
    """Test that fixtures directory structure is correct."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    tests_dir = Path(__file__).parent

    assert fixtures_dir.exists()
    assert (fixtures_dir / "README.md").exists()
    # conftest.py is now in the tests root directory
    assert (tests_dir / "conftest.py").exists()


def test_test_data_directory_structure():
    """Test that test_data directory structure is correct."""
    test_data_dir = Path(__file__).parent / "test_data"

    assert test_data_dir.exists()
    assert (test_data_dir / "sample_matches.json").exists()
    assert (test_data_dir / "README.md").exists()


def test_features_directory_structure():
    """Test that features directory structure is correct."""
    features_dir = Path(__file__).parent / "features"

    assert features_dir.exists()
    assert (features_dir / "value_score.feature").exists()


def test_dry_run_logger_fixture(mock_dry_run_logger):
    """Test that mock dry run logger fixture works."""
    # Test that logger methods exist and can be called
    mock_dry_run_logger.info("Test message")
    mock_dry_run_logger.warning("Test warning")
    mock_dry_run_logger.debug("Test debug")
    mock_dry_run_logger.error("Test error")

    # Verify methods were called
    mock_dry_run_logger.info.assert_called_with("Test message")
    mock_dry_run_logger.warning.assert_called_with("Test warning")
    mock_dry_run_logger.debug.assert_called_with("Test debug")
    mock_dry_run_logger.error.assert_called_with("Test error")
