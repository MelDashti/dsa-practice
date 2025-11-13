# Distributed Caching System (Redis/Memcached-style)

## 1. Problem Statement

Design a distributed caching system similar to Redis Cluster or Memcached that provides high-performance key-value storage with sub-millisecond latency, high availability, automatic sharding, and support for various data structures. The system should handle millions of operations per second while maintaining consistency and durability guarantees.

## 2. Requirements

### Functional Requirements
- **Basic operations**: GET, SET, DELETE with O(1) complexity
- **Data structures**: Strings, Lists, Sets, Sorted Sets, Hashes
- **Expiration**: TTL (time-to-live) support
- **Atomic operations**: INCR, DECR, GETSET
- **Pub/Sub**: Message broadcasting
- **Transactions**: Multi-command atomic execution
- **Persistence**: Optional disk persistence
- **Replication**: Master-slave replication
- **Cluster mode**: Automatic sharding across nodes

### Non-Functional Requirements
- **Latency**: P99 < 1ms for GET/SET
- **Throughput**: 1 million ops/second per node
- **Availability**: 99.99% uptime
- **Scalability**: Handle 100+ nodes in cluster
- **Memory efficiency**: <5% overhead
- **Durability**: Configurable (in-memory only or persistent)
- **Consistency**: Eventual consistency with optional strong consistency

### Out of Scope
- Complex query language (SQL)
- ACID transactions across multiple keys on different nodes
- Built-in machine learning features

## 3. Capacity Estimation

### Scale Assumptions
- Total keys: 1 billion
- Average key size: 50 bytes
- Average value size: 500 bytes
- QPS: 10 million (80% reads, 20% writes)
- Number of nodes: 100
- Replication factor: 3

### Memory Estimation
```
Per key-value pair:
- Key: 50 bytes
- Value: 500 bytes
- Metadata (TTL, type, etc.): 50 bytes
- Total: 600 bytes

Total data:
1B keys × 600 bytes = 600 GB

With replication (3x):
600 GB × 3 = 1.8 TB

With overhead (20%):
1.8 TB × 1.2 = 2.16 TB

Per node (100 nodes):
2.16 TB / 100 = 21.6 GB per node
```

### Network Bandwidth
```
QPS per node:
10M ops/sec / 100 nodes = 100K ops/sec

Average request size:
GET: 50 bytes (key only)
SET: 550 bytes (key + value)

Average: 0.8 × 50 + 0.2 × 550 = 150 bytes

Bandwidth per node:
100K ops/sec × 150 bytes = 15 MB/sec = 120 Mbps

With replication:
120 Mbps × 2 = 240 Mbps per node
```

## 4. High-Level Design

```
┌────────────────────────────────────────────────┐
│              Client Applications               │
└─────────────────┬──────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           Client-Side Router                    │
│  - Consistent hashing                           │
│  - Node discovery                               │
│  - Connection pooling                           │
└──────────┬──────────────────────────────────────┘
           │
           │ Route to shard
           ▼
┌──────────────────────────────────────────────────┐
│          Cache Cluster (Sharded)                 │
│                                                  │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │  Shard 1        │  │  Shard 2        │      │
│  │  ┌───────────┐  │  │  ┌───────────┐  │      │
│  │  │ Master    │  │  │  │ Master    │  │      │
│  │  │ (R/W)     │  │  │  │ (R/W)     │  │      │
│  │  └─────┬─────┘  │  │  └─────┬─────┘  │      │
│  │        │ Repl   │  │        │ Repl   │      │
│  │  ┌─────▼─────┐  │  │  ┌─────▼─────┐  │      │
│  │  │ Replica 1 │  │  │  │ Replica 1 │  │      │
│  │  │ (Read)    │  │  │  │ (Read)    │  │      │
│  │  └───────────┘  │  │  └───────────┘  │      │
│  │  ┌───────────┐  │  │  ┌───────────┐  │      │
│  │  │ Replica 2 │  │  │  │ Replica 2 │  │      │
│  │  │ (Read)    │  │  │  │ (Read)    │  │      │
│  │  └───────────┘  │  │  └───────────┘  │      │
│  └─────────────────┘  └─────────────────┘      │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│         Supporting Services                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Config       │  │ Monitoring   │            │
│  │ Service      │  │ & Metrics    │            │
│  │ (Cluster     │  │              │            │
│  │  topology)   │  │              │            │
│  └──────────────┘  └──────────────┘            │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│         Persistence Layer (Optional)             │
│  - AOF (Append-Only File)                        │
│  - RDB (Snapshot)                                │
│  - Write-Ahead Log                               │
└──────────────────────────────────────────────────┘
```

