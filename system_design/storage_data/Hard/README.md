# Hard Level - Storage & Data System Design

This folder contains advanced system design problems focused on building foundational distributed systems that power modern infrastructure. These problems require deep understanding of distributed systems, consistency models, replication strategies, and handling extreme scale.

## Problems

### 1. S3-like Object Storage
**File:** `s3_object_storage.md`

Design a highly scalable, durable object storage system like Amazon S3.

**Key Concepts:**
- Distributed storage architecture
- Consistent hashing for data placement
- Replication vs. erasure coding
- Strong vs. eventual consistency
- Metadata management at scale
- Storage tiering (hot/warm/cold)
- Durability (11 nines: 99.999999999%)

**Core Challenges:**
- Exabyte-scale storage
- 50M+ requests per second
- Multi-region replication
- Metadata sharding and indexing

### 2. Distributed Key-Value Store (DynamoDB/Cassandra)
**File:** `design_key_value_store.md`

Design a distributed NoSQL database with high availability and partition tolerance.

**Key Concepts:**
- Consistent hashing ring
- Replication and quorum-based consistency
- Gossip protocol for failure detection
- LSM tree storage engine
- Vector clocks for conflict resolution
- Hinted handoff
- Read repair and anti-entropy

**Core Challenges:**
- CAP theorem trade-offs (AP vs. CP)
- Tunable consistency levels
- Handling network partitions
- Compaction strategies

### 3. Distributed Email Service (Gmail-scale)
**File:** `distributed_email_service.md`

Design a large-scale email system handling billions of emails per day.

**Key Concepts:**
- SMTP protocol and email delivery
- Spam filtering with ML
- Email threading and conversations
- Full-text search at scale
- Real-time sync and push notifications
- Email storage and metadata management

**Core Challenges:**
- 10B+ emails per day
- Real-time spam detection
- Sub-100ms search latency
- Email deliverability and reliability

### 4. Video Conferencing (Zoom)
**File:** `design_zoom.md`

Design a real-time video conferencing platform with low latency globally.

**Key Concepts:**
- WebRTC and media servers
- SFU (Selective Forwarding Unit) architecture
- Adaptive bitrate and simulcast
- Network adaptation (FEC, jitter buffering)
- Global edge network with TURN servers
- Recording and cloud storage
- End-to-end encryption

**Core Challenges:**
- Sub-150ms end-to-end latency
- 1000+ participants per meeting
- Real-time audio/video synchronization
- Handling poor network conditions

## Advanced Patterns

### Distributed Systems Patterns

#### Replication & Consistency
- **Leader-based Replication**: Single leader for writes, multiple replicas for reads
- **Multi-leader Replication**: Multiple regions, conflict resolution required
- **Leaderless Replication**: Quorum-based (Dynamo, Cassandra)
- **Consensus Algorithms**: Raft, Paxos for strong consistency

#### Partitioning & Sharding
- **Consistent Hashing**: Even distribution, minimal rebalancing
- **Range-based Partitioning**: Good for range queries, risk of hot spots
- **Hash-based Partitioning**: Even distribution, no range queries
- **Secondary Indexes**: Local vs. global indexes trade-offs

#### Failure Handling
- **Failure Detection**: Gossip protocol, heartbeats
- **Failover**: Automatic leader election (Raft)
- **Split-brain Prevention**: Quorum-based decisions
- **Hinted Handoff**: Temporary storage when node down

### Storage Engine Patterns

#### LSM Tree (Log-Structured Merge Tree)
- **Write Path**: Memtable → SSTable
- **Read Path**: Memtable → SSTables (newest to oldest)
- **Compaction**: Size-tiered vs. leveled
- **Bloom Filters**: Skip unnecessary disk reads

#### B-Tree
- **Write Path**: In-place updates
- **Read Path**: Single tree traversal
- **WAL**: Write-ahead log for durability
- **Use Cases**: Traditional databases (PostgreSQL, MySQL)

### Network & Real-Time Patterns

#### Media Streaming
- **Mesh**: P2P, doesn't scale
- **MCU**: Server mixes streams, high CPU
- **SFU**: Server forwards streams, scalable

#### Bandwidth Adaptation
- **Simulcast**: Send multiple quality layers
- **SVC (Scalable Video Coding)**: Single stream, multiple layers
- **ABR (Adaptive Bitrate)**: Client-side quality switching

#### Latency Reduction
- **Edge Computing**: Process near users
- **Anycast DNS**: Route to nearest server
- **Protocol Optimization**: UDP vs. TCP, QUIC

## Consistency Models

### Strong Consistency
- **Linearizability**: Appears as single copy
- **Sequential Consistency**: Program order preserved
- **Implementation**: Raft, Paxos, Spanner
- **Cost**: Higher latency, lower availability

### Eventual Consistency
- **Convergence**: Eventually all replicas agree
- **Conflict Resolution**: Last-write-wins, CRDTs, vector clocks
- **Implementation**: Dynamo, Cassandra
- **Benefit**: Lower latency, higher availability

