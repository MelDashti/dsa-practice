# Design Instagram MVP (Minimum Viable Product)

## 1. Problem Statement & Scope

Design a simplified version of Instagram that allows users to share photos with their followers.

### In Scope:
- User registration and authentication
- User profiles (username, bio, profile picture)
- Photo upload (single photo per post)
- Chronological feed generation
- Following/unfollowing users
- Likes on posts
- Comments on posts
- View user profiles and their posts

### Out of Scope:
- Stories, Reels, IGTV
- Direct messaging
- Video uploads
- Advanced search and discovery
- Hashtags and tagging
- Complex recommendation algorithms
- Live streaming
- Multiple photos per post
- Filters and editing

### Target Users:
- Start with 1 million daily active users
- Focus on core photo-sharing experience

## 2. Functional Requirements

### Core Features:

**FR1: User Management**
- Users can register with email/phone and password
- Users can login and logout
- Users can view and edit their profile

**FR2: Photo Sharing**
- Users can upload photos (max 10MB per photo)
- Users can add captions to photos
- Users can delete their own photos

**FR3: Social Features**
- Users can follow/unfollow other users
- Users can like/unlike posts
- Users can comment on posts
- Users can view list of followers and following

**FR4: Feed**
- Users see a chronological feed of posts from people they follow
- Users can view individual posts
- Users can view other users' profiles and their posts

## 3. Non-Functional Requirements (Scale, Performance, Availability)

### Scale Requirements:
- **Daily Active Users (DAU):** 1 million
- **Total Users:** 5 million
- **Average posts per user:** 2 per week
- **Average follows per user:** 100
- **Read:Write Ratio:** 100:1 (more reads than writes)

### Performance Requirements:
- **Feed load time:** < 500ms
- **Photo upload:** < 3 seconds for 10MB image
- **API response time:** < 200ms for most operations
- **Image load time:** < 1 second (via CDN)

### Availability:
- **Target availability:** 99.9% (acceptable for MVP)
- **Data durability:** 99.99% (photos should not be lost)

### Other Requirements:
- **Consistency:** Eventual consistency acceptable for feed and counts
- **Security:** Secure authentication, HTTPS for all connections
- **Scalability:** Should handle 2x growth without major redesign

## 4. Back-of-envelope Calculations

### User Activity:
- **DAU:** 1 million
- **Average posts viewed per user per day:** 50
- **Average photos uploaded per day:** 1M users × 2 posts/week ÷ 7 = ~285,000 photos/day

### Storage Calculations:

**Photo Storage:**
- Average photo size: 2MB (after compression)
- Photos per day: 285,000
- Daily storage: 285,000 × 2MB = 570 GB/day
- Storage per year: 570 GB × 365 = ~208 TB/year
- With 3 sizes (original, medium, thumbnail): 208 TB × 3 = ~624 TB/year

**Metadata Storage:**
- Users: 5M × 1KB = 5 GB
- Posts: 285K × 365 × 1KB = ~104 GB/year
- Comments: ~10M × 500 bytes = 5 GB
- Likes: ~50M × 50 bytes = 2.5 GB
- Total metadata: ~120 GB/year (negligible)

**Total Storage (Year 1):** ~625 TB

### Bandwidth Calculations:

**Incoming (Upload):**
- 285,000 photos × 2MB = 570 GB/day
- Per second: 570 GB ÷ 86,400s = ~6.6 MB/s
- Peak (3x average): ~20 MB/s

**Outgoing (Download):**
- Feed views: 1M users × 50 posts = 50M image views/day
- Average image size (medium): 500KB
- 50M × 500KB = 25 TB/day
- Per second: 25 TB ÷ 86,400s = ~289 MB/s
- Peak (3x average): ~867 MB/s

**Bandwidth Summary:**
- Upload: ~20 MB/s (peak)
- Download: ~867 MB/s (peak) - **CDN is essential**

### Request Rate:

**API Calls:**
- Read operations: 1M users × 100 API calls/day = 100M requests/day
- Per second: 100M ÷ 86,400 = ~1,157 QPS
- Peak (3x): ~3,500 QPS

**Write Operations:**
- Posts: 285K/day = 3.3 QPS
- Likes: ~10M/day = 116 QPS
- Comments: ~2M/day = 23 QPS
- Total writes: ~142 QPS (peak: ~426 QPS)

