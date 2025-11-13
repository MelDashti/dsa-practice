# Design Spotify (Music Streaming with Personalized Playlists)

**Difficulty:** Medium

## 1. Problem Statement

Design a music streaming service like Spotify that allows users to stream millions of songs, create and share playlists, discover new music through personalized recommendations, follow artists, and enjoy both free (ad-supported) and premium (ad-free) tiers. The system should provide low-latency audio streaming globally and generate highly personalized content.

**Key Features:**
- On-demand music streaming
- Personalized playlists (Discover Weekly, Daily Mix)
- Social features (follow friends, share playlists)
- Offline downloads (premium)
- Podcast support
- Artist pages and albums

## 2. Requirements

### Functional Requirements
1. **Music Streaming**: Play any song from 100M+ track catalog
2. **Playlists**: Create, edit, share playlists
3. **Search**: Find songs, artists, albums, playlists
4. **Personalized Recommendations**:
   - Discover Weekly (new songs each Monday)
   - Daily Mix (multiple genre-based playlists)
   - Release Radar (new releases from followed artists)
5. **Social Features**: Follow users/artists, collaborative playlists
6. **Offline Mode**: Download songs for offline listening (premium)
7. **Queue Management**: Add songs to play queue, shuffle, repeat
8. **Lyrics**: Display synchronized lyrics
9. **Podcast Support**: Stream podcast episodes

### Non-Functional Requirements
1. **Availability**: 99.9% uptime
2. **Scalability**:
   - 500+ million users
   - 100+ million active users daily
   - 5+ million concurrent streams (peak)
3. **Performance**:
   - Song starts playing within 1 second
   - Zero buffering during playback
   - Search results < 300ms
4. **Audio Quality**:
   - Free: 160 kbps (Ogg Vorbis)
   - Premium: 320 kbps
   - High-quality streaming: AAC, FLAC support
5. **Global Coverage**: Low latency worldwide (CDN)
6. **Cost Efficiency**: Optimize bandwidth and storage

### Out of Scope
- Music upload by users
- Royalty payment processing
- Artist analytics dashboard
- Video content (Spotify Video)

## 3. Storage Estimation

### Assumptions
- **Total Users**: 500 million
- **Active Users**: 100 million daily
- **Track Catalog**: 100 million songs
- **Average Song Length**: 3.5 minutes (210 seconds)
- **Peak Concurrent Streams**: 5 million
- **Average Daily Listening**: 2 hours per active user
- **Premium Users**: 40% (160M of 400M subscribers)
- **Downloads**: 20 songs average per premium user

### Calculations

**Music Storage:**
```
Per song:
- Original master: ~50 MB (FLAC/WAV)
- 320 kbps: 210 sec × 320 kbps / 8 = 8.4 MB
- 160 kbps: 210 sec × 160 kbps / 8 = 4.2 MB
- 96 kbps: 210 sec × 96 kbps / 8 = 2.52 MB
Total per song: ~15 MB (all qualities)

Total Library: 100M songs × 15 MB = 1.5 Petabytes (PB)
With replication (3x): 4.5 PB
```

**Metadata Storage:**
```
Per song: 10 KB (title, artist, album, duration, genre, etc.)
100M songs × 10 KB = 1 TB

User data: 5 KB per user
500M users × 5 KB = 2.5 TB

Playlists: Avg 50 playlists × 100M users = 5B playlists
5B × 2 KB = 10 TB

Total Metadata: ~14 TB
```

**Daily Streaming Volume:**
```
100M daily active users × 2 hours × 160 kbps avg
= 200M hours × 160 kbps
= 32,000,000,000 Mbps-hours
= 32B × 3600 sec × 160 kbps / 8 bits
= 2.304 PB/day
```

**Peak Bandwidth:**
```
5M concurrent streams × 320 kbps max = 1,600,000 Mbps = 1.6 Tbps
```

**Offline Downloads (Premium):**
```
160M premium users × 20 songs × 8.4 MB = 26.88 PB
(Distributed across user devices, not Spotify storage)
```

**Listening History:**
```
Per play: 100 bytes (user_id, track_id, timestamp, duration)
100M DAU × 30 plays/day = 3B plays/day
3B × 100 bytes = 300 GB/day
Annual: 300 GB × 365 = 109.5 TB/year
```

**Database QPS:**
```
Reads:
- Play requests: 5M concurrent / 210 sec avg = ~23,800 starts/sec
- Each start: 5 queries (track info, user state, queue, recommendations)
- Read QPS: 23,800 × 5 = 119,000 QPS

Writes:
- Play tracking: 23,800/sec
- User interactions (like, skip): 23,800 × 0.3 = 7,140/sec
- Write QPS: ~31,000 QPS

Total: ~150,000 QPS
```

