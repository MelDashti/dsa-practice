# Design Instagram (Full Featured)

## 1. Problem Statement & Scope

Design a complete photo and video sharing social media platform similar to Instagram with advanced features including stories, recommendations, direct messaging, and real-time notifications.

### In Scope:
- User registration, authentication, and profiles
- Photo and video uploads (posts and stories)
- Feed generation with algorithmic ranking
- Stories (24-hour ephemeral content)
- Explore page with personalized recommendations
- Direct messaging (DMs)
- Likes, comments, and saves
- Following/followers system
- Search (users, hashtags, locations)
- Real-time notifications
- Activity status
- Video support (Reels)

### Out of Scope:
- Shopping and e-commerce features
- AR filters and effects
- Live streaming (Instagram Live)
- Professional business accounts analytics
- Ads platform
- Content moderation details (assume exists)

### Scale:
- 500 million daily active users (DAU)
- 2 billion total users
- 100 million photos/videos uploaded daily
- Average 30 stories per second during peak hours
- 5 billion likes per day
- Read:Write ratio of 100:1

## 2. Functional Requirements

### High Priority (P0):

**FR1: User Management**
- Register, login, logout with email/phone
- Profile management (bio, profile picture, website)
- Privacy settings (public/private accounts)
- Follow/unfollow users
- Block users

**FR2: Content Posting**
- Upload photos (up to 10 per post)
- Upload videos (up to 60 seconds)
- Add captions, location tags, user tags
- Edit and delete own posts

**FR3: Stories**
- Upload photos/videos as stories
- View stories from followed users
- Stories expire after 24 hours
- Story viewers list
- Story highlights (permanent stories on profile)

**FR4: Feed**
- Home feed with algorithmic ranking
- Chronological feed option
- Explore page with personalized content
- Profile view showing user's posts

**FR5: Engagement**
- Like/unlike posts and stories
- Comment on posts
- Save posts to collections
- Share posts via DM

**FR6: Direct Messaging**
- One-on-one messaging
- Group messaging
- Send photos, videos, posts
- Message reactions
- Message search

**FR7: Notifications**
- Real-time notifications for likes, comments, follows
- Push notifications
- In-app notification center

### Medium Priority (P1):

**FR8: Search and Discovery**
- Search users by username
- Search hashtags
- Search locations
- Trending hashtags

**FR9: Activity Status**
- Show when users are online
- Last seen timestamp

**FR10: Reels**
- Short-form videos (15-90 seconds)
- Dedicated Reels feed
- Audio library

## 3. Non-Functional Requirements (Scale, Performance, Availability)

### Scale Requirements:
- **Daily Active Users:** 500 million
- **Total Users:** 2 billion
- **Posts per day:** 100 million
- **Stories per day:** 500 million
- **Messages per day:** 10 billion
- **Peak QPS:** 500,000 requests/second
- **Concurrent users:** 100 million

### Performance Requirements:
- **Feed load time:** < 500ms (p95)
- **Story load time:** < 300ms (p95)
- **Image upload:** < 3 seconds for 10MB
- **Video upload:** < 30 seconds for 1GB
- **Message delivery:** < 100ms (real-time)
- **Notification delivery:** < 1 second
- **Search response:** < 200ms

### Availability:
- **Service availability:** 99.99% (52 minutes downtime/year)
- **Data durability:** 99.999999999% (11 nines)
- **Regional failover:** < 30 seconds

### Consistency:
- **Feeds:** Eventual consistency (1-2 seconds)
- **Messages:** Strong consistency
- **Likes/Comments:** Eventual consistency
- **User profile:** Strong consistency

### Security:
- End-to-end encryption for DMs
- HTTPS for all connections
- Rate limiting per user and IP
- Content scanning for abuse

## 4. Back-of-envelope Calculations

### Storage Calculations:

**Photo Storage:**
- Photos per day: 70M (70% of 100M posts)
- Average photo size: 2MB (compressed)
- Multiple sizes: original (2MB), medium (500KB), thumbnail (50KB)
- Daily storage: 70M × (2MB + 0.5MB + 0.05MB) = 178.5 TB/day
- Storage per year: 178.5 TB × 365 = ~65 PB/year

**Video Storage:**
- Videos per day: 30M (30% of 100M posts)
- Average video size: 30MB (30 seconds at various qualities)
- Daily storage: 30M × 30MB = 900 TB/day
- With multiple quality levels (4K, 1080p, 720p, 480p): 900 TB × 4 = 3.6 PB/day
- Storage per year: 3.6 PB × 365 = ~1.3 EB/year

**Stories Storage:**
- Stories per day: 500M
- Average story size: 5MB (mix of photo and video)
- Daily storage: 500M × 5MB = 2.5 PB/day
- Since stories expire after 24 hours: 2.5 PB × 2 (redundancy) = 5 PB buffer

**Messages Storage:**
- Messages per day: 10B
- Average message size: 500 bytes (text)
- Daily storage: 10B × 500B = 5 TB/day
- Storage per year: 5 TB × 365 = 1.8 PB/year

**Metadata Storage:**
- Users: 2B × 5KB = 10 TB
- Posts: 100M × 365 × 2KB = 73 PB/year
- Likes: 5B × 50 bytes = 250 GB/day = 91 TB/year
- Comments: 500M × 500 bytes = 250 GB/day = 91 TB/year

**Total Storage (Year 1):** ~1.5 EB (Exabytes)

### Bandwidth Calculations:

**Incoming (Upload):**
- Photos: 178.5 TB/day ÷ 86,400s = ~2 GB/s
- Videos: 900 TB/day ÷ 86,400s = ~10 GB/s
- Stories: 2.5 PB/day ÷ 86,400s = ~29 GB/s
- Peak (3x): ~123 GB/s upload bandwidth

