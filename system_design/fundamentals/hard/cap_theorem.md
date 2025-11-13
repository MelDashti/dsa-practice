# CAP Theorem: Consistency, Availability, Partition Tolerance

## 1. Problem Statement

In a distributed system, how do we balance consistency, availability, and partition tolerance? The CAP theorem states that a distributed system can only provide two out of three guarantees simultaneously: Consistency, Availability, and Partition tolerance. Understanding these trade-offs is crucial for designing distributed systems.

## 2. Requirements

### Functional Requirements
- Handle network partitions gracefully
- Provide consistent or available operations (based on choice)
- Support distributed data storage
- Enable trade-off configuration per use case
- Handle failure scenarios

### Non-functional Requirements
- **Consistency:** All nodes see same data at same time
- **Availability:** Every request receives response (success/failure)
- **Partition Tolerance:** System operates despite network failures
- **Recovery Time:** <5 minutes after partition heals
- **Data Loss Tolerance:** Configurable based on consistency model

## 3. Capacity Estimation

### Example: Distributed Key-Value Store

**Infrastructure:**
- 5 data centers globally
- 100 nodes per data center = 500 total nodes
- Network partition probability: 0.1% per hour
- Expected partitions per day: ~12

**Consistency Models Impact:**
```
Strong Consistency (CP):
- Write latency: 50-200ms (cross-region consensus)
- Availability during partition: Reduced (minority partition unavailable)
- Use case: Financial transactions

Eventual Consistency (AP):
- Write latency: 5-10ms (local write)
- Availability during partition: High (all partitions accept writes)
- Convergence time: Seconds to minutes
- Use case: Social media feeds

Tuneable Consistency:
- Read quorum (R): 2 nodes
- Write quorum (W): 2 nodes
- Total replicas (N): 3 nodes
- Strong consistency when: R + W > N
```

## 4. High-Level Design

### CAP Triangle

```
              Consistency (C)
                    /\
                   /  \
                  /    \
                 /  CA  \
                /        \
               /          \
              /     CP     \
             /              \
            /                \
           /        AP        \
          /____________________\
    Partition            Availability (A)
    Tolerance (P)
```

### System Architecture for Different CAP Choices

```
CP SYSTEM (Consistency + Partition Tolerance):
┌────────────────────────────────────────┐
│         Client Request                 │
└────────────┬───────────────────────────┘
             │
    ┌────────▼────────┐
    │  Leader Node    │  ← Only accepts writes
    │  (Paxos/Raft)   │     Ensures consensus
    └────┬─────┬──────┘
         │     │
    ┌────▼─┐ ┌▼────┐
    │Follower│Follower│    ← Replicate from leader
    └────────┘└──────┘

During Partition:
- Minority partition: UNAVAILABLE (rejects writes)
- Majority partition: AVAILABLE (accepts writes)

AP SYSTEM (Availability + Partition Tolerance):
┌──────────────────────────────────────────┐
│         Client Request                   │
└────┬─────────────┬─────────────┬─────────┘
     │             │             │
  ┌──▼──┐       ┌──▼──┐      ┌──▼──┐
  │Node1│       │Node2│      │Node3│  ← All accept writes
  └─────┘       └─────┘      └─────┘

During Partition:
- All partitions: AVAILABLE (accept writes)
- Conflicts: Resolved via versioning/CRDTs
- Eventually consistent after partition heals
```

## 5. API Design

### Configuration API for CAP Trade-offs

```
POST /api/v1/cluster/config
Request: {
  "consistency_model": "tunable",
  "read_consistency": "quorum",      // "one", "quorum", "all"
  "write_consistency": "quorum",     // "one", "quorum", "all"
  "replication_factor": 3,
  "partition_strategy": "prefer_availability"  // or "prefer_consistency"
}

GET /api/v1/data/{key}
Headers: {
  "Consistency-Level": "strong"  // "strong", "eventual", "quorum"
}
Response: {
  "key": "user:123",
  "value": {"name": "John", "age": 30},
  "version": "v5",
  "consistency_achieved": "strong",
  "nodes_queried": 3
}

PUT /api/v1/data/{key}
Headers: {
  "Consistency-Level": "quorum"
}
Request: {
  "value": {"name": "John", "age": 31},
  "if_version": "v5"  // Conditional write
}

GET /api/v1/cluster/health
Response: {
  "total_nodes": 5,
  "healthy_nodes": 5,
  "partitioned": false,
  "consistency_mode": "CP",
  "writable_partitions": 1,
  "read_only_partitions": 0
}

POST /api/v1/partition/simulate
Request: {
  "partition_groups": [
    ["node1", "node2"],
    ["node3", "node4", "node5"]
  ]
}
Response: {
  "partition_id": "part-123",
  "writable_nodes": ["node3", "node4", "node5"],  // Majority
  "readonly_nodes": ["node1", "node2"]            // Minority
}
```

