# Design Distributed Key-Value Store (DynamoDB/Cassandra)

**Difficulty:** Hard

## 1. Problem Statement

Design a distributed NoSQL key-value store like DynamoDB or Cassandra that provides high availability, partition tolerance, horizontal scalability, and low-latency access to data. The system should handle millions of operations per second, store petabytes of data, and maintain high availability even during node failures.

**Key Requirements:**
- Partition tolerance and availability (AP in CAP)
- Horizontal scalability (add nodes seamlessly)
- Single-digit millisecond latency
- Tunable consistency
- Automatic replication and sharding

## 2. Requirements

### Functional Requirements
1. **Basic Operations**:
   - GET(key) → value
   - PUT(key, value) → success
   - DELETE(key) → success
2. **Advanced Operations**:
   - Scan/Query with filters
   - Batch operations
   - Atomic counters
   - TTL (Time-To-Live)
3. **Data Model**: Flexible schema (JSON documents, key-value pairs)
4. **Secondary Indexes**: Query by non-key attributes

### Non-Functional Requirements
1. **Availability**: 99.99% (four nines)
2. **Scalability**:
   - Petabytes of data
   - Millions of ops/sec
   - Thousands of nodes
3. **Performance**:
   - GET latency: 1-5ms (p99)
   - PUT latency: 5-10ms (p99)
4. **Consistency**: Tunable (eventual, strong, read-your-writes)
5. **Durability**: No data loss (replication)
6. **Partition Tolerance**: Continue operating during network partitions

## 3. Storage Estimation

### Assumptions
- **Total Keys**: 1 trillion
- **Average Value Size**: 1 KB
- **Replication Factor**: 3
- **Read:Write Ratio**: 80:20
- **Peak QPS**: 10 million ops/sec

### Calculations

**Total Storage:**
```
1 trillion keys × 1 KB = 1 Petabyte (PB) raw
With replication (3x): 3 PB
```

**Node Storage:**
```
Assuming 10 TB per node:
3 PB / 10 TB = 300 nodes minimum
With overhead: 500 nodes
```

**Request Distribution:**
```
Peak: 10M ops/sec
- Reads: 8M/sec (80%)
- Writes: 2M/sec (20%)

Per node (500 nodes):
- 16,000 reads/sec per node
- 4,000 writes/sec per node
```

**Memory for Hot Data:**
```
20% hot data: 200 GB raw
Per node: 200 GB / 500 = 400 MB
With 64 GB RAM per node: Can cache 64 GB / 500 nodes = plenty
```

## 4. High-Level Architecture

```
┌────────────────────────────────────────────────┐
│            Client Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │SDK/Driver│  │REST API  │  │  CLI     │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────────────────────────────┘
                    │
                    │
        ┌───────────┴───────────┐
        │   Coordinator Nodes   │
        │  (Request Routing)    │
        └───────────┬───────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Node 1  │   │ Node 2  │   │ Node N  │
│Ring Pos │   │Ring Pos │   │Ring Pos │
│  0-100  │   │ 101-200 │   │ 201-300 │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
        ┌──────────┴──────────┐
        │  Gossip Protocol     │
        │  (Failure Detection) │
        └─────────────────────┘

Each Node:
├── Memtable (In-memory write buffer)
├── Commit Log (WAL)
├── SSTable (On-disk sorted files)
├── Bloom Filters (Membership test)
└── Compaction Engine
```

### Key Components

1. **Coordinator**: Routes requests to appropriate nodes
2. **Storage Nodes**: Store data partitions
3. **Gossip Protocol**: Peer-to-peer failure detection
4. **Consistent Hashing**: Data distribution
5. **Replication**: N copies across nodes
6. **Quorum Reads/Writes**: Tunable consistency
7. **Anti-Entropy**: Background data repair
8. **Compaction**: Merge SSTables, remove tombstones

## 5. API Design

### Basic Operations

```python
# PUT - Write key-value
client.put(
    key="user:12345",
    value={"name": "John", "age": 30},
    consistency="QUORUM",  # ONE, QUORUM, ALL
    ttl=3600  # seconds
)

# GET - Read value
value = client.get(
    key="user:12345",
    consistency="QUORUM"
)

# DELETE - Remove key
client.delete(
    key="user:12345",
    consistency="QUORUM"
)

# Batch Operations
client.batch_write([
    {"key": "user:1", "value": {...}},
    {"key": "user:2", "value": {...}},
])

# Conditional PUT
client.put_if_not_exists(
    key="user:12345",
    value={...}
)

# Atomic Increment
client.increment_counter(
    key="page:views",
    delta=1
)

# Query with Filter
results = client.query(
    partition_key="user",
    filter={"age": {"$gt": 25}},
    limit=100
)
```