**Outgoing (Download):**
- Assume each user views 100 images/videos per day
- 500M users × 100 views = 50B views/day
- Average size: 500KB (mix of images and videos)
- 50B × 500KB = 25 EB/day (!!)
- Per second: 25 EB ÷ 86,400s = ~289 TB/s
- Peak (3x): ~867 TB/s

**CDN is absolutely critical** - Will serve 99% of read traffic

### Compute Requirements:

**API Servers:**
- 500K QPS peak
- Each server handles 1K QPS
- Need: 500 servers (with redundancy: 1000 servers)

**Database Servers:**
- Write QPS: 500K ÷ 100 = 5K QPS
- Read QPS: 495K QPS (99% served by cache)
- Database QPS: ~50K (1% cache misses)
- Sharded across 100 database nodes

**Cache Servers:**
- Cache 99% of reads
- Working set: ~100 TB (hot data)
- Redis cluster: 500 nodes × 200 GB = 100 TB

## 5. High-Level Architecture Diagram Description

```
                            [Mobile Apps / Web Clients]
                                        |
                                        v
                            [Global DNS / Route 53]
                                        |
                +-----------------------+-----------------------+
                |                       |                       |
            [US Region]            [EU Region]            [APAC Region]
                |                       |                       |
                v                       v                       v
        [CloudFront CDN] -------- [CloudFront CDN] ------- [CloudFront CDN]
        (Images, Videos)          (Images, Videos)        (Images, Videos)
                |                       |                       |
                v                       v                       v
        [Load Balancer]           [Load Balancer]         [Load Balancer]
                |                       |                       |
                +------------- API Gateway Layer --------------+
                                        |
                +----------+------------+------------+-----------+
                |          |            |            |           |
                v          v            v            v           v
        [User      [Post       [Feed       [Message    [Notification
         Service]   Service]    Service]    Service]    Service]
                |          |            |            |           |
                v          v            v            v           v
        +-------+----------+------------+------------+-----------+-------+
        |                                                                |
        v                                                                v
[Service Mesh / Message Bus - Kafka]                          [WebSocket Servers]
        |                                                                |
        +----------+------------+------------+-----------+               |
                   |            |            |           |               |
                   v            v            v           v               v
           [Cache Layer - Redis Cluster (100TB)]    [Real-time Status]
                   |            |            |
                   v            v            v
    [PostgreSQL Cluster] [Cassandra]  [Elasticsearch]
    (Users, Posts)       (Messages,   (Search Index)
                         Stories)
                   |            |
                   v            v
            [S3 / Object Storage] ----> [CDN]
            (Images, Videos)
                   |
                   v
        [Video Transcoding Pipeline]
        (FFmpeg, Elastic Transcoder)
                   |
                   v
        [ML Services]
        (Recommendations, Content Moderation)
```

### Regional Architecture:

Each region contains:
- API Gateway cluster
- Microservices (User, Post, Feed, Message, Notification)
- Redis cache cluster
- Database read replicas
- S3 storage with cross-region replication

### Service Communication:

- **Synchronous:** gRPC for inter-service calls
- **Asynchronous:** Kafka for events
- **Real-time:** WebSockets for messaging and notifications

## 6. API Design (RESTful endpoints)

### User Service APIs

```
POST /api/v1/users/register
POST /api/v1/users/login
GET /api/v1/users/{user_id}
PUT /api/v1/users/{user_id}
DELETE /api/v1/users/{user_id}

POST /api/v1/users/{user_id}/follow
DELETE /api/v1/users/{user_id}/unfollow
GET /api/v1/users/{user_id}/followers
GET /api/v1/users/{user_id}/following

POST /api/v1/users/{user_id}/block
GET /api/v1/users/search?q={query}&limit=20
```

### Post Service APIs

```
POST /api/v1/posts
Request: multipart/form-data
{
  "images": [<file1>, <file2>],
  "caption": "Amazing view!",
  "location": "Paris, France",
  "tagged_users": ["user123", "user456"]
}

GET /api/v1/posts/{post_id}
PUT /api/v1/posts/{post_id}
DELETE /api/v1/posts/{post_id}

POST /api/v1/posts/{post_id}/like
DELETE /api/v1/posts/{post_id}/unlike

POST /api/v1/posts/{post_id}/comments
GET /api/v1/posts/{post_id}/comments?limit=50&offset=0
DELETE /api/v1/comments/{comment_id}

POST /api/v1/posts/{post_id}/save
DELETE /api/v1/posts/{post_id}/unsave
GET /api/v1/users/{user_id}/saved
```

### Feed Service APIs

```
GET /api/v1/feed/home?limit=20&cursor={cursor}
Response:
{
  "posts": [...],
  "next_cursor": "eyJwb3N0X2lkIjo...",
  "has_more": true
}

GET /api/v1/feed/explore?limit=20&cursor={cursor}
GET /api/v1/feed/user/{user_id}?limit=20&cursor={cursor}
GET /api/v1/feed/hashtag/{hashtag}?limit=20&cursor={cursor}
```

### Story Service APIs

```
POST /api/v1/stories
Request: multipart/form-data
{
  "media": <file>,
  "type": "image",  // or "video"
  "duration": 5     // seconds (for video)
}

GET /api/v1/stories/feed
Response:
{
  "story_rings": [
    {
      "user_id": "123",
      "username": "john_doe",
      "profile_pic": "...",
      "has_unseen": true,
      "stories": [
        {
          "story_id": "789",
          "media_url": "...",
          "type": "image",
          "created_at": "...",
          "expires_at": "..."
        }
      ]
    }
  ]
}

GET /api/v1/stories/{story_id}
DELETE /api/v1/stories/{story_id}
GET /api/v1/stories/{story_id}/viewers

POST /api/v1/stories/{story_id}/view
POST /api/v1/stories/{story_id}/like

POST /api/v1/highlights
GET /api/v1/users/{user_id}/highlights
```

