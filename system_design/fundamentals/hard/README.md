# Fundamentals: Hard Level

## Overview

This section covers advanced distributed systems concepts that form the theoretical foundation of large-scale systems. These topics are asked in senior/staff engineer interviews and require deep understanding of distributed computing challenges.

## Topics Covered

### 1. CAP Theorem (cap_theorem.md)
**Concept:** Consistency, Availability, Partition Tolerance Trade-offs

Understand the fundamental limitation of distributed systems:
- **The Theorem:** Can only guarantee 2 of 3 (C, A, P) during network partitions
- **CP Systems:** Raft, Zookeeper, HBase (consistency over availability)
- **AP Systems:** Cassandra, DynamoDB, Riak (availability over consistency)
- **Tunable Consistency:** Quorum-based systems (R + W > N)
- **PACELC Extension:** Latency vs Consistency trade-offs

**Key Insight:** P (partition tolerance) is not optional in distributed systems. The real choice is between CP and AP during partitions.

### 2. Distributed Consensus (distributed_consensus.md)
**Concept:** Paxos, Raft, and Distributed Coordination

Master algorithms for achieving agreement in distributed systems:
- **Raft Consensus:** Leader election, log replication, safety guarantees
- **Paxos Algorithm:** Prepare and accept phases, majority quorums
- **Use Cases:** Distributed locks, leader election, configuration management
- **Implementations:** etcd (Raft), Zookeeper (ZAB), Consul (Raft)
- **FLP Impossibility:** Theoretical limitations of consensus

**Real-World:** Google Chubby (Paxos), etcd/Consul (Raft) power systems handling billions of requests daily.

### 3. Event-Driven Architecture (event_driven_architecture.md)
**Concept:** Event Sourcing and CQRS Patterns

Build systems that treat events as the source of truth:
- **Event Sourcing:** Store all changes as immutable events
- **CQRS:** Separate read and write models for scalability
- **Event Bus:** Kafka, RabbitMQ for event distribution
- **Projections:** Build materialized views from events
- **Saga Pattern:** Distributed transactions using events

**Benefits:** Complete audit trail, time travel queries, independent read/write scaling.

## Why These Topics Are "Hard"

| Challenge | Description |
|-----------|-------------|
| **Abstract Concepts** | Requires understanding distributed computing theory |
| **No Single Answer** | Multiple valid approaches with trade-offs |
| **Failure Scenarios** | Must reason about network partitions, clock skew, split-brain |
| **Mathematical Proofs** | Consensus algorithms have formal correctness proofs |
| **Production Experience** | Hard to truly understand without building distributed systems |

## Theoretical Foundations

### CAP Theorem (Brewer, 2000)
- Proven impossibility result
- Partition tolerance is non-negotiable in distributed systems
- Must choose: Consistency or Availability during partitions

### FLP Impossibility (Fischer, Lynch, Paterson, 1985)
- Impossible to guarantee consensus in asynchronous system with even one faulty process
- Resolution: Use timeouts (partial synchrony)

### PACELC Theorem
- Extension of CAP
- If Partition: Choose A or C
- Else: Choose Latency or Consistency

## Interview Mastery

### CAP Theorem Questions

**Q:** "Is Cassandra CP or AP?"
**A:** AP by default (tunable to CP with quorum reads/writes)

**Q:** "Can you have both high availability and strong consistency?"
**A:** Not during network partitions (CAP theorem). Within a datacenter with rare partitions, yes.

**Q:** "How does Google Spanner achieve external consistency?"
**A:** TrueTime API (GPS + atomic clocks) to determine global ordering of transactions.

### Consensus Questions

**Q:** "Explain Raft leader election"
**A:**
1. Followers timeout → become candidates
2. Candidate votes for self, requests votes
3. Majority votes → becomes leader
4. Leader sends heartbeats to prevent elections

**Q:** "How does Raft handle split-brain?"
**A:** Requires majority quorum. Only partition with majority can elect leader and accept writes.

### Event-Driven Architecture Questions

**Q:** "How do you handle schema evolution in event sourcing?"
**A:**
- Versioned events (OrderCreatedV1, OrderCreatedV2)
- Upcasting: Convert old events on read
- Weak schema: JSON with optional fields

**Q:** "What happens if event processing fails?"
**A:**
- Retry with exponential backoff
- Dead letter queue for poison messages
- Idempotent handlers
- Circuit breaker

## Real-World System Examples

### CAP Trade-offs in Production

