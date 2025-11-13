# Design Social Graph Service

## 1. Problem Statement & Scope

Design a highly scalable service to store and query social relationships (friends, followers, connections) for billions of users. This is the foundational component that powers all social features: feeds, friend suggestions, privacy controls, and network analysis.

### In Scope:
- Store friendship/follow relationships
- Query operations (get friends, followers, mutual friends)
- Friend suggestion algorithm
- Graph traversal (friends of friends, degrees of separation)
- Privacy and visibility rules
- Relationship types (friend, follow, block, close friend, family)
- Bidirectional vs unidirectional relationships
- Scale to billions of users and relationships

### Out of Scope:
- Full social media platform (focus on graph only)
- Content storage (posts, photos, videos)
- Messaging system
- Activity feed generation (covered in News Feed design)

### Scale:
- 3 billion users
- Average 200 connections per user
- Total relationships: 600 billion edges
- Query load: 1 million QPS (read-heavy: 99% read, 1% write)
- Mutual friends queries: 100K QPS
- Friend suggestions: 50K requests/second

## 2. Functional Requirements

**FR1: Relationship Management**
- Create friendship/follow relationship
- Remove friendship/unfriend
- Block user
- Unblock user
- Accept/reject friend request
- Set relationship type (close friend, family, acquaintance)

**FR2: Query Operations**
- Get all friends of a user
- Get all followers of a user
- Get users a person is following
- Check if two users are friends
- Get mutual friends between two users
- Get friend count
- Get follower count

**FR3: Graph Traversal**
- Find friends of friends (2nd degree)
- Find shortest path between users
- Calculate degrees of separation
- Find all connections within N degrees

**FR4: Friend Suggestions**
- Suggest friends based on mutual friends
- Suggest based on common interests/groups
- Suggest based on contact import
- Rank suggestions by relevance

**FR5: Privacy and Visibility**
- Respect privacy settings
- Handle blocked users
- Support friend lists (close friends, restricted, etc.)
- Control who can see friend list

## 3. Non-Functional Requirements

### Scale:
- **Users:** 3 billion
- **Edges:** 600 billion (200 connections/user average)
- **Read QPS:** 990K QPS (99% of 1M total)
- **Write QPS:** 10K QPS (1% of 1M total)
- **Graph traversal queries:** 50K QPS

### Performance:
- **Get friends list:** < 100ms (p95)
- **Mutual friends:** < 200ms (p95)
- **Friend suggestions:** < 500ms (p95)
- **Check friendship:** < 10ms (p95)
- **Graph traversal (2-3 degrees):** < 1 second (p95)

### Availability:
- **Service availability:** 99.99%
- **Data consistency:** Strong consistency for critical operations (add/remove friend)

### Storage:
- **Raw edge data:** 600B edges × 16 bytes = 9.6 TB
- **Bidirectional index:** 9.6 TB × 2 = 19.2 TB
- **Metadata:** ~2 TB
- **Total:** ~22 TB

## 4. Back-of-envelope Calculations

### Storage Calculations:

```
Users: 3 billion
Average connections per user: 200
Total edges: 3B × 200 = 600 billion

Edge storage:
- user_id: 8 bytes (BIGINT)
- friend_id: 8 bytes (BIGINT)
- created_at: 8 bytes (TIMESTAMP)
- relationship_type: 1 byte (TINYINT)
Total per edge: 25 bytes

Total storage: 600B × 25 bytes = 15 TB

Bidirectional indexing (store both directions):
15 TB × 2 = 30 TB

With replication (3x):
30 TB × 3 = 90 TB total
```

### QPS Calculations:

```
Total QPS: 1M
Read QPS: 990K (99%)
Write QPS: 10K (1%)

Query distribution:
- Get friends: 500K QPS (50%)
- Check friendship: 300K QPS (30%)
- Get mutual friends: 100K QPS (10%)
- Get followers: 50K QPS (5%)
- Others: 40K QPS (5%)
```

### Cache Requirements:

```
Hot users: 10M users (power users, celebrities)
Each user's friend list: 200 friends × 8 bytes = 1.6 KB
Total cache: 10M × 1.6 KB = 16 GB

Mutual friends cache (pre-computed for common pairs):
Cache size: 50 GB

Total cache: ~70 GB (fits in single Redis instance)
```

