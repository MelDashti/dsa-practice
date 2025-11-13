# Design YouTube (Video Streaming Platform)

**Difficulty:** Medium

## 1. Problem Statement

Design a video streaming platform like YouTube that allows users to upload, store, process, and stream videos. The system should support billions of video views per day, provide recommendations, handle various video formats and qualities, enable comments and engagement, and deliver smooth playback experience globally.

**Key Features:**
- Video upload and processing
- Video streaming with adaptive bitrate
- Video recommendations
- User engagement (likes, comments, subscriptions)
- Search functionality
- Live streaming

## 2. Requirements

### Functional Requirements
1. **Video Upload**: Users can upload videos (up to 256 GB, 12 hours)
2. **Video Processing**: Transcode to multiple formats and resolutions
3. **Video Streaming**: Smooth playback with adaptive bitrate
4. **Search**: Search videos by title, description, tags
5. **Recommendations**: Suggest relevant videos
6. **User Engagement**:
   - Like/dislike videos
   - Comment on videos
   - Subscribe to channels
7. **Analytics**: Track views, watch time, engagement
8. **Thumbnail Generation**: Auto-generate and custom thumbnails

### Non-Functional Requirements
1. **Availability**: 99.99% uptime for streaming
2. **Scalability**:
   - 2 billion users
   - 500+ hours of video uploaded per minute
   - 1 billion hours watched per day
3. **Performance**:
   - Video starts playing within 2 seconds
   - No buffering for 95% of plays
   - Search results < 500ms
4. **Latency**:
   - CDN edge delivery < 100ms
   - Live streaming delay < 5 seconds
5. **Storage**: Exabytes of video data
6. **Durability**: 99.999999999% (11 nines)

### Out of Scope
- YouTube Studio (creator dashboard)
- Monetization and ads
- Copyright detection (Content ID)
- Community features (posts, stories)

## 3. Storage Estimation

### Assumptions
- **Total Users**: 2 billion
- **Daily Active Users**: 500 million
- **Videos Uploaded**: 500 hours/minute = 720,000 hours/day
- **Average Video Length**: 10 minutes
- **Average Video Size**: 100 MB (before transcoding)
- **Videos Watched**: 1 billion hours/day
- **Average Watch Session**: 40 minutes

### Calculations

**Daily Video Uploads:**
```
720,000 hours/day × 6 videos/hour (10 min each) = 4.32 million videos/day
```

**Daily Upload Storage (Raw):**
```
4.32M videos × 100 MB = 432,000,000 MB = 432 TB/day
Annual: 432 TB × 365 = 157.7 PB/year
```

**Storage After Transcoding:**
```
Multiple formats: 1080p, 720p, 480p, 360p, 240p, 144p
Multiple codecs: H.264, VP9, AV1
Audio variants: 128kbps, 256kbps

Average multiplier: 5x (accounting for different versions)
432 TB/day × 5 = 2,160 TB/day = 2.16 PB/day
Annual: 2.16 PB × 365 = 788 PB/year
```

**Total Storage (5 years):**
```
788 PB/year × 5 = 3,940 PB ≈ 4 Exabytes (EB)
```

**Daily Video Views:**
```
1 billion hours/day ÷ (10 min/60) = 6 billion video views/day
= 69,444 videos/second average
Peak (5x): 347,220 videos/second
```

**Bandwidth Requirements:**
```
Average bitrate: 2 Mbps (720p)
Concurrent viewers (peak): 50 million
Bandwidth: 50M × 2 Mbps = 100,000,000 Mbps = 100 Tbps
```

**Metadata Storage:**
```
Per video: 10 KB (title, description, tags, statistics)
Total videos (5 years): 4.32M/day × 365 × 5 = 7.88 billion videos
Metadata: 7.88B × 10 KB = 78.8 TB
```

**Database QPS:**
```
Video views: 69,444 views/sec × 5 queries/view = 347,220 QPS
Uploads: 4.32M/day ÷ 86,400 = 50 uploads/sec × 10 queries = 500 QPS
Total: ~350,000 QPS
```

**CDN Egress:**
```
Average: 100 Tbps
Peak: 500 Tbps
Daily: 100 Tbps × 86,400 sec ÷ 8 bits = 1.08 EB/day
Annual: 394 EB/year
```

## 4. High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      Client Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Web Player│  │Mobile App│  │Smart TV  │  │Embed     │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS / HLS / DASH
                           ▼
                  ┌────────────────────┐
                  │   Global CDN       │
                  │ (Distributed PoPs) │
                  └──────────┬─────────┘
                             │
                  ┌──────────┴─────────┐
                  │   Load Balancer    │
                  └──────────┬─────────┘
                             │
        ┌────────────────────┼───────────────────┐
        │                    │                   │
        ▼                    ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   API        │   │   Upload     │   │  Streaming   │
