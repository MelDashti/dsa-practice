# Distributed Consensus: Paxos, Raft, and Coordination

## 1. Problem Statement

How do multiple nodes in a distributed system agree on a single value or state in the presence of failures? Distributed consensus is the foundation for building fault-tolerant systems, enabling leader election, configuration management, and distributed locking despite node and network failures.

## 2. Requirements

### Functional Requirements
- Achieve agreement among nodes on a single value
- Handle node failures (crash and recover)
- Support leader election
- Maintain consistency across nodes
- Detect and prevent split-brain scenarios
- Support membership changes (add/remove nodes)

### Non-functional Requirements
- **Safety:** Never return incorrect result
- **Liveness:** Eventually reach consensus (in absence of failures)
- **Fault Tolerance:** Survive F failures with 2F+1 nodes
- **Latency:** <100ms for consensus in normal case
- **Throughput:** 10K+ operations/second
- **Recovery Time:** <5 seconds after node failure

## 3. Capacity Estimation

### Example: Distributed Configuration Store (etcd-like)

**Cluster Setup:**
- 5 nodes (tolerates 2 failures)
- Geographic distribution: 3 datacenters
- Network latency: 1-50ms between nodes

**Workload:**
- Write requests: 1,000/second
- Read requests: 10,000/second (can read from followers)
- Average value size: 1 KB
- Total data: 10 GB

**Consensus Performance:**
```
Leader election time: ~1-5 seconds
Write latency (leader → majority):
  - Same datacenter: 5-10ms
  - Cross datacenter: 50-200ms
  - Worst case (2 failures): 100-500ms

Throughput per leader:
  - Single-threaded: 10K writes/sec
  - Batching: 100K writes/sec

Storage per node:
  - Log size: 100 GB (with log compaction)
  - Snapshot size: 10 GB
```

## 4. High-Level Design

### Consensus System Architecture

```
                     Client Requests
                            │
                            ↓
                  ┌─────────────────┐
                  │  Client Library │
                  │ (Leader Discovery)│
                  └────────┬─────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ↓              ↓              ↓
      ┌─────────┐    ┌─────────┐    ┌─────────┐
      │  Node 1 │    │  Node 2 │    │  Node 3 │
      │(Leader) │◄──►│(Follower)│◄──►│(Follower)│
      └────┬────┘    └─────────┘    └─────────┘
           │              ▲              ▲
           │              │              │
           └──────────────┴──────────────┘
              Consensus Protocol
              (Raft/Paxos)

Each Node Contains:
┌────────────────────────────┐
│    Consensus Module        │
│  ┌──────────────────────┐  │
│  │  Log Replication     │  │
│  ├──────────────────────┤  │
│  │  Leader Election     │  │
│  ├──────────────────────┤  │
│  │  Safety Checks       │  │
│  └──────────────────────┘  │
├────────────────────────────┤
│    State Machine           │
│  (Key-Value Store)         │
├────────────────────────────┤
│    Persistent Storage      │
│  (Log + Snapshots)         │
└────────────────────────────┘
```

## 5. API Design

### Consensus Cluster API

```
POST /api/v1/consensus/propose
Request: {
  "key": "config/app/timeout",
  "value": "30s",
  "client_id": "client-123",
  "sequence": 42
}
Response: {
  "status": "committed",
  "index": 12345,
  "term": 5,
  "leader": "node-1"
}

GET /api/v1/consensus/query
Query: ?key=config/app/timeout
Response: {
  "key": "config/app/timeout",
  "value": "30s",
  "index": 12345,
  "term": 5
}

GET /api/v1/cluster/status
Response: {
  "leader": "node-1",
  "term": 5,
  "cluster_size": 5,
  "nodes": [
    {
      "id": "node-1",
      "role": "leader",
      "last_heartbeat": "2025-11-12T10:30:45Z",
      "match_index": 12345
    },
    {
      "id": "node-2",
      "role": "follower",
      "last_heartbeat": "2025-11-12T10:30:44Z",
      "match_index": 12340
    }
  ]
}

POST /api/v1/cluster/add-node
Request: {
  "node_id": "node-6",
  "address": "192.168.1.6:9000"
}

POST /api/v1/cluster/remove-node
Request: {
  "node_id": "node-5"
}

GET /api/v1/log/entries
Query: ?start_index=12340&end_index=12350
Response: {
  "entries": [
    {
      "index": 12340,
      "term": 5,
      "command": {"key": "foo", "value": "bar"},
      "timestamp": "2025-11-12T10:30:40Z"
    }
  ]
}
```