| System | Choice | Reasoning |
|--------|--------|-----------|
| **Bank Account** | CP | Consistency critical (can't show wrong balance) |
| **Twitter Feed** | AP | Availability critical (stale tweets acceptable) |
| **Shopping Cart** | AP | Availability critical (merge conflicts OK) |
| **Distributed Lock** | CP | Consistency critical (prevent split-brain) |
| **DNS** | AP | Availability critical (eventual consistency OK) |

### Consensus in Production

- **etcd (Kubernetes):** Stores cluster configuration using Raft
- **Consul:** Service discovery and configuration with Raft
- **Zookeeper (Kafka, HBase):** Coordination using ZAB (Paxos variant)
- **Chubby (Google):** Lock service using Paxos

### Event Sourcing Examples

- **Banking:** Event sourcing for regulatory compliance (full audit trail)
- **E-commerce:** Order processing with SAGA pattern
- **Gaming:** Player actions as events for replay/cheating detection
- **IoT:** Sensor readings as events for time-series analysis

## Advanced Concepts

### Beyond Basic CAP

**Harvest vs Yield:**
- Harvest: Completeness of response
- Yield: Probability of completing request
- Trade-off: Return partial results vs wait for complete data

**Sticky Availability:**
- Session-specific availability
- Client sees consistent view (even if stale)

**Compensating Transactions:**
- Undo operations in AP systems
- Example: Reserve → Charge → Ship (with rollback at each step)

### Consensus Optimizations

**Raft Optimizations:**
- Batching: Combine multiple log entries
- Pipelining: Send multiple AppendEntries without waiting
- Pre-vote: Check electability before starting election

**Multi-Paxos:**
- Skip prepare phase for subsequent proposals
- Similar to Raft in practice

### Event Sourcing Patterns

**CQRS Patterns:**
- Single write model, multiple read models
- Materialized views optimized for queries
- Eventually consistent projections

**Snapshotting:**
- Periodic state snapshots
- Replay from snapshot + subsequent events
- Reduces replay time

## Common Mistakes

### CAP Theorem
❌ "I'll build a CA system" (P is mandatory)
❌ "My system is CAP compliant" (misunderstanding of theorem)
❌ Ignoring partition scenarios

✅ Choose CP or AP based on requirements
✅ Design for partition scenarios
✅ Use tunable consistency where appropriate

### Consensus
❌ Rolling your own consensus algorithm
❌ Quorum without considering network partitions
❌ Synchronous replication without timeouts

✅ Use proven implementations (etcd, Consul)
✅ Understand failure modes
✅ Test with network partition simulation

### Event Sourcing
❌ Event sourcing everything
❌ Not planning for schema evolution
❌ Synchronous event processing

✅ Use where audit trail needed
✅ Version events from day one
✅ Async event processing with queues

## Study Resources

### Papers (Essential Reading)
- **CAP Theorem:** "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services" (Gilbert & Lynch, 2002)
- **Paxos:** "The Part-Time Parliament" (Lamport, 1998)
- **Raft:** "In Search of an Understandable Consensus Algorithm" (Ongaro & Ousterhout, 2014)
- **FLP:** "Impossibility of Distributed Consensus with One Faulty Process" (Fischer, Lynch, Paterson, 1985)

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann (Chapters 5, 7-9)
- "Database Internals" by Alex Petrov
- "Distributed Systems" by Maarten van Steen

### Tools for Learning
- **Raft Visualization:** raft.github.io/raftscope/index.html
- **Jepsen Testing:** Test distributed systems for consistency bugs
- **TLA+:** Model checking for distributed algorithms

## Practical Exercises

1. **CAP Theorem:**
   - Design a system for different CAP choices
   - Simulate network partition and observe behavior
   - Implement tunable consistency

2. **Consensus:**
   - Implement basic Raft (leader election only)
   - Use etcd for distributed lock
   - Simulate failure scenarios

3. **Event Sourcing:**
   - Build event store for a domain (e.g., banking)
   - Implement CQRS with read models
   - Handle event schema evolution

## Prerequisites

Before tackling hard-level topics:
- ✅ Solid understanding of distributed systems basics
- ✅ Database replication and sharding (Medium)
- ✅ Network protocols and failure modes
- ✅ Strong theoretical computer science background helpful
- ✅ Experience with production distributed systems beneficial

## Career Relevance

**Senior Engineer (L5-L6):**
- Must explain CAP trade-offs for design decisions
- Understand when to use consensus (distributed locks, leader election)
- Know event-driven patterns for scalability

**Staff+ Engineer (L7+):**
- Deep understanding of consensus algorithms
- Design new distributed systems with correctness guarantees
- Contribute to distributed systems infrastructure

**Architect:**
- Choose appropriate consistency models
- Design event-driven architectures for entire organizations
- Make fundamental distributed systems trade-offs

---

**Difficulty Rating:** ⭐⭐⭐⭐⭐ (5/5) - Requires deep theoretical understanding and practical experience with distributed systems