│  Gateway     │   │   Service    │   │   Service    │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                   │
       │                  ▼                   │
       │         ┌──────────────────┐        │
       │         │Video Processing  │        │
       │         │   Pipeline       │        │
       │         │  ┌────────────┐  │        │
       │         │  │Transcoding │  │        │
       │         │  │  Cluster   │  │        │
       │         │  └────────────┘  │        │
       │         └────────┬─────────┘        │
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────────────────────────────────────────┐
│            Application Services                  │
│  ┌─────────┐ ┌─────────────┐ ┌──────────────┐  │
│  │Video    │ │Recommendation│ │  Analytics   │  │
│  │Service  │ │   Service    │ │   Service    │  │
│  └─────────┘ └─────────────┘ └──────────────┘  │
│  ┌─────────┐ ┌─────────────┐ ┌──────────────┐  │
│  │Comment  │ │  Search      │ │  User        │  │
│  │Service  │ │  Service     │ │  Service     │  │
│  └─────────┘ └─────────────┘ └──────────────┘  │
└────────────────┬─────────────────────────────────┘
                 │
    ┌────────────┼─────────────────┐
    │            │                 │
    ▼            ▼                 ▼
┌─────────┐  ┌────────────┐  ┌──────────────┐
│Metadata │  │   Cache    │  │Message Queue │
│   DB    │  │  (Redis/   │  │  (Kafka)     │
│(Spanner)│  │ Memcached) │  └──────────────┘
└─────────┘  └────────────┘
    │
    ▼
┌────────────────────────────────────────────────┐
│          Storage Layer                         │
│  ┌──────────────┐  ┌────────────────────────┐ │
│  │Video Storage │  │  Search Index          │ │
│  │(GCS/S3)      │  │  (Elasticsearch)       │ │
│  │              │  └────────────────────────┘ │
│  │- Original    │  ┌────────────────────────┐ │
│  │- Transcoded  │  │  Data Warehouse        │ │
│  │- Thumbnails  │  │  (BigQuery)            │ │
│  └──────────────┘  └────────────────────────┘ │
└────────────────────────────────────────────────┘
```

### Key Components

1. **Client Applications**: Web, mobile, TV, embedded players
2. **Global CDN**: Edge servers worldwide for low-latency delivery
3. **API Gateway**: Request routing, authentication, rate limiting
4. **Upload Service**: Handle video uploads (chunked, resumable)
5. **Video Processing Pipeline**: Transcoding, thumbnail generation
6. **Streaming Service**: Deliver video segments (HLS/DASH)
7. **Recommendation Service**: ML-based video suggestions
8. **Search Service**: Video discovery via search
9. **Analytics Service**: Track views, watch time, engagement
10. **Metadata DB**: Video metadata, user data, comments
11. **Cache Layer**: Hot data caching
12. **Message Queue**: Async job processing
13. **Video Storage**: Blob storage for all video files
14. **Data Warehouse**: Analytics and reporting

## 5. API Design

### Video Operations

#### Upload Video
```http
POST /api/v1/videos/upload/initialize
Authorization: Bearer {token}

Request:
{
  "title": "How to Design YouTube",
  "description": "System design tutorial",
  "category": "Education",
  "tags": ["system design", "tutorial"],
  "privacy": "public", // public, unlisted, private
  "file_size": 104857600, // 100 MB
  "file_name": "video.mp4"
}

Response (200 OK):
{
  "upload_id": "upload_abc123",
  "video_id": "vid_xyz789",
  "upload_url": "https://upload.youtube.com/upload?id=upload_abc123",
  "chunk_size": 10485760, // 10 MB chunks
  "expires_at": "2025-11-12T11:30:00Z"
}
```

#### Upload Video Chunk
```http
PUT /api/v1/videos/upload/chunk
Authorization: Bearer {token}
Content-Type: application/octet-stream
Content-Range: bytes 0-10485759/104857600

Request Body: Binary chunk data

Response (200 OK):
{
  "upload_id": "upload_abc123",
  "chunk_index": 0,
  "uploaded_bytes": 10485760,
  "total_bytes": 104857600
}
```

#### Finalize Upload
```http
POST /api/v1/videos/upload/finalize
Authorization: Bearer {token}

Request:
{
  "upload_id": "upload_abc123"
}

Response (200 OK):
{
  "video_id": "vid_xyz789",
  "status": "processing",
  "watch_url": "https://youtube.com/watch?v=vid_xyz789",
  "estimated_processing_time": 300 // seconds
}
```

#### Get Video Details
```http
GET /api/v1/videos/{video_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "video_id": "vid_xyz789",
  "title": "How to Design YouTube",
  "description": "System design tutorial",
  "channel": {
    "channel_id": "ch_123",
    "name": "Tech Channel",
    "subscribers": 1000000
  },
  "duration": 600, // seconds
  "views": 15000,
  "likes": 1200,
  "dislikes": 50,
  "upload_date": "2025-11-12T10:00:00Z",
  "status": "ready", // processing, ready, failed
  "thumbnails": {
    "default": "https://i.ytimg.com/vi/vid_xyz789/default.jpg",
    "medium": "https://i.ytimg.com/vi/vid_xyz789/mqdefault.jpg",
    "high": "https://i.ytimg.com/vi/vid_xyz789/hqdefault.jpg"
  },
  "available_qualities": ["1080p", "720p", "480p", "360p", "240p"],
  "category": "Education",
  "tags": ["system design", "tutorial"]
}
```

### Streaming

#### Get Video Manifest (HLS/DASH)
```http
GET /api/v1/videos/{video_id}/stream
Authorization: Bearer {token}