### Message Service APIs

```
POST /api/v1/messages/threads
Request:
{
  "participants": ["user123", "user456"],
  "is_group": false
}

GET /api/v1/messages/threads
Response:
{
  "threads": [
    {
      "thread_id": "abc123",
      "participants": [...],
      "last_message": {...},
      "unread_count": 5,
      "updated_at": "..."
    }
  ]
}

GET /api/v1/messages/threads/{thread_id}?limit=50&cursor={cursor}

POST /api/v1/messages
Request:
{
  "thread_id": "abc123",
  "message_type": "text",
  "content": "Hello!",
  "reply_to": null  // optional
}

DELETE /api/v1/messages/{message_id}
POST /api/v1/messages/{message_id}/react
```

### Notification Service APIs

```
GET /api/v1/notifications?limit=50&offset=0
Response:
{
  "notifications": [
    {
      "notification_id": "123",
      "type": "like",
      "actor": {"user_id": "456", "username": "jane"},
      "post": {"post_id": "789", "thumbnail": "..."},
      "is_read": false,
      "created_at": "..."
    }
  ],
  "unread_count": 15
}

PUT /api/v1/notifications/{notification_id}/read
PUT /api/v1/notifications/read-all
```

### Search Service APIs

```
GET /api/v1/search/users?q={query}&limit=20
GET /api/v1/search/hashtags?q={query}&limit=20
GET /api/v1/search/locations?q={query}&limit=20
GET /api/v1/search/top?q={query}&limit=20
```

### WebSocket APIs

```
WS /ws/messages
Events:
- new_message
- message_delivered
- message_read
- user_typing

WS /ws/notifications
Events:
- new_notification
- notification_read

WS /ws/stories
Events:
- new_story (from followed users)
- story_expired
```

## 7. Database Design (Schema, Indexes)

### PostgreSQL (Users, Posts, Relationships)

```sql
-- Users Table (Sharded by user_id)
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    profile_pic_url VARCHAR(500),
    website VARCHAR(200),
    is_verified BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    posts_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);

-- Posts Table (Sharded by user_id)
CREATE TABLE posts (
    post_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    caption TEXT,
    location VARCHAR(200),
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    shares_count INT DEFAULT 0,
    saves_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id, created_at DESC);
CREATE INDEX idx_posts_location ON posts(location);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- Post Media Table
CREATE TABLE post_media (
    media_id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    media_type VARCHAR(10) NOT NULL, -- 'image', 'video'
    media_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    width INT,
    height INT,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_post_media_post_id ON post_media(post_id, display_order);

-- Followers (Sharded by follower_id)
CREATE TABLE followers (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_followers_followee ON followers(followee_id);

-- Likes (Sharded by post_id)
CREATE TABLE likes (
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id)
);

CREATE INDEX idx_likes_post_id ON likes(post_id, created_at DESC);
CREATE INDEX idx_likes_user_id ON likes(user_id, created_at DESC);

-- Comments (Sharded by post_id)
CREATE TABLE comments (
    comment_id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    parent_comment_id BIGINT,  -- for nested replies
    text TEXT NOT NULL,
    likes_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post ON comments(post_id, created_at DESC);
CREATE INDEX idx_comments_parent ON comments(parent_comment_id);

-- Saved Posts
CREATE TABLE saved_posts (
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    collection_id BIGINT,  -- optional collection
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id)
);

-- Tagged Users
CREATE TABLE post_tags (
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    x_coordinate FLOAT,  -- position in image
    y_coordinate FLOAT,
    PRIMARY KEY (post_id, user_id)
);

-- Hashtags
CREATE TABLE hashtags (
    hashtag_id BIGSERIAL PRIMARY KEY,
    hashtag VARCHAR(100) UNIQUE NOT NULL,
    posts_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hashtags_name ON hashtags(hashtag);

CREATE TABLE post_hashtags (
    post_id BIGINT NOT NULL,
    hashtag_id BIGINT NOT NULL,
    PRIMARY KEY (post_id, hashtag_id)
);

CREATE INDEX idx_post_hashtags_hashtag ON post_hashtags(hashtag_id);
```

### Cassandra (Stories, Messages - High Write Throughput)

```cql
-- Stories (TTL = 24 hours)
CREATE TABLE stories (
    user_id BIGINT,
    story_id TIMEUUID,
    media_url TEXT,
    thumbnail_url TEXT,
    media_type TEXT,
    duration INT,
    views_count COUNTER,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    PRIMARY KEY (user_id, story_id)
) WITH CLUSTERING ORDER BY (story_id DESC)
  AND default_time_to_live = 86400;

-- Story Views
CREATE TABLE story_views (
    story_id TIMEUUID,
    viewer_id BIGINT,
    viewed_at TIMESTAMP,
    PRIMARY KEY (story_id, viewer_id)
);

-- Messages (Partitioned by thread_id)
CREATE TABLE messages (
    thread_id UUID,
    message_id TIMEUUID,
    sender_id BIGINT,
    message_type TEXT,  -- 'text', 'image', 'video', 'post'
    content TEXT,
    media_url TEXT,
    reply_to TIMEUUID,
    is_deleted BOOLEAN,
    created_at TIMESTAMP,
    PRIMARY KEY (thread_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);

-- Message Threads
CREATE TABLE message_threads (
    thread_id UUID PRIMARY KEY,
    participant_ids SET<BIGINT>,
    is_group BOOLEAN,
    thread_name TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- User Inbox (for each user's threads)
CREATE TABLE user_message_threads (
    user_id BIGINT,
    thread_id UUID,
    last_message_id TIMEUUID,
    last_message_preview TEXT,
    unread_count INT,
    updated_at TIMESTAMP,
    PRIMARY KEY (user_id, updated_at, thread_id)
) WITH CLUSTERING ORDER BY (updated_at DESC);
```

