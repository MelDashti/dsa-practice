# Design TikTok

## 1. Problem Statement & Scope

Design a short-form video sharing platform where users can create, share, and discover videos, with a highly personalized recommendation algorithm (For You Page) that drives engagement.

### In Scope:
- User registration and profiles
- Video upload (15-60 seconds)
- Video feed (For You Page - FYP)
- Following feed
- Video engagement (like, comment, share, save)
- Video effects and filters (basic)
- Duets and stitches
- Sounds/audio library
- Hashtags and challenges
- Search (videos, users, sounds, hashtags)
- Real-time notifications
- Analytics for creators

### Out of Scope:
- TikTok Live (live streaming)
- TikTok Shop (e-commerce)
- Advanced AR effects (face filters)
- Direct messaging (separate system)
- Ads platform details
- Content moderation specifics

### Scale:
- 1 billion daily active users (DAU)
- 3 billion total users
- 100 million videos uploaded daily
- 10 billion video views daily
- Average watch time: 50 minutes/day per user
- Peak concurrent users: 150 million

## 2. Functional Requirements

### High Priority (P0):

**FR1: User Management**
- Register with email/phone
- User profiles with bio, profile video
- Follow/unfollow users
- Private/public accounts
- Block users

**FR2: Video Upload**
- Record video (15-60 seconds)
- Upload existing video
- Add music/sound from library
- Apply basic filters and effects
- Add caption and hashtags
- Set privacy (public, friends, private)

**FR3: For You Page (FYP)**
- Personalized video feed
- Infinite scroll
- Auto-play next video
- Pre-load next videos
- Algorithm-driven recommendations

**FR4: Following Feed**
- Videos from followed users
- Chronological or ranked
- Live updates when new video posted

**FR5: Video Engagement**
- Like/unlike videos
- Comment on videos
- Share videos (internal and external)
- Save to favorites
- View video details (description, music, hashtags)

**FR6: Video Creation Features**
- Duet (split-screen with another video)
- Stitch (use clip from another video)
- Use sounds from other videos
- Green screen effect
- Speed control (0.5x, 1x, 2x, 3x)

**FR7: Sound Library**
- Browse sounds by popularity, trending
- Use sound in video
- See all videos using a sound
- Save favorite sounds

**FR8: Search and Discovery**
- Search videos by keywords
- Search users
- Search sounds
- Search hashtags
- Trending page

### Medium Priority (P1):

**FR9: Hashtag Challenges**
- Create challenges with hashtag
- Join challenges
- Challenge leaderboard

**FR10: Analytics**
- View count
- Watch time
- Engagement rate
- Follower growth
- Traffic sources

**FR11: Notifications**
- New follower
- Likes and comments
- Video mentioned in another video
- Challenge invitations

## 3. Non-Functional Requirements (Scale, Performance, Availability)

### Scale Requirements:
- **Daily Active Users:** 1 billion
- **Total Users:** 3 billion
- **Videos uploaded per day:** 100 million
- **Video views per day:** 10 billion
- **Peak concurrent users:** 150 million
- **Average video size:** 20 MB (compressed)
- **Total video catalog:** 500 billion videos

### Performance Requirements:
- **Video upload:** < 30 seconds for 60-second video
- **Video processing:** < 2 minutes for all quality levels
- **FYP load time:** < 500ms for initial video
- **Video start latency:** < 200ms
- **Recommendation generation:** < 100ms
- **Search response:** < 300ms

### Availability:
- **Service availability:** 99.99%
- **Video availability:** 99.999%
- **Recommendation accuracy:** >70% watch-through rate

### Consistency:
- **Video uploads:** Strong consistency (visible immediately)
- **Engagement counts:** Eventual consistency (< 5 seconds)
- **Recommendations:** Eventual consistency (< 1 minute)
- **Trending:** Eventual consistency (< 5 minutes)

## 4. Back-of-envelope Calculations

### Traffic Estimates:

**Video Uploads:**
- Videos per day: 100M
- Videos per second: 100M ÷ 86,400 = ~1,157 videos/sec
- Peak (3x): ~3,471 videos/sec

**Video Views:**
- Views per day: 10B
- Views per second: 10B ÷ 86,400 = ~115,740 views/sec
- Peak (3x): ~347,220 views/sec

**User Sessions:**
- DAU: 1B
- Average watch time: 50 minutes
- Concurrent users: 1B × 50/1440 ≈ 35M average, 150M peak

### Storage Calculations:

**Video Storage:**
- Videos per day: 100M
- Average size (original): 30 MB
- Multiple qualities (4K, 1080p, 720p, 480p, 360p): 30 MB × 5 = 150 MB
- Daily storage: 100M × 150 MB = 15 PB/day
- Yearly storage: 15 PB × 365 = 5.5 EB/year

**Metadata:**
- Videos: 500B videos × 5 KB = 2.5 PB
- Users: 3B × 2 KB = 6 TB
- Comments: 50B × 500 bytes = 25 TB
- Likes: 500B × 20 bytes = 10 TB

**Machine Learning Models:**
- User embedding vectors: 3B users × 512 floats × 4 bytes = 6 TB
- Video embedding vectors: 500B videos × 512 floats × 4 bytes = 1 PB
- Model parameters: ~100 GB

