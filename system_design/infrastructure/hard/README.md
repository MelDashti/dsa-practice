# Infrastructure - Hard Level

## Overview
This directory contains advanced infrastructure system design problems that require deep understanding of distributed systems, consensus algorithms, advanced data structures, and complex trade-offs. These problems involve building highly available, fault-tolerant systems at massive scale with strict performance requirements.

## Problems

### 1. Distributed Job Scheduler
**File**: `distributed_job_scheduler.md`

**Description**: Design a distributed task scheduler (like Kubernetes CronJobs or Apache Airflow) that schedules and executes millions of jobs across thousands of worker nodes with strong consistency guarantees, dependency management, and fault tolerance.

**Key Concepts**:
- Time wheel for efficient scheduling
- DAG-based dependency resolution
- Leader election (ZooKeeper/etcd)
- At-most-once execution semantics
- Distributed consensus
- Job recovery and retry logic

**Why This is Hard**:
- Ensuring at-most-once execution in distributed system
- Handling clock skew across nodes
- Complex failure scenarios (scheduler, worker, network)
- Dependency resolution at scale
- Resource allocation optimization

**Related Problems**:
- Medium: Design Kafka (message queue for job distribution)
- Hard: Distributed Cache (for job state caching)

### 2. Distributed Caching System (Redis/Memcached-style)
**File**: `distributed_cache.md`

**Description**: Design a distributed in-memory caching system with sub-millisecond latency, automatic sharding, replication, persistence options, and support for advanced data structures.

**Key Concepts**:
- Consistent hashing for sharding
- Master-slave replication
- Eviction policies (LRU, LFU, TTL)
- Append-Only File (AOF) persistence
- Memory optimization techniques
- Split-brain prevention

**Why This is Hard**:
- Sub-millisecond latency requirements
- Balancing consistency and availability
- Memory efficiency at billion-key scale
- Handling network partitions
- Cache stampede mitigation
- Efficient data structure implementations

**Related Problems**:
- Medium: Metrics Monitoring (time-series caching)
- Hard: Distributed Rate Limiter (uses distributed cache)

### 3. Distributed Rate Limiter
**File**: `distributed_rate_limiter.md`

**Description**: Design a global rate limiting system that enforces limits across multiple servers and data centers with high accuracy, supporting multiple algorithms and minimal coordination overhead.

**Key Concepts**:
- Token bucket algorithm
- Sliding window counters
- Local + global coordination
- Eventual consistency trade-offs
- Lua scripting in Redis
- Multi-dimensional rate limiting

**Why This is Hard**:
- Achieving accuracy without centralized bottleneck
- Handling distributed state synchronization
- Sub-millisecond latency requirement
- Clock synchronization issues
- Balancing accuracy vs performance
- Preventing distributed gaming

**Related Problems**:
- Hard: Distributed Cache (infrastructure for rate limits)
- Fundamentals: Rate Limiter (single-server version)

### 4. Service Mesh Architecture
**File**: `service_mesh.md`

**Description**: Design a service mesh infrastructure layer (like Istio or Linkerd) that provides service-to-service communication, observability, security, and traffic management without application code changes.

**Key Concepts**:
- Sidecar proxy pattern (Envoy)
- mTLS certificate management
- Circuit breakers
- Service discovery
- Distributed tracing (OpenTelemetry)
- Traffic routing and load balancing

**Why This is Hard**:
- Minimal latency overhead requirement (<2ms)
- Complex failure modes (cascading failures)
- Certificate rotation at scale
- Configuration propagation
- Observability data volume
- Multi-cluster coordination

**Related Problems**:
- Hard: Distributed Rate Limiter (service-level rate limiting)
- Core Components: Load Balancer (traffic distribution)

## Learning Path

### Prerequisites

**Advanced Distributed Systems**:
- Consensus algorithms (Paxos, Raft)
- Vector clocks and logical timestamps
- Quorum-based systems
- Leader election protocols
- Distributed transactions (2PC, 3PC)

