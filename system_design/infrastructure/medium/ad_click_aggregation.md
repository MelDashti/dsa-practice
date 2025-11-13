# Real-Time Ad Click Event Aggregation

## 1. Problem Statement

Design a real-time ad click event aggregation system that can process billions of ad clicks per day, compute real-time analytics (clicks, impressions, CTR, revenue), detect fraud, and provide both real-time and historical reporting. The system should handle high throughput, provide low-latency queries, and ensure accurate billing data.

## 2. Requirements

### Functional Requirements
- **Event ingestion**: Collect ad click and impression events from web/mobile
- **Real-time aggregation**: Compute metrics within seconds (clicks, impressions, CTR, revenue)
- **Multi-dimensional analytics**: Aggregate by various dimensions (campaign, ad, user, geo, device)
- **Fraud detection**: Identify suspicious click patterns
- **Real-time dashboards**: Display metrics with <10 second latency
- **Historical reporting**: Query data for past days/months
- **Billing accuracy**: Ensure accurate charging for advertisers
- **Deduplication**: Handle duplicate click events

### Non-Functional Requirements
- **Throughput**: Handle 100,000 events/second (peak)
- **Scale**: Process 5 billion events/day
- **Latency**: Sub-second event processing, <5 second query latency
- **Accuracy**: 99.9% accuracy in counting (at-least-once processing acceptable)
- **Availability**: 99.99% uptime
- **Data retention**: 90 days detailed, 2 years aggregated
- **Cost efficiency**: Minimize storage and compute costs

### Out of Scope
- Ad serving and targeting logic
- Creative management
- Bid optimization
- User profiling beyond click behavior

## 3. Capacity Estimation

### Scale Assumptions
- Peak events per second: 100,000 (clicks + impressions)
- Daily events: 5 billion
- Ratio: 10 impressions : 1 click
- Average event size: 500 bytes
- Aggregation dimensions: 15 (campaign, ad_id, user_id, country, city, device, browser, os, etc.)
- Time windows: 1 minute, 5 minutes, 1 hour, 1 day
- Active campaigns: 1 million
- Active advertisers: 100,000

### Storage Estimation

**Raw Events (detailed logs)**
```
Daily events = 5 billion
Event size = 500 bytes
Daily storage = 5B × 500 bytes = 2.5 TB/day

90-day retention = 2.5 TB × 90 = 225 TB
With compression (5:1) = 45 TB
```

**Aggregated Data**
```
Per-minute aggregates:
- Time buckets per day = 1,440 (24 hours × 60 minutes)
- Metrics per campaign per minute = 10 values × 8 bytes = 80 bytes
- Campaigns = 1M
- Storage per day = 1,440 × 1M × 80 bytes = 115 GB/day

90-day retention = 115 GB × 90 = 10.4 TB

Hourly aggregates (2 years):
- Storage per day = 24 × 1M × 80 bytes = 1.9 GB/day
- 2 years = 1.9 GB × 730 = 1.4 TB

Total storage = 45 TB (raw) + 10.4 TB (minute) + 1.4 TB (hourly) ≈ 57 TB
```

### Memory Estimation
```
Real-time aggregation (in-memory):
- Active time windows: 5 minutes
- Events in window: 100K/sec × 300 sec = 30M events
- Per event state: 100 bytes
- Memory needed: 30M × 100 bytes = 3 GB

Per-node memory: 32 GB
Aggregation nodes: 10 nodes
Total memory: 320 GB
```

### Network Bandwidth
```
Ingestion:
100K events/sec × 500 bytes = 50 MB/sec = 400 Mbps

Replication and internal traffic:
400 Mbps × 3 = 1.2 Gbps

Query traffic:
~200 Mbps

Total: ~2 Gbps
```

## 4. High-Level Design

