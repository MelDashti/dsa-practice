# Medium Level - Storage & Data System Design

This folder contains intermediate-level system design problems focused on distributed storage, streaming platforms, and data-intensive applications. These problems require understanding of scalability, consistency, and complex data flows.

## Problems

### 1. Design Dropbox (Cloud Storage with Sync)
**File:** `design_dropbox.md`

Design a cloud storage service with automatic file synchronization across devices.

**Key Concepts:**
- File chunking and deduplication
- Conflict resolution
- Delta sync
- Offline mode
- Version history
- Client-server synchronization

### 2. Design Google Drive (File Sharing & Collaboration)
**File:** `design_google_drive.md`

Design a collaborative cloud storage platform with advanced permissions and real-time features.

**Key Concepts:**
- Granular permissions (view, comment, edit)
- Shared folders and inheritance
- Search indexing (Elasticsearch)
- Real-time collaboration
- Activity tracking
- Comments and notifications

### 3. Design YouTube (Video Streaming Platform)
**File:** `design_youtube.md`

Design a video streaming platform that handles uploads, transcoding, and billions of views.

**Key Concepts:**
- Video transcoding pipeline
- Adaptive bitrate streaming (HLS/DASH)
- CDN distribution
- Content recommendations
- Search and discovery
- Analytics and view tracking

### 4. Design Netflix (Video Streaming with CDN)
**File:** `design_netflix.md`

Design a subscription-based video streaming service optimized for quality and global reach.

**Key Concepts:**
- Open Connect CDN architecture
- Pre-encoding strategies
- Per-title encoding optimization
- Personalized recommendations
- Content popularity prediction
- Offline downloads

### 5. Design Spotify (Music Streaming)
**File:** `design_spotify.md`

Design a music streaming service with personalized playlists and social features.

**Key Concepts:**
- Audio streaming protocols
- Discover Weekly algorithm
- Collaborative filtering
- Audio feature analysis
- Playlist management
- Offline mode with DRM

## Common Patterns

### Storage Patterns
- **Chunking**: Split large files for efficient updates and transfers
- **Deduplication**: Store identical chunks once to save space
- **Tiering**: Hot (SSD) vs. cold (HDD) storage based on access patterns
- **CDN**: Edge caching for global low-latency access

### Data Patterns
- **Sharding**: Partition data by user_id or content_id
- **Replication**: 3x replication or erasure coding for durability
- **Caching**: Multi-level (L1: client, L2: CDN, L3: Redis, L4: DB)
- **Indexing**: Elasticsearch for full-text search

### Consistency Patterns
- **Eventual Consistency**: Acceptable for most media/file content
- **Strong Consistency**: Required for metadata, permissions
- **Conflict Resolution**: Last-write-wins, vector clocks, operational transformation

### Recommendation Patterns
- **Collaborative Filtering**: Users with similar tastes
- **Content-Based**: Similar items by features
- **Hybrid Models**: Combine multiple algorithms
- **A/B Testing**: Continuously improve recommendations

## Study Approach

1. **Start with Architecture**: Draw high-level diagrams showing data flow
2. **Scale Calculations**: Always estimate storage, bandwidth, QPS
3. **Focus on Bottlenecks**: Identify and address scalability bottlenecks
4. **Trade-off Analysis**: Compare different approaches (pros/cons)
5. **Optimize Progressively**: Start simple, then optimize specific areas

## Key Technologies

### Storage
- **Blob Storage**: S3, Google Cloud Storage (GCS)
- **Databases**: PostgreSQL, MySQL (relational), Cassandra, DynamoDB (NoSQL)
- **Search**: Elasticsearch, Algolia
- **Cache**: Redis, Memcached

### Streaming
- **Protocols**: HLS (HTTP Live Streaming), DASH (Dynamic Adaptive Streaming)
- **Encoding**: FFmpeg, HandBrake
- **CDN**: CloudFront, Akamai, Fastly

### Machine Learning
- **Recommendations**: Collaborative filtering, matrix factorization
- **Frameworks**: TensorFlow, PyTorch, scikit-learn
- **Feature Engineering**: Audio analysis (librosa), video analysis

## Interview Tips

1. **Clarify Requirements**: Ask about scale, features, constraints
2. **Start High-Level**: Don't dive into details too early
3. **Justify Decisions**: Explain why you chose specific technologies
4. **Discuss Trade-offs**: Show you understand different approaches
5. **Handle Follow-ups**: Be prepared for "what if" scenarios

## Next Steps

After mastering Medium problems, advance to Hard level covering:
- S3-like distributed object storage
- Distributed key-value stores (DynamoDB/Cassandra)
- Large-scale email systems
- Real-time video conferencing (Zoom)

## Resources

- [Designing Data-Intensive Applications (Book)](https://dataintensive.net/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability Blog](http://highscalability.com/)
- [Netflix Tech Blog](https://netflixtechblog.com/)
- [Spotify Engineering Blog](https://engineering.atspotify.com/)
- [YouTube at Scale](https://www.youtube.com/watch?v=5BzSj7bxKBw)