## 5. High-Level Architecture Diagram Description

```
                                    [Users/Mobile Apps/Web Browsers]
                                                |
                                                v
                                        [DNS / Route 53]
                                                |
                                                v
                                    [CDN - CloudFront/CloudFlare]
                                    (Serves images, static content)
                                                |
                                                v
                                        [Load Balancer]
                                        (Distributes traffic)
                                                |
                                                v
                            +-------------------+-------------------+
                            |                   |                   |
                            v                   v                   v
                    [Web Server 1]      [Web Server 2]      [Web Server 3]
                    (API Handlers)      (API Handlers)      (API Handlers)
                            |                   |                   |
                            +-------------------+-------------------+
                                                |
                                                v
                                        [Application Layer]
                                                |
                            +-------------------+-------------------+
                            |                   |                   |
                            v                   v                   v
                    [Redis Cache]       [PostgreSQL]      [S3 / Object Storage]
                    (Feed cache,        (User data,       (Original images,
                     user sessions,     posts, likes,      resized versions)
                     like counts)       comments)                  |
                                                                   v
                                                            [Image Processing]
                                                            (Async workers for
                                                             resize/thumbnail)
```

**Components:**

1. **CDN:** Caches and serves images globally with low latency
2. **Load Balancer:** Distributes incoming requests across web servers
3. **Web Servers:** Handle API requests, authentication, business logic
4. **Redis Cache:** Fast in-memory cache for feeds, sessions, counters
5. **PostgreSQL:** Primary datastore for structured data
6. **S3 Storage:** Object storage for images (original and processed)
7. **Image Processing Workers:** Async workers to resize/optimize images

## 6. API Design (RESTful endpoints)

### Authentication APIs

```
POST /api/v1/auth/register
Request:
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "hashed_password",
  "full_name": "John Doe"
}
Response: 201 Created
{
  "user_id": "123456",
  "username": "john_doe",
  "access_token": "jwt_token"
}

POST /api/v1/auth/login
Request:
{
  "email": "john@example.com",
  "password": "password"
}
Response: 200 OK
{
  "user_id": "123456",
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

### User APIs

```
GET /api/v1/users/{user_id}
Response: 200 OK
{
  "user_id": "123456",
  "username": "john_doe",
  "full_name": "John Doe",
  "bio": "Photographer",
  "profile_pic_url": "https://cdn.../profile.jpg",
  "followers_count": 1500,
  "following_count": 300,
  "posts_count": 250
}

PUT /api/v1/users/{user_id}
Request:
{
  "full_name": "John Doe Jr.",
  "bio": "Travel photographer"
}
Response: 200 OK

GET /api/v1/users/{user_id}/posts?limit=20&offset=0
Response: 200 OK
{
  "posts": [...],
  "has_more": true
}
```

### Follow APIs

```
POST /api/v1/users/{user_id}/follow
Response: 201 Created

DELETE /api/v1/users/{user_id}/follow
Response: 204 No Content

GET /api/v1/users/{user_id}/followers?limit=50&offset=0
Response: 200 OK
{
  "users": [{"user_id": "...", "username": "..."}],
  "has_more": false
}

GET /api/v1/users/{user_id}/following?limit=50&offset=0
Response: 200 OK
```

### Post APIs

```
POST /api/v1/posts
Request: multipart/form-data
{
  "image": <file>,
  "caption": "Beautiful sunset!"
}
Response: 201 Created
{
  "post_id": "789012",
  "image_url": "https://cdn.../image.jpg",
  "caption": "Beautiful sunset!",
  "created_at": "2025-11-12T10:30:00Z"
}

GET /api/v1/posts/{post_id}
Response: 200 OK
{
  "post_id": "789012",
  "user_id": "123456",
  "username": "john_doe",
  "user_profile_pic": "https://cdn.../profile.jpg",
  "image_url": "https://cdn.../image.jpg",
  "caption": "Beautiful sunset!",
  "likes_count": 245,
  "comments_count": 12,
  "is_liked_by_me": true,
  "created_at": "2025-11-12T10:30:00Z"
}

