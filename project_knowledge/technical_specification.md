Technical Specification: Unified Multi-Code Bet Generation Engine
This document provides the detailed technical specifications, formulas, and data schemas required to build the application.
1. Core Quantitative Formulas
1.2 Value Score Calculation
The Value Score is a measure of the expected value of a bet, normalized by the market price.
Formula: Value_Score = (model_probability / fair_implied_probability) - 1
model_probability: The probability of an outcome as determined by our internal predictive model.
fair_implied_probability: The bookmaker's decimal odds converted to a probability, with the overround (vig) removed.
1.4.1 Fractional Kelly Criterion
The Fractional Kelly Criterion is used for stake sizing to balance growth and risk.
Formula: Stake = Bankroll * Kelly_Fraction * ((Decimal_Odds * Probability) - 1) / (Decimal_Odds - 1)
Kelly_Fraction: A user-defined fraction (e.g., 0.5) to reduce risk.
max_stake_cap: A hard cap on any single bet as a percentage of bankroll (e.g., 4%).
3.3 Dynamic Fractional Kelly Staking
This evolves the staking formula to incorporate a Model Confidence Score (MCS).
Formula: Dynamic_Kelly_Fraction = Base_Kelly_Fraction * MCS
The Dynamic_Kelly_Fraction then replaces the static Kelly_Fraction in the staking formula.
Test Case: A bet with MCS=0.9 should have a recommended stake significantly larger than an identical bet with MCS=0.4.
2. Data Schemas (Pydantic)
Table 2.1: UnifiedRacingData Schema
Field
Data Type
Description
event_id
String
Unique identifier for the event.
race_id
String
Unique identifier for the race.
race_name
String
Name of the race.
venue
String
Racetrack venue.
race_start_time
DateTime
Official start time of the race.
runners
List
A list of runner objects.

Nested Runner Object:
Field
Data Type
Description
runner_id
String
Unique ID for the runner.
runner_name
String
Name of the horse.
barrier
Integer
Starting barrier number.
win_odds
Float
Decimal odds for winning.
gear_changes
String
Description of any gear changes.
sectional_times
List[Float]
List of sectional timing data.

Table 2.2: UnifiedSportsData Schema
Field
Data Type
Description
event_id
String
Unique identifier for the event.
sport_key
String
Key for the sport (e.g., 'aussierules_afl').
home_team
String
Name of the home team.
away_team
String
Name of the away team.
event_start_time
DateTime
Official start time of the game.
markets
List[Market]
A list of market objects.

Nested Market Object:
Field
Data Type
Description
market_key
String
Key for the market (e.g., 'h2h', 'player_tries').
outcomes
List[Outcome]
A list of outcome objects.

Nested Outcome Object:
Field
Data Type
Description
name
String
Name of the outcome (e.g., team name, player name).
price
Float
Decimal odds for the outcome.
prop_line
Float
The line for player prop bets (e.g., 0.5).

5. Advanced Logic Specifications
5.1 Advanced Dependence Modeling (Student's t-Copula)
To price Same-Game Multis, a Student's t-Copula will be used to model the tail dependence between correlated events.
Table 3: Advanced Logic Decomposition Map (Student's t-Copula)
Logical Step
Function/Method to Create
Specific Objective
1. Create Class Structure
CopulaCorrelationEngine class
Create a class to encapsulate the copula logic.
2. Fit Copula to Data
fit(self, historical_data)
Use the copulas library to fit a bivariate student_t copula to historical outcome data.
3. Calculate Conditional Probability
get_conditional_prob(self, u, v)
Use the fitted copula's conditional distribution function, `C(v
4. Price the SGM
price_sgm(self, prob_A, prob_B)
Orchestrate the process: transform probabilities, get conditional probability, and return the final joint probability `prob_A * P(B


