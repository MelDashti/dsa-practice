# Design Kafka - Distributed Message Queue

## 1. Problem Statement

Design a distributed message queue system similar to Apache Kafka that can handle high-throughput, fault-tolerant, and scalable publish-subscribe messaging. The system should support multiple producers publishing messages to topics and multiple consumers reading messages in a distributed and reliable manner.

## 2. Requirements

### Functional Requirements
- **Publish messages**: Producers can publish messages to topics
- **Subscribe to topics**: Consumers can subscribe and read messages from topics
- **Topic partitioning**: Topics are divided into partitions for parallelism
- **Message ordering**: Maintain order within a partition
- **Consumer groups**: Multiple consumers can form groups for parallel processing
- **Message retention**: Store messages for configurable retention period
- **Offset management**: Track consumer read positions

### Non-Functional Requirements
- **High throughput**: Handle millions of messages per second
- **Low latency**: Sub-10ms publish latency
- **Scalability**: Horizontal scaling for brokers and partitions
- **Durability**: Messages persisted to disk, no data loss
- **Fault tolerance**: Continue operating despite broker failures
- **High availability**: 99.99% uptime
- **Message delivery**: At-least-once delivery guarantees

### Out of Scope
- Exactly-once semantics (basic version)
- Stream processing (Kafka Streams)
- Schema registry
- Complex message transformations
- Multi-datacenter replication

## 3. Capacity Estimation

### Scale Assumptions
- 1 million messages per second (peak)
- Average message size: 1 KB
- 100 topics with 10 partitions each = 1000 partitions
- 7-day message retention
- 1000 producer clients
- 5000 consumer clients in 100 consumer groups

### Storage Estimation
```
Messages per day = 1M msg/sec × 86,400 sec = 86.4B messages/day
Data per day = 86.4B × 1 KB = 86.4 TB/day
7-day retention = 86.4 TB × 7 = 604.8 TB ≈ 600 TB

With 3x replication = 1800 TB
Number of brokers (10TB each) = 180 brokers
```

### Memory Estimation
```
Page cache per broker = 128 GB
ZooKeeper metadata = 10 GB
Consumer offset storage = 5 GB
Total memory per broker = ~140 GB
```

### Bandwidth Estimation
```
Write throughput = 1M msg/sec × 1 KB = 1 GB/sec
Replication traffic = 1 GB/sec × 2 (2 replicas) = 2 GB/sec
Read throughput = 1 GB/sec × 2 (avg 2 consumers per partition) = 2 GB/sec
Total bandwidth = 5 GB/sec = 40 Gbps
Per broker (180 brokers) = 222 Mbps
```

## 4. High-Level Design

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Producer 1 │  │  Producer 2 │  │  Producer N │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        │ Publish
                        ▼
            ┌───────────────────────┐
            │   Load Balancer       │
            └───────────┬───────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Broker 1│    │ Broker 2│    │ Broker 3│
   │         │◄──►│         │◄──►│         │  Replication
   └────┬────┘    └────┬────┘    └────┬────┘
        │              │              │
        │  ┌───────────┴───────────┐  │
        │  │                       │  │
        ▼  ▼                       ▼  ▼
   Topic A (P0, P1, P2)      Topic B (P0, P1)
        │                           │
        │                           │
        ▼                           ▼
   ┌─────────────┐            ┌─────────────┐
   │ Consumer    │            │ Consumer    │
   │ Group 1     │            │ Group 2     │
   │ ┌─────────┐ │            │ ┌─────────┐ │
   │ │Consumer1│ │            │ │Consumer1│ │
   │ │Consumer2│ │            │ │Consumer2│ │
   │ └─────────┘ │            │ └─────────┘ │
   └─────────────┘            └─────────────┘

   ┌─────────────────────┐
   │   ZooKeeper         │  (Metadata & Coordination)
   │   Cluster           │
   └─────────────────────┘
