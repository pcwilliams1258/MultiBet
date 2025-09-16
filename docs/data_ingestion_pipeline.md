# Data Ingestion Pipeline

**Last Reviewed: 2025-09-16**

This document outlines the comprehensive data ingestion pipeline for the Unified Multi-Code Bet Generation Engine, detailing how data will be sourced, ingested, and transformed to fit the defined schemas.

---

## 1. Data Sources

### 1.1 Primary Data Sources

#### Racing Data APIs
- **The Odds API (Racing):** Real-time horse and greyhound racing odds and market data
- **Racing.com API:** Historical race results, runner statistics, and form data
- **Punters.com.au API:** Sectional times, barrier positions, and gear changes
- **TAB API:** Official odds and market movements for Australian racing

#### Sports Data APIs
- **The Odds API (Sports):** Comprehensive sports betting markets including AFL, NRL, NBA, NFL
- **ESPN API:** Live scores, team statistics, and player performance data
- **SportRadar API:** Real-time game data, player props, and historical statistics
- **Official League APIs:** Direct feeds from AFL, NRL for authoritative data

### 1.2 Secondary Data Sources

#### Supplementary Data
- **Weather APIs:** Track conditions and weather impact analysis
- **Venue APIs:** Stadium information, surface conditions, and capacity data
- **Social Media APIs:** Sentiment analysis and public betting trends
- **Financial APIs:** Market volatility indicators and economic factors

#### Reference Data
- **Team/Runner Databases:** Static information about teams, horses, and players
- **Historical Archives:** Long-term performance data and statistical baselines
- **Configuration Data:** Market mappings, sport keys, and venue identifiers

---

## 2. Ingestion Mechanisms

### 2.1 Real-Time Data Ingestion

#### REST API Polling
```python
class ApiPoller:
    def __init__(self, endpoint: str, poll_interval: int = 30):
        self.endpoint = endpoint
        self.poll_interval = poll_interval
        
    async def poll_continuous(self):
        """Continuously poll API for live data updates"""
        while True:
            try:
                data = await self.fetch_data()
                await self.process_and_store(data)
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Polling error: {e}")
                await asyncio.sleep(self.poll_interval * 2)  # Backoff
```

#### WebSocket Streams
- **Live Odds Feeds:** Real-time price movements and market updates
- **In-Play Events:** Live scoring and game state changes
- **Market Suspension:** Immediate notifications of suspended markets

#### Event-Driven Ingestion
- **Scheduled Jobs:** Cron-based tasks for daily/weekly data collection
- **Trigger-Based:** Market opening/closing events and race start times
- **Message Queues:** Redis-based task distribution for parallel processing

### 2.2 Batch Data Processing

#### Historical Data Imports
- **Daily Batch Jobs:** End-of-day results and settlement data
- **Weekly Aggregations:** Performance statistics and trend analysis
- **Monthly Archives:** Long-term historical data for model training

#### Data Backfill Operations
- **Initial Setup:** Bulk import of historical data for new sports/venues
- **Gap Recovery:** Automatic detection and filling of missing data periods
- **Data Reconciliation:** Cross-validation between multiple source APIs

---

## 3. Transformation (ETL) Pipeline

### 3.1 Extract Phase

#### API Response Handling
```python
class DataExtractor:
    def extract_racing_data(self, api_response: dict) -> RawRacingData:
        """Extract racing data from API response"""
        return RawRacingData(
            source_api=self.api_name,
            raw_data=api_response,
            extracted_at=datetime.utcnow(),
            event_timestamp=self._parse_event_time(api_response)
        )
    
    def extract_sports_data(self, api_response: dict) -> RawSportsData:
        """Extract sports data from API response"""
        return RawSportsData(
            source_api=self.api_name,
            raw_data=api_response,
            extracted_at=datetime.utcnow(),
            event_timestamp=self._parse_event_time(api_response)
        )
```

#### Data Quality Checks
- **Completeness Validation:** Ensure all required fields are present
- **Format Verification:** Validate data types and value ranges
- **Freshness Checks:** Verify data timestamps and relevance
- **Duplicate Detection:** Identify and handle duplicate records

### 3.2 Transform Phase

#### Data Normalization
```python
class DataTransformer:
    def normalize_racing_data(self, raw_data: RawRacingData) -> UnifiedRacingData:
        """Transform raw racing data to unified schema"""
        runners = []
        for runner_data in raw_data.raw_data.get('runners', []):
            runners.append(Runner(
                runner_id=self._generate_runner_id(runner_data),
                runner_name=self._clean_name(runner_data.get('name')),
                barrier=int(runner_data.get('barrier', 0)),
                win_odds=float(runner_data.get('odds', 0.0)),
                gear_changes=self._parse_gear_changes(runner_data),
                sectional_times=self._parse_sectionals(runner_data)
            ))
        
        return UnifiedRacingData(
            event_id=self._generate_event_id(raw_data),
            race_id=self._generate_race_id(raw_data),
            race_name=self._clean_race_name(raw_data.raw_data.get('race_name')),
            venue=self._standardize_venue(raw_data.raw_data.get('venue')),
            race_start_time=self._parse_datetime(raw_data.raw_data.get('start_time')),
            runners=runners
        )
```

