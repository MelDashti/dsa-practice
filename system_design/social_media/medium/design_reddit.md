# Design Reddit

## 1. Problem Statement & Scope

Design a community-driven content aggregation and discussion platform where users can submit content, vote on posts and comments, participate in topical communities (subreddits), and engage in threaded discussions.

### In Scope:
- User registration and authentication
- Subreddit creation and management
- Post creation (text, link, image, video)
- Upvote/downvote system for posts and comments
- Nested comment threads
- Ranking algorithms (Hot, Top, New, Controversial)
- User karma system
- Moderation tools
- Search (posts, subreddits, users)
- Awards/coins system
- User profiles and post history

### Out of Scope:
- Reddit Live
- Reddit Talk (audio spaces)
- Reddit Premium details
- Advertising platform
- Chat messaging
- Cryptocurrency integrations

### Scale:
- 50 million daily active users (DAU)
- 100 million total users
- 2 million posts per day
- 20 million comments per day
- 500 million votes per day
- 100,000 active subreddits
- Read:Write ratio: 100:1

## 2. Functional Requirements

### High Priority (P0):

**FR1: User Management**
- Register with email/username
- Login and authentication
- User profiles with karma score
- User preferences and settings
- Follow users

**FR2: Subreddit Management**
- Create subreddit
- Subscribe/unsubscribe to subreddits
- Subreddit rules and description
- Moderator management
- Public/Private/Restricted subreddits

**FR3: Post Operations**
- Create text post
- Create link post
- Create image/video post
- Create poll
- Edit own posts
- Delete own posts
- Cross-post to other subreddits

**FR4: Voting System**
- Upvote/downvote posts
- Upvote/downvote comments
- Vote score calculation
- Prevent double voting

**FR5: Comment System**
- Add comment to post
- Reply to comment (nested threading)
- Edit own comments
- Delete own comments
- Comment sorting (Best, Top, New, Controversial)

**FR6: Feed/Ranking**
- Home feed (subscribed subreddits)
- Popular feed (trending across Reddit)
- Subreddit feed with multiple sort options:
  - Hot (time-weighted engagement)
  - Top (all-time, year, month, week, day, hour)
  - New (chronological)
  - Controversial (balanced votes)
  - Rising (early trending)

**FR7: Karma System**
- Post karma (upvotes - downvotes on posts)
- Comment karma (upvotes - downvotes on comments)
- Display total karma on profile

### Medium Priority (P1):

**FR8: Moderation**
- Remove posts/comments
- Ban users from subreddit
- Create AutoModerator rules
- Moderation queue
- Reports and flags

**FR9: Search**
- Search posts by title/content
- Search subreddits
- Search users
- Filter by subreddit, time, sort

**FR10: Awards**
- Give awards to posts/comments
- Award types (Gold, Silver, Platinum, etc.)
- Award display on posts

## 3. Non-Functional Requirements (Scale, Performance, Availability)

### Scale Requirements:
- **Daily Active Users:** 50 million
- **Total Users:** 100 million
- **Posts per day:** 2 million
- **Comments per day:** 20 million
- **Votes per day:** 500 million
- **Active subreddits:** 100,000
- **Peak concurrent users:** 5 million

### Performance Requirements:
- **Post creation:** < 200ms (p95)
- **Feed load:** < 500ms (p95)
- **Comment tree load:** < 300ms (p95)
- **Vote registration:** < 100ms (p95)
- **Search response:** < 500ms (p95)
- **Hot ranking update:** Every 30 seconds

### Availability:
- **Service availability:** 99.9%
- **Data durability:** 99.999999999%

### Consistency:
- **Votes:** Eventual consistency (acceptable delay: 5-10 seconds)
- **Comments:** Strong consistency (appear immediately)
- **Rankings:** Eventual consistency (update every 30-60 seconds)
- **Karma:** Eventual consistency

## 4. Back-of-envelope Calculations

### Traffic Estimates:

**Posts:**
- Posts per day: 2M
- Posts per second: 2M ÷ 86,400 = ~23 posts/sec
- Peak (5x): ~115 posts/sec

**Comments:**
- Comments per day: 20M
- Comments per second: ~231 comments/sec
- Peak (5x): ~1,155 comments/sec

**Votes:**
- Votes per day: 500M
- Votes per second: ~5,787 votes/sec
- Peak (5x): ~28,935 votes/sec

**Page Views:**
- DAU: 50M
- Average page views per user: 30
- Total: 1.5B page views/day
- Per second: ~17,361 requests/sec
- With caching (90% hit rate): ~1,736 requests/sec to origin

### Storage Calculations:

**Users:**
- Total users: 100M
- Data per user: 2 KB
- Total: 100M × 2 KB = 200 GB

**Subreddits:**
- Active subreddits: 100K
- Data per subreddit: 10 KB
- Total: 100K × 10 KB = 1 GB

**Posts:**
- Size per post: 5 KB (text, metadata)
- Daily: 2M × 5 KB = 10 GB/day
- Yearly: 10 GB × 365 = 3.65 TB/year

**Media (images/videos in posts):**
- 40% of posts have media
- Average media size: 2 MB
- Daily: 2M × 0.4 × 2 MB = 1.6 TB/day
- Yearly: 1.6 TB × 365 = 584 TB/year

**Comments:**
- Size per comment: 1 KB
- Daily: 20M × 1 KB = 20 GB/day
- Yearly: 20 GB × 365 = 7.3 TB/year

**Votes:**
- Size per vote: 20 bytes (user_id, post_id, vote_type, timestamp)
- Daily: 500M × 20 bytes = 10 GB/day
- Yearly: 10 GB × 365 = 3.65 TB/year

**Total Storage (Year 1):** ~600 TB (mostly media)

### Bandwidth:

**Incoming:**
- Posts + comments: 30 GB/day = 347 KB/s
- Media: 1.6 TB/day = 18.5 MB/s
- Votes: 10 GB/day = 115 KB/s
- Peak (5x): ~93 MB/s

**Outgoing:**
- Assume each page view loads 10 posts with thumbnails
- Average page size: 500 KB
- 1.5B page views × 500 KB = 750 TB/day
- Per second: 750 TB ÷ 86,400 = ~8.6 GB/s
- CDN will serve most traffic

### Cache Requirements:

**Hot Posts:**
- Top 10K posts accessed frequently
- Each post: 5 KB + comments summary: 10 KB
- Total: 10K × 15 KB = 150 MB

**Hot Subreddits:**
- Top 1K subreddits
- Each: 10 KB + top posts list: 50 KB
- Total: 1K × 60 KB = 60 MB

**User Sessions:**
- 5M concurrent users
- Session data: 2 KB
- Total: 5M × 2 KB = 10 GB

**Vote Counters:**
- Hot posts: 10K × 100 bytes = 1 MB
- Recent posts: 100K × 100 bytes = 10 MB

**Total Cache:** ~15 GB (easily fits in Redis)

## 5. High-Level Architecture Diagram Description

```
                        [Clients - Web, Mobile Apps]
                                    |
                                    v
                        [Global Load Balancer]
                                    |
                        [API Gateway + Rate Limiter]
                                    |
        +---------------+-----------+-----------+---------------+
        |               |           |           |               |
        v               v           v           v               v
    [Post         [Comment    [Vote       [Feed        [Search
     Service]      Service]    Service]    Service]     Service]
        |               |           |           |               |
        +---------------|-----------|-----------|---------------+
                        |
                        v
            [Event Bus - Kafka/RabbitMQ]
                        |
        +---------------+-----------+---------------+
        |               |           |               |
        v               v           v               v
    [Ranking       [Karma      [Moderation  [Notification
     Worker]        Worker]     Service]     Service]


        |               |           |               |
        v               v           v               v
    [Redis Cluster]  [PostgreSQL]  [Cassandra]  [Elasticsearch]
    (Rankings,       (Users,       (Votes,      (Full-text
     Hot posts,      Posts,        Comments)     search)
     Counters)       Subreddits)


        v
    [S3 Storage] ---------> [CloudFront CDN]
    (Media, Images)         (Media Delivery)


[Async Workers]
    |
    v
[Ranking Computation] (Calculate Hot, Top, etc.)
[Karma Aggregation] (Update user karma)
[Thumbnail Generation]
```

### Key Components:

1. **API Gateway:** Authentication, rate limiting, routing
2. **Post Service:** Create, edit, delete posts
3. **Comment Service:** Manage comment threads
4. **Vote Service:** Handle upvotes/downvotes
5. **Feed Service:** Generate home and subreddit feeds
6. **Ranking Workers:** Calculate Hot, Top, Rising scores
7. **Karma Workers:** Aggregate user karma
8. **Search Service:** Full-text search
9. **Moderation Service:** Mod tools and AutoMod
10. **PostgreSQL:** Primary datastore (users, posts, subreddits)
11. **Cassandra:** High-write data (votes, comments)
12. **Redis:** Cache and real-time rankings
13. **Elasticsearch:** Search index
14. **S3 + CDN:** Media storage and delivery

## 6. API Design (RESTful endpoints)

### Post APIs

```
POST /api/v1/posts
Request:
{
  "subreddit": "r/programming",
  "post_type": "text",  // or "link", "image", "video", "poll"
  "title": "How to design scalable systems",
  "text": "Long text content...",  // for text posts
  "url": "https://...",  // for link posts
  "media_id": "media_123",  // for image/video posts
  "flair": "Discussion",
  "nsfw": false,
  "spoiler": false,
  "oc": true  // original content
}
Response: 201 Created
{
  "post_id": "abc123",
  "subreddit": "r/programming",
  "author": "username",
  "title": "...",
  "score": 1,  // starts at 1 (self-upvote)
  "created_at": "...",
  "permalink": "/r/programming/comments/abc123/..."
}

GET /api/v1/posts/{post_id}
Response:
{
  "post_id": "abc123",
  "subreddit": {
    "name": "programming",
    "subscribers": 5000000
  },
  "author": {
    "username": "john_doe",
    "karma": {"post": 12345, "comment": 67890}
  },
  "title": "...",
  "text": "...",
  "score": 1523,
  "upvote_ratio": 0.89,
  "num_comments": 247,
  "created_at": "...",
  "awards": [
    {"type": "gold", "count": 3},
    {"type": "silver", "count": 12}
  ],
  "flair": "Discussion",
  "user_vote": 1  // 1=upvoted, -1=downvoted, 0=none
}

PUT /api/v1/posts/{post_id}
Request:
{
  "text": "Updated content..."
}

DELETE /api/v1/posts/{post_id}
Response: 204 No Content

POST /api/v1/posts/{post_id}/crosspost
Request:
{
  "target_subreddit": "r/coding",
  "title": "Cross-posting this gem"
}
```

### Comment APIs

```
POST /api/v1/posts/{post_id}/comments
Request:
{
  "text": "Great post! Here's my take...",
  "parent_id": null  // null for top-level, comment_id for reply
}
Response: 201 Created
{
  "comment_id": "xyz789",
  "post_id": "abc123",
  "parent_id": null,
  "author": "jane_doe",
  "text": "...",
  "score": 1,
  "depth": 0,  // nesting level
  "created_at": "...",
  "user_vote": 1
}

GET /api/v1/posts/{post_id}/comments?sort=best&limit=200
Query Parameters:
- sort: best, top, new, controversial, old, qa
- limit: max comments to return
- depth: max nesting depth

Response:
{
  "comments": [
    {
      "comment_id": "xyz789",
      "author": "jane_doe",
      "text": "...",
      "score": 523,
      "replies": [
        {
          "comment_id": "xyz790",
          "author": "bob_smith",
          "text": "...",
          "score": 142,
          "replies": [...]
        }
      ],
      "depth": 0,
      "is_submitter": false,
      "is_moderator": false,
      "awards": [...]
    }
  ],
  "total_comments": 247,
  "sort": "best"
}

PUT /api/v1/comments/{comment_id}
Request:
{
  "text": "Edited comment..."
}

DELETE /api/v1/comments/{comment_id}
```