## 6. Database Schema

### Metadata for Distributed System

```sql
CREATE TABLE cluster_nodes (
    node_id VARCHAR(50) PRIMARY KEY,
    host VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    datacenter VARCHAR(50),
    status ENUM('active', 'failed', 'partitioned', 'recovering'),
    last_heartbeat TIMESTAMP,
    partition_group VARCHAR(50), -- Nodes in same partition
    role ENUM('leader', 'follower', 'candidate'),
    INDEX idx_status (status),
    INDEX idx_partition (partition_group)
);

CREATE TABLE data_versions (
    key_hash VARCHAR(64),
    node_id VARCHAR(50),
    version BIGINT,
    value BLOB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vector_clock JSON, -- For conflict detection
    PRIMARY KEY (key_hash, node_id, version),
    INDEX idx_key_version (key_hash, version)
);

CREATE TABLE replication_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    key_hash VARCHAR(64),
    operation ENUM('PUT', 'DELETE'),
    value BLOB,
    version BIGINT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_node VARCHAR(50),
    replicated_to JSON, -- Array of node_ids
    INDEX idx_key (key_hash),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE conflict_resolution_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    key_hash VARCHAR(64),
    conflict_detected_at TIMESTAMP,
    conflicting_versions JSON,
    resolution_strategy ENUM('LWW', 'version_vector', 'application', 'merge'),
    resolved_version BIGINT,
    resolved_at TIMESTAMP,
    INDEX idx_key_time (key_hash, conflict_detected_at)
);
```

## 7. Detailed Component Design

### CP System: Strong Consistency with Raft

```python
class RaftNode:
    """
    CP system implementation using Raft consensus
    Sacrifices availability for consistency during partitions
    """

    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = 'follower'  # follower, candidate, or leader
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0

    async def write(self, key, value):
        """
        Write operation - only succeeds on leader with majority
        """
        if self.state != 'leader':
            # Redirect to leader
            leader = self.get_current_leader()
            if not leader:
                raise UnavailableError("No leader available - system unavailable")
            return await leader.write(key, value)

        # Append to log
        entry = LogEntry(
            term=self.current_term,
            key=key,
            value=value,
            index=len(self.log)
        )
        self.log.append(entry)

        # Replicate to followers
        successful_replicas = 1  # Self
        for peer in self.peers:
            try:
                success = await peer.append_entries([entry], timeout=1.0)
                if success:
                    successful_replicas += 1
            except TimeoutError:
                # Peer unreachable
                pass

        # Check if we have majority
        if successful_replicas >= (len(self.peers) + 1) // 2 + 1:
            # Majority achieved - commit
            self.commit_index = entry.index
            await self.apply_to_state_machine(entry)
            return True
        else:
            # Cannot achieve majority
            # In CP system: Reject write (unavailable)
            self.log.pop()  # Remove uncommitted entry
            raise UnavailableError("Cannot achieve majority - write rejected")

    async def read(self, key):
        """
        Read operation - ensure reading committed data
        """
        if self.state != 'leader':
            # Can read from follower (might be slightly stale)
            # Or redirect to leader for strong consistency
            return self.state_machine.get(key)

        # Leader must verify it's still leader (read barrier)
        if not await self.verify_leadership():
            raise UnavailableError("Lost leadership - cannot guarantee consistency")

        return self.state_machine.get(key)

    async def verify_leadership(self):
        """
        Verify still have majority (prevent split-brain reads)
        """
        responses = 1  # Self
        for peer in self.peers:
            try:
                if await peer.heartbeat(self.current_term, timeout=0.5):
                    responses += 1
            except:
                pass

        return responses >= (len(self.peers) + 1) // 2 + 1
```

### AP System: High Availability with Eventual Consistency

