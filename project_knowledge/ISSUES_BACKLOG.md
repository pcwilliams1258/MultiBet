# Issues Backlog

---

## Issue #1: Setup - Initialize Python Project Structure and Dependencies

**Body:**  
This issue covers the initial project setup as per User Story 1.1. It involves creating the directory structure, initializing Git, and defining project dependencies.

**Acceptance Criteria:**
- [ ] A `src` directory exists with subdirectories: `core_engine`, `data_pipelines`, `models`, `tests`.
- [ ] A root-level `config` directory exists.
- [ ] A root-level `data` directory exists.
- [ ] A Git repository is initialized.
- [ ] A standard Python `.gitignore` file is present.
- [ ] A `requirements.txt` file exists containing:
  - flask
  - pandas
  - numpy
  - redis
  - google-cloud-bigquery
  - scikit-learn
  - catboost
  - tensorflow
  - shap
  - requests
  - pydantic
  - pytest
  - requests-mock

**Labels:** `setup`, `chore`, `epic-1`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #2: Architect - Define Core Engine and BaseModel Interface

**Body:**  
Implements the core "pluggable" architecture as per User Story 1.2. Involves creating the abstract `BasePredictiveModel` interface and the `CoreEngine` orchestrator class.

**Acceptance Criteria:**
- [ ] `src/models/base_model.py` contains an abstract class `BasePredictiveModel`.
- [ ] `BasePredictiveModel` has an abstract method `generate_probabilities(self, data)`.
- [ ] `src/core_engine/engine.py` contains a class `CoreEngine`.
- [ ] `CoreEngine` constructor accepts a list of `BasePredictiveModel` instances.
- [ ] `CoreEngine` has a placeholder method `run_generation(self, risk_profile)`.

**Labels:** `architecture`, `epic-1`, `priority-high`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #3: Feat - Implement Foundational Quantitative Functions

**Body:**  
Implements core mathematical functions as per User Story 1.3. Involves creating `calculate_value_score` and `calculate_fractional_kelly_stake` functions.

**Acceptance Criteria:**
- [ ] `src/core_engine/quant_functions.py` is created.
- [ ] `calculate_value_score` function is implemented as per spec (Section 1.2).
- [ ] `calculate_fractional_kelly_stake` function is implemented as per spec (Section 1.4.1).
- [ ] Unit tests are created for both functions, validating scenarios from the spec.

**Labels:** `feature`, `epic-1`, `quant-logic`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #4: Feat - Implement Pydantic Schemas and Feature Store Interfaces

**Body:**  
Implements data validation schemas and feature store interfaces as per Epic 2.

**Acceptance Criteria:**
- [ ] `src/data_pipelines/schemas.py` is created.
- [ ] `UnifiedRacingData` Pydantic class matches Table 2.1 in the spec.
- [ ] `UnifiedSportsData` Pydantic class matches Table 2.2 in the spec.
- [ ] `src/data_pipelines/feature_store.py` is created with `OnlineFeatureStore` (Redis) and `OfflineFeatureStore` (BigQuery) classes with placeholder methods.
- [ ] `config/settings.py` is created and uses `os.getenv()` to load API keys.

**Labels:** `feature`, `epic-2`, `data-pipeline`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #5: Feat - Build API Clients for The Odds API and The Racing API

**Body:**  
Creation of API clients for external data sources as per User Stories 1.1 & 1.3.

**Acceptance Criteria:**
- [ ] `src/data_pipelines/api_clients.py` is created.
- [ ] `TheOddsAPIClient` class exists with a `get_odds` method.
- [ ] `TheRacingAPIClient` class exists with a `get_racecard` method.
- [ ] Both methods correctly import API keys from `config.settings`.
- [ ] Both methods use the `requests` library and include error handling for non-200 status codes.
- [ ] `src/tests/test_api_clients.py` is created with unit tests using `pytest` and `requests-mock`.

**Labels:** `feature`, `epic-2`, `api-integration`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #6: Feat - Engineer High-Impact Sports Features

**Body:**  
Implements feature engineering logic for sports data as per User Story 1.2.

**Acceptance Criteria:**
- [ ] `src/data_pipelines/feature_engineering.py` is created.
- [ ] Function `calculate_average_ruck_speed` parses play-by-play data and calculates average time between play-the-ball events.
- [ ] Function `calculate_forward_half_intercepts` parses event stream and counts intercepts in a team's forward half.
- [ ] Unit tests for both functions with mock data.

