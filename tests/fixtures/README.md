# Test Fixtures Directory

This directory contains reusable test components and fixtures for the MultiBet application testing suite.

## Files

### conftest.py
Main pytest configuration file containing shared fixtures for:
- **sample_match_data**: Loads sample betting match data from test_data directory
- **mock_odds_api**: Mock API client for testing odds retrieval
- **mock_prediction_model**: Mock machine learning model for testing predictions
- **mock_database**: Mock database connection for testing persistence
- **test_config**: Test configuration with DRY_RUN enabled
- **value_score_calculator**: Test implementation of value score calculations
- **betting_simulation_data**: Data for testing betting simulation logic
- **clv_test_data**: Closing Line Value test scenarios
- **mock_dry_run_logger**: Mock logger for testing DRY_RUN mode

## Usage

These fixtures are automatically available to all tests. Use them by including the fixture name as a test parameter:

```python
def test_odds_calculation(mock_odds_api, test_config):
    # Fixtures are automatically injected
    odds = mock_odds_api.get_match_odds()
    assert odds['home_win'] == 2.5
    assert test_config.dry_run is True
```

## Adding New Fixtures

When adding new fixtures:
1. Add them to `conftest.py` or create specialized fixture files
2. Use descriptive names that clearly indicate their purpose
3. Include docstrings explaining what the fixture provides
4. Consider fixture scopes (`function`, `class`, `module`, `session`) for performance
5. Use `@pytest.fixture` decorator with appropriate parameters

## Fixture Scopes

- **function**: Default scope, creates new instance for each test
- **class**: Shared across all tests in a test class
- **module**: Shared across all tests in a test module
- **session**: Shared across entire test session

## Best Practices

- Keep fixtures focused on a single responsibility
- Use dependency injection between fixtures when needed
- Mock external dependencies to ensure fast, isolated tests
- Provide realistic test data that covers edge cases
- Use parameterized fixtures for testing multiple scenarios