## 5. High-Level Architecture

```
                [Client Applications]
                        |
                        v
                [Load Balancer]
                        |
                        v
                [API Gateway]
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
[Relationship    [Friendship      [Suggestion
  Service]         Query Service]   Service]
        |               |               |
        v               v               v
        +-------[Cache Layer - Redis]-------+
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
[PostgreSQL       [Graph DB        [Graph Index
 Sharded]          (Optional)]      In-Memory]
   (Main            (Complex          (Fast
   Storage)         Queries)          Traversal)


[Async Processing]
        |
        v
[Friend Suggestion Worker]
        |
        v
[ML Model Training (Batch)]
```

## 6. Database Design

### PostgreSQL Schema (Sharded)

```sql
-- Adjacency List: Following (Outgoing Edges)
-- Sharded by user_id
CREATE TABLE following (
    user_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    relationship_type VARCHAR(20) DEFAULT 'friend',
        -- 'friend', 'follow', 'close_friend', 'family', 'blocked'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, followee_id)
);

CREATE INDEX idx_following_user ON following(user_id);
CREATE INDEX idx_following_type ON following(user_id, relationship_type);

-- Adjacency List: Followers (Incoming Edges)
-- Sharded by followee_id (user being followed)
CREATE TABLE followers (
    followee_id BIGINT NOT NULL,
    follower_id BIGINT NOT NULL,
    relationship_type VARCHAR(20) DEFAULT 'friend',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (followee_id, follower_id)
);

CREATE INDEX idx_followers_followee ON followers(followee_id);
CREATE INDEX idx_followers_type ON followers(followee_id, relationship_type);

-- Why two tables?
-- following table: Fast "Who does Alice follow?" queries
-- followers table: Fast "Who follows Alice?" queries
-- Trade space for query speed

-- Friend Requests (Pending Relationships)
CREATE TABLE friend_requests (
    request_id BIGSERIAL PRIMARY KEY,
    requester_id BIGINT NOT NULL,
    requestee_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
        -- 'pending', 'accepted', 'rejected', 'ignored'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (requester_id, requestee_id)
);

CREATE INDEX idx_friend_requests_requestee ON friend_requests(requestee_id, status);

-- User metadata (denormalized counts)
CREATE TABLE user_graph_stats (
    user_id BIGINT PRIMARY KEY,
    friends_count INT DEFAULT 0,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    pending_requests_count INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blocked users
CREATE TABLE blocked_users (
    user_id BIGINT NOT NULL,
    blocked_user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, blocked_user_id)
);
```

### Redis Cache Structures

```
# Friend list cache (Set)
Key: friends:{user_id}
Type: Set
Members: friend_user_ids
TTL: 1 hour

# Follower list cache
Key: followers:{user_id}
Type: Set
Members: follower_user_ids
TTL: 1 hour

# Friendship check cache
Key: friendship:{user_id1}:{user_id2}
Type: String ("1" or "0")
TTL: 30 minutes

# Mutual friends cache
Key: mutual:{user_id1}:{user_id2}
Type: Set
Members: mutual_friend_ids
TTL: 1 hour

# Friend count cache
Key: count:friends:{user_id}
Type: String (integer)
TTL: 1 hour

# Friend suggestions cache
Key: suggestions:{user_id}
Type: Sorted Set (score = relevance)
Members: suggested_user_ids
TTL: 24 hours
```

### Graph Database (Optional - Neo4j)

```cypher
// For complex graph queries only
// Main storage still in PostgreSQL

// Create user node
CREATE (u:User {user_id: 123, name: "Alice"})

// Create friendship relationship
MATCH (u1:User {user_id: 123}), (u2:User {user_id: 456})
CREATE (u1)-[:FRIENDS_WITH {created_at: timestamp()}]->(u2)

// Find mutual friends
MATCH (alice:User {user_id: 123})-[:FRIENDS_WITH]-(mutual)-[:FRIENDS_WITH]-(bob:User {user_id: 456})
RETURN mutual

// Find shortest path
MATCH path = shortestPath(
  (alice:User {user_id: 123})-[:FRIENDS_WITH*]-(bob:User {user_id: 456})
)
RETURN length(path)

// Find friends of friends
MATCH (alice:User {user_id: 123})-[:FRIENDS_WITH]-()-[:FRIENDS_WITH]-(fof)
WHERE fof.user_id != 123
RETURN DISTINCT fof
```

