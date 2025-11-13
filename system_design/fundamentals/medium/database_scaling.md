# Database Scaling: Replication, Sharding, and Partitioning Strategies

## 1. Problem Statement

How do we scale a database to handle increasing data volume, read/write traffic, and maintain high availability? As applications grow, a single database server becomes a bottleneck for performance, storage capacity, and availability. We need strategies to distribute data and load across multiple database instances.

## 2. Requirements

### Functional Requirements
- Support increasing read and write throughput
- Store growing volumes of data
- Provide data redundancy for reliability
- Enable geographic distribution
- Support complex queries across distributed data
- Maintain data consistency where required

### Non-functional Requirements
- **Availability:** 99.99% uptime
- **Read Latency:** <10ms for 95% of queries
- **Write Latency:** <50ms for 95% of writes
- **Consistency:** Configurable (strong vs eventual)
- **Scalability:** Linear scaling with added nodes
- **Fault Tolerance:** Survive multiple node failures

## 3. Capacity Estimation

### Example: Social Media Application

**Data Volume:**
- 100M users
- 10 posts per user average = 1B posts
- Each post: 1 KB metadata + 2 KB content = 3 KB
- Total storage: 1B * 3 KB = 3 TB
- With indexes and overhead: ~6 TB
- Growth rate: 20% per year

**Traffic:**
- Daily Active Users: 30M
- Reads per user per day: 100 (timeline, profiles, posts)
- Total reads: 3B per day = ~35K reads/second
- Writes per user per day: 5 (posts, likes, comments)
- Total writes: 150M per day = ~1,700 writes/second

**Read/Write Ratio:** 35K:1.7K ≈ 20:1 (read-heavy)

**Single Server Limits:**
- Modern DB server: ~10K QPS
- Storage: ~10 TB
- **Conclusion:** Need multiple servers for both throughput and storage

## 4. High-Level Design

### Complete Architecture

```
                        Application Layer
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Read Path              Write Path
                    │                   │
                    ↓                   ↓
            ┌──────────────┐    ┌──────────────┐
            │ Read Routing │    │Write Routing │
            └──────┬───────┘    └──────┬───────┘
                   │                   │
        ┌──────────┼───────────┐      │
        │          │           │      │
        ↓          ↓           ↓      ↓
    ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
    │Replica│ │Replica│ │Replica│ │Primary│
    │  1    │ │  2    │ │  3    │ │Master │
    └───────┘ └───────┘ └───────┘ └───┬───┘
                                       │
                              Replication Log
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                ┌───▼───┐          ┌───▼───┐         ┌───▼───┐
                │Shard 1│          │Shard 2│         │Shard 3│
                │Users  │          │Users  │         │Users  │
                │0-33M  │          │33-66M │         │66-100M│
                └───────┘          └───────┘         └───────┘
```

## 5. API Design

### Replication Management API

```
POST /api/v1/replication/configure
Request: {
  "primary": "db-master-01.example.com:5432",
  "replicas": [
    {"host": "db-replica-01.example.com:5432", "lag_threshold_ms": 1000},
    {"host": "db-replica-02.example.com:5432", "lag_threshold_ms": 1000}
  ],
  "replication_mode": "asynchronous",
  "auto_failover": true
}

GET /api/v1/replication/status
Response: {
  "primary": {
    "host": "db-master-01",
    "status": "healthy",
    "connections": 245,
    "writes_per_second": 1500
  },
  "replicas": [
    {
      "host": "db-replica-01",
      "status": "healthy",
      "replication_lag_ms": 45,
      "last_sync": "2025-11-12T10:30:45Z",
      "reads_per_second": 15000
    }
  ]
}

POST /api/v1/failover/initiate
Request: {
  "new_primary": "db-replica-01.example.com:5432",
  "force": false
}
```

### Sharding Management API

```
POST /api/v1/sharding/configure
Request: {
  "strategy": "range",
  "shard_key": "user_id",
  "shards": [
    {"id": "shard-1", "range": [0, 33333333], "host": "db-shard-01"},
    {"id": "shard-2", "range": [33333334, 66666666], "host": "db-shard-02"},
    {"id": "shard-3", "range": [66666667, 99999999], "host": "db-shard-03"}
  ]
}

GET /api/v1/sharding/locate
Query: ?user_id=12345678
Response: {
  "user_id": 12345678,
  "shard_id": "shard-1",
  "shard_host": "db-shard-01.example.com:5432"
}

POST /api/v1/sharding/rebalance
Request: {
  "source_shard": "shard-1",
  "target_shard": "shard-4",
  "key_range": [25000000, 33333333]
}
```

## 6. Database Schema

### Metadata Tables

