# Design Netflix (Video Streaming with Recommendations & CDN)

**Difficulty:** Medium

## 1. Problem Statement

Design a subscription-based video streaming service like Netflix that provides on-demand access to a catalog of movies and TV shows. The system should support millions of concurrent users globally, provide personalized recommendations, deliver high-quality streaming with minimal buffering, and handle various network conditions.

**Key Differences from YouTube:**
- Curated catalog (not user-generated content)
- Subscription model (not ad-supported)
- Pre-encoded content (not real-time upload/transcoding)
- Focus on binge-watching experience
- Download for offline viewing

## 2. Requirements

### Functional Requirements
1. **Content Catalog**: Browse movies/shows by genre, popularity, new releases
2. **Video Streaming**: High-quality adaptive streaming
3. **User Profiles**: Multiple profiles per account (family sharing)
4. **Personalized Recommendations**: Homepage tailored to user preferences
5. **Search**: Find content by title, actor, director, genre
6. **Continue Watching**: Resume from last watched position
7. **Offline Downloads**: Download content for offline viewing
8. **Watch History**: Track what user has watched
9. **Rating System**: Like/dislike content

### Non-Functional Requirements
1. **Availability**: 99.99% uptime
2. **Scalability**:
   - 200+ million subscribers
   - 15+ million concurrent streams (peak)
   - 5+ billion hours streamed per quarter
3. **Performance**:
   - Start streaming within 2 seconds
   - Zero buffering for 99% of plays
   - CDN hit rate > 95%
4. **Quality**:
   - Support 4K/HDR for premium content
   - Adaptive bitrate (144p to 4K)
5. **Global Coverage**: Available in 190+ countries
6. **Cost Efficiency**: Optimize CDN and storage costs

### Out of Scope
- Content creation/production
- Payment processing
- Subtitles generation
- Parental controls (can be added later)

## 3. Storage Estimation

### Assumptions
- **Total Subscribers**: 200 million
- **Content Library**: 10,000 titles (movies + shows)
- **Average Title Length**: 90 minutes
- **Active Users**: 50 million daily
- **Peak Concurrent Streams**: 15 million
- **Average Watch Time**: 2 hours/day per active user
- **Download Feature**: 10% of users download content

### Calculations

**Content Storage:**
```
Per movie encoding:
- 4K (15 Mbps): 90 min × 60 × 15 Mbps / 8 = 10.125 GB
- 1080p (5 Mbps): 90 min × 60 × 5 Mbps / 8 = 3.375 GB
- 720p (3 Mbps): 90 min × 60 × 3 Mbps / 8 = 2.025 GB
- 480p (1.5 Mbps): 90 min × 60 × 1.5 Mbps / 8 = 1.0125 GB
- 360p (0.8 Mbps): 90 min × 60 × 0.8 Mbps / 8 = 0.54 GB
Total per title: ~17 GB (all qualities)

Multiple audio tracks (5 languages): +2 GB
Multiple subtitle files: +50 MB
Total per title: ~19 GB

Total Library: 10,000 titles × 19 GB = 190 TB
With replication (3x): 570 TB
```

**CDN Cache Storage:**
```
Popular content (20% of catalog, 80% of traffic): 2,000 titles
Cache at edge: 2,000 × 19 GB = 38 TB per edge location
With 150+ edge locations: 5.7 PB total CDN cache
```

**Daily Streaming Volume:**
```
50M active users × 2 hours/day × 3 Mbps avg bitrate
= 100M hours × 3 Mbps
= 300M Mbps-hours
= 300M × 3600 seconds × 3 Mbps / 8 bits
= 4.05 Petabytes/day
```

**Peak Bandwidth:**
```
15M concurrent streams × 5 Mbps avg = 75,000,000 Mbps = 75 Tbps
```

**Metadata Storage:**
```
Per title: 50 KB (metadata, cast, crew, thumbnails references)
10,000 titles × 50 KB = 500 MB

User data (per user): 10 KB (profiles, watch history, preferences)
200M users × 10 KB = 2 TB

Total Metadata: ~2 TB
```

**Watch History Storage:**
```
Per viewing session: 200 bytes (user_id, title_id, timestamp, position)
50M daily active × 3 sessions/day = 150M sessions/day
150M × 200 bytes = 30 GB/day
Annual: 30 GB × 365 = 10.95 TB/year
```

