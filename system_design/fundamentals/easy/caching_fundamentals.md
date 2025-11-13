# Caching Fundamentals: Cache Strategies and Eviction Policies

## 1. Problem Statement

How do we reduce latency and improve system performance by storing frequently accessed data in fast-access storage? Caching is one of the most effective ways to improve application performance, reduce database load, and provide better user experience.

## 2. Requirements

### Functional Requirements
- Store frequently accessed data for quick retrieval
- Automatically evict old or unused data when cache is full
- Support different data types (strings, objects, binary)
- Provide cache invalidation mechanisms
- Handle cache misses gracefully

### Non-functional Requirements
- Low latency: <1ms for cache hits
- High throughput: 100K+ operations/second
- High cache hit rate: >80%
- Minimal memory footprint
- Thread-safe operations
- Configurable TTL (Time To Live)

## 3. Capacity Estimation

### Example: E-commerce Product Catalog

**Traffic:**
- 10M daily active users
- 50 product views per user per day
- 500M total product views per day
- ~5,800 views per second

**Data Size:**
- Average product data: 2 KB
- Total unique products: 1M
- Full catalog size: 2 GB
- Cache 20% hot products: 400 MB
- With metadata overhead: ~500 MB

**Memory Calculation:**
```
Cache entries: 200,000 products (20% of catalog)
Per entry: 2 KB product data + 200 bytes metadata
Total: 200,000 * 2.2 KB = 440 MB
Add 20% buffer: 528 MB
Round up: 1 GB cache size
```

## 4. High-Level Design

### Cache Architecture Layers

```
┌─────────────────────────────────────────────┐
│           Client Application                │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│         CDN Cache (Edge Servers)            │  ← Layer 1: Geographic
│         TTL: 1 hour                         │
└────────────────┬────────────────────────────┘
                 │ Miss
                 ↓
┌─────────────────────────────────────────────┐
│      Application Cache (Redis/Memcached)    │  ← Layer 2: Distributed
│      TTL: 15 minutes                        │
└────────────────┬────────────────────────────┘
                 │ Miss
                 ↓
┌─────────────────────────────────────────────┐
│      Local Cache (In-Memory)                │  ← Layer 3: Local
│      TTL: 5 minutes                         │
└────────────────┬────────────────────────────┘
                 │ Miss
                 ↓
┌─────────────────────────────────────────────┐
│         Database Query Cache                │  ← Layer 4: Database
└────────────────┬────────────────────────────┘
                 │ Miss
                 ↓
┌─────────────────────────────────────────────┐
│         Primary Database                    │
└─────────────────────────────────────────────┘
```

## 5. API Design

### Cache Operations

```
GET /api/v1/cache/{key}
Response: {
  "key": "product:12345",
  "value": {"id": 12345, "name": "Laptop", "price": 999.99},
  "ttl": 3600,
  "hit": true
}

PUT /api/v1/cache/{key}
Request: {
  "value": {"id": 12345, "name": "Laptop", "price": 999.99},
  "ttl": 3600
}

DELETE /api/v1/cache/{key}
Response: {
  "key": "product:12345",
  "deleted": true
}

POST /api/v1/cache/invalidate
Request: {
  "pattern": "product:*",
  "tags": ["electronics", "featured"]
}

GET /api/v1/cache/stats
Response: {
  "total_requests": 1000000,
  "cache_hits": 850000,
  "cache_misses": 150000,
  "hit_rate": 85.0,
  "evictions": 5000,
  "memory_used_mb": 450,
  "memory_limit_mb": 1024
}
```

## 6. Database Schema

### Cache Metadata (for persistent cache or cache analytics)

```sql
CREATE TABLE cache_entries (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_value BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    access_count INT DEFAULT 0,
    last_accessed_at TIMESTAMP,
    size_bytes INT,
    INDEX idx_expires (expires_at),
    INDEX idx_last_accessed (last_accessed_at)
);

CREATE TABLE cache_statistics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cache_hits BIGINT,
    cache_misses BIGINT,
    hit_rate DECIMAL(5,2),
    eviction_count INT,
    memory_usage_mb INT,
    avg_access_time_ms DECIMAL(8,3),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE cache_invalidation_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cache_key VARCHAR(255),
    invalidation_type ENUM('manual', 'ttl', 'eviction', 'update'),
    reason TEXT
);
```

## 7. Detailed Component Design

### Caching Strategies

#### 1. Cache-Aside (Lazy Loading)

**Pattern:**
```python
def get_data(key):
    # Try to get from cache
    data = cache.get(key)

    if data is None:  # Cache miss
        # Get from database
        data = database.query(key)
        # Store in cache
        cache.set(key, data, ttl=3600)

    return data
```

**Advantages:**
- Only requested data is cached
- Cache doesn't get filled with unused data
- Resilient: cache failure doesn't crash system

**Disadvantages:**
- Initial request is slow (cache miss penalty)
- Stale data possible if not invalidated properly
- Every cache miss = database hit

**Best For:** Read-heavy applications, unpredictable access patterns

#### 2. Write-Through Cache