```python
class DynamoStyleNode:
    """
    AP system implementation (Dynamo-style)
    Prioritizes availability over consistency
    """

    def __init__(self, node_id, N=3, R=2, W=2):
        self.node_id = node_id
        self.N = N  # Replication factor
        self.R = R  # Read quorum
        self.W = W  # Write quorum
        self.data = {}
        self.vector_clock = VectorClock()

    async def write(self, key, value, context=None):
        """
        Write operation - accepts write even during partition
        """
        # Determine replica nodes for this key
        replicas = self.get_replicas_for_key(key)

        # Generate new version
        new_version = self.vector_clock.increment(self.node_id)
        versioned_value = VersionedValue(
            value=value,
            version=new_version,
            timestamp=time.time()
        )

        # Write locally
        self.data[key] = versioned_value
        successful_writes = 1

        # Attempt to write to W-1 other nodes
        for replica in replicas[:self.W-1]:
            try:
                success = await replica.put(
                    key,
                    versioned_value,
                    timeout=0.1  # Short timeout
                )
                if success:
                    successful_writes += 1
            except:
                # Replica unreachable - continue anyway (sloppy quorum)
                pass

        # In AP system: Accept write even without full quorum
        if successful_writes >= self.W:
            return {'status': 'success', 'consistent': True}
        else:
            # Didn't reach quorum, but still accepted
            # Will sync via anti-entropy later
            return {'status': 'success', 'consistent': False, 'pending_sync': True}

    async def read(self, key):
        """
        Read operation - always returns a value
        """
        replicas = self.get_replicas_for_key(key)

        # Read from R replicas
        responses = []

        # Include self
        if key in self.data:
            responses.append(self.data[key])

        # Read from R-1 others
        for replica in replicas[:self.R-1]:
            try:
                value = await replica.get(key, timeout=0.1)
                if value:
                    responses.append(value)
            except:
                # Replica unreachable - continue with available data
                pass

        if not responses:
            # No data available (very rare)
            return None

        if len(responses) < self.R:
            # Didn't achieve read quorum
            # In AP system: Return best available data
            return {
                'value': responses[0].value,
                'consistent': False,
                'warning': 'Read quorum not met'
            }

        # Check for conflicts (multiple versions)
        if self.has_conflicts(responses):
            # Return all versions - let client resolve
            return {
                'value': [r.value for r in responses],
                'conflict': True,
                'versions': [r.version for r in responses]
            }
        else:
            # All versions agree or clearly ordered
            latest = self.get_latest_version(responses)
            return {
                'value': latest.value,
                'consistent': True
            }

    def has_conflicts(self, versions):
        """Check if versions have conflicts (concurrent writes)"""
        for i, v1 in enumerate(versions):
            for v2 in versions[i+1:]:
                if not v1.version.happens_before(v2.version) and \
                   not v2.version.happens_before(v1.version):
                    # Concurrent versions - conflict
                    return True
        return False

    async def anti_entropy_sync(self):
        """
        Background process to sync data across replicas
        Resolves inconsistencies from partition healing
        """
        while True:
            await asyncio.sleep(60)  # Run every minute

            # Pick random replica to sync with
            peer = random.choice(self.get_all_peers())

            # Exchange Merkle tree roots to find differences
            local_tree = self.build_merkle_tree()
            remote_tree = await peer.get_merkle_tree()

            differences = local_tree.diff(remote_tree)

            # Sync differing keys
            for key in differences:
                local_value = self.data.get(key)
                remote_value = await peer.get(key)

                if local_value and remote_value:
                    # Both have data - resolve conflict
                    resolved = self.resolve_conflict(local_value, remote_value)
                    self.data[key] = resolved
                    await peer.put(key, resolved)
                elif remote_value:
                    # Only remote has data
                    self.data[key] = remote_value
                elif local_value:
                    # Only local has data
                    await peer.put(key, local_value)
```

### Tunable Consistency (Quorum-based)

