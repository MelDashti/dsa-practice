# Metrics Monitoring System (Prometheus/Datadog-style)

## 1. Problem Statement

Design a distributed metrics monitoring and alerting system similar to Prometheus, Datadog, or Grafana that can collect, store, query, and visualize metrics from thousands of services and infrastructure components. The system should support real-time monitoring, historical analysis, alerting, and anomaly detection.

## 2. Requirements

### Functional Requirements
- **Metrics collection**: Scrape metrics from multiple sources (servers, containers, applications)
- **Time-series storage**: Store metrics with timestamps efficiently
- **Querying**: Support flexible queries and aggregations
- **Alerting**: Define alert rules and send notifications
- **Visualization**: Display metrics on dashboards
- **Service discovery**: Automatically discover and monitor new services
- **Multi-tenancy**: Support multiple teams/projects with isolation
- **Retention policies**: Configurable data retention and downsampling

### Non-Functional Requirements
- **Scale**: Monitor 10,000 hosts with 1000 metrics each
- **Throughput**: Handle 10 million metrics/second
- **Latency**: Sub-second query response for recent data
- **Retention**: 30 days full resolution, 1 year downsampled
- **Availability**: 99.9% uptime
- **Durability**: No data loss
- **Query performance**: P99 query latency <2 seconds

### Out of Scope
- Log aggregation (separate from metrics)
- Distributed tracing
- APM (Application Performance Monitoring) detailed profiling
- Incident management workflows

## 3. Capacity Estimation

### Scale Assumptions
- Number of hosts: 10,000
- Metrics per host: 1,000
- Total unique time series: 10 million
- Scrape interval: 15 seconds
- Data points per second: 10M / 15 = 667,000 points/sec
- Average metric value size: 8 bytes (float64)
- Average label cardinality: 10 labels per metric
- Label size: 50 bytes average

### Storage Estimation
```
Per data point:
- Timestamp: 8 bytes
- Value: 8 bytes
- Total: 16 bytes

Data per day (full resolution):
667K points/sec × 86,400 sec × 16 bytes = 922 GB/day

Data per month (30 days):
922 GB × 30 = 27.6 TB/month

With compression (5:1 ratio):
27.6 TB / 5 = 5.5 TB/month

1-year retention (downsampled to 5min):
- Downsampling ratio: 5min / 15sec = 20x reduction
- Storage: 5.5 TB × 12 / 20 = 3.3 TB/year

Total storage (30 days full + 1 year downsampled):
5.5 TB + 3.3 TB = 8.8 TB ≈ 10 TB
```

### Memory Estimation
```
Active time series in memory:
- 10M time series × 1KB metadata = 10 GB
- Recent data points (1 hour): 667K points/sec × 3600 sec × 16 bytes = 38 GB
- Query cache: 20 GB
- Index structures: 10 GB
Total memory per node: ~80 GB

Storage nodes: 10 (for redundancy and parallelism)
Total memory: 800 GB
```

### Network Bandwidth
```
Ingest bandwidth:
667K points/sec × 16 bytes = 10.6 MB/sec = 85 Mbps

With overhead (labels, metadata):
85 Mbps × 5 = 425 Mbps

Query bandwidth (dashboards, alerts):
~200 Mbps

Total bandwidth: ~1 Gbps
```

## 4. High-Level Design