### Vote APIs

```
POST /api/v1/vote
Request:
{
  "target_type": "post",  // or "comment"
  "target_id": "abc123",
  "direction": 1  // 1=upvote, -1=downvote, 0=remove vote
}
Response: 200 OK
{
  "new_score": 1524,
  "user_vote": 1
}

# Votes are idempotent - can call multiple times
```

### Subreddit APIs

```
POST /api/v1/subreddits
Request:
{
  "name": "scalability",
  "title": "System Scalability",
  "description": "Discussion about scaling systems",
  "type": "public",  // or "private", "restricted"
  "nsfw": false
}
Response: 201 Created

GET /api/v1/subreddits/{subreddit_name}
Response:
{
  "name": "programming",
  "title": "Programming",
  "description": "...",
  "subscribers": 5000000,
  "active_users": 12500,
  "created_at": "...",
  "rules": [...],
  "moderators": [...],
  "user_is_subscriber": true,
  "user_is_moderator": false
}

POST /api/v1/subreddits/{subreddit_name}/subscribe
DELETE /api/v1/subreddits/{subreddit_name}/subscribe

GET /api/v1/subreddits/{subreddit_name}/posts?sort=hot&time=day&limit=25
Sort: hot, top, new, rising, controversial
Time (for top): hour, day, week, month, year, all

GET /api/v1/subreddits/search?q=python&limit=25
```

### Feed APIs

```
GET /api/v1/feed/home?sort=hot&limit=25&after={cursor}
# Home feed from subscribed subreddits

GET /api/v1/feed/popular?sort=hot&limit=25
# Popular posts across all Reddit

GET /api/v1/feed/all?sort=hot&limit=25
# All posts from all subreddits

GET /api/v1/subreddits/{subreddit}/feed?sort=hot&time=day&limit=25
# Feed for specific subreddit
```

### User APIs

```
GET /api/v1/users/{username}
Response:
{
  "username": "john_doe",
  "created_at": "...",
  "karma": {
    "post": 12345,
    "comment": 67890,
    "total": 80235
  },
  "is_gold": false,
  "is_mod": ["r/programming", "r/golang"]
}

GET /api/v1/users/{username}/posts?sort=new&limit=25
GET /api/v1/users/{username}/comments?sort=new&limit=25
GET /api/v1/users/{username}/upvoted
GET /api/v1/users/{username}/downvoted
GET /api/v1/users/{username}/saved
```

### Search APIs

```
GET /api/v1/search?q=machine+learning&type=post&sort=relevance&time=week
Query Parameters:
- q: search query
- type: post, subreddit, user
- sort: relevance, hot, top, new, comments
- time: hour, day, week, month, year, all
- subreddit: restrict to subreddit

Response:
{
  "results": [
    {
      "type": "post",
      "post": {...}
    }
  ],
  "total": 12450,
  "after": "cursor_token"
}
```

### Moderation APIs

```
POST /api/v1/subreddits/{subreddit}/moderators
Request:
{
  "username": "new_mod",
  "permissions": ["posts", "comments", "config"]
}

POST /api/v1/subreddits/{subreddit}/ban
Request:
{
  "username": "spammer",
  "duration": 30,  // days, null=permanent
  "reason": "Spam"
}

DELETE /api/v1/posts/{post_id}/remove
Request:
{
  "reason": "Spam"
}

GET /api/v1/subreddits/{subreddit}/modqueue
# Posts/comments flagged for review
```

## 7. Database Design (Schema, Indexes)

### PostgreSQL Schema

```sql
-- Users
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    post_karma INT DEFAULT 0,
    comment_karma INT DEFAULT 0,
    is_gold BOOLEAN DEFAULT FALSE,
    is_suspended BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_karma ON users((post_karma + comment_karma) DESC);

-- Subreddits
CREATE TABLE subreddits (
    subreddit_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(21) UNIQUE NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    sidebar TEXT,
    subreddit_type VARCHAR(20) DEFAULT 'public', -- public, private, restricted
    subscribers_count INT DEFAULT 0,
    is_nsfw BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_subreddits_name ON subreddits(name);
CREATE INDEX idx_subreddits_subscribers ON subreddits(subscribers_count DESC);

-- Posts
CREATE TABLE posts (
    post_id VARCHAR(10) PRIMARY KEY, -- base36 encoded ID
    subreddit_id BIGINT NOT NULL REFERENCES subreddits(subreddit_id),
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    post_type VARCHAR(10) NOT NULL, -- text, link, image, video, poll
    title VARCHAR(300) NOT NULL,
    text TEXT, -- for text posts
    url VARCHAR(2000), -- for link posts
    media_id VARCHAR(50), -- for image/video posts
    thumbnail_url VARCHAR(500),
    score INT DEFAULT 1, -- cached score (upvotes - downvotes)
    upvotes_count INT DEFAULT 1,
    downvotes_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    hot_score FLOAT DEFAULT 0, -- pre-calculated hot score
    controversy_score FLOAT DEFAULT 0,
    flair VARCHAR(64),
    is_nsfw BOOLEAN DEFAULT FALSE,
    is_spoiler BOOLEAN DEFAULT FALSE,
    is_oc BOOLEAN DEFAULT FALSE,
    is_locked BOOLEAN DEFAULT FALSE,
    is_removed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP
);

CREATE INDEX idx_posts_subreddit ON posts(subreddit_id, created_at DESC);
CREATE INDEX idx_posts_user ON posts(user_id, created_at DESC);
CREATE INDEX idx_posts_hot ON posts(subreddit_id, hot_score DESC) WHERE is_removed = FALSE;
CREATE INDEX idx_posts_score ON posts(subreddit_id, score DESC, created_at DESC);
CREATE INDEX idx_posts_created ON posts(created_at DESC);

-- Subscriptions
CREATE TABLE subscriptions (
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    subreddit_id BIGINT NOT NULL REFERENCES subreddits(subreddit_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, subreddit_id)
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_subreddit ON subscriptions(subreddit_id);

-- Moderators
CREATE TABLE moderators (
    subreddit_id BIGINT NOT NULL REFERENCES subreddits(subreddit_id),
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    permissions JSONB, -- ["posts", "comments", "config", "mail", "flair"]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (subreddit_id, user_id)
);

-- Saved Posts
CREATE TABLE saved_posts (
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    post_id VARCHAR(10) NOT NULL REFERENCES posts(post_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id)
);
```