```

### Core Components
1. **Broker**: Server that stores and serves messages
2. **Topic**: Logical channel for messages
3. **Partition**: Physical subdivision of a topic for parallelism
4. **Producer**: Client that publishes messages
5. **Consumer**: Client that reads messages
6. **Consumer Group**: Set of consumers working together
7. **ZooKeeper**: Coordination service for cluster management

## 5. API Design

### Producer API

```java
// Initialize producer
Properties props = new Properties();
props.put("bootstrap.servers", "broker1:9092,broker2:9092");
props.put("key.serializer", "StringSerializer");
props.put("value.serializer", "StringSerializer");
props.put("acks", "all");  // Wait for all replicas
KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// Synchronous send
ProducerRecord<String, String> record =
    new ProducerRecord<>("topic-name", "key", "value");
RecordMetadata metadata = producer.send(record).get();
// Returns: partition, offset, timestamp

// Asynchronous send with callback
producer.send(record, new Callback() {
    public void onCompletion(RecordMetadata metadata, Exception e) {
        if (e != null) {
            // Handle error
        }
    }
});
```

### Consumer API

```java
// Initialize consumer
Properties props = new Properties();
props.put("bootstrap.servers", "broker1:9092,broker2:9092");
props.put("group.id", "consumer-group-1");
props.put("key.deserializer", "StringDeserializer");
props.put("value.deserializer", "StringDeserializer");
props.put("auto.offset.reset", "earliest");
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);

// Subscribe to topics
consumer.subscribe(Arrays.asList("topic1", "topic2"));

// Poll for messages
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("offset = %d, key = %s, value = %s%n",
                         record.offset(), record.key(), record.value());
    }
    // Commit offsets
    consumer.commitSync();
}
```

### Admin API

```java
// Create topic
AdminClient admin = AdminClient.create(props);
NewTopic newTopic = new NewTopic("topic-name", 10, (short) 3);
// 10 partitions, replication factor 3
admin.createTopics(Collections.singleton(newTopic));

// List topics
ListTopicsResult topics = admin.listTopics();

// Describe topic
DescribeTopicsResult description = admin.describeTopics(Collections.singleton("topic-name"));

// Delete topic
admin.deleteTopics(Collections.singleton("topic-name"));
```

## 6. Component Design

### Partition Structure

**Log-Structured Storage**
```
Partition Directory:
topic-0/
├── 00000000000000000000.log  (segment file)
├── 00000000000000000000.index (offset index)
├── 00000000000000000000.timeindex (timestamp index)
├── 00000000000001000000.log
├── 00000000000001000000.index
└── 00000000000001000000.timeindex

Each segment:
- Max size: 1 GB
- Messages are appended sequentially
- Immutable once written
```

**Message Format**
```
┌──────────────────────────────────────┐
│ Offset (8 bytes)                     │
├──────────────────────────────────────┤
│ Message Size (4 bytes)               │
├──────────────────────────────────────┤
│ CRC (4 bytes)                        │
├──────────────────────────────────────┤
│ Magic Byte (1 byte)                  │
├──────────────────────────────────────┤
│ Attributes (1 byte)                  │
├──────────────────────────────────────┤
│ Timestamp (8 bytes)                  │
├──────────────────────────────────────┤
│ Key Length (4 bytes)                 │
├──────────────────────────────────────┤
│ Key (variable)                       │
├──────────────────────────────────────┤
│ Value Length (4 bytes)               │
├──────────────────────────────────────┤
│ Value (variable)                     │
└──────────────────────────────────────┘
```

### Producer Write Path

**Algorithm**: Batch and compress messages for efficiency
```python
class Producer:
    def __init__(self):
        self.batch_buffer = {}  # partition -> list of messages
        self.batch_size = 16 * 1024  # 16 KB
        self.linger_ms = 10  # Wait up to 10ms to batch

    def send(self, topic, key, value):
        # 1. Select partition
        partition = self.get_partition(topic, key)

        # 2. Add to batch buffer
        message = self.serialize(key, value)
        self.batch_buffer[partition].append(message)

        # 3. Send if batch is full or linger time expired
        if self.should_send_batch(partition):
            self.send_batch(partition)

    def get_partition(self, topic, key):
        if key is not None:
            # Hash-based partitioning for same key
            return hash(key) % self.partition_count[topic]
        else:
            # Round-robin for null keys
            return self.next_partition[topic]

    def send_batch(self, partition):
        messages = self.batch_buffer[partition]

        # Compress batch
        compressed = self.compress(messages)

        # Send to leader broker
        leader = self.metadata.get_leader(partition)
        response = self.send_to_broker(leader, compressed)

        if response.error:
            self.handle_error(response.error, partition)
        else:
            self.handle_success(response.offset)

        # Clear batch
        self.batch_buffer[partition] = []
