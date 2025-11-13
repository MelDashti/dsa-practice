# Infrastructure - Medium Level

## Overview
This directory contains intermediate-level infrastructure system design problems that involve distributed systems, real-time processing, and large-scale data handling. These problems require understanding of distributed computing concepts, data consistency, fault tolerance, and performance optimization.

## Problems

### 1. Design Kafka - Distributed Message Queue
**File**: `design_kafka.md`

**Description**: Design a distributed message queue system similar to Apache Kafka that handles high-throughput, fault-tolerant publish-subscribe messaging with millions of messages per second.

**Key Concepts**:
- Partition-based architecture
- Leader-follower replication
- Consumer groups and rebalancing
- Log-structured storage
- Zero-copy transfers

**Why This Level**:
- Requires understanding of distributed consensus
- Complex coordination with ZooKeeper
- Multiple failure scenarios to handle
- Performance optimization critical

**Related Problems**:
- Easy: Web Crawler Basics (message passing patterns)
- Hard: Distributed Job Scheduler (task queuing)

### 2. Design Web Crawler - Large-Scale (Google-style)
**File**: `design_web_crawler.md`

**Description**: Design a large-scale distributed web crawler that can crawl billions of pages efficiently, prioritize important content, detect duplicates, and respect politeness policies.

**Key Concepts**:
- Distributed URL frontier
- Content deduplication (SimHash, Bloom filters)
- URL prioritization (PageRank)
- Politeness and rate limiting
- Consistent hashing for load distribution

**Why This Level**:
- Scales basic crawler to billions of pages
- Introduces distributed coordination
- Complex prioritization algorithms
- Multiple optimization techniques

**Related Problems**:
- Easy: Web Crawler Basics (foundation)
- Storage: CDN (content distribution)

### 3. Metrics Monitoring System (Prometheus/Datadog-style)
**File**: `metrics_monitoring.md`

**Description**: Design a distributed metrics monitoring system that collects, stores, queries, and visualizes time-series metrics from thousands of services with real-time alerting.

**Key Concepts**:
- Time-series database design
- Data compression (delta encoding, XOR)
- Efficient aggregation queries
- Inverted indexing for labels
- Pull vs push collection models

**Why This Level**:
- Specialized time-series storage design
- Complex query language (PromQL)
- High write throughput requirements
- Efficient compression algorithms

**Related Problems**:
- Medium: Ad Click Aggregation (real-time analytics)
- Hard: Distributed Cache (caching strategies)

### 4. Real-Time Ad Click Event Aggregation
**File**: `ad_click_aggregation.md`

**Description**: Design a real-time analytics system that processes billions of ad clicks per day, computes aggregations across multiple dimensions, detects fraud, and provides sub-second query latency.

**Key Concepts**:
- Stream processing (Apache Flink/Spark)
- Windowing and aggregation
- Fraud detection algorithms
- OLAP databases (ClickHouse, Druid)
- Lambda architecture (batch + streaming)

**Why This Level**:
- Real-time + historical data challenges
- Multiple data stores for different access patterns
- Complex event processing
- Fraud detection adds complexity

**Related Problems**:
- Medium: Metrics Monitoring (time-series aggregation)
- Fundamentals: Rate Limiter (traffic control)

## Learning Path

### Prerequisites
- **Distributed Systems Basics**:
  - CAP theorem
  - Consistency models
  - Replication strategies
  - Partitioning/sharding

- **Data Structures**:
  - Bloom filters
  - HyperLogLog
  - Consistent hashing
  - LSM trees

- **Technologies**:
  - Message queues (Kafka, RabbitMQ)
  - Stream processing (Flink, Spark Streaming)
  - NoSQL databases (Cassandra, HBase)
  - OLAP databases (ClickHouse, Druid)

### Skills Developed

1. **Distributed Systems Design**
   - Partitioning and sharding strategies
   - Replication and consistency
   - Failure handling and recovery
   - Coordination and consensus

2. **Performance Optimization**
   - Compression algorithms
   - Batch processing
   - Caching strategies
   - Zero-copy transfers

3. **Data Modeling**
   - Time-series data
   - Event streaming
   - Log-structured storage
   - Columnar formats

4. **Operational Excellence**
   - Monitoring and alerting
   - Capacity planning
   - Graceful degradation
   - SLA management

### Progression Path
1. Start with **Design Kafka** to understand message queues
2. Move to **Metrics Monitoring** for time-series concepts
3. Study **Ad Click Aggregation** for stream processing
4. Complete with **Web Crawler** for distributed coordination

After mastering medium-level problems, progress to:
- **Hard Level**: Distributed caching, job scheduling, service mesh

## Interview Tips

### Common Questions by Problem

**Design Kafka**
1. How do you handle broker failures?
2. Explain consumer group rebalancing
3. How do you achieve exactly-once semantics?
4. What's the difference between Kafka and RabbitMQ?

**Web Crawler**
1. How do you detect crawler traps?
2. How do you prioritize URLs?
3. How do you handle JavaScript-heavy sites?
4. How do you detect duplicate content?

**Metrics Monitoring**
1. How do you compress time-series data?
2. How do you handle high cardinality?
3. Explain downsampling strategies
4. How do you implement alerting?

**Ad Click Aggregation**
1. How do you detect click fraud?
2. How do you handle late-arriving events?
3. Explain windowing in stream processing
4. How do you ensure billing accuracy?

### Key Discussion Points

**Scalability**
- Horizontal vs vertical scaling
- Sharding strategies
- Bottleneck identification
- Load balancing approaches