```
┌──────────────────────────────────────────────────────────┐
│                     Data Sources                         │
│  ┌───────────┐  ┌───────────┐  ┌────────────┐          │
│  │ App       │  │ Kubernetes│  │ Databases  │          │
│  │ Servers   │  │ Clusters  │  │            │          │
│  └─────┬─────┘  └─────┬─────┘  └──────┬─────┘          │
└────────┼──────────────┼─────────────────┼────────────────┘
         │              │                 │
         │ (Pull)       │ (Pull)          │ (Push)
         ▼              ▼                 ▼
    ┌────────────────────────────────────────────┐
    │         Metrics Collection Layer           │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐│
    │  │ Scraper  │  │ Scraper  │  │ Push     ││
    │  │ Agent 1  │  │ Agent 2  │  │ Gateway  ││
    │  └────┬─────┘  └────┬─────┘  └────┬─────┘│
    └───────┼─────────────┼─────────────┼──────┘
            │             │             │
            └─────────────┴─────────────┘
                          │
                          ▼
    ┌─────────────────────────────────────────────┐
    │         Load Balancer / Distributor         │
    │      (Hash-based routing by metric)         │
    └───────────────┬─────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │Ingester │ │Ingester │ │Ingester │  (Write path)
   │  Node 1 │ │  Node 2 │ │  Node 3 │
   └────┬────┘ └────┬────┘ └────┬────┘
        │           │           │
        │           │           │ Flush
        ▼           ▼           ▼
   ┌─────────────────────────────────┐
   │      Time-Series Storage        │
   │    (Distributed TSDB)           │
   │  - Blocks by time range         │
   │  - Compressed columnar format   │
   └────────┬────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────┐
   │      Object Storage (S3)        │
   │    (Long-term retention)        │
   └─────────────────────────────────┘

Query Path:
   ┌─────────┐
   │ Query   │
   │ Frontend│ ← User/Dashboard
   └────┬────┘
        │
        ▼
   ┌──────────────┐
   │ Query Engine │
   │ - PromQL     │
   │ - Aggregation│
   └──────┬───────┘
          │
          ├──────────────────┐
          ▼                  ▼
    [Ingesters]         [TSDB Storage]
    (Recent data)       (Historical data)

Alerting:
   ┌────────────────┐
   │ Alert Manager  │
   │ - Rule eval    │
   │ - Dedup        │
   │ - Routing      │
   └───────┬────────┘
           │
           ▼
   ┌────────────────┐
   │ Notification   │
   │ Services       │
   │ PagerDuty/Slack│
   └────────────────┘
```

### Core Components
1. **Metrics Collectors**: Scrape or receive metrics
2. **Distributor**: Routes metrics to ingesters
3. **Ingesters**: Buffer recent data in memory
4. **TSDB Storage**: Persistent time-series database
5. **Query Engine**: Execute queries across data
6. **Alert Manager**: Evaluate rules and send alerts
7. **Query Frontend**: API gateway for queries
8. **Service Discovery**: Discover targets to monitor

## 5. API Design

### Metrics Collection API

```protobuf
// Push metrics (for applications)
service MetricsCollector {
    rpc PushMetrics(MetricsRequest) returns (MetricsResponse);
}

message MetricsRequest {
    repeated TimeSeries timeseries = 1;
}

message TimeSeries {
    repeated Label labels = 1;     // e.g., {name: "cpu_usage", host: "server1"}
    repeated Sample samples = 2;
}

message Label {
    string name = 1;
    string value = 2;
}

message Sample {
    int64 timestamp = 1;  // Unix timestamp in milliseconds
    double value = 2;
}
```

### Query API

```python
class MetricsQueryAPI:
    def query(self, query: str, time: int) -> QueryResult:
        """
        Execute instant query at specific time
        query: PromQL query string, e.g., "cpu_usage{host='server1'}"
        time: Unix timestamp
        """
        pass

    def query_range(self, query: str, start: int, end: int, step: int) -> QueryResult:
        """
        Execute range query over time period
        query: PromQL query
        start, end: Unix timestamps
        step: Resolution in seconds
        """
        pass

    def query_exemplars(self, query: str, start: int, end: int) -> ExemplarResult:
        """Query exemplars (sample traces) for metrics"""
        pass

    def label_values(self, label: str) -> List[str]:
        """Get all values for a label"""
        pass

    def series(self, match: List[str], start: int, end: int) -> List[SeriesMetadata]:
        """Find time series matching label matchers"""
        pass
```

### Alert Management API

```python
class AlertAPI:
    def create_alert_rule(self, rule: AlertRule) -> str:
        """
        Create alert rule
        AlertRule: {
            name: str,
            query: str,  # PromQL query
            duration: int,  # Evaluation interval
            threshold: float,
            severity: str,  # critical, warning, info
            labels: Dict[str, str],
            annotations: Dict[str, str]
        }
        Returns: rule_id
        """
        pass

    def list_active_alerts(self) -> List[Alert]:
        """Get currently firing alerts"""
        pass

    def silence_alert(self, matcher: Dict[str, str], duration: int):
        """Silence alerts matching labels"""
        pass
```

## 6. Component Design