## 6. Database Schema

### Consensus State Persistence

```sql
-- Raft persistent state
CREATE TABLE raft_state (
    node_id VARCHAR(50) PRIMARY KEY,
    current_term BIGINT NOT NULL DEFAULT 0,
    voted_for VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Log entries
CREATE TABLE log_entries (
    log_index BIGINT PRIMARY KEY,
    term BIGINT NOT NULL,
    command_type VARCHAR(50),
    command_data BLOB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_term (term)
);

-- Snapshots for log compaction
CREATE TABLE snapshots (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    last_included_index BIGINT NOT NULL,
    last_included_term BIGINT NOT NULL,
    snapshot_data BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_index (last_included_index)
);

-- Cluster membership
CREATE TABLE cluster_members (
    node_id VARCHAR(50) PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    status ENUM('active', 'leaving', 'removed'),
    added_at_index BIGINT,
    removed_at_index BIGINT,
    INDEX idx_status (status)
);

-- State machine (example: key-value store)
CREATE TABLE kv_store (
    key_name VARCHAR(255) PRIMARY KEY,
    value_data BLOB,
    last_modified_index BIGINT,
    last_modified_term BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 7. Detailed Component Design

### Raft Consensus Algorithm

#### Leader Election

```python
class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers

        # Persistent state
        self.current_term = 0
        self.voted_for = None
        self.log = []  # Log entries

        # Volatile state
        self.commit_index = 0
        self.last_applied = 0
        self.state = 'follower'  # follower, candidate, leader

        # Leader state
        self.next_index = {}  # For each peer
        self.match_index = {}  # For each peer

        # Timing
        self.election_timeout = random.uniform(150, 300)  # ms
        self.heartbeat_interval = 50  # ms
        self.last_heartbeat = time.time()

    async def run(self):
        """Main node loop"""
        while True:
            if self.state == 'follower':
                await self.run_follower()
            elif self.state == 'candidate':
                await self.run_candidate()
            elif self.state == 'leader':
                await self.run_leader()

    async def run_follower(self):
        """Follower state - wait for heartbeats"""
        timeout = self.election_timeout / 1000

        try:
            # Wait for heartbeat from leader
            await asyncio.wait_for(
                self.wait_for_heartbeat(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            # No heartbeat received - start election
            self.become_candidate()

    async def run_candidate(self):
        """Candidate state - request votes"""
        # Increment term
        self.current_term += 1
        self.voted_for = self.node_id

        # Reset election timer
        self.last_heartbeat = time.time()

        # Request votes from all peers
        votes_received = 1  # Vote for self
        votes_needed = (len(self.peers) + 1) // 2 + 1

        # Send RequestVote RPCs to all peers
        vote_tasks = [
            self.request_vote(peer)
            for peer in self.peers
        ]

        # Wait for responses or timeout
        timeout = self.election_timeout / 1000

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*vote_tasks, return_exceptions=True),
                timeout=timeout
            )

            for result in results:
                if isinstance(result, dict) and result.get('vote_granted'):
                    votes_received += 1

                    # Check if we won election
                    if votes_received >= votes_needed:
                        self.become_leader()
                        return

                # Higher term discovered
                if isinstance(result, dict) and result.get('term', 0) > self.current_term:
                    self.current_term = result['term']
                    self.become_follower()
                    return

        except asyncio.TimeoutError:
            # Election timeout - start new election
            pass

        # If we didn't win, we're still candidate - will retry

    async def run_leader(self):
        """Leader state - send heartbeats and replicate log"""
        while self.state == 'leader':
            # Send heartbeats to all followers
            heartbeat_tasks = [
                self.send_append_entries(peer, is_heartbeat=True)
                for peer in self.peers
            ]

            await asyncio.gather(*heartbeat_tasks, return_exceptions=True)

            # Wait before next heartbeat
            await asyncio.sleep(self.heartbeat_interval / 1000)

    async def request_vote(self, peer):
        """Request vote from peer"""
        last_log_index = len(self.log) - 1
        last_log_term = self.log[last_log_index].term if self.log else 0

        request = {
            'term': self.current_term,
            'candidate_id': self.node_id,
            'last_log_index': last_log_index,
            'last_log_term': last_log_term
        }

        try:
            response = await peer.vote_request(request)
            return response
        except Exception as e:
            return {'vote_granted': False, 'term': self.current_term}

    def handle_vote_request(self, request):
        """Handle vote request from candidate"""
        term = request['term']
        candidate_id = request['candidate_id']
        last_log_index = request['last_log_index']
        last_log_term = request['last_log_term']

        # If candidate's term is old, reject
        if term < self.current_term:
            return {'vote_granted': False, 'term': self.current_term}

        # Update term if candidate has higher term
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.become_follower()

        # Check if we can vote for this candidate
        can_vote = (
            (self.voted_for is None or self.voted_for == candidate_id)
            and self.is_log_up_to_date(last_log_index, last_log_term)
        )

        if can_vote:
            self.voted_for = candidate_id
            self.last_heartbeat = time.time()
            return {'vote_granted': True, 'term': self.current_term}
        else:
            return {'vote_granted': False, 'term': self.current_term}

    def is_log_up_to_date(self, last_log_index, last_log_term):
        """Check if candidate's log is at least as up-to-date as ours"""
        if not self.log:
            return True

        my_last_index = len(self.log) - 1
        my_last_term = self.log[my_last_index].term

        # Compare terms first, then indices
        if last_log_term > my_last_term:
            return True
        if last_log_term == my_last_term and last_log_index >= my_last_index:
            return True
        return False