## 4. High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   Client Layer                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Desktop   │ │Mobile App│ │Web Player│ │Car/IoT   │  │
│  │Client    │ │(iOS/And.)│ │          │ │Devices   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└──────────────────────────────────────────────────────────┘
                        │
                        │ HTTPS / Protocol Buffers
                        ▼
            ┌──────────────────────┐
            │   Global CDN         │
            │ (Fastly/CloudFlare)  │
            └──────────┬───────────┘
                       │
            ┌──────────┴───────────┐
            │   API Gateway        │
            │  (Kong/Ambassador)   │
            └──────────┬───────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
┌─────────┐   ┌──────────────┐   ┌──────────────┐
│Streaming│   │   Backend    │   │  Real-time   │
│Service  │   │   Services   │   │   Services   │
└────┬────┘   └──────┬───────┘   └──────┬───────┘
     │               │                   │
     │        ┌──────┴──────┬────────┐  │
     │        │             │        │  │
     │        ▼             ▼        ▼  ▼
     │  ┌─────────┐  ┌──────────┐ ┌──────────┐
     │  │ User    │  │ Playlist │ │ Social   │
     │  │ Service │  │ Service  │ │ Service  │
     │  └─────────┘  └──────────┘ └──────────┘
     │  ┌─────────┐  ┌──────────┐ ┌──────────┐
     │  │ Search  │  │Recommend │ │ Analytics│
     │  │ Service │  │ Service  │ │ Service  │
     │  └─────────┘  └──────────┘ └──────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│            Data Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │PostgreSQL│  │ Cassandra│  │  Redis   │     │
│  │(Metadata)│  │ (History)│  │ (Cache)  │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Elasticsearch│ │  Kafka   │  │Bigtable  │     │
│  │ (Search) │  │ (Stream) │  │(Analytics)│     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│          Storage Layer                          │
│  ┌──────────────┐  ┌──────────────────────┐    │
│  │Audio Storage │  │  ML Models Storage   │    │
│  │(GCS/S3)      │  │  (Recommendation)    │    │
│  └──────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Key Components

1. **Client Applications**: Desktop, mobile, web, embedded devices
2. **Global CDN**: Audio delivery, edge caching
3. **API Gateway**: Authentication, rate limiting, routing
4. **Streaming Service**: Audio streaming, DRM, quality selection
5. **User Service**: Authentication, profiles, subscriptions
6. **Playlist Service**: Playlist CRUD, collaborative playlists
7. **Search Service**: Full-text search (Elasticsearch)
8. **Recommendation Service**: ML-based personalization
9. **Social Service**: Following, activity feeds, sharing
10. **Analytics Service**: Play tracking, metrics
11. **PostgreSQL**: User accounts, catalog metadata
12. **Cassandra**: Time-series data (play history)
13. **Redis**: Caching, session management
14. **Kafka**: Event streaming, data pipeline
15. **Bigtable**: User activity analytics
16. **Audio Storage**: GCS/S3 for audio files

## 5. API Design

### Playback

#### Start Playing Track
```http
POST /api/v1/player/play
Authorization: Bearer {token}

Request:
{
  "track_id": "track_abc123",
  "context": {
    "uri": "spotify:playlist:xyz789", // Playing from playlist
    "position": 5 // Track position in context
  },
  "quality": "high", // low (96kbps), normal (160kbps), high (320kbps)
  "device_id": "device_123"
}

Response (200 OK):
{
  "playback_session_id": "session_abc",
  "track": {
    "track_id": "track_abc123",
    "title": "Song Title",
    "artists": [
      {"artist_id": "artist_456", "name": "Artist Name"}
    ],
    "album": {
      "album_id": "album_789",
      "title": "Album Title",
      "artwork_url": "https://i.scdn.co/image/abc123"
    },
    "duration_ms": 210000,
    "preview_url": "https://p.scdn.co/mp3-preview/abc123"
  },
  "streaming_urls": {
    "320kbps": "https://audio-ak-spotify-com.akamaized.net/...",
    "160kbps": "https://audio-ak-spotify-com.akamaized.net/...",
    "96kbps": "https://audio-ak-spotify-com.akamaized.net/..."
  },
  "encryption_key": "encrypted_key_for_drm",
  "next_tracks": [ /* queue */ ],
  "timestamp": "2025-11-12T12:00:00Z"
}
```

#### Update Playback State
```http
PUT /api/v1/player/state
Authorization: Bearer {token}

Request:
{
  "session_id": "session_abc",
  "position_ms": 45000,
  "is_playing": true,
  "volume": 80,
  "timestamp": "2025-11-12T12:00:45Z"
}

Response (200 OK):
{
  "updated": true
}
```