Query Parameters:
- format: hls | dash
- quality: auto | 1080p | 720p | 480p | 360p

Response (200 OK):
Content-Type: application/vnd.apple.mpegurl (HLS)

#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
https://cdn.youtube.com/vi/vid_xyz789/1080p/playlist.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720
https://cdn.youtube.com/vi/vid_xyz789/720p/playlist.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=854x480
https://cdn.youtube.com/vi/vid_xyz789/480p/playlist.m3u8
```

#### Track Video View
```http
POST /api/v1/videos/{video_id}/views
Authorization: Bearer {token}

Request:
{
  "session_id": "session_abc",
  "timestamp": "2025-11-12T10:30:00Z",
  "position": 120, // seconds into video
  "quality": "720p"
}

Response (200 OK):
{
  "tracked": true
}
```

### User Engagement

#### Like Video
```http
POST /api/v1/videos/{video_id}/like
Authorization: Bearer {token}

Response (200 OK):
{
  "video_id": "vid_xyz789",
  "user_action": "liked",
  "total_likes": 1201
}
```

#### Comment on Video
```http
POST /api/v1/videos/{video_id}/comments
Authorization: Bearer {token}

Request:
{
  "text": "Great tutorial!",
  "parent_comment_id": null // null for top-level, ID for reply
}

Response (201 Created):
{
  "comment_id": "comment_abc",
  "text": "Great tutorial!",
  "author": {
    "user_id": "user_456",
    "name": "John Doe"
  },
  "timestamp": "2025-11-12T10:30:00Z",
  "likes": 0,
  "replies_count": 0
}
```

#### Get Comments
```http
GET /api/v1/videos/{video_id}/comments?sort=top&limit=20&page_token=xyz
Authorization: Bearer {token}

Response (200 OK):
{
  "comments": [
    {
      "comment_id": "comment_abc",
      "text": "Great tutorial!",
      "author": {...},
      "timestamp": "2025-11-12T10:30:00Z",
      "likes": 45,
      "replies_count": 3
    }
  ],
  "next_page_token": "abc123"
}
```

### Search & Discovery

#### Search Videos
```http
GET /api/v1/search?q=system+design&sort=relevance&duration=medium&upload_date=week
Authorization: Bearer {token}

Response (200 OK):
{
  "results": [
    {
      "video_id": "vid_xyz789",
      "title": "How to Design YouTube",
      "channel": {...},
      "thumbnail": "https://i.ytimg.com/vi/vid_xyz789/mqdefault.jpg",
      "duration": 600,
      "views": 15000,
      "upload_date": "2025-11-12T10:00:00Z"
    }
  ],
  "total_results": 45000,
  "search_time_ms": 234
}
```

#### Get Recommendations
```http
GET /api/v1/videos/{video_id}/recommendations?limit=10
Authorization: Bearer {token}

Response (200 OK):
{
  "recommendations": [
    {
      "video_id": "vid_abc",
      "title": "System Design Interview Guide",
      "channel": {...},
      "thumbnail": "...",
      "duration": 720,
      "views": 50000
    }
  ]
}
```

### Channel Operations

#### Subscribe to Channel
```http
POST /api/v1/channels/{channel_id}/subscribe
Authorization: Bearer {token}

Response (200 OK):
{
  "channel_id": "ch_123",
  "subscribed": true,
  "subscriber_count": 1000001
}
```

## 6. Storage Strategy

### Video Storage Architecture

**Storage Tiers:**

```
Tier 1: Hot Storage (Recent videos, popular content)
- Storage: SSD-backed, low-latency
- Cost: High
- Usage: Videos uploaded in last 30 days, >1000 views/day
- Location: Multiple regions, CDN origin

Tier 2: Warm Storage (Moderate access)
- Storage: HDD-backed
- Cost: Medium
- Usage: Videos 30-365 days old, 100-1000 views/day

Tier 3: Cold Storage (Archival)
- Storage: Glacier/Coldline
- Cost: Low
- Usage: Videos >1 year old, <100 views/day
- Access: Slower (minutes to retrieve)
```

**File Organization:**
```
gs://youtube-videos/
├── hot/
│   └── {year}/{month}/{day}/
│       └── {video_id}/
│           ├── original.mp4
│           ├── 1080p/
│           │   ├── segment_0.ts
│           │   ├── segment_1.ts
│           │   └── playlist.m3u8
│           ├── 720p/
│           ├── 480p/
│           └── thumbnails/
│               ├── default.jpg
│               ├── frame_1.jpg
│               └── frame_2.jpg
├── warm/
│   └── {year}/{month}/...
└── cold/
    └── {year}/...