### Core Components
1. **Cache Node**: Stores data in memory
2. **Consistent Hashing**: Distributes keys across nodes
3. **Replication Manager**: Handles master-slave replication
4. **Persistence Engine**: Optional disk persistence
5. **Cluster Manager**: Manages cluster topology
6. **Client Router**: Routes requests to correct node
7. **Eviction Manager**: Manages memory limits

## 5. API Design

### Basic Operations API

```python
class CacheClient:
    def get(self, key: str) -> Optional[bytes]:
        """Get value by key"""
        pass

    def set(self, key: str, value: bytes, ttl: Optional[int] = None) -> bool:
        """
        Set key-value pair
        ttl: Time-to-live in seconds
        """
        pass

    def delete(self, key: str) -> bool:
        """Delete key"""
        pass

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        pass

    def expire(self, key: str, ttl: int) -> bool:
        """Set expiration on key"""
        pass

    def ttl(self, key: str) -> int:
        """Get remaining TTL for key"""
        pass

    # Atomic operations
    def incr(self, key: str, delta: int = 1) -> int:
        """Atomically increment integer value"""
        pass

    def getset(self, key: str, value: bytes) -> Optional[bytes]:
        """Atomically set value and return old value"""
        pass

    # Batch operations
    def mget(self, keys: List[str]) -> List[Optional[bytes]]:
        """Get multiple values"""
        pass

    def mset(self, key_values: Dict[str, bytes]) -> bool:
        """Set multiple key-value pairs"""
        pass
```

### Data Structure APIs

```python
# List operations
def lpush(self, key: str, values: List[bytes]) -> int:
    """Push values to left of list"""
    pass

def rpush(self, key: str, values: List[bytes]) -> int:
    """Push values to right of list"""
    pass

def lpop(self, key: str) -> Optional[bytes]:
    """Pop value from left of list"""
    pass

def lrange(self, key: str, start: int, stop: int) -> List[bytes]:
    """Get range of list elements"""
    pass

# Hash operations
def hset(self, key: str, field: str, value: bytes) -> bool:
    """Set hash field"""
    pass

def hget(self, key: str, field: str) -> Optional[bytes]:
    """Get hash field value"""
    pass

def hgetall(self, key: str) -> Dict[str, bytes]:
    """Get all hash fields and values"""
    pass

# Set operations
def sadd(self, key: str, members: List[bytes]) -> int:
    """Add members to set"""
    pass

def smembers(self, key: str) -> Set[bytes]:
    """Get all set members"""
    pass

def sismember(self, key: str, member: bytes) -> bool:
    """Check if member is in set"""
    pass

# Sorted Set operations
def zadd(self, key: str, score_members: Dict[float, bytes]) -> int:
    """Add members with scores to sorted set"""
    pass

def zrange(self, key: str, start: int, stop: int) -> List[Tuple[bytes, float]]:
    """Get range by rank"""
    pass

def zrangebyscore(self, key: str, min_score: float, max_score: float) -> List[bytes]:
    """Get range by score"""
    pass
```

## 6. Component Design

### Cache Node Architecture