```sql
-- Shard mapping table (stored on each shard or in distributed config)
CREATE TABLE shard_mappings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    shard_id VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    key_range_start BIGINT,
    key_range_end BIGINT,
    host VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    status ENUM('active', 'migrating', 'readonly', 'offline') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_table_range (table_name, key_range_start, key_range_end)
);

-- Replication monitoring
CREATE TABLE replication_status (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    primary_host VARCHAR(255),
    replica_host VARCHAR(255),
    replication_lag_ms INT,
    last_log_position BIGINT,
    status ENUM('healthy', 'lagging', 'broken'),
    INDEX idx_timestamp (timestamp),
    INDEX idx_replica (replica_host)
);

-- Example sharded table (on each shard)
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shard_id VARCHAR(50), -- Denormalized for debugging
    INDEX idx_username (username),
    INDEX idx_email (email)
) PARTITION BY RANGE (user_id) (
    PARTITION p0 VALUES LESS THAN (33333333),
    PARTITION p1 VALUES LESS THAN (66666666),
    PARTITION p2 VALUES LESS THAN (99999999),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

## 7. Detailed Component Design

### Replication Strategies

#### 1. Primary-Replica (Master-Slave) Replication

```
                    ┌─────────────┐
                    │   Primary   │
                    │  (Master)   │
                    └──────┬──────┘
                           │
                   Write to WAL
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ↓              ↓              ↓
      ┌──────────┐   ┌──────────┐   ┌──────────┐
      │ Replica1 │   │ Replica2 │   │ Replica3 │
      │  (Slave) │   │  (Slave) │   │  (Slave) │
      └──────────┘   └──────────┘   └──────────┘
```

**Synchronous Replication:**
```python
def write_with_sync_replication(data):
    # Write to primary
    primary_db.write(data)

    # Wait for at least N replicas to confirm
    confirmations = 0
    for replica in replicas:
        try:
            replica.replicate(data, timeout=1000)
            confirmations += 1
            if confirmations >= min_confirmations:
                break
        except TimeoutError:
            log_warning(f"Replica {replica} timed out")

    if confirmations < min_confirmations:
        raise ReplicationError("Insufficient replicas confirmed")

    return True
```

**Characteristics:**
- Strong consistency
- Higher write latency
- Guaranteed durability
- Reduced availability (if replicas down)

**Asynchronous Replication:**
```python
def write_with_async_replication(data):
    # Write to primary
    primary_db.write(data)

    # Queue for replication (non-blocking)
    replication_queue.enqueue(data)

    return True

# Background replication worker
def replication_worker():
    while True:
        data = replication_queue.dequeue()
        for replica in replicas:
            try:
                replica.replicate(data)
            except:
                # Retry later
                replication_queue.enqueue(data, delay=5)
```

**Characteristics:**
- Eventual consistency
- Lower write latency
- Higher availability
- Risk of data loss on primary failure

#### 2. Multi-Primary (Multi-Master) Replication

```
    ┌─────────┐ ←──────→ ┌─────────┐
    │Primary 1│          │Primary 2│
    └────┬────┘          └────┬────┘
         │                    │
         └──────────┬─────────┘
                    ↓
              Conflict Resolution
```

**Conflict Detection:**
```python
class ConflictResolver:
    def resolve_write_conflict(self, version1, version2):
        """Resolve conflict when same record updated on multiple primaries"""

        # Strategy 1: Last Write Wins (LWW)
        if version1.timestamp > version2.timestamp:
            return version1
        else:
            return version2

        # Strategy 2: Vector Clocks
        if self.happens_before(version1.vector_clock, version2.vector_clock):
            return version2
        elif self.happens_before(version2.vector_clock, version1.vector_clock):
            return version1
        else:
            # Concurrent writes - need application-level resolution
            return self.merge_versions(version1, version2)

    def merge_versions(self, v1, v2):
        """Application-specific merge logic"""
        # Example: merge both changes
        merged = {}
        for key in set(v1.data.keys()) | set(v2.data.keys()):
            if key in v1.data and key in v2.data:
                # Both modified - use application logic
                merged[key] = self.resolve_field(v1.data[key], v2.data[key])
            elif key in v1.data:
                merged[key] = v1.data[key]
            else:
                merged[key] = v2.data[key]
        return merged
```

### Sharding Strategies

#### 1. Range-Based Sharding

```python
class RangeSharding:
    def __init__(self, shards):
        # shards = [(range_start, range_end, shard_id), ...]
        self.shards = sorted(shards, key=lambda x: x[0])

    def get_shard(self, key):
        # Binary search for appropriate shard
        for start, end, shard_id in self.shards:
            if start <= key <= end:
                return shard_id
        raise ValueError(f"No shard found for key {key}")