```

**Time Complexity**: O(1) for adding to batch, O(n) for compression
**Space Complexity**: O(b) where b is batch size

### Broker Write Path

**Algorithm**: Sequential writes to append-only log
```python
class Broker:
    def handle_produce_request(self, request):
        partition_results = []

        for partition, messages in request.messages.items():
            try:
                # 1. Validate request
                self.validate_partition_leader(partition)

                # 2. Append to log
                offset = self.append_to_log(partition, messages)

                # 3. Replicate to followers (if acks=all)
                if request.acks == 'all':
                    self.wait_for_replicas(partition, offset)

                # 4. Update high watermark
                self.update_high_watermark(partition)

                partition_results.append(
                    PartitionResult(partition, offset, None)
                )

            except Exception as e:
                partition_results.append(
                    PartitionResult(partition, -1, e)
                )

        return ProduceResponse(partition_results)

    def append_to_log(self, partition, messages):
        log = self.partition_logs[partition]

        # Get current offset
        current_offset = log.get_next_offset()

        # Assign offsets to messages
        for i, message in enumerate(messages):
            message.offset = current_offset + i

        # Write to active segment
        segment = log.get_active_segment()
        file_position = segment.append(messages)

        # Update index
        segment.index.add_entry(current_offset, file_position)

        # Flush to disk (OS page cache)
        if self.should_flush():
            segment.flush()

        return current_offset
```

**Write Throughput**: Sequential writes ~100-200 MB/sec per disk

### Consumer Read Path

**Algorithm**: Sequential reads from committed log
```python
class Consumer:
    def __init__(self, group_id):
        self.group_id = group_id
        self.assigned_partitions = []
        self.current_offsets = {}  # partition -> offset

    def poll(self, timeout_ms):
        records = []

        for partition in self.assigned_partitions:
            # 1. Get current offset for partition
            offset = self.get_offset(partition)

            # 2. Fetch from broker
            fetch_request = FetchRequest(partition, offset, max_bytes=1MB)
            response = self.send_to_broker(partition.leader, fetch_request)

            # 3. Process fetched records
            for record in response.records:
                records.append(record)

            # 4. Update offset (but don't commit yet)
            if response.records:
                last_offset = response.records[-1].offset
                self.current_offsets[partition] = last_offset + 1

        return records

    def commit_sync(self):
        # Commit current offsets to Kafka
        for partition, offset in self.current_offsets.items():
            self.commit_offset(partition, offset)

    def commit_offset(self, partition, offset):
        # Write to __consumer_offsets topic
        request = OffsetCommitRequest(
            group_id=self.group_id,
            partition=partition,
            offset=offset
        )
        self.send_to_coordinator(request)