## 6. Data Partitioning & Consistent Hashing

### Consistent Hashing Ring

```python
class ConsistentHashRing:
    def __init__(self, nodes, virtual_nodes=150):
        self.ring = {}
        self.sorted_keys = []
        self.virtual_nodes = virtual_nodes
        
        for node in nodes:
            self.add_node(node)
    
    def add_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node.id}:{i}"
            hash_value = self.hash(virtual_key)
            self.ring[hash_value] = node
        
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_nodes(self, key, replication_factor=3):
        hash_value = self.hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_value)
        
        nodes = []
        unique_nodes = set()
        
        # Walk clockwise around ring
        for i in range(len(self.sorted_keys)):
            pos = (idx + i) % len(self.sorted_keys)
            node = self.ring[self.sorted_keys[pos]]
            
            if node.id not in unique_nodes:
                nodes.append(node)
                unique_nodes.add(node.id)
            
            if len(nodes) >= replication_factor:
                break
        
        return nodes
    
    def hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

### Data Distribution

```
Key: "user:12345"
Hash: MD5("user:12345") = abc123... → 42135 (ring position)

Ring (0-65535):
- Node A: 0-15000
- Node B: 15001-30000
- Node C: 30001-45000  ← Key 42135 goes here
- Node D: 45001-65535

Replicas (N=3):
- Primary: Node C
- Replica 1: Node D (next on ring)
- Replica 2: Node A (wrap around)
```

## 7. Replication & Consistency

### Replication Strategy

```python
class ReplicationManager:
    def write(self, key, value, consistency_level):
        # 1. Determine replicas
        nodes = self.ring.get_nodes(key, replication_factor=3)
        
        # 2. Write to all replicas (async)
        write_futures = []
        for node in nodes:
            future = node.async_write(key, value)
            write_futures.append(future)
        
        # 3. Wait based on consistency level
        if consistency_level == "ALL":
            required = 3  # All replicas
        elif consistency_level == "QUORUM":
            required = 2  # Majority
        elif consistency_level == "ONE":
            required = 1  # Any one replica
        
        # Wait for required responses
        success_count = 0
        for future in write_futures:
            try:
                result = future.wait(timeout=100ms)
                if result.success:
                    success_count += 1
                
                if success_count >= required:
                    return "SUCCESS"
            except Timeout:
                continue
        
        return "FAILURE" if success_count < required else "SUCCESS"
```

### Quorum-Based Consistency

```
N = Replication factor (3)
R = Read quorum (2)
W = Write quorum (2)

Guarantee: R + W > N → Strong consistency

Example:
Write to 2 nodes → Success
Read from 2 nodes → At least 1 overlaps with write
```

### Read Repair

```python
def read_with_repair(self, key, consistency):
    nodes = self.ring.get_nodes(key)
    
    # Read from all replicas
    responses = []
    for node in nodes:
        response = node.read(key)
        responses.append(response)
    
    # Find most recent version (by timestamp)
    latest = max(responses, key=lambda r: r.timestamp)
    
    # Repair stale replicas (async)
    for node, response in zip(nodes, responses):
        if response.timestamp < latest.timestamp:
            node.async_write(key, latest.value, latest.timestamp)
    
    return latest.value
```

### Hinted Handoff

**Problem:** Replica node temporarily down during write

**Solution:** Store hint on coordinator

```python
def write_with_hint(self, key, value):
    nodes = self.ring.get_nodes(key)
    
    write_count = 0
    for node in nodes:
        if node.is_available():
            node.write(key, value)
            write_count += 1
        else:
            # Store hint: "This write is for node X"
            hint = {"target": node.id, "key": key, "value": value}
            self.coordinator.store_hint(hint)
    
    return write_count >= QUORUM
```

**Hint Replay:**
```python
def replay_hints(self):
    for hint in self.coordinator.get_pending_hints():
        target_node = hint['target']
        
        if target_node.is_available():
            target_node.write(hint['key'], hint['value'])
            self.coordinator.delete_hint(hint['id'])
```

## 8. Storage Engine (LSM Tree)

### Write Path

```
1. Client Write Request
   ↓
2. Write to Commit Log (WAL) - Sequential append
   ↓
