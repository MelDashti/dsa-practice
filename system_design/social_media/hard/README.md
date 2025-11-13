# Hard Social Media System Design Problems

This directory contains deep-dive system design problems focused on specific complex components that power social media platforms. These problems require advanced knowledge of distributed systems, algorithms, and large-scale architecture.

## Overview

Hard-level system design problems focus on:
- Designing specific critical components in depth
- Advanced algorithms and data structures
- Extreme scale considerations (billions of users, petabytes of data)
- Complex distributed systems challenges
- Deep understanding of trade-offs
- Performance optimization at scale
- Advanced caching and storage strategies

## Problems in This Section

### 1. News Feed Generation Algorithm
**File:** `design_news_feed.md`

Design the core algorithm that powers Facebook's News Feed, including ranking, personalization, and real-time updates.

**Key Challenges:**
- Fanout strategies at extreme scale
- Real-time ranking algorithm
- Personalization with ML
- Handling celebrity/viral content
- Edge rank algorithm
- Story bumping
- Feed diversity

**Topics Covered:**
- Multi-stage ranking pipeline
- ML-based feed ranking
- Fanout on write vs. read trade-offs
- GraphQL for flexible feed queries
- Real-time updates with WebSockets
- A/B testing infrastructure
- Feed diversity algorithms

**Estimated Time:** 75-90 minutes

---

### 2. Social Graph Service
**File:** `design_social_graph.md`

Design a highly scalable service to store and query social relationships (friends, followers, connections) for billions of users.

**Key Challenges:**
- Storing billions of relationships
- Fast friend/follower queries
- Mutual friends calculation
- Friend suggestions algorithm
- Handling bidirectional relationships
- Graph traversal at scale
- Privacy and visibility rules

**Topics Covered:**
- Graph database vs. relational database
- Adjacency list storage
- Bidirectional indexing
- Graph algorithms (BFS, shortest path)
- Friend recommendation algorithms
- Denormalization strategies
- Consistent hashing for graph sharding

**Estimated Time:** 75-90 minutes

## What Makes These Problems "Hard"?

### 1. Depth Over Breadth
Unlike easy/medium problems that cover entire systems, hard problems dive deep into:
- Specific algorithm implementation details
- Data structure choices and trade-offs
- Query optimization strategies
- Cache coherence protocols
- Consistency models

### 2. Scale Complexity
Hard problems deal with:
- Billions of entities
- Petabytes of data
- Millions of QPS
- Sub-millisecond latency requirements
- Global distribution challenges

### 3. Advanced Concepts
Requires knowledge of:
- Advanced data structures (skip lists, B+ trees, LSM trees)
- Distributed algorithms (Paxos, Raft, vector clocks)
- Graph algorithms (PageRank, collaborative filtering)
- ML systems (feature stores, model serving)
- Stream processing (Apache Flink, Kafka Streams)

### 4. Real-World Constraints
Must consider:
- Cost optimization ($millions in infrastructure)
- Privacy and security
- Regulatory compliance (GDPR, CCPA)
- Disaster recovery
- Multi-datacenter coordination

## Key Concepts Deep Dive

### 1. Feed Ranking Algorithms