```

### Metadata Database Schema

**Google Spanner / Vitess (Sharded MySQL)**

```sql
-- Videos table
CREATE TABLE videos (
    video_id VARCHAR(36) PRIMARY KEY,
    channel_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration INT NOT NULL, -- seconds
    status ENUM('processing', 'ready', 'failed', 'deleted') DEFAULT 'processing',
    privacy ENUM('public', 'unlisted', 'private') DEFAULT 'public',
    upload_date TIMESTAMP NOT NULL,
    original_file_name VARCHAR(500),
    original_file_size BIGINT,
    storage_tier ENUM('hot', 'warm', 'cold') DEFAULT 'hot',
    storage_path VARCHAR(1000),

    -- Statistics (cached, updated periodically)
    view_count BIGINT DEFAULT 0,
    like_count INT DEFAULT 0,
    dislike_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,

    -- Metadata
    category VARCHAR(50),
    language VARCHAR(10),
    tags JSON, -- Array of tags
    thumbnail_url VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_channel (channel_id, upload_date DESC),
    INDEX idx_status (status),
    INDEX idx_upload_date (upload_date DESC),
    FULLTEXT idx_title_desc (title, description)
);

-- Video formats/qualities available
CREATE TABLE video_formats (
    video_id VARCHAR(36) NOT NULL,
    quality VARCHAR(20) NOT NULL, -- 1080p, 720p, etc.
    codec VARCHAR(20) NOT NULL, -- h264, vp9, av1
    bitrate INT NOT NULL, -- kbps
    file_size BIGINT NOT NULL,
    storage_path VARCHAR(1000) NOT NULL,
    manifest_url VARCHAR(1000),
    ready BOOL DEFAULT FALSE,

    PRIMARY KEY (video_id, quality, codec),
    FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE,
    INDEX idx_video_ready (video_id, ready)
);

-- Channels table
CREATE TABLE channels (
    channel_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    subscriber_count BIGINT DEFAULT 0,
    total_views BIGINT DEFAULT 0,
    video_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    avatar_url VARCHAR(500),
    banner_url VARCHAR(500),

    INDEX idx_user (user_id),
    INDEX idx_subscriber_count (subscriber_count DESC)
);

-- Subscriptions
CREATE TABLE subscriptions (
    subscription_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    channel_id VARCHAR(36) NOT NULL,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notifications_enabled BOOL DEFAULT TRUE,

    UNIQUE KEY uk_user_channel (user_id, channel_id),
    INDEX idx_user (user_id, subscribed_at DESC),
    INDEX idx_channel (channel_id)
);

-- Video views (write-heavy, consider Cassandra)
CREATE TABLE video_views (
    view_id VARCHAR(36) PRIMARY KEY,
    video_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36), -- NULL for anonymous
    session_id VARCHAR(36) NOT NULL,
    watched_seconds INT NOT NULL,
    quality VARCHAR(20),
    device_type VARCHAR(50),
    ip_address VARCHAR(45),
    timestamp TIMESTAMP NOT NULL,

    INDEX idx_video_time (video_id, timestamp DESC),
    INDEX idx_user_time (user_id, timestamp DESC)
);

-- Likes/Dislikes
CREATE TABLE video_reactions (
    user_id VARCHAR(36) NOT NULL,
    video_id VARCHAR(36) NOT NULL,
    reaction ENUM('like', 'dislike') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, video_id),
    INDEX idx_video (video_id, reaction)
);

-- Comments
CREATE TABLE comments (
    comment_id VARCHAR(36) PRIMARY KEY,
    video_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    parent_comment_id VARCHAR(36), -- NULL for top-level
    text TEXT NOT NULL,
    like_count INT DEFAULT 0,
    reply_count INT DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOL DEFAULT FALSE,

    INDEX idx_video_time (video_id, deleted, timestamp DESC),
    INDEX idx_parent (parent_comment_id, timestamp DESC),
    INDEX idx_user (user_id, timestamp DESC)
);

-- Watch history
CREATE TABLE watch_history (
    history_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    video_id VARCHAR(36) NOT NULL,
    watched_at TIMESTAMP NOT NULL,
    watch_duration INT NOT NULL, -- seconds watched
    completed BOOL DEFAULT FALSE,

    INDEX idx_user_time (user_id, watched_at DESC),
    INDEX idx_video (video_id)
);
```

## 7. Video Processing Pipeline

### Transcoding Workflow

```
1. Video Upload Complete
    ↓
2. Publish to Kafka: "video_uploaded" event
    ↓
3. Transcoding Worker picks up job
    ↓
4. Download original video from storage
    ↓
5. Parallel Transcoding:
    ├─→ 1080p H.264 (5000 kbps)
    ├─→ 720p H.264 (2800 kbps)
    ├─→ 480p H.264 (1400 kbps)
    ├─→ 360p H.264 (800 kbps)
    ├─→ 240p H.264 (400 kbps)
    ├─→ 144p H.264 (200 kbps)
    ├─→ Audio-only (128 kbps AAC)
    └─→ VP9 variants (parallel)
    ↓
6. Generate HLS/DASH segments
    ├─→ Split into 2-10 second chunks
    └─→ Create manifest files (playlist.m3u8)
    ↓
7. Upload transcoded files to storage
    ↓
8. Generate thumbnails:
    ├─→ Extract frames at 10%, 30%, 50%, 70%, 90%
    ├─→ Resize: default (120x90), medium (320x180), high (480x360)
    └─→ Upload to storage
    ↓
9. Update database: status = 'ready'
    ↓
10. Publish to Kafka: "video_ready" event
    ↓
11. Index video in Elasticsearch
    ↓