```

### Consumer Group Coordination

**Algorithm**: Rebalance protocol with generation IDs
```python
class GroupCoordinator:
    def __init__(self):
        self.consumer_groups = {}  # group_id -> GroupMetadata
        self.lock = threading.Lock()

    def join_group(self, group_id, consumer_id, topics):
        with self.lock:
            group = self.get_or_create_group(group_id)

            # Add consumer to group
            group.add_member(consumer_id, topics)

            # Trigger rebalance if needed
            if not group.is_stable():
                self.trigger_rebalance(group)
                group.state = 'REBALANCING'

            # Wait for rebalance to complete
            while group.state == 'REBALANCING':
                time.sleep(0.1)

            # Return partition assignment
            return JoinGroupResponse(
                generation_id=group.generation,
                member_id=consumer_id,
                leader_id=group.leader,
                members=group.members
            )

    def trigger_rebalance(self, group):
        # Increment generation
        group.generation += 1

        # Get all partitions for subscribed topics
        all_partitions = self.get_partitions(group.topics)

        # Assign partitions using strategy (e.g., range, round-robin)
        assignments = self.assign_partitions(
            all_partitions,
            group.members,
            strategy='range'
        )

        # Update assignments
        group.assignments = assignments
        group.state = 'STABLE'

    def assign_partitions(self, partitions, consumers, strategy):
        if strategy == 'range':
            return self.range_assignment(partitions, consumers)
        elif strategy == 'round-robin':
            return self.round_robin_assignment(partitions, consumers)

    def range_assignment(self, partitions, consumers):
        """
        Range strategy: Assign contiguous partition ranges
        Example: 10 partitions, 3 consumers
        Consumer 1: [0, 1, 2, 3]
        Consumer 2: [4, 5, 6]
        Consumer 3: [7, 8, 9]
        """
        assignments = {}
        consumers_list = sorted(consumers)
        partitions_list = sorted(partitions)

        partitions_per_consumer = len(partitions_list) // len(consumers_list)
        extra = len(partitions_list) % len(consumers_list)

        start = 0
        for i, consumer in enumerate(consumers_list):
            count = partitions_per_consumer + (1 if i < extra else 0)
            assignments[consumer] = partitions_list[start:start + count]
            start += count

        return assignments
```

### Replication Protocol

**Algorithm**: Leader-Follower with ISR (In-Sync Replicas)
```python
class ReplicationManager:
    def __init__(self):
        self.isr = {}  # partition -> set of in-sync replica brokers
        self.hw = {}   # partition -> high watermark offset
        self.leo = {}  # (partition, broker) -> log end offset

    def replicate_messages(self, partition, messages, leader_offset):
        # Followers fetch from leader
        for follower in self.get_followers(partition):
            try:
                # Follower sends fetch request
                response = follower.fetch(partition, follower_offset)

                # Update follower's LEO
                self.leo[(partition, follower)] = follower_offset + len(messages)

                # Check if follower is in-sync
                if self.is_in_sync(partition, follower):
                    self.isr[partition].add(follower)
                else:
                    self.isr[partition].discard(follower)

            except Exception as e:
                # Remove follower from ISR on failure
                self.isr[partition].discard(follower)

        # Update high watermark (min LEO of ISR)
        self.update_high_watermark(partition)

    def is_in_sync(self, partition, broker):
        leader_leo = self.leo[(partition, 'leader')]
        follower_leo = self.leo.get((partition, broker), 0)

        # Follower is in-sync if within replica.lag.max.messages
        lag = leader_leo - follower_leo
        return lag <= self.replica_lag_max

    def update_high_watermark(self, partition):
        # High watermark = min LEO among ISR members
        isr_leos = [
            self.leo.get((partition, broker), 0)
            for broker in self.isr[partition]
        ]
        self.hw[partition] = min(isr_leos) if isr_leos else 0
```

### Offset Management

**Storage**: Internal topic `__consumer_offsets`
```python
class OffsetManager:
    def __init__(self):
        self.offset_topic = "__consumer_offsets"
        self.offset_cache = {}  # (group, partition) -> offset

    def commit_offset(self, group_id, partition, offset):
        # Hash group_id to determine offset partition
        offset_partition = hash(group_id) % self.offset_partitions

        # Create offset commit message
        key = f"{group_id}:{partition.topic}:{partition.id}"
        value = {
            'offset': offset,
            'metadata': '',
            'timestamp': time.time()
        }

        # Write to __consumer_offsets topic
        self.produce(
            topic=self.offset_topic,
            partition=offset_partition,
            key=key,
            value=value
        )

        # Update cache
        self.offset_cache[(group_id, partition)] = offset

    def fetch_offset(self, group_id, partition):
        # Check cache first
        key = (group_id, partition)
        if key in self.offset_cache:
            return self.offset_cache[key]

        # Read from __consumer_offsets topic
        offset_partition = hash(group_id) % self.offset_partitions
        records = self.consume(
            topic=self.offset_topic,
            partition=offset_partition,
            key=f"{group_id}:{partition.topic}:{partition.id}"
        )

        # Return latest offset
        if records:
            return records[-1].value['offset']
        return None