```python
class CacheNode:
    """Single cache node instance"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.data_store = DataStore()  # In-memory data
        self.replication = ReplicationManager()
        self.persistence = PersistenceManager()
        self.eviction = EvictionManager()
        self.ttl_manager = TTLManager()

    async def get(self, key: str) -> Optional[bytes]:
        """Get value by key"""
        # Check if key expired
        if self.ttl_manager.is_expired(key):
            await self.delete(key)
            return None

        # Get from data store
        value = self.data_store.get(key)

        # Update access time (for LRU)
        if value is not None:
            self.data_store.update_access_time(key)

        return value

    async def set(self, key: str, value: bytes, ttl: Optional[int] = None):
        """Set key-value pair"""
        # Check memory limit
        if self.eviction.should_evict():
            await self.eviction.evict_keys()

        # Store value
        self.data_store.set(key, value)

        # Set TTL if specified
        if ttl:
            self.ttl_manager.set_expiration(key, time.time() + ttl)

        # Replicate to slaves
        await self.replication.replicate_command('SET', key, value, ttl)

        # Persist if enabled
        if self.persistence.is_enabled():
            await self.persistence.log_command('SET', key, value, ttl)

    async def delete(self, key: str):
        """Delete key"""
        self.data_store.delete(key)
        self.ttl_manager.remove_expiration(key)

        # Replicate deletion
        await self.replication.replicate_command('DEL', key)

        # Persist deletion
        if self.persistence.is_enabled():
            await self.persistence.log_command('DEL', key)
```

### Data Store Implementation

```python
class DataStore:
    """
    In-memory data storage with support for multiple data types
    Uses hash tables for O(1) operations
    """

    def __init__(self):
        # Main hash table: key -> CacheEntry
        self.data = {}

        # Access tracking for LRU
        self.access_times = {}

        # Memory tracking
        self.memory_used = 0

        # Lock for thread-safety
        self.lock = threading.RLock()

    def get(self, key: str) -> Optional[bytes]:
        """Get value by key"""
        with self.lock:
            entry = self.data.get(key)
            return entry.value if entry else None

    def set(self, key: str, value: bytes):
        """Set key-value pair"""
        with self.lock:
            # Calculate memory change
            old_size = self.get_entry_size(key)

            # Create/update entry
            entry = CacheEntry(
                key=key,
                value=value,
                value_type='string',
                created_at=time.time()
            )
            self.data[key] = entry

            # Update memory usage
            new_size = self.get_entry_size(key)
            self.memory_used += (new_size - old_size)

            # Update access time
            self.access_times[key] = time.time()

    def delete(self, key: str) -> bool:
        """Delete key"""
        with self.lock:
            if key not in self.data:
                return False

            # Update memory usage
            size = self.get_entry_size(key)
            self.memory_used -= size

            # Remove from store
            del self.data[key]
            self.access_times.pop(key, None)

            return True

    def get_entry_size(self, key: str) -> int:
        """Calculate memory size of entry"""
        if key not in self.data:
            return 0

        entry = self.data[key]
        # Key + value + metadata overhead
        return len(key) + len(entry.value) + 64  # 64 bytes overhead

class CacheEntry:
    """Single cache entry"""
    def __init__(self, key: str, value: bytes, value_type: str, created_at: float):
        self.key = key
        self.value = value
        self.value_type = value_type
        self.created_at = created_at
```

### Consistent Hashing for Sharding

```python
class ConsistentHash:
    """
    Consistent hashing ring for distributing keys across nodes
    Minimizes key movement when nodes are added/removed
    """

    def __init__(self, nodes: List[str], virtual_nodes: int = 150):
        self.ring = {}  # hash_value -> node_id
        self.sorted_keys = []
        self.virtual_nodes = virtual_nodes
        self.nodes = set()

        # Add initial nodes
        for node in nodes:
            self.add_node(node)

    def add_node(self, node_id: str):
        """Add node to ring"""
        self.nodes.add(node_id)

        # Add virtual nodes for better distribution
        for i in range(self.virtual_nodes):
            virtual_key = f"{node_id}:{i}"
            hash_value = self._hash(virtual_key)

            self.ring[hash_value] = node_id
            bisect.insort(self.sorted_keys, hash_value)

    def remove_node(self, node_id: str):
        """Remove node from ring"""
        self.nodes.discard(node_id)

        # Remove virtual nodes
        for i in range(self.virtual_nodes):
            virtual_key = f"{node_id}:{i}"
            hash_value = self._hash(virtual_key)

            self.ring.pop(hash_value, None)
            self.sorted_keys.remove(hash_value)

    def get_node(self, key: str) -> str:
        """Get node for key"""
        if not self.ring:
            return None

        hash_value = self._hash(key)

        # Find first node >= hash_value
        idx = bisect.bisect_right(self.sorted_keys, hash_value)

        if idx == len(self.sorted_keys):
            # Wrap around to first node
            idx = 0

        ring_key = self.sorted_keys[idx]
        return self.ring[ring_key]

    def get_nodes(self, key: str, count: int) -> List[str]:
        """Get multiple nodes for key (for replication)"""
        if not self.ring or count <= 0:
            return []

        hash_value = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_value)

        nodes = []
        seen = set()

        # Collect unique nodes
        for _ in range(len(self.sorted_keys)):
            if idx >= len(self.sorted_keys):
                idx = 0

            ring_key = self.sorted_keys[idx]
            node = self.ring[ring_key]

            if node not in seen:
                nodes.append(node)
                seen.add(node)

                if len(nodes) == count:
                    break

            idx += 1

        return nodes

    def _hash(self, key: str) -> int:
        """Hash function (MD5)"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_key_distribution(self) -> Dict[str, int]:
        """Get number of hash slots per node"""
        distribution = defaultdict(int)
        for node in self.ring.values():
            distribution[node] += 1
        return dict(distribution)
```

