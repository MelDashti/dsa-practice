# Hard - Messaging Systems

This directory contains advanced messaging system design problems that involve complex features, extreme scale, cross-platform integration, and sophisticated infrastructure. These problems require deep understanding of distributed systems, data consistency, multi-region deployment, and advanced optimization techniques.

## Problems

### 1. Facebook Messenger (`design_messenger.md`)
Design a comprehensive messaging platform with cross-platform support, voice/video, stories, payments, and deep social integration.

**Key Concepts**:
- Multi-region active-active deployment
- Cross-platform synchronization (web, mobile, desktop, VR)
- Voice/Video calling infrastructure (WebRTC)
- Stories with 24-hour expiry
- In-app payments and fraud prevention
- Bot platform and business messaging
- AI-powered features (smart replies, translations)
- Social graph integration

**Advanced Challenges**:
- Billions of users, 100B+ messages/day
- Data residency and compliance (GDPR)
- Complex feature integration
- Multi-region consistency
- Cost optimization at scale

### 2. Large-Scale Notification Service (`design_notification_service.md`)
Design a unified notification system handling billions of notifications daily across multiple channels.

**Key Concepts**:
- Multi-channel delivery (push, SMS, email, in-app, webhooks)
- Priority-based queuing and processing
- User preferences and quiet hours
- Rate limiting and throttling
- Delivery guarantees (at-least-once)
- Deduplication strategies
- Provider circuit breakers
- Comprehensive analytics

**Advanced Challenges**:
- 10M+ QPS at peak
- Multiple third-party providers
- Cost optimization (SMS/email costs)
- Compliance (CAN-SPAM, GDPR, TCPA)
- High availability despite provider failures

## Common Patterns in Hard Messaging Problems

### Multi-Region Architecture
- **Active-Active**: Multiple regions handling writes
- **Conflict Resolution**: CRDT, Last-Write-Wins, Vector Clocks
- **Data Replication**: Async replication across regions
- **Regional Routing**: Route users to nearest region
- **Failover**: Automatic regional failover

### Advanced Scaling
- **Sharding Strategies**: By user, conversation, geography
- **Hot Shard Mitigation**: Detect and split hot shards
- **Read/Write Separation**: Separate clusters for reads and writes
- **Caching Layers**: Multi-level caching (L1, L2, L3)
- **Connection Pooling**: Efficient database connections

### Complex Features
- **Voice/Video**: WebRTC, media servers, TURN/STUN
- **Stories**: Ephemeral content with TTL
- **Payments**: PCI compliance, fraud detection
- **Bots**: Webhook infrastructure, rate limiting
- **AI Features**: ML models for smart replies, translations

### Reliability Patterns
- **Circuit Breaker**: Prevent cascade failures
- **Bulkhead**: Isolate failures
- **Retry Logic**: Exponential backoff with jitter
- **Dead Letter Queue**: Handle persistent failures
- **Health Checks**: Proactive failure detection

### Cost Optimization
- **Provider Selection**: Choose cheapest/best provider
- **Batching**: Reduce API calls
- **Deduplication**: Prevent unnecessary sends
- **Compression**: Reduce bandwidth
- **Cold Storage**: Archive old data

## Architectural Comparison

| Aspect | Facebook Messenger | Notification Service |
|--------|-------------------|---------------------|
| **Primary Function** | Direct communication | Broadcast messaging |
| **Scale** | 3B users, 100B messages/day | 1B users, 10M QPS peak |
| **Latency** | < 100ms global | < 1s for critical |
| **Channels** | Messenger app, web | Push, SMS, email, in-app |
| **Complexity** | Very high (many features) | High (multi-channel) |
| **Cost Focus** | Infrastructure | Third-party APIs |
| **Data Model** | Conversation-centric | User-centric |
| **Delivery** | Real-time required | Best-effort acceptable |

## Key Technical Decisions

### 1. Consistency vs Availability
- **Messenger**: Eventual consistency acceptable for most features
- **Notifications**: At-least-once delivery, tolerate duplicates
- **Trade-off**: CAP theorem implications