### Redis Cache Structures

```
# User Profile Cache
Key: user:{user_id}
Type: Hash
TTL: 1 hour
Fields: {username, full_name, profile_pic_url, followers_count, ...}

# Feed Cache (pre-generated)
Key: feed:{user_id}
Type: Sorted Set (score = timestamp)
TTL: 10 minutes
Members: post_ids

# Story Rings Cache
Key: stories:feed:{user_id}
Type: List
TTL: 5 minutes
Data: JSON array of story rings

# Following List Cache
Key: following:{user_id}
Type: Set
TTL: 1 hour
Members: user_ids

# Post Cache
Key: post:{post_id}
Type: Hash
TTL: 30 minutes

# Like Count Cache
Key: likes:{post_id}
Type: String (counter)
TTL: No expiry
Update: INCR/DECR

# Online Users
Key: online_users
Type: Sorted Set (score = last_active_timestamp)
TTL: No expiry
Cleanup: Remove entries older than 15 minutes

# Session Cache
Key: session:{token}
Type: Hash
TTL: 7 days
```

### Elasticsearch (Search)

```json
{
  "users_index": {
    "mappings": {
      "properties": {
        "user_id": {"type": "long"},
        "username": {"type": "keyword"},
        "full_name": {"type": "text"},
        "bio": {"type": "text"},
        "followers_count": {"type": "integer"},
        "is_verified": {"type": "boolean"}
      }
    }
  },
  "hashtags_index": {
    "mappings": {
      "properties": {
        "hashtag": {"type": "keyword"},
        "posts_count": {"type": "integer"},
        "trending_score": {"type": "float"}
      }
    }
  }
}
```

## 8. Core Components

### A. Feed Generation Service

**Challenge:** Generate personalized feed for 500M users with low latency

**Architecture:**

```
Feed Request -> Check Cache -> [Cache Hit] -> Return Feed
                     |
                [Cache Miss]
                     v
            Offline Ranking Service
                     |
        +------------+------------+
        |            |            |
        v            v            v
   [Get Posts]  [ML Model]  [Business Rules]
   from followed               |
   users         Rank posts by:
                 - Recency
                 - Engagement (likes, comments)
                 - User affinity
                 - Content type preference
                 - Time spent prediction
                     |
                     v
              Store in Cache -> Return Feed
```

**Implementation:**

1. **Offline Feed Generation (Fanout on Write):**
   ```python
   # When user creates post
   def on_new_post(post_id, user_id):
       # Get followers (from cache or DB)
       follower_ids = get_followers(user_id)

       # Fanout only to active users (not all followers)
       active_followers = filter_active_users(follower_ids)

       # Add to each follower's feed cache
       for follower_id in active_followers:
           redis.zadd(f"feed:{follower_id}",
                     {post_id: current_timestamp()})
           # Keep only recent 500 posts
           redis.zremrangebyrank(f"feed:{follower_id}", 0, -501)

       # For inactive users, generate feed on-demand
   ```

2. **Online Feed Ranking:**
   ```python
   def get_ranked_feed(user_id, limit=20):
       # Get candidate posts from cache
       candidate_post_ids = redis.zrevrange(
           f"feed:{user_id}", 0, 100)

       # Fetch post details
       posts = batch_get_posts(candidate_post_ids)

       # Apply ML ranking
       ranked_posts = ml_ranker.rank(
           posts=posts,
           user_id=user_id,
           context={
               'time_of_day': current_hour(),
               'user_engagement_history': get_user_history(user_id)
           }
       )

       return ranked_posts[:limit]
   ```

3. **Ranking Algorithm:**
   ```python
   def calculate_post_score(post, user_context):
       score = 0

       # Recency score (decay over time)
       age_hours = (now() - post.created_at).hours
       recency_score = 1 / (1 + age_hours / 24)
       score += recency_score * 0.3

       # Engagement score
       engagement_rate = (post.likes_count + post.comments_count * 2) \
                        / max(1, post.author_followers_count)
       score += min(engagement_rate, 1.0) * 0.25

       # User affinity (how often user interacts with author)
       affinity = get_user_affinity(user_id, post.author_id)
       score += affinity * 0.2

       # Content type preference
       content_pref = user_context.content_type_preferences.get(
           post.media_type, 0.5)
       score += content_pref * 0.15

       # Diversity (penalize similar content)
       if recently_shown_similar_content(user_id, post):
           score *= 0.7

       # Predicted engagement (ML model)
       predicted_engagement = ml_model.predict(user_id, post_id)
       score += predicted_engagement * 0.1

       return score
   ```

**Hybrid Approach for Celebrities:**
- Regular users: Fanout on write
- Celebrities (>1M followers): Fanout on read
- Mix both in feed generation

### B. Media Storage

**Video Processing Pipeline:**

```
Upload -> S3 Upload -> Lambda Trigger -> Transcoding Queue
                                              |
                                              v
                                    Elastic Transcoder
                                    /      |      \
                                   /       |       \
                              4K        1080p     720p    480p
                               |         |        |        |
                               +-------- + --------+--------+
                                              |
                                              v
                                     S3 (Multiple Qualities)
                                              |
                                              v
                                       CloudFront CDN
```

**Adaptive Bitrate Streaming:**
- Use HLS (HTTP Live Streaming) or DASH
- Client automatically switches quality based on bandwidth
- Generate m3u8 playlist files