```
┌─────────────────────────────────────────────────────┐
│              Event Sources                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Web Apps │  │  Mobile  │  │   SDK    │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼─────────────┼─────────────┼───────────────┘
        │             │             │
        │  HTTP POST  │             │
        ▼             ▼             ▼
   ┌────────────────────────────────────┐
   │      API Gateway / Load Balancer   │
   └────────────┬───────────────────────┘
                │
                ▼
   ┌────────────────────────────────────┐
   │    Event Validation & Enrichment   │
   │  - Schema validation               │
   │  - Bot detection                   │
   │  - Geo lookup                      │
   │  - User-agent parsing              │
   └────────┬───────────────────────────┘
            │
            ▼
   ┌────────────────────────────────────┐
   │       Message Queue (Kafka)        │
   │  Topics:                           │
   │  - raw_events                      │
   │  - validated_events                │
   │  - fraud_flagged                   │
   └──┬──────────────────────┬──────────┘
      │                      │
      ▼                      ▼
┌──────────────┐    ┌─────────────────┐
│ Real-Time    │    │  Fraud          │
│ Aggregation  │    │  Detection      │
│ (Flink)      │    │  Service        │
└──────┬───────┘    └────────┬────────┘
       │                     │
       ▼                     ▼
┌──────────────────────────────────────┐
│         Storage Layer                 │
│  ┌───────────┐  ┌──────────────────┐│
│  │ Redis     │  │ ClickHouse/      ││
│  │ (real-time│  │ Druid            ││
│  │  metrics) │  │ (OLAP queries)   ││
│  └───────────┘  └──────────────────┘│
│  ┌───────────────────────────────┐  │
│  │ S3 (Raw events archive)       │  │
│  └───────────────────────────────┘  │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│      Query API & Dashboards          │
│  - Real-time metrics                 │
│  - Historical reports                │
│  - Billing data                      │
└──────────────────────────────────────┘
```

### Core Components
1. **Event Collector**: Receive and validate events
2. **Message Queue**: Buffer events for processing
3. **Stream Processor**: Real-time aggregation
4. **Fraud Detector**: Identify suspicious patterns
5. **OLAP Database**: Fast analytical queries
6. **Cache Layer**: Sub-second metric access
7. **Query API**: Serve dashboard and reports
8. **Archival Storage**: Long-term event storage

## 5. API Design

### Event Ingestion API

```protobuf
// Event submission
service AdEventCollector {
    rpc RecordEvent(EventRequest) returns (EventResponse);
    rpc RecordEventBatch(BatchEventRequest) returns (EventResponse);
}

message EventRequest {
    string event_id = 1;          // Unique event ID (for dedup)
    string event_type = 2;         // "click" or "impression"
    int64 timestamp = 3;           // Unix timestamp (ms)

    // Ad identifiers
    string campaign_id = 4;
    string ad_id = 5;
    string advertiser_id = 6;

    // User context
    string user_id = 7;            // Hashed user identifier
    string session_id = 8;
    string ip_address = 9;
    string user_agent = 10;

    // Placement
    string publisher_id = 11;
    string placement_id = 12;
    string page_url = 13;

    // Device & geo
    string device_type = 14;       // mobile, desktop, tablet
    string os = 15;
    string browser = 16;
    string country = 17;
    string city = 18;

    // Financial
    double bid_price = 19;         // Cost per click/impression
    string currency = 20;
}

message EventResponse {
    bool success = 1;
    string error_message = 2;
    string tracking_id = 3;
}
```

### Query API

```python
class AnalyticsQueryAPI:
    def get_realtime_metrics(
        self,
        campaign_id: str,
        time_window: int = 300  # Last 5 minutes
    ) -> RealtimeMetrics:
        """
        Get real-time metrics for campaign
        Returns: clicks, impressions, CTR, spend
        """
        pass

    def get_aggregated_metrics(
        self,
        dimensions: List[str],  # e.g., ["campaign_id", "country"]
        metrics: List[str],      # e.g., ["clicks", "impressions", "ctr"]
        start_time: int,
        end_time: int,
        granularity: str = "hour"  # minute, hour, day
    ) -> AggregatedResult:
        """
        Get aggregated metrics with grouping
        """
        pass

    def get_top_performers(
        self,
        metric: str,  # "clicks", "ctr", "revenue"
        dimension: str,  # "campaign", "ad", "geo"
        limit: int = 100,
        start_time: int,
        end_time: int
    ) -> List[TopPerformer]:
        """
        Get top performing entities by metric
        """
        pass

    def get_funnel_metrics(
        self,
        campaign_id: str,
        start_time: int,
        end_time: int
    ) -> FunnelMetrics:
        """
        Get conversion funnel: impressions -> clicks -> conversions
        """
        pass
```

## 6. Component Design

### Event Collector

**Validation and Enrichment Pipeline**