**Labels:** `feature`, `epic-2`, `feature-engineering`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #7: Feat - Engineer High-Impact Racing Features

**Body:**  
Implements feature engineering logic for racing data as per User Story 1.3.

**Acceptance Criteria:**
- [ ] `src/data_pipelines/feature_engineering.py` contains new functions.
- [ ] Function `calculate_finishing_speed_percentage` calculates ratio of final section speed to average race speed.
- [ ] Parsing function extracts `gear_change_type` from The Racing API response as a categorical feature.
- [ ] Unit tests for both functions.

**Labels:** `feature`, `epic-2`, `feature-engineering`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #8: Refactor - Create Skeletons for All Predictive Models

**Body:**  
Implements skeletons for all predictive models as per User Stories 2.1-2.4.

**Acceptance Criteria:**
- [ ] `src/models/racing_model.py` contains `RacingConditionalLogitModel`.
- [ ] `src/models/sports_model.py` contains `SportsCatBoostClassifier`.
- [ ] `src/models/player_props_model.py` contains `PlayerTriesNBModel`.
- [ ] `src/models/player_props_lstm.py` contains `PlayerDisposalsLSTMModel`.
- [ ] All inherit from `BasePredictiveModel` and implement required methods and constructor signatures.

**Labels:** `refactor`, `epic-3`, `architecture`, `model`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #9: Feat - Implement Quantitative Correlation Engine

**Body:**  
Implements advanced dependence model using Student's t-Copula as per User Stories 3.1 & 3.2.

**Acceptance Criteria:**
- [ ] `CopulaCorrelationEngine` class is created in `src/core_engine/correlation.py`.
- [ ] Class has `fit` method using copulas library.
- [ ] `get_conditional_prob` method uses fitted copula's CDF.
- [ ] `price_sgm` method orchestrates calculation for joint probability.
- [ ] Unit tests against pre-calculated theoretical results.

**Labels:** `feature`, `epic-4`, `priority-critical`, `quant-logic`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #10: Feat - Implement Dynamic Fractional Kelly Staking

**Body:**  
Evolves staking logic to be risk-aware by incorporating Model Confidence Score (MCS) as per User Story 3.3.

**Acceptance Criteria:**
- [ ] `calculate_fractional_kelly_stake` function updated to accept `model_confidence_score`.
- [ ] Stake calculation uses full dynamic formula from spec.
- [ ] Unit test validates high MCS results in larger stake.

**Labels:** `feature`, `epic-4`, `quant-logic`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #11: Feat - Automate Closing Line Value (CLV) Logging

**Body:**  
Operationalizes CLV logging as primary KPI for model performance as per User Story 4.1.

**Acceptance Criteria:**
- [ ] `CoreEngine.run_generation` logs finalized bet details to offline store (BigQuery).
- [ ] New script `clv_updater.py` is created.
- [ ] Script queries recent bets, fetches closing line odds, calculates CLV, and updates bet log.

**Labels:** `feature`, `epic-5`, `mlops`, `monitoring`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #12: Feat - Integrate SHAP for Model Explainability

**Body:**  
Implements model explainability using SHAP as per User Story 4.2. `SportsCatBoostClassifier.generate_probabilities` must be modified.

**Acceptance Criteria:**
- [ ] Method is modified to include SHAP TreeExplainer.
- [ ] SHAP values calculated for each prediction.
- [ ] Return signature includes probabilities and SHAP values.
- [ ] Unit test verifies new return signature.

**Labels:** `feature`, `epic-5`, `mlops`, `xai`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #13: Chore - Scaffold Automated Retraining Pipeline

**Body:**  
Creates core Python script for automated retraining pipeline as per User Story 4.3.

**Acceptance Criteria:**
- [ ] New script `retrain_models.py` is created.
- [ ] `get_latest_training_data` pulls from BigQuery.
- [ ] `train_new_model` trains new CatBoost model.
- [ ] `backtest_model_clv` evaluates new model.
- [ ] `compare_and_deploy` promotes model if CLV is superior.
- [ ] `main()` orchestrates pipeline.

**Labels:** `chore`, `epic-5`, `mlops`, `pipeline`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #14: Chore - Automate PROMPT_LOG.md Updates with GitHub Actions

**Body:**  
Implements automated prompt log update via GitHub Actions as per Section 2.3.1 of the specification.

