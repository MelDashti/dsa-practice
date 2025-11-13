# Core Components: Hard Level

## Overview

Hard-level components are foundational building blocks of distributed systems. These problems require deep understanding of distributed algorithms, consistency guarantees, and performance optimization. Mastering these components is essential for senior/staff+ engineers designing large-scale distributed systems.

## Problems Overview

### 1. Distributed Unique ID Generator (unique_id_generator.md)
**Design Twitter Snowflake-like ID generation**

Generate globally unique, time-sortable IDs at massive scale:

**Requirements:**
- Unique across all nodes
- Time-ordered (sortable)
- 64-bit integer (fits in long)
- 10K+ IDs per second per node
- No central coordination

**Twitter Snowflake Design:**
```
64-bit ID Structure:
┌─────────────┬──────────┬─────────────┬─────────────┐
│  Timestamp  │Machine ID│Datacenter ID│  Sequence   │
│   41 bits   │  10 bits │   5 bits    │   12 bits   │
└─────────────┴──────────┴─────────────┴─────────────┘

Components:
- Timestamp: Milliseconds since epoch (69 years)
- Machine ID: Unique server identifier (32 servers)
- Datacenter ID: Datacenter identifier (32 DCs)
- Sequence: Counter for same millisecond (4096 IDs)
```

**Alternatives:**
- **UUID:** 128-bit, no ordering, distributed generation
- **MongoDB ObjectID:** 96-bit, time + machine + counter
- **Instagram Sharding:** Database auto-increment + shard ID
- **Database Sequence:** Centralized, single point of failure

**Key Challenges:**
- Clock synchronization (NTP drift)
- Machine ID assignment
- Sequence number exhaustion
- Time going backwards

**Scale:** 100K IDs/sec globally, trillion IDs

**Real-World:** Twitter Snowflake, Instagram, Discord

---

### 2. Consistent Hashing (consistent_hashing.md)
**Design distributed caching with minimal reshuffling**

Distribute data across cache servers with minimal rebalancing:

**Problem with Simple Hashing:**
```
server = hash(key) % N

Adding/removing server: Most keys need to move
10 servers → 11 servers: 91% of keys rehashed!
```

**Consistent Hashing Solution:**
```
Hash Ring (0 to 2^32-1):
┌─────────────────────────────────────────┐
│     S1    S2         S3       S1'       │
│  ●─────●──────────●─────────●──────●   │
│     K1  K2       K3      K4            │
└─────────────────────────────────────────┘

Adding server: Only K/N keys move (K = total keys)
Removing server: Only keys from that server move
```

**Enhancements:**
- **Virtual Nodes:** Each server placed at multiple positions (150 vnodes typical)
- **Bounded Loads:** Prevent hotspot with max load cap
- **Jump Consistent Hash:** O(1) computation, no memory

**Key Challenges:**
- Uneven distribution (virtual nodes solve)
- Hotspot servers
- Adding/removing multiple servers simultaneously

**Scale:** 1000+ cache servers, billions of keys

**Real-World:** Amazon DynamoDB, Cassandra, Memcached

---

### 3. Distributed Lock (distributed_lock.md)
**Design distributed lock service (Chubby/Redlock)**

Provide mutual exclusion in distributed systems:

**Use Cases:**
- Leader election
- Prevent duplicate job execution
- Resource allocation (parking spot, inventory)
- Critical section protection

**Approaches:**

**1. Database-based Lock:**
```sql
-- Try to acquire lock
INSERT INTO locks (resource_id, owner, expires_at)
VALUES ('resource1', 'server1', NOW() + INTERVAL 30 SECOND)
ON CONFLICT DO NOTHING;

-- Release lock
DELETE FROM locks
WHERE resource_id = 'resource1' AND owner = 'server1';
```

**2. Redis Redlock Algorithm:**
```python
def acquire_lock(resource, ttl):
    # Try to acquire lock on N/2+1 Redis instances
    token = random_token()
    start_time = time()

    locked_instances = 0
    for redis in redis_instances:
        if redis.set(resource, token, nx=True, ex=ttl):
            locked_instances += 1

    elapsed = time() - start_time
    if locked_instances >= N/2 + 1 and elapsed < ttl:
        return token  # Lock acquired

    # Failed - release locks
    release_lock(resource, token)
    return None
```

**3. Zookeeper/etcd-based Lock:**
```
1. Create ephemeral sequential node
2. Get children of lock path
3. If my node is smallest → Lock acquired
4. Otherwise, watch node before mine
5. When that node deleted → Try again
```

**Key Challenges:**
- Network partitions (split-brain)
- Clock drift
- Deadlocks
- Lock holder crashes (need TTL)
- Fencing tokens (prevent stale lock holders)