**Storage Optimization:**
```python
class MediaStorageService:
    def upload_image(self, image_file, user_id):
        # Generate unique ID
        media_id = generate_id()

        # Create multiple sizes
        sizes = {
            'original': resize(image_file, max_size=2048),
            'large': resize(image_file, size=1080),
            'medium': resize(image_file, size=640),
            'thumbnail': resize(image_file, size=150)
        }

        # Optimize and upload
        urls = {}
        for size_name, image in sizes.items():
            # Compress
            compressed = optimize_jpeg(image, quality=85)

            # Upload to S3
            key = f"{user_id}/{media_id}_{size_name}.jpg"
            s3.upload(key, compressed)

            # Get CDN URL
            urls[size_name] = get_cdn_url(key)

        return urls

    def upload_video(self, video_file, user_id):
        media_id = generate_id()

        # Upload original to S3
        original_key = f"{user_id}/{media_id}_original.mp4"
        s3.upload(original_key, video_file)

        # Publish to transcoding queue
        transcoding_queue.publish({
            'media_id': media_id,
            'source_key': original_key,
            'output_formats': ['4k', '1080p', '720p', '480p']
        })

        # Return immediately with pending status
        return {
            'media_id': media_id,
            'status': 'processing',
            'thumbnail_url': generate_thumbnail(video_file)
        }
```

**Storage Tiers:**
```
Hot (Recent 30 days):    S3 Standard
Warm (30-180 days):      S3 Intelligent-Tiering
Cold (180+ days):        S3 Glacier
Very Cold (1+ year):     S3 Deep Glacier
```

### C. CDN Integration

**Multi-CDN Strategy:**

Primary: CloudFront (AWS)
Secondary: Cloudflare (failover)
Tertiary: Akamai (for specific regions)

**CDN Configuration:**
```nginx
# Cache-Control headers
Cache-Control: public, max-age=31536000, immutable  # Images/Videos
Cache-Control: public, max-age=300                   # Stories
Cache-Control: no-cache                              # User profiles

# Origin failover
origin_group {
    origin primary {
        domain: s3-us-east-1.amazonaws.com
    }
    origin secondary {
        domain: s3-eu-west-1.amazonaws.com
    }
    failover_criteria: [500, 502, 503, 504]
}

# Image optimization at edge
cloudflare_polish: lossless
auto_minify: on
```

**Smart Image Delivery:**
```
Client Request: /image/12345.jpg
                    |
                    v
        CDN checks User-Agent
                    |
        +-----------+-----------+
        |           |           |
    Mobile      Desktop      Slow
     (3G)                    Connection
        |           |           |
        v           v           v
   640x640     1080x1080    480x480
   WebP/AVIF    JPG         JPG (low quality)
```

### D. Cache Layer

**Multi-Layer Caching Strategy:**

```
L1: Application Memory (In-Process Cache)
    - Recent user sessions
    - Hot configuration
    - TTL: 1 minute
    - Size: 100MB per server

L2: Redis Cluster (Distributed Cache)
    - Feeds, user profiles, posts
    - TTL: 5-60 minutes
    - Size: 100 TB across cluster

L3: Database Query Cache
    - Query result caching
    - TTL: Variable
    - Size: Managed by DB

L4: CDN Edge Cache
    - Media files
    - TTL: 1 year (immutable)
    - Size: Petabytes globally
```

**Cache Invalidation Strategy:**

```python
class CacheInvalidator:
    def on_user_update(self, user_id):
        # Invalidate user cache
        redis.delete(f"user:{user_id}")

        # Invalidate feeds of followers
        followers = get_followers(user_id)
        for follower_id in followers[:1000]:  # Limit
            redis.delete(f"feed:{follower_id}")

        # Publish event for other services
        kafka.publish("user_updated", {
            "user_id": user_id,
            "timestamp": now()
        })

    def on_new_post(self, post_id, user_id):
        # Don't cache yet (will be cached on first read)
        pass

    def on_post_update(self, post_id):
        # Invalidate post cache
        redis.delete(f"post:{post_id}")

        # Invalidate feeds containing this post
        # (done lazily - stale data acceptable)

    def on_like(self, post_id, user_id):
        # Update counter in cache (eventual consistency)
        redis.incr(f"likes:{post_id}")

        # Debounced update to database
        update_queue.publish({
            "post_id": post_id,
            "action": "increment_likes"
        })
```

### E. Notification System

**Real-Time Push Architecture:**

```
[Event Source] -> [Kafka] -> [Notification Service] -> [Push Gateway]
                                        |                     |
                                        v                     v
                                [Notification DB]    [APNs/FCM/WebSocket]
                                                              |
                                                              v
                                                        [User Devices]
```

**Implementation:**

```python
class NotificationService:
    def send_notification(self, user_id, notification_type, data):
        # Create notification record
        notification = {
            'notification_id': generate_id(),
            'user_id': user_id,
            'type': notification_type,  # like, comment, follow, mention
            'data': data,
            'is_read': False,
            'created_at': now()
        }

        # Store in database
        db.insert('notifications', notification)

        # Update unread count in cache
        redis.incr(f"notifications:unread:{user_id}")

        # Send push notification
        self.send_push(user_id, notification)

        # Send WebSocket event (if user online)
        if self.is_user_online(user_id):
            websocket_server.send(user_id, {
                'type': 'new_notification',
                'data': notification
            })

    def send_push(self, user_id, notification):
        # Get user's device tokens
        devices = db.query("""
            SELECT device_token, platform
            FROM user_devices
            WHERE user_id = ? AND push_enabled = TRUE
        """, user_id)

        # Format notification
        title, body = self.format_notification(notification)

        # Send to each device
        for device in devices:
            if device.platform == 'ios':
                apns.send(device.device_token, title, body)
            elif device.platform == 'android':
                fcm.send(device.device_token, title, body)

    def format_notification(self, notification):
        templates = {
            'like': "{actor} liked your post",
            'comment': "{actor} commented: {preview}",
            'follow': "{actor} started following you",
            'mention': "{actor} mentioned you in a comment"
        }

        template = templates[notification.type]
        return template.format(**notification.data)
```

