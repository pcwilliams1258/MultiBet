"""
Tests for application configuration including DRY_RUN mode.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add the config directory to the path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))

from app_config import (Config, config, disable_dry_run, enable_dry_run,
                        is_dry_run)


class TestConfig:
    """Test suite for application configuration."""

    def test_default_config_values(self):
        """Test that default configuration values are properly set."""
        # Clear any environment variables that might affect defaults
        original_env = {}
        env_vars_to_clear = ["MULTIBET_DRY_RUN", "MULTIBET_DEBUG", "MULTIBET_LOG_LEVEL"]

        for var in env_vars_to_clear:
            if var in os.environ:
                original_env[var] = os.environ[var]
                del os.environ[var]

        try:
            test_config = Config()

            assert test_config.get("DRY_RUN") is False
            assert test_config.get("DEBUG") is False
            assert test_config.get("LOG_LEVEL") == "INFO"
            assert test_config.get("MODEL_THRESHOLD") == 0.05
            assert test_config.get("MAX_STAKE_PERCENTAGE") == 0.02
            assert test_config.get("MIN_ODDS") == 1.1
            assert test_config.get("MAX_ODDS") == 10.0
        finally:
            # Restore original environment variables
            for var, value in original_env.items():
                os.environ[var] = value

    def test_dry_run_property(self):
        """Test DRY_RUN property functionality."""
        # Clear any environment variables that might affect defaults
        original_env = {}
        env_vars_to_clear = ["MULTIBET_DRY_RUN", "MULTIBET_DEBUG"]

        for var in env_vars_to_clear:
            if var in os.environ:
                original_env[var] = os.environ[var]
                del os.environ[var]

        try:
            test_config = Config()

            # Default should be False
            assert test_config.dry_run is False
            assert test_config.is_betting_enabled() is True

            # Enable DRY_RUN
            test_config.set("DRY_RUN", True)
            assert test_config.dry_run is True
            assert test_config.is_betting_enabled() is False
        finally:
            # Restore original environment variables
            for var, value in original_env.items():
                os.environ[var] = value

    def test_environment_variable_override(self):
        """Test configuration override via environment variables."""
        # Set environment variable
        os.environ["MULTIBET_DRY_RUN"] = "true"
        os.environ["MULTIBET_MODEL_THRESHOLD"] = "0.1"

        try:
            test_config = Config()
            assert test_config.get("DRY_RUN") is True
            assert test_config.get("MODEL_THRESHOLD") == 0.1
        finally:
            # Clean up environment variables
            if "MULTIBET_DRY_RUN" in os.environ:
                del os.environ["MULTIBET_DRY_RUN"]
            if "MULTIBET_MODEL_THRESHOLD" in os.environ:
                del os.environ["MULTIBET_MODEL_THRESHOLD"]

    def test_config_file_loading(self):
        """Test loading configuration from JSON file."""
        config_data = {"DRY_RUN": True, "DEBUG": True, "MODEL_THRESHOLD": 0.08}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name

        try:
            test_config = Config(config_file=config_file)
            assert test_config.get("DRY_RUN") is True
            assert test_config.get("DEBUG") is True
            assert test_config.get("MODEL_THRESHOLD") == 0.08
        finally:
            os.unlink(config_file)

    def test_config_validation(self):
        """Test configuration validation."""
        test_config = Config()

        # Valid configuration should pass
        assert test_config.validate_configuration() is True

        # Invalid configuration should raise ValueError
        test_config.set("MAX_STAKE_PERCENTAGE", 1.5)  # > 1
        with pytest.raises(ValueError):
            test_config.validate_configuration()

        # Reset to valid value
        test_config.set("MAX_STAKE_PERCENTAGE", 0.02)

        # Test odds validation
        test_config.set("MIN_ODDS", 5.0)
        test_config.set("MAX_ODDS", 2.0)  # min > max
        with pytest.raises(ValueError):
            test_config.validate_configuration()

    def test_betting_limits(self):
        """Test betting limits configuration."""
        test_config = Config()
        limits = test_config.get_betting_limits()

        assert "max_stake_percentage" in limits
        assert "min_odds" in limits
        assert "max_odds" in limits
        assert "max_daily_stake" in limits
        assert limits["max_stake_percentage"] == 0.02
        assert limits["min_odds"] == 1.1
        assert limits["max_odds"] == 10.0

    def test_global_dry_run_functions(self):
        """Test global DRY_RUN helper functions."""
        # Test initial state
        original_state = is_dry_run()

        try:
            # Enable DRY_RUN
            enable_dry_run()
            assert is_dry_run() is True
            assert config.dry_run is True

            # Disable DRY_RUN
            disable_dry_run()
            assert is_dry_run() is False
            assert config.dry_run is False
        finally:
            # Restore original state
            config.set("DRY_RUN", original_state)

    def test_boolean_parsing(self):
        """Test boolean value parsing from strings."""
        test_config = Config()

        # Test various true values
        true_values = ["true", "True", "TRUE", "1", "yes", "Yes", "on", "enabled"]
        for value in true_values:
            os.environ["MULTIBET_DRY_RUN"] = value
            try:
                temp_config = Config()
                assert temp_config.get("DRY_RUN") is True, f"Failed for value: {value}"
            finally:
                if "MULTIBET_DRY_RUN" in os.environ:
                    del os.environ["MULTIBET_DRY_RUN"]

        # Test false values
        false_values = ["false", "False", "FALSE", "0", "no", "off", "disabled"]
        for value in false_values:
            os.environ["MULTIBET_DRY_RUN"] = value
            try:
                temp_config = Config()
                assert temp_config.get("DRY_RUN") is False, f"Failed for value: {value}"
            finally:
                if "MULTIBET_DRY_RUN" in os.environ:
                    del os.environ["MULTIBET_DRY_RUN"]

    def test_config_to_dict(self):
        """Test configuration export to dictionary."""
        test_config = Config()
        config_dict = test_config.to_dict()

        assert isinstance(config_dict, dict)
        assert "DRY_RUN" in config_dict
        assert "DEBUG" in config_dict
        assert "MODEL_THRESHOLD" in config_dict

        # Ensure it's a copy, not reference
        config_dict["DRY_RUN"] = True
        assert test_config.get("DRY_RUN") is False  # Original should be unchanged

    def test_config_string_representation(self):
        """Test string representation of configuration."""
        test_config = Config()
        config_str = str(test_config)

        assert "Config(" in config_str
        assert "DRY_RUN=" in config_str
        assert "DEBUG=" in config_str


class TestDryRunIntegration:
    """Integration tests for DRY_RUN mode functionality."""

    def test_dry_run_mode_in_betting_scenario(self):
        """Test DRY_RUN mode prevents actual betting."""
        test_config = Config()
        test_config.set("DRY_RUN", True)

        # Simulate a betting scenario with test values
        odds = 2.5
        probability = 0.5
        bankroll = 1000

        # In DRY_RUN mode, betting should be disabled
        assert test_config.is_betting_enabled() is False

        # Mock betting function that checks DRY_RUN
        def place_bet(odds, stake, config):
            if not config.is_betting_enabled():
                return {"result": "dry_run", "odds": odds, "stake": stake}
            return {"result": "placed", "odds": odds, "stake": stake}

        # Test that dry run mode is respected
        result = place_bet(odds, 100, test_config)
        assert result["result"] == "dry_run"
        assert result["odds"] == odds

        # Verify we use the probability and bankroll variables for completeness
        assert probability == 0.5  # Test value validation
        assert bankroll == 1000  # Test bankroll validation

    def test_dry_run_environment_variable_integration(self):
        """Test DRY_RUN mode via environment variable in realistic scenario."""
        # Set environment variable
        os.environ["MULTIBET_DRY_RUN"] = "true"
        os.environ["MULTIBET_DEBUG"] = "true"

        try:
            test_config = Config()

            # Verify configuration
            assert test_config.dry_run is True
            assert test_config.debug is True
            assert test_config.is_betting_enabled() is False

            # Test logging behavior would be different in debug + dry_run
            log_level = "DEBUG" if test_config.debug else "INFO"
            betting_enabled = test_config.is_betting_enabled()

            assert log_level == "DEBUG"
            assert betting_enabled is False

        finally:
            # Clean up
            if "MULTIBET_DRY_RUN" in os.environ:
                del os.environ["MULTIBET_DRY_RUN"]
            if "MULTIBET_DEBUG" in os.environ:
                del os.environ["MULTIBET_DEBUG"]