**Advanced Data Structures**:
- Time wheels
- Skip lists
- Bloom filters
- HyperLogLog
- Count-Min Sketch
- Consistent hashing rings

**Advanced Algorithms**:
- Exponential backoff
- Circuit breaker patterns
- Token bucket algorithm
- Sliding window algorithms
- DAG topological sort

**System Concepts**:
- Memory management and optimization
- Zero-copy transfers
- TLS/mTLS
- Certificate management
- Clock synchronization (NTP)

### Skills Developed

1. **Advanced Distributed Systems**
   - Consensus and coordination
   - Distributed state management
   - Split-brain prevention
   - Byzantine fault tolerance

2. **Performance Engineering**
   - Latency optimization (<1ms)
   - Memory efficiency
   - Lock-free data structures
   - CPU cache optimization

3. **Operational Excellence**
   - Zero-downtime upgrades
   - Disaster recovery
   - Capacity planning at scale
   - Multi-region deployment

4. **Security**
   - Mutual TLS implementation
   - Certificate rotation
   - Zero-trust networking
   - Secret management

### Progression Path

1. **Start with Distributed Cache**
   - Foundation for other systems
   - Introduces consistency/availability trade-offs
   - Memory optimization techniques

2. **Move to Distributed Rate Limiter**
   - Builds on caching concepts
   - Introduces synchronization challenges
   - Algorithm design focus

3. **Study Distributed Job Scheduler**
   - Complex state management
   - Leader election and consensus
   - Dependency resolution

4. **Complete with Service Mesh**
   - Integrates multiple concepts
   - Real-world complexity
   - Observability at scale

## Interview Tips

### Common Questions by Problem

**Distributed Job Scheduler**
1. How do you prevent duplicate job execution?
2. Explain leader election and failover
3. How do you handle clock skew?
4. How do you resolve job dependencies?
5. What happens if a worker fails mid-job?

**Distributed Cache**
1. Explain consistent hashing and virtual nodes
2. How do you handle cache stampede?
3. Compare eviction policies (LRU vs LFU)
4. How do you achieve strong consistency?
5. Explain AOF vs RDB persistence

**Distributed Rate Limiter**
1. Token bucket vs sliding window trade-offs
2. How do you achieve global rate limiting with low latency?
3. How do you handle clock synchronization?
4. Explain the accuracy vs performance trade-off
5. How do you prevent distributed gaming?

**Service Mesh**
1. Explain the sidecar proxy pattern
2. How does mTLS work end-to-end?
3. How do circuit breakers prevent cascading failures?
4. What's the latency overhead of service mesh?
5. How do you handle certificate rotation?

### Key Discussion Points

**Consensus and Coordination**
- Paxos vs Raft algorithms
- Leader election strategies
- Quorum requirements
- Split-brain scenarios
- CAP theorem applications

**Performance Optimization**
- Latency breakdown analysis
- Memory layout optimization
- CPU cache efficiency
- Lock-free algorithms
- Batch processing

**Failure Modes**
- Network partitions
- Cascading failures
- Byzantine failures
- Correlated failures
- Gray failures (partial)

**Operational Concerns**
- Rolling upgrades
- Configuration changes
- Monitoring and alerting
- Capacity planning
- Cost optimization

## Practice Approach

### Step 1: Deep Requirements (15 minutes)
- Clarify consistency requirements (strong vs eventual)
- Define exact latency requirements (P50, P99, P999)
- Understand scale (QPS, data size, number of nodes)
- Identify critical failure scenarios
- Discuss trade-offs upfront

### Step 2: Architecture (20 minutes)
- Draw component diagram with clear responsibilities
- Explain data flow for critical paths
- Identify single points of failure
- Discuss replication and sharding strategies
- Explain consensus mechanisms

### Step 3: Detailed Design (25 minutes)
- Design data structures with memory layout
- Explain key algorithms with complexity analysis
- Discuss synchronization mechanisms
- Design failure detection and recovery
- Optimize critical path

