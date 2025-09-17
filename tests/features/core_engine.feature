# In tests/features/core_engine.feature

Feature: Core Engine Model Interface
  As a developer
  I want a standardized interface for predictive models
  So that the system architecture is pluggable and maintainable.

  Scenario: Ensure the BasePredictiveModel cannot be instantiated directly
    Given the BasePredictiveModel interface exists
    When I attempt to create a direct instance of it
    Then the system should raise a TypeError
