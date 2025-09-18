**About This Repository**  
This repository contains the MultiBet project, a Unified Multi-Code Bet Generation Engine. Its purpose is to ingest real-time and historical data from various sports and racing APIs, apply predictive models, and generate betting suggestions based on a quantitative evaluation framework.

The core application logic is located in the src/ directory.

### **Primary Context Source**

**The markdown files in the /docs and /documentation directories are the primary source of truth.** For immediate context on development priorities, always refer to current\_project\_state.md first. For technical details, prioritize the patterns, schemas, and logic defined in these key documents:

* **docs/technical\_specification.md**: Defines core formulas, Pydantic data schemas, and the BasePredictiveModel interface.  
* **docs/CI\_CD\_STRATEGY.md**: Outlines the automated testing, linting, and deployment workflow.  
* **docs/error\_handling\_strategy.md**: Specifies how to handle API failures with circuit breakers and retries.  
* **docs/explainability\_plan.md**: Details the integration of SHAP for model confidence scoring.

### **Tech Stack**

* **Language:** Python  
* **Web Framework:** Flask  
* **Data Analysis & Manipulation:** pandas, NumPy  
* **Machine Learning:** scikit-learn, CatBoost, TensorFlow  
* **Model Explainability:** SHAP  
* **Online Data Store:** Redis (for caching, message queues, and real-time feature storage)  
* **Offline Data Warehouse:** Google Cloud BigQuery (for analytics and model training)  
* **Data Validation:** pydantic  
* **Testing:** pytest, requests-mock

### **Development Workflow & Best Practices**

#### **1\. Local Workflow & Tooling**

This project uses a modern, automated quality assurance process. Adherence to this workflow is mandatory.

* **Linting & Formatting:** We use **Ruff** for extremely fast, all-in-one linting, formatting, and import sorting. Configuration is managed in pyproject.toml.  
* **Local Quality Checks:** **Pre-commit hooks** are configured in .pre-commit-config.yaml. Before any commit, Ruff will automatically format your code and fix safe linting errors.

**Mandatory Local Setup**

After cloning the repository, you must run these commands once:

Bash

\# Install dependencies  
pip install \-r requirements.txt

\# Install pre-commit hooks  
pre-commit install

#### **2\. Coding Conventions & Architectural Rules**

**Do's**

* **Follow Documentation:** Adhere strictly to the logic and schemas defined in the /docs and /documentation markdown files.  
* **Data Schemas:** Use the UnifiedRacingData and UnifiedSportsData Pydantic models for all data transformation and validation.  
* **Error Handling:** Implement the specified error handling patterns: circuit breakers for API calls, exponential backoff with jitter for retries, and structured JSON logging.  
* **Configuration:** Store all secrets (API keys, DB credentials) in environment variables. Use the config/ directory only for non-sensitive configuration.  
* **Staking Logic:** When implementing staking calculations, use the Dynamic Fractional Kelly Staking formula, which incorporates the SHAP-derived Model Confidence Score.  
* **Dual-Store Architecture:** When loading data, write to both Redis for low-latency online access and Google BigQuery for long-term offline storage, as detailed in data\_ingestion\_pipeline.md.  
* **Write Tests:** All new features must be accompanied by pytest unit tests.  
* **Handle Secrets:** Access all secrets via environment variables loaded from GitHub secrets (e.g., os.getenv('THE\_ODDS\_API\_KEY')).

**Don'ts**

* Do not commit directly to the main branch. All work must be done in a feature branch and submitted via a pull request.  
* Do not ignore pre-commit failures. If hooks fail, stage the auto-formatted files (git add .) and re-commit.  
* Do not commit large data files, models, or notebooks. Use .gitignore.  
* Do not write business logic directly in Flask routes. Abstract it into service classes or helper functions within src/.  
* Do not introduce new error handling patterns that conflict with error\_handling\_strategy.md.  
* Avoid using standard floats for financial or odds calculations; use a high-precision type like Decimal where appropriate.

#### **3\. Interpreting CI/CD Feedback**

You will receive feedback directly on your pull request:

* **Ruff Annotations:** Linting or formatting errors will appear as annotations directly on the "Files changed" tab, highlighting the exact line of code with the issue. Use this to make precise corrections.  
* **Pytest Summary:** If tests fail, a summary will be posted in the workflow run, clearly listing the failed test functions. Use this to identify and debug the failing logic.

### **How to Get Help**

For questions about the project, please open an issue in the repository. For information on specific libraries, refer to their official documentation:

* [pydantic](https://docs.pydantic.dev/)  
* [SHAP](https://shap.readthedocs.io/en/latest/)  
* [CatBoost](https://catboost.ai/en/docs/)

- [CatBoost](https://catboost.ai/en/docs/)
- [Google Cloud BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