**Pattern:**
```python
def update_data(key, value):
    # Write to database first
    database.update(key, value)
    # Then update cache
    cache.set(key, value, ttl=3600)

    return value
```

**Advantages:**
- Cache always has latest data
- No cache inconsistency
- Write penalty is acceptable for read-heavy loads

**Disadvantages:**
- Write latency increased
- Wasted writes for rarely accessed data
- Still need cache-aside for reads

**Best For:** Write operations where consistency is critical

#### 3. Write-Behind (Write-Back) Cache

**Pattern:**
```python
def update_data(key, value):
    # Write to cache immediately
    cache.set(key, value)
    # Queue database write for later
    write_queue.enqueue(key, value)

    return value

# Background worker
def flush_to_database():
    while True:
        batch = write_queue.dequeue_batch(100)
        database.batch_update(batch)
        time.sleep(1)
```

**Advantages:**
- Low write latency
- Can batch database writes
- Reduces database load

**Disadvantages:**
- Risk of data loss if cache crashes
- Complex to implement
- Eventual consistency issues

**Best For:** Write-heavy applications, logging systems

#### 4. Read-Through Cache

**Pattern:**
```python
# Cache layer handles database queries transparently
def get_data(key):
    # Cache checks itself, queries DB if needed
    return cache.get(key)  # Cache internally handles miss

# Inside cache implementation
def cache_get_internal(key):
    data = self.storage.get(key)
    if data is None:
        data = self.database.query(key)
        self.storage.set(key, data)
    return data
```

**Advantages:**
- Cleaner application code
- Cache logic centralized
- Automatic cache population

**Disadvantages:**
- Tight coupling with data source
- First access still slow
- Cache must know how to fetch data

**Best For:** Centralized caching layer, microservices

### Cache Eviction Policies

#### 1. LRU (Least Recently Used)