```

#### Log Replication

```python
class RaftNode:
    async def replicate_log_entry(self, command):
        """
        Leader replicates log entry to followers
        Returns when entry is committed
        """
        if self.state != 'leader':
            raise NotLeaderError("Only leader can replicate")

        # Append to local log
        entry = LogEntry(
            index=len(self.log),
            term=self.current_term,
            command=command
        )
        self.log.append(entry)

        # Replicate to followers
        replication_tasks = [
            self.replicate_to_follower(peer, entry)
            for peer in self.peers
        ]

        # Wait for majority
        results = await asyncio.gather(*replication_tasks, return_exceptions=True)

        # Count successful replications
        successful = sum(1 for r in results if r is True)

        # Including leader's log
        if successful + 1 >= (len(self.peers) + 1) // 2 + 1:
            # Majority achieved - commit
            self.commit_index = entry.index
            await self.apply_to_state_machine(entry)
            return entry.index
        else:
            raise ConsensusFailure("Could not achieve majority")

    async def replicate_to_follower(self, follower, entry):
        """Replicate specific entry to a follower"""
        # Get next index for this follower
        next_idx = self.next_index.get(follower.id, len(self.log))

        # Prepare entries to send (might need to send previous entries)
        prev_log_index = next_idx - 1
        prev_log_term = self.log[prev_log_index].term if prev_log_index >= 0 else 0

        entries_to_send = self.log[next_idx:]

        request = {
            'term': self.current_term,
            'leader_id': self.node_id,
            'prev_log_index': prev_log_index,
            'prev_log_term': prev_log_term,
            'entries': entries_to_send,
            'leader_commit': self.commit_index
        }

        try:
            response = await follower.append_entries(request)

            if response['success']:
                # Update indices
                self.next_index[follower.id] = len(self.log)
                self.match_index[follower.id] = len(self.log) - 1
                return True
            else:
                # Log inconsistency - decrement next_index and retry
                self.next_index[follower.id] = max(0, next_idx - 1)
                return False

        except Exception:
            return False

    def handle_append_entries(self, request):
        """Follower handles append entries from leader"""
        term = request['term']
        leader_id = request['leader_id']
        prev_log_index = request['prev_log_index']
        prev_log_term = request['prev_log_term']
        entries = request['entries']
        leader_commit = request['leader_commit']

        # Reject if term is old
        if term < self.current_term:
            return {'success': False, 'term': self.current_term}

        # Update term and become follower if needed
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.become_follower()

        # Reset election timer (received heartbeat)
        self.last_heartbeat = time.time()

        # Check log consistency
        if prev_log_index >= 0:
            if prev_log_index >= len(self.log):
                # Missing entries
                return {'success': False, 'term': self.current_term}

            if self.log[prev_log_index].term != prev_log_term:
                # Conflict - delete conflicting entry and all that follow
                self.log = self.log[:prev_log_index]
                return {'success': False, 'term': self.current_term}

        # Append new entries
        for entry in entries:
            if entry.index < len(self.log):
                # Conflicting entry - replace
                if self.log[entry.index].term != entry.term:
                    self.log = self.log[:entry.index]
                    self.log.append(entry)
            else:
                # Append new entry
                self.log.append(entry)

        # Update commit index
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)

            # Apply committed entries to state machine
            while self.last_applied < self.commit_index:
                self.last_applied += 1
                await self.apply_to_state_machine(self.log[self.last_applied])

        return {'success': True, 'term': self.current_term}