## 4. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Web Client│ │Mobile App│ │Smart TV  │ │Game      │     │
│  │          │ │(iOS/And.)│ │(Roku/LG) │ │Console   │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS
                           ▼
        ┌──────────────────────────────────────┐
        │      Netflix Open Connect            │
        │     (Custom CDN - 150+ PoPs)         │
        │   ┌────────────────────────────┐     │
        │   │  Cache Servers (ISP Embed) │     │
        │   └────────────────────────────┘     │
        └─────────────┬────────────────────────┘
                      │
          ┌───────────┴──────────┐
          │                      │
          ▼                      ▼
    ┌───────────┐         ┌───────────┐
    │  Origin   │         │  Origin   │
    │ (Fallback)│         │ (Backup)  │
    └───────────┘         └───────────┘
          │
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│                 Backend Services (AWS)                  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   API        │  │ Play Service │  │Recommendation│ │
│  │  Gateway     │  │              │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Search     │  │   User       │  │  Analytics  │ │
│  │   Service    │  │   Service    │  │   Service   │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │  Content     │  │  Download    │                   │
│  │  Service     │  │  Service     │                   │
│  └──────────────┘  └──────────────┘                   │
└──────────────┬──────────────────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌──────────────┐
│Cassandra│ │DynamoDB │ │  Redis/      │
│(Watch   │ │(User    │ │  ElastiCache │
│History) │ │Metadata)│ │  (Cache)     │
└─────────┘ └─────────┘ └──────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   S3 / Cloud Storage │
    │   - Video files      │
    │   - Artwork/Images   │
    │   - Metadata         │
    └──────────────────────┘
```

### Key Components

1. **Netflix Open Connect (OC)**: Custom CDN with cache servers embedded in ISPs
2. **API Gateway**: Entry point for all client requests
3. **Play Service**: Handles playback sessions, streaming URLs
4. **Recommendation Service**: ML-based personalized recommendations
5. **Search Service**: Content discovery via search
6. **User Service**: User accounts, profiles, preferences
7. **Content Service**: Content metadata, catalog management
8. **Download Service**: Offline download management
9. **Analytics Service**: View tracking, A/B testing
10. **Cassandra**: Watch history, viewing activity (time-series)
11. **DynamoDB**: User data, subscriptions
12. **ElastiCache/Redis**: Caching layer
13. **S3**: Origin storage for video files and assets

## 5. API Design

### Content Discovery

#### Get Homepage
```http
GET /api/v1/homepage?profile_id=profile_123
Authorization: Bearer {token}

Response (200 OK):
{
  "rows": [
    {
      "id": "trending_now",
      "title": "Trending Now",
      "type": "carousel",
      "items": [
        {
          "title_id": "movie_abc",
          "title": "The Algorithm",
          "type": "movie",
          "thumbnail": "https://cdn.netflix.com/images/movie_abc_landscape.jpg",
          "match_score": 95, // Personalized match %
          "duration": 120,
          "rating": "PG-13",
          "year": 2024
        }
      ]
    },
    {
      "id": "because_you_watched",
      "title": "Because You Watched 'Stranger Things'",
      "type": "carousel",
      "items": [...]
    },
    {
      "id": "continue_watching",
      "title": "Continue Watching",
      "items": [
        {
          "title_id": "show_xyz",
          "episode_id": "ep_s02e05",
          "progress": 0.65, // 65% watched
          "thumbnail": "...",
          "time_left": 420 // seconds
        }
      ]
    }
  ]
}
```

#### Get Title Details
```http
GET /api/v1/titles/{title_id}?profile_id=profile_123
Authorization: Bearer {token}

Response (200 OK):
{
  "title_id": "movie_abc",
  "type": "movie",
  "title": "The Algorithm",
  "description": "A gripping tale of...",
  "year": 2024,
  "duration": 120,
  "rating": "PG-13",
  "genres": ["Thriller", "Sci-Fi"],
  "cast": [
    {"name": "Actor A", "role": "Protagonist"},
    {"name": "Actor B", "role": "Antagonist"}
  ],
  "director": "Director X",
  "match_score": 95,
  "media": {
    "thumbnail": "https://cdn.netflix.com/images/movie_abc_portrait.jpg",
    "hero_image": "https://cdn.netflix.com/images/movie_abc_hero.jpg",
    "trailer": "https://cdn.netflix.com/trailers/movie_abc.mp4"
  },
  "available_qualities": ["4K", "1080p", "720p", "480p"],
  "audio_tracks": [
    {"language": "en", "type": "original"},
    {"language": "es", "type": "dubbed"},
    {"language": "fr", "type": "dubbed"}
  ],
  "subtitles": ["en", "es", "fr", "de", "ja"]
}
```

### Playback

#### Start Playback Session
```http
POST /api/v1/play
Authorization: Bearer {token}

Request:
{
  "profile_id": "profile_123",
  "title_id": "movie_abc",
  "episode_id": null, // For shows
  "quality": "auto", // or specific: 4K, 1080p, etc.
  "device_id": "device_xyz"
}