## 7. Core Components

### A. Relationship Service

```python
class RelationshipService:
    """
    Handle CRUD operations for relationships
    """

    def add_friend(self, user_id, friend_id):
        """
        Add bidirectional friendship
        """

        # Validation
        if user_id == friend_id:
            raise ValueError("Cannot friend yourself")

        if self.is_blocked(user_id, friend_id):
            raise ValueError("Cannot friend blocked user")

        # Check if already friends
        if self.are_friends(user_id, friend_id):
            return  # Idempotent

        # For bidirectional friendship, insert both directions
        # Transaction for consistency
        with db.transaction():
            # Insert into following table (user_id -> friend_id)
            db.execute("""
                INSERT INTO following (user_id, followee_id, relationship_type)
                VALUES (?, ?, 'friend')
                ON CONFLICT DO NOTHING
            """, user_id, friend_id)

            # Insert reverse (friend_id -> user_id)
            db.execute("""
                INSERT INTO following (user_id, followee_id, relationship_type)
                VALUES (?, ?, 'friend')
                ON CONFLICT DO NOTHING
            """, friend_id, user_id)

            # Insert into followers table (user_id <- friend_id)
            db.execute("""
                INSERT INTO followers (followee_id, follower_id, relationship_type)
                VALUES (?, ?, 'friend')
                ON CONFLICT DO NOTHING
            """, user_id, friend_id)

            # Insert reverse
            db.execute("""
                INSERT INTO followers (followee_id, follower_id, relationship_type)
                VALUES (?, ?, 'friend')
                ON CONFLICT DO NOTHING
            """, friend_id, user_id)

            # Update counts
            db.execute("""
                UPDATE user_graph_stats
                SET friends_count = friends_count + 1
                WHERE user_id IN (?, ?)
            """, user_id, friend_id)

        # Invalidate caches
        self.invalidate_friend_cache(user_id)
        self.invalidate_friend_cache(friend_id)

        # Publish event for downstream processing
        kafka.publish("friendship_created", {
            "user_id": user_id,
            "friend_id": friend_id,
            "timestamp": time.time()
        })

    def remove_friend(self, user_id, friend_id):
        """
        Remove bidirectional friendship
        """

        with db.transaction():
            # Delete both directions
            db.execute("""
                DELETE FROM following
                WHERE (user_id = ? AND followee_id = ?)
                   OR (user_id = ? AND followee_id = ?)
            """, user_id, friend_id, friend_id, user_id)

            db.execute("""
                DELETE FROM followers
                WHERE (followee_id = ? AND follower_id = ?)
                   OR (followee_id = ? AND follower_id = ?)
            """, user_id, friend_id, friend_id, user_id)

            # Update counts
            db.execute("""
                UPDATE user_graph_stats
                SET friends_count = friends_count - 1
                WHERE user_id IN (?, ?)
            """, user_id, friend_id)

        # Invalidate caches
        self.invalidate_friend_cache(user_id)
        self.invalidate_friend_cache(friend_id)

        kafka.publish("friendship_removed", {
            "user_id": user_id,
            "friend_id": friend_id
        })

    def follow_user(self, follower_id, followee_id):
        """
        Unidirectional follow (like Twitter)
        """

        with db.transaction():
            # Insert into following
            db.execute("""
                INSERT INTO following (user_id, followee_id, relationship_type)
                VALUES (?, ?, 'follow')
                ON CONFLICT DO NOTHING
            """, follower_id, followee_id)

            # Insert into followers
            db.execute("""
                INSERT INTO followers (followee_id, follower_id, relationship_type)
                VALUES (?, ?, 'follow')
                ON CONFLICT DO NOTHING
            """, followee_id, follower_id)

            # Update counts
            db.execute("""
                UPDATE user_graph_stats
                SET following_count = following_count + 1
                WHERE user_id = ?
            """, follower_id)

            db.execute("""
                UPDATE user_graph_stats
                SET followers_count = followers_count + 1
                WHERE user_id = ?
            """, followee_id)

        self.invalidate_following_cache(follower_id)
        self.invalidate_followers_cache(followee_id)

    def block_user(self, user_id, blocked_user_id):
        """
        Block a user (removes existing friendship if any)
        """

        with db.transaction():
            # Remove any existing relationship
            self.remove_friend(user_id, blocked_user_id)

            # Add to blocked list
            db.execute("""
                INSERT INTO blocked_users (user_id, blocked_user_id)
                VALUES (?, ?)
                ON CONFLICT DO NOTHING
            """, user_id, blocked_user_id)

        # Cache block status
        redis.setex(
            f"blocked:{user_id}:{blocked_user_id}",
            3600,
            "1"
        )
```