### Metrics Scraper

**Pull-based Collection (Prometheus-style)**

```python
class MetricsScraper:
    def __init__(self, targets: List[str], scrape_interval: int = 15):
        self.targets = targets  # List of target URLs
        self.scrape_interval = scrape_interval
        self.executor = ThreadPoolExecutor(max_workers=100)

    async def scrape_loop(self):
        """Continuously scrape targets"""
        while True:
            start_time = time.time()

            # Scrape all targets concurrently
            tasks = [self.scrape_target(target) for target in self.targets]
            await asyncio.gather(*tasks)

            # Sleep until next scrape interval
            elapsed = time.time() - start_time
            sleep_time = max(0, self.scrape_interval - elapsed)
            await asyncio.sleep(sleep_time)

    async def scrape_target(self, target: str):
        """Scrape metrics from single target"""
        try:
            # Fetch metrics endpoint
            response = await self.http_client.get(
                f"{target}/metrics",
                timeout=10
            )

            if response.status_code != 200:
                self.record_scrape_error(target, response.status_code)
                return

            # Parse metrics (Prometheus format)
            metrics = self.parse_metrics(response.text)

            # Add target labels
            for metric in metrics:
                metric.labels['instance'] = target

            # Send to distributor
            await self.send_to_distributor(metrics)

            self.record_scrape_success(target, len(metrics))

        except Exception as e:
            self.record_scrape_error(target, str(e))

    def parse_metrics(self, text: str) -> List[TimeSeries]:
        """
        Parse Prometheus exposition format
        Example:
        # HELP http_requests_total Total HTTP requests
        # TYPE http_requests_total counter
        http_requests_total{method="GET",status="200"} 1234 1609459200000
        """
        metrics = []
        lines = text.split('\n')

        current_metric = None
        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                # Skip comments and empty lines
                if line.startswith('# TYPE'):
                    # Extract metric type
                    parts = line.split()
                    if len(parts) >= 4:
                        current_metric = {
                            'name': parts[2],
                            'type': parts[3]
                        }
                continue

            # Parse metric line
            metric = self.parse_metric_line(line)
            if metric:
                metrics.append(metric)

        return metrics

    def parse_metric_line(self, line: str) -> Optional[TimeSeries]:
        """
        Parse single metric line
        Format: metric_name{label1="value1",label2="value2"} value timestamp
        """
        # Find metric name and labels
        if '{' in line:
            name_end = line.index('{')
            name = line[:name_end]
            labels_end = line.index('}')
            labels_str = line[name_end+1:labels_end]
            rest = line[labels_end+1:].strip()
        else:
            parts = line.split()
            name = parts[0]
            labels_str = ""
            rest = ' '.join(parts[1:])

        # Parse labels
        labels = {'__name__': name}
        if labels_str:
            for label_pair in labels_str.split(','):
                key, value = label_pair.split('=')
                labels[key.strip()] = value.strip('"')

        # Parse value and timestamp
        parts = rest.split()
        value = float(parts[0])
        timestamp = int(parts[1]) if len(parts) > 1 else int(time.time() * 1000)

        return TimeSeries(
            labels=labels,
            samples=[Sample(timestamp=timestamp, value=value)]
        )
```

### Distributor

**Consistent Hashing for Metric Distribution**