DELETE /api/v1/posts/{post_id}
Response: 204 No Content
```

### Feed APIs

```
GET /api/v1/feed?limit=20&offset=0
Response: 200 OK
{
  "posts": [
    {
      "post_id": "789012",
      "user_id": "123456",
      "username": "john_doe",
      "user_profile_pic": "https://cdn.../profile.jpg",
      "image_url": "https://cdn.../image.jpg",
      "caption": "Beautiful sunset!",
      "likes_count": 245,
      "comments_count": 12,
      "is_liked_by_me": false,
      "created_at": "2025-11-12T10:30:00Z"
    }
  ],
  "has_more": true
}
```

### Like APIs

```
POST /api/v1/posts/{post_id}/like
Response: 201 Created

DELETE /api/v1/posts/{post_id}/like
Response: 204 No Content

GET /api/v1/posts/{post_id}/likes?limit=50&offset=0
Response: 200 OK
{
  "users": [{"user_id": "...", "username": "..."}],
  "total_count": 245,
  "has_more": true
}
```

### Comment APIs

```
POST /api/v1/posts/{post_id}/comments
Request:
{
  "text": "Amazing photo!"
}
Response: 201 Created
{
  "comment_id": "345678",
  "user_id": "123456",
  "username": "john_doe",
  "text": "Amazing photo!",
  "created_at": "2025-11-12T10:35:00Z"
}

GET /api/v1/posts/{post_id}/comments?limit=50&offset=0
Response: 200 OK
{
  "comments": [
    {
      "comment_id": "345678",
      "user_id": "123456",
      "username": "john_doe",
      "user_profile_pic": "https://cdn.../profile.jpg",
      "text": "Amazing photo!",
      "created_at": "2025-11-12T10:35:00Z"
    }
  ],
  "has_more": false
}