```python
class EventCollector:
    def __init__(self):
        self.kafka_producer = KafkaProducer('raw_events')
        self.redis_dedup = RedisClient()
        self.geo_service = GeoIPService()
        self.user_agent_parser = UserAgentParser()

    async def record_event(self, event: EventRequest) -> EventResponse:
        """Process incoming event"""
        try:
            # 1. Validate event
            if not self.validate_event(event):
                return EventResponse(
                    success=False,
                    error_message="Invalid event data"
                )

            # 2. Check for duplicates
            if await self.is_duplicate(event.event_id):
                return EventResponse(
                    success=True,
                    tracking_id=event.event_id
                )

            # 3. Enrich event
            enriched_event = await self.enrich_event(event)

            # 4. Quick fraud check
            fraud_score = await self.quick_fraud_check(enriched_event)
            enriched_event.fraud_score = fraud_score

            # 5. Publish to Kafka
            await self.kafka_producer.send(
                topic='raw_events',
                key=event.campaign_id,  # Partition by campaign
                value=enriched_event.serialize()
            )

            # 6. Mark as seen (for deduplication)
            await self.mark_seen(event.event_id)

            return EventResponse(
                success=True,
                tracking_id=event.event_id
            )

        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return EventResponse(
                success=False,
                error_message=str(e)
            )

    def validate_event(self, event: EventRequest) -> bool:
        """Validate event fields"""
        # Check required fields
        if not event.event_id or not event.campaign_id:
            return False

        # Validate timestamp (not in future, not too old)
        now = int(time.time() * 1000)
        if event.timestamp > now + 60000:  # 1 minute future tolerance
            return False
        if event.timestamp < now - 86400000:  # 24 hours old
            return False

        # Validate event type
        if event.event_type not in ['click', 'impression']:
            return False

        # Validate bid price
        if event.bid_price < 0:
            return False

        return True

    async def is_duplicate(self, event_id: str) -> bool:
        """Check if event already processed using Redis"""
        # Use Redis SET with expiration
        key = f"event:{event_id}"
        exists = await self.redis_dedup.exists(key)
        return exists

    async def mark_seen(self, event_id: str):
        """Mark event as seen with 24-hour TTL"""
        key = f"event:{event_id}"
        await self.redis_dedup.setex(key, 86400, "1")

    async def enrich_event(self, event: EventRequest) -> EnrichedEvent:
        """Enrich event with additional context"""
        enriched = EnrichedEvent.from_event(event)

        # Parse user agent
        if event.user_agent:
            ua_info = self.user_agent_parser.parse(event.user_agent)
            enriched.device_type = ua_info.device_type
            enriched.browser = ua_info.browser
            enriched.browser_version = ua_info.browser_version
            enriched.os = ua_info.os
            enriched.os_version = ua_info.os_version

        # Geo lookup from IP
        if event.ip_address:
            geo_info = await self.geo_service.lookup(event.ip_address)
            enriched.country = geo_info.country
            enriched.city = geo_info.city
            enriched.latitude = geo_info.latitude
            enriched.longitude = geo_info.longitude

        # Add server timestamp
        enriched.server_timestamp = int(time.time() * 1000)

        return enriched

    async def quick_fraud_check(self, event: EnrichedEvent) -> float:
        """Quick fraud score (0-1, higher = more suspicious)"""
        score = 0.0

        # Check click frequency from same IP
        recent_clicks = await self.get_recent_clicks(event.ip_address)
        if recent_clicks > 100:  # >100 clicks in 1 minute
            score += 0.5

        # Check if user agent is suspicious
        if not event.user_agent or event.user_agent in KNOWN_BOT_AGENTS:
            score += 0.3

        # Check for impossible click times (< 100ms between impression and click)
        # This would be checked in fraud detection service with full context

        return min(score, 1.0)
```

### Stream Processor (Apache Flink)

**Real-Time Aggregation**

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common.time import Time