#### Report Playback Event
```http
POST /api/v1/player/events
Authorization: Bearer {token}

Request:
{
  "session_id": "session_abc",
  "track_id": "track_abc123",
  "event_type": "track_played", // track_played, track_skipped, track_completed
  "position_ms": 210000,
  "duration_played_ms": 210000,
  "quality": "high",
  "timestamp": "2025-11-12T12:03:30Z"
}

Response (202 Accepted):
{
  "tracked": true
}
```

### Playlist Management

#### Create Playlist
```http
POST /api/v1/playlists
Authorization: Bearer {token}

Request:
{
  "name": "My Workout Mix",
  "description": "High energy tracks",
  "public": true,
  "collaborative": false
}

Response (201 Created):
{
  "playlist_id": "playlist_xyz",
  "name": "My Workout Mix",
  "description": "High energy tracks",
  "owner": {
    "user_id": "user_123",
    "display_name": "John Doe"
  },
  "public": true,
  "collaborative": false,
  "tracks_count": 0,
  "followers": 0,
  "url": "https://open.spotify.com/playlist/xyz",
  "created_at": "2025-11-12T12:00:00Z"
}
```

#### Add Tracks to Playlist
```http
POST /api/v1/playlists/{playlist_id}/tracks
Authorization: Bearer {token}

Request:
{
  "track_ids": ["track_abc", "track_def", "track_ghi"],
  "position": 0 // Insert at beginning, null for end
}

Response (200 OK):
{
  "snapshot_id": "snapshot_v2", // Version ID for playlist state
  "tracks_added": 3
}
```

#### Get Playlist
```http
GET /api/v1/playlists/{playlist_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "playlist_id": "playlist_xyz",
  "name": "My Workout Mix",
  "description": "High energy tracks",
  "owner": {...},
  "public": true,
  "collaborative": false,
  "tracks": [
    {
      "track_id": "track_abc",
      "title": "Song Title",
      "artists": [...],
      "album": {...},
      "duration_ms": 210000,
      "added_at": "2025-11-12T12:00:00Z",
      "added_by": {"user_id": "user_123"}
    }
  ],
  "tracks_count": 25,
  "followers": 150,
  "snapshot_id": "snapshot_v2"
}
```

### Search

#### Search Content
```http
GET /api/v1/search?q=billie+eilish&type=track,artist,album&limit=20
Authorization: Bearer {token}

Response (200 OK):
{
  "tracks": [
    {
      "track_id": "track_abc",
      "title": "Bad Guy",
      "artists": [{"artist_id": "artist_be", "name": "Billie Eilish"}],
      "album": {...},
      "duration_ms": 194000,
      "popularity": 95
    }
  ],
  "artists": [
    {
      "artist_id": "artist_be",
      "name": "Billie Eilish",
      "genres": ["pop", "electropop"],
      "followers": 50000000,
      "image_url": "https://i.scdn.co/image/artist_be"
    }
  ],
  "albums": [...],
  "total_results": 450,
  "search_time_ms": 125
}
```

### Recommendations

#### Get Personalized Recommendations
```http
GET /api/v1/recommendations?seed_tracks=track_abc,track_def&limit=20
Authorization: Bearer {token}

Response (200 OK):
{
  "tracks": [
    {
      "track_id": "track_xyz",
      "title": "Recommended Song",
      "artists": [...],
      "album": {...},
      "match_score": 0.92,
      "reason": "Based on your recent listening"
    }
  ],
  "seeds": [
    {"type": "track", "id": "track_abc"},
    {"type": "track", "id": "track_def"}
  ]
}
```

#### Get Discover Weekly
```http
GET /api/v1/playlists/discover-weekly
Authorization: Bearer {token}

Response (200 OK):
{
  "playlist_id": "auto_discover_weekly_user123",
  "name": "Discover Weekly",
  "description": "Your weekly mixtape of fresh music. Enjoy new music and deep cuts picked for you. Updates every Monday.",
  "tracks": [ /* 30 tracks */ ],
  "generated_at": "2025-11-11T00:00:00Z", // Monday
  "expires_at": "2025-11-18T00:00:00Z"
}
```

### Social Features

#### Follow Artist
```http
PUT /api/v1/me/following/artists/{artist_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "following": true,
  "artist_id": "artist_be"
}
```

#### Get User's Activity Feed
```http
GET /api/v1/me/social/feed?limit=20
Authorization: Bearer {token}

Response (200 OK):
{
  "activities": [
    {
      "activity_id": "act_123",
      "user": {
        "user_id": "friend_456",
        "display_name": "Jane"
      },
      "type": "playlist_created",
      "playlist": {...},
      "timestamp": "2025-11-12T10:00:00Z"
    },
    {
      "activity_id": "act_124",
      "user": {...},
      "type": "artist_followed",
      "artist": {...},
      "timestamp": "2025-11-12T09:30:00Z"
    }
  ]
}
```