```

### Paxos Algorithm (Basic)

```python
class PaxosProposer:
    """Paxos Proposer - initiates consensus"""

    def __init__(self, node_id, acceptors):
        self.node_id = node_id
        self.acceptors = acceptors
        self.proposal_number = 0

    async def propose(self, value):
        """Propose a value and try to achieve consensus"""

        # Phase 1: Prepare
        self.proposal_number += 1
        proposal_id = (self.proposal_number, self.node_id)

        prepare_requests = [
            acceptor.prepare(proposal_id)
            for acceptor in self.acceptors
        ]

        responses = await asyncio.gather(*prepare_requests, return_exceptions=True)

        # Need majority of promises
        promises = [r for r in responses if isinstance(r, dict) and r.get('promise')]

        if len(promises) < len(self.acceptors) // 2 + 1:
            raise ConsensusFailure("Could not get majority promises")

        # Check if any acceptor already accepted a value
        accepted_values = [
            (p['accepted_id'], p['accepted_value'])
            for p in promises
            if p.get('accepted_value') is not None
        ]

        if accepted_values:
            # Use the value from the highest proposal number
            _, value = max(accepted_values, key=lambda x: x[0])

        # Phase 2: Accept
        accept_requests = [
            acceptor.accept(proposal_id, value)
            for acceptor in self.acceptors
        ]

        responses = await asyncio.gather(*accept_requests, return_exceptions=True)

        # Need majority of accepts
        accepts = [r for r in responses if isinstance(r, dict) and r.get('accepted')]

        if len(accepts) >= len(self.acceptors) // 2 + 1:
            # Consensus achieved!
            return value
        else:
            raise ConsensusFailure("Could not get majority accepts")


class PaxosAcceptor:
    """Paxos Acceptor - promises and accepts proposals"""

    def __init__(self, node_id):
        self.node_id = node_id
        self.promised_id = None
        self.accepted_id = None
        self.accepted_value = None

    async def prepare(self, proposal_id):
        """Handle prepare request from proposer"""
        if self.promised_id is None or proposal_id > self.promised_id:
            # Promise not to accept any proposal with lower ID
            self.promised_id = proposal_id

            return {
                'promise': True,
                'accepted_id': self.accepted_id,
                'accepted_value': self.accepted_value
            }
        else:
            # Already promised to higher proposal
            return {
                'promise': False,
                'promised_id': self.promised_id
            }

    async def accept(self, proposal_id, value):
        """Handle accept request from proposer"""
        if self.promised_id is None or proposal_id >= self.promised_id:
            # Accept this proposal
            self.promised_id = proposal_id
            self.accepted_id = proposal_id
            self.accepted_value = value

            return {'accepted': True}
        else:
            # Promised to higher proposal - reject
            return {
                'accepted': False,
                'promised_id': self.promised_id
            }
```

### Log Compaction (Snapshots)

```python
class SnapshotManager:
    """Manage snapshots for log compaction in Raft"""

    def __init__(self, state_machine, log):
        self.state_machine = state_machine
        self.log = log
        self.last_snapshot_index = 0
        self.last_snapshot_term = 0

    async def create_snapshot(self):
        """Create snapshot of current state machine state"""
        # Serialize state machine
        snapshot_data = self.state_machine.serialize()

        # Record last included index and term
        self.last_snapshot_index = self.state_machine.last_applied
        self.last_snapshot_term = self.log[self.last_snapshot_index].term

        # Save snapshot to disk
        await self.save_snapshot(snapshot_data)

        # Discard log entries up to snapshot point
        self.log = self.log[self.last_snapshot_index + 1:]

        return {
            'index': self.last_snapshot_index,
            'term': self.last_snapshot_term,
            'size': len(snapshot_data)
        }

    async def install_snapshot(self, snapshot_data, last_index, last_term):
        """Install snapshot received from leader"""
        # Discard entire log if snapshot is more up-to-date
        if last_index >= len(self.log) or self.log[last_index].term != last_term:
            self.log = []
        else:
            # Keep log entries after snapshot
            self.log = self.log[last_index + 1:]

        # Restore state machine from snapshot
        self.state_machine.deserialize(snapshot_data)
        self.state_machine.last_applied = last_index

        self.last_snapshot_index = last_index
        self.last_snapshot_term = last_term