12. Send notification to creator
```

### Transcoding Infrastructure

**Distributed Transcoding Cluster:**

```python
class TranscodingWorker:
    def __init__(self):
        self.kafka_consumer = KafkaConsumer('video_uploaded')
        self.s3_client = S3Client()

    def process_video(self, video_id):
        # 1. Download original
        original_path = self.s3_client.download(
            f"{video_id}/original.mp4"
        )

        # 2. Get video metadata
        metadata = get_video_metadata(original_path)
        duration = metadata['duration']

        # 3. Parallel transcoding
        transcode_jobs = [
            {'quality': '1080p', 'bitrate': '5000k', 'codec': 'h264'},
            {'quality': '720p', 'bitrate': '2800k', 'codec': 'h264'},
            {'quality': '480p', 'bitrate': '1400k', 'codec': 'h264'},
            {'quality': '360p', 'bitrate': '800k', 'codec': 'h264'},
        ]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for job in transcode_jobs:
                future = executor.submit(
                    self.transcode_video,
                    original_path,
                    job['quality'],
                    job['bitrate'],
                    job['codec']
                )
                futures.append(future)

            # Wait for all transcoding jobs
            for future in futures:
                result = future.result()
                self.upload_transcoded(video_id, result)

        # 4. Generate HLS segments
        self.generate_hls_segments(video_id)

        # 5. Generate thumbnails
        self.generate_thumbnails(video_id, original_path)

        # 6. Update database
        db.update_video(video_id, status='ready')

        # 7. Cleanup
        os.remove(original_path)

    def transcode_video(self, input_path, quality, bitrate, codec):
        output_path = f"/tmp/{quality}_{codec}.mp4"

        # Use FFmpeg for transcoding
        command = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264' if codec == 'h264' else 'libvpx-vp9',
            '-b:v', bitrate,
            '-c:a', 'aac',
            '-b:a', '128k',
            '-vf', f'scale=-2:{quality[:-1]}',  # e.g., scale to 720p
            '-preset', 'medium',
            '-movflags', '+faststart',
            output_path
        ]

        subprocess.run(command, check=True)
        return {'quality': quality, 'path': output_path}

    def generate_hls_segments(self, video_id):
        # Generate HLS playlist and segments
        for quality in ['1080p', '720p', '480p', '360p']:
            input_path = f"/tmp/{quality}_h264.mp4"
            output_dir = f"/tmp/{video_id}/{quality}/"
            os.makedirs(output_dir, exist_ok=True)

            command = [
                'ffmpeg',
                '-i', input_path,
                '-codec', 'copy',
                '-start_number', '0',
                '-hls_time', '10',  # 10-second segments
                '-hls_list_size', '0',
                '-f', 'hls',
                f'{output_dir}/playlist.m3u8'
            ]

            subprocess.run(command, check=True)

            # Upload segments to S3
            self.s3_client.upload_directory(
                output_dir,
                f"{video_id}/{quality}/"
            )

    def generate_thumbnails(self, video_id, video_path):
        thumbnails = []
        positions = [0.1, 0.3, 0.5, 0.7, 0.9]  # Extract at these points

        for i, pos in enumerate(positions):
            output_path = f"/tmp/{video_id}_thumb_{i}.jpg"

            command = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'select=eq(n\\,{int(pos*100)})',
                '-vframes', '1',
                '-q:v', '2',  # Quality
                output_path
            ]

            subprocess.run(command, check=True)

            # Upload thumbnail
            self.s3_client.upload(
                output_path,
                f"{video_id}/thumbnails/frame_{i}.jpg"
            )
            thumbnails.append(f"https://cdn.youtube.com/vi/{video_id}/frame_{i}.jpg")

        return thumbnails
```

**Optimization Strategies:**

1. **Adaptive Transcoding:**
   - Analyze source video quality
   - Skip transcoding to higher quality than source
   - Example: 720p source → don't generate 1080p

2. **Priority Queue:**
   - High priority: Videos from popular channels
   - Low priority: Unlisted/private videos
   - Use separate Kafka topics/partitions

3. **Spot Instances:**
   - Use AWS Spot / GCP Preemptible VMs
   - 70-90% cost savings
   - Implement checkpointing for resumable jobs

4. **GPU Acceleration:**
   - Use NVIDIA GPUs for faster encoding
   - H.264: 5-10x faster with GPU
   - Cost vs. speed trade-off

## 8. Streaming Protocols

### HLS (HTTP Live Streaming)

**Why HLS?**
- Widely supported (all browsers, iOS, Android)
- Adaptive bitrate streaming
- Uses standard HTTP (CDN-friendly)
- Fallback mechanism built-in

**HLS Master Playlist:**
```m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
https://cdn.youtube.com/vi/xyz789/1080p/playlist.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
https://cdn.youtube.com/vi/xyz789/720p/playlist.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=854x480,CODECS="avc1.64001e,mp4a.40.2"
https://cdn.youtube.com/vi/xyz789/480p/playlist.m3u8
```

**Quality-Specific Playlist (720p):**
```m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.0,
segment_0.ts
#EXTINF:10.0,
segment_1.ts
#EXTINF:10.0,
segment_2.ts
#EXT-X-ENDLIST
```

### DASH (Dynamic Adaptive Streaming over HTTP)

**Alternative to HLS:**
- Industry standard (ISO/IEC 23009-1)
- Better compression with modern codecs
- Used by YouTube for some clients

**MPD (Media Presentation Description):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011">
  <Period>
    <AdaptationSet mimeType="video/mp4" codecs="avc1.64001f">
      <Representation id="720p" bandwidth="2800000" width="1280" height="720">
        <BaseURL>https://cdn.youtube.com/vi/xyz789/720p/</BaseURL>
        <SegmentList>
          <Initialization sourceURL="init.mp4"/>
          <SegmentURL media="segment_0.m4s"/>
          <SegmentURL media="segment_1.m4s"/>
        </SegmentList>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
```