**Key Movement on Node Addition**:
With 150 virtual nodes per physical node:
- Adding a node: ~1/N keys move (where N is number of nodes)
- Example: 100 nodes → 101 nodes: ~1% of keys move

### Replication

```python
class ReplicationManager:
    """Manage master-slave replication"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.role = 'master'  # or 'slave'
        self.master_id = None  # If slave, ID of master
        self.slaves = []  # If master, list of slave IDs
        self.replication_offset = 0
        self.replication_buffer = deque(maxlen=10000)

    async def replicate_command(self, *command):
        """Replicate command to slaves"""
        if self.role != 'master':
            return

        # Add to replication buffer
        self.replication_offset += 1
        self.replication_buffer.append((self.replication_offset, command))

        # Send to all slaves asynchronously
        tasks = []
        for slave_id in self.slaves:
            task = self.send_to_slave(slave_id, command)
            tasks.append(task)

        # Don't wait for slaves (async replication)
        asyncio.gather(*tasks, return_exceptions=True)

    async def send_to_slave(self, slave_id: str, command):
        """Send command to slave"""
        try:
            await self.rpc_client.send_command(slave_id, command)
        except Exception as e:
            logger.error(f"Failed to replicate to slave {slave_id}: {e}")
            # Remove dead slave
            self.slaves.remove(slave_id)

    async def sync_from_master(self, master_id: str):
        """Synchronize data from master (for new slave)"""
        self.role = 'slave'
        self.master_id = master_id

        # 1. Request full sync
        snapshot = await self.rpc_client.request_snapshot(master_id)

        # 2. Load snapshot
        await self.load_snapshot(snapshot)

        # 3. Start receiving incremental updates
        await self.start_replication_stream(master_id)

    async def start_replication_stream(self, master_id: str):
        """Receive continuous stream of updates from master"""
        while self.role == 'slave':
            try:
                commands = await self.rpc_client.receive_commands(
                    master_id,
                    from_offset=self.replication_offset
                )

                for offset, command in commands:
                    await self.apply_command(command)
                    self.replication_offset = offset

            except Exception as e:
                logger.error(f"Replication error: {e}")
                await asyncio.sleep(1)

    async def failover_to_slave(self):
        """Promote slave to master (failover)"""
        if self.role != 'slave':
            return

        logger.info(f"Promoting slave {self.node_id} to master")

        self.role = 'master'
        self.master_id = None

        # Notify other nodes of promotion
        await self.announce_promotion()
```

### Eviction Policies