### Cassandra Schema (for high-write data)

```cql
-- Votes (500M per day - needs high write throughput)
CREATE TABLE votes (
    target_type TEXT, -- 'post' or 'comment'
    target_id TEXT,
    user_id BIGINT,
    vote_direction INT, -- 1 (upvote), -1 (downvote)
    created_at TIMESTAMP,
    PRIMARY KEY ((target_type, target_id), user_id)
);

-- Vote counts (materialized view, updated async)
CREATE TABLE vote_counts (
    target_type TEXT,
    target_id TEXT,
    upvotes COUNTER,
    downvotes COUNTER,
    PRIMARY KEY ((target_type, target_id))
);

-- Comments (20M per day - high write throughput)
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    post_id TEXT,
    parent_id TEXT, -- null for top-level comments
    user_id BIGINT,
    text TEXT,
    score INT,
    is_edited BOOLEAN,
    is_removed BOOLEAN,
    depth INT, -- nesting level
    created_at TIMESTAMP,
    edited_at TIMESTAMP
);

CREATE INDEX ON comments(post_id);
CREATE INDEX ON comments(parent_id);
CREATE INDEX ON comments(user_id);

-- Comment tree (for efficient comment loading)
CREATE TABLE comment_tree (
    post_id TEXT,
    comment_id TEXT,
    parent_id TEXT,
    path TEXT, -- e.g., "root.abc.def.ghi" for traversal
    depth INT,
    created_at TIMESTAMP,
    score INT,
    PRIMARY KEY (post_id, path)
) WITH CLUSTERING ORDER BY (path ASC);

-- User comment history
CREATE TABLE user_comments (
    user_id BIGINT,
    comment_id TEXT,
    post_id TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at, comment_id)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

### Redis Cache

```
# Hot posts by subreddit (Sorted Set)
Key: subreddit:r/programming:hot
Type: Sorted Set
Score: hot_score
Members: post_ids
TTL: 5 minutes

# Post details cache
Key: post:{post_id}
Type: Hash
TTL: 30 minutes
Fields: {title, score, comment_count, author, ...}

# Comment tree cache
Key: comments:post:{post_id}:best
Type: List (JSON)
TTL: 10 minutes
Value: Nested comment tree structure

# Vote status cache (did user vote on this?)
Key: vote:{user_id}:{target_type}:{target_id}
Type: String
Value: "1" (upvote), "-1" (downvote), "0" (no vote)
TTL: 1 hour

# User subscriptions cache
Key: subscriptions:{user_id}
Type: Set
Members: subreddit_ids
TTL: 1 hour

# Leaderboard (top posts of the day)
Key: leaderboard:top:day
Type: Sorted Set
Score: score
Members: post_ids
TTL: 1 hour

# Rate limiting
Key: ratelimit:post:{user_id}
Type: String (counter)
TTL: 1 hour
Limit: 10 posts per hour