**Safety Requirements:**
1. **Mutual Exclusion:** Only one client holds lock
2. **Deadlock Free:** Eventually can acquire lock
3. **Fault Tolerance:** Works despite failures

**Scale:** 10K lock operations/sec, 1000s of resources

**Real-World:** Google Chubby, Apache Zookeeper, etcd

---

## Complexity Comparison

| Component | Primary Challenge | Failure Mode | Correctness |
|-----------|------------------|--------------|-------------|
| **ID Generator** | Time sync, uniqueness | Duplicate IDs | Must be unique |
| **Consistent Hashing** | Load distribution | Hotspots | Best-effort balance |
| **Distributed Lock** | Safety guarantees | Split-brain | Must prevent double-locking |

## Deep Dive: Distributed Lock Correctness

### The Martin Kleppmann vs Salvatore Sanfilippo Debate

**Martin Kleppmann's Critique of Redlock:**
```
Scenario:
1. Client 1 acquires lock from 3/5 Redis nodes
2. Client 1 GC pause (stop-the-world)
3. Lock expires during GC pause
4. Client 2 acquires lock from 3/5 nodes
5. Client 1 resumes, thinks it has lock
6. Both clients in critical section! 💥

Problem: Redlock doesn't provide fencing tokens
```

**Solution: Fencing Tokens**
```
1. Lock service issues monotonic token (1, 2, 3, ...)
2. Client includes token in all operations
3. Resource server rejects operations with old tokens

Example:
Client 1 gets lock with token=33
Client 1 pauses (GC)
Client 2 gets lock with token=34
Client 1 resumes, tries operation with token=33
Server rejects (34 > 33) ✅ Safety preserved
```

### Distributed Lock Hierarchy

| Guarantee | Algorithm | Complexity | Use Case |
|-----------|-----------|------------|----------|
| **Best Effort** | Single Redis | Simple | Rate limiting, caching |
| **Strong** | Redlock (5 Redis) | Medium | Job scheduling |
| **Linearizable** | Zookeeper/etcd | Complex | Leader election |

## Advanced Algorithms

### Twitter Snowflake Implementation

```python
class SnowflakeIDGenerator:
    def __init__(self, datacenter_id, machine_id):
        self.datacenter_id = datacenter_id
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = 0

        # Configuration
        self.epoch = 1288834974657  # Twitter epoch
        self.datacenter_id_bits = 5
        self.machine_id_bits = 5
        self.sequence_bits = 12

        # Max values
        self.max_datacenter_id = (1 << self.datacenter_id_bits) - 1
        self.max_machine_id = (1 << self.machine_id_bits) - 1
        self.max_sequence = (1 << self.sequence_bits) - 1

        # Bit shifts
        self.machine_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.machine_id_bits
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits + self.datacenter_id_bits

    def next_id(self):
        timestamp = self._current_millis()

        # Handle clock moving backwards
        if timestamp < self.last_timestamp:
            raise ClockMovedBackwardsError(
                f"Clock moved backwards. Refusing to generate ID"
            )

        # Same millisecond - increment sequence
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.max_sequence
            if self.sequence == 0:
                # Sequence exhausted - wait for next millisecond
                timestamp = self._wait_next_millis(self.last_timestamp)
        else:
            # New millisecond - reset sequence
            self.sequence = 0

        self.last_timestamp = timestamp

        # Generate ID
        id = ((timestamp - self.epoch) << self.timestamp_shift) | \
             (self.datacenter_id << self.datacenter_id_shift) | \
             (self.machine_id << self.machine_id_shift) | \
             self.sequence

        return id

    def _current_millis(self):
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp
```

### Consistent Hashing with Virtual Nodes

```python
import bisect
import hashlib

class ConsistentHash:
    def __init__(self, nodes, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []

        for node in nodes:
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        """Add node with virtual nodes"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = node
            bisect.insort(self.sorted_keys, hash_value)

    def remove_node(self, node):
        """Remove node and its virtual nodes"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)
            del self.ring[hash_value]
            self.sorted_keys.remove(hash_value)

    def get_node(self, key):
        """Get node for key"""
        if not self.ring:
            return None

        hash_value = self._hash(key)

        # Find first node >= hash_value
        idx = bisect.bisect_right(self.sorted_keys, hash_value)
        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]

    def get_nodes(self, key, count=3):
        """Get N nodes for replication"""
        if len(self.ring) < count:
            return list(set(self.ring.values()))

        hash_value = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_value)

        nodes = []
        seen = set()

        while len(nodes) < count:
            if idx >= len(self.sorted_keys):
                idx = 0

            node = self.ring[self.sorted_keys[idx]]
            if node not in seen:
                nodes.append(node)
                seen.add(node)

            idx += 1

        return nodes
```

## Production War Stories

### Snowflake ID Generation Failures