### B. Query Service

```python
class FriendshipQueryService:
    """
    Handle read queries on social graph
    """

    def get_friends(self, user_id, limit=5000):
        """
        Get all friends of a user
        """

        # Check cache
        cache_key = f"friends:{user_id}"
        cached = redis.smembers(cache_key)

        if cached:
            # Cache hit
            return list(cached)

        # Cache miss - query database
        friends = db.query("""
            SELECT followee_id
            FROM following
            WHERE user_id = ?
              AND relationship_type IN ('friend', 'close_friend', 'family')
            LIMIT ?
        """, user_id, limit)

        friend_ids = [f.followee_id for f in friends]

        # Cache for future
        if friend_ids:
            redis.sadd(cache_key, *friend_ids)
            redis.expire(cache_key, 3600)

        return friend_ids

    def get_followers(self, user_id, limit=5000):
        """
        Get all followers of a user
        """

        cache_key = f"followers:{user_id}"
        cached = redis.smembers(cache_key)

        if cached:
            return list(cached)

        followers = db.query("""
            SELECT follower_id
            FROM followers
            WHERE followee_id = ?
            LIMIT ?
        """, user_id, limit)

        follower_ids = [f.follower_id for f in followers]

        if follower_ids:
            redis.sadd(cache_key, *follower_ids)
            redis.expire(cache_key, 3600)

        return follower_ids

    def are_friends(self, user_id1, user_id2):
        """
        Check if two users are friends (bidirectional check)
        """

        # Check cache
        cache_key = f"friendship:{min(user_id1, user_id2)}:{max(user_id1, user_id2)}"
        cached = redis.get(cache_key)

        if cached is not None:
            return cached == "1"

        # Query database
        result = db.query("""
            SELECT 1
            FROM following
            WHERE user_id = ? AND followee_id = ?
            LIMIT 1
        """, user_id1, user_id2)

        is_friend = len(result) > 0

        # Cache result
        redis.setex(cache_key, 1800, "1" if is_friend else "0")

        return is_friend

    def get_mutual_friends(self, user_id1, user_id2):
        """
        Get mutual friends between two users
        Optimized with set intersection
        """

        # Check cache
        cache_key = f"mutual:{min(user_id1, user_id2)}:{max(user_id1, user_id2)}"
        cached = redis.smembers(cache_key)

        if cached:
            return list(cached)

        # Get friend lists for both users
        friends1 = set(self.get_friends(user_id1))
        friends2 = set(self.get_friends(user_id2))

        # Set intersection (very fast in Python)
        mutual = friends1 & friends2

        # Cache result
        if mutual:
            redis.sadd(cache_key, *mutual)
            redis.expire(cache_key, 3600)

        return list(mutual)

    def get_mutual_friends_count(self, user_id1, user_id2):
        """
        Just get count (faster than getting full list)
        """

        # Try cache first
        mutual = self.get_mutual_friends(user_id1, user_id2)
        return len(mutual)

    def get_friend_count(self, user_id):
        """
        Get total friend count (from denormalized count)
        """

        # Check cache
        cache_key = f"count:friends:{user_id}"
        cached = redis.get(cache_key)

        if cached:
            return int(cached)

        # Query from denormalized table
        result = db.query("""
            SELECT friends_count
            FROM user_graph_stats
            WHERE user_id = ?
        """, user_id)

        count = result[0].friends_count if result else 0

        # Cache
        redis.setex(cache_key, 3600, str(count))

        return count
```