# Example usage
sharding = RangeSharding([
    (0, 33_333_333, "shard-1"),
    (33_333_334, 66_666_666, "shard-2"),
    (66_666_667, 99_999_999, "shard-3")
])

shard_id = sharding.get_shard(user_id=12345678)  # Returns "shard-1"
```

**Advantages:**
- Range queries efficient (often on same shard)
- Simple to understand and implement
- Easy to add new shards for new ranges

**Disadvantages:**
- Uneven distribution (hotspots)
- Requires rebalancing as data grows
- Sequential IDs can cause write hotspots

#### 2. Hash-Based Sharding

```python
import hashlib

class HashSharding:
    def __init__(self, num_shards):
        self.num_shards = num_shards

    def get_shard(self, key):
        # Hash the key and mod by number of shards
        hash_value = int(hashlib.md5(str(key).encode()).hexdigest(), 16)
        shard_id = hash_value % self.num_shards
        return f"shard-{shard_id}"

# Example usage
sharding = HashSharding(num_shards=10)
shard_id = sharding.get_shard(user_id=12345678)
```

**Advantages:**
- Even distribution of data
- No hotspot issues
- Automatic load balancing

**Disadvantages:**
- Range queries span all shards
- Adding shards requires rehashing
- Difficult to rebalance

#### 3. Consistent Hashing

```python
import bisect
import hashlib

class ConsistentHashing:
    def __init__(self, nodes, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []

        for node in nodes:
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = node
            self.sorted_keys.append(hash_value)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)
            del self.ring[hash_value]
            self.sorted_keys.remove(hash_value)

    def get_node(self, key):
        if not self.ring:
            return None

        hash_value = self._hash(key)
        # Find first node >= hash_value
        idx = bisect.bisect_right(self.sorted_keys, hash_value)
        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]
```

**Advantages:**
- Minimal data movement when adding/removing nodes
- Even distribution
- Scales well

**Disadvantages:**
- More complex implementation
- Range queries still span multiple shards

#### 4. Directory-Based Sharding

```python
class DirectorySharding:
    def __init__(self):
        # Maintain a lookup table
        self.directory = {}  # key -> shard_id

    def get_shard(self, key):
        if key in self.directory:
            return self.directory[key]

        # Assign to shard (could use any strategy)
        shard_id = self._assign_shard(key)
        self.directory[key] = shard_id
        return shard_id

    def _assign_shard(self, key):
        # Use least loaded shard
        shard_loads = self._get_shard_loads()
        return min(shard_loads, key=shard_loads.get)

    def migrate_key(self, key, new_shard):
        """Manually move a key to different shard"""
        old_shard = self.directory[key]
        # Migrate data
        data = self._get_data(old_shard, key)
        self._write_data(new_shard, key, data)
        self._delete_data(old_shard, key)
        # Update directory
        self.directory[key] = new_shard
```

**Advantages:**
- Flexible shard assignment
- Can rebalance easily
- Support complex routing logic

**Disadvantages:**
- Directory is single point of failure
- Directory can become bottleneck
- Additional lookup overhead

### Partitioning Strategies

#### 1. Horizontal Partitioning (Sharding)

Splits rows across multiple tables/databases:
```
users_shard1: user_id 0-33M
users_shard2: user_id 33M-66M
users_shard3: user_id 66M-100M
```

#### 2. Vertical Partitioning

Splits columns across multiple tables:
```
users_basic: user_id, username, email
users_profile: user_id, bio, avatar_url, preferences
users_stats: user_id, post_count, follower_count, login_count
```

**Advantages:**
- Reduce row size
- Separate hot and cold data
- Different storage engines for different data types

#### 3. Functional Partitioning

Split by business function:
```
user_database: users, profiles, authentication
content_database: posts, comments, likes
analytics_database: events, metrics, reports
```

## 8. Trade-offs and Considerations

### Consistency Models

#### Strong Consistency
```
Write → Primary → Wait for replicas → Acknowledge
Read → Can read from any replica (all have same data)
```
- **Pros:** Simple programming model, no stale reads
- **Cons:** Higher latency, lower availability

#### Eventual Consistency
```
Write → Primary → Acknowledge immediately
Background: Replicas catch up eventually
Read → Might see stale data
```
- **Pros:** Low latency, high availability
- **Cons:** Complex application logic, stale reads possible

#### Read-Your-Writes Consistency
```
Write → Remember write timestamp
Read → Only from replicas caught up past timestamp
```
- **Pros:** User sees their own writes
- **Cons:** More complex, may need to read from primary

### Cross-Shard Operations

**Problem:** JOIN across sharded tables

```sql
-- Before sharding
SELECT u.username, p.title
FROM users u
JOIN posts p ON u.user_id = p.user_id
WHERE u.user_id = 12345;