```python
class TunableConsistencyStore:
    """
    Allows choosing consistency vs availability per request
    R + W > N ensures strong consistency
    """

    def __init__(self, N=3):
        self.N = N  # Replication factor

    async def read(self, key, consistency_level='quorum'):
        """
        Read with configurable consistency
        - 'one': Fast, eventually consistent
        - 'quorum': Balanced
        - 'all': Strongly consistent but slow
        """
        if consistency_level == 'one':
            R = 1
            timeout = 0.05  # 50ms
        elif consistency_level == 'quorum':
            R = (self.N // 2) + 1
            timeout = 0.2  # 200ms
        elif consistency_level == 'all':
            R = self.N
            timeout = 1.0  # 1s
        else:
            raise ValueError(f"Unknown consistency level: {consistency_level}")

        replicas = self.get_replicas_for_key(key)
        responses = await self.read_from_replicas(replicas, key, R, timeout)

        if len(responses) < R:
            raise UnavailableError(f"Could not achieve {consistency_level} read")

        # Read repair: Sync stale replicas
        asyncio.create_task(self.read_repair(key, responses, replicas))

        return self.get_latest_version(responses)

    async def write(self, key, value, consistency_level='quorum'):
        """Write with configurable consistency"""
        if consistency_level == 'one':
            W = 1
            timeout = 0.05
        elif consistency_level == 'quorum':
            W = (self.N // 2) + 1
            timeout = 0.2
        elif consistency_level == 'all':
            W = self.N
            timeout = 1.0
        else:
            raise ValueError(f"Unknown consistency level: {consistency_level}")

        replicas = self.get_replicas_for_key(key)
        version = self.generate_version()

        successful_writes = await self.write_to_replicas(
            replicas, key, value, version, W, timeout
        )

        if successful_writes < W:
            # Hinted handoff: Store hint for failed nodes
            await self.store_hints(replicas, key, value, version)
            raise UnavailableError(f"Could not achieve {consistency_level} write")

        return version
```

### Conflict Resolution Strategies

```python
class ConflictResolver:
    """Strategies for resolving conflicts in AP systems"""

    @staticmethod
    def last_write_wins(versions):
        """
        LWW: Use timestamp to determine winner
        Simple but can lose data if clocks are skewed
        """
        return max(versions, key=lambda v: v.timestamp)

    @staticmethod
    def version_vector_resolution(versions):
        """
        Use version vectors to find causally latest version
        """
        # Remove versions that are ancestors of others
        non_dominated = []
        for v1 in versions:
            is_dominated = False
            for v2 in versions:
                if v1 != v2 and v2.version.dominates(v1.version):
                    is_dominated = True
                    break
            if not is_dominated:
                non_dominated.append(v1)

        if len(non_dominated) == 1:
            return non_dominated[0]
        else:
            # True conflict - need application-level resolution
            return {'conflict': True, 'versions': non_dominated}

    @staticmethod
    def application_merge(versions, merge_function):
        """
        Let application define merge logic
        Example: Merge shopping cart items
        """
        merged_value = merge_function([v.value for v in versions])
        latest_version = max(v.version for v in versions)
        return VersionedValue(merged_value, latest_version)

    @staticmethod
    def crdt_merge(crdts):
        """
        Use CRDT (Conflict-free Replicated Data Type)
        Mathematically guaranteed conflict resolution
        """
        # Example: G-Counter (grow-only counter)
        merged = {}
        for crdt in crdts:
            for node_id, count in crdt.counts.items():
                merged[node_id] = max(merged.get(node_id, 0), count)
        return merged
```

### Vector Clocks Implementation

```python
class VectorClock:
    """
    Vector clock for tracking causality in distributed systems
    """

    def __init__(self):
        self.clock = {}  # node_id -> counter

    def increment(self, node_id):
        """Increment clock for this node"""
        self.clock[node_id] = self.clock.get(node_id, 0) + 1
        return VectorClock.from_dict(self.clock)

    def merge(self, other):
        """Merge with another vector clock"""
        merged = {}
        all_nodes = set(self.clock.keys()) | set(other.clock.keys())
        for node in all_nodes:
            merged[node] = max(
                self.clock.get(node, 0),
                other.clock.get(node, 0)
            )
        return VectorClock.from_dict(merged)

    def happens_before(self, other):
        """Check if this clock happens before other"""
        # self < other if all components <= and at least one <
        all_less_or_equal = all(
            self.clock.get(node, 0) <= other.clock.get(node, 0)
            for node in set(self.clock.keys()) | set(other.clock.keys())
        )
        at_least_one_less = any(
            self.clock.get(node, 0) < other.clock.get(node, 0)
            for node in set(self.clock.keys()) | set(other.clock.keys())
        )
        return all_less_or_equal and at_least_one_less

    def concurrent_with(self, other):
        """Check if events are concurrent (neither happens before)"""
        return not self.happens_before(other) and not other.happens_before(self)
```

## 8. Trade-offs and Considerations

### CAP Trade-off Scenarios