### Offline Downloads

#### Get Download Status
```http
GET /api/v1/downloads
Authorization: Bearer {token}

Response (200 OK):
{
  "downloads": [
    {
      "track_id": "track_abc",
      "status": "completed",
      "downloaded_at": "2025-11-10T15:00:00Z",
      "size_bytes": 8388608,
      "quality": "high",
      "expires_at": "2025-12-10T15:00:00Z" // 30 days
    }
  ],
  "total_downloads": 50,
  "storage_used_bytes": 419430400,
  "download_limit": 10000 // Premium tier limit
}
```

## 6. Storage Strategy

### Audio Storage

**File Organization:**
```
gs://spotify-audio/
├── tracks/
│   ├── 00/
│   │   └── 00/
│   │       └── 0000/
│   │           └── track_abc123/
│   │               ├── 320kbps.ogg
│   │               ├── 160kbps.ogg
│   │               └── 96kbps.ogg
│   └── ...
├── previews/ (30-second clips)
│   └── track_abc123_preview.mp3
└── artwork/
    ├── albums/
    │   └── album_789/
    │       ├── 640x640.jpg
    │       ├── 300x300.jpg
    │       └── 64x64.jpg
    └── artists/
        └── artist_456/
            └── profile.jpg
```

**Audio Format:**
- **Codec**: Ogg Vorbis (primary), AAC (fallback)
- **Quality Tiers**:
  - Free: 160 kbps (Ogg Vorbis)
  - Premium: 320 kbps (Ogg Vorbis)
  - Podcasts: 96 kbps (optimized for speech)

**DRM (Digital Rights Management):**
```
Encrypted audio stream with Widevine/FairPlay
- Encryption key provided in play response
- Key rotation every 24 hours
- Device-specific decryption
```

### Database Schema

**PostgreSQL (Relational Data):**

```sql
-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    country VARCHAR(2),
    subscription_tier VARCHAR(20), -- free, premium, family
    subscription_status VARCHAR(20), -- active, cancelled, expired
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    profile_image_url VARCHAR(500)
);

-- Artists table
CREATE TABLE artists (
    artist_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    genres TEXT[], -- Array of genres
    verified BOOLEAN DEFAULT FALSE,
    follower_count BIGINT DEFAULT 0,
    monthly_listeners BIGINT DEFAULT 0,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Albums table
CREATE TABLE albums (
    album_id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id UUID REFERENCES artists(artist_id),
    release_date DATE,
    album_type VARCHAR(20), -- album, single, compilation
    total_tracks INT,
    genres TEXT[],
    label VARCHAR(255),
    artwork_url VARCHAR(500),
    popularity INT DEFAULT 0, -- 0-100 score

    INDEX idx_artist (artist_id),
    INDEX idx_release_date (release_date DESC)
);

-- Tracks table
CREATE TABLE tracks (
    track_id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    album_id UUID REFERENCES albums(album_id),
    track_number INT,
    disc_number INT DEFAULT 1,
    duration_ms INT NOT NULL,
    explicit BOOLEAN DEFAULT FALSE,
    isrc VARCHAR(20), -- International Standard Recording Code
    popularity INT DEFAULT 0,
    preview_url VARCHAR(500),
    storage_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_album (album_id),
    INDEX idx_popularity (popularity DESC)
);

-- Track artists (many-to-many)
CREATE TABLE track_artists (
    track_id UUID REFERENCES tracks(track_id),
    artist_id UUID REFERENCES artists(artist_id),
    position INT DEFAULT 0, -- Primary artist = 0, features = 1,2,3...

    PRIMARY KEY (track_id, artist_id)
);

-- Playlists table
CREATE TABLE playlists (
    playlist_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_user_id UUID REFERENCES users(user_id),
    public BOOLEAN DEFAULT TRUE,
    collaborative BOOLEAN DEFAULT FALSE,
    tracks_count INT DEFAULT 0,
    follower_count BIGINT DEFAULT 0,
    snapshot_id VARCHAR(100), -- Version ID for playlist state
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_owner (owner_user_id),
    INDEX idx_public (public, follower_count DESC)
);

-- Playlist tracks (ordered)
CREATE TABLE playlist_tracks (
    playlist_id UUID REFERENCES playlists(playlist_id),
    track_id UUID REFERENCES tracks(track_id),
    position INT NOT NULL,
    added_at TIMESTAMP DEFAULT NOW(),
    added_by_user_id UUID REFERENCES users(user_id),

    PRIMARY KEY (playlist_id, position),
    INDEX idx_playlist (playlist_id, position)
);

-- User saved tracks (Liked Songs)
CREATE TABLE user_saved_tracks (
    user_id UUID REFERENCES users(user_id),
    track_id UUID REFERENCES tracks(track_id),
    saved_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (user_id, track_id),
    INDEX idx_user_saved (user_id, saved_at DESC)
);

-- Follows (users follow artists)
CREATE TABLE follows (
    user_id UUID REFERENCES users(user_id),
    artist_id UUID REFERENCES artists(artist_id),
    followed_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (user_id, artist_id),
    INDEX idx_user (user_id),
    INDEX idx_artist (artist_id)
);

-- Social follows (users follow users)
CREATE TABLE user_follows (
    follower_user_id UUID REFERENCES users(user_id),
    followed_user_id UUID REFERENCES users(user_id),
    followed_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (follower_user_id, followed_user_id),
    INDEX idx_follower (follower_user_id),
    INDEX idx_followed (followed_user_id)
);
```