-- After sharding (users and posts on different shards)
-- Option 1: Denormalize
posts table includes: post_id, user_id, username, title

-- Option 2: Application-level join
users_data = query_shard1("SELECT * FROM users WHERE user_id = 12345")
posts_data = query_shard2("SELECT * FROM posts WHERE user_id = 12345")
result = join_in_application(users_data, posts_data)

-- Option 3: Scatter-gather
results = []
for shard in all_shards:
    result = query_shard(shard, "SELECT * FROM posts WHERE created_at > '2025-01-01'")
    results.extend(result)
return merge_and_sort(results)
```

### Shard Rebalancing

```python
class ShardRebalancer:
    def rebalance(self, source_shard, target_shard, key_range):
        """Move data from source to target shard"""

        # 1. Start dual writes (write to both shards)
        self.enable_dual_writes(key_range, [source_shard, target_shard])

        # 2. Copy existing data
        data = source_shard.read_range(key_range)
        for record in data:
            target_shard.write(record)

        # 3. Verify data copied correctly
        if not self.verify_migration(source_shard, target_shard, key_range):
            raise MigrationError("Data verification failed")

        # 4. Update routing to point to target
        self.update_routing(key_range, target_shard)

        # 5. Stop dual writes, remove from source
        self.disable_dual_writes(key_range)
        source_shard.delete_range(key_range)

        # 6. Verify and complete
        return self.verify_final_state(target_shard, key_range)
```

## 9. Scalability & Bottlenecks

### Read Scaling

**Solution: Add Read Replicas**
- Linear scaling for reads
- No code changes needed
- Caveat: Eventual consistency

**Bottleneck:** Replication lag
- Monitor lag metrics
- Use async replication
- Add more replicas if needed

### Write Scaling

**Solution: Shard the database**
- Distributes writes across shards
- Each shard handles subset of data
- Caveat: Complex querying

**Bottleneck:** Single shard hotspot
- Use hash sharding for even distribution
- Monitor per-shard metrics
- Repartition hot shards

### Storage Scaling

**Solution: Add more shards**
- Each shard stores subset of data
- Total storage = sum of all shards
- Caveat: Rebalancing required

### Network Bottleneck

**Symptoms:**
- High replication lag
- Slow cross-shard queries

**Solutions:**
- Compress replication traffic
- Batch replication updates
- Use faster network hardware
- Reduce cross-shard queries

## 10. Follow-up Questions

1. **How do you handle transactions across multiple shards?**
   - Two-phase commit (2PC)
   - SAGA pattern for distributed transactions
   - Eventual consistency with compensation
   - Avoid cross-shard transactions when possible

2. **What happens during failover in primary-replica setup?**
   - Detect primary failure (heartbeat timeout)
   - Elect new primary (from replicas)
   - Update routing to new primary
   - Ensure no split-brain scenario

3. **How do you choose the right shard key?**
   - High cardinality (many unique values)
   - Even distribution
   - Frequently used in queries
   - Avoid hotspots
   - Example: user_id good, country bad (uneven)

4. **How do you handle schema changes in sharded database?**
   - Rolling schema updates
   - Backward compatible changes
   - Use schema versioning
   - Test on single shard first
   - Gradual rollout across shards

5. **What is the difference between sharding and partitioning?**
   - Partitioning: Division within single database instance
   - Sharding: Division across multiple database instances
   - Partitioning: Transparent to application
   - Sharding: Usually requires application awareness

6. **How do you backup a sharded database?**
   - Backup each shard independently
   - Coordinate timing for consistency
   - Use point-in-time recovery
   - Test restore procedures
   - Consider backup windows for each shard

7. **When should you shard your database?**
   - Data volume exceeds single server capacity
   - Write throughput exceeds single server
   - Need geographic distribution
   - Read replicas insufficient
   - **Don't shard too early** - complexity cost high

8. **How do you monitor a distributed database?**
   - Replication lag per replica
   - Query latency per shard
   - Disk usage per shard
   - Connection pool utilization
   - Cross-shard query frequency
   - Slow query log

9. **What are the challenges with multi-primary replication?**
   - Conflict resolution complexity
   - Last-write-wins may lose data
   - Need vector clocks or CRDTs
   - Higher complexity
   - Use cases: Multi-region writes

10. **How do you test database scaling strategies?**
    - Load testing with realistic data
    - Simulate failures (chaos engineering)
    - Test rebalancing procedures
    - Measure replication lag under load
    - Benchmark different strategies