#### Odds Standardization
- **Decimal Conversion:** Convert all odds formats to decimal
- **Market Mapping:** Standardize market keys across different APIs
- **Price Validation:** Remove invalid or suspicious odds values
- **Overround Calculation:** Compute and store market margins

#### Data Enrichment
- **Historical Context:** Add rolling averages and form indicators
- **Derived Metrics:** Calculate implied probabilities and value scores
- **Contextual Data:** Merge weather, venue, and other supplementary data
- **Feature Engineering:** Create model-ready feature vectors

### 3.3 Load Phase

#### Dual-Store Architecture
```python
class DataLoader:
    def __init__(self, redis_client: Redis, bigquery_client: bigquery.Client):
        self.redis = redis_client
        self.bigquery = bigquery_client
    
    async def load_to_stores(self, unified_data: UnifiedData):
        """Load data to both online and offline stores"""
        # Online store for real-time predictions
        await self._load_to_redis(unified_data)
        
        # Offline store for analytics and model training
        await self._load_to_bigquery(unified_data)
    
    async def _load_to_redis(self, data: UnifiedData):
        """Load to Redis for low-latency access"""
        key = f"live_data:{data.event_id}"
        await self.redis.set(key, data.json(), ex=3600)  # 1 hour TTL
    
    async def _load_to_bigquery(self, data: UnifiedData):
        """Load to BigQuery for long-term storage"""
        table_ref = self.bigquery.dataset('multibet').table('unified_data')
        job = self.bigquery.load_table_from_json([data.dict()], table_ref)
        job.result()  # Wait for completion
```

---

## 4. Schema Enforcement

### 4.1 Pydantic Validation

#### Runtime Validation
```python
from pydantic import BaseModel, validator, ValidationError

class UnifiedRacingData(BaseModel):
    event_id: str
    race_id: str
    race_name: str
    venue: str
    race_start_time: datetime
    runners: List[Runner]
    
    @validator('event_id')
    def validate_event_id(cls, v):
        if not re.match(r'^[A-Z]{2,3}_\d{8}_\d+$', v):
            raise ValueError('Invalid event_id format')
        return v
    
    @validator('runners')
    def validate_runners(cls, v):
        if len(v) < 2:
            raise ValueError('Race must have at least 2 runners')
        return v
    
    @validator('race_start_time')
    def validate_future_time(cls, v):
        if v < datetime.utcnow() - timedelta(hours=1):
            raise ValueError('Race start time cannot be more than 1 hour in the past')
        return v
```

#### Schema Evolution Management
- **Version Control:** Track schema changes with semantic versioning
- **Backward Compatibility:** Maintain support for older data formats
- **Migration Scripts:** Automated schema upgrade procedures
- **Validation Reporting:** Detailed error logs for failed validations

### 4.2 Data Integrity Measures

#### Constraint Enforcement
- **Primary Keys:** Ensure unique identification across all records
- **Foreign Keys:** Maintain referential integrity between related data
- **Check Constraints:** Validate business rules and data ranges
- **Not Null Constraints:** Enforce required field completeness

#### Data Quality Monitoring
```python
class DataQualityMonitor:
    def validate_data_quality(self, data_batch: List[UnifiedData]) -> QualityReport:
        """Comprehensive data quality assessment"""
        report = QualityReport()
        
        for record in data_batch:
            # Completeness check
            report.completeness_score += self._check_completeness(record)
            
            # Accuracy validation
            report.accuracy_score += self._validate_accuracy(record)
            
            # Consistency verification
            report.consistency_score += self._check_consistency(record)
            
            # Timeliness assessment
            report.timeliness_score += self._assess_timeliness(record)
        
        return report.calculate_overall_score()
```

---

## 5. API Integration Specifications

### 5.1 Authentication Management

#### API Key Rotation
```python
class ApiKeyManager:
    def __init__(self):
        self.keys = {
            'the_odds_api': os.getenv('THE_ODDS_API_KEY'),
            'racing_api': os.getenv('RACING_API_KEY'),
            'sportradar': os.getenv('SPORTRADAR_API_KEY')
        }
        self.rotation_schedule = {}
    
    def get_active_key(self, api_name: str) -> str:
        """Get currently active API key with rotation logic"""
        if self._should_rotate_key(api_name):
            self._rotate_key(api_name)
        return self.keys[api_name]
```

#### OAuth 2.0 Implementation
- **Token Management:** Automatic refresh of expired tokens
- **Scope Handling:** Request minimal required permissions
- **Secure Storage:** Encrypted token storage in environment variables
- **Fallback Mechanisms:** Alternative authentication methods

### 5.2 Rate Limiting Strategy