**Cassandra (Time-Series Data):**

```sql
-- Listening history
CREATE TABLE listening_history (
    user_id UUID,
    timestamp TIMESTAMP,
    track_id UUID,
    context_type TEXT, -- playlist, album, artist, search
    context_id UUID,
    duration_played_ms INT,
    completed BOOLEAN,
    skipped BOOLEAN,
    quality TEXT,
    device_id UUID,

    PRIMARY KEY ((user_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Recently played
CREATE TABLE recently_played (
    user_id UUID,
    timestamp TIMESTAMP,
    track_id UUID,
    context_uri TEXT,

    PRIMARY KEY ((user_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
AND default_time_to_live = 2592000; -- 30 days TTL

-- Track play counts (for analytics)
CREATE TABLE track_plays_daily (
    track_id UUID,
    date DATE,
    play_count COUNTER,
    unique_listeners COUNTER,
    total_duration_ms COUNTER,

    PRIMARY KEY ((track_id), date)
) WITH CLUSTERING ORDER BY (date DESC);
```

## 7. Streaming Protocol

### Audio Streaming Flow

```
Client Request to Play Track
    ↓
1. API Gateway → Play Service
    ↓
2. Check user subscription (premium/free)
    ↓
3. Fetch track metadata from PostgreSQL
    ↓
4. Generate streaming URLs (CDN + signature)
    ↓
5. Return streaming URLs to client
    ↓
6. Client downloads audio chunks from CDN
    ↓
7. Local playback with buffering
    ↓
8. Report playback events to Analytics Service
```

### Chunked Streaming

**Why chunking?**
- Resume playback quickly
- Adaptive quality switching
- Efficient CDN caching

**Implementation:**
```
Track divided into 10-second chunks:
- track_abc123/320kbps/chunk_0.ogg (0-10 sec)
- track_abc123/320kbps/chunk_1.ogg (10-20 sec)
- track_abc123/320kbps/chunk_2.ogg (20-30 sec)
...
- track_abc123/320kbps/chunk_21.ogg (210-220 sec)
```

**Client Buffering Strategy:**
```python
class AudioPlayer:
    def __init__(self, track_id, quality):
        self.track_id = track_id
        self.quality = quality
        self.buffer = []
        self.current_chunk = 0
        self.buffer_target = 30  # seconds

    async def start_playback(self):
        # 1. Preload first 3 chunks (30 seconds)
        for i in range(3):
            chunk = await self.download_chunk(i)
            self.buffer.append(chunk)

        # 2. Start playing
        self.play(self.buffer[0])
        self.current_chunk = 0

        # 3. Background: Keep buffer filled
        asyncio.create_task(self.maintain_buffer())

    async def maintain_buffer(self):
        while self.is_playing:
            # Buffer next 3 chunks ahead of current position
            for i in range(self.current_chunk + 1, self.current_chunk + 4):
                if i not in self.buffered_chunks():
                    chunk = await self.download_chunk(i)
                    self.buffer.append(chunk)

            await asyncio.sleep(5)  # Check every 5 seconds

    async def download_chunk(self, chunk_index):
        url = f"https://audio-cdn.spotify.com/{self.track_id}/{self.quality}/chunk_{chunk_index}.ogg"
        response = await http_client.get(url)
        return response.content

    def handle_quality_switch(self, new_quality):
        # Switch quality mid-playback
        self.quality = new_quality

        # Clear buffer, reload current chunk in new quality
        self.buffer.clear()
        current_time = self.get_current_position()
        chunk_index = current_time // 10  # 10 sec per chunk

        chunk = self.download_chunk(chunk_index)
        self.play_from_chunk(chunk, offset=current_time % 10)
```