```python
class EvictionManager:
    """Manage memory eviction policies"""

    def __init__(self, max_memory: int, policy: str = 'lru'):
        self.max_memory = max_memory
        self.policy = policy
        self.data_store = None  # Reference to data store

    def should_evict(self) -> bool:
        """Check if eviction is needed"""
        return self.data_store.memory_used > self.max_memory

    async def evict_keys(self):
        """Evict keys based on policy"""
        if self.policy == 'lru':
            await self.evict_lru()
        elif self.policy == 'lfu':
            await self.evict_lfu()
        elif self.policy == 'random':
            await self.evict_random()
        elif self.policy == 'ttl':
            await self.evict_ttl()

    async def evict_lru(self):
        """Evict least recently used keys"""
        # Find keys with oldest access time
        sorted_keys = sorted(
            self.data_store.access_times.items(),
            key=lambda x: x[1]
        )

        # Evict until under memory limit
        for key, _ in sorted_keys:
            if not self.should_evict():
                break

            await self.data_store.delete(key)
            logger.debug(f"Evicted key: {key}")

    async def evict_lfu(self):
        """Evict least frequently used keys"""
        # Track access frequency
        access_counts = defaultdict(int)

        # Sample keys and count accesses
        # (full scan would be expensive)
        sample_size = min(1000, len(self.data_store.data))
        sample_keys = random.sample(list(self.data_store.data.keys()), sample_size)

        for key in sample_keys:
            entry = self.data_store.data[key]
            access_counts[key] = getattr(entry, 'access_count', 0)

        # Sort by frequency
        sorted_keys = sorted(access_counts.items(), key=lambda x: x[1])

        # Evict least frequent
        for key, _ in sorted_keys:
            if not self.should_evict():
                break

            await self.data_store.delete(key)

    async def evict_random(self):
        """Evict random keys"""
        while self.should_evict():
            key = random.choice(list(self.data_store.data.keys()))
            await self.data_store.delete(key)

    async def evict_ttl(self):
        """Evict keys with earliest expiration"""
        # Get keys with TTL
        ttl_keys = self.data_store.ttl_manager.get_all_with_ttl()

        # Sort by expiration time
        sorted_keys = sorted(ttl_keys, key=lambda x: x[1])

        # Evict keys with earliest expiration
        for key, _ in sorted_keys:
            if not self.should_evict():
                break

            await self.data_store.delete(key)
```

### TTL Management

```python
class TTLManager:
    """Manage key expiration"""

    def __init__(self):
        self.expirations = {}  # key -> expiration_timestamp
        self.expiration_queue = []  # Min heap of (expiration_time, key)
        self.lock = threading.Lock()

    def set_expiration(self, key: str, expiration_time: float):
        """Set expiration for key"""
        with self.lock:
            self.expirations[key] = expiration_time
            heapq.heappush(self.expiration_queue, (expiration_time, key))

    def remove_expiration(self, key: str):
        """Remove expiration for key"""
        with self.lock:
            self.expirations.pop(key, None)
            # Note: don't remove from heap (will be ignored during cleanup)

    def is_expired(self, key: str) -> bool:
        """Check if key is expired"""
        if key not in self.expirations:
            return False

        return time.time() >= self.expirations[key]

    async def cleanup_expired_keys(self):
        """Background task to clean up expired keys"""
        while True:
            current_time = time.time()
            expired_keys = []

            with self.lock:
                # Check heap for expired keys
                while self.expiration_queue:
                    expiration_time, key = self.expiration_queue[0]

                    if expiration_time > current_time:
                        break

                    heapq.heappop(self.expiration_queue)

                    # Verify key still has this expiration
                    if key in self.expirations and self.expirations[key] == expiration_time:
                        expired_keys.append(key)
                        del self.expirations[key]

            # Delete expired keys
            for key in expired_keys:
                await self.data_store.delete(key)

            await asyncio.sleep(0.1)  # Run every 100ms
```

### Persistence