DELETE /api/v1/comments/{comment_id}
Response: 204 No Content
```

## 7. Database Design (Schema, Indexes)

### PostgreSQL Schema

```sql
-- Users Table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    profile_pic_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Posts Table
CREATE TABLE posts (
    post_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_medium_url VARCHAR(500),
    image_thumbnail_url VARCHAR(500),
    caption TEXT,
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

-- Followers Table (relationship between users)
CREATE TABLE followers (
    follower_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    followee_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_followers_follower ON followers(follower_id);
CREATE INDEX idx_followers_followee ON followers(followee_id);

-- Likes Table
CREATE TABLE likes (
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    post_id BIGINT NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id)
);

CREATE INDEX idx_likes_post_id ON likes(post_id);
CREATE INDEX idx_likes_user_id ON likes(user_id);
CREATE INDEX idx_likes_created ON likes(created_at DESC);

-- Comments Table
CREATE TABLE comments (
    comment_id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post_id ON comments(post_id, created_at DESC);
CREATE INDEX idx_comments_user_id ON comments(user_id);
```

### Key Design Decisions:

1. **User IDs:** Using BIGSERIAL for auto-incrementing IDs (can handle billions of users)
2. **Composite Primary Keys:** For likes and followers (prevents duplicates)
3. **Denormalized Counts:** likes_count and comments_count in posts table for performance
4. **Cascade Deletes:** When a user is deleted, their posts, likes, and comments are removed
5. **Indexes:**
   - B-tree indexes on foreign keys for joins
   - Composite index on (user_id, created_at) for user profile posts
   - Index on created_at DESC for chronological ordering

### Database Maintenance:

```sql
-- Update denormalized counts (can be done async)
UPDATE posts
SET likes_count = (SELECT COUNT(*) FROM likes WHERE post_id = posts.post_id)
WHERE post_id = ?;

-- Periodically update follower counts in users table
ALTER TABLE users ADD COLUMN followers_count INT DEFAULT 0;
ALTER TABLE users ADD COLUMN following_count INT DEFAULT 0;
```

## 8. Core Components

### A. Feed Generation Service

**Purpose:** Generate chronological feed for each user

**Implementation:**

```python
class FeedService:
    def get_feed(self, user_id, limit=20, offset=0):
        # 1. Check cache first
        cache_key = f"feed:{user_id}:{offset}"
        cached_feed = redis.get(cache_key)
        if cached_feed:
            return json.loads(cached_feed)

        # 2. Get list of users that the current user follows
        following_ids = db.query("""
            SELECT followee_id
            FROM followers
            WHERE follower_id = ?
        """, user_id)

        # 3. Get recent posts from followed users
        posts = db.query("""
            SELECT p.*, u.username, u.profile_pic_url,
                   EXISTS(SELECT 1 FROM likes
                          WHERE post_id = p.post_id
                          AND user_id = ?) as is_liked_by_me
            FROM posts p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.user_id IN (?)
            ORDER BY p.created_at DESC
            LIMIT ? OFFSET ?
        """, user_id, following_ids, limit, offset)

        # 4. Cache the result (5 minutes TTL)
        redis.setex(cache_key, 300, json.dumps(posts))

        return posts
```

**Optimization:**
- Cache feed for 5 minutes
- Invalidate cache when user follows/unfollows someone
- For users following many people, pre-generate feed asynchronously

### B. Media Storage

**Purpose:** Store and serve images efficiently

**Architecture:**

1. **Upload Flow:**
   ```
   Client -> API Server -> S3 (original image)
                        -> Message Queue (for processing)

   Image Processing Worker:
   - Reads from queue
   - Downloads original from S3
   - Generates 3 sizes:
     * Original (max 2048x2048)
     * Medium (640x640)
     * Thumbnail (150x150)
   - Uploads all sizes to S3
   - Updates database with URLs
   ```

2. **S3 Bucket Structure:**
   ```
   instagram-images/
   ├── original/
   │   └── {user_id}/{post_id}.jpg
   ├── medium/
   │   └── {user_id}/{post_id}_medium.jpg
   └── thumbnail/
       └── {user_id}/{post_id}_thumb.jpg
   ```

3. **Image Processing Service:**
   ```python
   class ImageProcessor:
       def process_image(self, post_id, original_url):
           # Download original
           image = download_from_s3(original_url)

           # Resize
           original = resize(image, max_size=2048)
           medium = resize(image, size=640)
           thumbnail = resize(image, size=150)

           # Optimize (compress)
           original = optimize_jpeg(original, quality=90)
           medium = optimize_jpeg(medium, quality=85)
           thumbnail = optimize_jpeg(thumbnail, quality=80)

           # Upload back to S3
           s3.upload(f"original/{post_id}.jpg", original)
           s3.upload(f"medium/{post_id}_medium.jpg", medium)
           s3.upload(f"thumbnail/{post_id}_thumb.jpg", thumbnail)

           # Update database
           db.update_post(post_id, {
               'image_medium_url': medium_url,
               'image_thumbnail_url': thumbnail_url
           })
   ```

### C. CDN Integration

**Purpose:** Serve images with low latency globally

**Configuration:**

1. **CloudFront/CloudFlare Setup:**
   - Origin: S3 bucket
   - Cache TTL: 1 year (images are immutable)
   - Cache key: Full URL
   - Compression: Enable Gzip/Brotli

2. **URL Structure:**
   ```
   https://cdn.instagram-mvp.com/original/12345/67890.jpg
   https://cdn.instagram-mvp.com/medium/12345/67890_medium.jpg
   https://cdn.instagram-mvp.com/thumbnail/12345/67890_thumb.jpg
   ```

3. **Benefits:**
   - Reduced latency (edge locations)
   - Reduced load on origin servers
   - Automatic scaling
   - DDoS protection

### D. Cache Layer

**Purpose:** Reduce database load and improve response times

**Redis Cache Strategy:**

```python
# 1. User Feed Cache
Key: feed:{user_id}:{offset}
TTL: 5 minutes
Invalidation: On new post by followed user, on follow/unfollow

# 2. User Profile Cache
Key: user:{user_id}
TTL: 1 hour
Invalidation: On profile update

# 3. Post Details Cache
Key: post:{post_id}
TTL: 10 minutes
Invalidation: On post update, on like/comment (debounced)

# 4. Like Counts Cache
Key: likes:{post_id}
TTL: 30 seconds
Update: Increment/decrement on like/unlike

# 5. Session Cache
Key: session:{token}
TTL: 24 hours
Data: user_id, permissions

# 6. Following List Cache
Key: following:{user_id}
TTL: 1 hour
Invalidation: On follow/unfollow
```

**Cache-Aside Pattern:**
```python
def get_post(post_id):
    # Try cache first
    cache_key = f"post:{post_id}"
    post = redis.get(cache_key)

    if post is None:
        # Cache miss - query database
        post = db.query("SELECT * FROM posts WHERE post_id = ?", post_id)
        # Store in cache
        redis.setex(cache_key, 600, json.dumps(post))
    else:
        post = json.loads(post)

    return post
```

### E. Notification System

**Purpose:** Notify users of likes, comments, and new followers

**Simple Implementation (MVP):**

1. **Notification Table:**
   ```sql
   CREATE TABLE notifications (
       notification_id BIGSERIAL PRIMARY KEY,
       user_id BIGINT NOT NULL REFERENCES users(user_id),
       actor_id BIGINT NOT NULL REFERENCES users(user_id),
       notification_type VARCHAR(20) NOT NULL, -- 'like', 'comment', 'follow'
       entity_id BIGINT, -- post_id or comment_id
       is_read BOOLEAN DEFAULT FALSE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE INDEX idx_notifications_user ON notifications(user_id, created_at DESC);
   CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read, created_at DESC);
   ```

2. **Notification Creation:**
   ```python
   def create_notification(user_id, actor_id, type, entity_id):
       # Don't notify self
       if user_id == actor_id:
           return

       # Create notification
       db.insert("""
           INSERT INTO notifications
           (user_id, actor_id, notification_type, entity_id)
           VALUES (?, ?, ?, ?)
       """, user_id, actor_id, type, entity_id)

       # Increment unread count in cache
       redis.incr(f"notifications:unread:{user_id}")
   ```

3. **Notification API:**
   ```
   GET /api/v1/notifications?limit=20&offset=0
   Response:
   {
       "notifications": [
           {
               "notification_id": "123",
               "actor": {"user_id": "456", "username": "jane_doe"},
               "type": "like",
               "post_id": "789",
               "is_read": false,
               "created_at": "2025-11-12T10:40:00Z"
           }
       ],
       "unread_count": 5
   }
   ```

4. **Push Notifications (Optional for MVP):**
   - Use Firebase Cloud Messaging (FCM) for mobile
   - Store device tokens in database
   - Send push when notification is created

## 9. Data Flow

### Flow 1: User Uploads a Photo

```
1. User selects photo in mobile app
2. App uploads photo to API server
   POST /api/v1/posts
   - Multipart form data with image file
3. API server:
   - Validates authentication token
   - Validates image size/format
   - Generates unique post_id
4. Upload original image to S3
   - Key: original/{user_id}/{post_id}.jpg
   - Returns S3 URL
5. Insert post record in database
   INSERT INTO posts (user_id, image_url, caption)
6. Publish message to image processing queue
   {
       "post_id": "123",
       "original_url": "s3://bucket/original/..."
   }
7. Return response to client
   {
       "post_id": "123",
       "image_url": "https://cdn.../original/..."
   }
8. [Async] Image processing worker:
   - Reads message from queue
   - Downloads original image from S3
   - Generates medium and thumbnail versions
   - Uploads to S3
   - Updates database with new URLs
9. [Async] Invalidate follower feeds
   - Get list of followers
   - Delete cached feeds for each follower
```

### Flow 2: User Views Feed

```
1. User opens app / refreshes feed
2. App requests feed from API
   GET /api/v1/feed?limit=20&offset=0
3. API server:
   - Validates authentication token
   - Extracts user_id from token
4. Check Redis cache
   - Key: feed:{user_id}:0
5. If cache HIT:
   - Return cached feed data
   - [Response time: ~50ms]
6. If cache MISS:
   - Query database for following list
     SELECT followee_id FROM followers WHERE follower_id = ?
   - Query database for posts from followed users
     SELECT posts with user info, ordered by created_at DESC
   - For each post, check if current user liked it
   - Store result in Redis (TTL: 5 minutes)
   - Return feed data
   - [Response time: ~200ms]
7. Client receives feed
8. Client requests images from CDN
   - CDN serves from edge location
   - If not in CDN cache, fetches from S3
```

### Flow 3: User Likes a Post

```
1. User taps like button
2. App sends like request
   POST /api/v1/posts/{post_id}/like
3. API server:
   - Validates authentication token
   - Checks if user already liked the post
4. Insert like record
   INSERT INTO likes (user_id, post_id) VALUES (?, ?)
5. Update like count in cache
   INCR likes:{post_id}
6. Asynchronously update database count
   UPDATE posts SET likes_count = likes_count + 1 WHERE post_id = ?
7. Create notification for post owner
   INSERT INTO notifications (user_id, actor_id, type, entity_id)
8. Return success response
9. Client updates UI optimistically
```

### Flow 4: User Follows Another User

```
1. User taps follow button on profile
2. App sends follow request
   POST /api/v1/users/{user_id}/follow
3. API server:
   - Validates authentication token
   - Checks if already following
4. Insert follower relationship
   INSERT INTO followers (follower_id, followee_id) VALUES (?, ?)
5. Invalidate caches:
   - DELETE following:{follower_id}
   - DELETE feed:{follower_id}:*
6. Create notification
   INSERT INTO notifications (user_id, actor_id, type)
7. Return success response
8. Client updates UI
```

## 10. Scalability Considerations

### Current Bottlenecks:

1. **Database Read Load:**
   - Problem: Feed generation requires querying all posts from followed users
   - Solution: Implement Redis cache with 5-minute TTL
   - Future: Pre-generate feeds asynchronously (fanout on write)

2. **Image Storage:**
   - Problem: S3 can handle scale, but costs increase
   - Solution: Use CDN aggressively to reduce S3 requests
   - Future: Implement tiered storage (hot/warm/cold)

3. **Single Database:**
   - Problem: Single PostgreSQL instance is a bottleneck
   - Solution: Read replicas for read-heavy operations
   - Future: Shard database by user_id

### Scaling Strategies:

**Phase 1: Vertical Scaling (Current MVP)**
- Single PostgreSQL instance (16 cores, 64GB RAM)
- Redis cache (8GB)
- Multiple stateless web servers behind load balancer
- S3 + CloudFront CDN

**Phase 2: Read Replicas (10M users)**
- Master-slave PostgreSQL replication
- Read queries go to slaves
- Write queries go to master
- Connection pooling (PgBouncer)

**Phase 3: Caching Layer (50M users)**
- Larger Redis cluster
- Cache all feeds for 5-10 minutes
- Cache user profiles for 1 hour
- Cache-aside pattern for all reads

**Phase 4: Database Sharding (100M+ users)**
- Shard by user_id (consistent hashing)
- Each shard handles subset of users
- Application layer routes queries to correct shard
- Cross-shard queries avoided or done asynchronously

**Phase 5: Microservices (500M+ users)**
- Split into separate services:
  * User Service
  * Post Service
  * Feed Service
  * Notification Service
- Each service has its own database
- Use message queues for inter-service communication

### Monitoring and Metrics:

```
Key metrics to track:
- API response times (p50, p95, p99)
- Database query times
- Cache hit rates
- Image processing queue length
- Error rates per endpoint
- Active users (concurrent)
- Database connection pool usage
```

## 11. Trade-offs

### 1. Chronological Feed vs. Algorithmic Feed

**Decision: Chronological Feed**

**Pros:**
- Simple to implement (ORDER BY created_at DESC)
- Fast queries with proper indexing
- Predictable behavior
- No complex recommendation system needed

**Cons:**
- Less engaging than algorithmic feed
- Users might miss important posts
- No personalization

**Rationale:** For MVP, simplicity is key. Can add algorithmic ranking later.

---

### 2. Eventual Consistency vs. Strong Consistency

**Decision: Eventual Consistency for counts and feeds**

**Pros:**
- Better performance (no locks)
- Higher availability
- Reduced database load

**Cons:**
- Like counts might be slightly off
- Feed might not be immediately updated
- Can confuse users in rare cases

**Rationale:** Users don't notice 1-2 second delays in counts. Performance > precision.

---

### 3. Fanout on Write vs. Fanout on Read (Feed Generation)

**Decision: Fanout on Read (with caching)**

**Pros:**
- No storage overhead for feeds
- Works for users with millions of followers
- Easier to implement initially

**Cons:**
- Slower feed generation (database query needed)
- More complex queries

**Rationale:** For MVP with 1M users, fanout on read + cache is sufficient.

**Future:** Hybrid approach - fanout on write for regular users, fanout on read for celebrities.

---

### 4. SQL vs. NoSQL Database

**Decision: PostgreSQL (SQL)**

**Pros:**
- Strong consistency and ACID guarantees
- Powerful queries and joins
- Mature ecosystem and tools
- Good for structured data (users, posts, relationships)

**Cons:**
- Harder to scale horizontally
- Might need sharding at very large scale

**Rationale:** Social graph is relational. PostgreSQL is perfect for MVP.

---

### 5. Synchronous vs. Asynchronous Image Processing

**Decision: Asynchronous processing**

**Pros:**
- API responds immediately (better UX)
- Can handle spikes in uploads
- Processing doesn't block web servers

**Cons:**
- More complex architecture
- Thumbnails not immediately available
- Requires message queue and workers

**Rationale:** Image processing is slow. Async is essential for good UX.

---

### 6. Normalized vs. Denormalized Counts

**Decision: Denormalized (store counts in posts table)**

**Pros:**
- Extremely fast reads (no COUNT query)
- Reduces database load significantly
- Simple to display in feed

**Cons:**
- Requires updates on every like/comment
- Can become inconsistent
- Need periodic reconciliation

**Rationale:** Read:Write ratio is 100:1. Optimize for reads.

## 12. Follow-up Questions

### Functional Requirements:

1. **Q: How do we handle users with millions of followers (celebrities)?**
   - A: Hybrid fanout approach - don't update all follower feeds immediately
   - Use fanout on read for celebrities, cache their popular posts
   - Implement "verified" user tier with special handling

2. **Q: Should we support private accounts?**
   - A: Yes, add `is_private` field to users table
   - Check privacy before showing posts in feed
   - Require approval for follow requests (new table)

3. **Q: How do we handle deleted posts?**
   - A: Soft delete initially (add `deleted_at` timestamp)
   - Hard delete after 30 days (compliance)
   - Remove from CDN cache immediately

4. **Q: What about spam and abuse?**
   - A: Add reporting mechanism
   - Rate limit post creation (max 10 per hour)
   - Implement content moderation (manual or AI)

### Scale & Performance:

5. **Q: What if database becomes bottleneck?**
   - A: Implement read replicas (master-slave)
   - Aggressive caching strategy
   - Consider sharding by user_id for writes

6. **Q: How to handle millions of concurrent users?**
   - A: Horizontal scaling of web servers (stateless)
   - Connection pooling for database
   - Redis cluster for distributed caching
   - Global load balancing (multi-region)

7. **Q: What about image storage costs?**
   - A: Lifecycle policies (move old images to cheaper storage)
   - Delete thumbnails for very old posts
   - Compress more aggressively for old content

8. **Q: How to reduce CDN costs?**
   - A: Serve lower quality images on mobile data
   - Lazy load images (only visible content)
   - Implement progressive image loading

### Availability & Reliability:

9. **Q: What if S3 goes down?**
   - A: Multi-region S3 replication
   - Graceful degradation (show placeholders)
   - Queue image uploads and retry

10. **Q: How to ensure zero data loss?**
    - A: Database backups (continuous)
    - S3 versioning enabled
    - Transaction logs for point-in-time recovery

11. **Q: What's the disaster recovery plan?**
    - A: Automated backups every 6 hours
    - Multi-region database replication
    - Recovery Time Objective (RTO): 4 hours
    - Recovery Point Objective (RPO): 1 hour

### Security:

12. **Q: How to prevent unauthorized access?**
    - A: JWT tokens with expiration
    - HTTPS everywhere
    - Rate limiting per IP and per user
    - Input validation and sanitization

13. **Q: How to handle GDPR compliance?**
    - A: Implement user data export
    - Account deletion removes all user data
    - Anonymize data for analytics

### Future Features:

14. **Q: How would you add stories (24-hour posts)?**
    - A: Separate table with TTL
    - Redis sorted set for chronological ordering
    - Automated deletion after 24 hours
    - Separate storage bucket with lifecycle policy

15. **Q: How to add direct messaging?**
    - A: New service with WebSocket connections
    - Message queue for delivery
    - Read receipts using Redis
    - Encrypt messages at rest

---

**Estimated Interview Time:** 45-60 minutes for complete discussion

**Difficulty Level:** Easy (focuses on core concepts without complex algorithms)

**Key Learning Points:**
- Basic system design principles
- Database schema design
- API design best practices
- Caching strategies
- Media storage and CDN usage
- Simple feed generation