class AdEventStreamProcessor:
    def __init__(self):
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.set_parallelism(10)

    def create_pipeline(self):
        """Create Flink processing pipeline"""

        # 1. Read from Kafka
        events = self.env.add_source(
            FlinkKafkaConsumer(
                topics=['raw_events'],
                deserialization_schema=EventDeserializationSchema(),
                properties={'bootstrap.servers': 'kafka:9092'}
            )
        )

        # 2. Parse and validate
        valid_events = events.filter(lambda e: e.fraud_score < 0.8)

        # 3. Aggregate by multiple dimensions

        # 3a. Per-campaign, per-minute aggregation
        campaign_metrics = (valid_events
            .key_by(lambda e: e.campaign_id)
            .window(TumblingProcessingTimeWindows.of(Time.minutes(1)))
            .aggregate(CampaignAggregator())
        )

        # 3b. Per-campaign-country, per-minute aggregation
        campaign_country_metrics = (valid_events
            .key_by(lambda e: (e.campaign_id, e.country))
            .window(TumblingProcessingTimeWindows.of(Time.minutes(1)))
            .aggregate(MultiDimensionAggregator(['campaign_id', 'country']))
        )

        # 3c. Per-advertiser aggregation
        advertiser_metrics = (valid_events
            .key_by(lambda e: e.advertiser_id)
            .window(TumblingProcessingTimeWindows.of(Time.minutes(1)))
            .aggregate(AdvertiserAggregator())
        )

        # 4. Sink to Redis (real-time) and ClickHouse (historical)
        campaign_metrics.add_sink(RedisSink())
        campaign_metrics.add_sink(ClickHouseSink())

        campaign_country_metrics.add_sink(RedisSink())
        campaign_country_metrics.add_sink(ClickHouseSink())

        advertiser_metrics.add_sink(RedisSink())
        advertiser_metrics.add_sink(ClickHouseSink())

        # 5. Archive raw events to S3
        events.add_sink(S3Sink())

        # Execute pipeline
        self.env.execute("Ad Click Aggregation")

class CampaignAggregator(AggregateFunction):
    """Aggregate metrics per campaign"""

    def create_accumulator(self):
        return {
            'clicks': 0,
            'impressions': 0,
            'spend': 0.0,
            'unique_users': set()
        }

    def add(self, value: AdEvent, accumulator: Dict):
        if value.event_type == 'click':
            accumulator['clicks'] += 1
            accumulator['spend'] += value.bid_price
        elif value.event_type == 'impression':
            accumulator['impressions'] += 1

        accumulator['unique_users'].add(value.user_id)
        return accumulator

    def get_result(self, accumulator: Dict) -> CampaignMetrics:
        clicks = accumulator['clicks']
        impressions = accumulator['impressions']
        ctr = clicks / impressions if impressions > 0 else 0

        return CampaignMetrics(
            clicks=clicks,
            impressions=impressions,
            ctr=ctr,
            spend=accumulator['spend'],
            unique_users=len(accumulator['unique_users'])
        )

    def merge(self, acc1: Dict, acc2: Dict) -> Dict:
        """Merge accumulators (for parallel processing)"""
        return {
            'clicks': acc1['clicks'] + acc2['clicks'],
            'impressions': acc1['impressions'] + acc2['impressions'],
            'spend': acc1['spend'] + acc2['spend'],
            'unique_users': acc1['unique_users'] | acc2['unique_users']
        }