Response (200 OK):
{
  "session_id": "session_abc123",
  "streaming_urls": {
    "manifest": "https://oc.netflix.com/manifest/movie_abc.mpd",
    "hls": "https://oc.netflix.com/hls/movie_abc/master.m3u8"
  },
  "token": "eyJ...", // Streaming auth token
  "expires_at": "2025-11-12T14:00:00Z",
  "available_qualities": [
    {
      "quality": "4K",
      "bitrate": 25000, // kbps
      "resolution": "3840x2160",
      "cdn_url": "https://oc-east.netflix.com/..."
    },
    {
      "quality": "1080p",
      "bitrate": 5000,
      "resolution": "1920x1080",
      "cdn_url": "https://oc-east.netflix.com/..."
    }
  ],
  "resume_position": 0, // seconds
  "duration": 7200
}
```

#### Update Playback Progress
```http
POST /api/v1/play/{session_id}/progress
Authorization: Bearer {token}

Request:
{
  "position": 1800, // seconds
  "timestamp": "2025-11-12T12:30:00Z"
}

Response (200 OK):
{
  "updated": true
}
```

#### End Playback Session
```http
POST /api/v1/play/{session_id}/stop
Authorization: Bearer {token}

Request:
{
  "position": 5400,
  "completed": false,
  "quality_played": "1080p",
  "buffering_events": 2
}

Response (200 OK):
{
  "session_ended": true,
  "watch_time": 5400
}
```

### User Profiles

#### Get User Profiles
```http
GET /api/v1/profiles
Authorization: Bearer {token}

Response (200 OK):
{
  "profiles": [
    {
      "profile_id": "profile_123",
      "name": "John",
      "avatar": "https://cdn.netflix.com/avatars/avatar_1.png",
      "kids_profile": false,
      "language": "en"
    },
    {
      "profile_id": "profile_456",
      "name": "Kids",
      "avatar": "https://cdn.netflix.com/avatars/avatar_kids.png",
      "kids_profile": true,
      "language": "en"
    }
  ],
  "max_profiles": 5
}
```

### Search

#### Search Content
```http
GET /api/v1/search?q=stranger+things&profile_id=profile_123
Authorization: Bearer {token}

Response (200 OK):
{
  "query": "stranger things",
  "results": [
    {
      "title_id": "show_xyz",
      "type": "show",
      "title": "Stranger Things",
      "year": 2016,
      "thumbnail": "...",
      "match_score": 98,
      "seasons": 4
    },
    {
      "title_id": "movie_similar",
      "type": "movie",
      "title": "Super 8",
      "match_score": 85
    }
  ],
  "total_results": 15,
  "search_time_ms": 87
}
```

### Download (Offline)

#### Get Download Options
```http
GET /api/v1/downloads/{title_id}/options
Authorization: Bearer {token}

Response (200 OK):
{
  "title_id": "movie_abc",
  "available_qualities": [
    {"quality": "High", "size": 2147483648, "bitrate": 3000},
    {"quality": "Medium", "size": 1073741824, "bitrate": 1500},
    {"quality": "Low", "size": 536870912, "bitrate": 800}
  ],
  "expiry_policy": "Downloaded content expires 48 hours after first play",
  "max_downloads": 100 // Per account
}
```

#### Request Download
```http
POST /api/v1/downloads
Authorization: Bearer {token}

Request:
{
  "title_id": "movie_abc",
  "episode_id": null,
  "quality": "High",
  "profile_id": "profile_123",
  "device_id": "device_xyz"
}

Response (200 OK):
{
  "download_id": "dl_abc123",
  "download_url": "https://download.netflix.com/movie_abc/high.enc",
  "license_url": "https://api.netflix.com/licenses/dl_abc123",
  "size": 2147483648,
  "expires_at": "2025-12-12T00:00:00Z"
}
```

## 6. Storage Strategy

### Content Storage

**Multi-Tier Storage:**

```
Tier 1: CDN Edge (Open Connect Appliances)
- Location: Embedded in ISP data centers
- Storage: 100+ TB SSD per appliance
- Content: Top 20% most popular titles (80% of traffic)
- Cost: Netflix provides hardware to ISPs

Tier 2: Regional Origin
- Location: AWS regions (US-East, EU-West, Asia-Pacific)
- Storage: S3 with CloudFront
- Content: Full catalog
- Cost: Medium