### C. Graph Traversal Service

```python
class GraphTraversalService:
    """
    Handle graph traversal operations
    BFS, shortest path, etc.
    """

    def get_friends_of_friends(self, user_id, max_results=100):
        """
        Get 2nd degree connections (friends of friends)
        Who are not already friends
        """

        # Get direct friends (1st degree)
        friends = self.get_friends(user_id)

        # Get friends of each friend (2nd degree)
        fof_set = set()

        for friend_id in friends:
            # Get this friend's friends
            friends_of_friend = self.get_friends(friend_id)
            fof_set.update(friends_of_friend)

        # Remove self and direct friends
        fof_set.discard(user_id)
        fof_set -= set(friends)

        # Limit results
        return list(fof_set)[:max_results]

    def find_shortest_path(self, start_user_id, end_user_id, max_depth=6):
        """
        Find shortest path between two users using BFS
        Returns list of user IDs in path
        """

        # If same user
        if start_user_id == end_user_id:
            return [start_user_id]

        # If directly connected
        if self.are_friends(start_user_id, end_user_id):
            return [start_user_id, end_user_id]

        # BFS
        queue = deque([(start_user_id, [start_user_id])])
        visited = {start_user_id}
        depth = 0

        while queue and depth < max_depth:
            # Process current level
            level_size = len(queue)

            for _ in range(level_size):
                current_user, path = queue.popleft()

                # Get friends of current user
                friends = self.get_friends(current_user)

                for friend_id in friends:
                    if friend_id == end_user_id:
                        # Found target
                        return path + [friend_id]

                    if friend_id not in visited:
                        visited.add(friend_id)
                        queue.append((friend_id, path + [friend_id]))

            depth += 1

        # No path found within max_depth
        return None

    def calculate_degrees_of_separation(self, user_id1, user_id2):
        """
        Calculate degrees of separation (6 degrees concept)
        """

        path = self.find_shortest_path(user_id1, user_id2)

        if path:
            # Degrees = path length - 1
            return len(path) - 1
        else:
            return None  # Not connected

    def find_all_connections_within_n_degrees(self, user_id, n=2):
        """
        Find all users within N degrees of separation
        Use BFS with depth limit
        """

        connections = set()
        queue = deque([(user_id, 0)])
        visited = {user_id}

        while queue:
            current_user, depth = queue.popleft()

            if depth >= n:
                continue

            friends = self.get_friends(current_user)

            for friend_id in friends:
                if friend_id not in visited:
                    visited.add(friend_id)
                    connections.add(friend_id)
                    queue.append((friend_id, depth + 1))

        return list(connections)
```

### D. Friend Suggestion Service