| System | Choice | Trade-off | Example |
|--------|--------|-----------|---------|
| Banking | CP | Rejects transactions during partition | Bank account transfers |
| Social Media | AP | Shows stale data during partition | Twitter feed |
| E-commerce Cart | AP | Might see old cart briefly | Amazon shopping cart |
| Distributed Lock | CP | Lock unavailable during partition | Leader election |
| DNS | AP | Different servers return different IPs | Domain name resolution |

### Real-World CAP Examples

**CP Systems:**
- HBase
- MongoDB (with majority write concern)
- Redis Cluster (with wait command)
- Zookeeper
- etcd

**AP Systems:**
- Cassandra (tunable)
- DynamoDB (with eventual consistency)
- Riak
- CouchDB

**CA Systems (No Partition Tolerance):**
- Single-node databases
- Traditional RDBMS in single datacenter
- Not realistic for distributed systems

## 9. Scalability & Bottlenecks

### Partition Detection

```python
class PartitionDetector:
    """Detect network partitions in the cluster"""

    def __init__(self, nodes, heartbeat_interval=1.0, timeout=5.0):
        self.nodes = nodes
        self.heartbeat_interval = heartbeat_interval
        self.timeout = timeout
        self.last_heartbeat = {}

    async def monitor(self):
        """Continuously monitor for partitions"""
        while True:
            await asyncio.sleep(self.heartbeat_interval)

            reachable = set()
            unreachable = set()

            for node in self.nodes:
                try:
                    await node.ping(timeout=self.timeout)
                    self.last_heartbeat[node.id] = time.time()
                    reachable.add(node.id)
                except TimeoutError:
                    unreachable.add(node.id)

            if unreachable:
                await self.handle_partition(reachable, unreachable)

    async def handle_partition(self, reachable, unreachable):
        """Handle detected partition"""
        # Determine which partition this node is in
        if self.node_id in reachable:
            # We're in the reachable group
            if len(reachable) > len(unreachable):
                # Majority partition - continue operating
                await self.enter_operational_mode()
            else:
                # Minority partition - in CP system, go read-only
                await self.enter_readonly_mode()
```

## 10. Follow-up Questions

1. **Is CAP theorem really "pick 2 of 3"?**
   - No, it's really "CP or AP when partitions occur"
   - P (partition tolerance) is not optional in distributed systems
   - Networks always have partitions
   - Real choice: Consistency or Availability during partition

2. **What is PACELC theorem?**
   - Extension of CAP
   - If Partition: Choose Availability or Consistency
   - Else (no partition): Choose Latency or Consistency
   - Example: Cassandra is PA/EL (available during partition, low latency normally)

3. **How do you test CAP properties?**
   - Chaos engineering
   - Network partition simulation (iptables, toxiproxy)
   - Measure availability during partition
   - Verify consistency guarantees
   - Monitor conflict rates

4. **How long does it take to detect a partition?**
   - Depends on heartbeat interval
   - Typically: 1-10 seconds
   - Fast detection: More network overhead
   - False positives from slow networks

5. **What happens when partition heals?**
   - CP system: Minority partition syncs from majority
   - AP system: Anti-entropy process resolves conflicts
   - Duration: Seconds to hours depending on divergence
   - May trigger conflict resolution

6. **How do you choose R, W, N values?**
   - N: Higher = more durability, more cost
   - R + W > N: Strong consistency
   - R = W = (N//2) + 1: Balanced
   - R = 1, W = N: Fast reads
   - R = N, W = 1: Fast writes

7. **Can you have both strong consistency and high availability?**
   - Not during network partitions (CAP theorem)
   - Within a datacenter: Yes (rare partitions)
   - Across regions: Must choose
   - Use: Tunable consistency per request

8. **What are the hidden costs of eventual consistency?**
   - Application complexity (handle conflicts)
   - User confusion (see old data)
   - Conflict resolution logic
   - Testing complexity
   - Debugging distributed state

9. **How do financial systems handle CAP?**
   - Choose CP (consistency critical)
   - Accept unavailability during partitions
   - Use techniques: 2-phase commit, consensus
   - Fallback: Manual reconciliation
   - Prevention: Redundant networks

10. **What is the difference between consistency in CAP and ACID?**
    - CAP consistency: All nodes see same data
    - ACID consistency: Data meets constraints
    - Different concepts, both important
    - Distributed systems need both