```

### Fraud Detection Service

**Pattern-based Fraud Detection**

```python
class FraudDetectionService:
    def __init__(self):
        self.redis = RedisClient()
        self.rule_engine = FraudRuleEngine()

    async def analyze_event(self, event: EnrichedEvent) -> FraudAnalysis:
        """Comprehensive fraud analysis"""
        signals = []
        fraud_score = 0.0

        # 1. Click frequency analysis
        ip_clicks = await self.get_click_count(
            key=f"ip:{event.ip_address}",
            window=60  # Last 1 minute
        )
        if ip_clicks > 100:
            signals.append("high_click_frequency")
            fraud_score += 0.4

        # 2. User-agent analysis
        if not event.user_agent or self.is_bot_user_agent(event.user_agent):
            signals.append("suspicious_user_agent")
            fraud_score += 0.3

        # 3. Impossible click pattern
        # Click within 100ms of impression (bot-like behavior)
        if event.event_type == 'click':
            last_impression = await self.get_last_impression(
                user_id=event.user_id,
                ad_id=event.ad_id
            )
            if last_impression:
                time_diff = event.timestamp - last_impression.timestamp
                if time_diff < 100:  # < 100ms
                    signals.append("impossible_click_time")
                    fraud_score += 0.5

        # 4. Geographic anomaly
        if await self.is_geo_anomaly(event):
            signals.append("geo_anomaly")
            fraud_score += 0.3

        # 5. Click farm detection
        if await self.is_click_farm(event.ip_address):
            signals.append("click_farm")
            fraud_score += 0.6

        # 6. Device fingerprint mismatch
        if await self.is_device_mismatch(event):
            signals.append("device_mismatch")
            fraud_score += 0.2

        fraud_score = min(fraud_score, 1.0)

        return FraudAnalysis(
            fraud_score=fraud_score,
            signals=signals,
            is_fraud=fraud_score > 0.7
        )

    async def is_click_farm(self, ip_address: str) -> bool:
        """Detect if IP is from known click farm"""
        # Check against blacklist
        is_blacklisted = await self.redis.sismember('ip_blacklist', ip_address)

        # Check if IP has excessive unique user IDs
        # (click farms rotate user IDs from same IP)
        unique_users = await self.redis.scard(f"ip_users:{ip_address}")
        if unique_users > 1000:  # 1000 different users from same IP
            return True

        return is_blacklisted

    async def is_geo_anomaly(self, event: EnrichedEvent) -> bool:
        """Detect geographic anomalies"""
        # Check if user jumped locations impossibly fast
        last_event = await self.get_last_user_event(event.user_id)

        if last_event and last_event.country != event.country:
            time_diff = (event.timestamp - last_event.timestamp) / 1000  # seconds

            # Calculate distance
            distance = self.calculate_distance(
                last_event.latitude, last_event.longitude,
                event.latitude, event.longitude
            )

            # Check if physically possible (even by plane)
            max_speed = 1000  # km/h (speed of commercial plane)
            required_speed = distance / (time_diff / 3600)

            if required_speed > max_speed:
                return True

        return False
```

### Storage Layer

**Redis for Real-Time Metrics**

```python
class RealtimeMetricsCache:
    """Redis-based cache for sub-second metric access"""

    def __init__(self):
        self.redis = redis.Redis(decode_responses=True)

    async def update_campaign_metrics(self, campaign_id: str, metrics: CampaignMetrics):
        """Update real-time metrics in Redis"""
        key = f"campaign:{campaign_id}:1m"

        # Use Redis hash for metrics
        pipeline = self.redis.pipeline()

        pipeline.hincrby(key, 'clicks', metrics.clicks)
        pipeline.hincrby(key, 'impressions', metrics.impressions)
        pipeline.hincrbyfloat(key, 'spend', metrics.spend)

        # Set TTL to 10 minutes
        pipeline.expire(key, 600)

        await pipeline.execute()

    async def get_realtime_metrics(self, campaign_id: str) -> CampaignMetrics:
        """Get real-time metrics from Redis"""
        key = f"campaign:{campaign_id}:1m"

        data = await self.redis.hgetall(key)

        if not data:
            return None

        return CampaignMetrics(
            clicks=int(data.get('clicks', 0)),
            impressions=int(data.get('impressions', 0)),
            spend=float(data.get('spend', 0.0)),
            ctr=self.calculate_ctr(data)
        )

    def calculate_ctr(self, data: Dict) -> float:
        clicks = int(data.get('clicks', 0))
        impressions = int(data.get('impressions', 0))
        return clicks / impressions if impressions > 0 else 0
