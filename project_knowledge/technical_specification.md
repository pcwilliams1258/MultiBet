# Technical Specification: Unified Multi-Code Bet Generation Engine

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

## 4. Data Ingestion Pipeline

This section outlines the architecture and process for sourcing, processing, and storing data from external APIs into the two-layer Feature Store.

### 4.1 Data Sources

The system will integrate with the following external APIs to provide comprehensive sports and racing data:

| Data Source              | Coverage                    | Primary Use Case                                           |
|--------------------------|-----------------------------|------------------------------------------------------------|
| **The Odds API**         | Sports odds and markets     | Core pricing information for sports betting markets       |
| **Sportradar**           | Granular sports statistics  | High-alpha feature engineering (e.g., Average Ruck Speed) |
| **The Racing API**       | Racing odds and basic data  | Racing market pricing and basic race information          |
| **Total Performance Data** | Granular racing statistics | High-alpha racing features (gear changes, sectional times)|

---

### 4.2 ETL Process

The Extract, Transform, and Load (ETL) process follows a structured approach to ensure data quality and consistency.

#### 4.2.1 Extract

Data extraction from source APIs will be implemented using the following mechanisms:

| Method              | Description                                           | Use Cases                        |
|---------------------|-------------------------------------------------------|----------------------------------|
| **Scheduled Jobs**  | Cron-based jobs for regular data updates            | Daily odds updates, race cards  |
| **Webhooks**        | Real-time event notifications from API providers    | Live odds changes, event updates |
| **On-Demand Pulls** | Manual or triggered data retrieval                  | Historical data backfills       |

**Implementation Details:**
- API clients will be implemented in `src/data_pipelines/api_clients.py`
- Each API client will include retry logic and exponential backoff
- Rate limiting will be enforced per API provider specifications
- Data extraction will be logged for monitoring and debugging

#### 4.2.2 Transform

Raw API data will be transformed into standardized formats using the following process:

1. **Data Validation:** All incoming data will be validated against Pydantic schemas:
   - `UnifiedRacingData` for racing-related data
   - `UnifiedSportsData` for sports-related data

2. **Data Cleaning Steps:**
   - Remove duplicate records based on event_id and race_id
   - Standardize team/runner names and venue names
   - Convert timestamp formats to UTC
   - Handle missing or null values according to business rules

3. **Feature Engineering Pipeline:**
   - Calculate derived fields (e.g., implied probabilities from odds)
   - Apply data quality checks and outlier detection
   - Enrich data with historical context where applicable

4. **Schema Mapping:**
   - Map API-specific field names to unified schema fields
   - Apply data type conversions and formatting
   - Ensure all required fields are populated or provide defaults

#### 4.2.3 Load

Transformed data will be loaded into the two-layer Feature Store architecture:

**Online Feature Store (Redis):**
- **Purpose:** Low-latency access for real-time predictions
- **Data Structure:** Key-value pairs optimized for fast retrieval
- **Update Frequency:** Real-time for live odds, every 15 minutes for other data
- **Retention:** 7 days of rolling data for active events
- **Key Format:** `{sport_key}:{event_id}:{data_type}`

**Offline Feature Store (BigQuery):**
- **Purpose:** Historical data storage for analytics and model training
- **Data Structure:** Partitioned tables by date and sport type
- **Update Frequency:** Batch loads every hour
- **Retention:** 5 years of historical data
- **Schema:** Matches Pydantic schemas with additional metadata fields

**Load Strategy:**
- **Upsert Operations:** Handle both new records and updates to existing data
- **Data Versioning:** Maintain audit trail of data changes
- **Batch Processing:** Aggregate multiple records for efficient BigQuery inserts
- **Error Handling:** Failed loads are quarantined for manual review

---

### 4.3 API Integration

#### 4.3.1 Authentication and Security

| Aspect           | Implementation                                        |
|------------------|-------------------------------------------------------|
| **API Keys**     | Stored in environment variables via `config.settings` |
| **Rotation**     | Automated key rotation where supported by providers   |
| **Encryption**   | API keys encrypted at rest using cloud KMS           |

#### 4.3.2 Rate Limiting

Each API provider has specific rate limits that must be respected:

- **The Odds API:** 500 requests/hour (free tier)
- **Sportradar:** Varies by subscription level
- **Racing APIs:** Typically 1000 requests/day

**Rate Limiting Strategy:**
- Implement token bucket algorithm for each API
- Queue requests during high-traffic periods
- Prioritize real-time data over historical backfills
- Monitor usage and adjust request patterns accordingly

#### 4.3.3 Error Handling and Resilience

**HTTP Error Scenarios:**

| Error Type        | Response Strategy                                   |
|-------------------|-----------------------------------------------------|
| **4xx Errors**    | Log error, skip record, continue processing        |
| **5xx Errors**    | Retry with exponential backoff (max 3 attempts)    |
| **Timeout**       | Retry with increased timeout, fallback to cache    |
| **Rate Limit**    | Respect rate limit headers, queue request          |

**Data Quality Issues:**
- Invalid data formats are logged and quarantined
- Missing critical fields trigger alerts
- Data validation failures are tracked for pattern analysis
- Fallback to previous valid data where appropriate

**Monitoring and Alerting:**
- API availability monitoring with health checks
- Data freshness alerts for stale information
- Volume anomaly detection for unusual data patterns
- Performance metrics tracking for optimization

---

**Note:**  
- All formulas and schemas are open to extension and clarification as implementation proceeds.
- Edge cases and error handling (e.g., missing data, zero odds) should be explicitly covered in code.
