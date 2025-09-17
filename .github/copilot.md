## About This Repository

This repository contains the `MultiBet` project, a Unified Multi-Code Bet Generation Engine. Its purpose is to ingest real-time and historical data from various sports and racing APIs, apply predictive models, and generate betting suggestions based on a quantitative evaluation framework.

The core application logic is located in the `src/` directory.

## Project Documentation (Primary Context Source)

**The markdown files in the `/docs` and `/documentation` directories are the primary source of truth for this repository.** They contain detailed specifications that MUST be followed. When generating code, prioritize the patterns and schemas defined in these documents.

### Core Specifications (`/docs`)
- **`technical_specification.md`**: Defines the core quantitative formulas (`Value_Score`, `Dynamic Fractional Kelly Staking`), Pydantic data schemas (`UnifiedRacingData`, `UnifiedSportsData`), and advanced betting strategies.
- **`data_ingestion_pipeline.md`**: Details the ETL pipeline, the dual-store architecture (Redis for online, BigQuery for offline), API polling/rate-limiting classes, and data transformation/normalization logic.
- **`error_handling_strategy.md`**: Specifies the comprehensive strategy for handling API failures (timeouts, 5xx errors) using circuit breakers, exponential backoff with jitter, structured JSON logging, and dead-letter queues.
- **`explainability_plan.md`**: Outlines the integration of SHAP for model explainability. It defines how a `Model Confidence Score` (MCS) is derived from SHAP values and is a key input for the `Dynamic Fractional Kelly Staking` formula.

### Supplementary Documentation (`/documentation`)
- **`current_project_state.md`**: Provides a high-level overview of the project's current status, active development priorities, and known blockers. **Refer to this file first for immediate context.**
- **`technical_debt_log.md`**: A log of identified technical debt, including areas needing refactoring, performance bottlenecks, and temporary workarounds. Consult this before implementing new features to avoid exacerbating existing issues.

## Tech Stack

- **Language:** Python
- **Web Framework:** Flask
- **Data Analysis & Manipulation:** pandas, NumPy
- **Machine Learning:** scikit-learn, CatBoost, TensorFlow
- **Model Explainability:** SHAP
- **Online Data Store:** Redis (for caching, message queues, and real-time feature storage)
- **Offline Data Warehouse:** Google Cloud BigQuery (for analytics and model training)
- **Data Validation:** pydantic
- **Testing:** pytest, requests-mock

## Coding Conventions & Best Practices

### Do's
- **Follow Documentation:** Adhere strictly to the logic and schemas defined in the `/docs` and `/documentation` markdown files.
- **Data Schemas:** Use the `UnifiedRacingData` and `UnifiedSportsData` Pydantic models for all data transformation and validation.
- **Error Handling:** Implement the specified error handling patterns: circuit breakers for API calls, exponential backoff with jitter for retries, and structured JSON logging.
- **Configuration:** Store all secrets (API keys, DB credentials) in environment variables. Use the `config/` directory only for non-sensitive configuration.
- **Staking Logic:** When implementing staking calculations, use the `Dynamic Fractional Kelly Staking` formula, which incorporates the SHAP-derived `Model Confidence Score`.
- **Dual-Store Architecture:** When loading data, write to both Redis for low-latency online access and Google BigQuery for long-term offline storage, as detailed in `data_ingestion_pipeline.md`.

### Don'ts
- Do not commit large data files, models, or notebooks. Use `.gitignore`.
- Do not write business logic directly in Flask routes. Abstract it into service classes or helper functions within `src/`.
- Do not introduce new error handling patterns that conflict with `error_handling_strategy.md`.
- Avoid using standard floats for financial or odds calculations; use a high-precision type like `Decimal` where appropriate.

## How to Get Help

For questions about the project, please open an issue in the repository. For information on specific libraries, refer to their official documentation:
- [pydantic](https://docs.pydantic.dev/)
- [SHAP](https://shap.readthedocs.io/en/latest/)
- [CatBoost](https://catboost.ai/en/docs/)
- [Google Cloud BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)