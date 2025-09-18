"""
Configuration settings for the MultiBet application.
This module provides configuration management including DRY_RUN mode.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Application configuration class with DRY_RUN mode support."""

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration with optional config file."""
        self.config_data = self._load_default_config()

        if config_file:
            self._load_config_file(config_file)

        # Override with environment variables
        self._load_environment_variables()

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            # Core application settings
            "DRY_RUN": False,
            "DEBUG": False,
            "LOG_LEVEL": "INFO",
            # Betting strategy settings
            "MODEL_THRESHOLD": 0.05,
            "MAX_STAKE_PERCENTAGE": 0.02,
            "MIN_ODDS": 1.1,
            "MAX_ODDS": 10.0,
            "CLV_THRESHOLD": 0.03,
            # Kelly criterion settings
            "KELLY_FRACTION": 0.25,  # Fractional Kelly for risk management
            "MIN_STAKE": 10.0,
            "MAX_STAKE": 1000.0,
            # Database and API settings
            "DATABASE_URL": "sqlite:///multibet.db",
            "REDIS_URL": "redis://localhost:6379/0",
            "API_TIMEOUT": 30,
            "RATE_LIMIT_REQUESTS": 100,
            "RATE_LIMIT_WINDOW": 3600,
            # Model and prediction settings
            "MODEL_UPDATE_INTERVAL": 86400,  # 24 hours in seconds
            "PREDICTION_CONFIDENCE_THRESHOLD": 0.7,
            "FEATURE_IMPORTANCE_THRESHOLD": 0.01,
            # Risk management
            "MAX_DAILY_STAKE": 500.0,
            "MAX_EXPOSURE_PER_MATCH": 200.0,
            "STOP_LOSS_THRESHOLD": -0.1,  # 10% bankroll loss
            # Monitoring and alerts
            "ALERT_WEBHOOK_URL": None,
            "MONITORING_ENABLED": True,
            "PERFORMANCE_LOG_INTERVAL": 3600,
        }

    def _load_config_file(self, config_file: str) -> None:
        """Load configuration from a JSON file."""
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        try:
            with open(config_path, "r") as f:
                file_config = json.load(f)
                self.config_data.update(file_config)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

    def _load_environment_variables(self) -> None:
        """Load configuration from environment variables."""
        # Map environment variables to config keys
        env_mapping = {
            "MULTIBET_DRY_RUN": ("DRY_RUN", self._parse_bool),
            "MULTIBET_DEBUG": ("DEBUG", self._parse_bool),
            "MULTIBET_LOG_LEVEL": ("LOG_LEVEL", str),
            "MULTIBET_MODEL_THRESHOLD": ("MODEL_THRESHOLD", float),
            "MULTIBET_MAX_STAKE_PERCENTAGE": ("MAX_STAKE_PERCENTAGE", float),
            "MULTIBET_MIN_ODDS": ("MIN_ODDS", float),
            "MULTIBET_MAX_ODDS": ("MAX_ODDS", float),
            "MULTIBET_CLV_THRESHOLD": ("CLV_THRESHOLD", float),
            "MULTIBET_DATABASE_URL": ("DATABASE_URL", str),
            "MULTIBET_REDIS_URL": ("REDIS_URL", str),
            "MULTIBET_KELLY_FRACTION": ("KELLY_FRACTION", float),
            "MULTIBET_MAX_DAILY_STAKE": ("MAX_DAILY_STAKE", float),
        }

        for env_var, (config_key, parser) in env_mapping.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    self.config_data[config_key] = parser(env_value)
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid value for {env_var}: {env_value} ({e})")

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Parse boolean value from string."""
        if isinstance(value, bool):
            return value
        return value.lower() in ("true", "1", "yes", "on", "enabled")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config_data[key] = value

    @property
    def dry_run(self) -> bool:
        """Check if application is in DRY_RUN mode."""
        return self.get("DRY_RUN", False)

    @property
    def debug(self) -> bool:
        """Check if application is in debug mode."""
        return self.get("DEBUG", False)

    def is_betting_enabled(self) -> bool:
        """Check if actual betting is enabled (not in DRY_RUN mode)."""
        return not self.dry_run

    def get_betting_limits(self) -> Dict[str, float]:
        """Get current betting limits configuration."""
        return {
            "max_stake_percentage": self.get("MAX_STAKE_PERCENTAGE"),
            "min_odds": self.get("MIN_ODDS"),
            "max_odds": self.get("MAX_ODDS"),
            "max_daily_stake": self.get("MAX_DAILY_STAKE"),
            "max_exposure_per_match": self.get("MAX_EXPOSURE_PER_MATCH"),
            "min_stake": self.get("MIN_STAKE"),
            "max_stake": self.get("MAX_STAKE"),
        }

    def validate_configuration(self) -> bool:
        """Validate configuration values for consistency."""
        errors = []

        # Validate percentage values
        if not 0 <= self.get("MAX_STAKE_PERCENTAGE", 0) <= 1:
            errors.append("MAX_STAKE_PERCENTAGE must be between 0 and 1")

        if not 0 <= self.get("KELLY_FRACTION", 0) <= 1:
            errors.append("KELLY_FRACTION must be between 0 and 1")

        # Validate odds ranges
        min_odds = self.get("MIN_ODDS", 1.0)
        max_odds = self.get("MAX_ODDS", 10.0)
        if min_odds >= max_odds:
            errors.append("MIN_ODDS must be less than MAX_ODDS")

        # Validate stake limits
        min_stake = self.get("MIN_STAKE", 0)
        max_stake = self.get("MAX_STAKE", float("inf"))
        if min_stake >= max_stake:
            errors.append("MIN_STAKE must be less than MAX_STAKE")

        if errors:
            raise ValueError("Configuration validation failed: " + "; ".join(errors))

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config_data.copy()

    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(DRY_RUN={self.dry_run}, DEBUG={self.debug})"


# Global configuration instance
config = Config()


def enable_dry_run():
    """Enable DRY_RUN mode globally."""
    config.set("DRY_RUN", True)


def disable_dry_run():
    """Disable DRY_RUN mode globally."""
    config.set("DRY_RUN", False)


def is_dry_run() -> bool:
    """Check if application is currently in DRY_RUN mode."""
    return config.dry_run