3. Write to Memtable (In-memory sorted tree)
   ↓
4. Return success to client
   ↓
5. [Background] When Memtable full → Flush to SSTable
   ↓
6. [Background] Compact SSTables periodically
```

**Implementation:**
```python
class LSMTree:
    def __init__(self):
        self.memtable = SortedDict()  # In-memory
        self.commit_log = CommitLog()
        self.sstables = []
        self.memtable_size_limit = 64 * 1024 * 1024  # 64 MB
    
    def put(self, key, value):
        # 1. Write to commit log (durability)
        self.commit_log.append(f"PUT {key} {value}\n")
        
        # 2. Write to memtable
        self.memtable[key] = {
            'value': value,
            'timestamp': now()
        }
        
        # 3. Check if memtable full
        if self.memtable.size() >= self.memtable_size_limit:
            self.flush_memtable()
    
    def get(self, key):
        # 1. Check memtable first
        if key in self.memtable:
            return self.memtable[key]['value']
        
        # 2. Check SSTables (newest to oldest)
        for sstable in reversed(self.sstables):
            # Use bloom filter to check membership
            if not sstable.bloom_filter.might_contain(key):
                continue  # Definitely not in this SSTable
            
            value = sstable.get(key)
            if value:
                return value
        
        return None  # Key not found
    
    def flush_memtable(self):
        # Write memtable to disk as new SSTable
        sstable = SSTable.from_memtable(self.memtable)
        self.sstables.append(sstable)
        
        # Clear memtable
        self.memtable.clear()
        
        # Truncate commit log
        self.commit_log.truncate()
```

### SSTable Structure

```
SSTable File:
┌─────────────────────────┐
│  Data Block 1 (4 KB)    │  key1:value1, key2:value2...
├─────────────────────────┤
│  Data Block 2 (4 KB)    │
├─────────────────────────┤
│  ...                    │
├─────────────────────────┤
│  Index Block            │  key1→offset1, key2→offset2...
├─────────────────────────┤
│  Bloom Filter           │  Probabilistic membership test
├─────────────────────────┤
│  Footer (Metadata)      │  Version, compression, checksums
└─────────────────────────┘
```

### Compaction

**Purpose:** 
- Merge multiple SSTables
- Remove deleted keys (tombstones)
- Reduce read amplification

**Strategies:**

1. **Size-Tiered Compaction (Cassandra default):**
```python
def size_tiered_compaction(self):
    # Group SSTables by size tier
    tiers = self.group_by_size(self.sstables)
    
    for tier in tiers:
        if len(tier) >= 4:  # Threshold
            # Merge these 4 SSTables into 1
            merged = self.merge_sstables(tier)
            
            # Replace old SSTables
            for old in tier:
                self.sstables.remove(old)
                old.delete()
            
            self.sstables.append(merged)
```

2. **Leveled Compaction (LevelDB):**
```
Level 0: 4 SSTables (10 MB each)
Level 1: 10 SSTables (100 MB each)
Level 2: 100 SSTables (1 GB each)

Compaction: Move SSTable from L0 to L1, merge overlapping
```

## 9. Failure Detection & Gossip Protocol

### Gossip Protocol

```python
class GossipProtocol:
    def __init__(self, node):
        self.node = node
        self.peers = []  # All nodes in cluster
        self.heartbeats = {}  # node_id → (heartbeat, timestamp)
        self.gossip_interval = 1.0  # seconds
    
    def start(self):
        while True:
            self.gossip_round()
            time.sleep(self.gossip_interval)
    
    def gossip_round(self):
        # 1. Increment own heartbeat
        self.heartbeats[self.node.id] = (
            self.heartbeats.get(self.node.id, (0, 0))[0] + 1,
            now()
        )
        
        # 2. Select random peer
        peer = random.choice(self.peers)
        
        # 3. Send heartbeat table to peer
        peer.send_gossip(self.heartbeats)
        
        # 4. Receive peer's heartbeat table
        peer_heartbeats = peer.receive_gossip()
        
        # 5. Merge heartbeat tables
        for node_id, (heartbeat, timestamp) in peer_heartbeats.items():
            if node_id not in self.heartbeats:
                self.heartbeats[node_id] = (heartbeat, timestamp)
            else:
                current_hb, current_ts = self.heartbeats[node_id]
                if heartbeat > current_hb:
                    self.heartbeats[node_id] = (heartbeat, timestamp)
        
        # 6. Detect failures
        self.detect_failures()
    
    def detect_failures(self):
        current_time = now()
        failure_threshold = 10  # seconds
        
        for node_id, (heartbeat, timestamp) in self.heartbeats.items():
            if current_time - timestamp > failure_threshold:
                # Node suspected failed
                self.mark_node_down(node_id)