### Adaptive Bitrate Streaming (ABR)

**Client-Side Logic:**
```javascript
class AdaptiveBitratePlayer {
  constructor(videoElement, manifestUrl) {
    this.video = videoElement;
    this.manifestUrl = manifestUrl;
    this.qualities = [];
    this.currentQuality = null;
    this.buffer = [];
    this.bufferTarget = 30; // seconds
  }

  async initialize() {
    // 1. Fetch master playlist
    const manifest = await fetch(this.manifestUrl);
    this.qualities = this.parseManifest(manifest);

    // 2. Select initial quality based on bandwidth estimate
    const estimatedBandwidth = await this.estimateBandwidth();
    this.currentQuality = this.selectQuality(estimatedBandwidth);

    // 3. Start playback
    this.startBuffering();
  }

  async estimateBandwidth() {
    // Download small segment and measure speed
    const start = Date.now();
    const response = await fetch(this.qualities[0].testSegment);
    const data = await response.arrayBuffer();
    const duration = (Date.now() - start) / 1000;

    const bandwidth = (data.byteLength * 8) / duration; // bits per second
    return bandwidth;
  }

  selectQuality(bandwidth) {
    // Select highest quality that bandwidth can support
    // with 80% safety margin
    const safeBandwidth = bandwidth * 0.8;

    for (let i = this.qualities.length - 1; i >= 0; i--) {
      if (this.qualities[i].bitrate <= safeBandwidth) {
        return this.qualities[i];
      }
    }

    // Fallback to lowest quality
    return this.qualities[0];
  }

  async startBuffering() {
    while (this.buffer.length < this.bufferTarget) {
      // 1. Fetch next segment
      const segment = await this.fetchSegment(this.currentQuality);

      // 2. Add to buffer
      this.buffer.push(segment);

      // 3. Monitor playback and adjust quality
      if (this.shouldSwitchQuality()) {
        const newBandwidth = this.getCurrentBandwidth();
        this.currentQuality = this.selectQuality(newBandwidth);
      }
    }
  }

  shouldSwitchQuality() {
    // Switch if:
    // - Buffer is running low (buffering)
    // - Bandwidth significantly improved
    // - Too many dropped frames

    const bufferHealth = this.buffer.length;
    const droppedFrames = this.video.getVideoPlaybackQuality().droppedVideoFrames;

    return bufferHealth < 10 || droppedFrames > 100;
  }
}
```

## 9. Content Recommendation System

### Recommendation Pipeline

```
User Context
├─→ Watch history
├─→ Search history
├─→ Liked videos
├─→ Subscribed channels
└─→ Demographics

    ↓

Feature Engineering
├─→ User features: age, location, watch patterns
├─→ Video features: category, tags, engagement rate
├─→ Context features: time of day, device

    ↓

ML Models (Ensemble)
├─→ Collaborative Filtering (similar users)
├─→ Content-Based (similar videos)
├─→ Deep Neural Network (complex patterns)
└─→ Ranking Model (final ordering)

    ↓

Candidate Generation (1000s of videos)
    ↓
Ranking & Filtering
    ↓
Top N Recommendations (10-50)
```

### Two-Stage Recommendation

**Stage 1: Candidate Generation**
```python
def generate_candidates(user_id):
    candidates = []

    # 1. Collaborative filtering: Users who liked similar videos
    similar_users = get_similar_users(user_id, limit=1000)
    for user in similar_users:
        user_videos = get_user_liked_videos(user.id, limit=10)
        candidates.extend(user_videos)

    # 2. Content-based: Videos similar to user's history
    user_history = get_watch_history(user_id, limit=50)
    for video in user_history:
        similar_videos = get_similar_videos(video.id, limit=20)
        candidates.extend(similar_videos)

    # 3. Trending in user's categories
    user_categories = get_user_preferred_categories(user_id)
    for category in user_categories:
        trending = get_trending_videos(category, limit=100)
        candidates.extend(trending)

    # 4. Subscribed channels' new uploads
    subscriptions = get_user_subscriptions(user_id)
    for channel in subscriptions:
        recent_videos = get_channel_videos(channel.id, limit=5)
        candidates.extend(recent_videos)

    # Deduplicate and filter
    candidates = deduplicate(candidates)
    candidates = filter_already_watched(user_id, candidates)

    return candidates  # ~1000-5000 candidates
```