Tier 3: Archive
- Location: S3 Glacier
- Content: Original masters, unused formats
- Cost: Low
```

**File Organization:**
```
s3://netflix-content/
├── titles/
│   ├── movie_abc/
│   │   ├── master/
│   │   │   └── original_4K_HDR.mp4
│   │   ├── 4K/
│   │   │   ├── manifest.mpd
│   │   │   ├── video/
│   │   │   │   ├── segment_0.m4s
│   │   │   │   └── segment_1.m4s
│   │   │   └── audio/
│   │   │       ├── en/
│   │   │       ├── es/
│   │   │       └── fr/
│   │   ├── 1080p/
│   │   ├── 720p/
│   │   ├── 480p/
│   │   └── 360p/
│   └── show_xyz/
│       ├── s01/
│       │   ├── e01/
│       │   └── e02/
│       └── s02/
├── artwork/
│   ├── movie_abc/
│   │   ├── portrait.jpg
│   │   ├── landscape.jpg
│   │   └── hero.jpg
└── metadata/
    └── catalog.json
```

### Database Schema

**DynamoDB Tables:**

```javascript
// Users Table
{
  TableName: "netflix_users",
  KeySchema: [
    { AttributeName: "user_id", KeyType: "HASH" }
  ],
  Attributes: {
    user_id: "user_123",
    email: "user@example.com",
    subscription_tier: "premium", // basic, standard, premium
    subscription_status: "active",
    subscription_expires: "2026-11-12T00:00:00Z",
    created_at: "2020-01-15T00:00:00Z",
    country: "US",
    payment_method_id: "pm_abc"
  }
}

// Profiles Table
{
  TableName: "netflix_profiles",
  KeySchema: [
    { AttributeName: "profile_id", KeyType: "HASH" }
  ],
  GlobalSecondaryIndexes: [
    { IndexName: "user_id_index", Key: "user_id" }
  ],
  Attributes: {
    profile_id: "profile_123",
    user_id: "user_123",
    name: "John",
    avatar_id: "avatar_1",
    kids_profile: false,
    language: "en",
    viewing_preferences: {
      auto_play_next: true,
      auto_play_previews: false
    }
  }
}