### Adaptive Quality

**Bandwidth Detection:**
```python
def detect_bandwidth():
    # Download small test chunk, measure speed
    start = time.time()
    test_chunk = download("https://cdn.spotify.com/test_chunk.ogg")
    duration = time.time() - start

    size_mb = len(test_chunk) / (1024 * 1024)
    bandwidth_mbps = (size_mb * 8) / duration

    return bandwidth_mbps

def select_quality(bandwidth_mbps, user_subscription):
    if user_subscription == 'free':
        max_quality = 160  # kbps
    else:
        max_quality = 320  # kbps

    # Select quality with 50% safety margin
    safe_bandwidth_kbps = bandwidth_mbps * 1024 * 0.5

    if safe_bandwidth_kbps >= max_quality:
        return max_quality
    elif safe_bandwidth_kbps >= 160:
        return 160
    else:
        return 96  # Minimum quality
```

## 8. Recommendation System

### Spotify's Recommendation Approach

**Three Main Algorithms:**

1. **Collaborative Filtering**: Users who like similar music
2. **Content-Based Filtering**: Audio analysis (tempo, key, loudness)
3. **Natural Language Processing**: Analyze text (blogs, reviews)

### Discover Weekly Implementation

**Goal:** Generate 30-song personalized playlist every Monday

**Algorithm:**

```python
def generate_discover_weekly(user_id):
    # 1. Get user's listening history (last 90 days)
    user_history = get_listening_history(user_id, days=90)

    # Extract favorite artists, genres, audio features
    favorite_artists = extract_top_artists(user_history, limit=50)
    favorite_genres = extract_top_genres(user_history)
    audio_features = extract_audio_features(user_history)

    # 2. Collaborative filtering: Find similar users
    similar_users = find_similar_users(user_id, limit=1000)

    # 3. Get tracks liked by similar users (but not by this user)
    candidate_tracks = []
    for other_user in similar_users:
        other_tracks = get_liked_tracks(other_user)
        for track in other_tracks:
            if track not in user_history:
                candidate_tracks.append(track)

    # 4. Score each candidate
    scored_tracks = []
    for track in candidate_tracks:
        score = 0

        # Artist match
        if track.artist in favorite_artists:
            score += 10

        # Genre match
        genre_overlap = len(set(track.genres) & set(favorite_genres))
        score += genre_overlap * 5

        # Audio feature similarity
        track_features = get_audio_features(track.id)
        feature_similarity = cosine_similarity(audio_features, track_features)
        score += feature_similarity * 20

        # Popularity (slight bias toward popular tracks)
        score += track.popularity * 0.1

        # Freshness (prefer newer tracks)
        days_old = (now() - track.release_date).days
        if days_old < 90:
            score += (90 - days_old) / 10

        scored_tracks.append((track, score))

    # 5. Sort by score and diversify
    sorted_tracks = sorted(scored_tracks, key=lambda x: x[1], reverse=True)

    # 6. Apply diversity rules
    final_tracks = []
    artist_count = {}

    for track, score in sorted_tracks:
        # Max 2 tracks per artist
        if artist_count.get(track.artist, 0) < 2:
            final_tracks.append(track)
            artist_count[track.artist] = artist_count.get(track.artist, 0) + 1

        if len(final_tracks) >= 30:
            break

    # 7. Create playlist
    playlist = create_playlist(
        user_id,
        name="Discover Weekly",
        description="Your weekly mixtape of fresh music",
        tracks=final_tracks
    )

    return playlist
```

### Audio Feature Analysis

**Spotify's Audio Analysis:**
```python
# Using Essentia or librosa for audio analysis
def analyze_audio_features(track_file):
    audio, sr = librosa.load(track_file)

    features = {
        # Tempo (BPM)
        'tempo': librosa.beat.tempo(audio, sr=sr)[0],

        # Key (0-11, C=0, C#=1, ..., B=11)
        'key': estimate_key(audio),

        # Mode (0=minor, 1=major)
        'mode': estimate_mode(audio),

        # Loudness (dB)
        'loudness': librosa.feature.rms(y=audio).mean(),

        # Energy (0-1)
        'energy': calculate_energy(audio),

        # Danceability (0-1)
        'danceability': calculate_danceability(audio),

        # Valence (0-1, happiness/positivity)
        'valence': calculate_valence(audio),

        # Speechiness (0-1, presence of spoken words)
        'speechiness': calculate_speechiness(audio),

        # Acousticness (0-1, acoustic vs. electronic)
        'acousticness': calculate_acousticness(audio),

        # Instrumentalness (0-1, vocal presence)
        'instrumentalness': calculate_instrumentalness(audio),

        # Time signature
        'time_signature': estimate_time_signature(audio)
    }

    return features
```