**Notification Aggregation:**
```python
# Instead of "Alice liked your post", "Bob liked your post"
# Show "Alice, Bob and 10 others liked your post"

def aggregate_notifications(user_id):
    recent = db.query("""
        SELECT type, entity_id, COUNT(*) as count,
               array_agg(actor_id) as actors
        FROM notifications
        WHERE user_id = ?
          AND created_at > NOW() - INTERVAL '1 hour'
          AND is_read = FALSE
        GROUP BY type, entity_id
    """, user_id)

    aggregated = []
    for group in recent:
        if group.count > 1:
            aggregated.append({
                'type': group.type,
                'actors': group.actors[:3],
                'total_count': group.count
            })
    return aggregated
```

## 9. Data Flow

### Flow 1: User Uploads Post with Multiple Photos

```
1. User selects 5 photos in mobile app
2. App compresses images locally (2MB each)
3. App requests upload URLs
   POST /api/v1/posts/upload-urls
   {
       "media_count": 5,
       "media_types": ["image", "image", "image", "image", "image"]
   }
4. API returns presigned S3 URLs
5. App uploads directly to S3 (parallel uploads)
6. App confirms upload and creates post
   POST /api/v1/posts
   {
       "media_keys": ["s3://bucket/temp/..."],
       "caption": "Amazing trip!",
       "location": "Tokyo, Japan",
       "tagged_users": ["user123"]
   }
7. Post Service:
   - Validates media files exist in S3
   - Generates post_id
   - Inserts post record in PostgreSQL
   - Inserts media records
   - Publishes event to Kafka: "post_created"
8. Image Processing Workers:
   - Subscribe to "post_created" events
   - Download original images from S3
   - Generate resized versions (large, medium, thumbnail)
   - Upload to permanent S3 location
   - Update media URLs in database
9. Feed Service (subscribes to "post_created"):
   - Get followers of post author
   - Add post to followers' feed caches (fanout)
   - For users following >1000 people, skip (will generate on-demand)
10. Notification Service:
    - Send notification to tagged users
11. Search Service:
    - Extract hashtags from caption
    - Update Elasticsearch index
12. Return success to client
```

### Flow 2: User Opens App and Views Feed

```
1. App launches and requests feed
   GET /api/v1/feed/home?limit=20
2. API Gateway routes to Feed Service
3. Feed Service:
   - Validates JWT token
   - Extracts user_id
4. Check Redis cache
   Key: feed:{user_id}
5. If cache HIT:
   - Get post_ids from sorted set (top 20)
   - Batch fetch post details from cache
   - If post cache miss, fetch from PostgreSQL
   - Return feed [50ms response time]
6. If cache MISS:
   - Get list of followed users from cache/DB
   - Query recent posts from followed users
   - Apply ML ranking algorithm
   - Store ranked post IDs in cache (TTL: 10 min)
   - Fetch post details
   - Return feed [300ms response time]
7. Client receives feed JSON
8. Client requests images in parallel
   - Thumbnail first (150x150)
   - Then medium (640x640) as user scrolls
9. CDN serves images from nearest edge location
10. Client tracks impressions and sends analytics
    POST /api/v1/analytics/impressions
    {
        "post_ids": [123, 456, 789],
        "scroll_depth": 0.6
    }
```

### Flow 3: User Views Stories

```
1. User taps on story ring
2. App requests stories
   GET /api/v1/stories/{user_id}
3. Story Service:
   - Query Cassandra for user's active stories
   - Filter expired stories (>24 hours)
4. Return stories ordered by creation time
5. Client displays first story
6. Client preloads next 3 stories in background
7. User views story (auto-advances every 5 seconds)
8. Client sends view event
   POST /api/v1/stories/{story_id}/view
9. Story Service:
   - Increment view counter in Cassandra
   - Record viewer in story_views table
   - Send notification to story author (async)
10. After 24 hours:
    - Cassandra auto-deletes story (TTL)
    - CDN cache expires
```

### Flow 4: User Sends Direct Message

```
1. User types message and hits send
2. App optimistically shows message as "sending"
3. App sends WebSocket message
   WS -> {
       "action": "send_message",
       "thread_id": "abc123",
       "content": "Hello!",
       "client_msg_id": "xyz789"
   }
4. WebSocket server receives message
5. Message Service:
   - Validates user is participant in thread
   - Generates message_id (TIMEUUID)
   - Inserts message in Cassandra
   - Updates thread last_message in cache
   - Increments unread count for recipients
6. Publish to Kafka: "message_sent"
7. WebSocket server sends to online recipients
   WS -> {
       "action": "new_message",
       "thread_id": "abc123",
       "message": {...},
       "sender": {...}
   }
8. Push Notification Service:
   - Checks if recipients are online
   - Sends push to offline users
9. Client receives WebSocket event
   - Updates UI
   - Marks original message as "delivered"
10. Recipient's app sends read receipt
    WS -> {
        "action": "mark_read",
        "thread_id": "abc123",
        "message_id": "..."
    }
11. Sender receives read receipt
    - Updates UI to show "Seen"
```

## 10. Scalability Considerations

### Database Sharding Strategy

**User Data Sharding (by user_id):**
```
Shard 0: user_id % 100 == 0
Shard 1: user_id % 100 == 1
...
Shard 99: user_id % 100 == 99
```