### Step 4: Advanced Topics (10 minutes)
- Security considerations
- Monitoring and observability
- Operational procedures
- Cost analysis
- Future improvements

### Step 5: Validation (5 minutes)
- Walk through failure scenarios
- Verify latency requirements
- Check consistency guarantees
- Confirm scalability limits

## Common Pitfalls to Avoid

1. **Ignoring Clock Skew**: Not accounting for time synchronization issues
2. **Overlooking Split-Brain**: Not preventing conflicting leaders
3. **Assuming Perfect Networks**: Ignoring packet loss, partitions
4. **Weak Failure Handling**: Not considering all failure modes
5. **Inefficient Algorithms**: Using O(n) when O(1) is needed
6. **Memory Leaks**: Not managing resource cleanup
7. **Centralized Bottlenecks**: Single coordinator for all operations
8. **Ignoring Latency Budget**: Each component adds latency

## Advanced Concepts

### Consensus Algorithms

**Raft**
- Leader election with terms
- Log replication with majority quorum
- Safety: election safety, leader append-only, log matching
- Easier to understand than Paxos

**Paxos**
- Multi-Paxos for sequence of values
- Roles: proposers, acceptors, learners
- Two phases: prepare and accept
- More flexible but complex

### Memory Optimization

**Techniques**:
- Memory pooling
- Object reuse
- Compact data structures
- Memory mapping
- NUMA-aware allocation

**Data Structure Optimization**:
- Cache-line alignment
- False sharing prevention
- Lock-free structures
- Zero-copy techniques

### Failure Detection

**Methods**:
- Heartbeats with timeouts
- Gossip protocols
- Phi Accrual failure detector
- SWIM (Scalable Weakly-consistent Infection-style Membership)

**Challenges**:
- False positives (network delays)
- False negatives (slow detection)
- Flapping (oscillation)

### Time Synchronization

