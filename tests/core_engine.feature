Feature: Core Engine Model Interface
  As a developer
  I want a standardized abstract interface for all predictive models
  So that the system's architecture is pluggable, consistent, and maintainable.

Background:
  Given the core engine's `BasePredictiveModel` interface exists

Scenario: Ensure the BasePredictiveModel cannot be instantiated directly
  When I attempt to create a direct instance of the `BasePredictiveModel`
  Then the system should raise a TypeError
  And confirm that the architectural contract is being enforced.