```

## 7. Data Structures & Storage

### Log Segment Structure

```python
class LogSegment:
    def __init__(self, base_offset, log_dir):
        self.base_offset = base_offset
        self.log_file = open(f"{log_dir}/{base_offset:020d}.log", "ab+")
        self.index_file = open(f"{log_dir}/{base_offset:020d}.index", "ab+")
        self.size = 0
        self.index = OffsetIndex()

    def append(self, messages):
        """Append messages to log segment"""
        position = self.log_file.tell()

        # Write messages
        for message in messages:
            self.log_file.write(message.serialize())

        # Update index (sparse)
        if self.should_add_index_entry():
            self.index.add_entry(
                offset=messages[0].offset,
                position=position
            )

        self.size += len(messages)
        return position

    def read(self, start_offset, max_bytes):
        """Read messages from offset"""
        # Look up position in index
        position = self.index.lookup(start_offset)

        # Seek to position
        self.log_file.seek(position)

        # Read messages
        messages = []
        bytes_read = 0

        while bytes_read < max_bytes:
            message = self.read_message()
            if message is None:
                break
            messages.append(message)
            bytes_read += message.size

        return messages
```

### Offset Index Structure

**Sparse Index for Fast Lookup**
```python
class OffsetIndex:
    """
    Sparse index mapping offsets to file positions
    Index entry every 4KB of log data
    """
    def __init__(self):
        self.entries = []  # List of (offset, position) tuples
        self.entry_size = 8  # 4 bytes offset + 4 bytes position

    def add_entry(self, offset, position):
        """Add index entry (offset -> file position)"""
        self.entries.append((offset, position))

    def lookup(self, target_offset):
        """
        Binary search to find largest offset <= target
        Returns file position to start reading
        """
        left, right = 0, len(self.entries) - 1

        while left <= right:
            mid = (left + right) // 2
            offset, position = self.entries[mid]

            if offset == target_offset:
                return position
            elif offset < target_offset:
                left = mid + 1
            else:
                right = mid - 1

        # Return position of largest offset <= target
        if right >= 0:
            return self.entries[right][1]
        return 0
```

**Time Complexity**: O(log n) for lookup
**Space Complexity**: 8 bytes per entry, ~8 MB per 1M entries

### Metadata Storage (ZooKeeper)

```
ZooKeeper Structure:
/brokers
  /ids
    /0 -> {"host": "broker1", "port": 9092}
    /1 -> {"host": "broker2", "port": 9092}
  /topics
    /topic-A
      /partitions
        /0
          /state -> {"leader": 1, "isr": [1, 2, 3]}
        /1
          /state -> {"leader": 2, "isr": [2, 3, 1]}
/consumers
  /group-1
    /ids
      /consumer-1 -> {"subscription": ["topic-A"]}
    /offsets
      /topic-A
        /0 -> 12345
/controller
  -> {"brokerid": 1, "timestamp": 1234567890}
```

## 8. Fault Tolerance & High Availability

### Broker Failure Handling

**Scenario 1: Follower Broker Fails**
```python
def handle_follower_failure(partition, failed_broker):
    # 1. Remove from ISR
    isr = get_isr(partition)
    isr.remove(failed_broker)
    update_isr(partition, isr)

    # 2. Update high watermark
    update_high_watermark(partition)

    # 3. Log failure
    log.warning(f"Follower {failed_broker} removed from ISR for {partition}")

    # System continues with remaining replicas
```

**Scenario 2: Leader Broker Fails**
```python
def handle_leader_failure(partition):
    # 1. Controller detects leader failure (via ZooKeeper)
    controller = get_controller()

    # 2. Select new leader from ISR
    isr = get_isr(partition)
    if not isr:
        # No ISR available, choose from all replicas (data loss risk)
        isr = get_all_replicas(partition)

    new_leader = select_leader(isr)  # Choose highest LEO

    # 3. Update metadata in ZooKeeper
    update_leader(partition, new_leader)
    update_isr(partition, [new_leader])

    # 4. Notify producers and consumers
    send_metadata_update(partition, new_leader)

    # 5. New leader starts accepting writes
    log.info(f"New leader {new_leader} elected for {partition}")