**Total Storage (Year 1):** ~5.5 EB (exabytes)

### Bandwidth Calculations:

**Incoming (Upload):**
- 100M videos × 30 MB = 3 PB/day
- Per second: 3 PB ÷ 86,400 = ~35 GB/s
- Peak (3x): ~105 GB/s

**Outgoing (Streaming):**
- 10B views × 20 MB average = 200 PB/day
- Per second: 200 PB ÷ 86,400 = ~2.3 TB/s
- Peak (3x): ~6.9 TB/s
- **CDN is absolutely critical**

### Compute Requirements:

**Video Processing:**
- 100M videos/day to encode
- Each video: 5 quality levels × 2 minutes = 10 CPU-minutes
- Total: 100M × 10 = 1B CPU-minutes/day
- Instances needed: 1B ÷ 1440 ÷ 60 = ~11,500 instances (continuous)

**Recommendation Engine:**
- 1B users × 100 recommendations per session = 100B recommendations/day
- Per second: 100B ÷ 86,400 = ~1.15M recommendations/sec
- Using cached models, each recommendation: 10ms
- Servers needed: 1.15M × 0.01 ÷ 1000 = ~11,500 servers

**API Servers:**
- 350K QPS (peak views)
- Each server: 1K QPS
- Servers: 350 × 3 (redundancy) = 1,050 servers

## 5. High-Level Architecture Diagram Description

```
                    [Mobile Apps - iOS/Android]
                                |
                                v
                    [Global Load Balancer / GeoDNS]
                                |
            +-------------------+-------------------+
            |                   |                   |
        [US Region]         [EU Region]        [APAC Region]
            |                   |                   |
            v                   v                   v
    [Multi-CDN Strategy]
    (CloudFront, Akamai, Cloudflare)
    [Serves 95% of video traffic]
            |
            v
    [API Gateway + Rate Limiter]
            |
    +-------+-------+-------+-------+-------+
    |       |       |       |       |       |
    v       v       v       v       v       v
[Upload  [Feed   [Recommendation  [Search  [Social
 Service] Service]   Engine]      Service] Service]
    |       |           |              |        |
    +-------|-----------|--------------|--------|
            |
            v
    [Event Stream - Kafka]
            |
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
[Analytics  [Trending  [Notification  [Content
 Service]    Service]    Service]      Moderation]


    |           |           |           |
    v           v           v           v
[PostgreSQL] [Cassandra] [Redis]  [Elasticsearch]
(Users,      (Videos,    (Cache,   (Search)
 Profiles)    Engagement) Rankings)
    |
    v
[Video Processing Pipeline]
    |
    v
[S3/Object Storage] -> [CDN]
(Multi-region replication)


[ML Infrastructure]
    |
    v
[Feature Store] -> [Model Serving] -> [A/B Testing]
    |                   |
[Offline Training]  [Online Inference]
(Spark/Flink)      (TensorFlow Serving)
```

### Key Services:

1. **Upload Service:** Handle video uploads, validation
2. **Video Processing Pipeline:** Transcode to multiple formats
3. **Feed Service:** Serve FYP and Following feeds
4. **Recommendation Engine:** ML-based video ranking
5. **Social Service:** Follows, likes, comments
6. **Search Service:** Full-text search across videos/users
7. **Analytics Service:** Track views, engagement, watch time
8. **Trending Service:** Calculate trending videos/sounds
9. **CDN:** Global video delivery
10. **ML Infrastructure:** Training and serving recommendation models

## 6. API Design (RESTful endpoints)

### Video Upload APIs

```
POST /api/v1/videos/upload/init
Request:
{
  "video_duration": 30,
  "file_size": 25000000,
  "video_metadata": {
    "width": 1080,
    "height": 1920,
    "fps": 30
  }
}
Response: 200 OK
{
  "upload_id": "upload_abc123",
  "upload_url": "https://s3.../presigned_url",
  "expires_at": "2025-11-12T11:00:00Z"
}

POST /api/v1/videos/upload/complete
Request:
{
  "upload_id": "upload_abc123",
  "caption": "Check out this cool trick! #fyp #dance",
  "sound_id": "sound_456",
  "hashtags": ["fyp", "dance"],
  "privacy": "public",
  "duet_enabled": true,
  "stitch_enabled": true,
  "comment_enabled": true
}
Response: 201 Created
{
  "video_id": "vid_789",
  "status": "processing",
  "estimated_completion": "2025-11-12T10:32:00Z"
}

GET /api/v1/videos/{video_id}/status
Response: 200 OK
{
  "video_id": "vid_789",
  "status": "completed",
  "available_qualities": ["4k", "1080p", "720p", "480p", "360p"],
  "thumbnail_url": "https://cdn.../thumb.jpg",
  "duration": 30
}
```

### Video Playback APIs