```

**ClickHouse for OLAP Queries**

```sql
-- ClickHouse table schema for aggregated metrics
CREATE TABLE ad_metrics_1m (
    date Date,
    timestamp DateTime,
    campaign_id String,
    ad_id String,
    advertiser_id String,
    country String,
    city String,
    device_type String,
    clicks UInt64,
    impressions UInt64,
    spend Float64,
    unique_users UInt64
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (campaign_id, timestamp, country, device_type);

-- Query example: Get campaign metrics for last 24 hours
SELECT
    campaign_id,
    sum(clicks) as total_clicks,
    sum(impressions) as total_impressions,
    sum(clicks) / sum(impressions) as ctr,
    sum(spend) as total_spend
FROM ad_metrics_1m
WHERE timestamp >= now() - INTERVAL 24 HOUR
  AND campaign_id = 'campaign_123'
GROUP BY campaign_id;

-- Query example: Top campaigns by CTR
SELECT
    campaign_id,
    sum(clicks) as clicks,
    sum(impressions) as impressions,
    sum(clicks) / sum(impressions) as ctr
FROM ad_metrics_1m
WHERE date = today()
GROUP BY campaign_id
HAVING impressions > 10000
ORDER BY ctr DESC
LIMIT 100;

-- Multi-dimensional drill-down
SELECT
    country,
    device_type,
    sum(clicks) as clicks,
    sum(impressions) as impressions,
    sum(spend) as spend
FROM ad_metrics_1m
WHERE campaign_id = 'campaign_123'
  AND date >= today() - 7
GROUP BY country, device_type
ORDER BY clicks DESC;
```

## 7. Data Structures & Storage

### Event Schema

```protobuf
message AdEvent {
    string event_id = 1;
    string event_type = 2;  // click, impression
    int64 timestamp = 3;

    // Dimensions (for grouping)
    map<string, string> dimensions = 4;

    // Metrics
    double bid_price = 5;
    double fraud_score = 6;
}
```

### Aggregation State

```python
# In-memory state (Flink)
class AggregationState:
    clicks: int = 0
    impressions: int = 0
    spend: float = 0.0
    unique_users: HyperLogLog = HyperLogLog(0.01)  # Cardinality estimation
    last_update: int = 0
```

## 8. Fault Tolerance & High Availability

### Kafka Checkpointing

```python
# Flink checkpointing for exactly-once processing
env.enable_checkpointing(60000)  # Checkpoint every 60 seconds
env.get_checkpoint_config().set_min_pause_between_checkpoints(30000)
```

### Redis Replication

```python
# Redis Sentinel for HA
redis_sentinel = Sentinel([
    ('sentinel1', 26379),
    ('sentinel2', 26379),
    ('sentinel3', 26379)
])
redis_master = redis_sentinel.master_for('mymaster')
```

### Data Reconciliation

```python
# Periodic reconciliation between Redis and ClickHouse
async def reconcile_metrics(campaign_id: str, timestamp: int):
    """Verify metrics consistency"""
    redis_metrics = await redis_cache.get_metrics(campaign_id, timestamp)
    clickhouse_metrics = await clickhouse.query_metrics(campaign_id, timestamp)

    if abs(redis_metrics.clicks - clickhouse_metrics.clicks) > 10:
        # Alert on discrepancy
        alert_discrepancy(campaign_id, redis_metrics, clickhouse_metrics)
```

## 9. Monitoring & Observability

### Key Metrics

```python
# Ingestion metrics
events_received_total = Counter('events_received_total', labels=['event_type'])
events_processed_total = Counter('events_processed_total', labels=['status'])
ingestion_latency = Histogram('ingestion_latency_seconds')

# Processing metrics
events_per_second = Gauge('events_per_second')
aggregation_lag = Gauge('aggregation_lag_seconds')
fraud_detection_rate = Gauge('fraud_detection_rate')

# Storage metrics
redis_hit_rate = Gauge('redis_hit_rate')
clickhouse_query_latency = Histogram('clickhouse_query_latency_seconds')

# Business metrics
total_clicks = Counter('total_clicks')
total_spend = Counter('total_spend')
average_ctr = Gauge('average_ctr')
```

## 10. Scalability

### Horizontal Scaling

- **Event Collectors**: Add more API servers behind load balancer
- **Kafka**: Increase partitions for higher throughput
- **Flink**: Increase parallelism and add more task managers
- **ClickHouse**: Add more nodes to cluster
- **Redis**: Use Redis Cluster for sharding

### Optimization Techniques

```python
# Batch processing for better throughput
async def process_batch(events: List[AdEvent]):
    # Batch write to Kafka
    await kafka_producer.send_batch(events)

    # Batch write to ClickHouse
    await clickhouse.insert_batch(events)
```

## 11. Trade-offs

### Accuracy vs Latency
- **Exact counting**: Slower, more resources
- **Approximate (HyperLogLog)**: Faster, 1-2% error

### Storage Duration
- **Long retention**: High storage cost
- **Short retention with aggregation**: Lower cost, less detail

### Processing Semantics
- **At-least-once**: Possible duplicates, but no data loss
- **Exactly-once**: More complex, higher latency

## 12. Follow-up Questions

1. How would you handle late-arriving events?
2. How would you implement conversion tracking (post-click conversions)?
3. How would you handle multi-touch attribution?
4. How would you scale to 1M events/second?
5. How would you implement real-time alerting for campaigns?
6. How would you handle timezone conversions for global campaigns?
7. How would you implement A/B testing for ads?
8. How would you detect click injection fraud?
9. How would you implement budget pacing?
10. How would you handle GDPR compliance for user data?