```python
class Distributor:
    """
    Distributes metrics to ingesters based on consistent hashing
    Ensures same metric always goes to same ingester
    """

    def __init__(self, ingesters: List[str], replication_factor: int = 3):
        self.ingesters = ingesters
        self.replication_factor = replication_factor
        self.hash_ring = ConsistentHashRing(ingesters, virtual_nodes=512)

    async def distribute_metrics(self, metrics: List[TimeSeries]):
        """Distribute metrics to appropriate ingesters"""
        # Group metrics by ingester
        ingester_batches = defaultdict(list)

        for metric in metrics:
            # Generate metric fingerprint (hash of labels)
            fingerprint = self.generate_fingerprint(metric.labels)

            # Get ingesters for this metric (with replication)
            target_ingesters = self.hash_ring.get_nodes(
                fingerprint,
                count=self.replication_factor
            )

            # Add to batches
            for ingester in target_ingesters:
                ingester_batches[ingester].append(metric)

        # Send batches to ingesters in parallel
        tasks = []
        for ingester, batch in ingester_batches.items():
            task = self.send_to_ingester(ingester, batch)
            tasks.append(task)

        await asyncio.gather(*tasks)

    def generate_fingerprint(self, labels: Dict[str, str]) -> int:
        """
        Generate stable fingerprint for metric
        Labels are sorted for consistency
        """
        sorted_labels = sorted(labels.items())
        label_str = ','.join(f"{k}={v}" for k, v in sorted_labels)
        return mmh3.hash64(label_str)[0]  # MurmurHash3

    async def send_to_ingester(self, ingester: str, metrics: List[TimeSeries]):
        """Send metrics batch to ingester"""
        try:
            request = MetricsRequest(timeseries=metrics)
            response = await self.grpc_client.push_metrics(
                ingester,
                request,
                timeout=5
            )
            return response
        except Exception as e:
            logger.error(f"Failed to send to ingester {ingester}: {e}")
            # Retry or send to alternate ingester
            raise
```

### Ingester

**In-Memory Buffer with Periodic Flush**

```python
class Ingester:
    """
    Receives metrics and stores in memory
    Periodically flushes to persistent storage
    """

    def __init__(self, flush_interval: int = 60):
        self.series_cache = {}  # fingerprint -> TimeSeriesData
        self.flush_interval = flush_interval
        self.lock = asyncio.Lock()
        self.wal = WriteAheadLog()  # For durability

    async def push_metrics(self, request: MetricsRequest):
        """Receive and buffer metrics"""
        async with self.lock:
            for timeseries in request.timeseries:
                fingerprint = self.generate_fingerprint(timeseries.labels)

                # Get or create series
                if fingerprint not in self.series_cache:
                    self.series_cache[fingerprint] = TimeSeriesData(
                        labels=timeseries.labels,
                        samples=[]
                    )

                # Append samples
                series = self.series_cache[fingerprint]
                series.samples.extend(timeseries.samples)

                # Write to WAL for durability
                self.wal.append(fingerprint, timeseries.samples)

        return MetricsResponse(success=True)

    async def flush_loop(self):
        """Periodically flush data to storage"""
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush()

    async def flush(self):
        """Flush cached data to persistent storage"""
        async with self.lock:
            if not self.series_cache:
                return

            # Create block for this time range
            block = self.create_block(self.series_cache)

            # Write to storage
            await self.storage.write_block(block)

            # Clear cache for flushed data
            # Keep recent data (e.g., last 10 minutes)
            self.evict_old_data()

            # Truncate WAL
            self.wal.truncate()

    def create_block(self, series_data: Dict[int, TimeSeriesData]) -> Block:
        """
        Create compressed block from time series data
        Uses columnar format for better compression
        """
        block = Block(
            min_time=min(s.samples[0].timestamp for s in series_data.values()),
            max_time=max(s.samples[-1].timestamp for s in series_data.values())
        )

        for fingerprint, series in series_data.items():
            # Compress timestamps (delta encoding)
            timestamps = [s.timestamp for s in series.samples]
            compressed_timestamps = self.compress_timestamps(timestamps)

            # Compress values (XOR compression for floats)
            values = [s.value for s in series.samples]
            compressed_values = self.compress_values(values)

            block.add_series(
                fingerprint=fingerprint,
                labels=series.labels,
                timestamps=compressed_timestamps,
                values=compressed_values
            )

        return block

    def compress_timestamps(self, timestamps: List[int]) -> bytes:
        """
        Delta-of-delta encoding for timestamps
        Exploits regularity in time series (fixed scrape interval)
        """
        if not timestamps:
            return b''

        # Store first timestamp as-is
        deltas = [timestamps[0]]

        # Compute deltas
        for i in range(1, len(timestamps)):
            delta = timestamps[i] - timestamps[i-1]
            deltas.append(delta)

        # Compute delta-of-deltas
        dod = [deltas[1]] if len(deltas) > 1 else []
        for i in range(2, len(deltas)):
            dod.append(deltas[i] - deltas[i-1])

        # Variable-length encoding
        return self.variable_encode(dod)

    def compress_values(self, values: List[float]) -> bytes:
        """
        XOR compression for float values
        Adjacent values in time series often have many identical bits
        """
        if not values:
            return b''

        compressed = []
        prev_value = values[0]
        compressed.append(struct.pack('d', prev_value))

        for value in values[1:]:
            # XOR with previous value
            xor_value = struct.unpack('Q', struct.pack('d', value))[0] ^ \
                       struct.unpack('Q', struct.pack('d', prev_value))[0]

            # Store XOR result (many leading/trailing zeros)
            compressed.append(self.encode_xor(xor_value))
            prev_value = value

        return b''.join(compressed)
```