```python
class FriendSuggestionService:
    """
    Generate friend suggestions using multiple signals
    """

    def get_friend_suggestions(self, user_id, limit=10):
        """
        Get personalized friend suggestions
        """

        # Check cache
        cache_key = f"suggestions:{user_id}"
        cached = redis.zrevrange(cache_key, 0, limit - 1)

        if cached:
            return cached

        # Generate suggestions
        suggestions = self.generate_suggestions(user_id)

        # Rank suggestions
        ranked = self.rank_suggestions(user_id, suggestions)

        # Cache results (24 hours)
        if ranked:
            # Store as sorted set
            score_dict = {user_id: score for user_id, score in ranked}
            redis.zadd(cache_key, score_dict)
            redis.expire(cache_key, 86400)

        return [user_id for user_id, score in ranked[:limit]]

    def generate_suggestions(self, user_id):
        """
        Generate candidate suggestions from multiple sources
        """

        candidates = set()

        # Source 1: Mutual friends (strongest signal)
        mutual_candidates = self.get_mutual_friend_candidates(user_id)
        candidates.update(mutual_candidates)

        # Source 2: Friends of friends
        fof = self.get_friends_of_friends(user_id, max_results=500)
        candidates.update(fof)

        # Source 3: Same school/workplace (if available)
        # same_network = self.get_same_network_users(user_id)
        # candidates.update(same_network)

        # Source 4: Similar interests (if available)
        # similar = self.get_similar_interest_users(user_id)
        # candidates.update(similar)

        # Filter out existing friends and self
        friends = set(self.get_friends(user_id))
        candidates.discard(user_id)
        candidates -= friends

        # Filter out blocked users
        blocked = set(self.get_blocked_users(user_id))
        candidates -= blocked

        return list(candidates)

    def rank_suggestions(self, user_id, candidates):
        """
        Rank suggestion candidates by relevance
        """

        scored = []

        for candidate_id in candidates:
            score = self.calculate_suggestion_score(user_id, candidate_id)
            scored.append((candidate_id, score))

        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored

    def calculate_suggestion_score(self, user_id, candidate_id):
        """
        Calculate relevance score for a suggestion
        Multiple factors considered
        """

        score = 0.0

        # Factor 1: Mutual friends (strongest signal)
        mutual_count = self.get_mutual_friends_count(user_id, candidate_id)
        score += mutual_count * 10  # High weight

        # Factor 2: Closeness of mutual friends
        # If mutual friends are close friends, higher score
        mutual_friends = self.get_mutual_friends(user_id, candidate_id)
        for friend_id in mutual_friends[:10]:  # Check top 10
            if self.is_close_friend(user_id, friend_id):
                score += 5

        # Factor 3: Network proximity (degrees of separation)
        degrees = self.calculate_degrees_of_separation(user_id, candidate_id)
        if degrees == 2:
            score += 20
        elif degrees == 3:
            score += 10
        elif degrees == 4:
            score += 5

        # Factor 4: Profile completeness
        # More complete profiles are better suggestions
        profile_score = self.get_profile_completeness(candidate_id)
        score += profile_score * 2

        # Factor 5: Recent activity
        # Active users are better suggestions
        if self.is_recently_active(candidate_id, days=7):
            score += 10

        # Factor 6: Common groups/pages (if available)
        # common_groups = self.get_common_groups(user_id, candidate_id)
        # score += len(common_groups) * 3

        return score

    def get_mutual_friend_candidates(self, user_id):
        """
        Get candidates who have mutual friends
        Optimized query
        """

        # Get all friends
        friends = self.get_friends(user_id)

        # Count how many times each candidate appears
        # as friend of my friends
        candidate_counts = {}

        for friend_id in friends:
            # Get this friend's friends
            fof = self.get_friends(friend_id)

            for candidate_id in fof:
                if candidate_id != user_id:
                    candidate_counts[candidate_id] = \
                        candidate_counts.get(candidate_id, 0) + 1

        # Return candidates with at least 2 mutual friends
        return [
            candidate_id
            for candidate_id, count in candidate_counts.items()
            if count >= 2
        ]
```

## 8. Database Sharding Strategy

```python
class GraphShardingStrategy:
    """
    Shard social graph by user_id using consistent hashing
    """

    def __init__(self, num_shards=100):
        self.num_shards = num_shards

    def get_shard_for_user(self, user_id):
        """
        Determine which shard stores data for user_id
        """

        # Simple modulo sharding
        shard_id = user_id % self.num_shards
        return shard_id

    def get_shard_for_following(self, user_id):
        """
        following table sharded by user_id
        "Who does user_id follow?"
        """

        return self.get_shard_for_user(user_id)

    def get_shard_for_followers(self, user_id):
        """
        followers table sharded by followee_id
        "Who follows user_id?"
        """

        return self.get_shard_for_user(user_id)

    def get_friends_cross_shard(self, user_id):
        """
        Get friends list (may require cross-shard query for followers)
        """

        # Primary shard (where user's following data is)
        primary_shard = self.get_shard_for_user(user_id)

        # Query following table on primary shard
        friends_following = db[primary_shard].query("""
            SELECT followee_id
            FROM following
            WHERE user_id = ?
        """, user_id)

        # For bidirectional check, also query followers table
        # (may be on different shard)
        followers_shard = self.get_shard_for_followers(user_id)
        friends_followers = db[followers_shard].query("""
            SELECT follower_id
            FROM followers
            WHERE followee_id = ?
        """, user_id)

        # Intersect to get bidirectional friends
        following_set = set(f.followee_id for f in friends_following)
        followers_set = set(f.follower_id for f in friends_followers)

        bidirectional_friends = following_set & followers_set

        return list(bidirectional_friends)
```