**Acceptance Criteria:**
- [ ] Workflow file at `.github/workflows/prompt_log_updater.yml`.
- [ ] Workflow triggers on Pull Request open.
- [ ] Identifies if source issue is assigned to @founder-username ("Glass Box" task).
- [ ] Action appends a new entry to `PROMPT_LOG.md` with GitHub Issue link and PR number.
- [ ] Action commits updated `PROMPT_LOG.md` to feature branch.

**Labels:** `chore`, `automation`, `documentation`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #15: Chore - Configure Branch Protection Rules for main

**Body:**  
Sets up branch protection for main branch to enforce PR workflow.

**Acceptance Criteria:**
- [ ] `main` branch is protected.
- [ ] "Require a pull request before merging" is enabled.
- [ ] "Require status checks to pass before merging" is enabled.
- [ ] "Do not allow bypassing settings" is enabled for admins.

**Labels:** `chore`, `setup`, `repository-settings`  
**Assignee:** @founder-username (Manual setup, not code generation)

---

## Issue #16: Chore - Create GitHub Issue Templates

**Body:**  
Creates standardized templates for bug reports and feature requests.

**Acceptance Criteria:**
- [ ] `.github/ISSUE_TEMPLATE` directory is created.
- [ ] `bug_report.md` template with sections: "Steps to Reproduce," "Expected Behavior," "Actual Behavior."
- [ ] `feature_request.md` template with sections: "Problem Description," "Proposed Solution," "Acceptance Criteria."

**Labels:** `chore`, `documentation`, `repository-settings`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #17: Chore - Configure CI/CD for Automated Retraining Pipeline

**Body:**  
Sets up GitHub Actions workflow to run retraining pipeline on a schedule as per User Story 4.3.

**Acceptance Criteria:**
- [ ] Workflow at `.github/workflows/retrain_pipeline.yml`.
- [ ] Runs weekly on Sunday at 3 AM UTC.
- [ ] Steps: checkout code, set up Python, install dependencies.
- [ ] Step to authenticate with Google Cloud for BigQuery.
- [ ] Executes `retrain_models.py` script.

**Labels:** `chore`, `automation`, `mlops`, `pipeline`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #18: Feat - Implement Performance Monitoring Dashboard and Alerting

**Body:**  
Implements a real-time performance monitoring dashboard and automated alerting for model degradation, as per User Story 5.4.

**Acceptance Criteria:**
- [ ] A new script `monitoring/dashboard.py` is created using a library like Dash or Streamlit.
- [ ] The dashboard visualizes key metrics: CLV, SHAP values, and prediction accuracy over time.
- [ ] Data is pulled from the BigQuery bet log.
- [ ] A separate script `monitoring/alerter.py` runs on a schedule.
- [ ] The alerter script checks if average CLV over the last 100 bets drops below a predefined threshold.
- [ ] If the threshold is breached, an alert (e.g., email, Slack) is triggered.

**Labels:** `feature`, `epic-5`, `mlops`, `monitoring`  
**Assignee:** @copilot (Recommended Track: Delegation)

---

## Issue #19: Feat - Build Robust Back-testing Framework

**Body:**  
Develops a comprehensive back-testing framework to evaluate model performance on historical data, as per User Story 5.5.

**Acceptance Criteria:**
- [ ] A new script `tools/backtester.py` is created.
- [ ] The script accepts a model version, a date range, and a betting strategy as input.
- [ ] It simulates the `CoreEngine`'s logic against historical data from the offline feature store (BigQuery).
- [ ] It outputs a detailed performance report including total profit/loss, ROI, and CLV.
- [ ] The framework can be run from the command line.

**Labels:** `feature`, `epic-5`, `mlops`, `back-testing`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---

## Issue #20: Feat - Implement A/B Testing Framework for Live Models

**Body:**  
Creates an A/B testing framework to compare the performance of two different model versions in a live production environment, as per User Story 5.6.

**Acceptance Criteria:**
- [ ] The `CoreEngine` is modified to support A/B testing logic.
- [ ] When an A/B test is active, the engine routes a percentage of requests to a "challenger" model.
- [ ] Bet placements made by the challenger model are tagged accordingly in the BigQuery log.
- [ ] A new script `tools/ab_test_analyzer.py` is created to compare the performance of the challenger vs. the champion model.
- [ ] The analysis script provides statistical significance (e.g., p-value) for the performance difference.

**Labels:** `feature`, `epic-5`, `mlops`, `ab-testing`  
**Assignee:** @founder-username (Recommended Track: Glass Box)

---
