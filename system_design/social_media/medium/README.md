# Medium Social Media System Design Problems

This directory contains full-featured social media platform designs that incorporate complex features, distributed systems concepts, and advanced scalability patterns.

## Overview

Medium-level system design problems require understanding of:
- Distributed systems architecture
- Microservices patterns
- Advanced caching strategies
- Message queues and async processing
- Complex algorithms (recommendations, ranking, trending)
- Real-time features
- Data partitioning and sharding
- Multi-region deployments

## Problems in This Section

### 1. Instagram (Full Featured)
**File:** `design_instagram.md`

Complete Instagram system with stories, explore feed, and recommendations.

**Key Features:**
- Feed with algorithmic ranking
- Stories (24-hour content)
- Explore page with recommendations
- Video support (Reels)
- Direct messaging
- Search and discovery

**Complexity Additions:**
- Recommendation algorithms
- Real-time story updates
- Video streaming infrastructure
- Graph database for social connections
- Multi-region data replication

**Estimated Time:** 60-75 minutes

---

### 2. Twitter/X
**File:** `design_twitter.md`

Real-time microblogging platform with trending topics and timeline generation.

**Key Features:**
- Tweet creation and threading
- Timeline generation (home, user)
- Trending topics algorithm
- Mentions and notifications
- Retweets and quote tweets
- Search and hashtags

**Complexity Additions:**
- Real-time trending calculation
- Fan-out service architecture
- Timeline generation at scale
- Full-text search implementation
- Rate limiting and abuse prevention

**Estimated Time:** 60-75 minutes

---

### 3. Reddit
**File:** `design_reddit.md`

Community-driven content platform with voting and nested comments.

**Key Features:**
- Subreddit creation and moderation
- Post creation (text, link, media)
- Upvote/downvote system
- Nested comment threads
- Hot/Top/New ranking algorithms
- User karma system

**Complexity Additions:**
- Vote counting at scale
- Ranking algorithms (hot, controversial)
- Nested comment storage and retrieval
- Moderation tools and spam detection
- Real-time vote updates

**Estimated Time:** 60-75 minutes

---

### 4. TikTok
**File:** `design_tiktok.md`

Short-form video platform with personalized For You Page.

**Key Features:**
- Video upload and processing
- For You Page (FYP) algorithm
- Following feed
- Likes, comments, shares
- Video effects and filters
- Duets and stitches

**Complexity Additions:**
- Video encoding and adaptive streaming
- ML-based recommendation system
- Real-time video processing
- Global content distribution
- Collaborative filtering algorithm

**Estimated Time:** 60-75 minutes

## Key Concepts to Master

### 1. Microservices Architecture

Break monolithic applications into smaller, independent services:

```
User Service    Post Service    Feed Service    Notification Service
     |               |                |                   |
     +---------------+----------------+-------------------+
                            |
                    [Message Bus / Event Stream]
                            |
     +---------------+----------------+-------------------+
     |               |                |                   |
Search Service  Analytics     Media Service      Cache Service
```

**Benefits:**
- Independent scaling
- Technology diversity
- Fault isolation
- Easier deployment

**Challenges:**
- Service discovery
- Distributed transactions
- Network latency
- Debugging complexity

---

### 2. Advanced Caching Strategies

**Multi-Level Caching:**

```
[Browser Cache] -> [CDN] -> [Application Cache] -> [Database Cache] -> [Database]
```

**Cache Patterns:**

1. **Cache-Aside (Lazy Loading):**
   - Application checks cache first
   - On miss, load from database and populate cache

2. **Write-Through:**
   - Write to cache and database simultaneously
   - Ensures consistency

3. **Write-Behind (Write-Back):**
   - Write to cache immediately
   - Asynchronously write to database
   - Better performance, eventual consistency

4. **Read-Through:**
   - Cache automatically loads from database on miss

**Cache Invalidation Strategies:**
- TTL (Time To Live)
- Event-based invalidation
- Version-based invalidation

---

### 3. Message Queues and Event-Driven Architecture

**Use Cases:**
- Decouple services
- Handle traffic spikes
- Async processing
- Event sourcing

**Technologies:**
- **Apache Kafka:** High-throughput streaming
- **RabbitMQ:** Traditional message queue
- **AWS SQS:** Managed queue service
- **Redis Streams:** Lightweight streaming