```
GET /api/v1/videos/{video_id}
Response: 200 OK
{
  "video_id": "vid_789",
  "user": {
    "user_id": "user_123",
    "username": "@johndoe",
    "display_name": "John Doe",
    "avatar_url": "...",
    "is_verified": false,
    "follower_count": 15000
  },
  "caption": "Check out this cool trick! #fyp #dance",
  "sound": {
    "sound_id": "sound_456",
    "name": "Original Sound - @johndoe",
    "duration": 30,
    "usage_count": 1234
  },
  "video_urls": {
    "4k": "https://cdn.../4k.m3u8",
    "1080p": "https://cdn.../1080p.m3u8",
    "720p": "https://cdn.../720p.m3u8",
    "480p": "https://cdn.../480p.m3u8"
  },
  "thumbnail_url": "...",
  "duration": 30,
  "stats": {
    "views": 125000,
    "likes": 8500,
    "comments": 342,
    "shares": 156,
    "saves": 89
  },
  "user_engagement": {
    "has_liked": false,
    "has_saved": false,
    "has_followed": true
  },
  "created_at": "2025-11-12T10:30:00Z"
}

POST /api/v1/videos/{video_id}/view
Request:
{
  "watch_time": 25,  // seconds
  "completion_rate": 0.83,
  "source": "fyp"  // or "following", "hashtag", "sound", "profile"
}
Response: 204 No Content
```

### Feed APIs

```
GET /api/v1/feed/for-you?limit=20&cursor={cursor}
Response: 200 OK
{
  "videos": [
    {
      "video_id": "vid_789",
      "video": {...},
      "reason": "trending_in_your_area"
    }
  ],
  "next_cursor": "eyJvZmZzZXQiOjIwfQ==",
  "prefetch_ids": ["vid_790", "vid_791", "vid_792"]
}

GET /api/v1/feed/following?limit=20&cursor={cursor}
Response: Similar to for-you

GET /api/v1/feed/friends
# Videos from mutual follows
```

### Engagement APIs

```
POST /api/v1/videos/{video_id}/like
Response: 201 Created
{
  "likes_count": 8501
}

DELETE /api/v1/videos/{video_id}/like
Response: 204 No Content

POST /api/v1/videos/{video_id}/comments
Request:
{
  "text": "Amazing! 🔥",
  "parent_comment_id": null
}

GET /api/v1/videos/{video_id}/comments?limit=50&cursor={cursor}

POST /api/v1/videos/{video_id}/share
Request:
{
  "share_type": "internal",  // or "external"
  "platform": "whatsapp"  // for external shares
}

POST /api/v1/videos/{video_id}/save
DELETE /api/v1/videos/{video_id}/save
```

### Social APIs

```
POST /api/v1/users/{user_id}/follow
DELETE /api/v1/users/{user_id}/unfollow

GET /api/v1/users/{user_id}
GET /api/v1/users/{user_id}/videos?limit=20
GET /api/v1/users/{user_id}/liked?limit=20

POST /api/v1/videos/{video_id}/duet
Request:
{
  "upload_id": "upload_xyz"
}

POST /api/v1/videos/{video_id}/stitch
Request:
{
  "upload_id": "upload_xyz",
  "clip_start": 5,  // seconds
  "clip_end": 10
}
```

### Sound APIs

```
GET /api/v1/sounds/{sound_id}
Response:
{
  "sound_id": "sound_456",
  "name": "Original Sound - @johndoe",
  "author": {...},
  "duration": 30,
  "usage_count": 1234,
  "is_original": true,
  "audio_url": "https://cdn.../audio.mp3"
}

GET /api/v1/sounds/{sound_id}/videos?limit=20
# Videos using this sound

GET /api/v1/sounds/trending?limit=50
```

### Search APIs

```
GET /api/v1/search/videos?q=dance&limit=20
GET /api/v1/search/users?q=johndoe&limit=20
GET /api/v1/search/sounds?q=trending+song&limit=20
GET /api/v1/search/hashtags?q=fyp&limit=20

GET /api/v1/hashtags/{hashtag}/videos?limit=20
```

### Analytics APIs

```
GET /api/v1/analytics/video/{video_id}
Response:
{
  "video_id": "vid_789",
  "period": "last_7_days",
  "metrics": {
    "views": 125000,
    "unique_viewers": 98000,
    "avg_watch_time": 25.5,
    "completion_rate": 0.85,
    "likes": 8500,
    "comments": 342,
    "shares": 156,
    "engagement_rate": 0.072
  },
  "traffic_sources": {
    "fyp": 0.75,
    "following": 0.15,
    "hashtag": 0.05,
    "profile": 0.03,
    "sound": 0.02
  },
  "audience": {
    "age_groups": {...},
    "genders": {...},
    "countries": {...}
  }
}

GET /api/v1/analytics/creator/{user_id}/overview
# Creator dashboard metrics
```

## 7. Database Design (Schema, Indexes)

### PostgreSQL (Users, Profiles)

```sql
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255),
    display_name VARCHAR(50),
    bio VARCHAR(160),
    avatar_url VARCHAR(500),
    profile_video_id VARCHAR(20),
    is_verified BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    likes_count INT DEFAULT 0,
    video_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_follower_count ON users(follower_count DESC);

CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_follows_followee ON follows(followee_id);
```

### Cassandra (Videos, Engagement)