**Incident: Clock Skew**
```
Problem: NTP sync moved clock backwards 2 seconds
Impact: ID generator refused to generate IDs
Duration: 2 minutes until clock caught up

Prevention:
- Monitor clock drift
- Allow small backwards drift (< 5ms)
- Emergency fallback to UUID
```

**Incident: Sequence Exhaustion**
```
Problem: Burst traffic exceeded 4096 IDs/millisecond
Impact: Generator blocked waiting for next millisecond
Duration: Microsecond-level delays

Prevention:
- More sequence bits (13 bits = 8192 IDs/ms)
- Spread load across multiple generators
- Pre-generate ID batches
```

### Consistent Hashing Pitfalls

**Incident: Uneven Distribution**
```
Problem: Used simple hashing without virtual nodes
Impact: 1 server got 5x more keys than others

Solution:
- Implemented 150 virtual nodes per server
- Distribution variance reduced from 5x to 1.1x
```

### Distributed Lock Horror Stories

**Incident: Split-Brain**
```
Problem: Network partition, both partitions elected leader
Impact: Duplicate job execution, data corruption

Prevention:
- Use consensus-based locks (Zookeeper/etcd)
- Implement fencing tokens
- Monitor lock holder health
```

## Interview Strategies

### ID Generator
**Q:** "How would you generate unique IDs without coordination?"

**Framework:**
1. **Requirements:** Unique, time-sortable, 64-bit
2. **Options:** Snowflake, UUID, database sequence
3. **Chosen:** Snowflake (compact, sortable)
4. **Challenges:** Clock sync, machine ID
5. **Solutions:** NTP monitoring, allow small drift

### Consistent Hashing
**Q:** "How do you handle hotspot keys in consistent hashing?"

**Solutions:**
1. **Virtual Nodes:** Better distribution
2. **Bounded Loads:** Cap per-server load
3. **Key Splitting:** Split hot keys
4. **Replication:** Replicate hot data

### Distributed Lock
**Q:** "Is Redlock safe?"

**Nuanced Answer:**
- **Best effort:** Yes, good enough for most cases
- **Strict safety:** No, need fencing tokens
- **Alternative:** Use Zookeeper/etcd for critical sections
- **Trade-off:** Simplicity (Redlock) vs Safety (Zookeeper)

## Common Mistakes

### ID Generator
❌ Using random IDs (not sortable)
❌ 32-bit IDs (too small)
❌ No handling of clock drift

✅ 64-bit with timestamp
✅ Monitor NTP sync
✅ Fallback strategy

### Consistent Hashing
❌ No virtual nodes (uneven distribution)
❌ Not handling node failures
❌ Ignoring hotspot keys

✅ 150+ virtual nodes
✅ Replica nodes for availability
✅ Monitor key distribution

### Distributed Lock
❌ No lock timeout (deadlock)
❌ No heartbeat (holder crashes)
❌ No fencing (double-locking)

✅ Mandatory TTL
✅ Periodic lock refresh
✅ Fencing tokens

## Real-World Scale

| System | Component | Scale | Details |
|--------|-----------|-------|---------|
| **Twitter** | Snowflake | 100K IDs/sec | 41-bit timestamp = 69 years |
| **Instagram** | ID Generation | 25K photos/sec | DB sharding + auto-increment |
| **Amazon** | Consistent Hashing | 1000+ nodes | DynamoDB partitioning |
| **Google** | Distributed Lock | 10K locks/sec | Chubby (Paxos-based) |

## Success Criteria

You've mastered hard-level components when you can:
- ✅ Implement Snowflake ID generator from scratch
- ✅ Build consistent hashing with virtual nodes
- ✅ Explain distributed lock correctness guarantees
- ✅ Handle clock skew and network partitions
- ✅ Make safety vs. performance trade-offs
- ✅ Discuss production failure scenarios

## Additional Resources

### Papers
- **Consistent Hashing:** "Consistent Hashing and Random Trees" (Karger et al., 1997)
- **Distributed Locks:** "How to do distributed locking" (Martin Kleppmann, 2016)
- **Redlock:** "Is Redlock safe?" (antirez response)

### Implementations
- **Snowflake:** Twitter's original implementation (Scala)
- **Instagram:** Blog post on sharding and ID generation
- **Dynamo:** Amazon's consistent hashing paper

### Tools
- **Curator:** Zookeeper distributed lock recipes
- **Redlock:** Redis-based distributed lock
- **etcd:** Go implementation with fencing

---

**Difficulty Rating:** ⭐⭐⭐⭐⭐ (5/5) - Requires deep distributed systems expertise

**Interview Frequency:** 40% of senior+ interviews, 80% of staff+ interviews

**Estimated Study Time:** 2-3 weeks for all three components (with implementation and testing)

**Career Impact:** Mastering these components is often the difference between senior and staff+ level engineers.