**Patterns:**

1. **Pub/Sub:**
   ```
   Publisher -> [Topic] -> Multiple Subscribers
   ```

2. **Work Queue:**
   ```
   Producer -> [Queue] -> Competing Consumers
   ```

3. **Event Sourcing:**
   ```
   Events -> [Event Store] -> Materialized Views
   ```

---

### 4. Data Partitioning and Sharding

**Why Shard?**
- Single database can't handle all data
- Horizontal scaling requirement
- Distribute load across multiple machines

**Sharding Strategies:**

1. **Hash-Based Sharding:**
   ```
   shard = hash(user_id) % num_shards
   ```
   - Pros: Even distribution
   - Cons: Difficult to add shards

2. **Range-Based Sharding:**
   ```
   Shard 1: user_id 1-1M
   Shard 2: user_id 1M-2M
   ```
   - Pros: Easy to add shards
   - Cons: Potential hotspots

3. **Geo-Based Sharding:**
   ```
   US Users -> US Shard
   EU Users -> EU Shard
   ```
   - Pros: Low latency, compliance
   - Cons: Uneven distribution

**Challenges:**
- Cross-shard queries
- Rebalancing shards
- Maintaining relationships

---

### 5. Recommendation Systems

**Collaborative Filtering:**
- User-based: Find similar users
- Item-based: Find similar items
- Matrix factorization

**Content-Based Filtering:**
- Analyze item features
- Match with user preferences

**Hybrid Approaches:**
- Combine multiple signals
- Machine learning models

**Implementation Considerations:**
- Offline batch processing
- Online serving layer
- A/B testing framework
- Cold start problem

---

### 6. Real-Time Features

**WebSockets:**
- Bi-directional communication
- Keep connection open
- Push updates to clients

**Server-Sent Events (SSE):**
- One-way (server to client)
- Simpler than WebSockets
- Automatic reconnection

**Long Polling:**
- Client polls server
- Server holds request until data available
- Fallback for old browsers

**Technologies:**
- Socket.io
- AWS AppSync
- Firebase Realtime Database

---

### 7. Search Implementation

**Full-Text Search:**
- Inverted index
- Tokenization and stemming
- Relevance ranking

**Technologies:**
- **Elasticsearch:** Distributed search engine
- **Apache Solr:** Enterprise search
- **AWS CloudSearch:** Managed service

**Search Optimizations:**
- Auto-complete (Trie data structure)
- Fuzzy matching
- Synonym handling
- Faceted search

---

### 8. Rate Limiting

**Algorithms:**

1. **Token Bucket:**
   - Tokens added at fixed rate
   - Request consumes token
   - Allows bursts

2. **Leaky Bucket:**
   - Fixed rate processing
   - Smooths traffic
   - No bursts allowed

3. **Fixed Window:**
   - Count requests in time window
   - Simple but can have burst at boundary

4. **Sliding Window:**
   - More accurate than fixed window
   - Combines counters from multiple windows

**Implementation:**
```python
# Redis-based rate limiter
def is_allowed(user_id, limit, window):
    key = f"rate_limit:{user_id}"
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, window)
    return current <= limit
```

## Common Architecture Patterns

### Pattern 1: Fan-Out Service

**Problem:** User posts content, need to update all followers' feeds

**Solutions:**

1. **Fan-Out on Write:**
   ```
   New Post -> Write to all followers' feeds immediately
   - Fast reads
   - Slow writes for celebrities
   - High storage
   ```

2. **Fan-Out on Read:**
   ```
   New Post -> Store in user's outbox
   Feed generation -> Query followed users' outboxes
   - Fast writes
   - Slower reads
   - Less storage
   ```

3. **Hybrid:**
   ```
   Regular users: Fan-out on write
   Celebrities: Fan-out on read
   ```

---

### Pattern 2: CQRS (Command Query Responsibility Segregation)

**Concept:** Separate read and write models

```
Write Model:                    Read Model:
[Commands] -> [Event Store] -> [Projections] -> [Query Database]
```

**Benefits:**
- Optimize reads and writes separately
- Scale independently
- Better performance

---

### Pattern 3: Circuit Breaker

**Problem:** Cascade failures when service is down