```

## 8. Trade-offs and Considerations

### Raft vs Paxos

| Aspect | Raft | Paxos |
|--------|------|-------|
| **Understandability** | Easier to understand | More complex |
| **Leader** | Strong leader model | No permanent leader |
| **Log Structure** | Must be contiguous | Can have gaps |
| **Membership Changes** | Explicit joint consensus | Can be complex |
| **Implementation** | Easier | More difficult |
| **Flexibility** | Less flexible | More flexible |
| **Performance** | Comparable | Comparable |

### Multi-Paxos vs Raft

Multi-Paxos (optimized version) and Raft are very similar:
- Both have a leader
- Both replicate logs
- Raft is essentially "Paxos made understandable"

## 9. Scalability & Bottlenecks

### Performance Optimizations

```python
class RaftOptimizations:
    """Various optimizations for Raft performance"""

    def batch_commits(self, commands, max_batch_size=100):
        """Batch multiple commands into single log entry"""
        batches = []
        current_batch = []

        for cmd in commands:
            current_batch.append(cmd)
            if len(current_batch) >= max_batch_size:
                batches.append(current_batch)
                current_batch = []

        if current_batch:
            batches.append(current_batch)

        # Commit each batch as single entry
        for batch in batches:
            await self.replicate_log_entry({'batch': batch})

    def pipeline_replication(self, follower):
        """Pipeline append entries without waiting for responses"""
        # Send multiple append_entries without waiting
        # Process responses asynchronously
        # Trade-off: Complexity for throughput
        pass

    def use_prevote(self):
        """
        PreVote optimization: Before starting election,
        check if candidate could actually win
        Prevents unnecessary term increases
        """
        pass
```

### Bottlenecks

1. **Single Leader Bottleneck:**
   - All writes go through leader
   - Solution: Read from followers (stale reads acceptable)
   - Solution: Lease-based reads (leader can serve reads)

2. **Network Latency:**
   - Cross-datacenter consensus is slow
   - Solution: Local quorums within datacenter
   - Solution: Hierarchical consensus

3. **Disk I/O:**
   - Must persist to disk before responding
   - Solution: Batch writes
   - Solution: Group commit

## 10. Follow-up Questions

1. **How does Raft handle network partitions?**
   - Minority partition: Cannot elect leader (no quorum)
   - Majority partition: Continues operating normally
   - Split-brain prevented by quorum requirement
   - When partition heals: Minority syncs from majority

2. **What is the difference between consensus and consistency?**
   - Consensus: Agreement on a single value/state
   - Consistency: Guarantees about what values are read
   - Consensus enables strong consistency
   - Can have consistency without consensus (single node)

3. **How do you add/remove nodes safely?**
   - Raft: Joint consensus (both old and new configs)
   - Must have agreement from both majorities
   - Two-phase process prevents split-brain
   - After committed, switch to new configuration

4. **What is the FLP impossibility result?**
   - Fischer, Lynch, Paterson (1985)
   - Impossible to guarantee consensus in asynchronous system with even one faulty process
   - Resolution: Use timeouts (makes system partially synchronous)

5. **How do you handle disk failures?**
   - Lose persistent state (voted_for, log)
   - Solution: Replicate to other nodes
   - Solution: RAID/replication at storage level
   - Recovery: Re-join as new node, sync from leader

6. **What is linearizability and how does consensus provide it?**
   - Linearizability: Operations appear instantaneous
   - Consensus ensures all operations are totally ordered
   - Read-after-write consistency guaranteed
   - Requires quorum reads or leader leases

7. **How do you optimize for read-heavy workloads?**
   - Allow reads from followers (eventually consistent)
   - Lease-based reads from leader (strongly consistent)
   - ReadIndex optimization (verify leadership without disk write)
   - Follower reads with read quorum

8. **What are the failure modes of consensus systems?**
   - Less than quorum: System unavailable
   - Network partition: Minority unavailable
   - Leader failure: Brief unavailability during election
   - All nodes fail: Total data loss (without backup)

9. **How do you test consensus implementations?**
   - Jepsen testing (network partitions, failures)
   - Randomized testing (random crashes, delays)
   - Model checking (TLA+)
   - Chaos engineering in production

10. **When should you NOT use consensus?**
    - Single datacenter with low fault tolerance needs
    - Cannot tolerate consensus latency (50-200ms)
    - AP system more appropriate than CP
    - Simple use cases (caching, sessions)