## 9. Privacy and Visibility

```python
class PrivacyService:
    """
    Handle privacy rules for social graph
    """

    def can_see_friend_list(self, viewer_id, profile_user_id):
        """
        Check if viewer can see profile_user's friend list
        """

        # User can always see their own friend list
        if viewer_id == profile_user_id:
            return True

        # Check privacy setting
        privacy = self.get_privacy_setting(
            profile_user_id, 'friend_list_visibility')

        if privacy == 'public':
            return True
        elif privacy == 'friends':
            # Only friends can see
            return self.are_friends(viewer_id, profile_user_id)
        elif privacy == 'friends_of_friends':
            # Friends and friends of friends
            if self.are_friends(viewer_id, profile_user_id):
                return True
            # Check if friends of friends
            mutual = self.get_mutual_friends_count(viewer_id, profile_user_id)
            return mutual > 0
        else:  # 'only_me'
            return False

    def get_visible_friends(self, viewer_id, profile_user_id):
        """
        Get friend list that viewer is allowed to see
        """

        # Check permission
        if not self.can_see_friend_list(viewer_id, profile_user_id):
            raise PermissionDenied("Cannot view friend list")

        # Get friend list
        friends = self.get_friends(profile_user_id)

        # Filter out friends who have blocked viewer
        visible = [
            friend_id
            for friend_id in friends
            if not self.has_blocked(friend_id, viewer_id)
        ]

        return visible
```

## 10. Trade-offs

### 1. Two Tables (following + followers) vs. One Table

**Decision: Two Tables**

**One Table:**
- Less storage
- Simpler schema
- Need index on both user_id and followee_id

**Two Tables:**
- 2x storage
- Faster queries (optimized for each direction)
- No need for complex indexes

At Facebook scale, query speed > storage cost

### 2. Graph Database vs. Relational Database

**Decision: Hybrid**

**Relational (PostgreSQL):**
- Mature, proven at scale
- Easy to shard
- Strong consistency
- Main storage

**Graph DB (Neo4j):**
- Natural for graph queries
- Excellent for complex traversals
- Used only for specific queries
- Optional, not critical path

### 3. Real-time Updates vs. Eventual Consistency

**Decision: Strong consistency for writes, eventual for reads**

Friend add/remove: Strong consistency
Friend counts: Eventual (denormalized)
Suggestions: Eventual (cached for 24h)

### 4. Pre-compute Suggestions vs. On-demand

**Decision: Pre-compute for active users**

Batch job runs daily to pre-compute suggestions
Cache for 24 hours
On-demand for first-time users

## 11. Optimizations

### 1. Denormalized Counts
Store friend_count, follower_count in user table for fast access

### 2. Bloom Filters
Use bloom filter to quickly check "definitely not friends"

### 3. Graph Index in Memory
Load hot portion of graph (10M users) into memory for fast traversal

### 4. Batch Processing
Process friend requests in batches to reduce DB load

## 12. Follow-up Questions

**Q1: How to handle celebrity users with 100M followers?**
A: Shard followers across multiple shards, paginate results, cache aggressively

**Q2: How to detect fake accounts and spam friend requests?**
A: ML model trained on patterns, rate limiting, CAPTCHA, phone verification

**Q3: How to suggest friends across platforms (WhatsApp + Facebook)?**
A: Unified identity service, phone number matching, contact import

**Q4: How to handle GDPR data deletion?**
A: Remove all edges involving user, anonymize in analytics, 30-day grace period

**Q5: How to scale to 10 billion users?**
A: More shards (1000+), graph partitioning algorithms, distributed graph processing (GraphX)

---

**Estimated Interview Time:** 75-90 minutes

**Difficulty:** Hard (requires deep understanding of graph algorithms and distributed systems)