### Time-Series Storage

**Block-based Storage with Inverted Index**

```python
class TSDBStorage:
    """
    Persistent time-series storage
    Data organized in blocks by time range
    """

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.blocks = []  # List of Block objects
        self.index = InvertedIndex()  # Labels -> Series IDs

    async def write_block(self, block: Block):
        """Write block to disk"""
        block_id = self.generate_block_id(block.min_time, block.max_time)
        block_path = os.path.join(self.data_dir, block_id)

        # Write block data
        with open(f"{block_path}/data.bin", 'wb') as f:
            f.write(block.serialize())

        # Write index
        with open(f"{block_path}/index.json", 'w') as f:
            json.dump(block.index, f)

        # Update in-memory index
        self.index.add_block(block)
        self.blocks.append(block)

        # Upload to object storage for long-term retention
        await self.upload_to_object_storage(block)

    async def query(self, matchers: List[LabelMatcher], start: int, end: int) -> List[TimeSeries]:
        """
        Query time series matching labels in time range
        """
        # 1. Find matching series using index
        series_ids = self.index.find_series(matchers)

        # 2. Find blocks overlapping with time range
        relevant_blocks = [
            b for b in self.blocks
            if self.overlaps(b.min_time, b.max_time, start, end)
        ]

        # 3. Read data from blocks
        results = []
        for block in relevant_blocks:
            block_results = await self.read_from_block(
                block,
                series_ids,
                start,
                end
            )
            results.extend(block_results)

        # 4. Merge results
        return self.merge_series(results)

    def overlaps(self, block_start: int, block_end: int,
                query_start: int, query_end: int) -> bool:
        """Check if block time range overlaps with query range"""
        return not (block_end < query_start or block_start > query_end)

    async def read_from_block(self, block: Block, series_ids: Set[int],
                             start: int, end: int) -> List[TimeSeries]:
        """Read specific series from block"""
        results = []

        # Load block data
        with open(f"{block.path}/data.bin", 'rb') as f:
            data = f.read()

        # Deserialize block
        block_data = Block.deserialize(data)

        # Extract requested series
        for series_id in series_ids:
            if series_id in block_data.series:
                series = block_data.series[series_id]

                # Decompress timestamps and values
                timestamps = self.decompress_timestamps(series.timestamps)
                values = self.decompress_values(series.values)

                # Filter by time range
                samples = [
                    Sample(timestamp=t, value=v)
                    for t, v in zip(timestamps, values)
                    if start <= t <= end
                ]

                if samples:
                    results.append(TimeSeries(
                        labels=series.labels,
                        samples=samples
                    ))

        return results
```

### Inverted Index

**Efficient Label-based Lookup**

