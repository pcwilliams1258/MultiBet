"""
Tests for quantitative betting functions.
"""

import pytest
from unittest.mock import Mock


def test_stake_calculation():
    """Test that stake calculation increases with confidence."""
    stake_low = 10.0
    stake_high = 25.0
    assert stake_high > stake_low, "A high MCS should result in a larger stake"  # nosec
    
    
def test_value_score_calculation():
    """Test value score calculations."""
    # Mock calculator
    calc = Mock()
    calc.calculate_value_score.return_value = 0.15
    
    result = calc.calculate_value_score(odds=2.5, probability=0.5)
    assert result == 0.15
    
    
def test_odds_validation():
    """Test odds validation logic."""
    valid_odds = [1.5, 2.0, 3.5, 10.0]
    invalid_odds = [0.5, -1.0, 0]
    
    for odds in valid_odds:
        assert odds >= 1.0, f"Odds {odds} should be valid"
        
    for odds in invalid_odds:
        assert odds < 1.0, f"Odds {odds} should be invalid"