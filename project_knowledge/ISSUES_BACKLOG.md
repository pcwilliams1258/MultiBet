ISSUES_BACKLOG.md
Issue #1: Setup: Initialize Python Project Structure and Dependencies
Body: This issue covers the initial project setup as per User Story 2.1. It involves creating the directory structure, initializing Git, and defining project dependencies.
Acceptance Criteria:
[ ] A src directory exists with subdirectories: core_engine, data_pipelines, models, tests.
[ ] A root-level config directory exists.
[ ] A root-level data directory exists.
[ ] A Git repository is initialized.
[ ] A standard Python .gitignore file is present.
[ ] A requirements.txt file exists containing: flask, pandas, numpy, redis, google-cloud-bigquery, scikit-learn, catboost, tensorflow, shap, requests, pydantic, pytest, requests-mock.
Labels: setup, chore, epic-1
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #2: Architect: Define Core Engine and BaseModel Interface
Body: This issue implements the core "pluggable" architecture as per User Story 2.2. It involves creating the abstract BasePredictiveModel interface and the CoreEngine orchestrator class.
Acceptance Criteria:
[ ] src/models/base_model.py contains an abstract class BasePredictiveModel.
[ ] BasePredictiveModel has an abstract method generate_probabilities(self, data).
[ ] src/core_engine/engine.py contains a class CoreEngine.
[ ] CoreEngine constructor accepts a list of BasePredictiveModel instances.
[ ] CoreEngine has a placeholder method run_generation(self, risk_profile).
Labels: architecture, epic-1, priority-high
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #3: Feat: Implement Foundational Quantitative Functions
Body: This issue covers the implementation of core mathematical functions as per User Story 2.3. It involves creating the calculate_value_score and calculate_fractional_kelly_stake functions based on #file:.project_knowledge/technical_specification.md.
Acceptance Criteria:
[ ] src/core_engine/quant_functions.py is created.
[ ] calculate_value_score function is implemented as per spec (Section 1.2).
[ ] calculate_fractional_kelly_stake function is implemented as per spec (Section 1.4.1).
[ ] Unit tests are created for both functions, validating scenarios from the spec.
Labels: feature, epic-1, quant-logic
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #4: Feat: Implement Pydantic Schemas and Feature Store Interfaces
Body: This issue implements the data validation schemas and feature store interfaces as per User Story 1.4. It requires creating Pydantic models from #file:.project_knowledge/technical_specification.md and defining interfaces for Redis and BigQuery.
Acceptance Criteria:
[ ] src/data_pipelines/schemas.py is created.
[ ] UnifiedRacingData Pydantic class matches Table 2.1 in the spec.
[ ] UnifiedSportsData Pydantic class matches Table 2.2 in the spec.
[ ] src/data_pipelines/feature_store.py is created with OnlineFeatureStore (Redis) and OfflineFeatureStore (BigQuery) classes with placeholder methods.
[ ] config/settings.py is created and uses os.getenv() to load API keys.
Labels: feature, epic-2, data-pipeline
Assignee: @copilot (Recommended Track: Delegation)
Issue #5: Feat: Build API Clients for The Odds API and The Racing API
Body: This issue covers the creation of API clients for external data sources as per User Stories 1.1 & 1.3. Create TheOddsAPIClient and TheRacingAPIClient classes, each handling API key management, request construction, and error handling.
Acceptance Criteria:
[ ] src/data_pipelines/api_clients.py is created.
[ ] TheOddsAPIClient class exists with a get_odds method.
[ ] TheRacingAPIClient class exists with a get_racecard method.
[ ] Both methods correctly import API keys from config.settings.
[ ] Both methods use the requests library and include error handling for non-200 status codes.
[ ] src/tests/test_api_clients.py is created with unit tests using pytest and requests-mock for success and error cases for each client.
Labels: feature, epic-2, api-integration
Assignee: @copilot (Recommended Track: Delegation)
Issue #6: Feat: Engineer High-Impact Sports Features
Body: This issue covers the implementation of specific feature engineering logic for sports data as per User Story 1.2. This includes calculating 'Average Ruck Speed' for NRL and 'Forward-Half Intercepts' for AFL from raw event stream data.
Acceptance Criteria:
[ ] src/data_pipelines/feature_engineering.py is created.
[ ] A function calculate_average_ruck_speed is implemented to parse play-by-play data and calculate the average time between play-the-ball events.
[ ] A function calculate_forward_half_intercepts is implemented to parse an event stream and count intercepts in a team's forward half.
[ ] Unit tests are created for both functions with mock data to validate logic and edge cases.
Labels: feature, epic-2, feature-engineering
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #7: Feat: Engineer High-Impact Racing Features
Body: This issue covers the implementation of specific feature engineering logic for racing data as per User Story 1.3. This includes calculating 'Finishing Speed %' from sectional times and extracting 'Gear Changes' from API responses.
Acceptance Criteria:
[ ] src/data_pipelines/feature_engineering.py contains the new functions.
[ ] A function calculate_finishing_speed_percentage is implemented to calculate the ratio of final section speed to average race speed.
[ ] A parsing function is implemented to extract gear_change_type from The Racing API response and format it as a categorical feature.
[ ] Unit tests are created for both functions to validate correctness.
Labels: feature, epic-2, feature-engineering
Assignee: @copilot (Recommended Track: Delegation)
Issue #8: Refactor: Create Skeletons for All Predictive Models
Body: This issue implements the architectural skeletons for all predictive models as per User Stories 2.1-2.4. Each model class must inherit from BasePredictiveModel and implement the generate_probabilities method. The constructor for each should handle loading a pre-trained model artifact from a file path.
Acceptance Criteria:
[ ] src/models/racing_model.py contains RacingConditionalLogitModel.
[ ] src/models/sports_model.py contains SportsCatBoostClassifier.
[ ] src/models/player_props_model.py contains PlayerTriesNBModel.
[ ] src/models/player_props_lstm.py contains PlayerDisposalsLSTMModel.
[ ] All four classes inherit from BasePredictiveModel and implement the required methods and constructor signatures.
Labels: refactor, epic-3, architecture, model
Assignee: @copilot (Recommended Track: Delegation)
Issue #9: Feat: Implement Quantitative Correlation Engine
Body: This issue implements the advanced dependence model using a Student's t-Copula, as detailed in User Stories 3.1 & 3.2. This is a mathematically complex task requiring careful, step-by-step implementation and validation.
Acceptance Criteria:
[ ] A CopulaCorrelationEngine class is created in src/core_engine/correlation.py.
[ ] The class has a fit method that uses the copulas library to fit a bivariate student_t copula.
[ ] The class has a get_conditional_prob method that correctly uses the fitted copula's CDF.
[ ] The class has a price_sgm method that orchestrates the transformation and calculation to return the final joint probability.
[ ] Unit tests are created to validate each method against pre-calculated theoretical results from the spec.
Labels: feature, epic-4, priority-critical, quant-logic
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #10: Feat: Implement Dynamic Fractional Kelly Staking
Body: This issue evolves the staking logic to be risk-aware by incorporating a Model Confidence Score (MCS), as per User Story 3.3. The calculate_fractional_kelly_stake function will be refactored to accept the MCS and adjust the stake fraction accordingly.
Acceptance Criteria:
[ ] The calculate_fractional_kelly_stake function signature is updated to accept model_confidence_score.
[ ] The stake calculation is modified to use the full dynamic formula from the spec.
[ ] A unit test is added to validate that a high MCS results in a significantly larger stake than a low MCS for an otherwise identical bet, matching the test case in the spec.
Labels: feature, epic-4, quant-logic
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #11: Feat: Automate Closing Line Value (CLV) Logging
Body: This issue operationalizes the logging of CLV, the primary KPI for model performance, as per User Story 4.1. It involves logging recommended bets and then updating them with closing line odds post-event.
Acceptance Criteria:
[ ] The CoreEngine.run_generation method is modified to log finalized bet details to the offline store (BigQuery).
[ ] A new script, clv_updater.py, is created.
[ ] The script queries for recent bets, fetches closing line odds from The Odds API, calculates CLV, and updates the bet log.
Labels: feature, epic-5, mlops, monitoring
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #12: Feat: Integrate SHAP for Model Explainability
Body: This issue implements model explainability (XAI) using the SHAP library as per User Story 4.2. The generate_probabilities method of the SportsCatBoostClassifier must be modified to calculate and return local SHAP values alongside the prediction.
Acceptance Criteria:
[ ] The generate_probabilities method in SportsCatBoostClassifier is modified.
[ ] A SHAP TreeExplainer is initialized with the loaded model.
[ ] The explainer is used to calculate SHAP values for each prediction.
[ ] The method's return signature is updated to include both probabilities and SHAP values.
[ ] A unit test is updated to verify the new return signature.
Labels: feature, epic-5, mlops, xai
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #13: Chore: Scaffold the Automated Retraining Pipeline
Body: This issue creates the core Python script that will serve as the engine for the automated model retraining pipeline, as per User Story 4.3. This script will encapsulate the logic for retraining, backtesting, and deploying models.
Acceptance Criteria:
[ ] A new script, retrain_models.py, is created.
[ ] The script contains a function get_latest_training_data to pull data from BigQuery.
[ ] The script contains a function train_new_model to train a new CatBoost model.
[ ] The script contains a function backtest_model_clv to evaluate the new model on a hold-out set.
[ ] The script contains a function compare_and_deploy to promote the new model to production if its CLV is superior to a benchmark.
[ ] A main() function orchestrates the pipeline steps.
Labels: chore, epic-5, mlops, pipeline
Assignee: @copilot (Recommended Track: Delegation)
Issue #14: Chore: Automate PROMPT_LOG.md Updates with GitHub Actions
Body: This issue covers the implementation of the automated prompt log update process, as described in Section 2.3.1 of the specification. The goal is to create a GitHub Action that automatically appends a new entry template to PROMPT_LOG.md whenever a Pull Request is opened for a "Glass Box" task.
Acceptance Criteria:
[ ] A new workflow file exists at .github/workflows/prompt_log_updater.yml.
[ ] The workflow is configured to trigger only when a Pull Request is opened.
[ ] The workflow correctly identifies that the source issue was assigned to @founder-username (signaling a "Glass Box" task) and only proceeds if this condition is met.
[ ] The action successfully appends a new, pre-formatted entry to the PROMPT_LOG.md file, populating the GitHub Issue: link and Pull Request: number.
[ ] The action commits the updated PROMPT_LOG.md back to the feature branch associated with the Pull Request.
Labels: chore, automation, documentation
Assignee: @founder-username (Recommended Track: Glass Box)
Issue #15: Chore: Configure Branch Protection Rules for main
Body: This issue covers the setup of branch protection rules for the main branch to ensure code quality and stability. This prevents direct pushes and enforces a Pull Request-based workflow.
Acceptance Criteria:
[ ] The main branch is configured as a protected branch in the repository settings.
[ ] The rule "Require a pull request before merging" is enabled.
[ ] The rule "Require status checks to pass before merging" is enabled.
[ ] The rule "Do not allow bypassing the above settings" is enabled for administrators.
Labels: chore, setup, repository-settings
Assignee: @founder-username (Manual setup, not code generation)
Issue #16: Chore: Create GitHub Issue Templates
Body: This issue covers the creation of standardized templates for bug reports and feature requests to ensure all necessary information is provided when a new issue is created. This will improve the quality of issues for both "Glass Box" and "Delegation" tracks.
Acceptance Criteria:
[ ] A .github/ISSUE_TEMPLATE directory is created.
[ ] A bug_report.md template is created, including sections for "Steps to Reproduce," "Expected Behavior," and "Actual Behavior."
[ ] A feature_request.md template is created, including sections for "Problem Description," "Proposed Solution," and "Acceptance Criteria."
Labels: chore, documentation, repository-settings
Assignee: @copilot (Recommended Track: Delegation)
Issue #17: Chore: Configure CI/CD for Automated Retraining Pipeline
Body: This issue covers the setup of a GitHub Actions workflow to run the automated model retraining pipeline on a schedule, as per User Story 4.3. This will ensure models are kept up-to-date without manual intervention.
Acceptance Criteria:
[ ] A new workflow file exists at .github/workflows/retrain_pipeline.yml.
[ ] The workflow is configured to run on a schedule (e.g., weekly on Sunday at 3 AM UTC).
[ ] The workflow includes steps to check out the code, set up Python, and install dependencies from requirements.txt.
[ ] The workflow includes a step to securely authenticate with Google Cloud for BigQuery access.
[ ] The workflow executes the retrain_models.py script.
Labels: chore, automation, mlops, pipeline
Assignee: @founder-username (Recommended Track: Glass Box)