**Implementation:**
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        self.head = Node(0, 0)  # Dummy head
        self.tail = Node(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.value
        return None

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self._add_to_head(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            # Remove least recently used
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

**Characteristics:**
- Evicts least recently accessed item
- Time Complexity: O(1) for get/put
- Space Complexity: O(n)

**Best For:** General purpose caching, temporal locality

#### 2. LFU (Least Frequently Used)

**Characteristics:**
- Evicts item with lowest access count
- Better for items with consistent access patterns
- More complex to implement efficiently

**Best For:** Long-term caching, stable access patterns

#### 3. FIFO (First In, First Out)

**Characteristics:**
- Evicts oldest item regardless of access
- Simple to implement
- Doesn't consider access patterns

**Best For:** Simple caching needs, queue-like data

#### 4. TTL (Time To Live)

**Characteristics:**
- Items expire after fixed time
- Can combine with other policies
- Prevents stale data

**Best For:** Time-sensitive data, reducing cache size

#### 5. Random Replacement

**Characteristics:**
- Randomly evicts an item
- Simple and fast
- Surprisingly effective in some scenarios

**Best For:** When access patterns are truly random

### Cache Eviction Policy Comparison

```
Access Pattern: A, B, C, D, A, E, F, G, A, H

Cache Size: 4

LRU Final State: [A, H, G, F]
- Evicts based on time since last access
- A kept because accessed recently

LFU Final State: [A, H, G, F] (assuming equal frequency for most)
- Evicts based on total access count
- A kept because accessed 3 times

FIFO Final State: [E, F, G, H]
- Evicts in order of insertion
- A evicted despite multiple accesses

Random Final State: [Unpredictable]
- Could be any combination
```

## 8. Trade-offs and Considerations

### Cache Hit Ratio

**Formula:**
```
Hit Ratio = Cache Hits / (Cache Hits + Cache Misses)
```

**Example:**
```
1,000,000 requests
850,000 cache hits
150,000 cache misses
Hit Ratio = 850,000 / 1,000,000 = 85%
```

**Improving Hit Ratio:**
1. Increase cache size
2. Better eviction policy
3. Longer TTL (if acceptable)
4. Cache warm-up strategies
5. Predictive caching

### Cache Stampede Problem

**Problem:**
```
Time 0: Cache expires
Time 1: 1000 concurrent requests arrive
Time 2: All 1000 requests miss cache
Time 3: All 1000 requests hit database simultaneously
Result: Database overload
```

**Solutions:**

1. **Probabilistic Early Expiration:**
```python
def get_with_early_expiration(key, ttl, beta=1.0):
    data, expiry = cache.get_with_expiry(key)

    if data is None:
        return refresh_cache(key, ttl)

    # Probabilistically refresh before expiry
    now = time.time()
    time_left = expiry - now
    if time_left < 0:
        return refresh_cache(key, ttl)

    # XFetch algorithm
    if random.random() < beta * (1.0 / time_left):
        return refresh_cache(key, ttl)

    return data
```

2. **Lock-Based Prevention:**
```python
def get_with_lock(key):
    data = cache.get(key)
    if data is not None:
        return data

    lock_key = f"lock:{key}"
    if cache.set_if_not_exists(lock_key, "locked", ttl=10):
        # This request got the lock, refresh cache
        try:
            data = database.query(key)
            cache.set(key, data, ttl=3600)
            return data
        finally:
            cache.delete(lock_key)
    else:
        # Another request is refreshing, wait and retry
        time.sleep(0.1)
        return get_with_lock(key)
```

### Cache Consistency

**Scenarios:**

1. **Database Update, Cache Not Updated:**
```
Result: Stale data served from cache
Solution: Write-through or cache invalidation
```

2. **Concurrent Updates:**
```
Thread 1: Read from DB (v1)
Thread 2: Update DB (v2)
Thread 2: Update cache (v2)
Thread 1: Update cache (v1) ← Wrong!
Result: Cache has old value

Solution: Versioning or atomic operations
```

3. **Distributed Cache Consistency:**
```
Server 1 cache: product:123 = {price: $10}
Server 2 cache: product:123 = {price: $15}
Result: Different users see different prices

Solution: Centralized cache (Redis) or cache invalidation pub/sub
```

## 9. Scalability & Bottlenecks

### Scaling Cache

#### Single Instance Limitations
- Memory: Typically 64-128 GB max
- Network: 10 Gbps bottleneck
- CPU: Single-threaded operations limited

#### Distributed Caching

**Consistent Hashing:**
```python
class DistributedCache:
    def __init__(self, nodes):
        self.ring = {}
        self.sorted_keys = []
        for node in nodes:
            for i in range(150):  # Virtual nodes
                hash_key = self._hash(f"{node}:{i}")
                self.ring[hash_key] = node
                self.sorted_keys.append(hash_key)
        self.sorted_keys.sort()

    def get_node(self, key):
        hash_key = self._hash(key)
        # Binary search for the first node >= hash_key
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]
```

**Benefits:**
- Minimal key redistribution on node add/remove
- Load balancing across nodes
- Fault tolerance

### Cache Monitoring Metrics

```python
class CacheMetrics:
    """Track cache performance metrics"""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.access_times = []

    def record_hit(self, access_time_ms):
        self.hits += 1
        self.access_times.append(access_time_ms)

    def record_miss(self, access_time_ms):
        self.misses += 1
        self.access_times.append(access_time_ms)

    def get_stats(self):
        total = self.hits + self.misses
        return {
            'hit_rate': self.hits / total if total > 0 else 0,
            'miss_rate': self.misses / total if total > 0 else 0,
            'avg_access_time_ms': sum(self.access_times) / len(self.access_times),
            'eviction_rate': self.evictions / total if total > 0 else 0
        }
```

**Key Metrics to Monitor:**
1. Hit rate / Miss rate
2. Eviction rate
3. Memory usage
4. Access latency (p50, p95, p99)
5. Cache size / entry count
6. Expired keys
7. Network bandwidth (for distributed cache)

## 10. Follow-up Questions

1. **How do you handle cache warm-up after deployment?**
   - Pre-populate cache with most accessed data
   - Gradual traffic ramp-up
   - Background job to load hot data
   - Use previous cache snapshot

2. **What's the difference between Redis and Memcached?**
   - Redis: Supports complex data structures, persistence, pub/sub
   - Memcached: Simple key-value, no persistence, slightly faster for simple operations
   - Redis: Single-threaded (multi-threaded in Redis 6+)
   - Memcached: Multi-threaded

3. **How do you invalidate cache in a microservices architecture?**
   - Event-driven invalidation (pub/sub)
   - Cache tags/dependencies
   - TTL-based expiration
   - Version-based cache keys
   - Central cache invalidation service

4. **When should you NOT use caching?**
   - Data must always be absolutely fresh
   - Highly personalized data with low reuse
   - Very high write-to-read ratio
   - Limited memory resources
   - Data size too large for cache

5. **How do you test cache performance?**
   - Load testing with realistic traffic patterns
   - Measure hit rates under different scenarios
   - Benchmark different eviction policies
   - Simulate cache failures
   - Monitor production metrics

6. **What are cache aside pattern drawbacks?**
   - Cache miss penalty on every first access
   - Potential for stale data
   - Code complexity (application manages cache)
   - Race conditions on concurrent updates

7. **How do you size a cache appropriately?**
   - Analyze access patterns (Pareto principle: 80/20 rule)
   - Calculate working set size
   - Consider cost vs. benefit (diminishing returns)
   - Monitor hit rates at different sizes
   - Factor in memory costs

8. **What is cache penetration and how to prevent it?**
   - **Problem:** Queries for non-existent keys always hit DB
   - **Solutions:**
     - Bloom filters for existence check
     - Cache null/empty results with short TTL
     - Request validation/sanitization
     - Rate limiting on suspicious patterns

9. **How do you handle cache in multi-region deployments?**
   - Regional caches with eventual consistency
   - Geographic routing to nearest cache
   - Cache replication across regions
   - Consider data sovereignty laws
   - Accept stale data in remote regions

10. **What's the impact of serialization on cache performance?**
    - JSON: Human-readable, slower, larger
    - Protocol Buffers: Fast, compact, requires schema
    - MessagePack: Fast, compact, schema-less
    - Choose based on: network bandwidth, CPU, interoperability needs