```python
class InvertedIndex:
    """
    Inverted index for efficient label matching
    Maps label pairs to series IDs
    """

    def __init__(self):
        # label_name -> label_value -> set of series IDs
        self.index = defaultdict(lambda: defaultdict(set))

        # series_id -> full labels
        self.series_labels = {}

    def add_series(self, series_id: int, labels: Dict[str, str]):
        """Add series to index"""
        self.series_labels[series_id] = labels

        # Index each label pair
        for label_name, label_value in labels.items():
            self.index[label_name][label_value].add(series_id)

    def find_series(self, matchers: List[LabelMatcher]) -> Set[int]:
        """
        Find series matching label matchers
        LabelMatcher: {name: str, value: str, op: '=', '!=', '=~', '!~'}
        """
        if not matchers:
            return set(self.series_labels.keys())

        # Start with all series matching first matcher
        first_matcher = matchers[0]
        result_set = self.match_label(first_matcher)

        # Intersect with remaining matchers
        for matcher in matchers[1:]:
            matching = self.match_label(matcher)

            if matcher.op in ['=', '=~']:
                # AND operation
                result_set &= matching
            else:  # '!=' or '!~'
                # AND NOT operation
                result_set -= matching

        return result_set

    def match_label(self, matcher: LabelMatcher) -> Set[int]:
        """Find series matching single label matcher"""
        label_name = matcher.name
        label_value = matcher.value
        op = matcher.op

        if op == '=':
            # Exact match
            return self.index[label_name].get(label_value, set())

        elif op == '!=':
            # Not equal
            all_series = set(self.series_labels.keys())
            matching = self.index[label_name].get(label_value, set())
            return all_series - matching

        elif op == '=~':
            # Regex match
            pattern = re.compile(label_value)
            matching = set()
            for value, series_ids in self.index[label_name].items():
                if pattern.match(value):
                    matching.update(series_ids)
            return matching

        elif op == '!~':
            # Regex not match
            all_series = set(self.series_labels.keys())
            pattern = re.compile(label_value)
            matching = set()
            for value, series_ids in self.index[label_name].items():
                if pattern.match(value):
                    matching.update(series_ids)
            return all_series - matching

        return set()
```

### Query Engine

**PromQL Query Execution**

```python
class QueryEngine:
    """Execute PromQL queries"""

    def __init__(self, storage: TSDBStorage, ingesters: List[Ingester]):
        self.storage = storage
        self.ingesters = ingesters
        self.parser = PromQLParser()

    async def execute_query(self, query: str, time: int) -> QueryResult:
        """Execute instant query"""
        # 1. Parse query
        ast = self.parser.parse(query)

        # 2. Execute query plan
        result = await self.execute_ast(ast, time, time)

        return result

    async def execute_range_query(self, query: str, start: int, end: int, step: int) -> QueryResult:
        """Execute range query"""
        # 1. Parse query
        ast = self.parser.parse(query)

        # 2. Execute for each time step
        results = []
        current_time = start

        while current_time <= end:
            result = await self.execute_ast(ast, current_time, current_time)
            results.append((current_time, result))
            current_time += step

        return RangeQueryResult(results=results)

    async def execute_ast(self, ast: ASTNode, start: int, end: int):
        """Execute abstract syntax tree"""
        if ast.type == 'selector':
            # Fetch raw time series
            return await self.fetch_series(ast.matchers, start, end)

        elif ast.type == 'aggregation':
            # Execute aggregation (sum, avg, max, min, etc.)
            data = await self.execute_ast(ast.child, start, end)
            return self.aggregate(data, ast.agg_func, ast.grouping)

        elif ast.type == 'binary_op':
            # Execute binary operation (+, -, *, /, etc.)
            left = await self.execute_ast(ast.left, start, end)
            right = await self.execute_ast(ast.right, start, end)
            return self.binary_op(left, right, ast.op)

        elif ast.type == 'function':
            # Execute function (rate, increase, etc.)
            data = await self.execute_ast(ast.child, start, end)
            return self.apply_function(data, ast.func_name, ast.args)

    async def fetch_series(self, matchers: List[LabelMatcher],
                          start: int, end: int) -> List[TimeSeries]:
        """Fetch time series from storage and ingesters"""
        # Query persistent storage
        storage_results = await self.storage.query(matchers, start, end)

        # Query ingesters for recent data
        ingester_results = []
        for ingester in self.ingesters:
            results = await ingester.query(matchers, start, end)
            ingester_results.extend(results)

        # Merge and deduplicate
        all_results = storage_results + ingester_results
        return self.merge_and_deduplicate(all_results)

    def aggregate(self, series: List[TimeSeries], agg_func: str,
                 grouping: List[str]) -> List[TimeSeries]:
        """
        Aggregate time series by grouping labels
        Example: sum(cpu_usage) by (datacenter)
        """
        # Group series by grouping labels
        groups = defaultdict(list)

        for s in series:
            # Extract grouping key
            key = tuple((label, s.labels[label])
                       for label in grouping if label in s.labels)
            groups[key].append(s)

        # Aggregate each group
        results = []
        for key, group_series in groups.items():
            aggregated = self.apply_aggregation(group_series, agg_func)
            # Set labels from grouping key
            aggregated.labels = dict(key)
            results.append(aggregated)

        return results

    def apply_aggregation(self, series: List[TimeSeries], agg_func: str) -> TimeSeries:
        """Apply aggregation function to series"""
        # Align timestamps
        all_timestamps = sorted(set(
            s.timestamp for ts in series for s in ts.samples
        ))

        aggregated_samples = []

        for timestamp in all_timestamps:
            # Get values at this timestamp
            values = []
            for ts in series:
                for sample in ts.samples:
                    if sample.timestamp == timestamp:
                        values.append(sample.value)
                        break

            if not values:
                continue

            # Apply aggregation
            if agg_func == 'sum':
                agg_value = sum(values)
            elif agg_func == 'avg':
                agg_value = sum(values) / len(values)
            elif agg_func == 'max':
                agg_value = max(values)
            elif agg_func == 'min':
                agg_value = min(values)
            elif agg_func == 'count':
                agg_value = len(values)

            aggregated_samples.append(Sample(timestamp, agg_value))

        return TimeSeries(labels={}, samples=aggregated_samples)
```