```

**Gossip Convergence:**
- In cluster of N nodes
- Each node gossips every 1 second
- Full convergence in O(log N) rounds
- Example: 1000 nodes → ~10 seconds

## 10. Vector Clocks & Conflict Resolution

### Vector Clocks for Causality

```python
class VectorClock:
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = defaultdict(int)
    
    def increment(self):
        self.clock[self.node_id] += 1
    
    def update(self, other_clock):
        for node, count in other_clock.items():
            self.clock[node] = max(self.clock[node], count)
        self.increment()
    
    def happens_before(self, other):
        # self happened before other if:
        # - All counters in self <= other
        # - At least one counter in self < other
        
        all_less_or_equal = all(
            self.clock[node] <= other.clock[node]
            for node in self.clock
        )
        
        at_least_one_less = any(
            self.clock[node] < other.clock.get(node, 0)
            for node in self.clock
        )
        
        return all_less_or_equal and at_least_one_less
    
    def concurrent_with(self, other):
        return not self.happens_before(other) and not other.happens_before(self)
```

**Example:**
```
Node A writes: {value: "v1", vector_clock: {A:1}}
Node B writes: {value: "v2", vector_clock: {B:1}}

Both writes happen concurrently (network partition)

After partition heals:
- Vector clocks show conflict: {A:1} || {B:1}
- Both versions returned to client
- Client resolves conflict (or use last-write-wins)
```

### Conflict Resolution Strategies

1. **Last-Write-Wins (LWW):**
```python
def resolve_lww(versions):
    return max(versions, key=lambda v: v.timestamp)
```

2. **Application-Level Resolution:**
```python
def resolve_shopping_cart(versions):
    # Merge all items from both carts
    merged_cart = set()
    for version in versions:
        merged_cart.update(version.items)
    return list(merged_cart)
```

## 11. Secondary Indexes

### Local Secondary Index

```python
class LocalSecondaryIndex:
    def __init__(self, attribute_name):
        self.attribute = attribute_name
        self.index = SortedDict()  # attribute_value → [primary_keys]
    
    def insert(self, primary_key, item):
        attribute_value = item.get(self.attribute)
        if attribute_value:
            if attribute_value not in self.index:
                self.index[attribute_value] = []
            self.index[attribute_value].append(primary_key)
    
    def query(self, attribute_value):
        primary_keys = self.index.get(attribute_value, [])
        
        # Fetch items by primary key
        items = []
        for pk in primary_keys:
            item = self.table.get(pk)
            items.append(item)
        
        return items
```

### Global Secondary Index (DynamoDB-style)

```
Separate table with different partition key

Primary Table:
- Partition Key: user_id
- Sort Key: timestamp
- Attributes: {name, email, age}

GSI on email:
- Partition Key: email
- Projects: {user_id, name}
- Eventually consistent with main table
```

## 12. Advanced Features

### TTL (Time-To-Live)

```python
def put_with_ttl(self, key, value, ttl_seconds):
    expiration = now() + timedelta(seconds=ttl_seconds)
    
    self.put(key, {
        'value': value,
        'expiration': expiration.timestamp()
    })

def get_with_ttl_check(self, key):
    item = self.get(key)
    
    if item and 'expiration' in item:
        if now().timestamp() > item['expiration']:
            # Expired, delete and return None
            self.delete(key)
            return None
    
    return item['value']
```

### Conditional Writes

```python
def put_if_not_exists(self, key, value):
    current = self.get(key)
    
    if current is not None:
        return False  # Key already exists
    
    self.put(key, value)
    return True

def compare_and_swap(self, key, old_value, new_value):
    current = self.get(key)
    
    if current != old_value:
        return False
    
    self.put(key, new_value)
    return True
```

### Atomic Counters

```python
class AtomicCounter:
    def increment(self, key, delta=1):
        # Use commutative operation (addition)
        # Safe during conflicts: A+1+1 = (A+1)+1
        
        self.put(key, {
            'counter': 'INCREMENT',
            'delta': delta,
            'timestamp': now()
        })
    
    def read_counter(self, key):
        # Read all increments, sum them
        versions = self.get_all_versions(key)
        
        total = 0
        for version in versions:
            if version['counter'] == 'INCREMENT':
                total += version['delta']
        
        return total