**EdgeRank (Facebook's Original Algorithm):**
```
EdgeRank Score = Affinity × Weight × Time Decay

Where:
- Affinity: How often user interacts with content creator
- Weight: Type of interaction (comment > like > view)
- Time Decay: Exponential decay based on post age
```

**Modern ML-Based Ranking:**
```python
# Two-stage ranking

# Stage 1: Candidate Generation (fast, approximate)
candidates = generate_candidates(user, limit=1000)

# Stage 2: Heavy ranking (ML model, expensive)
for each candidate:
    features = extract_features(user, post)
    score = ml_model.predict(features)

ranked = sort(candidates, by=score, descending=True)
return ranked[:20]
```

**Factors Considered:**
- User engagement history
- Content type preference (photo vs. video vs. text)
- Recency
- Creator relationship (close friend vs. acquaintance)
- Engagement velocity (trending content)
- Diversity (don't show 10 posts from same person)
- Clickbait detection (penalize)

---

### 2. Graph Storage Strategies

**Adjacency List (Most Common):**

```sql
-- Two tables for bidirectional relationships

-- Outgoing edges (who I follow)
CREATE TABLE following (
    user_id BIGINT,
    followee_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, followee_id)
);

-- Incoming edges (who follows me)
CREATE TABLE followers (
    user_id BIGINT,  -- the person being followed
    follower_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, follower_id)
);

-- Why two tables?
-- Fast queries for both:
-- - "Who does Alice follow?" → Query following WHERE user_id = alice_id
-- - "Who follows Alice?" → Query followers WHERE user_id = alice_id
```

**Graph Database (Neo4j, JanusGraph):**
```cypher
// Create relationship
CREATE (alice:User {id: 1})-[:FOLLOWS]->(bob:User {id: 2})

// Find friends of friends
MATCH (alice:User {id: 1})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(fof)
WHERE NOT (alice)-[:FOLLOWS]->(fof) AND fof.id != alice.id
RETURN DISTINCT fof
LIMIT 10

// Pros: Natural graph queries, efficient traversal
// Cons: Harder to scale horizontally, less mature than SQL
```

**Hybrid Approach (Best of Both Worlds):**
```
- Store edges in SQL/NoSQL (scalability)
- Build graph index in memory for fast traversal
- Use graph database for complex queries (friend suggestions)
- Cache common queries (mutual friends) in Redis
```

---

### 3. Fanout Strategies

**Fanout on Write (Push Model):**

```python
def on_post_created(user_id, post_id):
    # Get all followers
    followers = get_followers(user_id)  # Could be millions

    # Write to each follower's inbox
    for follower_id in followers:
        feed_inbox.insert(follower_id, post_id)

    # Pros: Fast reads (feed pre-computed)
    # Cons: Slow writes, celebrity problem
```

**Fanout on Read (Pull Model):**

```python
def get_feed(user_id):
    # Get users this person follows
    following = get_following(user_id)

    # Query recent posts from each
    posts = []
    for followee_id in following:
        recent = get_recent_posts(followee_id, limit=10)
        posts.extend(recent)

    # Merge and rank
    ranked = rank_posts(posts)
    return ranked[:20]

    # Pros: No celebrity problem, fresh data
    # Cons: Slow reads, query amplification
```

**Hybrid (Best Practice):**

```python
def hybrid_fanout(user_id, post_id):
    follower_count = get_follower_count(user_id)

    if follower_count < 10000:
        # Regular user: fanout on write
        fanout_on_write(user_id, post_id)
    else:
        # Celebrity: fanout on read
        mark_as_celebrity_post(user_id, post_id)

def get_feed_hybrid(user_id):
    # Get pre-computed posts (from non-celebrities)
    inbox_posts = get_inbox_posts(user_id)

    # Get recent posts from celebrities
    celebrity_posts = get_celebrity_posts(user_id)

    # Merge and rank
    return rank_posts(inbox_posts + celebrity_posts)
```

---

### 4. Real-Time Feed Updates

**Problem:** User creates post, followers should see it immediately

**Solutions:**

**1. WebSockets (Best for Real-Time):**
```python
# When user creates post
def on_post_created(post):
    active_followers = get_online_followers(post.user_id)

    for follower_id in active_followers:
        websocket_server.send(follower_id, {
            "type": "new_post",
            "post": post
        })

# Client receives and inserts at top of feed
```

**2. Long Polling (Fallback):**
```python
# Client polls every 30 seconds
GET /api/feed/updates?since={last_post_id}

# Server holds request until new content available
# Or timeout after 30 seconds
```

**3. Server-Sent Events (SSE):**
```python
# Server pushes updates to client
GET /api/feed/stream

# Server keeps connection open, sends events:
event: new_post
data: {"post_id": "123", ...}
```

---

### 5. Caching Strategies for Feed

**Multi-Level Caching:**

```
Level 1: CDN (Static content - images, videos)
Level 2: Redis (Feed cache, user profiles)
Level 3: Application cache (Hot data in memory)
Level 4: Database query cache
```

**Cache Invalidation:**

```python
# Problem: User posts, need to invalidate followers' feeds

# Naive approach (too expensive):
def invalidate_all_feeds(user_id):
    followers = get_followers(user_id)
    for follower_id in followers:
        cache.delete(f"feed:{follower_id}")
    # If celebrity has 100M followers, this takes forever!

# Better approach (lazy invalidation):
def get_feed_cached(user_id):
    cache_key = f"feed:{user_id}"
    version_key = f"feed_version:{user_id}"

    cached = cache.get(cache_key)
    cached_version = cache.get(version_key)
    current_version = get_current_feed_version(user_id)

    if cached and cached_version == current_version:
        return cached

    # Regenerate
    feed = generate_feed(user_id)
    cache.set(cache_key, feed, ttl=300)
    cache.set(version_key, current_version, ttl=300)
    return feed

# Increment version when following graph changes
def on_follow(follower_id, followee_id):
    cache.incr(f"feed_version:{follower_id}")
```

---

### 6. Friend Suggestion Algorithms

**1. Mutual Friends:**
```sql
-- Find users with most mutual friends

SELECT friend_of_friend, COUNT(*) as mutual_count
FROM (
    -- Get my friends
    SELECT followee_id as my_friend
    FROM following
    WHERE user_id = ?
) my_friends
JOIN following fof ON my_friends.my_friend = fof.user_id
WHERE fof.followee_id != ?  -- Not myself
  AND fof.followee_id NOT IN (
      SELECT followee_id FROM following WHERE user_id = ?
  )  -- Not already following
GROUP BY fof.followee_id
ORDER BY mutual_count DESC
LIMIT 10;
```

**2. Graph-Based (People You May Know - PYMK):**

```python
# Use graph algorithms like collaborative filtering

def suggest_friends(user_id):
    # Get user's friends
    friends = get_friends(user_id)

    # Get friends' friends (depth 2)
    suggestions = {}
    for friend_id in friends:
        fof = get_friends(friend_id)
        for fof_id in fof:
            if fof_id != user_id and fof_id not in friends:
                # Score based on number of mutual friends
                suggestions[fof_id] = suggestions.get(fof_id, 0) + 1

    # Additional signals
    for user in suggestions:
        score = suggestions[user]

        # Boost if same school/company
        if same_school(user_id, user):
            score *= 2

        # Boost if similar interests
        similarity = calculate_interest_similarity(user_id, user)
        score *= (1 + similarity)

        suggestions[user] = score

    # Return top suggestions
    return sorted(suggestions.items(), key=lambda x: x[1], reverse=True)[:10]
```

**3. Machine Learning Approach:**
```python
# Train model to predict P(user will accept friend request)

features = {
    'mutual_friends_count': 5,
    'mutual_groups': 2,
    'same_school': 1,
    'same_company': 0,
    'geographic_distance': 50,  # miles
    'age_difference': 3,
    'interest_similarity': 0.7,
    'activity_similarity': 0.5
}

probability = ml_model.predict(features)

# Rank suggestions by probability
```

---

### 7. Query Optimization for Social Graphs

**Problem:** "Get mutual friends" query is expensive

**Naive Query (Slow):**
```sql
SELECT f1.followee_id as mutual_friend
FROM following f1
JOIN following f2 ON f1.followee_id = f2.followee_id
WHERE f1.user_id = ? AND f2.user_id = ?
```

**Optimized Approach:**
```python
# Use set intersection (much faster)

def get_mutual_friends(user_id1, user_id2):
    # Get both friend lists (from cache)
    friends1 = set(cache.smembers(f"friends:{user_id1}"))
    friends2 = set(cache.smembers(f"friends:{user_id2}"))

    # Set intersection (O(min(n, m)))
    mutual = friends1 & friends2

    return list(mutual)

# Precompute and cache friend lists
def cache_friend_list(user_id):
    friends = db.query(
        "SELECT followee_id FROM following WHERE user_id = ?",
        user_id
    )
    cache.sadd(f"friends:{user_id}", *friends)
    cache.expire(f"friends:{user_id}", 3600)
```

---

### 8. Handling Privacy in Social Graphs

**Friend Lists Visibility:**

```python
def can_see_friends(viewer_id, profile_user_id):
    # Get privacy setting
    privacy = get_privacy_setting(profile_user_id, 'friends_list')

    if privacy == 'public':
        return True
    elif privacy == 'friends':
        return is_friend(viewer_id, profile_user_id)
    elif privacy == 'private':
        return viewer_id == profile_user_id
    else:
        return False

def get_visible_friends(viewer_id, profile_user_id):
    if not can_see_friends(viewer_id, profile_user_id):
        raise PermissionDenied()

    friends = get_friends(profile_user_id)

    # Filter out friends who have blocked viewer
    visible = [
        f for f in friends
        if not has_blocked(f, viewer_id)
    ]

    return visible
```

## Interview Approach for Hard Problems

### 1. Clarify Constraints (10 minutes)
- Exact scale numbers (QPS, data volume)
- Latency requirements
- Consistency requirements
- Budget constraints

### 2. High-Level Design (10-15 minutes)
- Don't spend too much time here
- Focus on the specific component being designed
- Show you understand the big picture

### 3. Deep Dive (45-60 minutes)
This is where hard problems differ:

**For Feed Ranking:**
- Explain ranking algorithm in detail
- Discuss feature engineering
- ML model architecture
- A/B testing methodology
- Performance optimization

**For Social Graph:**
- Data structure choices
- Query optimization strategies
- Sharding strategy
- Index design
- Graph algorithms

### 4. Optimizations (10-15 minutes)
- Caching strategies
- Database indexing
- Denormalization trade-offs
- Approximation algorithms (for suggestion)

### 5. Monitoring and Operations (5 minutes)
- Key metrics to track
- Alerting strategies
- Debugging approaches

## Common Pitfalls to Avoid

### 1. Not Going Deep Enough
Hard problems require depth. Don't just say "use ML" - explain the model, features, training pipeline.

### 2. Ignoring Scale
Everything works at small scale. Focus on what breaks at billions of users.

### 3. Over-Engineering
Start simple, then optimize. Don't jump to complex solutions immediately.

### 4. Forgetting Trade-offs
Every decision has trade-offs. Discuss pros/cons explicitly.

### 5. Ignoring Cost
At this scale, infrastructure costs millions. Discuss cost optimization.

## Advanced Topics to Study

### Distributed Systems:
- Consensus algorithms (Paxos, Raft)
- Consistent hashing
- Vector clocks
- CAP theorem implications

### Database Internals:
- B+ tree vs LSM tree
- Write amplification
- Read amplification
- Query planning and optimization

### Machine Learning Systems:
- Feature stores (Feast, Tecton)
- Model serving (TensorFlow Serving, TorchServe)
- Online learning
- A/B testing platforms

### Graph Algorithms:
- Breadth-First Search (BFS)
- PageRank
- Community detection
- Shortest path algorithms

### Stream Processing:
- Apache Kafka
- Apache Flink
- Exactly-once semantics
- Windowing and aggregation

## Success Criteria

You've mastered hard problems when you can:

- Design systems for billions of users with specific latency requirements
- Explain algorithm implementations in detail
- Optimize query performance with concrete numbers
- Discuss ML system architecture and training pipelines
- Make and justify complex trade-off decisions
- Estimate costs and optimize for budget
- Design for global scale with multi-region considerations

## Resources

### Papers:
- "TAO: Facebook's Distributed Data Store for the Social Graph"
- "The Anatomy of a Large-Scale Hypertextual Web Search Engine" (Google)
- "The Chubby Lock Service for Loosely-Coupled Distributed Systems"

### Books:
- "Designing Data-Intensive Applications" (Martin Kleppmann) - Chapters 6-12
- "Web Scalability for Startup Engineers" (Artur Ejsmont)
- "Database Internals" (Alex Petrov)

### Courses:
- "Mining Massive Datasets" (Stanford)
- "Large Scale Machine Learning" (Coursera)

---

**Time Investment:** 40-60 hours to master hard problems

**Recommendation:** Master medium problems first before attempting hard problems
