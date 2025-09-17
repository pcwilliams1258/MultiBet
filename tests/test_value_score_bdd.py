"""
BDD test implementation for value score calculation feature.
This module implements the step definitions for the value_score.feature file.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import math


# Load all scenarios from the feature file
scenarios('features/value_score.feature')


class ValueScoreCalculator:
    """Mock value score calculator for BDD testing."""
    
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.odds = None
        self.probability = None
        self.value_score = None
        self.last_calculation_result = None
    
    def set_odds(self, odds):
        """Set the closing odds for calculation."""
        self.odds = float(odds)
    
    def set_probability(self, probability):
        """Set the model predicted probability."""
        self.probability = float(probability)
    
    def calculate_value_score(self):
        """Calculate the value score based on odds and probability."""
        if self.odds is None or self.probability is None:
            raise ValueError("Odds and probability must be set before calculation")
        
        # Value score formula: (probability * odds) - 1
        # Positive value indicates a value bet
        self.value_score = (self.probability * self.odds) - 1
        
        self.last_calculation_result = {
            'value_score': self.value_score,
            'is_value_bet': self.value_score > 0,
            'dry_run': self.dry_run,
            'calculation_completed': True
        }
        
        return self.value_score


# Test context to hold state between steps
@pytest.fixture
def betting_context():
    """Fixture to provide test context for BDD scenarios."""
    return {
        'calculator': None,
        'dry_run_mode': False,
        'system_initialized': False
    }


# Background steps
@given('the betting system is initialized')
def betting_system_initialized(betting_context):
    """Initialize the betting system for testing."""
    betting_context['system_initialized'] = True
    betting_context['calculator'] = ValueScoreCalculator()


@given('we have access to odds data')
def odds_data_available(betting_context):
    """Ensure odds data is available for calculations."""
    # In a real implementation, this would verify connection to odds API
    assert betting_context['system_initialized']


# Scenario-specific given steps
@given(parsers.parse('a match with closing odds of {odds:g}'))
def match_with_odds(betting_context, odds):
    """Set the closing odds for the match."""
    betting_context['calculator'].set_odds(odds)


@given(parsers.parse('the model predicts a probability of {probability:g}'))
def model_prediction(betting_context, probability):
    """Set the model's predicted probability."""
    betting_context['calculator'].set_probability(probability)


@given('DRY RUN mode is enabled')
def dry_run_mode_enabled(betting_context):
    """Enable DRY RUN mode for safe testing."""
    betting_context['dry_run_mode'] = True
    betting_context['calculator'] = ValueScoreCalculator(dry_run=True)


# When steps
@when('I calculate the value score')
def calculate_value_score(betting_context):
    """Perform the value score calculation."""
    betting_context['calculator'].calculate_value_score()


# Then steps
@then('the value score should be positive')
def value_score_positive(betting_context):
    """Verify the value score is positive."""
    assert betting_context['calculator'].value_score > 0


@then('the value score should be negative')
def value_score_negative(betting_context):
    """Verify the value score is negative."""
    assert betting_context['calculator'].value_score < 0


@then('the value score should be approximately zero')
def value_score_zero(betting_context):
    """Verify the value score is approximately zero."""
    assert abs(betting_context['calculator'].value_score) < 0.001


@then('the result should indicate a value bet')
def result_indicates_value_bet(betting_context):
    """Verify the result indicates a value betting opportunity."""
    result = betting_context['calculator'].last_calculation_result
    assert result['is_value_bet'] is True


@then('the result should indicate no value')
def result_indicates_no_value(betting_context):
    """Verify the result indicates no value betting opportunity."""
    result = betting_context['calculator'].last_calculation_result
    assert result['is_value_bet'] is False


@then('the result should indicate breakeven')
def result_indicates_breakeven(betting_context):
    """Verify the result indicates a breakeven scenario."""
    result = betting_context['calculator'].last_calculation_result
    # Breakeven means value score near zero and no value bet
    assert abs(betting_context['calculator'].value_score) < 0.001
    assert result['is_value_bet'] is False


@then('the value score should be calculated without error')
def calculation_completed_without_error(betting_context):
    """Verify the calculation completed successfully."""
    result = betting_context['calculator'].last_calculation_result
    assert result['calculation_completed'] is True
    assert betting_context['calculator'].value_score is not None


@then('the result should be properly formatted')
def result_properly_formatted(betting_context):
    """Verify the result is properly formatted."""
    result = betting_context['calculator'].last_calculation_result
    assert isinstance(result['value_score'], float)
    assert isinstance(result['is_value_bet'], bool)


@then('the calculation should complete')
def calculation_should_complete(betting_context):
    """Verify the calculation completes successfully."""
    result = betting_context['calculator'].last_calculation_result
    assert result['calculation_completed'] is True


@then('no actual betting should occur')
def no_actual_betting(betting_context):
    """Verify no actual betting occurs in DRY RUN mode."""
    result = betting_context['calculator'].last_calculation_result
    assert result['dry_run'] is True


@then('the result should be logged for validation')
def result_logged_for_validation(betting_context):
    """Verify the result is logged for validation purposes."""
    result = betting_context['calculator'].last_calculation_result
    # In a real implementation, this would verify logging
    assert result is not None
    assert 'value_score' in result