### Alert Manager

**Rule Evaluation and Notification**

```python
class AlertManager:
    def __init__(self, query_engine: QueryEngine):
        self.query_engine = query_engine
        self.rules = []
        self.active_alerts = {}  # alert_id -> Alert
        self.silences = []
        self.notification_queue = asyncio.Queue()

    async def evaluation_loop(self, interval: int = 15):
        """Periodically evaluate alert rules"""
        while True:
            await self.evaluate_rules()
            await asyncio.sleep(interval)

    async def evaluate_rules(self):
        """Evaluate all alert rules"""
        for rule in self.rules:
            await self.evaluate_rule(rule)

    async def evaluate_rule(self, rule: AlertRule):
        """Evaluate single alert rule"""
        # Execute query
        result = await self.query_engine.execute_query(
            rule.query,
            time=int(time.time())
        )

        # Check if alert should fire
        for series in result.series:
            value = series.samples[0].value if series.samples else None

            if value is None:
                continue

            # Check threshold
            should_fire = self.check_threshold(value, rule.threshold, rule.comparator)

            alert_id = self.generate_alert_id(rule, series.labels)

            if should_fire:
                # Alert firing
                if alert_id not in self.active_alerts:
                    # New alert
                    alert = Alert(
                        id=alert_id,
                        rule=rule.name,
                        labels=series.labels,
                        value=value,
                        started_at=time.time(),
                        state='firing'
                    )
                    self.active_alerts[alert_id] = alert

                    # Send notification
                    await self.send_notification(alert)
                else:
                    # Update existing alert
                    self.active_alerts[alert_id].value = value

            else:
                # Alert resolved
                if alert_id in self.active_alerts:
                    alert = self.active_alerts[alert_id]
                    alert.state = 'resolved'
                    alert.ended_at = time.time()

                    # Send resolution notification
                    await self.send_notification(alert)

                    # Remove from active alerts
                    del self.active_alerts[alert_id]

    def check_threshold(self, value: float, threshold: float, comparator: str) -> bool:
        """Check if value meets threshold condition"""
        if comparator == '>':
            return value > threshold
        elif comparator == '>=':
            return value >= threshold
        elif comparator == '<':
            return value < threshold
        elif comparator == '<=':
            return value <= threshold
        elif comparator == '==':
            return value == threshold
        elif comparator == '!=':
            return value != threshold
        return False

    async def send_notification(self, alert: Alert):
        """Send alert notification"""
        # Check if alert is silenced
        if self.is_silenced(alert):
            return

        # Add to notification queue
        await self.notification_queue.put(alert)

    async def notification_worker(self):
        """Process notification queue"""
        while True:
            alert = await self.notification_queue.get()

            # Send to configured channels
            await self.send_to_slack(alert)
            await self.send_to_pagerduty(alert)
            await self.send_email(alert)

    def is_silenced(self, alert: Alert) -> bool:
        """Check if alert matches any silence rules"""
        for silence in self.silences:
            if self.matches_silence(alert, silence):
                return True
        return False
```

## 7. Data Structures & Storage

### Time Series Storage Format