```cql
-- Videos
CREATE TABLE videos (
    video_id TEXT PRIMARY KEY,
    user_id BIGINT,
    caption TEXT,
    sound_id TEXT,
    hashtags SET<TEXT>,
    video_urls MAP<TEXT, TEXT>,  -- quality -> url
    thumbnail_url TEXT,
    duration INT,
    width INT,
    height INT,
    views_count BIGINT,
    likes_count INT,
    comments_count INT,
    shares_count INT,
    saves_count INT,
    privacy VARCHAR(20),
    is_duet_enabled BOOLEAN,
    is_stitch_enabled BOOLEAN,
    is_comment_enabled BOOLEAN,
    created_at TIMESTAMP,
    PRIMARY KEY (video_id)
);

-- User videos (for profile page)
CREATE TABLE user_videos (
    user_id BIGINT,
    video_id TEXT,
    created_at TIMESTAMP,
    likes_count INT,
    views_count BIGINT,
    PRIMARY KEY (user_id, created_at, video_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Video engagement
CREATE TABLE video_likes (
    video_id TEXT,
    user_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (video_id, user_id)
);

CREATE TABLE user_liked_videos (
    user_id BIGINT,
    video_id TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at, video_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Comments
CREATE TABLE video_comments (
    comment_id TEXT,
    video_id TEXT,
    user_id BIGINT,
    parent_comment_id TEXT,
    text TEXT,
    likes_count INT,
    created_at TIMESTAMP,
    PRIMARY KEY (video_id, created_at, comment_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Video views (for analytics)
CREATE TABLE video_views (
    video_id TEXT,
    user_id BIGINT,
    view_id TIMEUUID,
    watch_time INT,
    completion_rate FLOAT,
    source TEXT,  -- fyp, following, hashtag, sound, profile
    created_at TIMESTAMP,
    PRIMARY KEY (video_id, created_at, view_id)
) WITH CLUSTERING ORDER BY (created_at DESC)
  AND default_time_to_live = 2592000;  -- 30 days

-- Sounds
CREATE TABLE sounds (
    sound_id TEXT PRIMARY KEY,
    name TEXT,
    author_user_id BIGINT,
    duration INT,
    usage_count INT,
    is_original BOOLEAN,
    audio_url TEXT,
    created_at TIMESTAMP
);

CREATE TABLE sound_videos (
    sound_id TEXT,
    video_id TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (sound_id, created_at, video_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Hashtags
CREATE TABLE hashtag_videos (
    hashtag TEXT,
    video_id TEXT,
    created_at TIMESTAMP,
    views_count BIGINT,
    PRIMARY KEY (hashtag, created_at, video_id)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

### Redis Cache

```
# User feed cache (pre-generated recommendations)
Key: feed:fyp:{user_id}
Type: List
Value: [video_id1, video_id2, ...]
TTL: 30 minutes
Size: 100 videos

# Trending videos cache
Key: trending:global
Type: Sorted Set
Score: trending_score
Members: video_ids
TTL: 5 minutes

# Video metadata cache
Key: video:{video_id}
Type: Hash
TTL: 1 hour

# User profile cache
Key: user:{user_id}
Type: Hash
TTL: 30 minutes

# Video view count (real-time counter)
Key: views:{video_id}
Type: String (counter)
TTL: No expiry
Update: INCR on each view

# Hot videos (for recommendation warmup)
Key: hot:videos
Type: Sorted Set
Score: engagement_score
Members: video_ids
TTL: 10 minutes

# User embedding cache (for recommendations)
Key: embedding:user:{user_id}
Type: String (binary vector)
TTL: 1 hour

# Video embedding cache
Key: embedding:video:{video_id}
Type: String (binary vector)
TTL: 24 hours
```

### Feature Store (for ML)

```python
# User features
{
    "user_id": 123,
    "age_group": "18-24",
    "gender": "F",
    "location": "US-CA",
    "interests": ["dance", "comedy", "food"],
    "avg_watch_time": 45.2,
    "preferred_video_length": "15-30s",
    "active_hours": [18, 19, 20, 21, 22],
    "engagement_rate": 0.12,
    "following_count": 234,
    "follower_count": 156
}