```

## 13. Performance Optimizations

### Bloom Filters

```python
class BloomFilter:
    def __init__(self, size=1000000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size
    
    def add(self, key):
        for i in range(self.num_hashes):
            index = self.hash(key, i) % self.size
            self.bit_array[index] = True
    
    def might_contain(self, key):
        for i in range(self.num_hashes):
            index = self.hash(key, i) % self.size
            if not self.bit_array[index]:
                return False  # Definitely not present
        return True  # Might be present (false positives possible)
    
    def hash(self, key, seed):
        return int(hashlib.md5(f"{key}:{seed}".encode()).hexdigest(), 16)
```

**Benefit:** 
- Skip SSTable read if key definitely not present
- 1% false positive rate → Save 99% unnecessary disk reads

### Caching

```python
class CacheLayer:
    def __init__(self, max_size=10000):
        self.cache = LRUCache(max_size)
    
    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        
        # Cache miss
        value = self.storage.get(key)
        self.cache.put(key, value)
        
        return value
```

### Compression

```python
def compress_value(self, value):
    # Use Snappy or LZ4 compression
    compressed = snappy.compress(json.dumps(value))
    
    if len(compressed) < len(value):
        return compressed
    else:
        return value  # Don't compress if not beneficial
```

## 14. Trade-offs

### Eventual vs. Strong Consistency

**Eventual Consistency:**
- ✅ Higher availability
- ✅ Lower latency
- ❌ Stale reads possible

**Strong Consistency (QUORUM):**
- ✅ No stale reads
- ❌ Higher latency
- ❌ Lower availability

**Decision:** Tunable per request

### Replication Factor

**N=3:**
- ✅ Standard, good durability
- ❌ 3x storage cost

**N=5:**
- ✅ Higher durability
- ❌ 5x storage cost
- ❌ Slower writes (more nodes)

**Decision:** N=3 for most use cases

### Compaction Strategy

**Size-Tiered:**
- ✅ Better write throughput
- ❌ Read amplification
- ❌ Space amplification

**Leveled:**
- ✅ Better read performance
- ✅ Predictable space
- ❌ Higher write amplification

**Decision:** Depends on workload

## 15. Follow-up Questions

1. **How do you handle hot keys (celebrity problem)?**
   - Replicate hot keys to more nodes
   - Cache at client/coordinator level
   - Use consistent hashing with virtual nodes

2. **How would you implement range queries?**
   - Use sort keys (Cassandra clustering columns)
   - Store data sorted by range key
   - Query: Start key → End key

3. **How do you ensure data consistency during compaction?**
   - Compaction is online (doesn't block reads/writes)
   - Use versioning (SSTables immutable)
   - Atomic swap after compaction complete

4. **How would you implement transactions?**
   - Lightweight transactions using Paxos
   - Compare-and-set operations
   - Limited to single partition

5. **How do you handle schema evolution?**
   - Flexible schema (JSON)
   - No schema migrations needed
   - Client handles versioning

6. **How would you backup and restore data?**
   - Snapshot SSTables (immutable)
   - Stream to S3/GCS
   - Restore: Copy SSTables back, rebuild indexes

7. **How do you optimize for time-series data?**
   - Partition by time window
   - TTL for automatic expiration
   - Compaction strategy: Time-window

8. **How would you implement cross-datacenter replication?**
   - Async replication between DCs
   - Each DC has full replica set
   - Resolve conflicts with vector clocks

9. **How do you handle node replacement?**
   - Bootstrap new node
   - Stream data from existing replicas
   - Remove old node from ring

10. **How would you implement auditing/logging?**
    - Write-ahead log (commit log)
    - Separate log stream to Kafka
    - Process logs for analytics

## Complexity Analysis

- **Time Complexity:**
  - GET: O(log n) where n = number of SSTables
  - PUT: O(1) write to memtable
  - Range Query: O(k) where k = result size

- **Space Complexity:**
  - Total: O(n) where n = data size
  - With replication: O(r × n) where r = replication factor
  - Per node: O(n / num_nodes)

## References

- [Dynamo Paper (Amazon)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Cassandra Architecture](https://cassandra.apache.org/doc/latest/architecture/)
- [DynamoDB Paper](https://www.usenix.org/system/files/atc22-elhemali.pdf)
- [LSM Trees](https://en.wikipedia.org/wiki/Log-structured_merge-tree)
- [Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing)