```python
class PersistenceManager:
    """Handle disk persistence"""

    def __init__(self, mode: str = 'aof'):
        self.mode = mode  # 'aof' (append-only file) or 'rdb' (snapshot)
        self.aof_file = None
        self.rdb_file = None
        self.enabled = True

    async def log_command(self, *command):
        """Log command to AOF"""
        if self.mode != 'aof' or not self.enabled:
            return

        # Format command
        command_str = self.format_command(command)

        # Append to file
        self.aof_file.write(command_str.encode())

        # Optionally fsync
        # (trade-off between durability and performance)
        if self.sync_policy == 'always':
            self.aof_file.flush()
            os.fsync(self.aof_file.fileno())

    async def create_snapshot(self):
        """Create RDB snapshot"""
        if self.mode != 'rdb':
            return

        temp_file = f"{self.rdb_file}.temp"

        # Write snapshot in child process (fork)
        pid = os.fork()

        if pid == 0:
            # Child process
            self.write_snapshot(temp_file)
            os._exit(0)
        else:
            # Parent process
            os.waitpid(pid, 0)

            # Rename temp file
            os.rename(temp_file, self.rdb_file)

    def write_snapshot(self, filename: str):
        """Write current data to snapshot file"""
        with open(filename, 'wb') as f:
            # Write magic header
            f.write(b'REDIS0009')

            # Write all keys
            for key, entry in self.data_store.data.items():
                self.write_entry(f, key, entry)

            # Write EOF marker
            f.write(b'\xff')

    async def recover_from_aof(self):
        """Recover data from AOF file"""
        if not os.path.exists(self.aof_filename):
            return

        with open(self.aof_filename, 'r') as f:
            for line in f:
                command = self.parse_command(line)
                await self.apply_command(command)

    async def recover_from_rdb(self):
        """Recover data from RDB snapshot"""
        if not os.path.exists(self.rdb_file):
            return

        with open(self.rdb_file, 'rb') as f:
            # Read header
            magic = f.read(9)
            if magic != b'REDIS0009':
                raise ValueError("Invalid RDB file")

            # Read entries
            while True:
                entry = self.read_entry(f)
                if entry is None:  # EOF
                    break

                key, value = entry
                await self.data_store.set(key, value)
```

## 7. Data Structures & Storage

### Memory Layout

```
Cache Entry Structure:
┌────────────────────────────┐
│ Key (variable)             │
├────────────────────────────┤
│ Value Type (1 byte)        │
├────────────────────────────┤
│ Value (variable)           │
├────────────────────────────┤
│ TTL (8 bytes)              │
├────────────────────────────┤
│ Created Time (8 bytes)     │
├────────────────────────────┤
│ Access Count (4 bytes)     │
├────────────────────────────┤
│ Access Time (8 bytes)      │
└────────────────────────────┘

Total overhead: ~33 bytes per entry
```

## 8. Fault Tolerance & High Availability

### Failure Scenarios

```python
# Master failure: Promote slave
async def handle_master_failure(master_id: str):
    # Select slave with highest replication offset
    slave = select_best_slave(master_id)

    # Promote slave to master
    await promote_slave(slave)

    # Update cluster configuration
    await update_cluster_config(slave, role='master')

    # Notify clients
    await notify_clients_of_failover(slave)
```

### Split-Brain Prevention

```python
# Require quorum for write operations
async def set_with_quorum(key: str, value: bytes):
    nodes = consistent_hash.get_nodes(key, count=replication_factor)

    # Write to all nodes
    results = await asyncio.gather(
        *[node.set(key, value) for node in nodes],
        return_exceptions=True
    )

    # Require majority success
    successes = sum(1 for r in results if not isinstance(r, Exception))
    if successes < (replication_factor // 2) + 1:
        raise QuorumNotReachedException()
```

## 9. Monitoring & Observability

```python
# Key metrics
cache_hits = Counter('cache_hits_total')
cache_misses = Counter('cache_misses_total')
command_latency = Histogram('command_latency_seconds', labels=['command'])
memory_used = Gauge('memory_used_bytes')
evictions_total = Counter('evictions_total', labels=['reason'])
replication_lag = Gauge('replication_lag_seconds')
```

## 10. Scalability

- Add more nodes to cluster
- Increase replication factor for read-heavy workloads
- Use read replicas for read scaling
- Partition data across multiple independent clusters

## 11. Trade-offs

### In-Memory vs Persistent
- **In-memory**: Faster, but data lost on restart
- **Persistent**: Durable, but slower and more complex

### Replication: Sync vs Async
- **Sync**: Strong consistency, higher latency
- **Async**: Better performance, eventual consistency

### Eviction Policy
- **LRU**: Good for general use, moderate overhead
- **LFU**: Better for hot keys, higher overhead
- **Random**: Lowest overhead, unpredictable

## 12. Follow-up Questions

1. How would you implement transactions across multiple keys?
2. How would you handle cache stampede (thundering herd)?
3. How would you implement geo-replication?
4. How would you optimize for very large values (>1MB)?
5. How would you implement cache warming?
6. How would you handle hotspots (uneven key distribution)?
7. How would you implement Lua scripting support?
8. How would you optimize memory usage further?
9. How would you implement automatic cluster rebalancing?
10. How would you handle version conflicts in multi-master setup?