# Video features
{
    "video_id": "vid_789",
    "duration": 30,
    "categories": ["dance", "transition"],
    "sound_id": "sound_456",
    "hashtags": ["fyp", "dance"],
    "upload_time": "2025-11-12T10:30:00Z",
    "creator_follower_count": 15000,
    "early_engagement_rate": 0.15,
    "completion_rate": 0.85,
    "share_rate": 0.012
}
```

## 8. Core Components

### A. For You Page (FYP) Recommendation Engine

**Multi-Stage Ranking:**

```python
class FYPRecommendationEngine:
    def generate_feed(self, user_id, limit=20):
        """
        Generate personalized FYP feed
        Multi-stage funnel: Candidate Generation -> Ranking -> Re-ranking
        """

        # Stage 1: Candidate Generation (retrieve ~1000 videos)
        candidates = self.generate_candidates(user_id, candidate_count=1000)

        # Stage 2: Ranking (ML model scores all candidates)
        ranked = self.rank_candidates(user_id, candidates)

        # Stage 3: Re-ranking (diversity, freshness, business logic)
        final_feed = self.rerank(user_id, ranked, limit=limit)

        # Cache for future requests
        redis.lpush(f"feed:fyp:{user_id}", *final_feed)
        redis.expire(f"feed:fyp:{user_id}", 1800)  # 30 min

        return final_feed

    def generate_candidates(self, user_id, candidate_count=1000):
        """
        Candidate generation from multiple sources
        """

        candidates = []

        # Source 1: Collaborative Filtering (50% of candidates)
        # Find similar users and their liked videos
        similar_users = self.find_similar_users(user_id, limit=100)
        cf_candidates = self.get_liked_videos_from_users(
            similar_users, limit=500)
        candidates.extend(cf_candidates)

        # Source 2: Content-Based (30% of candidates)
        # Videos similar to user's watch history
        user_history = self.get_user_watch_history(user_id, limit=50)
        cb_candidates = self.find_similar_videos(
            user_history, limit=300)
        candidates.extend(cb_candidates)

        # Source 3: Trending (15% of candidates)
        trending = redis.zrevrange("trending:global", 0, 149)
        candidates.extend(trending)

        # Source 4: Followed Creators (5% of candidates)
        following = self.get_following(user_id)
        following_videos = self.get_recent_videos_from_users(
            following, limit=50)
        candidates.extend(following_videos)

        # Deduplicate and filter already seen
        candidates = self.deduplicate(candidates)
        candidates = self.filter_seen(user_id, candidates)

        return candidates[:candidate_count]

    def rank_candidates(self, user_id, candidates):
        """
        Rank candidates using ML model
        Model predicts: P(user will watch video to completion)
        """

        # Get user embedding
        user_embedding = self.get_user_embedding(user_id)

        # Get video embeddings (batch)
        video_embeddings = self.batch_get_video_embeddings(candidates)

        # Prepare features
        features = []
        for video_id, video_emb in zip(candidates, video_embeddings):
            feature = self.create_feature_vector(
                user_id=user_id,
                video_id=video_id,
                user_embedding=user_embedding,
                video_embedding=video_emb
            )
            features.append(feature)

        # Batch inference using TensorFlow Serving
        scores = self.ml_model.predict(features)

        # Sort by predicted engagement
        ranked = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [video_id for video_id, score in ranked]

    def rerank(self, user_id, ranked_videos, limit=20):
        """
        Re-rank for diversity and business logic
        """

        final_feed = []
        seen_creators = set()
        seen_sounds = set()
        seen_categories = set()

        for video_id in ranked_videos:
            if len(final_feed) >= limit:
                break

            video = self.get_video(video_id)

            # Diversity rules
            # Don't show 2 videos from same creator consecutively
            if video.user_id in seen_creators:
                continue

            # Don't show 3 videos with same sound
            if video.sound_id in seen_sounds and seen_sounds[video.sound_id] >= 3:
                continue

            # Add to feed
            final_feed.append(video_id)
            seen_creators.add(video.user_id)
            seen_sounds[video.sound_id] = seen_sounds.get(video.sound_id, 0) + 1

            # Reset seen creators every 5 videos
            if len(final_feed) % 5 == 0:
                seen_creators.clear()

        return final_feed

    def create_feature_vector(self, user_id, video_id, user_embedding, video_embedding):
        """Create feature vector for ML model"""

        # User features
        user_features = self.get_user_features(user_id)

        # Video features
        video_features = self.get_video_features(video_id)

        # Interaction features
        creator = self.get_user(video_features['creator_id'])
        is_following = self.is_following(user_id, creator.user_id)
        time_since_upload = time.time() - video_features['created_at']

        # Combine all features
        features = {
            # User embedding (512 dims)
            **{'user_emb_' + str(i): val for i, val in enumerate(user_embedding)},

            # Video embedding (512 dims)
            **{'video_emb_' + str(i): val for i, val in enumerate(video_embedding)},

            # Dense features
            'user_age_group': user_features['age_group'],
            'user_gender': user_features['gender'],
            'user_avg_watch_time': user_features['avg_watch_time'],
            'video_duration': video_features['duration'],
            'creator_follower_count': creator.follower_count,
            'is_following_creator': 1 if is_following else 0,
            'time_since_upload_hours': time_since_upload / 3600,
            'video_early_engagement_rate': video_features.get('early_engagement_rate', 0),
            'hour_of_day': datetime.now().hour,
            'day_of_week': datetime.now().weekday()
        }

        return features

    def get_user_embedding(self, user_id):
        """Get user embedding vector (from cache or model)"""

        # Check cache
        cache_key = f"embedding:user:{user_id}"
        cached = redis.get(cache_key)

        if cached:
            return np.frombuffer(cached, dtype=np.float32)

        # Generate using embedding model
        user_features = self.get_user_features(user_id)
        user_history = self.get_user_watch_history(user_id, limit=100)

        embedding = self.user_embedding_model.encode(
            user_features, user_history)

        # Cache for 1 hour
        redis.setex(cache_key, 3600, embedding.tobytes())

        return embedding