#### Adaptive Rate Limiting
```python
class RateLimiter:
    def __init__(self, base_rate: int = 100, burst_capacity: int = 10):
        self.base_rate = base_rate  # requests per minute
        self.burst_capacity = burst_capacity
        self.request_history = deque()
        self.backoff_multiplier = 1.0
    
    async def acquire(self, api_name: str) -> bool:
        """Acquire permission to make API request"""
        current_time = time.time()
        
        # Remove old requests outside the window
        while (self.request_history and 
               current_time - self.request_history[0] > 60):
            self.request_history.popleft()
        
        # Check if under rate limit
        effective_rate = self.base_rate / self.backoff_multiplier
        if len(self.request_history) < effective_rate:
            self.request_history.append(current_time)
            return True
        
        return False  # Rate limit exceeded
    
    def handle_rate_limit_response(self, response_headers: dict):
        """Adjust rate limiting based on API response"""
        if 'X-RateLimit-Remaining' in response_headers:
            remaining = int(response_headers['X-RateLimit-Remaining'])
            if remaining < 10:  # Approaching limit
                self.backoff_multiplier *= 1.5
```

#### Circuit Breaker Pattern
- **Failure Detection:** Monitor API response patterns
- **Automatic Recovery:** Gradual restoration of API calls
- **Fallback Data:** Use cached or alternative data sources
- **Alert System:** Notifications for prolonged API failures

### 5.3 Endpoint Configuration

#### API Endpoint Registry
```python
class EndpointRegistry:
    ENDPOINTS = {
        'the_odds_api': {
            'base_url': 'https://api.the-odds-api.com/v4',
            'sports': '/sports/{sport}/odds',
            'racing': '/sports/horse_racing_au/odds',
            'live': '/sports/{sport}/events/{event_id}/odds'
        },
        'racing_api': {
            'base_url': 'https://api.racing.com',
            'results': '/racing/results/{date}',
            'form': '/horse/{horse_id}/form',
            'sectionals': '/race/{race_id}/sectionals'
        }
    }
    
    def get_endpoint(self, api_name: str, endpoint_type: str, **kwargs) -> str:
        """Build complete endpoint URL with parameters"""
        config = self.ENDPOINTS[api_name]
        endpoint = config[endpoint_type].format(**kwargs)
        return f"{config['base_url']}{endpoint}"
```

#### Request/Response Handling
- **Retry Logic:** Exponential backoff for failed requests
- **Timeout Management:** Configurable timeouts per endpoint
- **Response Caching:** Intelligent caching based on data volatility
- **Error Classification:** Distinguish between retryable and permanent errors

---

## 6. Monitoring and Observability

### 6.1 Pipeline Monitoring

#### Health Check Endpoints
```python
class PipelineHealthCheck:
    def check_pipeline_health(self) -> HealthStatus:
        """Comprehensive pipeline health assessment"""
        return HealthStatus(
            api_connectivity=self._check_api_connectivity(),
            data_freshness=self._check_data_freshness(),
            processing_lag=self._measure_processing_lag(),
            error_rate=self._calculate_error_rate(),
            storage_health=self._check_storage_health()
        )
```

#### Metrics and Alerting
- **Data Volume Metrics:** Track ingestion rates and storage growth
- **Latency Monitoring:** Measure end-to-end processing times
- **Error Rate Tracking:** Monitor validation failures and API errors
- **Resource Utilization:** CPU, memory, and network usage patterns

### 6.2 Data Lineage Tracking

#### Audit Trail Maintenance
- **Source Attribution:** Track original data sources for each record
- **Transformation History:** Log all data modification operations
- **Quality Scores:** Maintain confidence scores throughout pipeline
- **Compliance Reporting:** Generate audit reports for regulatory requirements

---

## 7. Disaster Recovery and Backup

### 7.1 Data Backup Strategy

#### Multi-Tier Backup
- **Real-Time Replication:** Continuous backup of critical live data
- **Daily Snapshots:** Complete data warehouse backups
- **Weekly Archives:** Long-term storage for historical analysis
- **Geographic Distribution:** Cross-region backup storage

### 7.2 Recovery Procedures

#### Automated Recovery
```python
class DisasterRecovery:
    def initiate_recovery(self, failure_type: str, affected_systems: List[str]):
        """Execute appropriate recovery procedure"""
        if failure_type == 'api_outage':
            self._activate_fallback_sources()
        elif failure_type == 'storage_failure':
            self._restore_from_backup()
        elif failure_type == 'processing_failure':
            self._restart_pipeline_components()
        
        self._notify_stakeholders(failure_type, affected_systems)
```

---

## 8. Future Enhancements

### 8.1 Planned Improvements

- **Machine Learning Integration:** Automated data quality scoring
- **Real-Time Stream Processing:** Apache Kafka for high-volume data
- **Advanced Caching:** Redis Cluster for improved performance
- **API Gateway:** Centralized API management and monitoring

### 8.2 Scalability Considerations

- **Horizontal Scaling:** Kubernetes-based auto-scaling
- **Database Sharding:** Partition strategies for large datasets
- **CDN Integration:** Global data distribution networks
- **Microservices Architecture:** Service-based pipeline components

---

This data ingestion pipeline provides a robust foundation for the MultiBet system, ensuring reliable, scalable, and high-quality data flow from multiple sources to support advanced betting analytics and model predictions.