**Post Data Sharding (by user_id, co-located with user):**
- Keeps user's posts on same shard
- Efficient for profile queries
- Cross-shard queries needed for feeds

**Relationship Sharding (two copies):**
```
Following shard (by follower_id):
- Shard(follower_id) stores (follower_id, followee_id)
- Efficient for "who does Alice follow?"

Followers shard (by followee_id):
- Shard(followee_id) stores (follower_id, followee_id)
- Efficient for "who follows Bob?"
```

### Handling Hotspots

**Celebrity Problem:**
```python
# Detect celebrities
if user.followers_count > 1_000_000:
    # Don't fanout to all followers
    # Instead, mark as celebrity
    redis.sadd("celebrities", user_id)

# Feed generation for celebrity followers
def get_feed(user_id):
    following = get_following(user_id)

    # Separate regular users and celebrities
    regular = [u for u in following if not is_celebrity(u)]
    celebrities = [u for u in following if is_celebrity(u)]

    # Regular: use pre-generated feed
    feed = redis.zrevrange(f"feed:{user_id}", 0, 50)

    # Celebrities: query on-demand
    celebrity_posts = db.query("""
        SELECT * FROM posts
        WHERE user_id IN (?)
          AND created_at > ?
        ORDER BY created_at DESC
        LIMIT 10
    """, celebrities, yesterday())

    # Merge and rank
    return rank_and_merge(feed, celebrity_posts)
```

**Thundering Herd:**
```python
# When cache expires, many requests hit DB
# Solution: Probabilistic early expiration

def get_with_early_expiration(key, ttl):
    data, remaining_ttl = redis.get_with_ttl(key)

    if data is None:
        # Cache miss - acquire lock and fetch
        lock = redis.set(f"{key}:lock", "1", nx=True, ex=10)
        if lock:
            data = fetch_from_db(key)
            redis.setex(key, ttl, data)
        else:
            # Wait for other thread to populate
            time.sleep(0.1)
            return get_with_early_expiration(key, ttl)

    # Probabilistic early expiration
    # Refresh cache before it expires
    elif remaining_ttl < ttl * 0.1:  # Last 10% of TTL
        if random.random() < 0.1:  # 10% chance
            # Async refresh
            async_refresh(key, ttl)

    return data
```

### Multi-Region Architecture

```
Region: US-EAST
- Primary write database
- Full read replicas
- Full cache cluster
- All microservices

Region: EU-WEST
- Read replicas (sync lag: <100ms)
- Full cache cluster
- All microservices
- Writes proxied to US-EAST

Region: APAC
- Read replicas (sync lag: <100ms)
- Full cache cluster
- All microservices
- Writes proxied to US-EAST

Cross-Region Replication:
- Database: PostgreSQL streaming replication
- Cache: Redis cross-region replication (async)
- Storage: S3 cross-region replication
```

### Auto-Scaling Strategy

```yaml
# Kubernetes HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 100
  maxReplicas: 1000
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"

# Scale-up policy: aggressive
behavior:
  scaleUp:
    stabilizationWindowSeconds: 30
    policies:
    - type: Percent
      value: 100
      periodSeconds: 30
  # Scale-down policy: conservative
  scaleDown:
    stabilizationWindowSeconds: 300
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60
```

## 11. Trade-offs

### 1. Feed Generation: Fanout on Write vs. Fanout on Read

**Decision: Hybrid Approach**

| Aspect | Fanout on Write | Fanout on Read | Hybrid |
|--------|----------------|----------------|---------|
| Write Latency | Slow (must update all followers) | Fast | Medium |
| Read Latency | Fast (pre-computed) | Slow (compute on demand) | Fast |
| Storage | High (duplicate data) | Low | Medium |
| Celebrity Problem | Doesn't scale | Scales well | Best of both |

**Implementation:**
- Users with <10K followers: Fanout on write
- Users with >10K followers: Fanout on read
- Cache aggressively for both

---

### 2. Consistency Model for Likes/Comments

**Decision: Eventual Consistency**

**Pros:**
- Much faster (no distributed locks)
- Higher availability
- Better user experience (instant feedback)

**Cons:**
- Counts might be slightly off
- Rare race conditions (double-like)