```

### B. Video Processing Pipeline

**Multi-Quality Encoding:**

```python
class VideoProcessingPipeline:
    def process_video(self, upload_id, video_file_path):
        """
        Process uploaded video:
        1. Validate
        2. Extract thumbnail
        3. Transcode to multiple qualities
        4. Generate HLS playlists
        5. Upload to CDN
        6. Update database
        """

        # Step 1: Validate
        if not self.validate_video(video_file_path):
            raise VideoValidationError("Invalid video format")

        # Step 2: Extract metadata
        metadata = self.extract_metadata(video_file_path)
        duration = metadata['duration']
        width = metadata['width']
        height = metadata['height']
        fps = metadata['fps']

        # Step 3: Extract thumbnail (at 1 second)
        thumbnail = self.extract_frame(video_file_path, at_second=1.0)
        thumbnail_url = self.upload_to_s3(thumbnail, "thumbnails/")

        # Step 4: Transcode to multiple qualities
        qualities = self.transcode_video(video_file_path, metadata)

        # Step 5: Generate HLS playlists
        hls_urls = self.generate_hls(qualities)

        # Step 6: Extract audio (for sound library)
        audio_path = self.extract_audio(video_file_path)
        audio_url = self.upload_to_s3(audio_path, "sounds/")

        # Step 7: Update database
        video_id = self.get_video_id_from_upload(upload_id)
        self.update_video_record(
            video_id=video_id,
            video_urls=hls_urls,
            thumbnail_url=thumbnail_url,
            audio_url=audio_url,
            duration=duration,
            width=width,
            height=height,
            status="completed"
        )

        # Step 8: Generate video embedding for recommendations
        self.generate_video_embedding_async(video_id, video_file_path)

        # Step 9: Publish event
        kafka.publish("video_processed", {
            "video_id": video_id,
            "user_id": self.get_user_id(upload_id)
        })

        return video_id

    def transcode_video(self, input_path, metadata):
        """
        Transcode to multiple qualities using FFmpeg
        TikTok uses vertical format (9:16 aspect ratio)
        """

        qualities = {}

        # Original video is typically 1080x1920 (9:16)
        # Generate lower qualities

        quality_configs = [
            {"name": "1080p", "width": 1080, "height": 1920, "bitrate": "3000k"},
            {"name": "720p", "width": 720, "height": 1280, "bitrate": "2000k"},
            {"name": "480p", "width": 480, "height": 854, "bitrate": "1000k"},
            {"name": "360p", "width": 360, "height": 640, "bitrate": "600k"},
        ]

        for config in quality_configs:
            output_path = f"/tmp/{uuid.uuid4()}_{config['name']}.mp4"

            # FFmpeg command
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vf", f"scale={config['width']}:{config['height']}",
                "-b:v", config['bitrate'],
                "-c:v", "libx264",
                "-preset", "medium",
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                "-y",
                output_path
            ]

            subprocess.run(cmd, check=True)

            # Upload to S3
            s3_key = f"videos/{video_id}/{config['name']}.mp4"
            s3_url = self.upload_to_s3(output_path, s3_key)

            qualities[config['name']] = s3_url

            # Clean up temp file
            os.remove(output_path)

        return qualities

    def generate_hls(self, qualities):
        """
        Generate HLS (HTTP Live Streaming) playlists
        For adaptive bitrate streaming
        """

        hls_urls = {}

        for quality, video_url in qualities.items():
            # Generate HLS segments and m3u8 playlist
            video_path = self.download_from_s3(video_url)
            output_dir = f"/tmp/hls_{uuid.uuid4()}/"
            os.makedirs(output_dir)

            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-codec:", "copy",
                "-start_number", "0",
                "-hls_time", "2",  # 2-second segments
                "-hls_list_size", "0",
                "-f", "hls",
                f"{output_dir}/playlist.m3u8"
            ]

            subprocess.run(cmd, check=True)

            # Upload all segments and playlist to S3
            s3_prefix = f"videos/{video_id}/hls/{quality}/"
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                s3_url = self.upload_to_s3(file_path, s3_prefix + file)

            hls_urls[quality] = f"{s3_prefix}playlist.m3u8"

            # Clean up
            shutil.rmtree(output_dir)
            os.remove(video_path)

        return hls_urls
```

### C. CDN Integration and Video Delivery

**Adaptive Streaming:**

```python
class VideoDeliveryService:
    def get_video_url(self, video_id, user_context):
        """
        Return optimal video quality based on:
        - User's network speed
        - Device type
        - Data saver settings
        """

        # Get video metadata
        video = self.get_video(video_id)

        # Determine initial quality
        if user_context.data_saver_enabled:
            quality = "360p"
        elif user_context.connection_type == "wifi":
            quality = "1080p"
        elif user_context.connection_type == "4g":
            quality = "720p"
        else:  # 3G or slower
            quality = "480p"

        # Return HLS playlist URL (client will adapt)
        cdn_url = f"https://cdn.tiktok.com/{video.video_urls[quality]}"

        return {
            "video_url": cdn_url,
            "adaptive_urls": video.video_urls,  # all qualities
            "thumbnail_url": video.thumbnail_url
        }

# Multi-CDN strategy for global distribution
class MultiCDNManager:
    def __init__(self):
        self.cdns = {
            "cloudfront": CloudFrontCDN(),
            "akamai": AkamaiCDN(),
            "cloudflare": CloudflareCDN()
        }

    def get_optimal_cdn(self, user_location):
        """
        Route user to optimal CDN based on location
        """

        # Geographic routing
        if user_location.continent == "NA":
            return self.cdns["cloudfront"]
        elif user_location.continent == "EU":
            return self.cdns["akamai"]
        elif user_location.continent == "AS":
            return self.cdns["cloudflare"]
        else:
            return self.cdns["cloudfront"]

    def failover(self, primary_cdn, video_url):
        """
        Failover to backup CDN if primary fails
        """

        try:
            return primary_cdn.get_url(video_url)
        except CDNError:
            # Try next CDN
            for cdn_name, cdn in self.cdns.items():
                if cdn != primary_cdn:
                    try:
                        return cdn.get_url(video_url)
                    except CDNError:
                        continue

            raise AllCDNsFailedError()
