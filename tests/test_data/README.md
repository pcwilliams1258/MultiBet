# Test Data Directory

This directory contains sample and mock data files used for testing the MultiBet application.

## Files

### sample_matches.json
Contains sample betting match data for testing value score calculations, CLV metrics, and model predictions. Each entry includes:
- Match metadata (teams, IDs)
- Opening and closing odds for home win, draw, and away win
- Model probability predictions
- Actual match results
- Calculated CLV (Closing Line Value) metrics

## Usage

Test files can load this data using the `sample_match_data` fixture from `tests/fixtures/conftest.py`:

```python
def test_my_function(sample_match_data):
    # sample_match_data contains the loaded JSON data
    first_match = sample_match_data[0]
    assert first_match['match_id'] == 'test_001'
```

## Adding New Test Data

When adding new test data files:
1. Use descriptive filenames (e.g., `edge_case_odds.json`, `historical_clv_data.csv`)
2. Include a comment in this README describing the file's purpose
3. Add corresponding fixtures in `tests/fixtures/conftest.py` if needed
4. Ensure data follows realistic formats and ranges

## Data Format Standards

- Odds should be in decimal format (e.g., 2.5, not 3/2 or +150)
- Probabilities should be between 0 and 1
- All probabilities for a match should sum to approximately 1.0
- CLV values are typically small decimals (usually between -0.5 and 0.5)
- Match IDs should follow the pattern `test_XXX` for test data