**Mitigation:**
- Reconciliation jobs run hourly
- Acceptable for social media (users don't notice)

---

### 3. Database Choice for Messages

**Decision: Cassandra (NoSQL)**

**Why not PostgreSQL?**
- 10B messages/day = 115K writes/second
- PostgreSQL would need heavy sharding
- Messages don't need complex joins

**Why Cassandra?**
- Optimized for high write throughput
- Linear scalability (add nodes)
- TTL support (auto-delete old messages)
- Time-series data model fits well

---

### 4. Video Storage: Self-Hosted vs. Cloud Service

**Decision: AWS + Elastic Transcoder**

| Aspect | Self-Hosted (FFmpeg) | Cloud (Elastic Transcoder) |
|--------|---------------------|--------------------------|
| Cost | Lower (long-term) | Higher |
| Scalability | Manual | Automatic |
| Maintenance | High | Low |
| Quality | Full control | Good defaults |
| Time to Market | Slow | Fast |

**Rationale:** For MVP and rapid scaling, cloud service is better. Can optimize later.

---

### 5. Real-time Updates: WebSockets vs. Long Polling

**Decision: WebSockets with Long Polling fallback**

**WebSockets Pros:**
- True real-time (<100ms)
- Efficient (one connection)
- Bi-directional

**WebSockets Cons:**
- Connection management complexity
- Harder to scale (stateful)
- Not supported by all proxies

**Implementation:**
- Primary: WebSockets (Socket.io)
- Fallback: Long polling for old clients/proxies
- Separate WebSocket server cluster

---

### 6. Image Format: JPEG vs. WebP vs. AVIF

**Decision: Serve WebP/AVIF to modern browsers, JPEG to others**

| Format | Size | Quality | Browser Support |
|--------|------|---------|----------------|
| JPEG | Baseline (100%) | Good | 100% |
| WebP | ~30% smaller | Better | 95% |
| AVIF | ~50% smaller | Best | 70% |

**Implementation:**
```python
def serve_image(image_id, user_agent):
    if supports_avif(user_agent):
        return f"{CDN}/avif/{image_id}.avif"
    elif supports_webp(user_agent):
        return f"{CDN}/webp/{image_id}.webp"
    else:
        return f"{CDN}/jpeg/{image_id}.jpg"
```

## 12. Follow-up Questions

### Functional Features

**Q1: How would you implement story highlights?**
A: Create `story_highlights` table with references to stories. Don't delete highlighted stories after 24 hours. Store permanent copies in S3.

**Q2: How to handle story replies (DMs)?**
A: When user replies to story, create new DM thread or use existing one. Add `story_id` reference to message. Show context in message thread.

**Q3: How would you add filters and effects?**
A: Two approaches:
- Client-side: Apply filters in app before upload (reduces server load)
- Server-side: Store original + filter parameters, apply on-demand
- Hybrid: Popular filters pre-generated, rare ones on-demand

**Q4: Implement "close friends" feature for stories?**
A:
```sql
CREATE TABLE close_friends (
    user_id BIGINT,
    friend_id BIGINT,
    PRIMARY KEY (user_id, friend_id)
);

-- When posting story
CREATE TABLE stories (
    ...
    audience VARCHAR(10), -- 'all', 'close_friends', 'custom'
    custom_audience BIGINT[] -- array of user_ids
);
```

### Scale and Performance

**Q5: How to handle 1 billion daily active users?**
A:
- Shard database across 1000+ nodes
- Deploy in 10+ regions worldwide
- Use read replicas heavily (1:100 write:read ratio)
- Implement aggressive caching (cache hit rate >99%)
- Consider eventually consistent databases (Cassandra) for more data
- Pre-compute feeds for all users (batch jobs)

**Q6: What if Redis cluster fails?**
A:
- Redis Cluster with automatic failover
- AOF (Append-Only File) persistence for durability
- Replicas in multiple AZs
- Circuit breaker to database if Redis fails
- Graceful degradation (serve stale data or compute on-the-fly)

**Q7: How to reduce latency for global users?**
A:
- Deploy in multiple regions (US, EU, APAC, SA, Africa)
- Use GeoDNS to route to nearest region
- Replicate static content (images) to all regions
- Allow regional databases with async replication
- Edge computing for feed generation

**Q8: How to optimize search at scale?**
A:
- Elasticsearch cluster with 100+ nodes
- Shard by user_id or hashtag prefix
- Implement auto-complete with Trie or Elasticsearch suggest
- Cache popular search results
- Use approximate algorithms for trending (Count-Min Sketch)

### Reliability and Security

**Q9: How to prevent spam and fake accounts?**
A:
- Rate limiting (max 10 posts/hour, 100 follows/hour)
- CAPTCHA on registration
- Phone verification
- ML models to detect spam patterns
- User reporting system
- Shadowban suspicious accounts

**Q10: How to handle GDPR data deletion requests?**
A:
- Mark user as deleted immediately
- Anonymize user data (replace with "Deleted User")
- Schedule async deletion of posts, comments, messages
- Remove from cache immediately
- Delete media from S3 (lifecycle policy)
- Keep audit log (encrypted)

**Q11: How to ensure high availability during database failover?**
A:
- Master-slave replication with automatic failover
- Use ProxySQL or PgBouncer for connection pooling
- Health checks every 5 seconds
- Failover time: <30 seconds
- Read replicas continue serving reads
- Write buffer in message queue during failover

### Advanced Features

**Q12: How would you implement recommendation system for Explore page?**
A:
- Collaborative filtering (users who liked X also liked Y)
- Content-based filtering (show similar posts)
- Hybrid: Combine both with ML model
- Features:
  * User's like history
  * User's follow graph
  * Post engagement rate
  * Content type (photo/video/reels)
  * Time of day
  * User demographics
- Offline batch job to generate recommendations
- Online serving layer with real-time adjustments

**Q13: How to implement verified accounts?**
A:
```sql
ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN verification_date TIMESTAMP;

-- Blue check badge
-- Manual verification process
-- Show badge in UI
-- Prioritize in search results
```

**Q14: How would you add Instagram Reels (TikTok competitor)?**
A:
- Separate `reels` table
- Video processing pipeline (portrait orientation)
- Dedicated Reels feed (separate from main feed)
- Recommendation algorithm (similar to TikTok FYP)
- Audio library service
- Video effects and transitions
- Engagement metrics (completion rate, replays)

**Q15: How to implement live video streaming?**
A:
- Use WebRTC for peer-to-peer
- Or RTMP to media server (Wowza, Red5)
- Distribute via CDN (HLS/DASH)
- Chat service for live comments
- Viewer count tracking
- Save replay to S3 after stream ends
- Notification system for "went live" events

---

**Total Estimated Interview Time:** 60-75 minutes

**Key Focus Areas:**
- Feed generation algorithm (critical)
- Database sharding strategy
- Caching architecture
- Real-time features (stories, messaging)
- Global scale considerations

**Success Metrics:**
- Can explain ranking algorithm clearly
- Understands trade-offs between consistency and performance
- Knows when to use different databases (SQL vs. NoSQL)
- Can design for 100M+ concurrent users
- Discusses monitoring and observability