```

### D. Trending Algorithm

```python
class TrendingService:
    def calculate_trending_score(self, video_id):
        """
        Calculate trending score based on:
        - Recent engagement velocity
        - Completion rate
        - Share rate
        - Time decay
        """

        # Get video stats
        video = self.get_video(video_id)
        age_hours = (time.time() - video.created_at) / 3600

        # Get recent engagement (last 6 hours)
        recent_views = self.get_recent_views(video_id, hours=6)
        recent_likes = self.get_recent_likes(video_id, hours=6)
        recent_shares = self.get_recent_shares(video_id, hours=6)

        # Calculate velocity (engagement per hour)
        views_velocity = recent_views / 6
        likes_velocity = recent_likes / 6
        shares_velocity = recent_shares / 6

        # Weight different engagements
        engagement_score = (
            views_velocity * 1 +
            likes_velocity * 10 +
            shares_velocity * 50
        )

        # Quality signals
        completion_rate = self.get_completion_rate(video_id)
        share_rate = recent_shares / max(recent_views, 1)

        quality_multiplier = (
            completion_rate * 0.5 +
            share_rate * 100 * 0.5
        )

        # Time decay (exponential)
        # Newer videos get boost
        recency_boost = math.exp(-age_hours / 24)

        # Final trending score
        trending_score = (
            engagement_score *
            quality_multiplier *
            (1 + recency_boost)
        )

        return trending_score

    def update_trending(self):
        """
        Periodically update trending videos
        Runs every 5 minutes
        """

        # Get videos from last 48 hours
        recent_videos = cassandra.execute("""
            SELECT video_id, created_at
            FROM videos
            WHERE created_at > ?
        """, two_days_ago())

        # Calculate scores
        scores = {}
        for video in recent_videos:
            score = self.calculate_trending_score(video.video_id)
            scores[video.video_id] = score

        # Update Redis sorted set
        redis.zadd("trending:global", scores)

        # Keep only top 1000
        redis.zremrangebyrank("trending:global", 0, -1001)

        # Set expiry
        redis.expire("trending:global", 300)  # 5 minutes