**Storing Audio Features:**
```sql
CREATE TABLE audio_features (
    track_id UUID PRIMARY KEY REFERENCES tracks(track_id),
    tempo FLOAT,
    key INT, -- 0-11
    mode INT, -- 0=minor, 1=major
    loudness FLOAT,
    energy FLOAT,
    danceability FLOAT,
    valence FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    time_signature INT,
    duration_ms INT,

    INDEX idx_tempo (tempo),
    INDEX idx_energy (energy),
    INDEX idx_danceability (danceability)
);
```

### Daily Mix Generation

**Goal:** Generate 6 playlists with different genres/moods

```python
def generate_daily_mixes(user_id):
    # 1. Cluster user's listening history by genre/mood
    user_history = get_listening_history(user_id, days=180)

    # 2. Apply K-means clustering (k=6)
    clusters = kmeans_clustering(user_history, k=6)

    daily_mixes = []

    for i, cluster in enumerate(clusters):
        # 3. For each cluster, find similar tracks
        cluster_features = extract_average_features(cluster)
        similar_tracks = find_tracks_by_features(
            cluster_features,
            limit=50
        )

        # 4. Mix familiar (80%) and new (20%) tracks
        familiar = [t for t in similar_tracks if t in user_history][:40]
        new = [t for t in similar_tracks if t not in user_history][:10]

        mix_tracks = familiar + new
        shuffle(mix_tracks)

        # 5. Create playlist
        playlist = create_playlist(
            user_id,
            name=f"Daily Mix {i+1}",
            description=f"Made for {user.display_name}",
            tracks=mix_tracks
        )

        daily_mixes.append(playlist)

    return daily_mixes
```

## 9. Scalability & Performance

### Horizontal Scaling

**Microservices Auto-Scaling:**
```
Streaming Service:
- 500+ instances (peak)
- Scale based on concurrent streams
- Target: 10,000 concurrent streams per instance

Play Service:
- 200+ instances
- Scale based on API requests/sec
- Target: 500 RPS per instance

Recommendation Service:
- 100+ instances
- ML model inference
- GPU instances for heavy models
```

### Database Scaling

**PostgreSQL Sharding:**
```
Shard by user_id hash:
- Shard 0: user_id % 10 == 0
- Shard 1: user_id % 10 == 1
- ...
- Shard 9: user_id % 10 == 9

Each shard:
- Master (writes)
- 2 Read Replicas (reads)

Routing logic in application layer
```

**Cassandra Scaling:**
```
Ring architecture:
- 100+ nodes
- Replication factor: 3
- Partition key: user_id (for listening_history)
- Automatic data distribution
```

### Caching Strategy

**Redis Cache:**
```python
# Cache popular tracks metadata
def get_track(track_id):
    cache_key = f"track:{track_id}"
    cached = redis.get(cache_key)

    if cached:
        return json.loads(cached)

    # Cache miss
    track = db.query_track(track_id)
    redis.setex(cache_key, 3600, json.dumps(track))  # 1 hour TTL

    return track

# Cache user's current playback state
def get_playback_state(user_id):
    cache_key = f"playback:{user_id}"
    return redis.get(cache_key)

def update_playback_state(user_id, state):
    cache_key = f"playback:{user_id}"
    redis.setex(cache_key, 600, json.dumps(state))  # 10 min TTL

# Cache playlists
def get_playlist(playlist_id):
    cache_key = f"playlist:{playlist_id}"
    cached = redis.get(cache_key)

    if cached:
        return json.loads(cached)

    playlist = db.query_playlist(playlist_id)
    redis.setex(cache_key, 1800, json.dumps(playlist))  # 30 min TTL

    return playlist
```

**CDN Caching:**
```
Audio files:
- Cache forever (immutable content)
- Cache-Control: public, max-age=31536000, immutable

Artwork:
- Cache for 24 hours
- Cache-Control: public, max-age=86400

API responses (optional):
- Cache for 60 seconds
- Vary by Authorization header
```

### Performance Optimizations

**1. Prefetching:**
```python
# Prefetch next track in queue
def on_track_start(current_track, next_track):
    # Preload first 2 chunks of next track
    for i in range(2):
        url = f"https://cdn.spotify.com/{next_track.id}/320kbps/chunk_{i}.ogg"
        prefetch(url)
```

**2. Connection Pooling:**
```python
# Database connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=10,
    maxconn=100,
    host='db.spotify.com',
    database='spotify'
)

# HTTP connection pooling
http_session = requests.Session()
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
http_session.mount('https://', adapter)
```