**Protocols**:
- NTP (Network Time Protocol)
- PTP (Precision Time Protocol)
- TrueTime (Google's GPS + atomic clocks)

**Challenges**:
- Clock drift
- Network latency
- Leap seconds
- Time zones

## Advanced Patterns

### Leader Election
```
1. Candidate nodes propose themselves with term number
2. Majority vote required to become leader
3. Leader sends periodic heartbeats
4. Followers timeout and trigger new election
5. Higher term always wins
```

### Token Bucket
```
1. Bucket holds tokens (capacity limit)
2. Tokens refill at constant rate
3. Request consumes tokens
4. If insufficient tokens, reject request
5. Allows burst up to capacity
```

### Circuit Breaker
```
States: Closed → Open → Half-Open → Closed

Closed: Normal operation
  → Open after N consecutive failures

Open: Reject immediately
  → Half-Open after timeout

Half-Open: Allow test requests
  → Closed after M successes
  → Open after any failure
```

### Consistent Hashing
```
1. Hash nodes onto ring (with virtual nodes)
2. Hash keys onto same ring
3. Walk clockwise to find responsible node
4. Add/remove nodes: only K/N keys move
5. Virtual nodes improve distribution
```

## Time Estimates

Per problem:
- **Reading & Understanding**: 60-90 minutes
- **Initial Design**: 60-90 minutes
- **Deep Dive Study**: 4-6 hours
- **Implementation (optional)**: 16-24 hours
- **Interview Discussion**: 60-75 minutes

**Total for Hard Level**: 40-60 hours

## Success Criteria

You've mastered this level when you can:
- Design systems with <1ms P99 latency
- Explain consensus algorithms in detail
- Handle complex failure scenarios
- Optimize for memory and CPU efficiency
- Design for 99.99%+ availability
- Make nuanced trade-off decisions
- Discuss operational procedures
- Estimate costs at scale
- Explain security implementations
- Design for zero-downtime operations

## Additional Resources

### Papers
- "Time, Clocks, and the Ordering of Events in a Distributed System" (Lamport)
- "The Raft Consensus Algorithm" (Ongaro & Ousterhout)
- "Paxos Made Simple" (Lamport)
- "Dynamo: Amazon's Highly Available Key-value Store"
- "The Chubby Lock Service" (Google)
- "Large-scale cluster management at Google with Borg"

### Books
- "Designing Data-Intensive Applications" (Kleppmann) - Advanced chapters
- "Database Internals" (Petrov)
- "Distributed Systems: Principles and Paradigms" (Tanenbaum)
- "Understanding Distributed Systems" (Peteiro)

### Courses
- MIT 6.824: Distributed Systems (with labs)
- Stanford CS244B: Distributed Systems
- Google's SRE Books
- Cloud Provider Architecture Docs (AWS, GCP, Azure)

### Open Source Study
- **Raft**: etcd, Consul
- **Redis**: Redis Cluster implementation
- **Envoy**: Service mesh data plane
- **Kubernetes**: Scheduler implementation
- **Apache Airflow**: Workflow orchestration
- **Istio**: Service mesh control plane

## Real-World Case Studies

### Netflix
- Chaos engineering (Chaos Monkey)
- Regional failover
- Cache warming strategies
- Distributed tracing at scale

### Uber
- Schemaless (distributed datastore)
- Ringpop (consistent hash ring)
- TChannel (RPC framework)
- Jaeger (distributed tracing)

### LinkedIn
- Kafka (distributed log)
- Samza (stream processing)
- Cruise Control (cluster management)

### Google
- Borg (cluster scheduler)
- Chubby (lock service)
- Spanner (globally distributed database)
- TrueTime (synchronized clocks)

## Interview Anti-Patterns

**What NOT to do**:
1. Jump to implementation without clarifying requirements
2. Ignore failure scenarios
3. Propose single points of failure
4. Assume perfect networks and clocks
5. Use buzzwords without understanding
6. Ignore resource constraints (memory, CPU, network)
7. Over-complicate simple solutions
8. Under-estimate operational complexity

**What TO do**:
1. Ask clarifying questions about scale and requirements
2. Discuss trade-offs for each decision
3. Address failure handling proactively
4. Provide concrete numbers (latency, throughput)
5. Draw clear diagrams
6. Explain reasoning behind choices
7. Discuss operational procedures
8. Acknowledge limitations and alternatives

## Next Steps

After completing hard-level problems:

1. **Implement Prototypes**: Build simplified versions to solidify understanding
2. **Read Source Code**: Study production implementations (Redis, etcd, Envoy)
3. **Contribute to OSS**: Contribute to distributed systems projects
4. **Write Technical Blogs**: Explain concepts to deepen understanding
5. **Conduct Mock Interviews**: Practice explaining under time pressure
6. **Study Real Incidents**: Read postmortems from major outages
7. **Explore Research**: Read recent academic papers
8. **Specialize**: Deep dive into one area (consensus, caching, scheduling)

## Career Applications

These skills are valuable for:
- **Senior/Staff Engineer**: Design distributed systems
- **System Architect**: Make technology decisions
- **SRE/DevOps**: Operate large-scale systems
- **Technical Lead**: Guide team on architecture
- **Performance Engineer**: Optimize critical systems
- **Platform Engineer**: Build infrastructure services

Companies that value these skills:
- FAANG (Meta, Amazon, Netflix, Google)
- Cloud providers (AWS, GCP, Azure, DigitalOcean)
- Database companies (MongoDB, Datastax, Cockroach Labs)
- Infrastructure companies (HashiCorp, Confluent, Databricks)
- High-scale startups (Stripe, Uber, Airbnb, DoorDash)

---

**Remember**: The goal isn't to memorize solutions, but to develop intuition for:
- When to use which consensus algorithm
- How to balance consistency vs availability
- Where to optimize for latency vs throughput
- How to handle inevitable failures gracefully
- How to operate systems at scale

Focus on understanding principles, trade-offs, and real-world constraints. These problems represent the pinnacle of distributed systems design - master them and you'll be prepared for the most challenging infrastructure interviews.