```

### E. Analytics Service

```python
class AnalyticsService:
    def track_view(self, video_id, user_id, watch_time, completion_rate, source):
        """
        Track video view for analytics
        """

        # Insert into Cassandra (time-series data)
        cassandra.execute("""
            INSERT INTO video_views
            (video_id, user_id, view_id, watch_time, completion_rate, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, video_id, user_id, uuid.uuid1(), watch_time, completion_rate, source, now())

        # Update real-time counter in Redis
        redis.incr(f"views:{video_id}")

        # Update video record (async, batched)
        self.queue_view_count_update(video_id)

        # Track for recommendation model
        kafka.publish("video_viewed", {
            "video_id": video_id,
            "user_id": user_id,
            "watch_time": watch_time,
            "completion_rate": completion_rate,
            "source": source,
            "timestamp": time.time()
        })

        # Update user watch history (for recommendations)
        redis.lpush(f"watch_history:{user_id}", video_id)
        redis.ltrim(f"watch_history:{user_id}", 0, 99)  # Keep last 100

    def get_video_analytics(self, video_id, period="last_7_days"):
        """
        Get aggregated analytics for video
        """

        # Check cache
        cache_key = f"analytics:video:{video_id}:{period}"
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Calculate date range
        end_date = datetime.now()
        if period == "last_7_days":
            start_date = end_date - timedelta(days=7)
        elif period == "last_30_days":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=1)

        # Query Cassandra (aggregate on application side)
        views = cassandra.execute("""
            SELECT user_id, watch_time, completion_rate, source, created_at
            FROM video_views
            WHERE video_id = ? AND created_at >= ? AND created_at < ?
        """, video_id, start_date, end_date)

        # Aggregate metrics
        total_views = len(views)
        unique_viewers = len(set(v.user_id for v in views))
        avg_watch_time = sum(v.watch_time for v in views) / max(total_views, 1)
        avg_completion_rate = sum(v.completion_rate for v in views) / max(total_views, 1)

        # Traffic sources
        sources = {}
        for v in views:
            sources[v.source] = sources.get(v.source, 0) + 1

        source_percentages = {
            source: count / total_views
            for source, count in sources.items()
        }

        analytics = {
            "video_id": video_id,
            "period": period,
            "metrics": {
                "views": total_views,
                "unique_viewers": unique_viewers,
                "avg_watch_time": round(avg_watch_time, 2),
                "completion_rate": round(avg_completion_rate, 4)
            },
            "traffic_sources": source_percentages
        }

        # Cache for 1 hour
        redis.setex(cache_key, 3600, json.dumps(analytics))

        return analytics
```

## 9. Data Flow

### Flow 1: User Uploads Video

```
1. User records 30-second video in app
2. App compresses video locally (< 30 MB)
3. App requests upload URL
   POST /api/v1/videos/upload/init
4. Upload Service:
   - Generates upload_id
   - Returns presigned S3 URL
5. App uploads directly to S3 (< 30 seconds)
6. App confirms upload
   POST /api/v1/videos/upload/complete
7. Video Processing Pipeline (async):
   - Validates video format
   - Extracts thumbnail at 1 second
   - Transcodes to 5 qualities (1080p, 720p, 480p, 360p)
   - Generates HLS playlists for adaptive streaming
   - Extracts audio for sound library
   - Total processing time: 1-2 minutes
8. Update video status to "completed"
9. Generate video embedding (ML model)
10. Index in Elasticsearch for search
11. Publish to Kafka: "video_uploaded"
12. Notify followers (async)
```

### Flow 2: User Scrolls FYP

```
1. User opens TikTok app
2. App requests FYP feed
   GET /api/v1/feed/for-you?limit=20
3. Feed Service:
   - Check cache: feed:fyp:{user_id}
4. If cache HIT:
   - Return cached video IDs (< 50ms)
5. If cache MISS:
   - Trigger recommendation engine
   - Candidate generation: 1000 videos
   - Ranking: ML model scores all candidates
   - Re-ranking: Apply diversity and business rules
   - Cache result (TTL: 30 min)
   - Return top 20 videos (< 300ms)
6. Client receives video list
7. Client requests first video
   GET /api/v1/videos/{video_id}
8. Video Service returns metadata + HLS URLs
9. Client streams video from CDN
   - HLS adaptive streaming
   - Preload next 3 videos in background
10. Client tracks view
    POST /api/v1/videos/{video_id}/view
11. Analytics Service:
    - Track view in Cassandra
    - Update view counter in Redis
    - Publish to Kafka for ML model training
12. Recommendation Engine:
    - User watched 85% of video → positive signal
    - Show more videos like this
```

### Flow 3: Video Goes Viral

```
1. Video gets 1000 likes in first hour
2. Trending Service detects high engagement velocity
3. Calculate trending score (high)
4. Add to trending:global sorted set in Redis
5. Recommendation Engine:
   - Boost video in FYP for more users
   - Especially users in same region/interest
6. Video appears in FYP for millions of users
7. Views spike to 1M per hour
8. CDN handles load:
   - Edge caches serve 99% of requests
   - Minimal origin load
9. Analytics tracks engagement:
   - View count updated in real-time (Redis)
   - Detailed analytics in Cassandra
10. Creator dashboard shows real-time stats
```

## 10. Scalability Considerations

### Video Storage and CDN

```
Challenge: 100M videos/day × 150 MB = 15 PB/day

Solutions:
- Multi-region S3 replication (US, EU, APAC)
- Tiered storage:
  * Hot (< 30 days): S3 Standard
  * Warm (30-180 days): S3 Intelligent-Tiering
  * Cold (180+ days): S3 Glacier
- Aggressive CDN caching (99% hit rate)
- Delete low-engagement videos after 1 year
```

### Recommendation Engine Scaling

```
Challenge: 1B users × 100 recommendations = 100B recommendations/day

Solutions:
- Pre-compute feeds for active users (cache)
- Batch inference (process 1000s of predictions in parallel)
- Model serving cluster with auto-scaling
- Feature caching (user/video embeddings)
- Approximate nearest neighbor search (FAISS)
```

### Database Sharding

```
Users: Shard by user_id (consistent hashing)
Videos: Shard by video_id (Cassandra handles automatically)
Social graph: Replicate in multiple shards
```

### ML Model Training

```
Offline training pipeline:
- Spark cluster processes 10B view events/day
- Extract features, train models
- Daily model updates
- A/B test new models before rollout
```

## 11. Trade-offs

### 1. Video Quality vs. Storage Cost
**Decision:** Store 5 qualities, use adaptive streaming

### 2. Recommendation Accuracy vs. Latency
**Decision:** Cache pre-computed feeds (30-min stale acceptable)

### 3. Real-time Analytics vs. Cost
**Decision:** Hybrid - real-time counters in Redis, detailed analytics in batch

### 4. SQL vs. NoSQL
**Decision:** PostgreSQL for users, Cassandra for videos/engagement

### 5. Self-hosted vs. Cloud Video Processing
**Decision:** Cloud (AWS Elastic Transcoder) for scalability

## 12. Follow-up Questions

**Q1: How to handle copyright detection?**
A: Audio fingerprinting (Shazam-like), video fingerprinting (YouTube ContentID), ML models for copyrighted content.

**Q2: How to add live streaming?**
A: WebRTC for low latency (<3s), HLS for scalability, separate live service.

**Q3: How to implement duets technically?**
A: Client-side video merging, or server-side FFmpeg to combine videos side-by-side.

**Q4: How to prevent bots from artificially boosting views?**
A: Device fingerprinting, rate limiting, CAPTCHA, ML anomaly detection.

**Q5: How to scale ML model training?**
A: Distributed training (Horovod, PyTorch Distributed), parameter servers, pipeline parallelism.

---

**Estimated Interview Time:** 70-90 minutes

**Difficulty:** Medium-High (ML systems, video processing, global scale)
