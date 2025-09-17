Feature: Value Score Calculation
    As a sports bettor using MultiBet
    I want to calculate value scores for betting opportunities
    So that I can identify positive expected value bets

    Background:
        Given the betting system is initialized
        And we have access to odds data

    Scenario: Calculate positive value score
        Given a match with closing odds of 2.5
        And the model predicts a probability of 0.5
        When I calculate the value score
        Then the value score should be positive
        And the result should indicate a value bet

    Scenario: Calculate negative value score
        Given a match with closing odds of 1.5
        And the model predicts a probability of 0.4
        When I calculate the value score
        Then the value score should be negative
        And the result should indicate no value

    Scenario: Calculate breakeven value score
        Given a match with closing odds of 2.0
        And the model predicts a probability of 0.5
        When I calculate the value score
        Then the value score should be approximately zero
        And the result should indicate breakeven

    Scenario: Handle edge case with very low odds
        Given a match with closing odds of 1.01
        And the model predicts a probability of 0.95
        When I calculate the value score
        Then the value score should be calculated without error
        And the result should be properly formatted

    Scenario: Validate DRY RUN mode
        Given DRY RUN mode is enabled
        And a match with closing odds of 2.0
        And the model predicts a probability of 0.6
        When I calculate the value score
        Then the calculation should complete
        And no actual betting should occur
        And the result should be logged for validation