# Hot ranking computation (temporary scores)
Key: trending:post:{post_id}
Type: Hash
Fields: {upvotes, downvotes, age_hours, hot_score}
TTL: 1 hour
```

### Elasticsearch Index

```json
{
  "posts_index": {
    "settings": {
      "number_of_shards": 10,
      "analysis": {
        "analyzer": {
          "reddit_analyzer": {
            "tokenizer": "standard",
            "filter": ["lowercase", "stop", "snowball"]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "post_id": {"type": "keyword"},
        "subreddit": {"type": "keyword"},
        "author": {"type": "keyword"},
        "title": {
          "type": "text",
          "analyzer": "reddit_analyzer",
          "boost": 2.0
        },
        "text": {
          "type": "text",
          "analyzer": "reddit_analyzer"
        },
        "score": {"type": "integer"},
        "comment_count": {"type": "integer"},
        "created_at": {"type": "date"},
        "is_nsfw": {"type": "boolean"}
      }
    }
  },
  "comments_index": {
    "mappings": {
      "properties": {
        "comment_id": {"type": "keyword"},
        "post_id": {"type": "keyword"},
        "author": {"type": "keyword"},
        "text": {"type": "text", "analyzer": "reddit_analyzer"},
        "score": {"type": "integer"},
        "created_at": {"type": "date"}
      }
    }
  },
  "subreddits_index": {
    "mappings": {
      "properties": {
        "name": {"type": "keyword"},
        "title": {"type": "text"},
        "description": {"type": "text"},
        "subscribers_count": {"type": "integer"}
      }
    }
  }
}
```

## 8. Core Components

### A. Feed Generation Service

**Home Feed Generation:**

```python
class FeedService:
    def get_home_feed(self, user_id, sort='hot', limit=25, after=None):
        """Generate home feed from subscribed subreddits"""

        # Get user's subscriptions
        subscribed_subreddits = self.get_subscriptions(user_id)

        if sort == 'hot':
            return self.get_hot_feed(subscribed_subreddits, limit, after)
        elif sort == 'top':
            return self.get_top_feed(subscribed_subreddits, limit, after)
        elif sort == 'new':
            return self.get_new_feed(subscribed_subreddits, limit, after)

    def get_hot_feed(self, subreddit_ids, limit, after):
        """Get hot posts from multiple subreddits"""

        # Check cache first
        cache_key = f"feed:home:{','.join(subreddit_ids)}:hot"
        cached = redis.get(cache_key)
        if cached and not after:
            return json.loads(cached)[:limit]

        # Fetch hot posts from each subreddit
        all_posts = []

        for subreddit_id in subreddit_ids:
            # Get from Redis sorted set (pre-computed hot scores)
            post_ids = redis.zrevrange(
                f"subreddit:{subreddit_id}:hot",
                0, 10  # Top 10 from each
            )

            # Fetch post details
            posts = self.batch_get_posts(post_ids)
            all_posts.extend(posts)

        # Merge and sort by hot score
        all_posts.sort(key=lambda p: p.hot_score, reverse=True)

        # Paginate
        result = all_posts[:limit]

        # Cache for 2 minutes
        redis.setex(cache_key, 120, json.dumps(result))

        return result

    def get_subscriptions(self, user_id):
        """Get list of subreddits user is subscribed to"""

        # Check cache
        cache_key = f"subscriptions:{user_id}"
        cached = redis.smembers(cache_key)

        if cached:
            return list(cached)

        # Fetch from database
        subreddits = db.query("""
            SELECT subreddit_id
            FROM subscriptions
            WHERE user_id = ?
        """, user_id)

        # Cache for 1 hour
        if subreddits:
            redis.sadd(cache_key, *subreddits)
            redis.expire(cache_key, 3600)

        return subreddits
```

### B. Voting Service

**Vote Processing:**

```python
class VotingService:
    def vote(self, user_id, target_type, target_id, direction):
        """
        Process a vote (upvote/downvote)
        direction: 1 (upvote), -1 (downvote), 0 (remove vote)
        """

        # Check rate limit
        if not self.check_rate_limit(user_id):
            raise RateLimitError("Too many votes")

        # Get current vote
        current_vote = self.get_user_vote(user_id, target_type, target_id)

        # If same vote, no-op
        if current_vote == direction:
            return self.get_score(target_type, target_id)

        # Calculate delta
        if current_vote == 0:
            # No previous vote
            delta = direction
        elif direction == 0:
            # Removing vote
            delta = -current_vote
        else:
            # Changing vote (e.g., upvote to downvote)
            delta = direction - current_vote

        # Update vote in Cassandra
        cassandra.execute("""
            INSERT INTO votes (target_type, target_id, user_id, vote_direction, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, target_type, target_id, user_id, direction, now())

        # Update counters in Cassandra (using COUNTER type)
        if delta > 0:
            cassandra.execute("""
                UPDATE vote_counts
                SET upvotes = upvotes + ?
                WHERE target_type = ? AND target_id = ?
            """, abs(delta), target_type, target_id)
        else:
            cassandra.execute("""
                UPDATE vote_counts
                SET downvotes = downvotes + ?
                WHERE target_type = ? AND target_id = ?
            """, abs(delta), target_type, target_id)

        # Update Redis cache (immediate feedback)
        redis.hincrby(f"score:{target_type}:{target_id}", "upvotes", delta if delta > 0 else 0)
        redis.hincrby(f"score:{target_type}:{target_id}", "downvotes", -delta if delta < 0 else 0)

        # Cache user's vote
        redis.setex(
            f"vote:{user_id}:{target_type}:{target_id}",
            3600,
            str(direction)
        )

        # Publish event for ranking update
        kafka.publish("vote_cast", {
            "target_type": target_type,
            "target_id": target_id,
            "delta": delta,
            "timestamp": time.time()
        })

        # Async: Update PostgreSQL denormalized score
        self.update_score_async(target_type, target_id)

        # Return new score
        return self.get_score(target_type, target_id)

    def get_score(self, target_type, target_id):
        """Get current score (upvotes - downvotes)"""

        # Try Redis first
        cached = redis.hmget(
            f"score:{target_type}:{target_id}",
            "upvotes", "downvotes"
        )

        if all(cached):
            upvotes, downvotes = int(cached[0]), int(cached[1])
            return upvotes - downvotes

        # Fetch from Cassandra
        result = cassandra.execute("""
            SELECT upvotes, downvotes
            FROM vote_counts
            WHERE target_type = ? AND target_id = ?
        """, target_type, target_id)

        if result:
            upvotes, downvotes = result[0].upvotes, result[0].downvotes
            # Cache for future
            redis.hmset(f"score:{target_type}:{target_id}", {
                "upvotes": upvotes,
                "downvotes": downvotes
            })
            return upvotes - downvotes

        return 0
```

### C. Ranking Algorithms

**Hot Score (Reddit's famous hot algorithm):**

```python
import math
from datetime import datetime

def calculate_hot_score(upvotes, downvotes, created_at):
    """
    Reddit's hot ranking algorithm
    Based on: https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9
    """

    # Calculate score (upvotes - downvotes)
    score = upvotes - downvotes

    # Determine order of magnitude
    # Favors posts with more votes
    order = math.log10(max(abs(score), 1))

    # Determine sign (-1, 0, 1)
    sign = 1 if score > 0 else -1 if score < 0 else 0

    # Calculate time component (in seconds from epoch)
    epoch = datetime(1970, 1, 1)
    seconds = (created_at - epoch).total_seconds() - 1134028003

    # Formula: sign(score) * log10(|score|) + (age_in_seconds / 45000)
    # 45000 seconds ≈ 12.5 hours (time decay factor)
    hot_score = round(sign * order + seconds / 45000, 7)

    return hot_score


def calculate_controversy_score(upvotes, downvotes):
    """
    Controversial ranking
    Favors posts with both many upvotes and downvotes
    """

    if upvotes == 0 or downvotes == 0:
        return 0

    total_votes = upvotes + downvotes
    balance = min(upvotes, downvotes) / max(upvotes, downvotes)

    # Higher score when votes are balanced and numerous
    return total_votes ** balance


def calculate_best_score(upvotes, downvotes):
    """
    'Best' ranking for comments
    Uses Wilson score confidence interval
    """

    if upvotes + downvotes == 0:
        return 0

    n = upvotes + downvotes
    p = upvotes / n

    # Wilson score with 95% confidence
    # https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    z = 1.96  # 95% confidence
    denominator = 1 + z**2 / n
    p_hat = (p + z**2 / (2 * n)) / denominator
    width = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator

    return p_hat - width


# Ranking computation worker
class RankingWorker:
    def run(self):
        """Periodically recompute rankings"""

        while True:
            # Get posts created in last 48 hours
            recent_posts = db.query("""
                SELECT post_id, upvotes_count, downvotes_count, created_at
                FROM posts
                WHERE created_at > NOW() - INTERVAL '48 hours'
            """)

            # Calculate hot scores
            for post in recent_posts:
                hot_score = calculate_hot_score(
                    post.upvotes_count,
                    post.downvotes_count,
                    post.created_at
                )

                # Update in database
                db.execute("""
                    UPDATE posts
                    SET hot_score = ?
                    WHERE post_id = ?
                """, hot_score, post.post_id)

                # Update Redis sorted set
                redis.zadd(
                    f"subreddit:{post.subreddit_id}:hot",
                    {post.post_id: hot_score}
                )

            # Sleep for 30 seconds
            time.sleep(30)
```

### D. Comment Tree Service

**Nested Comment Loading:**

```python
class CommentService:
    def get_comment_tree(self, post_id, sort='best', max_depth=10):
        """
        Load nested comment tree for a post
        Returns tree structure with depth-limited nesting
        """

        # Check cache
        cache_key = f"comments:post:{post_id}:{sort}"
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Fetch all comments for post
        comments = cassandra.execute("""
            SELECT comment_id, parent_id, user_id, text, score, depth, created_at
            FROM comments
            WHERE post_id = ?
        """, post_id)

        # Build comment tree
        comment_map = {}
        root_comments = []

        # First pass: create comment objects
        for comment in comments:
            comment_obj = {
                'comment_id': comment.comment_id,
                'parent_id': comment.parent_id,
                'author': self.get_username(comment.user_id),
                'text': comment.text,
                'score': comment.score,
                'depth': comment.depth,
                'created_at': comment.created_at.isoformat(),
                'replies': []
            }
            comment_map[comment.comment_id] = comment_obj

            if comment.parent_id is None:
                root_comments.append(comment_obj)

        # Second pass: build tree structure
        for comment in comments:
            if comment.parent_id and comment.parent_id in comment_map:
                parent = comment_map[comment.parent_id]
                child = comment_map[comment.comment_id]
                parent['replies'].append(child)

        # Sort based on algorithm
        if sort == 'best':
            self.sort_by_best(root_comments)
        elif sort == 'top':
            self.sort_by_score(root_comments)
        elif sort == 'new':
            self.sort_by_time(root_comments)

        # Limit depth
        result = self.limit_depth(root_comments, max_depth)

        # Cache for 10 minutes
        redis.setex(cache_key, 600, json.dumps(result))

        return result

    def sort_by_best(self, comments):
        """Sort comments by 'best' algorithm (Wilson score)"""

        for comment in comments:
            # Calculate best score (would need vote data)
            comment['best_score'] = self.calculate_comment_best_score(comment)

            # Recursively sort replies
            if comment['replies']:
                self.sort_by_best(comment['replies'])

        comments.sort(key=lambda c: c['best_score'], reverse=True)

    def limit_depth(self, comments, max_depth, current_depth=0):
        """Limit comment tree depth"""

        if current_depth >= max_depth:
            return comments

        for comment in comments:
            if comment['replies']:
                comment['replies'] = self.limit_depth(
                    comment['replies'],
                    max_depth,
                    current_depth + 1
                )

        return comments

    def add_comment(self, post_id, user_id, text, parent_id=None):
        """Add a new comment"""

        comment_id = generate_id()

        # Determine depth
        depth = 0
        if parent_id:
            parent = self.get_comment(parent_id)
            depth = parent.depth + 1

        # Insert into Cassandra
        cassandra.execute("""
            INSERT INTO comments
            (comment_id, post_id, parent_id, user_id, text, score, depth, created_at)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?)
        """, comment_id, post_id, parent_id, user_id, text, depth, now())

        # Update post comment count
        db.execute("""
            UPDATE posts
            SET comment_count = comment_count + 1
            WHERE post_id = ?
        """, post_id)

        # Invalidate cache
        redis.delete(f"comments:post:{post_id}:*")

        # Award karma to user (async)
        kafka.publish("comment_created", {
            "user_id": user_id,
            "comment_id": comment_id
        })

        return comment_id
```

### E. Karma System

**Karma Calculation:**

```python
class KarmaService:
    def update_user_karma(self, user_id):
        """Recalculate user's karma"""

        # Calculate post karma
        post_karma = db.query("""
            SELECT SUM(score) as total
            FROM posts
            WHERE user_id = ? AND is_removed = FALSE
        """, user_id)[0].total or 0

        # Calculate comment karma
        comment_karma = cassandra.execute("""
            SELECT SUM(score) as total
            FROM user_comments
            WHERE user_id = ?
        """, user_id)[0].total or 0

        # Update user record
        db.execute("""
            UPDATE users
            SET post_karma = ?, comment_karma = ?
            WHERE user_id = ?
        """, post_karma, comment_karma, user_id)

        # Update cache
        redis.hmset(f"user:{user_id}:karma", {
            "post": post_karma,
            "comment": comment_karma,
            "total": post_karma + comment_karma
        })

        return post_karma, comment_karma

    # Async karma worker (listens to Kafka events)
    def karma_worker(self):
        """Periodically update karma for active users"""

        consumer = kafka.consumer("vote_cast")

        for message in consumer:
            event = json.loads(message.value)

            if event['target_type'] == 'post':
                # Get post author
                post = db.query("SELECT user_id FROM posts WHERE post_id = ?",
                               event['target_id'])
                if post:
                    # Queue for karma update (debounced)
                    redis.sadd("karma:update_queue", post[0].user_id)

        # Batch update every minute
        while True:
            time.sleep(60)

            user_ids = redis.smembers("karma:update_queue")
            redis.delete("karma:update_queue")

            for user_id in user_ids:
                self.update_user_karma(user_id)
```

## 9. Data Flow

### Flow 1: User Creates a Post

```
1. User submits post to r/programming
2. Frontend sends POST request
   POST /api/v1/posts
3. Post Service:
   - Validates user is not banned from subreddit
   - Generates post_id (base36 encoded)
   - Inserts into PostgreSQL posts table
   - Initial score = 1 (self-upvote)
   - Calculate initial hot_score
4. Insert into Elasticsearch for search
5. Add to Redis sorted sets:
   - subreddit:r/programming:hot
   - subreddit:r/programming:new
6. If has media:
   - Store media in S3
   - Generate thumbnail (async worker)
7. Publish event to Kafka: "post_created"
8. Return success to user (< 200ms)
9. [Async] Notify moderators (modqueue)
10. [Async] Check AutoMod rules
```

### Flow 2: User Votes on Post

```
1. User clicks upvote button
2. Frontend sends POST request
   POST /api/v1/vote
   {
       "target_type": "post",
       "target_id": "abc123",
       "direction": 1
   }
3. Vote Service:
   - Check if user already voted
   - Update vote in Cassandra votes table
   - Update vote_counts (counter column)
   - Update Redis cache immediately
4. Calculate new score
5. Publish to Kafka: "vote_cast"
6. Return new score to client (< 100ms)
7. [Async] Ranking Worker:
   - Recalculate hot_score
   - Update Redis sorted sets
   - Update PostgreSQL posts table
8. [Async] Karma Worker:
   - Queue post author for karma update
   - Update after 1 minute (batched)
```

### Flow 3: User Loads Subreddit Feed

```
1. User navigates to r/programming
2. Frontend requests feed
   GET /api/v1/subreddits/programming/posts?sort=hot&limit=25
3. Feed Service:
   - Check Redis cache
   - Key: subreddit:programming:hot
4. Cache HIT:
   - Get top 25 post IDs from sorted set
   - Batch fetch post details from Redis
   - For cache misses, fetch from PostgreSQL
   - Return to client (< 100ms)
5. Cache MISS:
   - Query PostgreSQL:
     SELECT * FROM posts
     WHERE subreddit_id = ? AND is_removed = FALSE
     ORDER BY hot_score DESC
     LIMIT 25
   - Cache post details in Redis
   - Add to sorted set
   - Return to client (< 300ms)
6. Client renders posts
7. Lazy-load media from CDN
```

### Flow 4: User Loads Comment Thread

```
1. User clicks on post
2. Frontend requests comments
   GET /api/v1/posts/abc123/comments?sort=best
3. Comment Service:
   - Check cache: comments:post:abc123:best
4. Cache HIT:
   - Return cached comment tree (< 50ms)
5. Cache MISS:
   - Query Cassandra for all comments on post
   - Build comment tree in memory
   - Sort by 'best' algorithm
   - Limit depth to 10 levels
   - Cache result (TTL: 10 min)
   - Return to client (< 300ms)
6. Client renders nested comments
7. "Load more comments" loads additional replies
```

## 10. Scalability Considerations

### Database Sharding

**Posts Table Sharding:**
```
Shard by subreddit_id

Benefits:
- All posts in a subreddit on same shard
- Fast subreddit feed queries
- Good distribution (100K subreddits)

Challenges:
- Popular subreddits create hotspots
- Solution: Further shard large subreddits by time range
```

**Comments Sharding:**
```
Cassandra handles this automatically
Partition key: post_id
Good distribution (2M posts/day)
```

### Caching Strategy

```
Three-tier caching:

L1: Application cache (in-process)
- Active user sessions
- Recent votes by user
- Size: 100 MB per server

L2: Redis cluster
- Post details
- Comment trees
- Rankings
- Size: 500 GB

L3: CDN
- Media files
- Static assets
- Size: Unlimited

Cache invalidation:
- Post/comment edit: Invalidate specific key
- New vote: Update counter immediately, recalc rank every 30s
- New comment: Invalidate comment tree cache
```

### Handling Viral Posts

```python
# When post goes viral (e.g., 1000+ upvotes in 1 hour)

if post.score > 1000 and post.age_hours < 1:
    # Mark as viral
    redis.sadd("viral_posts", post_id)

    # Aggressive caching
    redis.setex(f"post:{post_id}", 3600, post_data)

    # Rate limit votes (prevent vote manipulation)
    # Require CAPTCHA for votes

    # Load balance comment queries
    # Replicate post data across multiple cache nodes
```

### Auto-Scaling

```yaml
# Post Service
min_replicas: 10
max_replicas: 100
metrics:
  - type: cpu
    target: 70%
  - type: custom
    metric: posts_per_second
    target: 100

# Vote Service (handles most traffic)
min_replicas: 50
max_replicas: 500
metrics:
  - type: custom
    metric: votes_per_second
    target: 200

# Comment Service
min_replicas: 20
max_replicas: 200
```

## 11. Trade-offs

### 1. Comment Storage: PostgreSQL vs. Cassandra

**Decision: Cassandra**

PostgreSQL:
- Good for tree structure (recursive queries)
- Strong consistency
- Complex queries supported
- Hard to scale writes (20M comments/day)

Cassandra:
- Excellent write throughput
- Linear scalability
- Eventual consistency (acceptable for comments)
- Tree structure requires application-level logic

### 2. Vote Counting: Real-time vs. Batch

**Decision: Hybrid (real-time for cache, batch for DB)**

Real-time:
- Users see immediate feedback
- Redis counters updated instantly
- Database updated async (eventual consistency)

### 3. Ranking: Pre-compute vs. On-demand

**Decision: Pre-compute (every 30 seconds)**

Pre-compute:
- Fast feed loading (< 100ms)
- Requires background workers
- Stale data (30-60 second lag)

On-demand:
- Always fresh data
- Slow (calculate for every request)
- High CPU usage

### 4. Comment Threading: Depth Limit

**Decision: Limit to 10 levels**

Reasons:
- Prevents infinite nesting
- Improves load time
- "Continue this thread" link for deeper
- Rare to go beyond 10 levels

### 5. Search: Built-in vs. Elasticsearch

**Decision: Elasticsearch**

Built-in (PostgreSQL full-text search):
- Simple to implement
- No additional infrastructure
- Doesn't scale to 100M posts

Elasticsearch:
- Excellent full-text search
- Faceted search
- Scales horizontally
- Additional operational complexity

## 12. Follow-up Questions

### Functional

**Q1: How to implement Reddit Gold/Awards?**
A: Create `awards` table (award_type, giver_id, recipient_id, post_id, comment_id). Deduct coins from giver, grant benefits to recipient (ad-free, coins, etc.). Display award icons on posts.

**Q2: How to handle deleted comments in threads?**
A: Soft delete (set `is_deleted=true`). Show "[deleted]" as author and "[removed]" as text. Keep structure for replies. Permanently delete after 30 days.

**Q3: How to implement AutoModerator?**
A: Rule engine with pattern matching. Check posts/comments against rules on creation. Actions: remove, spam, approve, report. Store rules in subreddit config (JSONB).

**Q4: How to implement "saved" posts?**
A: Create `saved_posts` table (user_id, post_id, saved_at). API to save/unsave. User can view saved posts in their profile.

### Scale

**Q5: How to handle a subreddit with 50M subscribers?**
A:
- Shard subreddit data by time (current month, last month, older)
- Cache hot posts aggressively
- Use CDN for all media
- Consider read replicas for specific large subreddits

**Q6: What if a post gets 100K comments?**
A:
- Load comments in batches (pagination)
- "Continue this thread" for deep nesting
- Collapse low-scored comment trees by default
- Cache top-level comments only
- Load replies on demand

**Q7: How to handle 1M votes per second during major event?**
A:
- Cassandra can handle the writes
- Queue votes in Kafka (buffer)
- Async workers process votes
- Update counters in batches
- Eventual consistency (5-10 second lag acceptable)

### Reliability

**Q8: What if Redis cache fails?**
A:
- Redis Cluster with automatic failover
- Fall back to database if Redis unavailable
- Graceful degradation (slower but still works)
- Circuit breaker to prevent cascade

**Q9: How to prevent vote manipulation?**
A:
- Rate limiting (1000 votes per hour)
- CAPTCHA for suspicious patterns
- Detect vote brigading (many votes from same IP)
- Shadowban users who manipulate votes
- Algorithm to detect unnatural voting patterns

**Q10: How to ensure comment consistency?**
A:
- Cassandra provides eventual consistency
- For critical operations (moderation), use quorum reads
- Typically 1-2 second lag is acceptable
- Users can refresh to see latest

### Advanced

**Q11: How to implement Reddit's "Best" sorting for comments?**
A: Use Wilson score confidence interval. Accounts for both upvotes and total votes. Prevents single upvote from ranking above 100 upvotes / 10 downvotes.

**Q12: How to implement multi-reddits (custom feed from multiple subreddits)?**
A: Store in `multireddits` table (user_id, name, subreddit_ids[]). Feed generation merges posts from all subreddits, sorts by hot score.

**Q13: How to add real-time live threads?**
A: WebSocket connection for real-time updates. Comment stream via Kafka. Push new comments to connected clients. Throttle to prevent spam (max 10/sec).

**Q14: How to implement Reddit's search syntax (author:, subreddit:, etc.)?**
A: Parse query in Search Service. Convert to Elasticsearch query. Support operators: author:, subreddit:, flair:, -exclude, OR, AND, quotes.

**Q15: How to handle shadowbanning?**
A: Add `is_shadowbanned` to users table. Shadowbanned users see their posts/comments normally, but others don't see them. Useful for spam prevention.

---

**Estimated Interview Time:** 60-75 minutes

**Key Learning Points:**
- Ranking algorithms (Hot, Controversial, Best)
- Nested comment tree storage and retrieval
- High-write vote system with Cassandra
- Karma calculation and aggregation
- Eventual consistency trade-offs
- Caching strategy for rankings

**Difficulty:** Medium (requires understanding of ranking algorithms and nested data structures)