// Content Catalog Table
{
  TableName: "netflix_catalog",
  KeySchema: [
    { AttributeName: "title_id", KeyType: "HASH" }
  ],
  GlobalSecondaryIndexes: [
    { IndexName: "genre_index", Key: "genre" },
    { IndexName: "release_date_index", Key: "release_date" }
  ],
  Attributes: {
    title_id: "movie_abc",
    type: "movie", // or "show"
    title: "The Algorithm",
    description: "...",
    year: 2024,
    duration: 7200, // seconds
    rating: "PG-13",
    genres: ["Thriller", "Sci-Fi"],
    cast: [...],
    director: "Director X",
    available_qualities: ["4K", "1080p", "720p"],
    audio_languages: ["en", "es", "fr"],
    subtitle_languages: ["en", "es", "fr", "de"],
    artwork: {
      portrait: "s3://...",
      landscape: "s3://...",
      hero: "s3://..."
    },
    content_urls: {
      "4K": "s3://...",
      "1080p": "s3://..."
    },
    popularity_score: 0.95,
    release_date: "2024-11-01",
    availability: {
      countries: ["US", "CA", "UK", "FR"],
      expires_at: "2026-11-01" // License expiry
    }
  }
}
```

**Cassandra Tables (Time-Series Data):**

```sql
-- Watch history
CREATE TABLE watch_history (
    profile_id UUID,
    timestamp TIMESTAMP,
    title_id UUID,
    episode_id UUID,
    position INT, -- seconds
    duration INT,
    completed BOOLEAN,
    device_id UUID,
    quality TEXT,

    PRIMARY KEY ((profile_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Playback sessions
CREATE TABLE playback_sessions (
    session_id UUID PRIMARY KEY,
    profile_id UUID,
    title_id UUID,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    total_watch_time INT, -- seconds
    buffering_events INT,
    average_bitrate INT,
    device_info TEXT,
    cdn_node TEXT
);

-- Title popularity (for recommendations)
CREATE TABLE title_popularity (
    date DATE,
    title_id UUID,
    view_count BIGINT,
    watch_time BIGINT, -- total seconds
    completion_rate DOUBLE,
    rating_avg DOUBLE,

    PRIMARY KEY ((date), view_count, title_id)
) WITH CLUSTERING ORDER BY (view_count DESC);
```

## 7. Video Encoding & Processing

### Encoding Pipeline

**Netflix Approach: Optimized Encoding**

Unlike YouTube (user content), Netflix controls all content and can optimize encoding per title.

```
Original Master (4K HDR ProRes)
    ↓
Content Analysis
├─→ Scene complexity detection
├─→ Motion analysis
├─→ Color grading analysis
└─→ Optimal bitrate calculation (Per-Title Encoding)
    ↓
Parallel Encoding (AWS Batch)
├─→ 4K (HDR10, Dolby Vision)
│   └─→ Bitrate: 15-25 Mbps (dynamic per scene)
├─→ 1080p
│   └─→ Bitrate: 4-6 Mbps
├─→ 720p
│   └─→ Bitrate: 2-4 Mbps
├─→ 480p
│   └─→ Bitrate: 0.8-1.5 Mbps
└─→ 360p/240p (mobile)
    └─→ Bitrate: 0.4-0.8 Mbps
    ↓
Segment Generation (DASH/HLS)
├─→ 2-10 second segments
└─→ Multiple codec support (H.264, VP9, AV1)
    ↓
Quality Verification
├─→ Automated QC (VMAF score)
└─→ Manual review for premium content
    ↓
Upload to Origin S3
    ↓
Populate CDN Cache (Open Connect)
    ↓
Ready for Streaming
```

### Per-Title Encoding

**Problem:** Fixed bitrate wastes bandwidth for simple scenes

**Solution:** Analyze each title, optimize bitrate per scene

```python
def optimize_encoding(video_file):
    # 1. Analyze video complexity
    scenes = detect_scenes(video_file)
    complexity_scores = []

    for scene in scenes:
        # Calculate complexity (motion, detail, color variance)
        complexity = calculate_scene_complexity(scene)
        complexity_scores.append(complexity)

    # 2. Determine optimal bitrate per quality tier
    bitrate_ladder = {
        "4K": [],
        "1080p": [],
        "720p": []
    }

    for quality in bitrate_ladder.keys():
        for scene, complexity in zip(scenes, complexity_scores):
            # Simple scene: lower bitrate
            # Complex scene: higher bitrate
            bitrate = calculate_optimal_bitrate(quality, complexity)
            bitrate_ladder[quality].append(bitrate)

    # 3. Encode with variable bitrate
    for quality, bitrates in bitrate_ladder.items():
        encode_video(video_file, quality, bitrates)

    # 4. Validate quality (VMAF score)
    for quality in bitrate_ladder.keys():
        encoded_file = f"output_{quality}.mp4"
        vmaf_score = calculate_vmaf(original=video_file, encoded=encoded_file)

        # Target: VMAF > 95 for high quality
        if vmaf_score < 95:
            # Re-encode with higher bitrate
            adjust_and_reencode(encoded_file, vmaf_score)
```

**Results:**
- Simple animations: 50% bandwidth savings
- Complex action scenes: Maintained quality
- Overall: 20-30% bandwidth reduction across catalog

## 8. Netflix Open Connect (CDN)

### Architecture

**Traditional CDN vs. Open Connect:**

```
Traditional CDN:
User → ISP → CDN PoP (3rd party) → Origin
- Multiple hops
- ISP pays transit costs
- Limited control

Netflix Open Connect:
User → ISP → OC Appliance (in ISP) → Origin (fallback)
- Single hop within ISP
- Free for ISPs (Netflix provides hardware)
- Optimal performance
```

**Open Connect Appliance (OCA):**

```
Hardware Specs:
- Storage: 100-200 TB SSD
- RAM: 256 GB
- Network: 100 Gbps
- Serves: 10,000-30,000 concurrent streams

Software:
- FreeBSD OS
- nginx for HTTP serving
- Custom cache management
- Nightly content refresh
```

### Content Distribution

**Fill Algorithm (Nightly):**

```python
class OpenConnectFillAlgorithm:
    def __init__(self, oca_capacity, region):
        self.capacity = oca_capacity
        self.region = region
        self.titles_to_cache = []

    def calculate_nightly_fill(self):
        # 1. Get popularity data for region
        popularity = get_regional_popularity(self.region)

        # 2. Predict next day's demand
        predicted_titles = []
        for title in popularity:
            demand_score = self.predict_demand(title)
            predicted_titles.append((title, demand_score))

        # 3. Sort by expected demand
        predicted_titles.sort(key=lambda x: x[1], reverse=True)

        # 4. Fill cache with top titles (knapsack problem)
        used_capacity = 0
        for title, score in predicted_titles:
            title_size = get_title_size(title)

            if used_capacity + title_size <= self.capacity:
                self.titles_to_cache.append(title)
                used_capacity += title_size
            else:
                break

        return self.titles_to_cache

    def predict_demand(self, title):
        # Factors:
        # - Historical views in region
        # - New release bonus
        # - Seasonal trends (e.g., horror in October)
        # - Similar title performance
        # - Marketing campaigns

        score = 0

        # Historical popularity
        views_last_week = get_views(title, region=self.region, days=7)
        score += views_last_week * 0.5

        # Trending
        if is_trending(title):
            score += 10000

        # New release
        if is_new_release(title):
            score += 5000

        # Seasonal
        if matches_seasonal_trend(title):
            score += 2000

        return score
```

### Cache Hit Rate

**Target: 95%+ hit rate**

**Strategies:**
1. **Predictive Caching**: Pre-fill popular content
2. **Regional Optimization**: Different cache per region
3. **Time-Based Updates**: Refresh during low-traffic hours
4. **Long-Tail Strategy**: Less popular content stays at origin

```python
def calculate_cache_hit_rate():
    # Metrics
    total_requests = 1000000
    cache_hits = 950000
    cache_misses = 50000

    hit_rate = cache_hits / total_requests
    print(f"Cache Hit Rate: {hit_rate * 100}%")  # 95%

    # Cost savings
    origin_cost_per_gb = 0.01  # $0.01/GB
    avg_video_size_gb = 2

    # Without cache: All requests hit origin
    cost_without_cache = total_requests * avg_video_size_gb * origin_cost_per_gb
    # = 1M * 2 * $0.01 = $20,000

    # With cache: Only misses hit origin
    cost_with_cache = cache_misses * avg_video_size_gb * origin_cost_per_gb
    # = 50K * 2 * $0.01 = $1,000

    savings = cost_without_cache - cost_with_cache
    print(f"Cost Savings: ${savings}")  # $19,000 per 1M requests
```

## 9. Recommendation System

### Multi-Armed Bandit Approach

**Netflix uses sophisticated ML, but simplified here:**

```
Homepage Generation:
1. Candidate Generation (Top N thousands)
2. Ranking (Top 100-200)
3. Diversification (Final 50-80)
4. Personalized Rows
```

### Recommendation Models

**1. Collaborative Filtering:**
```python
def collaborative_filtering(profile_id):
    # Find similar users based on viewing history
    user_vector = get_user_viewing_vector(profile_id)

    similar_users = []
    for other_user in all_users:
        if other_user == profile_id:
            continue

        other_vector = get_user_viewing_vector(other_user)
        similarity = cosine_similarity(user_vector, other_vector)

        if similarity > 0.7:  # Threshold
            similar_users.append((other_user, similarity))

    # Get titles watched by similar users
    recommendations = []
    for user, similarity in similar_users:
        user_titles = get_watched_titles(user)
        for title in user_titles:
            if not has_watched(profile_id, title):
                score = similarity * get_title_rating(user, title)
                recommendations.append((title, score))

    # Aggregate and sort
    aggregated = aggregate_scores(recommendations)
    return sorted(aggregated, key=lambda x: x[1], reverse=True)
```

**2. Content-Based Filtering:**
```python
def content_based_filtering(profile_id):
    # Find titles similar to what user enjoyed
    liked_titles = get_liked_titles(profile_id)

    recommendations = []
    for title in liked_titles:
        # Get title features (genre, cast, director, etc.)
        title_features = get_title_features(title)

        # Find similar titles
        similar_titles = find_similar_by_features(title_features)

        for similar_title in similar_titles:
            if not has_watched(profile_id, similar_title):
                similarity_score = calculate_feature_similarity(
                    title_features,
                    get_title_features(similar_title)
                )
                recommendations.append((similar_title, similarity_score))

    return sorted(recommendations, key=lambda x: x[1], reverse=True)
```

**3. Deep Learning Model:**
```python
# Simplified neural network approach
def neural_recommendation(profile_id):
    # Input features
    features = {
        # User features
        'user_embedding': get_user_embedding(profile_id),  # 128-dim vector
        'watch_history': get_recent_watches(profile_id, limit=50),
        'time_of_day': get_current_hour(),
        'day_of_week': get_current_day(),
        'device_type': get_device_type(profile_id),

        # Candidate title features
        'title_embedding': get_title_embeddings(all_titles),  # 128-dim
        'genre_vectors': get_genre_vectors(all_titles),
        'popularity_scores': get_popularity_scores(all_titles)
    }

    # Neural network predicts probability of watching each title
    model = load_model('recommendation_model_v5.h5')
    predictions = model.predict(features)

    # Sort by predicted probability
    ranked_titles = sorted(
        zip(all_titles, predictions),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_titles[:100]
```

### Homepage Personalization

**Dynamic Rows:**
```python
def generate_homepage(profile_id):
    rows = []

    # Row 1: Continue Watching (always first if applicable)
    continue_watching = get_continue_watching(profile_id)
    if continue_watching:
        rows.append({
            'id': 'continue_watching',
            'title': 'Continue Watching',
            'items': continue_watching
        })

    # Row 2: Trending Now (region-specific)
    user_region = get_user_region(profile_id)
    trending = get_trending_in_region(user_region, limit=20)
    rows.append({
        'id': 'trending',
        'title': 'Trending Now',
        'items': trending
    })

    # Row 3-4: Personalized based on viewing history
    recent_watch = get_most_recent_watch(profile_id)
    if recent_watch:
        similar_titles = get_similar_titles(recent_watch, limit=20)
        rows.append({
            'id': f'because_you_watched_{recent_watch.id}',
            'title': f"Because You Watched '{recent_watch.title}'",
            'items': similar_titles
        })

    # Row 5+: Genre-specific rows
    preferred_genres = get_preferred_genres(profile_id)
    for genre in preferred_genres[:3]:
        genre_titles = get_top_titles_by_genre(genre, limit=20)
        rows.append({
            'id': f'genre_{genre}',
            'title': genre.capitalize(),
            'items': genre_titles
        })

    # Row: New Releases
    new_releases = get_new_releases(region=user_region, limit=20)
    rows.append({
        'id': 'new_releases',
        'title': 'New on Netflix',
        'items': new_releases
    })

    # Row: Top 10 in Your Country
    top_10 = get_top_10_in_country(user_region)
    rows.append({
        'id': 'top_10',
        'title': f'Top 10 in {user_region}',
        'items': top_10
    })

    return rows
```

### A/B Testing

**Every recommendation is an experiment:**
```python
def log_recommendation_result(profile_id, title_id, position, clicked):
    # Track if user clicked on recommendation
    event = {
        'profile_id': profile_id,
        'title_id': title_id,
        'row_id': get_row_id(title_id),
        'position': position,  # Position in carousel
        'clicked': clicked,
        'timestamp': now(),
        'experiment_id': get_active_experiment(profile_id)
    }

    kafka.publish('recommendation_events', event)

    # Offline analysis:
    # - Which row types perform best?
    # - Optimal number of rows?
    # - Best carousel ordering?
    # - Effect of artwork on CTR?
```

## 10. Scalability & Performance

### Horizontal Scaling

**Microservices Architecture:**
```
Each service independently scalable:
- API Gateway: 100+ instances
- Play Service: 200+ instances
- Recommendation: 50+ instances (ML heavy)
- Search: 30+ instances

Auto-scaling based on:
- CPU utilization > 70%
- Request latency > 200ms
- Queue depth > 1000
```

**Database Scaling:**
```
DynamoDB:
- On-demand capacity mode
- Auto-scales read/write units
- Global tables for multi-region

Cassandra:
- Ring architecture (100+ nodes)
- Replication factor: 3
- Partition by profile_id for watch history
```

### Caching Strategy

**Multi-Level Cache:**
```
L1: Client-side (app memory)
- Homepage layout: 5 min
- Title metadata: 1 hour

L2: CDN Edge (Open Connect)
- Video segments: Forever (immutable)
- Images/artwork: 24 hours

L3: Application Cache (ElastiCache/Redis)
- User profiles: 10 min
- Catalog metadata: 1 hour
- Recommendation results: 5 min

L4: Database
```

**Cache Warming:**
```python
def warm_cache_on_new_release(title_id):
    # Pre-populate cache before announcing new release

    # 1. Push to all CDN nodes
    for oc_node in open_connect_nodes:
        oc_node.cache(title_id, priority='high')

    # 2. Cache metadata in Redis
    title_metadata = db.get_title(title_id)
    redis.setex(
        f"title:{title_id}",
        3600,
        json.dumps(title_metadata)
    )

    # 3. Pre-generate recommendations
    for genre in title_metadata['genres']:
        similar = get_similar_titles_by_genre(genre, limit=50)
        redis.setex(
            f"similar:{title_id}",
            3600,
            json.dumps(similar)
        )
```

### Performance Optimizations

**1. Lazy Loading:**
```javascript
// Client-side: Load homepage rows progressively
async function loadHomepage() {
  // Load first 2 rows immediately
  const priority_rows = await api.getHomepage({ limit: 2 });
  renderRows(priority_rows);

  // Load remaining rows in background
  const remaining_rows = await api.getHomepage({ offset: 2 });
  renderRows(remaining_rows);
}
```

**2. Image Optimization:**
```
- Multiple sizes: thumbnail (200x300), landscape (400x225), hero (1920x1080)
- WebP format (30% smaller than JPEG)
- Lazy loading: Load images as user scrolls
- Blur placeholder: Show low-res blurred image while loading
```

**3. Predictive Prefetching:**
```python
def prefetch_likely_titles(profile_id):
    # Predict next titles user will click
    recommendations = get_homepage(profile_id)

    # Prefetch top 3 most likely titles
    for title in recommendations[:3]:
        # Prefetch manifest and first segments
        cdn.prefetch(
            f"{title.id}/manifest.mpd",
            f"{title.id}/720p/segment_0.m4s"
        )
```

## 11. Trade-offs

### Pre-encoding All Qualities vs. On-Demand

**Pre-encoding (Netflix approach):**
- ✅ Instant playback
- ✅ Consistent quality
- ❌ High storage costs (6+ versions per title)

**On-demand encoding:**
- ✅ Lower storage
- ✅ Only encode what's requested
- ❌ First-view latency
- ❌ Complex cache management

**Decision:** Pre-encode all (predictable costs, better UX)

### Open Connect vs. Traditional CDN

**Open Connect:**
- ✅ 95%+ cache hit rate
- ✅ Zero transit costs for ISPs
- ✅ Single-hop latency
- ❌ High initial investment (hardware)
- ❌ Complex ISP relationships

**Traditional CDN (CloudFront, Akamai):**
- ✅ Easier setup
- ✅ Pay-as-you-go
- ❌ Higher long-term costs
- ❌ Lower cache hit rates

**Decision:** Open Connect for scale (Netflix traffic = 15% of global internet)

### Real-time vs. Batch Recommendations

**Real-time:**
- ✅ Instant personalization
- ✅ Reflects latest behavior
- ❌ High computational cost
- ❌ Latency impact

**Batch (Netflix approach):**
- ✅ Lower cost (pre-computed)
- ✅ Fast response
- ❌ Stale (updated every few hours)

**Decision:** Hybrid (batch base, real-time adjustments)

## 12. Follow-up Questions

1. **How would you handle a new episode release with 10M concurrent viewers?**
   - Pre-warm all OC caches 1 hour before release
   - Scale Play Service instances 2x
   - Use queue-based throttling for API requests
   - Monitor and auto-scale databases
   - Stagger release by region (rolling midnight release)

2. **How do you ensure video quality on slow connections?**
   - Adaptive bitrate streaming (start low, increase)
   - Preload next segment based on bandwidth
   - Smart quality adjustment (avoid frequent switching)
   - Downloadable content for offline viewing
   - Lower resolution options (144p, 240p)

3. **How would you implement parental controls?**
   - Rating-based filtering (G, PG, PG-13, R)
   - Kids profiles with curated content
   - PIN protection for mature content
   - View history hidden from kids profiles
   - Content locked by rating threshold

4. **How do you handle content licensing expiration?**
   - Automated expiry dates in catalog DB
   - 30-day warning to users (in "My List")
   - Background job: Remove from cache, mark unavailable
   - Licensing team notified for renewal
   - Analytics: Track view impact of expiring content

5. **How would you detect account sharing abuse?**
   - Track concurrent streams per account
   - IP address clustering (multiple distant locations)
   - Device fingerprinting
   - Viewing pattern analysis
   - Limit: Standard plan = 2 concurrent streams
   - Action: Prompt to upgrade or verify device

6. **How do you optimize for low-end devices (old Smart TVs)?**
   - Lightweight client app
   - Lower max quality (720p instead of 4K)
   - Simplified UI (fewer rows, larger thumbnails)
   - Limit concurrent operations
   - Graceful degradation (disable previews)

7. **How would you implement a "Surprise Me" feature (random episode)?**
   - Filter watched episodes
   - Weight by rating, popularity
   - Bias toward recent seasons
   - Exclude first episodes (avoid spoilers)
   - Cache selection for 24 hours (avoid repetition)

8. **How do you measure and improve recommendation quality?**
   - Metrics: Click-through rate (CTR), watch time, completion rate
   - A/B testing: Test new models vs. baseline
   - Offline evaluation: Historical data replay
   - User feedback: Thumbs up/down integration
   - Long-term engagement: Retention rate

9. **How would you handle a CDN outage in a region?**
   - Fallback to origin servers
   - Route traffic to nearest healthy OC node
   - Temporarily serve lower quality (reduce bandwidth)
   - Monitor and alert (PagerDuty)
   - Graceful error messages to users

10. **How do you prevent buffering during playback?**
    - Maintain 30-second buffer ahead of playhead
    - Adaptive bitrate (lower quality if bandwidth drops)
    - Preload multiple segments
    - Monitor network conditions (speed tests)
    - Fallback to lower quality permanently if consistently slow

## Complexity Analysis

- **Time Complexity:**
  - Video streaming: O(1) per segment request
  - Homepage generation: O(k) where k = number of rows
  - Search: O(log n) with indexing
  - Recommendations: O(m × n) where m = candidates, n = features

- **Space Complexity:**
  - Total storage: O(t × q) where t = titles, q = qualities
  - CDN cache: O(popular_titles × qualities)
  - User data: O(u × h) where u = users, h = history size

## References

- [Netflix Tech Blog](https://netflixtechblog.com/)
- [Open Connect Overview](https://openconnect.netflix.com/)
- [Per-Title Encoding](https://netflixtechblog.com/per-title-encode-optimization-7e99442b62a2)
- [Recommendation System](https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429)
- [A/B Testing at Netflix](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)
