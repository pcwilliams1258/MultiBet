# Enhanced Multi-Bet Engine Roadmap

This document outlines the strategic roadmap for developing the Unified Multi-Code Bet Generation Engine. The project is structured into five distinct epics, each containing a series of user stories that detail the functional requirements.

---

## Epic 1: Scaffolding the Application and Core Engine

**Objective:**  
Establish a robust, scalable project structure and implement foundational quantitative logic.

**User Stories:**
- **1.1:** As the founder, I need to initialize the project environment with a clean directory structure, version control, and all necessary dependencies so that development can begin on a solid foundation.
- **1.2:** As the founder, I need to generate the core engine architecture, including the abstract `BasePredictiveModel` interface and the `CoreEngine` orchestrator, to ensure a modular and pluggable system.
- **1.3:** As the founder, I need to implement the foundational quantitative logic for value score calculation and initial staking to form the core of the bet identification process.

---

## Epic 2: Building the Data Pipeline and Feature Store

**Objective:**  
Build the data infrastructure required to ingest, process, and store data from various sources.

**User Stories:**
- **2.1:** As the founder, I need to architect and deploy a two-layer Feature Store (Online/Redis, Offline/BigQuery) and define data schemas to ensure data consistency and performance.
- **2.2:** As the founder, I need to ingest market and odds data from The Odds API to provide the core pricing information for the engine.
- **2.3:** As the founder, I need to ingest granular sports statistics from Sportradar to create high-alpha sports features like "Average Ruck Speed" and "Forward-Half Intercepts".
- **2.4:** As the founder, I need to ingest granular racing statistics, including gear changes and sectional times, from The Racing API and Total Performance Data to create high-alpha racing features.

---

## Epic 3: Implementing the Predictive Model Suite

**Objective:**  
Develop the architectural skeletons for all specialized predictive models.

**User Stories:**
- **3.1 (Racing):** As the founder, I need to create the `RacingConditionalLogitModel` class skeleton to handle multi-runner racing predictions.
- **3.2 (Sports):** As the founder, I need to create the `SportsCatBoostClassifier` class skeleton for team-based sports predictions.
- **3.3 (Player Props):** As the founder, I need to create the `PlayerTriesNBModel` class skeleton for count-based player prop predictions.
- **3.4 (Time-Series):** As the founder, I need to create the `PlayerDisposalsLSTMModel` class skeleton to capture time-series dynamics in player performance.

---

## Epic 4: Engineering the Advanced Multi-Bet Engine

**Objective:**  
Implement the sophisticated quantitative logic for correlation modeling and dynamic staking.

**User Stories:**
- **4.1 & 4.2:** As the founder, I need to implement a quantitative correlation engine, using a Student's t-Copula, to accurately price Same-Game Multis by modeling the dependence between outcomes.
- **4.3:** As the founder, I need to implement dynamic Fractional Kelly staking, which adjusts the stake size based on a model's confidence score for a given bet, to optimize capital allocation.

---

## Epic 5: Establishing the Continuous Improvement Framework

**Objective:**  
Build the MLOps and validation frameworks to ensure the project's long-term viability and performance.

**User Stories:**
- **5.1:** As the founder, I need to automate the logging and calculation of Closing Line Value (CLV) for every recommended bet to have a definitive KPI for model performance.
- **5.2:** As the founder, I need to integrate model explainability (XAI) using SHAP to understand model predictions and feed a confidence score into the dynamic staking engine.
- **5.3:** As the founder, I need to scaffold an automated retraining pipeline to combat model drift and ensure the predictive models adapt to evolving market conditions.

---