```

**Election Time**: Typically <1 second

### Replication Strategies

**min.insync.replicas**
```python
class Producer:
    def send_with_acks(self, message, acks='all'):
        if acks == 'all':
            # Wait for all ISR replicas to acknowledge
            required_acks = len(get_isr(partition))
            min_isr = get_config('min.insync.replicas')  # e.g., 2

            if required_acks < min_isr:
                raise NotEnoughReplicasException(
                    f"Only {required_acks} in ISR, need {min_isr}"
                )

            # Send and wait for ISR acks
            self.send_and_wait(message, required_acks)
        elif acks == 1:
            # Wait only for leader
            self.send_and_wait(message, 1)
        else:  # acks == 0
            # Fire and forget
            self.send_async(message)
```

### Data Durability

**Flushing Strategy**
```python
class LogManager:
    def __init__(self):
        self.flush_messages = 10000  # Flush every 10K messages
        self.flush_interval_ms = 1000  # Or every 1 second
        self.messages_since_flush = 0
        self.last_flush_time = time.time()

    def append(self, messages):
        # Write to OS page cache
        self.log_file.write(messages)
        self.messages_since_flush += len(messages)

        # Flush if needed
        if self.should_flush():
            self.flush()

    def should_flush(self):
        return (
            self.messages_since_flush >= self.flush_messages or
            (time.time() - self.last_flush_time) >= self.flush_interval_ms / 1000
        )

    def flush(self):
        # Force write to disk
        self.log_file.flush()
        os.fsync(self.log_file.fileno())
        self.messages_since_flush = 0
        self.last_flush_time = time.time()
```

### Consumer Failure Handling

**Rebalancing on Consumer Failure**
```python
class ConsumerGroup:
    def handle_consumer_failure(self, consumer_id):
        # 1. Detect failure (heartbeat timeout)
        if not self.is_alive(consumer_id):
            log.info(f"Consumer {consumer_id} failed")

            # 2. Remove from group
            self.members.remove(consumer_id)

            # 3. Trigger rebalance
            self.trigger_rebalance()

            # 4. Remaining consumers get reassigned partitions
            # Partitions from failed consumer are redistributed

    def heartbeat_check(self):
        while True:
            time.sleep(1)
            for consumer_id in self.members:
                last_heartbeat = self.last_heartbeat_time[consumer_id]
                if time.time() - last_heartbeat > self.session_timeout:
                    self.handle_consumer_failure(consumer_id)
```

## 9. Monitoring & Observability

### Key Metrics

**Broker Metrics**
```python
class BrokerMetrics:
    # Throughput
    messages_in_per_sec = Counter()
    bytes_in_per_sec = Counter()
    messages_out_per_sec = Counter()
    bytes_out_per_sec = Counter()

    # Latency
    produce_request_latency_ms = Histogram()  # p50, p99, p999
    fetch_request_latency_ms = Histogram()

    # Replication
    under_replicated_partitions = Gauge()  # ISR < replicas
    offline_partitions = Gauge()  # No leader

    # Resource utilization
    network_io_rate = Gauge()
    disk_io_rate = Gauge()
    page_cache_hit_ratio = Gauge()

    # Errors
    failed_produce_requests = Counter()
    failed_fetch_requests = Counter()
```

**Producer Metrics**
```python
class ProducerMetrics:
    record_send_rate = Counter()
    record_error_rate = Counter()
    record_retry_rate = Counter()
    request_latency_avg = Gauge()
    request_latency_max = Gauge()
    batch_size_avg = Gauge()
    compression_rate_avg = Gauge()