### 2. Database Selection
- **Cassandra**: High write throughput, time-series data
- **PostgreSQL**: Consistency, complex queries, metadata
- **MySQL**: Proven at scale, good for relational data
- **MongoDB**: Flexible schema, document storage

### 3. Message Queue
- **Kafka**: High throughput, replay, ordering
- **Pulsar**: Multi-tenancy, geo-replication
- **RabbitMQ**: Traditional, reliable, lower throughput
- **SQS**: Managed, serverless, cloud-native

### 4. Caching Strategy
- **Redis**: In-memory, fast, pub/sub
- **Memcached**: Simple, fast, no persistence
- **Application Cache**: Fastest, not distributed

## Interview Approach for Hard Problems

### 1. Requirements Clarification (10 min)
- Understand scale (users, QPS, storage)
- Clarify functional requirements
- Non-functional requirements (latency, availability)
- Constraints and assumptions

### 2. High-Level Design (15 min)
- Draw system architecture
- Identify major components
- Data flow diagrams
- Technology choices

### 3. Deep Dive (20 min)
- Pick 2-3 components for detailed design
- API design
- Data models
- Algorithm/logic

### 4. Trade-offs and Scalability (10 min)
- Discuss alternative approaches
- Explain trade-offs
- Scaling strategies
- Failure scenarios

### 5. Follow-up Questions (5 min)
- How to extend the system
- How to handle specific edge cases
- Monitoring and operations

## Common Hard Problems

### Scale Challenges
- **How to handle 10x growth?**
  - Horizontal scaling
  - Database sharding
  - Regional deployment
  - Caching optimization

- **How to reduce costs at scale?**
  - Optimize third-party API usage
  - Efficient resource utilization
  - Data compression
  - Cold storage for old data

### Reliability Challenges
- **How to ensure 99.99% availability?**
  - Multi-region deployment
  - Graceful degradation
  - Circuit breakers
  - Comprehensive monitoring

- **How to handle provider failures?**
  - Multi-provider setup
  - Automatic failover
  - Circuit breakers
  - Retry strategies

### Consistency Challenges
- **How to maintain ordering across regions?**
  - Lamport timestamps
  - Vector clocks
  - Consensus protocols (Raft, Paxos)

- **How to resolve conflicts?**
  - Last-Write-Wins
  - CRDT
  - Application-level resolution

### Security Challenges
- **How to ensure data privacy?**
  - End-to-end encryption
  - Data residency compliance
  - Access control
  - Audit logging

- **How to prevent fraud?**
  - ML-based detection
  - Rate limiting
  - Behavioral analysis
  - Manual review

## Advanced Topics

### 1. Distributed Tracing
- OpenTelemetry
- Jaeger, Zipkin
- Trace context propagation
- Performance debugging

### 2. Service Mesh
- Istio, Linkerd
- Traffic management
- Security (mTLS)
- Observability

### 3. Event-Driven Architecture
- Event sourcing
- CQRS pattern
- Saga pattern
- Event replay

### 4. Chaos Engineering
- Failure injection
- Resilience testing
- Recovery validation
- Production testing

### 5. Machine Learning Integration
- Real-time inference
- Model serving
- A/B testing
- Feature pipelines

## Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Building Microservices" by Sam Newman
- "System Design Interview" by Alex Xu

### Tech Blogs
- Facebook Engineering Blog
- Netflix Tech Blog
- Uber Engineering Blog
- Discord Engineering Blog
- Slack Engineering Blog

### Papers
- "Dynamo: Amazon's Highly Available Key-value Store"
- "Cassandra - A Decentralized Structured Storage System"
- "The Chubby lock service for loosely-coupled distributed systems"
- "Kafka: A Distributed Messaging System for Log Processing"

### Tools & Technologies
- Apache Kafka / Pulsar
- Cassandra / ScyllaDB
- Redis / KeyDB
- PostgreSQL / CockroachDB
- WebRTC / Janus
- Elasticsearch
- Prometheus / Grafana
- Kubernetes