**Solution:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold, timeout):
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func):
        if self.state == "OPEN":
            raise Exception("Circuit is OPEN")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
```

---

### Pattern 4: Saga Pattern

**Problem:** Distributed transactions across microservices

**Solutions:**

1. **Choreography:**
   - Each service publishes events
   - Other services react to events
   - Decentralized

2. **Orchestration:**
   - Central coordinator
   - Manages transaction steps
   - Centralized control

## Scalability Deep Dive

### Scaling Reads

1. **Caching Layers:**
   - Application cache (Redis)
   - Query result cache
   - Object cache
   - CDN for static content

2. **Database Read Replicas:**
   - Master-slave replication
   - Read from slaves
   - Replication lag consideration

3. **Database Indexing:**
   - B-tree indexes
   - Covering indexes
   - Partial indexes
   - Query optimization

---

### Scaling Writes

1. **Database Sharding:**
   - Horizontal partitioning
   - Consistent hashing
   - Shard key selection

2. **Queue-Based Processing:**
   - Async writes
   - Batch processing
   - Eventual consistency

3. **Write-Optimized Storage:**
   - LSM trees (Cassandra, RocksDB)
   - Append-only logs

---

### Scaling Storage

1. **Tiered Storage:**
   - Hot data: SSD
   - Warm data: HDD
   - Cold data: S3 Glacier

2. **Data Compression:**
   - Compress old data
   - Trade CPU for storage

3. **Data Archival:**
   - Move old data to cheaper storage
   - Delete unnecessary data

## Trade-Off Analysis Framework

When making design decisions, consider:

### 1. Consistency vs. Availability (CAP Theorem)
- Strong consistency: Slower, less available
- Eventual consistency: Faster, more available

### 2. Latency vs. Throughput
- Low latency: Quick responses
- High throughput: More requests processed

### 3. Cost vs. Performance
- Higher performance: More expensive
- Cost optimization: Some performance sacrifice

### 4. Complexity vs. Scalability
- Simple architecture: Easier to maintain
- Complex architecture: Better scalability

### 5. Flexibility vs. Performance
- Generic solutions: More flexible
- Specialized solutions: Better performance

## Interview Approach for Medium Problems

### 1. Requirements Gathering (5-10 minutes)
- Clarify functional requirements
- Define scale expectations
- Identify critical features
- Discuss constraints

### 2. High-Level Design (10-15 minutes)
- Draw system architecture
- Identify major components
- Explain data flow
- Discuss API design

### 3. Deep Dives (20-30 minutes)
Choose 2-3 areas to dive deep:
- Database schema
- Specific algorithm (ranking, recommendation)
- Scalability bottleneck
- Real-time feature implementation

### 4. Trade-Offs and Alternatives (10 minutes)
- Discuss design decisions
- Explain alternatives
- Justify choices

### 5. Wrap-Up (5 minutes)
- Monitoring and metrics
- Potential improvements
- Answer follow-up questions

## Common Pitfalls to Avoid

1. **Over-Engineering:** Don't add complexity without justification
2. **Ignoring Scale:** Always consider numbers and calculations
3. **Single Point of Failure:** Identify and eliminate SPOFs
4. **No Monitoring:** Always discuss observability
5. **Ignoring Security:** At least mention authentication/authorization
6. **Perfect Solution:** No design is perfect; acknowledge trade-offs
7. **Skipping API Design:** APIs are crucial for component interaction

## Success Criteria

You've mastered medium problems when you can:
- Design systems for 100M+ users
- Explain complex algorithms (ranking, recommendations)
- Design microservices architecture
- Implement distributed caching
- Handle real-time features
- Plan for multi-region deployment
- Discuss advanced trade-offs

## Progression to Hard Problems

After mastering medium problems, move to hard problems which focus on:
- Designing specific complex components
- Deep algorithmic challenges
- Extreme scale (billions of users)
- Advanced distributed systems concepts
- Multi-datacenter coordination
- Custom protocols
- ML infrastructure

---

**Recommended Study Order:**
1. Instagram (builds on MVP)
2. Twitter (introduces real-time concepts)
3. Reddit (voting and ranking algorithms)
4. TikTok (recommendation systems and video processing)

**Total Time Investment:** 20-30 hours to master all medium problems
