# Design Twitter/X

## 1. Problem Statement & Scope

Design a microblogging and social networking platform where users can post short messages (tweets), follow other users, and engage with content through likes, retweets, and replies.

### In Scope:
- User registration, authentication, and profiles
- Tweet creation (text, images, videos)
- Tweet threading and replies
- Timeline generation (home, user, mentions)
- Following/followers system
- Likes, retweets, and quote tweets
- Real-time trending topics
- Hashtags and mentions
- Search (tweets, users, trending)
- Real-time notifications
- Tweet analytics (views, engagement)

### Out of Scope:
- Twitter Spaces (audio chat)
- Direct messaging (covered separately)
- Twitter Blue / premium features
- Ads platform
- Content moderation details
- Twitter Lists
- Bookmarks (similar to likes)

### Scale:
- 400 million daily active users (DAU)
- 500 million tweets per day
- 200 billion timeline reads per day
- Peak: 150,000 tweets/second (major events)
- Average: 6,000 tweets/second
- Read:Write ratio: 1000:1

## 2. Functional Requirements

### High Priority (P0):

**FR1: User Management**
- Register with email/phone
- Login and authentication
- Profile management (bio, location, website, banner)
- Verified accounts (blue check)
- Follow/unfollow users

**FR2: Tweet Operations**
- Create tweet (max 280 characters)
- Upload media (up to 4 images or 1 video)
- Delete own tweets
- Edit tweets (with edit history)
- View single tweet with reply thread

**FR3: Engagement**
- Like/unlike tweets
- Retweet/undo retweet
- Quote tweet (retweet with comment)
- Reply to tweets
- View tweet analytics (impressions, engagements)

