# Unified Multi-Bet Research Plan

This document outlines the research and rationale behind the key technical and architectural decisions for the project.

---

## 1. Core Architectural Principles

### Pluggable Model Architecture
- **Design:** The system enforces a strict separation between the `CoreEngine` and the predictive models, achieved via a `BasePredictiveModel` abstract base class.
- **Rationale:** This allows independent development, testing, and updating of models without affecting the core business logic. New models (e.g., for a new sport) can be "plugged in" as long as they adhere to the contract.

### Two-Layer Feature Store
- **Online Store (Redis):** Optimized for low-latency reads of feature vectors needed for real-time predictions.
- **Offline Store (Google BigQuery):** Optimized for large-scale storage and complex queries on historical data, useful for model training, backtesting, and analytics.
- **Rationale:** Separation addresses different operational needs. A single database would compromise either speed for live predictions or efficiency for analytics.

---

## 2. Predictive Model Selection

The choice of model is tailored to the statistical nature of the betting market being predicted:

- **Racing (Multi-Runner Events):**  
  *Conditional Logit Model*  
  _Rationale:_ Simple binary (win/loss) models are statistically inappropriate for races with multiple potential winners. A Conditional Logit model correctly frames the problem as a choice model.

- **Team Sports (Head-to-Head):**  
  *CatBoost Classifier*  
  _Rationale:_ Sports data is rich with categorical features (e.g., venue, day of the week, team names). CatBoost is a gradient boosting algorithm designed to handle categorical features natively.

- **Player Props (Count-Based):**  
  *Negative Binomial Regression*  
  _Rationale:_ Predicting discrete counts (e.g., number of tries, goals) is not a classification problem. Poisson or Negative Binomial regression models are designed to predict count outcomes. The Negative Binomial model is preferred for over-dispersed count data.

- **Player Props (Time-Series):**  
  *LSTM Network*  
  _Rationale:_ To capture a player's form or momentum, simple rolling averages are insufficient. LSTM (Long Short-Term Memory) networks are designed to learn temporal dependencies in sequential data.

---

## 3. Advanced Quantitative Logic

- **Correlation Modeling (Student's t-Copula):**  
  _Rationale:_ Simply multiplying probabilities of correlated events for Same-Game Multi bets leads to mispricing. A copula function separates the modeling of marginal probabilities from their dependence structure.

- **Explainability (SHAP):**  
  _Rationale:_ "Black box" models are risky. SHAP (SHapley Additive exPlanations) uses game theory to explain model output, providing transparency for stakeholders and aiding model validation.

---