**Stage 2: Ranking**
```python
def rank_candidates(user_id, candidates):
    # Feature extraction
    features = []
    for video in candidates:
        feature_vector = {
            # Video features
            'video_age_days': (now() - video.upload_date).days,
            'view_count': video.view_count,
            'like_rate': video.like_count / max(video.view_count, 1),
            'comment_rate': video.comment_count / max(video.view_count, 1),
            'watch_time_avg': video.avg_watch_duration / video.duration,

            # User-video affinity
            'category_match': user_prefers_category(user_id, video.category),
            'channel_subscribed': is_subscribed(user_id, video.channel_id),
            'language_match': video.language == user.preferred_language,

            # Context features
            'time_of_day': get_hour(),
            'day_of_week': get_weekday(),
            'device_type': get_user_device(user_id),

            # Historical features
            'user_previous_engagement': get_user_engagement_with_similar(user_id, video),
        }
        features.append(feature_vector)

    # Run ML model (e.g., Gradient Boosted Trees, Neural Network)
    scores = recommendation_model.predict(features)

    # Sort by score
    ranked_videos = sort_by_score(candidates, scores)

    # Diversity injection: Don't show too many videos from same channel
    final_list = apply_diversity_rules(ranked_videos)

    return final_list[:50]  # Top 50 recommendations
```

### Offline Training

```python
# Daily batch job
def train_recommendation_model():
    # 1. Extract training data from data warehouse
    training_data = bigquery.query("""
        SELECT
            user_id,
            video_id,
            watch_duration / video.duration AS completion_rate,
            liked,
            commented,
            shared,
            video.* ,
            user.*
        FROM video_views
        JOIN videos ON video_views.video_id = videos.video_id
        JOIN users ON video_views.user_id = users.user_id
        WHERE timestamp >= CURRENT_DATE() - INTERVAL 30 DAY
    """)

    # 2. Feature engineering
    X = extract_features(training_data)
    y = training_data['completion_rate']  # Predict watch completion

    # 3. Train model
    model = xgboost.XGBRegressor()
    model.fit(X, y)

    # 4. Evaluate
    test_score = model.score(X_test, y_test)
    print(f"Model R²: {test_score}")

    # 5. Deploy new model
    upload_model_to_production(model)
```

## 10. Scalability & CDN

### Global CDN Architecture

**Multi-Tier CDN:**

```
User Request
    ↓
Tier 1: Edge PoP (200+ locations worldwide)
    ├─→ Cache Hit (90-95%) → Serve from edge
    └─→ Cache Miss
        ↓
Tier 2: Regional Cache (20-30 locations)
    ├─→ Cache Hit → Serve from regional
    └─→ Cache Miss
        ↓
Origin: Video Storage (GCS/S3)
    └─→ Fetch and cache at all tiers
```

**CDN Configuration:**

```nginx
# CDN edge server config
location /vi/ {
    # Video segments
    proxy_cache video_cache;
    proxy_cache_valid 200 365d;  # Cache for 1 year
    proxy_cache_key $scheme$host$uri;
    proxy_cache_lock on;

    # Origin
    proxy_pass https://origin-storage.youtube.com;

    # Headers
    add_header X-Cache-Status $upstream_cache_status;
    add_header Cache-Control "public, max-age=31536000, immutable";

    # Range requests support (seeking)
    proxy_cache_revalidate on;
    proxy_http_version 1.1;
    proxy_set_header Range $http_range;
}
```

**Cache Strategy:**

```
Hot Videos (>1M views/day):
- Pre-populate to all edge locations
- Cache forever (immutable content)

Warm Videos (10K-1M views/day):
- Cache at regional level
- Promote to edge on demand

Cold Videos (<10K views/day):
- Origin fetch on demand
- Cache at regional only
```

### Database Scaling

**Sharding Strategy:**

```
Shard by video_id hash:
- Shard 0: video_id % 100 == 0-9
- Shard 1: video_id % 100 == 10-19
- ...
- Shard 9: video_id % 100 == 90-99

Each shard:
- Master (writes)
- 2-3 Read Replicas (reads)
```

**Caching Layer:**

```python
# Redis cache for hot data
def get_video_details(video_id):
    # Check cache first
    cache_key = f"video:{video_id}"
    cached = redis.get(cache_key)

    if cached:
        return json.loads(cached)

    # Cache miss: fetch from database
    video = db.query(f"SELECT * FROM videos WHERE video_id = '{video_id}'")

    # Store in cache (5 minute TTL)
    redis.setex(cache_key, 300, json.dumps(video))

    return video
```

**Write Optimization:**

```python
# Video views: High write volume
# Use Cassandra for time-series data

def record_view(video_id, user_id, watch_duration):
    # Write to Cassandra (fast writes)
    cassandra.execute("""
        INSERT INTO video_views (video_id, timestamp, user_id, watch_duration)
        VALUES (?, ?, ?, ?)
    """, (video_id, now(), user_id, watch_duration))

    # Async: Update aggregated statistics
    kafka.publish('view_recorded', {
        'video_id': video_id,
        'timestamp': now()
    })

# Separate consumer updates view_count
def update_view_count_consumer():
    # Batch updates every 10 seconds
    view_counts = defaultdict(int)

    while True:
        messages = kafka.poll(timeout=10)
        for msg in messages:
            view_counts[msg['video_id']] += 1

        # Batch update database
        for video_id, count in view_counts.items():
            db.execute("""
                UPDATE videos
                SET view_count = view_count + ?
                WHERE video_id = ?
            """, (count, video_id))

        view_counts.clear()
```

