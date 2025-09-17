# Technical Specification: Unified Multi-Code Bet Generation Engine

**Last Reviewed: 2025-09-16**

This document provides the detailed technical specifications, formulas, and data schemas required to build the application.

---

## 1. Core Quantitative Formulas

### 1.1 Value Score Calculation

The Value Score is a measure of the expected value of a bet, normalized by the market price.

**Formula:**  
`Value_Score = (model_probability / fair_implied_probability) - 1`

- **model_probability:** The probability of an outcome as determined by our internal predictive model.
- **fair_implied_probability:** The bookmaker's decimal odds converted to a probability, with the overround (vig) removed.

---

### 1.2 Fractional Kelly Criterion

The Fractional Kelly Criterion is used for stake sizing to balance growth and risk.

**Formula:**  
`Stake = Bankroll * Kelly_Fraction * ((Decimal_Odds * Probability) - 1) / (Decimal_Odds - 1)`

- **Kelly_Fraction:** A user-defined fraction (e.g., 0.5) to reduce risk.
- **max_stake_cap:** A hard cap on any single bet as a percentage of bankroll (e.g., 4%).

---

### 1.3 Dynamic Fractional Kelly Staking

This evolves the staking formula to incorporate a Model Confidence Score (MCS).

**Formula:**  
`Dynamic_Kelly_Fraction = Base_Kelly_Fraction * MCS`

The Dynamic_Kelly_Fraction then replaces the static Kelly_Fraction in the staking formula.

**Test Case:**  
A bet with MCS=0.9 should have a recommended stake significantly larger than an identical bet with MCS=0.4.

---

## 2. Data Schemas (Pydantic)

### 2.1 UnifiedRacingData Schema

| Field            | Data Type   | Description                       |
|------------------|------------|-----------------------------------|
| event_id         | String      | Unique identifier for the event.  |
| race_id          | String      | Unique identifier for the race.   |
| race_name        | String      | Name of the race.                 |
| venue            | String      | Racetrack venue.                  |
| race_start_time  | DateTime    | Official start time of the race.  |
| runners          | List        | A list of runner objects.         |

#### Nested Runner Object

| Field           | Data Type      | Description                        |
|-----------------|---------------|------------------------------------|
| runner_id       | String         | Unique ID for the runner.          |
| runner_name     | String         | Name of the horse.                 |
| barrier         | Integer        | Starting barrier number.           |
| win_odds        | Float          | Decimal odds for winning.          |
| gear_changes    | String         | Description of any gear changes.   |
| sectional_times | List[Float]    | List of sectional timing data.     |

---

### 2.2 UnifiedSportsData Schema

| Field            | Data Type   | Description                                    |
|------------------|------------|------------------------------------------------|
| event_id         | String      | Unique identifier for the event.               |
| sport_key        | String      | Key for the sport (e.g., 'aussierules_afl').  |
| home_team        | String      | Name of the home team.                         |
| away_team        | String      | Name of the away team.                         |
| event_start_time | DateTime    | Official start time of the game.               |
| markets          | List[Market]| A list of market objects.                      |

#### Nested Market Object

| Field      | Data Type      | Description                                |
|------------|---------------|--------------------------------------------|
| market_key | String         | Key for the market (e.g., 'h2h', 'player_tries'). |
| outcomes   | List[Outcome]  | A list of outcome objects.                 |

#### Nested Outcome Object

| Field     | Data Type | Description                                      |
|-----------|-----------|--------------------------------------------------|
| name      | String    | Name of the outcome (e.g., team name, player name). |
| price     | Float     | Decimal odds for the outcome.                    |
| prop_line | Float     | The line for player prop bets (e.g., 0.5).       |

---

## 3. Advanced Logic Specifications

### 3.1 Advanced Dependence Modeling (Student's t-Copula)

To price Same-Game Multis (SGMs), a Student's t-Copula will be used to model the tail dependence between correlated events.

#### Advanced Logic Decomposition Map (Student's t-Copula)

| Logical Step            | Function/Method              | Specific Objective                                                                                      |
|-------------------------|-----------------------------|--------------------------------------------------------------------------------------------------------|
| 1. Create Class Structure | `CopulaCorrelationEngine` class | Create a class to encapsulate the copula logic.                                                        |
| 2. Fit Copula to Data     | `fit(self, historical_data)`   | Use the copulas library to fit a bivariate student_t copula to historical outcome data.                |
| 3. Calculate Conditional Probability | `get_conditional_prob(self, u, v)` | Use the fitted copula's conditional distribution function, e.g., `C(v|u)`                              |
| 4. Price the SGM          | `price_sgm(self, prob_A, prob_B)` | Orchestrate the process: transform probabilities, get conditional probability, and return joint probability `prob_A * P(B|A)` |

---

**Note:**  
- All formulas and schemas are open to extension and clarification as implementation proceeds.
- Edge cases and error handling (e.g., missing data, zero odds) should be explicitly covered in code.

---

## 4. Core Engine and Model Interface

### 4.1 BasePredictiveModel Abstract Class

To ensure a pluggable architecture, all predictive models MUST inherit from the BasePredictiveModel abstract base class. This class defines the standard interface for interaction with the Core Engine.

**File Location:** src/core_engine/base_model.py

**Definition:**
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePredictiveModel(ABC):
    """
    Abstract base class for all predictive models.
    Enforces a standard contract for model interaction.
    """

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a prediction based on input features.

        Args:
            features: A dictionary of feature names and their values.

        Returns:
            A dictionary containing the prediction, typically including
            outcome probabilities and a model confidence score.
        """
        pass

    @abstractmethod
    def explain(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides an explanation for a prediction using SHAP or a similar method.

        Args:
            features: A dictionary of feature names and their values.

        Returns:
            A dictionary detailing the contribution of each feature to the
            final prediction.
        """
        pass
```

### 4.2 Standardized Prediction Object Schema

The predict method of any BasePredictiveModel implementation MUST return a dictionary that conforms to the following structure to ensure consistent processing by the Core Engine.

**Key Fields:**

| Field | Data Type | Description | Required |
|---|---|---|---|
| prediction_probability | Float | The model's calculated probability for the primary outcome. | Yes |
| value_score | Float | The calculated value score based on the prediction and odds. | Yes |
| confidence_score | Float | The model's confidence in the prediction (e.g., derived from SHAP values), ranging from 0.0 to 1.0. | Yes |
| explanation | Dict | A dictionary containing the top positive and negative features influencing the prediction. | Yes |
| model_version | String | The version identifier of the model that generated the prediction. | Yes |
| raw_prediction | Any | The raw output from the underlying model library (e.g., probabilities for all outcomes). | No |