### Causal Consistency
- **Causally related ops** are ordered
- **Concurrent ops** can be reordered
- **Implementation**: Vector clocks, Hybrid Logical Clocks
- **Sweet spot**: Between strong and eventual

## CAP Theorem

**Choose 2 of 3:**
- **C** (Consistency): All nodes see same data
- **A** (Availability): Every request receives response
- **P** (Partition Tolerance): System continues despite network partitions

**In Reality:**
- Partition tolerance is required (networks fail)
- Trade-off: Consistency vs. Availability

**Examples:**
- **CP Systems**: HBase, MongoDB (strong consistency mode), Spanner
- **AP Systems**: Cassandra, DynamoDB, Riak
- **CA Systems**: Don't exist in distributed systems (network partitions happen)

## Interview Strategy for Hard Problems

### 1. Requirements Clarification (5-10 min)
- Scale: Users, data size, request rate
- Features: Core vs. nice-to-have
- Constraints: Latency, consistency, cost

### 2. High-Level Design (10-15 min)
- Draw architecture diagram
- Identify major components
- Explain data flow
- Discuss trade-offs at high level

### 3. Deep Dive (20-25 min)
- Pick 2-3 critical areas based on interviewer interest:
  - Data model and partitioning
  - Replication and consistency
  - Failure handling
  - Specific algorithms (Raft, consistent hashing)
- Show detailed understanding
- Discuss implementation challenges

### 4. Bottlenecks & Optimizations (5-10 min)
- Identify performance bottlenecks
- Propose solutions
- Discuss monitoring and operations

## Key Technologies

### Storage & Databases
- **Object Storage**: S3, Google Cloud Storage, MinIO
- **NoSQL Databases**: Cassandra, DynamoDB, Riak, ScyllaDB
- **NewSQL**: Google Spanner, CockroachDB, TiDB
- **Time-Series**: InfluxDB, TimescaleDB

### Consensus & Coordination
- **Consensus**: Raft, Multi-Paxos
- **Leader Election**: ZooKeeper, etcd, Consul
- **Distributed Locks**: Redlock, Chubby

### Message Queues & Streaming
- **Message Queues**: Kafka, RabbitMQ, Pulsar
- **Stream Processing**: Flink, Spark Streaming, Storm

### Monitoring & Observability
- **Metrics**: Prometheus, Datadog, Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: Jaeger, Zipkin, OpenTelemetry

## Common Pitfalls to Avoid

1. **Ignoring Scale**: Always start with scale calculations
2. **Overengineering**: Start simple, optimize later
3. **Single Points of Failure**: Identify and eliminate SPOFs
4. **Neglecting Failure Scenarios**: Discuss what happens when things break
5. **Vague Answers**: Be specific about algorithms, numbers, trade-offs
6. **Not Justifying Decisions**: Explain why you chose specific approaches

## Study Resources

### Books
- **Designing Data-Intensive Applications** by Martin Kleppmann (Essential!)
- **Database Internals** by Alex Petrov
- **Distributed Systems** by Maarten van Steen & Andrew S. Tanenbaum

### Papers
- **Dynamo** (Amazon): AP key-value store
- **Bigtable** (Google): Wide-column store
- **Spanner** (Google): Globally distributed SQL database
- **Cassandra** (Facebook/Apache): Distributed NoSQL
- **Raft Consensus**: Understandable consensus algorithm

### Blogs & Talks
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/)
- [The Morning Paper](https://blog.acolyer.org/) - Research paper summaries
- [Distributed Systems Course (MIT 6.824)](https://pdos.csail.mit.edu/6.824/)

### Courses
- **Distributed Systems (MIT 6.824)**: Free, excellent course
- **Database Systems (CMU 15-445)**: Deep dive into DB internals
- **Grokking System Design Interview**: Practice problems

## Practice Approach

1. **Understand Fundamentals First**: Don't jump to hard problems without strong fundamentals
2. **Read the Papers**: Understand how real systems work (Dynamo, Bigtable, Spanner)
3. **Draw Diagrams**: Practice sketching architectures on paper/whiteboard
4. **Implement Toy Versions**: Build simplified versions (e.g., mini-Cassandra)
5. **Mock Interviews**: Practice explaining designs out loud

## Progression Path

1. **Master Easy Problems**: Understand basics
2. **Solve Medium Problems**: Learn distributed patterns
3. **Tackle Hard Problems**: Build foundational infrastructure
4. **Study Real Systems**: Read architecture blogs from FAANG
5. **Mock Interviews**: Practice with peers or interviewers

## Success Metrics

You're ready for senior/staff level interviews when you can:
- ✅ Design distributed systems from scratch
- ✅ Explain CAP theorem and consistency models
- ✅ Choose appropriate replication strategies
- ✅ Design for failure and handle edge cases
- ✅ Make and justify trade-off decisions
- ✅ Estimate scale and identify bottlenecks
- ✅ Discuss operational concerns (monitoring, debugging)

Good luck with your system design journey!