**Fault Tolerance**
- Replication strategies (sync vs async)
- Failure detection mechanisms
- Recovery procedures
- Data consistency guarantees

**Performance**
- Latency vs throughput trade-offs
- Caching layers
- Batch vs stream processing
- Compression techniques

**Operations**
- Monitoring and observability
- Capacity planning
- Deployment strategies
- Disaster recovery

## Practice Approach

### Step 1: Requirements (10 minutes)
- Clarify functional requirements
- Define non-functional requirements (scale, latency, consistency)
- Ask about constraints and assumptions
- Identify primary use cases

### Step 2: High-Level Design (15 minutes)
- Draw component diagram
- Identify main data flows
- Explain component responsibilities
- Discuss trade-offs between alternatives

### Step 3: Deep Dive (20 minutes)
- Design data model and storage
- Explain key algorithms
- Discuss failure scenarios
- Optimize for performance

### Step 4: Special Topics (10 minutes)
- Monitoring and alerting
- Scaling strategies
- Security considerations
- Cost optimization

### Step 5: Wrap Up (5 minutes)
- Summarize key decisions
- Discuss trade-offs made
- Mention future improvements
- Answer follow-up questions

## Common Pitfalls to Avoid

1. **Ignoring Scale**: Not considering implications at stated scale
2. **Over-engineering**: Adding unnecessary complexity for small scale
3. **Single Points of Failure**: Not addressing fault tolerance
4. **Ignoring Network Partitions**: Assuming network is always reliable
5. **Poor Data Modeling**: Not optimizing for access patterns
6. **Neglecting Operations**: Forgetting monitoring and debugging
7. **Unrealistic Assumptions**: Ignoring real-world constraints
8. **Skipping Trade-offs**: Not discussing pros/cons of choices

## Key Technologies & Concepts

### Message Queues
- **Apache Kafka**: High-throughput distributed log
- **RabbitMQ**: Traditional message broker
- **Amazon SQS/SNS**: Managed queue services

### Stream Processing
- **Apache Flink**: Stateful stream processing
- **Apache Spark Streaming**: Micro-batch processing
- **Apache Storm**: Real-time computation

### Time-Series Databases
- **Prometheus**: Metrics monitoring
- **InfluxDB**: General-purpose TSDB
- **TimescaleDB**: PostgreSQL extension for time-series

### OLAP Databases
- **ClickHouse**: Fast columnar OLAP
- **Apache Druid**: Real-time analytics
- **Apache Pinot**: Real-time distributed OLAP

### Coordination Services
- **Apache ZooKeeper**: Distributed coordination
- **etcd**: Distributed key-value store
- **Consul**: Service mesh and configuration

## Advanced Concepts

### Consistency Models
- **Strong Consistency**: All nodes see same data
- **Eventual Consistency**: Nodes converge over time
- **Causal Consistency**: Preserves causality
- **Read-your-writes**: Client sees own writes

### Replication Strategies
- **Master-Slave**: One writer, multiple readers
- **Multi-Master**: Multiple writers
- **Quorum-based**: Majority agreement
- **Chain Replication**: Sequential propagation

### Partitioning Strategies
- **Hash-based**: Consistent hashing
- **Range-based**: Key ranges
- **List-based**: Explicit mapping
- **Composite**: Combination of strategies

### Compression Techniques
- **Delta Encoding**: Store differences
- **XOR Compression**: Exploit bit patterns (Gorilla)
- **Dictionary Encoding**: Replace values with codes
- **Run-Length Encoding**: Compress repeated values

## Time Estimates

Per problem:
- **Reading & Understanding**: 45-60 minutes
- **Initial Design**: 45-60 minutes
- **Deep Dive Study**: 2-3 hours
- **Implementation (optional)**: 8-12 hours
- **Interview Discussion**: 45-60 minutes

**Total for Medium Level**: 20-30 hours

## Success Criteria

You've mastered this level when you can:
- Design systems that handle millions of requests per second
- Explain replication and consistency trade-offs
- Choose appropriate partitioning strategies
- Design for fault tolerance and high availability
- Optimize for both latency and throughput
- Discuss operational concerns (monitoring, scaling, debugging)
- Compare and contrast different distributed systems
- Make informed trade-offs based on requirements

## Additional Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Streaming Systems" by Tyler Akidau, Slava Chernyak, Reuven Lax
- "Database Internals" by Alex Petrov
- "Building Microservices" by Sam Newman

### Papers
- "Kafka: A Distributed Messaging System for Log Processing"
- "The Log: What every software engineer should know about real-time data"
- "Gorilla: A Fast, Scalable, In-Memory Time Series Database"
- "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing"

### Online Courses
- MIT 6.824: Distributed Systems
- Apache Kafka Documentation & Tutorials
- Flink Forward Conference Talks
- High Scalability Blog

### Tools to Explore
- Set up local Kafka cluster
- Run Prometheus monitoring stack
- Experiment with ClickHouse queries
- Build simple stream processing pipeline with Flink

## Next Steps

After completing medium-level problems:

1. **Practice Variations**: Try modifying requirements (10x scale, different consistency needs)
2. **Compare Approaches**: Study how different companies solve similar problems
3. **Build Prototypes**: Implement core algorithms to solidify understanding
4. **Read Post-Mortems**: Learn from real-world incidents
5. **Progress to Hard Level**: Tackle distributed cache, job scheduler, service mesh

Remember: The goal isn't to memorize solutions, but to develop intuition for designing distributed systems. Focus on understanding trade-offs and making informed decisions based on requirements.