```

**Consumer Metrics**
```python
class ConsumerMetrics:
    records_consumed_rate = Counter()
    bytes_consumed_rate = Counter()
    fetch_latency_avg = Gauge()
    commit_latency_avg = Gauge()

    # Lag metrics (critical)
    records_lag = Gauge()  # Current offset - committed offset
    records_lag_max = Gauge()  # Max lag across partitions

    # Rebalancing
    rebalance_count = Counter()
    rebalance_latency_avg = Gauge()
```

### Alerting Rules

```yaml
alerts:
  - name: HighConsumerLag
    condition: records_lag > 100000
    severity: warning
    description: "Consumer is lagging behind by >100K messages"

  - name: UnderReplicatedPartitions
    condition: under_replicated_partitions > 0
    severity: critical
    description: "Some partitions have fewer than required replicas"

  - name: OfflinePartitions
    condition: offline_partitions > 0
    severity: critical
    description: "Some partitions have no leader"

  - name: HighProduceLatency
    condition: produce_request_latency_p99 > 100ms
    severity: warning
    description: "99th percentile produce latency >100ms"

  - name: BrokerDown
    condition: broker_status == down
    severity: critical
    description: "Broker is not responding"
```

### Logging Strategy

```python
# Structured logging
logger.info("Message produced", extra={
    'topic': topic,
    'partition': partition,
    'offset': offset,
    'size_bytes': len(message),
    'latency_ms': latency
})

logger.error("Replication failed", extra={
    'partition': partition,
    'follower': follower_id,
    'error': str(error)
})

# Audit logging
audit_logger.info("Consumer group rebalanced", extra={
    'group_id': group_id,
    'generation': generation_id,
    'members': member_ids,
    'assignments': partition_assignments
})
```

## 10. Scalability

### Horizontal Scaling

**Adding Brokers**
```python
def scale_out_brokers(new_broker_count):
    # 1. Start new broker instances
    for i in range(new_broker_count):
        broker = start_broker(config)

        # 2. Register with ZooKeeper
        register_broker(broker.id, broker.host, broker.port)

    # 3. Reassign partitions to balance load
    reassign_partitions(get_all_brokers())

    # 4. Replicate data to new brokers
    trigger_replication()
```

**Partition Reassignment**
```json
{
  "version": 1,
  "partitions": [
    {
      "topic": "topic-A",
      "partition": 0,
      "replicas": [1, 2, 3],
      "new_replicas": [1, 2, 4]
    }
  ]
}
```

### Adding Partitions

```python
def increase_partition_count(topic, new_count):
    current_count = get_partition_count(topic)

    if new_count <= current_count:
        raise ValueError("Can only increase partition count")

    # Create new partitions
    for partition_id in range(current_count, new_count):
        # Select brokers for replicas
        brokers = select_brokers(replication_factor)

        # Create partition
        create_partition(topic, partition_id, brokers)

        # Initialize log segments
        for broker in brokers:
            initialize_log(broker, topic, partition_id)

    # Update metadata
    update_partition_count(topic, new_count)

    # Trigger consumer rebalance (partition assignment changes)
    notify_consumers(topic)
```

**Note**: Cannot decrease partition count (limitation)

### Performance Optimization

**Zero-Copy Transfer**
```python
# Use sendfile() for efficient data transfer
# Avoids copying data between kernel and user space

def send_messages_to_consumer(socket, log_file, offset, length):
    # Traditional approach (4 copies):
    # 1. Disk -> kernel buffer
    # 2. Kernel buffer -> user space
    # 3. User space -> kernel socket buffer
    # 4. Kernel socket buffer -> NIC

    # Zero-copy approach (2 copies):
    # 1. Disk -> kernel buffer
    # 2. Kernel buffer -> NIC
    os.sendfile(socket.fileno(), log_file.fileno(), offset, length)
```

**Batching and Compression**
```python
class ProducerOptimizations:
    # Batch size: 16KB default
    batch_size = 16 * 1024

    # Linger time: Wait up to 10ms to fill batch
    linger_ms = 10

    # Compression: GZIP, Snappy, LZ4, ZSTD
    compression_type = 'lz4'  # Best balance of speed/ratio

    # Results:
    # - 10x throughput improvement from batching
    # - 50% bandwidth reduction from compression
    # - <10ms latency overhead