**3. Batch Operations:**
```python
# Batch track metadata fetches
def get_tracks_batch(track_ids):
    # Single query instead of N queries
    query = "SELECT * FROM tracks WHERE track_id IN %s"
    tracks = db.execute(query, (tuple(track_ids),))
    return tracks
```

## 10. Trade-offs

### Full Track Storage vs. Chunked

**Chunked (Spotify approach):**
- ✅ Fast seek/skip
- ✅ Better CDN caching
- ✅ Adaptive quality switching
- ❌ More files to manage
- ❌ Slightly higher storage overhead

**Full Track:**
- ✅ Simpler implementation
- ✅ Lower storage overhead
- ❌ Slower seeks
- ❌ Must re-download for quality change

**Decision:** Chunked for better UX

### Real-time vs. Batch Recommendations

**Real-time:**
- ✅ Reflects latest behavior immediately
- ❌ High computational cost
- ❌ Increased latency

**Batch (Discover Weekly approach):**
- ✅ Lower cost (pre-computed)
- ✅ Fast response
- ❌ Updated weekly (stale)

**Decision:** Hybrid (weekly batch + real-time adjustments)

### Free vs. Premium Quality

**Free Tier (160 kbps):**
- ✅ Lower bandwidth costs
- ✅ Incentivizes premium upgrades
- ❌ Lower perceived quality

**Premium (320 kbps):**
- ✅ Better audio quality
- ✅ Competitive with Apple Music
- ❌ Higher bandwidth costs

**Decision:** Tiered quality (business model requirement)

## 11. Follow-up Questions

1. **How would you implement lyrics display synchronized with playback?**
   - Store lyrics with timestamps (LRC format)
   - Client fetches lyrics on playback start
   - Highlight current line based on playback position
   - Cache lyrics locally

2. **How do you handle offline playlist sync?**
   - Download tracks to local storage (encrypted)
   - Store playlist metadata locally (SQLite)
   - Sync changes when online
   - Expire downloads after 30 days of no connectivity

3. **How would you implement collaborative playlists?**
   - WebSocket for real-time updates
   - Optimistic UI updates (immediate feedback)
   - Conflict resolution (last-write-wins)
   - Activity log (who added/removed what)

4. **How do you prevent music piracy/DRM circumvention?**
   - Encrypt audio files with DRM (Widevine)
   - Device-specific decryption keys
   - Watermarking audio (embed user_id)
   - Detect unauthorized apps/clients

5. **How would you implement a social listening party (Group Session)?**
   - Host creates session, generates shareable link
   - WebSocket for real-time sync
   - Host controls playback, others follow
   - Queue: Participants can add songs
   - Handle latency (buffer to sync playback position)

6. **How do you optimize for low-bandwidth users?**
   - Adaptive quality (start at 96 kbps)
   - Smaller chunk sizes (5-second instead of 10)
   - Prefetch only 1-2 chunks ahead
   - Option to set maximum quality
   - Offline mode (download on WiFi)

7. **How would you implement a "Behind the Lyrics" feature (Genius integration)?**
   - Partner with Genius API
   - Fetch annotations for track
   - Display at specific timestamps
   - Cache annotations

8. **How do you handle artist royalty tracking?**
   - Log every play (user_id, track_id, duration)
   - Daily aggregation: Track → Artist → Royalty calculation
   - Store in BigQuery/data warehouse
   - Payment processing separate system

9. **How would you implement podcast support?**
   - Similar to music but different metadata
   - Episodic structure (show → season → episode)
   - Variable length (5 min to 3 hours)
   - Lower quality (96 kbps speech-optimized)
   - Playback position saving per episode

10. **How do you handle geographic licensing restrictions?**
    - Store `available_countries` per track
    - Check user's country on playback request
    - Return error if not available
    - Filter search results by country
    - VPN detection (ban if detected)

## Complexity Analysis

- **Time Complexity:**
  - Play track: O(1) metadata fetch
  - Search: O(log n) with indexing
  - Recommendations: O(k × m) where k = candidates, m = features
  - Playlist operations: O(1) for append, O(n) for reorder

- **Space Complexity:**
  - Total storage: O(t × q) where t = tracks, q = qualities
  - User data: O(u × h) where u = users, h = history size
  - Cache: O(popular_tracks × metadata_size)

## References

- [How Spotify Scales](https://engineering.atspotify.com/)
- [Discover Weekly Algorithm](https://qz.com/571007/the-magic-that-makes-spotifys-discover-weekly-playlists-so-damn-good/)
- [Audio Feature Analysis](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)
- [Cassandra at Spotify](https://engineering.atspotify.com/2015/01/09/cassandra-at-spotify/)
- [Personalization at Spotify](https://engineering.atspotify.com/category/personalization/)