**FR4: Timeline Generation**
- Home timeline (from followed users)
- User timeline (user's tweets and retweets)
- Mentions timeline (tweets mentioning user)
- Algorithmic ranking option

**FR5: Hashtags and Mentions**
- Click hashtag to see all tweets with that hashtag
- Mention users with @username
- Receive notifications for mentions

**FR6: Trending Topics**
- Real-time trending hashtags
- Trending topics by location
- "For You" trending (personalized)

**FR7: Search**
- Search tweets by keywords
- Search users
- Advanced search (date range, from user, etc.)
- Real-time search

### Medium Priority (P1):

**FR8: Tweet Threading**
- Create multi-tweet threads
- View threaded conversations
- Reply chains

**FR9: Notifications**
- Real-time notifications for likes, retweets, mentions
- Push notifications
- Notification preferences

**FR10: Analytics**
- View count for each tweet
- Engagement rate
- Follower growth

## 3. Non-Functional Requirements (Scale, Performance, Availability)

### Scale Requirements:
- **Daily Active Users:** 400 million
- **Total Users:** 1 billion
- **Tweets per day:** 500 million
- **Timeline reads per day:** 200 billion
- **Peak tweets/second:** 150,000 (during major events)
- **Average tweets/second:** 6,000
- **Concurrent users:** 50 million

### Performance Requirements:
- **Tweet creation:** < 100ms (p95)
- **Timeline load:** < 500ms (p95)
- **Search response:** < 300ms (p95)
- **Trending calculation:** < 1 second lag
- **Notification delivery:** < 500ms
- **Tweet delivery to followers:** < 5 seconds (p95)

### Availability:
- **Service availability:** 99.99%
- **Data durability:** 99.999999999% (11 nines)
- **Maximum downtime:** 52 minutes/year

### Consistency:
- **Tweet creation:** Strong consistency
- **Timelines:** Eventual consistency (< 5 seconds)
- **Trending:** Eventual consistency (< 1 minute)
- **Counts (likes, retweets):** Eventual consistency

### Scalability:
- Handle 10x traffic during breaking news
- Auto-scale to handle viral tweets
- Graceful degradation during outages

## 4. Back-of-envelope Calculations

### Traffic Estimates:

**Tweets:**
- Tweets per day: 500M
- Tweets per second: 500M ÷ 86,400 = ~6K TPS
- Peak (during events): 150K TPS (25x normal)

**Timeline Reads:**
- Daily active users: 400M
- Average timeline refreshes per user: 20/day
- Timeline reads: 400M × 20 = 8 billion/day
- Reads per second: 8B ÷ 86,400 = ~92K RPS
- With cache misses (10%): ~9K RPS to database

**Fan-out:**
- Average followers per user: 200
- Tweets per day: 500M
- Fan-out writes: 500M × 200 = 100 billion timeline writes/day
- Per second: 100B ÷ 86,400 = 1.15M writes/second

### Storage Calculations:

**Tweets:**
- Size per tweet: 280 characters × 2 bytes = 560 bytes
- Metadata: 500 bytes (user_id, timestamp, likes_count, etc.)
- Total per tweet: ~1 KB
- Daily: 500M × 1 KB = 500 GB/day
- Yearly: 500 GB × 365 = 182 TB/year

**Media:**
- 30% of tweets have media
- Average image size: 1 MB (compressed)
- Media tweets per day: 500M × 0.3 = 150M
- Daily storage: 150M × 1 MB = 150 TB/day
- Yearly: 150 TB × 365 = 55 PB/year

**User Data:**
- Total users: 1 billion
- Data per user: 5 KB
- Total: 1B × 5 KB = 5 TB

**Social Graph:**
- Average follows per user: 200
- Total relationships: 1B × 200 = 200 billion
- Storage per relationship: 16 bytes (8 bytes each for follower_id, followee_id)
- Total: 200B × 16 bytes = 3.2 TB

**Timeline Cache:**
- Active users: 400M
- Cache 500 tweet IDs per user
- Size: 400M × 500 × 8 bytes = 1.6 TB

**Total Storage (Year 1):** ~55 PB (mostly media)

### Bandwidth:

**Incoming (Tweets):**
- 500 GB/day (text) = 5.8 MB/s
- 150 TB/day (media) = 1.7 GB/s
- Peak (25x): 42.5 GB/s

**Outgoing (Timeline reads):**
- Assume 10 tweets per timeline view
- 8B timeline views × 10 tweets = 80B tweet views
- Average tweet with thumbnail: 50 KB
- 80B × 50 KB = 4 PB/day = 46 TB/s
- **CDN is essential**

### Compute:

**API Servers:**
- 100K RPS (read + write)
- Each server: 1K RPS
- Servers needed: 100 servers × 3 (redundancy) = 300 servers

**Cache Servers:**
- Working set: 2 TB (timelines + tweets)
- Redis cluster: 10 nodes × 200 GB = 2 TB

**Database Servers:**
- Write: 6K TPS (tweets)
- Read: 9K RPS (cache misses)
- Sharded across 50 database nodes

## 5. High-Level Architecture Diagram Description

```
                        [Clients - Web, Mobile, API]
                                    |
                                    v
                            [Global Load Balancer]
                                    |
                    +---------------+---------------+
                    |               |               |
                [US-EAST]       [EU-WEST]       [APAC]
                    |               |               |
                    v               v               v
            [Regional Load Balancer]
                    |
                    v
            [API Gateway / Rate Limiter]
                    |
        +-----------+-----------+-----------+-----------+
        |           |           |           |           |
        v           v           v           v           v
    [Tweet      [Timeline   [Search    [Trending  [Notification
     Service]    Service]    Service]   Service]   Service]
        |           |           |           |           |
        +-----------|-----------|-----------|-----------|
                    |
                    v
        [Kafka Event Stream / Message Bus]
                    |
        +-----------+-----------+-----------+
        |           |           |           |
        v           v           v           v
    [Fanout     [Analytics  [Real-time  [Content
     Service]    Service]    Service]    Moderation]


        v                   v                   v
[PostgreSQL Cluster] [Redis Cluster]    [Elasticsearch]
(Users, Tweets,      (Timelines,        (Search Index)
 Relationships)      Tweet Cache)
    (Sharded)          (2 TB)
        |
        v
    [S3 Storage]  ---------> [CloudFront CDN]
    (Media Files)             (Media Delivery)


[Additional Services]
    |
    v
[Trending Computation] (Apache Flink/Storm)
    |
    v
[Time-Series DB] (InfluxDB for analytics)
```

### Key Components:

1. **API Gateway:** Request routing, authentication, rate limiting
2. **Tweet Service:** Create, delete, edit tweets
3. **Timeline Service:** Generate and serve timelines
4. **Search Service:** Full-text search, real-time indexing
5. **Trending Service:** Calculate trending topics
6. **Fanout Service:** Distribute tweets to followers' timelines
7. **Notification Service:** Push notifications
8. **Kafka:** Event streaming between services
9. **PostgreSQL:** Primary datastore (sharded)
10. **Redis:** Cache layer for timelines and tweets
11. **Elasticsearch:** Search index
12. **S3 + CDN:** Media storage and delivery

## 6. API Design (RESTful endpoints)

### Tweet APIs

```
POST /api/v1/tweets
Request:
{
  "text": "Hello Twitter! #firstTweet",
  "media_ids": ["media_123", "media_456"],
  "reply_to_tweet_id": null,
  "quote_tweet_id": null,
  "poll": null
}
Response: 201 Created
{
  "tweet_id": "1234567890",
  "user": {
    "user_id": "123",
    "username": "johndoe",
    "display_name": "John Doe",
    "profile_pic": "https://...",
    "verified": true
  },
  "text": "Hello Twitter! #firstTweet",
  "media": [...],
  "created_at": "2025-11-12T10:30:00Z",
  "metrics": {
    "likes": 0,
    "retweets": 0,
    "replies": 0,
    "views": 0
  }
}

GET /api/v1/tweets/{tweet_id}
Response: 200 OK
{
  "tweet_id": "1234567890",
  "user": {...},
  "text": "Hello Twitter!",
  "entities": {
    "hashtags": ["firstTweet"],
    "mentions": [],
    "urls": []
  },
  "media": [...],
  "metrics": {...},
  "viewer_context": {
    "has_liked": false,
    "has_retweeted": false
  },
  "created_at": "...",
  "source": "Twitter for iPhone"
}

DELETE /api/v1/tweets/{tweet_id}
Response: 204 No Content

PUT /api/v1/tweets/{tweet_id}
Request:
{
  "text": "Updated tweet text"
}
Response: 200 OK
# Returns tweet with edit_history field
```

### Engagement APIs

```
POST /api/v1/tweets/{tweet_id}/like
Response: 201 Created

DELETE /api/v1/tweets/{tweet_id}/like
Response: 204 No Content

POST /api/v1/tweets/{tweet_id}/retweet
Response: 201 Created
{
  "retweet_id": "9876543210",
  "original_tweet": {...}
}

DELETE /api/v1/tweets/{tweet_id}/retweet
Response: 204 No Content

POST /api/v1/tweets/{tweet_id}/quote
Request:
{
  "text": "Great point!",
  "quoted_tweet_id": "1234567890"
}
Response: 201 Created

GET /api/v1/tweets/{tweet_id}/likers?limit=50&cursor={cursor}
GET /api/v1/tweets/{tweet_id}/retweeters?limit=50&cursor={cursor}
```

### Timeline APIs

```
GET /api/v1/timelines/home?limit=20&cursor={cursor}
Query Parameters:
- limit: Number of tweets (default: 20, max: 100)
- cursor: Pagination cursor
- algorithm: 'chronological' or 'ranked' (default: ranked)

Response: 200 OK
{
  "tweets": [
    {
      "tweet_id": "...",
      "user": {...},
      "text": "...",
      "created_at": "...",
      "type": "tweet", // or "retweet", "quote_tweet"
      "original_tweet": {...} // if retweet
    }
  ],
  "next_cursor": "eyJwb3NpdGlvbiI6MjB9",
  "has_more": true
}

GET /api/v1/timelines/user/{user_id}?limit=20&cursor={cursor}
# User's tweets and retweets

GET /api/v1/timelines/user/{user_id}/tweets?limit=20
# Only user's original tweets (no retweets)

GET /api/v1/timelines/user/{user_id}/replies?limit=20
# User's replies

GET /api/v1/timelines/user/{user_id}/media?limit=20
# Tweets with media

GET /api/v1/timelines/user/{user_id}/likes?limit=20
# Tweets liked by user

GET /api/v1/timelines/mentions?limit=20&cursor={cursor}
# Tweets mentioning the authenticated user
```

### Search APIs

```
GET /api/v1/search/tweets?q={query}&limit=20&cursor={cursor}
Query Parameters:
- q: Search query (supports operators)
- limit: Results per page
- cursor: Pagination
- filters: 'media', 'verified', 'replies'
- sort: 'top', 'latest', 'people'
- since: ISO date (start date)
- until: ISO date (end date)

Examples:
/api/v1/search/tweets?q=bitcoin
/api/v1/search/tweets?q=from:elonmusk
/api/v1/search/tweets?q=to:support
/api/v1/search/tweets?q=%23AI+lang:en

Response: 200 OK
{
  "tweets": [...],
  "next_cursor": "...",
  "query_id": "search_123"
}

GET /api/v1/search/users?q={query}&limit=20
GET /api/v1/search/hashtags?q={query}&limit=20
```

### Trending APIs

```
GET /api/v1/trends/available
Response: List of locations with trending data

GET /api/v1/trends/place?id={woeid}
# woeid: Where On Earth ID (location identifier)
Response: 200 OK
{
  "trends": [
    {
      "name": "#BlackFriday",
      "url": "https://twitter.com/search?q=%23BlackFriday",
      "tweet_volume": 125000,
      "promoted": false,
      "rank": 1
    }
  ],
  "as_of": "2025-11-12T10:30:00Z",
  "location": {
    "name": "United States",
    "woeid": 23424977
  }
}

GET /api/v1/trends/for-you
# Personalized trends for authenticated user
```

### User APIs

```
GET /api/v1/users/{user_id}
GET /api/v1/users/by/username/{username}

POST /api/v1/users/{user_id}/follow
DELETE /api/v1/users/{user_id}/follow

GET /api/v1/users/{user_id}/followers?limit=50&cursor={cursor}
GET /api/v1/users/{user_id}/following?limit=50&cursor={cursor}

POST /api/v1/users/{user_id}/mute
POST /api/v1/users/{user_id}/block
```

### Media Upload APIs

```
POST /api/v1/media/upload
Request: multipart/form-data
{
  "media": <file>,
  "media_category": "tweet_image" // or "tweet_video"
}
Response: 200 OK
{
  "media_id": "media_123456",
  "media_url": "https://...",
  "type": "image",
  "size": 1234567,
  "processing_status": "succeeded"
}

# For large videos (chunked upload)
POST /api/v1/media/upload/init
POST /api/v1/media/upload/append
POST /api/v1/media/upload/finalize
```

### Notification APIs

```
GET /api/v1/notifications?limit=50&cursor={cursor}&types=mention,like,retweet

Response:
{
  "notifications": [
    {
      "notification_id": "123",
      "type": "like",
      "created_at": "...",
      "actors": [
        {"user_id": "456", "username": "jane"}
      ],
      "tweet": {...},
      "is_read": false
    }
  ],
  "unread_count": 15
}

PUT /api/v1/notifications/mark-read
```

## 7. Database Design (Schema, Indexes)

### PostgreSQL Schema (Sharded by user_id)

```sql
-- Users Table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(50),
    bio VARCHAR(160),
    location VARCHAR(100),
    website VARCHAR(200),
    profile_pic_url VARCHAR(500),
    banner_url VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    is_protected BOOLEAN DEFAULT FALSE, -- private account
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    tweets_count INT DEFAULT 0,
    joined_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Tweets Table (Sharded by user_id for co-location)
CREATE TABLE tweets (
    tweet_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    text TEXT,
    reply_to_tweet_id BIGINT,
    reply_to_user_id BIGINT,
    quote_tweet_id BIGINT,
    retweet_of_tweet_id BIGINT, -- if this is a retweet
    is_edited BOOLEAN DEFAULT FALSE,
    edit_history JSONB, -- array of previous versions
    likes_count INT DEFAULT 0,
    retweets_count INT DEFAULT 0,
    replies_count INT DEFAULT 0,
    quote_tweets_count INT DEFAULT 0,
    views_count BIGINT DEFAULT 0,
    source VARCHAR(100), -- "Twitter for iPhone"
    lang VARCHAR(10),
    possibly_sensitive BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tweets_user_id ON tweets(user_id, created_at DESC);
CREATE INDEX idx_tweets_reply_to ON tweets(reply_to_tweet_id);
CREATE INDEX idx_tweets_created_at ON tweets(created_at DESC);

-- Tweet Media
CREATE TABLE tweet_media (
    media_id BIGSERIAL PRIMARY KEY,
    tweet_id BIGINT NOT NULL,
    media_type VARCHAR(10) NOT NULL, -- 'image', 'video', 'gif'
    media_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    width INT,
    height INT,
    duration INT, -- for videos
    alt_text VARCHAR(1000),
    display_order INT DEFAULT 0
);

CREATE INDEX idx_tweet_media_tweet_id ON tweet_media(tweet_id);

-- Tweet Entities (hashtags, mentions, URLs extracted from text)
CREATE TABLE tweet_entities (
    entity_id BIGSERIAL PRIMARY KEY,
    tweet_id BIGINT NOT NULL,
    entity_type VARCHAR(20) NOT NULL, -- 'hashtag', 'mention', 'url'
    entity_value TEXT NOT NULL,
    start_index INT,
    end_index INT
);

CREATE INDEX idx_tweet_entities_tweet ON tweet_entities(tweet_id);
CREATE INDEX idx_tweet_entities_value ON tweet_entities(entity_type, entity_value);

-- Followers Table (Sharded twice - by follower and by followee)
-- Shard 1: By follower_id (for "who do I follow?")
CREATE TABLE following (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_following_followee ON following(followee_id);

-- Shard 2: By followee_id (for "who follows me?")
CREATE TABLE followers (
    followee_id BIGINT NOT NULL,
    follower_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (followee_id, follower_id)
);

CREATE INDEX idx_followers_follower ON followers(follower_id);

-- Likes Table (Sharded by tweet_id)
CREATE TABLE likes (
    tweet_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tweet_id, user_id)
);

CREATE INDEX idx_likes_user_id ON likes(user_id, created_at DESC);

-- Retweets Table
CREATE TABLE retweets (
    retweet_id BIGINT NOT NULL,
    original_tweet_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (original_tweet_id, user_id)
);

CREATE INDEX idx_retweets_user ON retweets(user_id, created_at DESC);

-- Hashtags Table
CREATE TABLE hashtags (
    hashtag_id BIGSERIAL PRIMARY KEY,
    hashtag VARCHAR(139) UNIQUE NOT NULL, -- lowercase
    tweet_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hashtags_tag ON hashtags(hashtag);
CREATE INDEX idx_hashtags_count ON hashtags(tweet_count DESC);

-- Trending Topics (computed periodically)
CREATE TABLE trending_topics (
    trend_id BIGSERIAL PRIMARY KEY,
    hashtag VARCHAR(139) NOT NULL,
    location_woeid INT NOT NULL, -- Where On Earth ID
    tweet_volume INT NOT NULL,
    trend_score FLOAT NOT NULL,
    rank INT NOT NULL,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trending_location ON trending_topics(location_woeid, rank);
CREATE INDEX idx_trending_computed ON trending_topics(computed_at DESC);

-- User Timeline Cache (materialized timelines)
-- Stores in PostgreSQL but heavily cached in Redis
CREATE TABLE user_timelines (
    user_id BIGINT NOT NULL,
    tweet_id BIGINT NOT NULL,
    tweet_owner_id BIGINT NOT NULL,
    is_retweet BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, tweet_id)
);

CREATE INDEX idx_user_timelines_user ON user_timelines(user_id, created_at DESC);
```

### Redis Cache Structures

```
# Home Timeline Cache (Sorted Set by timestamp)
Key: timeline:home:{user_id}
Type: Sorted Set
Score: timestamp (for chronological order)
Members: tweet_id
TTL: 10 minutes
Size: Top 500 tweets
Commands:
  ZADD timeline:home:123 1699876543 tweet_456
  ZREVRANGE timeline:home:123 0 19 WITHSCORES

# Tweet Cache
Key: tweet:{tweet_id}
Type: Hash
TTL: 1 hour
Fields: {user_id, text, created_at, likes_count, retweets_count, ...}

# User Cache
Key: user:{user_id}
Type: Hash
TTL: 1 hour
Fields: {username, display_name, profile_pic, followers_count, ...}

# Following List Cache
Key: following:{user_id}
Type: Set
TTL: 1 hour
Members: user_ids of people this user follows
Size: Varies (average 200)

# Like Status Cache (did user X like tweet Y?)
Key: like:{user_id}:{tweet_id}
Type: String
Value: "1" or not exists
TTL: 30 minutes

# Tweet Counts (real-time counters)
Key: tweet:counts:{tweet_id}
Type: Hash
TTL: No expiry
Fields: {likes: 123, retweets: 45, replies: 12, views: 5000}

# Trending Cache
Key: trending:{location_woeid}
Type: List of JSON objects
TTL: 5 minutes
Data: [{hashtag, volume, rank}, ...]

# Rate Limiting
Key: ratelimit:tweet:{user_id}
Type: String (counter)
TTL: 1 hour
Limit: 50 tweets per hour

Key: ratelimit:follow:{user_id}
Type: String (counter)
TTL: 1 hour
Limit: 400 follows per hour
```

### Elasticsearch Index

```json
{
  "tweets_index": {
    "settings": {
      "number_of_shards": 50,
      "number_of_replicas": 2,
      "analysis": {
        "analyzer": {
          "tweet_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "stop", "snowball"]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "tweet_id": {"type": "long"},
        "user_id": {"type": "long"},
        "username": {"type": "keyword"},
        "text": {
          "type": "text",
          "analyzer": "tweet_analyzer",
          "fields": {
            "keyword": {"type": "keyword"}
          }
        },
        "hashtags": {"type": "keyword"},
        "mentions": {"type": "keyword"},
        "created_at": {"type": "date"},
        "likes_count": {"type": "integer"},
        "retweets_count": {"type": "integer"},
        "lang": {"type": "keyword"},
        "has_media": {"type": "boolean"},
        "is_verified_user": {"type": "boolean"},
        "location": {"type": "geo_point"}
      }
    }
  }
}
```

## 8. Core Components

### A. Feed Generation Service

**Challenge:** Generate timeline for 400M users in real-time

**Approach: Hybrid Fanout**

```python
class TimelineService:
    def __init__(self):
        self.CELEBRITY_THRESHOLD = 1_000_000  # 1M followers

    def on_tweet_created(self, tweet_id, user_id):
        """Called when user creates a tweet"""
        # Get follower count
        user = self.get_user(user_id)

        if user.followers_count > self.CELEBRITY_THRESHOLD:
            # Celebrity: Don't fanout
            # Followers will pull tweets when they request timeline
            self.mark_as_celebrity_tweet(tweet_id, user_id)
        else:
            # Regular user: Fanout to all followers
            self.fanout_to_followers(tweet_id, user_id)

    def fanout_to_followers(self, tweet_id, user_id):
        """Push tweet to all followers' timelines"""
        # Get followers from cache
        follower_ids = redis.smembers(f"followers:{user_id}")

        if not follower_ids:
            # Cache miss - load from DB
            follower_ids = db.query("""
                SELECT follower_id FROM followers
                WHERE followee_id = ?
            """, user_id)
            redis.sadd(f"followers:{user_id}", *follower_ids)

        # Batch fanout (async)
        timestamp = int(time.time())
        pipeline = redis.pipeline()

        for follower_id in follower_ids:
            # Add to follower's timeline (sorted set)
            pipeline.zadd(
                f"timeline:home:{follower_id}",
                {tweet_id: timestamp}
            )
            # Trim to keep only latest 500 tweets
            pipeline.zremrangebyrank(
                f"timeline:home:{follower_id}",
                0, -501
            )

        pipeline.execute()

        # Also write to persistent storage (async)
        kafka.publish("timeline_insert", {
            "tweet_id": tweet_id,
            "follower_ids": follower_ids,
            "timestamp": timestamp
        })

    def get_home_timeline(self, user_id, limit=20, cursor=None):
        """Get home timeline for user"""
        # Check cache first
        cache_key = f"timeline:home:{user_id}"
        cached_timeline = redis.zrevrange(cache_key, 0, limit - 1)

        if cached_timeline:
            # Cache hit
            tweets = self.hydrate_tweets(cached_timeline)
            return self.rank_tweets(tweets, user_id)

        # Cache miss - generate timeline
        timeline = self.generate_timeline(user_id, limit)

        # Cache for next time
        self.cache_timeline(user_id, timeline)

        return timeline

    def generate_timeline(self, user_id, limit=20):
        """Generate timeline from scratch"""
        # Get users that current user follows
        following_ids = redis.smembers(f"following:{user_id}")

        if not following_ids:
            following_ids = db.query("""
                SELECT followee_id FROM following
                WHERE follower_id = ?
            """, user_id)

        # Separate regular users and celebrities
        regular_users = []
        celebrities = []

        for followee_id in following_ids:
            if self.is_celebrity(followee_id):
                celebrities.append(followee_id)
            else:
                regular_users.append(followee_id)

        # Get tweets from regular users (pre-fanned out)
        regular_tweets = redis.zrevrange(
            f"timeline:home:{user_id}", 0, limit * 2)

        # Get recent tweets from celebrities (pull model)
        celebrity_tweets = []
        if celebrities:
            celebrity_tweets = db.query("""
                SELECT tweet_id, created_at
                FROM tweets
                WHERE user_id IN (?)
                  AND created_at > NOW() - INTERVAL '3 days'
                ORDER BY created_at DESC
                LIMIT ?
            """, celebrities, limit)

        # Merge and rank
        all_tweet_ids = regular_tweets + [t.tweet_id for t in celebrity_tweets]
        tweets = self.hydrate_tweets(all_tweet_ids)

        return self.rank_tweets(tweets, user_id)[:limit]

    def rank_tweets(self, tweets, user_id):
        """Apply ranking algorithm"""
        # Simple chronological for now
        # In production: ML-based ranking

        for tweet in tweets:
            score = 0

            # Recency (0-1, decays over time)
            age_hours = (time.time() - tweet.created_at) / 3600
            recency = 1 / (1 + age_hours / 24)
            score += recency * 0.4

            # Engagement rate
            engagement = (tweet.likes_count + tweet.retweets_count * 2)
            engagement_score = min(engagement / 100, 1.0)
            score += engagement_score * 0.3

            # User affinity (how often user interacts with author)
            affinity = self.get_user_affinity(user_id, tweet.user_id)
            score += affinity * 0.2

            # Tweet type (some users prefer media)
            if tweet.has_media:
                score += 0.1

            tweet.score = score

        # Sort by score
        return sorted(tweets, key=lambda t: t.score, reverse=True)

    def hydrate_tweets(self, tweet_ids):
        """Fetch full tweet details"""
        tweets = []

        # Batch fetch from cache
        pipeline = redis.pipeline()
        for tweet_id in tweet_ids:
            pipeline.hgetall(f"tweet:{tweet_id}")
        cached_tweets = pipeline.execute()

        # For cache misses, fetch from DB
        missing_ids = []
        for i, tweet_data in enumerate(cached_tweets):
            if tweet_data:
                tweets.append(Tweet.from_dict(tweet_data))
            else:
                missing_ids.append(tweet_ids[i])

        if missing_ids:
            db_tweets = db.query("""
                SELECT * FROM tweets WHERE tweet_id IN (?)
            """, missing_ids)
            tweets.extend(db_tweets)

            # Cache for future
            for tweet in db_tweets:
                redis.hmset(f"tweet:{tweet.tweet_id}", tweet.to_dict())
                redis.expire(f"tweet:{tweet.tweet_id}", 3600)

        return tweets
```

### B. Media Storage

**Architecture:**

```
Upload Flow:
1. Client requests upload URL
2. API generates presigned S3 URL
3. Client uploads directly to S3
4. Client confirms upload
5. Background worker processes media:
   - Images: Resize, optimize, generate thumbnails
   - Videos: Transcode to multiple qualities
6. Update tweet with final media URLs
```

**Implementation:**

```python
class MediaService:
    def initiate_upload(self, media_type, file_size):
        """Generate presigned URL for direct S3 upload"""
        media_id = generate_snowflake_id()

        # Generate S3 key
        key = f"media/temp/{media_id}.{media_type}"

        # Presigned URL (valid for 15 minutes)
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'twitter-media', 'Key': key},
            ExpiresIn=900
        )

        # Store metadata
        redis.setex(
            f"media:upload:{media_id}",
            900,
            json.dumps({
                'status': 'pending',
                'media_type': media_type,
                'temp_key': key
            })
        )

        return {
            'media_id': media_id,
            'upload_url': upload_url
        }

    def finalize_upload(self, media_id):
        """Confirm upload and start processing"""
        # Get metadata
        metadata = redis.get(f"media:upload:{media_id}")
        if not metadata:
            raise Exception("Upload expired")

        metadata = json.loads(metadata)

        # Verify file exists in S3
        if not s3_client.object_exists(metadata['temp_key']):
            raise Exception("File not found")

        # Queue for processing
        kafka.publish("media_processing", {
            'media_id': media_id,
            'media_type': metadata['media_type'],
            'temp_key': metadata['temp_key']
        })

        return {'media_id': media_id, 'status': 'processing'}

    def process_image(self, media_id, temp_key):
        """Process uploaded image"""
        # Download from S3
        image = s3_client.download(temp_key)

        # Generate sizes
        sizes = {
            'original': resize(image, max_size=4096),
            'large': resize(image, max_size=2048),
            'medium': resize(image, max_size=1200),
            'small': resize(image, max_size=680),
            'thumb': resize(image, max_size=150)
        }

        # Optimize and upload
        urls = {}
        for size_name, img in sizes.items():
            # Optimize (80% quality for smaller sizes)
            quality = 90 if size_name == 'original' else 80
            optimized = optimize_jpeg(img, quality=quality)

            # Upload to permanent location
            key = f"media/images/{media_id}_{size_name}.jpg"
            s3_client.upload(key, optimized)

            # Get CDN URL
            urls[size_name] = f"https://cdn.twitter.com/{key}"

        # Delete temp file
        s3_client.delete(temp_key)

        # Update metadata
        db.update("tweet_media", {
            'media_url': urls['original'],
            'thumbnail_url': urls['thumb'],
            'processing_status': 'completed'
        }, {'media_id': media_id})

        return urls

    def process_video(self, media_id, temp_key):
        """Process uploaded video"""
        # Use AWS Elastic Transcoder or similar
        job = transcoder.create_job({
            'input': temp_key,
            'outputs': [
                {'preset': '1080p', 'key': f"{media_id}_1080p.mp4"},
                {'preset': '720p', 'key': f"{media_id}_720p.mp4"},
                {'preset': '480p', 'key': f"{media_id}_480p.mp4"},
                {'preset': 'thumbnail', 'key': f"{media_id}_thumb.jpg"}
            ]
        })

        # Update status
        db.update("tweet_media", {
            'processing_status': 'transcoding',
            'job_id': job.id
        }, {'media_id': media_id})

        # Job completion will trigger callback
```

### C. CDN Integration

**Strategy:**

```
User Request -> DNS -> GeoDNS selects nearest CDN edge
                           |
                           v
                    CloudFront Edge Location
                           |
                   +-------+-------+
                   |               |
              [In Cache?]          |
                   |               |
                  YES              NO
                   |               |
                   v               v
            Return Cached     Fetch from S3
                               Cache at edge
                               Return to user

Cache-Control:
- Images: max-age=31536000 (1 year, immutable)
- Videos: max-age=31536000
- Thumbnails: max-age=86400 (1 day)
```

### D. Cache Layer

**Caching Strategy:**

```python
class CacheManager:
    def __init__(self):
        self.redis_cluster = RedisCluster(
            startup_nodes=[...],
            max_connections_per_node=50
        )

    # Cache aside pattern
    def get_tweet(self, tweet_id):
        # Try cache
        cache_key = f"tweet:{tweet_id}"
        tweet = self.redis_cluster.hgetall(cache_key)

        if tweet:
            # Cache hit
            return Tweet.from_dict(tweet)

        # Cache miss - fetch from DB
        tweet = db.query(
            "SELECT * FROM tweets WHERE tweet_id = ?",
            tweet_id
        )

        if tweet:
            # Store in cache
            self.redis_cluster.hmset(cache_key, tweet.to_dict())
            self.redis_cluster.expire(cache_key, 3600)

        return tweet

    # Write-through pattern for counts
    def increment_like_count(self, tweet_id):
        # Update cache immediately
        self.redis_cluster.hincrby(
            f"tweet:counts:{tweet_id}",
            "likes",
            1
        )

        # Async update to DB
        kafka.publish("update_counts", {
            "tweet_id": tweet_id,
            "field": "likes_count",
            "operation": "increment"
        })

    # Cache invalidation
    def invalidate_tweet(self, tweet_id):
        self.redis_cluster.delete(f"tweet:{tweet_id}")

        # Also invalidate timelines containing this tweet
        # (Usually done lazily)

    # Batch caching
    def mget_tweets(self, tweet_ids):
        pipeline = self.redis_cluster.pipeline()
        for tweet_id in tweet_ids:
            pipeline.hgetall(f"tweet:{tweet_id}")

        cached = pipeline.execute()

        tweets = []
        missing = []

        for i, data in enumerate(cached):
            if data:
                tweets.append(Tweet.from_dict(data))
            else:
                missing.append(tweet_ids[i])

        # Fetch missing from DB
        if missing:
            db_tweets = db.query(
                "SELECT * FROM tweets WHERE tweet_id IN (?)",
                missing
            )
            tweets.extend(db_tweets)

            # Cache for future
            for tweet in db_tweets:
                self.set_tweet_cache(tweet)

        return tweets
```

### E. Notification System

**Real-Time Push:**

```python
class NotificationService:
    def on_tweet_liked(self, tweet_id, liker_id):
        """Send notification when tweet is liked"""
        # Get tweet author
        tweet = self.get_tweet(tweet_id)

        # Don't notify self
        if tweet.user_id == liker_id:
            return

        # Check if already notified recently (debounce)
        recent_key = f"notif:like:{tweet_id}:{tweet.user_id}"
        if redis.exists(recent_key):
            # Add to aggregated notification
            redis.sadd(f"notif:likers:{tweet_id}", liker_id)
            return

        # Set debounce (don't send individual notifications for 5 min)
        redis.setex(recent_key, 300, "1")

        # Create notification
        notification = {
            'type': 'like',
            'tweet_id': tweet_id,
            'actor_id': liker_id,
            'recipient_id': tweet.user_id,
            'created_at': time.time()
        }

        # Store in DB
        db.insert("notifications", notification)

        # Send push notification
        self.send_push(tweet.user_id, {
            'title': f"@{liker.username} liked your tweet",
            'body': tweet.text[:100],
            'action': f"/tweets/{tweet_id}"
        })

        # Send WebSocket if user online
        if self.is_online(tweet.user_id):
            websocket.send(tweet.user_id, {
                'type': 'notification',
                'data': notification
            })

    def aggregate_notifications(self):
        """Periodically aggregate similar notifications"""
        # Run every 5 minutes
        # "Alice liked your tweet" + "Bob liked your tweet"
        # becomes "Alice, Bob and 3 others liked your tweet"

        # Implementation similar to Instagram
```

## 9. Data Flow

### Flow 1: User Creates a Tweet

```
1. User types tweet in mobile app (280 chars)
2. User attaches 2 images
3. App uploads images in parallel
   POST /api/v1/media/upload (x2)
4. App receives media_ids
5. User hits "Tweet" button
6. App sends tweet creation request
   POST /api/v1/tweets
   {
       "text": "Amazing sunset! #photography",
       "media_ids": ["media_123", "media_456"]
   }
7. Tweet Service:
   - Validates text length (<=280 chars)
   - Validates media exists
   - Generates unique tweet_id (Snowflake ID)
   - Inserts into PostgreSQL tweets table
   - Extracts entities (hashtags, mentions)
   - Inserts into tweet_entities table
8. Publishes event to Kafka:
   {
       "event": "tweet_created",
       "tweet_id": "1234567890",
       "user_id": "123",
       "timestamp": 1699876543
   }
9. Fanout Service (Kafka consumer):
   - Checks if user is celebrity (>1M followers)
   - If not: Fans out to all followers' timelines
   - Adds tweet_id to Redis sorted sets
10. Search Service (Kafka consumer):
    - Indexes tweet in Elasticsearch
    - Updates hashtag counts
11. Trending Service (Kafka consumer):
    - Updates hashtag trending scores
12. Notification Service (Kafka consumer):
    - Sends notifications to mentioned users
13. Returns success to client (200 OK)
    Total time: <100ms
```

### Flow 2: User Refreshes Home Timeline

```
1. User pulls down to refresh timeline
2. App requests timeline
   GET /api/v1/timelines/home?limit=20
3. API Gateway:
   - Authenticates JWT token
   - Routes to Timeline Service
4. Timeline Service:
   - Extracts user_id from token
   - Checks Redis cache: timeline:home:{user_id}
5. Cache HIT scenario:
   - Get top 20 tweet IDs from sorted set
   - Batch fetch tweet details from cache
   - For cache misses, fetch from PostgreSQL
   - Hydrate with user info, media URLs
   - Apply ranking algorithm (if not chronological)
   - Return to client
   Total time: ~50ms
6. Cache MISS scenario:
   - Get list of users current user follows
   - Check if following any celebrities
   - For regular users: pre-fanned-out tweets already in timeline
   - For celebrities: query their recent tweets from DB
   - Merge and rank all tweets
   - Store in Redis cache (TTL: 10 min)
   - Return to client
   Total time: ~300ms
7. Client receives tweets
8. Client lazy-loads images from CDN
   - First request goes to CDN edge
   - Edge caches for future requests
9. Client sends impression events (async)
   POST /api/v1/analytics/impressions
```

### Flow 3: Celebrity Tweets (Breaking News)

```
Example: President tweets, has 100M followers

1. Celebrity creates tweet
2. Tweet Service:
   - Inserts tweet into database
   - Publishes to Kafka
3. Fanout Service:
   - Detects user is celebrity
   - SKIPS fanout to all followers (would be 100M writes)
   - Instead, marks tweet as "celebrity tweet"
   - Caches tweet heavily in Redis
4. When followers request timeline:
   - Timeline Service detects they follow a celebrity
   - Queries celebrity's recent tweets (last 24 hours)
   - Merges with regular fanned-out tweets
   - Ranks and returns
5. Tweet goes viral:
   - 10M people view in first minute
   - All requests hit Redis cache
   - CDN serves media
   - Database load: minimal
6. Trending Service:
   - Detects spike in hashtag usage
   - Adds to trending topics
   - Updates every 30 seconds
```

### Flow 4: Real-Time Trending Calculation

```
1. Tweets stream into Kafka topic: "all_tweets"
2. Apache Flink/Storm Stream Processing:
   - Window: 5-minute sliding windows
   - Count hashtags in each window
   - Compare with historical baseline
3. Trending Score Calculation:
   score = (current_volume - expected_volume) / expected_volume
   - High score = trending
4. Filter:
   - Minimum 1000 tweets in window
   - Spike must be >300% of baseline
5. Store top 50 trending topics per region
6. Update Redis cache:
   Key: trending:{location_id}
   Value: JSON array of topics
   TTL: 5 minutes
7. API serves from Redis cache:
   GET /api/v1/trends/place?id=23424977
8. Update frequency: Every 30-60 seconds
```

## 10. Scalability Considerations

### Database Sharding

**Tweets Sharding:**
```
Shard by user_id (co-located with user data)

Shard 0: user_id % 100 == 0
Shard 1: user_id % 100 == 1
...
Shard 99: user_id % 100 == 99

Benefits:
- User's tweets on same shard (fast profile queries)
- User data and tweets together (JOIN friendly)

Tradeoffs:
- Uneven distribution (celebrities have more tweets)
- Cross-shard queries for timelines
```

**Timeline Sharding:**
```
Shard by user_id (different from tweets)

Each user's timeline on a specific shard
Fast timeline reads
Write amplification during fanout (distributed across shards)
```

### Handling Celebrity Problem

```python
# Tiered approach based on follower count

Tier 1: 0-10K followers
- Full fanout to all followers
- Pre-generate timelines

Tier 2: 10K-100K followers
- Fanout to active followers only
- On-demand generation for inactive followers

Tier 3: 100K-1M followers
- Fanout to recently active followers (last 7 days)
- Cache heavily
- On-demand for others

Tier 4: 1M+ followers (Celebrities)
- No fanout
- All followers pull on-demand
- Aggressive caching (Redis + CDN)
- Dedicated celebrity tweet cache
```

### Auto-Scaling

```yaml
# Different scaling policies for different services

Tweet Service:
- Scale on: Write QPS
- Min: 50 pods
- Max: 500 pods
- Target: 70% CPU

Timeline Service:
- Scale on: Read QPS
- Min: 200 pods
- Max: 2000 pods
- Target: 80% CPU

Fanout Service:
- Scale on: Kafka lag
- Min: 100 pods
- Max: 1000 pods
- Target: <10 seconds lag

Search Service:
- Scale on: Elasticsearch CPU
- Min: 50 pods
- Max: 200 pods

Trending Service:
- Fixed size (stream processing)
- Pods: 20 (fault-tolerant)
```

### Multi-Region Strategy

```
Primary Region: US-EAST
- Master database
- All writes go here
- Full services

Secondary Regions: EU-WEST, APAC
- Read replicas (< 100ms lag)
- Read-only operations
- Write operations proxied to primary
- Full cache cluster

Benefits:
- Low latency reads globally
- Data locality for compliance (GDPR)
- Disaster recovery

Failover:
- If primary fails, promote secondary to primary
- DNS update (<30 seconds)
- Accept writes in any region temporarily
- Reconcile later (conflict resolution)
```

### Rate Limiting

```python
class RateLimiter:
    # Different limits for different actions

    LIMITS = {
        'tweet_create': (50, 3600),      # 50 per hour
        'tweet_delete': (100, 3600),     # 100 per hour
        'follow': (400, 86400),          # 400 per day
        'like': (1000, 86400),           # 1000 per day
        'api_read': (15000, 900),        # 15K per 15 min
    }

    def check_rate_limit(self, user_id, action):
        limit, window = self.LIMITS[action]
        key = f"ratelimit:{action}:{user_id}"

        # Sliding window counter
        current = redis.incr(key)

        if current == 1:
            redis.expire(key, window)

        if current > limit:
            raise RateLimitExceeded(
                f"Rate limit exceeded: {current}/{limit}",
                retry_after=redis.ttl(key)
            )

        return True

# Also: IP-based rate limiting
# Prevents abuse from bots
```

## 11. Trade-offs

### 1. Fanout on Write vs. Fanout on Read

**Decision: Hybrid**

Regular users: Fanout on write
- Fast reads (pre-computed)
- Slow writes for users with many followers
- High storage (duplicated timeline data)

Celebrities: Fanout on read
- Fast writes (no fanout)
- Slower reads (query on-demand)
- Low storage (no duplication)

### 2. Timeline Ranking: Chronological vs. Algorithmic

**Decision: Offer both**

Chronological:
- Simple, predictable
- Users see everything
- No ML needed

Algorithmic:
- Better engagement
- Show "best" tweets first
- Requires ML models
- Can miss some tweets

Implementation: Default to algorithmic, allow users to switch

### 3. Elasticsearch vs. PostgreSQL Full-Text Search

**Decision: Elasticsearch**

| Aspect | PostgreSQL FTS | Elasticsearch |
|--------|---------------|---------------|
| Performance | Good for <1M docs | Excellent at any scale |
| Features | Basic | Advanced (fuzzy, boost) |
| Scalability | Vertical | Horizontal |
| Latency | <100ms | <50ms |
| Cost | Lower | Higher |

For Twitter scale, Elasticsearch is necessary

### 4. Message Queue: Kafka vs. RabbitMQ

**Decision: Kafka**

Kafka benefits:
- High throughput (millions/sec)
- Replay capability
- Distributed by design
- Event sourcing friendly

Twitter needs:
- Handle 500M tweets/day
- Multiple consumers per event
- Event replay for debugging

### 5. Media Storage: Self-hosted vs. Cloud

**Decision: Cloud (S3 + CloudFront)**

Self-hosted:
- Lower cost (long-term)
- Full control
- Operational burden

Cloud:
- Higher cost
- Auto-scaling
- Global CDN included
- 11 nines durability

For global scale, cloud is better

### 6. Trending Calculation: Exact vs. Approximate

**Decision: Approximate (HyperLogLog, Count-Min Sketch)**

Exact counting:
- Accurate
- Expensive (store every occurrence)
- Doesn't scale

Approximate:
- 99% accurate (good enough)
- Constant memory
- Scales to billions of events

### 7. Tweet Edit: Mutable vs. Immutable

**Decision: Immutable with history**

Store edit history in JSONB column
Show "Edited" label
Allow viewing previous versions
Prevents abuse (changing viral tweet meaning)

## 12. Follow-up Questions

### Functional

**Q1: How to implement tweet threading?**
A: Add `thread_id` to tweets table. First tweet generates thread_id, replies use same thread_id. Display in tree structure on frontend.

**Q2: How to handle tweet deletion?**
A: Soft delete (add `deleted_at` column). Remove from timelines immediately. Keep in DB for compliance (30 days). Remove from search index.

**Q3: How to implement polls in tweets?**
A: Create `polls` table (poll_id, tweet_id, duration). `poll_options` table. `poll_votes` table (user_id, option_id). Update counts in real-time.

**Q4: How to add Twitter Spaces (audio chat)?**
A: Separate service with WebRTC. Agora/Twilio for infrastructure. Real-time participant list. Recording storage in S3.

### Scale

**Q5: How to handle 1 million tweets/second?**
A:
- Kafka can handle (proven at this scale)
- 1000+ database shards
- Delay fanout (queue-based, eventual consistency)
- Aggressive caching
- CDN for all media

**Q6: How to optimize timeline generation for users following 5000+ people?**
A:
- Don't generate complete timeline
- Sample tweets from most engaged-with users
- Use ML to predict which tweets user will like
- Pre-compute during off-peak hours

**Q7: How to make search real-time (tweets appear in search within seconds)?**
A:
- Elasticsearch with near-real-time indexing
- Bulk indexing every 1 second
- In-memory buffer for immediate search
- Hot/warm/cold index architecture

### Reliability

**Q8: What if Kafka goes down?**
A:
- Kafka cluster with replication (3 replicas)
- ZooKeeper/KRaft for coordination
- Circuit breaker to database if queue fails
- Buffer tweets in API layer temporarily

**Q9: How to handle database failover?**
A:
- Master-slave replication
- Automatic failover (Patroni, ProxySQL)
- Failover time: <30 seconds
- Read replicas keep serving reads

**Q10: How to prevent spam bots?**
A:
- Rate limiting (50 tweets/hour)
- CAPTCHA on registration
- Phone verification
- ML models for spam detection
- Shadowban suspicious accounts
- Monitor for abnormal patterns

### Advanced

**Q11: How to implement verified accounts (blue check)?**
A: Add `is_verified` boolean to users table. Manual verification process. Show badge in UI. Prioritize in search.

**Q12: How would you add Twitter Blue (edit tweets, undo send)?**
A:
- Undo send: Delay tweet publication by 30 seconds
- Edit tweets: Version history (already covered)
- Longer tweets: Increase char limit for premium users

**Q13: How to detect and remove abusive content?**
A:
- User reporting system
- ML model for abuse detection
- Image/video scanning (AWS Rekognition)
- Human moderation team for edge cases
- Quarantine suspicious content

**Q14: How to implement Twitter Analytics?**
A:
- Time-series database (InfluxDB, TimescaleDB)
- Track: views, engagements, clicks, profile visits
- Batch processing (Spark) for historical data
- Real-time dashboard (Grafana)

**Q15: How to add direct messaging?**
A: (See Instagram DM design - similar approach)
- Separate service with WebSockets
- Cassandra for message storage
- End-to-end encryption
- Read receipts
- Message reactions

---

**Estimated Interview Time:** 60-75 minutes

**Key Learning Points:**
- Hybrid fanout strategy for feed generation
- Handling celebrity/hotspot problem
- Real-time trending algorithms
- Search at scale with Elasticsearch
- Event-driven architecture with Kafka
- Multi-level caching strategy
- Rate limiting and abuse prevention

**Difficulty:** Medium (requires understanding of distributed systems and real-time processing)