```

### Bottleneck Analysis

**Disk I/O Bottleneck**
```
Solution:
1. Use SSDs instead of HDDs
2. Use RAID for better IOPS
3. Increase OS page cache (80% of RAM)
4. Optimize segment size
5. Separate log disks from index disks
```

**Network Bottleneck**
```
Solution:
1. Use 10Gbps+ network interfaces
2. Enable compression
3. Increase socket buffer sizes
4. Use multiple NICs
5. Colocate consumers with brokers
```

**CPU Bottleneck**
```
Solution:
1. Use efficient compression (LZ4 > GZIP)
2. Minimize serialization overhead
3. Use batch processing
4. Optimize message format
```

## 11. Trade-offs

### Replication Factor

**RF=3 (Common)**
- Pros: Survives 2 broker failures, good durability
- Cons: 3x storage cost, slower writes (wait for 3 acks)

**RF=2 (Cost-optimized)**
- Pros: 2x storage, faster writes
- Cons: Only survives 1 failure, less durable

**RF=1 (No replication)**
- Pros: Minimal storage, fastest writes
- Cons: Data loss on broker failure

### Acknowledgment Mode

**acks=all (Highest durability)**
- Pros: No data loss (all ISR must ack)
- Cons: Highest latency (~10-20ms)

**acks=1 (Balance)**
- Pros: Leader ack only, faster (~5ms)
- Cons: Data loss if leader fails before replication

**acks=0 (Highest throughput)**
- Pros: Fire and forget, <1ms
- Cons: No guarantee of delivery

### Partition Count

**Many Partitions (100+)**
- Pros: Higher parallelism, better load distribution
- Cons: More memory overhead, slower leader election, more files

**Few Partitions (10-30)**
- Pros: Lower overhead, faster elections
- Cons: Limited parallelism, potential hotspots

### Consumer Offset Storage

**Kafka Topic (__consumer_offsets)**
- Pros: Same durability as messages, integrated
- Cons: Slight overhead, complex implementation

**External Store (ZooKeeper/Redis)**
- Pros: Flexible, can be queried easily
- Cons: Extra dependency, consistency challenges

### Message Ordering

**Partition-level Ordering (Current)**
- Pros: Achievable with high throughput
- Cons: Only within partition, not global

**Global Ordering**
- Pros: Total order across all messages
- Cons: Single partition only, limits throughput

## 12. Follow-up Questions

### Architecture & Design
1. How would you handle exactly-once semantics (idempotent producer + transactional consumer)?
2. How would you implement multi-datacenter replication?
3. How would you design a schema registry for message validation?
4. How would you implement message filtering at the broker level?

### Performance & Scalability
5. How would you optimize for very large messages (>1MB)?
6. How would you handle traffic spikes (10x normal load)?
7. How would you implement tiered storage (hot/cold data)?
8. How would you optimize consumer lag when it's very high?

### Reliability & Operations
9. How would you implement automatic partition rebalancing?
10. How would you handle broker disk failures?
11. How would you upgrade a Kafka cluster with zero downtime?
12. How would you implement quota management (rate limiting per client)?

### Consumer Groups
13. How would you implement static membership (avoid rebalances on restart)?
14. How would you handle a slow consumer affecting the group?
15. How would you implement priority consumers?
16. How would you handle consumer group lag monitoring and alerting?

### Security
17. How would you implement authentication and authorization?
18. How would you encrypt data at rest and in transit?
19. How would you implement audit logging for compliance?
20. How would you handle multi-tenancy and isolation?

### Advanced Features
21. How would you implement stream processing (joins, aggregations)?
22. How would you handle message deduplication?
23. How would you implement message scheduling (delay queues)?
24. How would you support wildcard topic subscriptions efficiently?

### Comparisons
25. Kafka vs RabbitMQ: When to use which?
26. Kafka vs Amazon Kinesis: Trade-offs?
27. Log compaction vs time-based retention: Use cases?
28. Pull-based consumers vs push-based: Pros and cons?