## 11. Trade-offs

### Storage: Full Qualities vs. Adaptive Encoding

**Full Qualities (YouTube approach):**
- ✅ Predictable storage costs
- ✅ Simpler implementation
- ❌ Higher total storage (6+ versions per video)
- ❌ Overkill for unpopular videos

**Adaptive Encoding:**
- ✅ Lower storage for unpopular videos
- ✅ Encode on-demand
- ❌ Complex cache management
- ❌ First-view latency

**Decision:** Pre-encode popular qualities (720p, 480p, 360p), encode 1080p/4K on-demand

### Recommendation: Accuracy vs. Latency

**Complex ML Model:**
- ✅ Better recommendations (higher CTR)
- ❌ Slower inference (100-500ms)
- ❌ Expensive GPU infrastructure

**Simple Model:**
- ✅ Fast (10-50ms)
- ✅ Lower cost
- ❌ Lower accuracy

**Decision:** Two-stage hybrid (fast candidate generation + complex ranking)

### Comments: SQL vs. NoSQL

**MySQL:**
- ✅ Transactions, consistency
- ✅ Complex queries (nested comments)
- ❌ Write scaling limitations

**Cassandra:**
- ✅ High write throughput
- ✅ Horizontal scalability
- ❌ Limited query flexibility
- ❌ Eventual consistency

**Decision:** MySQL for comments (moderate scale), shard by video_id

## 12. Follow-up Questions

1. **How would you handle a viral video with 10M concurrent viewers?**
   - Pre-warm CDN edge caches globally
   - Provision extra origin bandwidth
   - Rate-limit API requests (view count updates)
   - Use approximate counters (eventual consistency OK)
   - Auto-scale streaming infrastructure

2. **How do you detect and remove copyrighted content?**
   - Content ID system: Fingerprint audio/video
   - Compare uploaded videos against fingerprint database
   - Automatic takedown if match found
   - Manual review for disputes

3. **How would you implement live streaming?**
   - Use RTMP for ingestion (OBS → YouTube)
   - Transcode and package into HLS/DASH in real-time
   - Lower latency protocols: WebRTC, Low-Latency HLS
   - Buffering: 2-10 second delay acceptable
   - Scalable edge servers for distribution

4. **How do you prevent bot views from inflating view counts?**
   - Track IP addresses, user agents
   - Require minimum watch duration (e.g., 30 seconds)
   - Machine learning: Detect bot patterns
   - Rate limiting per IP
   - CAPTCHA for suspicious activity

5. **How would you optimize video upload for slow connections?**
   - Resumable uploads (track uploaded chunks)
   - Adaptive chunk size based on bandwidth
   - Client-side compression before upload
   - Background uploads (allow user to navigate away)
   - Upload during off-peak hours (schedule)

6. **How do you handle video takedown requests (DMCA)?**
   - API endpoint for takedown requests
   - Store in moderation queue
   - Immediate soft-delete (hide video)
   - Manual review by team
   - Notify uploader, allow counter-notification
   - Permanent deletion if confirmed

7. **How would you implement subtitles/closed captions?**
   - Store as separate WebVTT/SRT files
   - Auto-generate using speech-to-text (Google Cloud Speech API)
   - Allow user-submitted corrections
   - Serve from CDN alongside video
   - Multiple languages support

8. **How do you optimize for mobile devices?**
   - Lower default quality (360p/480p)
   - Smaller video player size
   - Prefetch only next 2-3 segments
   - Optimize thumbnails (smaller size)
   - Lazy load comments/recommendations

9. **How would you handle a database outage?**
   - Serve video content from CDN (cached)
   - Graceful degradation: Read-only mode
   - Failover to read replicas
   - Queue writes to Kafka (replay after recovery)
   - Show cached metadata (may be slightly stale)

10. **How do you implement video analytics dashboard for creators?**
    - Data warehouse (BigQuery) for analytics queries
    - Batch ETL jobs: Aggregate view data
    - Real-time pipeline: Kafka → Spark → Dashboard
    - Metrics: Views, watch time, demographics, traffic sources
    - Cache aggregated data (15-minute intervals)

## Complexity Analysis

- **Time Complexity:**
  - Video upload: O(n) where n = video size
  - Streaming: O(1) per segment request
  - Search: O(log n) with indexing
  - Recommendations: O(k) where k = candidate size

- **Space Complexity:**
  - Total storage: O(v × d × q) where v = videos, d = duration, q = qualities
  - With deduplication: ~0.9 × original (10% savings)
  - CDN cache: O(popular_videos × qualities)

## References

- [YouTube Architecture (High Scalability)](http://highscalability.com/youtube-architecture)
- [HLS Specification (Apple)](https://developer.apple.com/streaming/)
- [DASH Specification (ISO)](https://www.iso.org/standard/79329.html)
- [Recommendation Systems (Google Research)](https://research.google/pubs/pub45530/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