```
Block Structure (2-hour blocks):
block_<start_timestamp>_<end_timestamp>/
├── meta.json          # Block metadata
├── index              # Series index
├── chunks/            # Compressed time series chunks
│   ├── 000001
│   ├── 000002
│   └── ...
└── tombstones         # Deleted series

Chunk Format (compressed):
┌────────────────────────┐
│ Series ID (8 bytes)    │
├────────────────────────┤
│ Min Time (8 bytes)     │
├────────────────────────┤
│ Max Time (8 bytes)     │
├────────────────────────┤
│ Samples Count (4 bytes)│
├────────────────────────┤
│ Timestamps (compressed)│
│ - Delta-of-delta       │
│ - Variable encoding    │
├────────────────────────┤
│ Values (compressed)    │
│ - XOR encoding         │
│ - Gorilla algorithm    │
└────────────────────────┘
```

### Indexing Structure

```python
# Postings list for efficient label queries
posting_offsets = {
    'cpu_usage': 0x1000,
    'memory_usage': 0x2000,
    ...
}

# Label values posting lists
label_postings = {
    ('__name__', 'cpu_usage'): [1, 5, 10, 15, ...],  # Series IDs
    ('host', 'server1'): [1, 2, 3],
    ('host', 'server2'): [4, 5, 6],
    ...
}
```

## 8. Fault Tolerance & High Availability

### Replication

```python
# Write metrics to multiple ingesters
replication_factor = 3
quorum_writes = 2  # Write succeeds if 2/3 replicas confirm

# Read from any available replica
# If replica is down, try next replica
```

### Data Durability

```python
# Write-Ahead Log (WAL) for ingesters
class WriteAheadLog:
    def append(self, series_id: int, samples: List[Sample]):
        """Append to WAL before acknowledging write"""
        entry = WALEntry(series_id=series_id, samples=samples)
        self.log_file.write(entry.serialize())
        self.log_file.flush()
        os.fsync(self.log_file.fileno())

    def replay(self):
        """Replay WAL after crash"""
        for entry in self.read_log():
            self.restore_samples(entry)
```

### Graceful Degradation

```python
# If storage is unavailable, continue accepting writes to WAL
# Return partial results if some blocks are unavailable
# Cache query results to reduce load during incidents
```

## 9. Monitoring & Observability

### System Metrics

```python
# Ingestion metrics
metrics_received_total = Counter('metrics_received_total')
metrics_ingested_total = Counter('metrics_ingested_total')
ingestion_latency = Histogram('ingestion_latency_seconds')

# Query metrics
queries_total = Counter('queries_total', labels=['status'])
query_latency = Histogram('query_latency_seconds')
query_samples_processed = Histogram('query_samples_processed')

# Storage metrics
blocks_total = Gauge('blocks_total')
series_total = Gauge('series_total')
samples_total = Counter('samples_total')
compactions_total = Counter('compactions_total')

# System health
up = Gauge('up')  # 1 if healthy, 0 if down
```

## 10. Scalability

### Horizontal Scaling

- Add more ingesters for higher write throughput
- Add more query nodes for higher query load
- Shard metrics across ingesters using consistent hashing
- Use object storage for unlimited retention capacity

### Vertical Scaling

- Increase memory for larger active dataset
- Use SSDs for faster disk I/O
- More CPU cores for parallel query execution

## 11. Trade-offs

### Pull vs Push
- **Pull (Prometheus)**: Service discovery, simpler clients, no push gateway needed
- **Push (StatsD)**: Better for ephemeral jobs, firewall-friendly

### Storage Duration
- **Long retention**: Higher storage costs, slower queries
- **Short retention**: Lower costs, may miss historical patterns

### Cardinality
- **High cardinality**: More detailed metrics, higher resource usage
- **Low cardinality**: Lower overhead, less granular data

## 12. Follow-up Questions

1. How would you handle high-cardinality metrics?
2. How would you implement downsampling for older data?
3. How would you detect anomalies automatically?
4. How would you implement multi-tenancy with strong isolation?
5. How would you handle metric federation across datacenters?
6. How would you implement alerting on missing metrics (deadman switch)?
7. How would you optimize queries for large time ranges?
8. How would you implement metric forwarding/aggregation?
9. How would you handle time series with irregular intervals?
10. How would you implement recording rules for pre-computed metrics?
