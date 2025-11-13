# Design Dropbox (Cloud Storage with Sync)

**Difficulty:** Medium

## 1. Problem Statement

Design a cloud storage service like Dropbox that allows users to store files in the cloud and automatically synchronize them across multiple devices. Users should be able to access their files from any device, share files with others, and have their changes automatically synced in real-time.

**Key Features:**
- File upload/download across devices
- Automatic file synchronization
- File sharing with other users
- Version history
- Offline access with sync when online

## 2. Requirements

### Functional Requirements
1. **File Upload/Download**: Users can upload and download files
2. **File Synchronization**: Automatic sync across all user devices
3. **File Sharing**: Share files/folders with other users
4. **Version History**: Track file versions, allow rollback
5. **Notifications**: Notify users of changes/sync events
6. **Conflict Resolution**: Handle concurrent edits
7. **Offline Mode**: Work offline, sync when reconnected

### Non-Functional Requirements
1. **Availability**: 99.99% uptime
2. **Consistency**: Strong consistency for file operations
3. **Durability**: 99.999999999% durability (11 nines)
4. **Scalability**: Support 500M users, 1B files
5. **Performance**:
   - Sync latency < 1 second for small files
   - Upload/download 100 MB file in < 30 seconds
6. **Reliability**: No data loss during sync

### Out of Scope
- Real-time collaborative editing (like Google Docs)
- Advanced admin features for enterprise
- Built-in file preview (can be added later)

## 3. Storage Estimation

### Assumptions
- **Total Users**: 500 million
- **Active Users**: 100 million daily active users (DAU)
- **Average Files per User**: 200 files
- **Average File Size**: 100 KB
- **Storage per User**: 2 GB average
- **Sync Operations**: Each user syncs 5 files per day
- **Data Retention**: Versions kept for 30 days

### Calculations

**Total Storage:**
```
500M users × 2 GB = 1,000,000,000 GB = 1 Exabyte (EB)
With replication (3x): 3 EB
```

**Total Files:**
```
500M users × 200 files = 100 billion files
```

**Daily Sync Operations:**
```
100M DAU × 5 syncs/day = 500M sync operations/day
= 5,787 syncs/second average
Peak (10x): 57,870 syncs/second
```

**Bandwidth Requirements:**
```
Assuming 1 MB average sync size:
500M syncs/day × 1 MB = 500 TB/day
= 5.79 GB/second average
Peak: 57.9 GB/second
```

**Metadata Storage:**
```
Per file metadata: 1 KB (path, size, hash, timestamps, permissions)
100B files × 1 KB = 100 TB metadata
```

**Database QPS:**
```
File operations: 5,787 syncs/sec × 3 DB queries/sync = ~17,000 QPS
Peak: 170,000 QPS
```

## 4. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │Desktop App  │  │ Mobile App  │  │  Web App    │         │
│  │ + Watcher   │  │ + Watcher   │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS/WebSocket
                           ▼
                ┌────────────────────┐
                │   Load Balancer    │
                │  (Geographic LB)   │
                └──────────┬─────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   API        │  │Sync Service  │  │Notification  │
│  Servers     │  │  (WebSocket) │  │  Service     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       │     ┌───────────┴──────┐          │
       │     │                  │          │
       ▼     ▼                  ▼          ▼
┌─────────────────┐     ┌──────────────────────┐
│  Metadata DB    │     │   Message Queue      │
│   (MySQL +      │     │   (Kafka/RabbitMQ)   │
│   Cassandra)    │     └──────────────────────┘
└─────────────────┘
       │
       │
       ▼
┌─────────────────────────────────────────┐
│          Block Server Cluster           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Block    │  │ Block    │  │ Block  ││
│  │ Server 1 │  │ Server 2 │  │Server N││
│  └────┬─────┘  └────┬─────┘  └───┬────┘│
└───────┼─────────────┼────────────┼──────┘
        │             │            │
        └─────────────┼────────────┘
                      ▼
        ┌──────────────────────────┐
        │   Cloud Blob Storage     │
        │      (S3 / GCS)          │
        │   ┌─────────────────┐    │
        │   │ Chunks Storage  │    │
        │   └─────────────────┘    │
        └──────────────────────────┘
```

### Key Components

1. **Client Applications**: Desktop/mobile apps with file system watchers
2. **Load Balancer**: Routes requests to appropriate service
3. **API Servers**: Handle REST API requests (upload, download, share)
4. **Sync Service**: Maintains WebSocket connections for real-time sync
5. **Notification Service**: Sends push notifications to clients
6. **Metadata Database**: Stores file metadata, user info, permissions
7. **Message Queue**: Asynchronous task processing (Kafka)
8. **Block Servers**: Handle chunking, deduplication, compression
9. **Cloud Blob Storage**: Stores actual file chunks (S3)

## 5. API Design

### File Operations

#### Upload File
```http
POST /api/v1/files/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

Request Body:
{
  "file": binary,
  "path": "/Documents/report.pdf",
  "device_id": "device_123",
  "modified_time": "2025-11-12T10:30:00Z"
}

Response (201 Created):
{
  "file_id": "file_abc123",
  "version_id": "v1",
  "path": "/Documents/report.pdf",
  "size": 2048576,
  "modified_time": "2025-11-12T10:30:00Z",
  "checksum": "md5:abc123def456"
}
```

#### Download File
```http
GET /api/v1/files/download?path=/Documents/report.pdf
Authorization: Bearer {token}

Response (200 OK):
- Binary file data
- Headers:
  Content-Type: application/pdf
  X-File-Version: v1
  ETag: "abc123def456"
```

#### Get File Metadata
```http
GET /api/v1/files/metadata?path=/Documents/report.pdf
Authorization: Bearer {token}

Response (200 OK):
{
  "file_id": "file_abc123",
  "path": "/Documents/report.pdf",
  "size": 2048576,
  "modified_time": "2025-11-12T10:30:00Z",
  "version_id": "v1",
  "checksum": "md5:abc123def456",
  "is_folder": false,
  "shared": false
}
```

#### List Files
```http
GET /api/v1/files/list?path=/Documents&recursive=false
Authorization: Bearer {token}

Response (200 OK):
{
  "files": [
    {
      "path": "/Documents/report.pdf",
      "size": 2048576,
      "modified_time": "2025-11-12T10:30:00Z",
      "is_folder": false
    },
    {
      "path": "/Documents/Images",
      "is_folder": true,
      "item_count": 15
    }
  ],
  "cursor": "next_page_token"
}
```

### Sync Operations

#### Get Sync Updates
```http
GET /api/v1/sync/updates?since={timestamp}&device_id=device_123
Authorization: Bearer {token}

Response (200 OK):
{
  "updates": [
    {
      "operation": "create",
      "path": "/Documents/new_file.txt",
      "file_id": "file_xyz",
      "version_id": "v1",
      "timestamp": "2025-11-12T10:35:00Z",
      "device_id": "device_456"
    },
    {
      "operation": "modify",
      "path": "/Documents/report.pdf",
      "version_id": "v2",
      "timestamp": "2025-11-12T10:36:00Z"
    }
  ],
  "latest_timestamp": "2025-11-12T10:36:00Z"
}
```

#### Request File Chunks
```http
POST /api/v1/chunks/query
Authorization: Bearer {token}

Request Body:
{
  "checksums": ["md5:chunk1", "md5:chunk2", "md5:chunk3"]
}

Response (200 OK):
{
  "missing_chunks": ["md5:chunk2"],
  "existing_chunks": ["md5:chunk1", "md5:chunk3"]
}
```

### Sharing Operations

#### Share File/Folder
```http
POST /api/v1/share
Authorization: Bearer {token}

Request Body:
{
  "path": "/Documents/report.pdf",
  "share_with": "user@example.com",
  "permission": "read" // or "write"
}

Response (200 OK):
{
  "share_id": "share_123",
  "share_link": "https://dropbox.com/s/abc123",
  "permission": "read",
  "expires_at": null
}
```

## 6. Storage Strategy

### Chunking & Deduplication

**Why Chunking?**
- **Efficient Updates**: Only sync changed chunks, not entire files
- **Deduplication**: Save storage by storing identical chunks once
- **Bandwidth Optimization**: Transfer only new/modified chunks
- **Resume Capability**: Resume failed uploads from last chunk

**Chunking Strategy:**
```
File: report.pdf (10 MB)
↓
Split into fixed-size chunks (4 MB each)
↓
Chunk 1 (4 MB) → MD5: abc123
Chunk 2 (4 MB) → MD5: def456
Chunk 3 (2 MB) → MD5: ghi789
```

**Chunk Size Selection:**
- **Fixed Size**: 4 MB chunks (most implementations)
- **Variable Size**: Content-defined chunking (CDC) using Rabin fingerprinting
  - Better deduplication for file edits
  - More complex to implement

### Block Server Architecture

**Process Flow:**
```
1. Client uploads file
   ↓
2. Block Server receives file
   ↓
3. Split into chunks (4 MB each)
   ↓
4. Calculate MD5 hash for each chunk
   ↓
5. Check if chunk already exists (deduplication)
   ↓
6. Upload only new chunks to S3
   ↓
7. Store chunk metadata in database
   ↓
8. Create file record with chunk references
```

**Chunk Metadata Schema:**
```sql
CREATE TABLE chunks (
    chunk_id VARCHAR(64) PRIMARY KEY, -- MD5 hash
    size INT NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    ref_count INT DEFAULT 1, -- How many files reference this chunk
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_ref_count (ref_count)
);

CREATE TABLE file_chunks (
    file_id VARCHAR(36) NOT NULL,
    version_id VARCHAR(36) NOT NULL,
    chunk_id VARCHAR(64) NOT NULL,
    chunk_order INT NOT NULL, -- Order of chunk in file

    PRIMARY KEY (file_id, version_id, chunk_order),
    FOREIGN KEY (chunk_id) REFERENCES chunks(chunk_id),
    INDEX idx_file_version (file_id, version_id)
);
```

### Metadata Storage

**Database Choice:**
- **Relational DB (MySQL)**: For structured data, transactions
- **NoSQL (Cassandra)**: For file metadata at scale

**Schema Design:**

```sql
-- Users table
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    storage_used BIGINT DEFAULT 0,
    storage_quota BIGINT DEFAULT 2147483648, -- 2 GB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Files metadata table
CREATE TABLE files (
    file_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    path VARCHAR(1000) NOT NULL,
    name VARCHAR(255) NOT NULL,
    size BIGINT NOT NULL,
    is_folder BOOLEAN DEFAULT FALSE,
    parent_folder_id VARCHAR(36),
    modified_time TIMESTAMP NOT NULL,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE,
    current_version_id VARCHAR(36),

    INDEX idx_user_path (user_id, path),
    INDEX idx_parent (parent_folder_id),
    INDEX idx_modified (modified_time),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Version history table
CREATE TABLE file_versions (
    version_id VARCHAR(36) PRIMARY KEY,
    file_id VARCHAR(36) NOT NULL,
    version_number INT NOT NULL,
    size BIGINT NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    modified_by VARCHAR(36) NOT NULL,
    modified_time TIMESTAMP NOT NULL,
    device_id VARCHAR(36),

    UNIQUE KEY uk_file_version (file_id, version_number),
    INDEX idx_file_id (file_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);

-- Sharing permissions
CREATE TABLE file_shares (
    share_id VARCHAR(36) PRIMARY KEY,
    file_id VARCHAR(36) NOT NULL,
    owner_id VARCHAR(36) NOT NULL,
    shared_with_user_id VARCHAR(36),
    permission ENUM('read', 'write') NOT NULL,
    share_link VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,

    INDEX idx_file_id (file_id),
    INDEX idx_shared_with (shared_with_user_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);

-- Device tracking
CREATE TABLE devices (
    device_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    device_name VARCHAR(100),
    device_type ENUM('desktop', 'mobile', 'web'),
    last_sync_time TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Sync state tracking
CREATE TABLE sync_state (
    user_id VARCHAR(36) NOT NULL,
    device_id VARCHAR(36) NOT NULL,
    file_id VARCHAR(36) NOT NULL,
    version_id VARCHAR(36) NOT NULL,
    sync_status ENUM('pending', 'syncing', 'synced', 'error'),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, device_id, file_id),
    INDEX idx_device_status (device_id, sync_status)
);
```

### Blob Storage Organization

```
s3://dropbox-storage/
├── chunks/
│   ├── ab/c1/abc123def456... (chunk stored by hash prefix)
│   ├── de/f4/def456ghi789...
│   └── ...
├── metadata/
│   └── backups/
└── thumbnails/ (optional)
    └── user_123/
        └── file_abc_thumb.jpg
```

## 7. Synchronization Strategy

### File Watcher (Client Side)

**Desktop Implementation:**
- Use OS-specific file system watchers
  - **Linux**: inotify
  - **macOS**: FSEvents
  - **Windows**: ReadDirectoryChangesW

**Events to Monitor:**
- File created
- File modified
- File deleted
- File moved/renamed

**Client Sync Logic:**
```python
class FileWatcher:
    def on_file_changed(self, file_path):
        # 1. Calculate file hash
        file_hash = calculate_md5(file_path)

        # 2. Check if file changed (compare with local cache)
        if file_hash == local_cache.get_hash(file_path):
            return  # No change

        # 3. Split file into chunks
        chunks = chunk_file(file_path, chunk_size=4MB)

        # 4. Query server: which chunks already exist?
        chunk_hashes = [chunk.hash for chunk in chunks]
        response = api.query_chunks(chunk_hashes)
        missing_chunks = response.missing_chunks

        # 5. Upload only missing chunks
        for chunk in chunks:
            if chunk.hash in missing_chunks:
                api.upload_chunk(chunk)

        # 6. Commit file metadata
        api.commit_file(file_path, chunk_hashes, file_hash)

        # 7. Update local cache
        local_cache.update(file_path, file_hash)
```

### Sync Service (Server Side)

**WebSocket Connection:**
- Each device maintains persistent WebSocket connection
- Server pushes sync events in real-time
- Fallback to polling if WebSocket unavailable

**Sync Algorithm:**

```python
class SyncService:
    def handle_file_upload(self, user_id, device_id, file_path, chunks):
        # 1. Store chunks in S3
        for chunk in chunks:
            if not chunk_exists(chunk.hash):
                s3.upload(chunk)
                db.create_chunk_record(chunk.hash)

        # 2. Create new version
        version = db.create_file_version(
            file_id=file.id,
            chunks=chunks,
            device_id=device_id
        )

        # 3. Notify other devices
        other_devices = db.get_user_devices(user_id, exclude=device_id)
        for device in other_devices:
            notification = {
                'type': 'file_updated',
                'file_path': file_path,
                'version_id': version.id,
                'chunks': [c.hash for c in chunks]
            }
            websocket.send(device.id, notification)

        # 4. Publish to message queue for async processing
        kafka.publish('file_events', {
            'event': 'file_updated',
            'user_id': user_id,
            'file_id': file.id,
            'version_id': version.id
        })
```

### Conflict Resolution

**Conflict Scenarios:**
1. Same file edited on multiple devices while offline
2. File deleted on one device, modified on another
3. Folder renamed while files inside are being edited

**Resolution Strategy:**

**1. Last-Write-Wins (Simple):**
- Use timestamp to determine winner
- Loser's version saved as conflict copy
- Example: `report (conflicted copy from Device-A).pdf`

**2. Version Vector (Advanced):**
- Each device maintains vector clock
- Detect true conflicts vs. causally ordered updates
- Only create conflict copy when necessary

**Implementation:**
```python
def resolve_conflict(file_a, file_b):
    # Compare modification times
    if file_a.modified_time > file_b.modified_time:
        winner = file_a
        loser = file_b
    else:
        winner = file_b
        loser = file_a

    # Save loser as conflict copy
    conflict_name = generate_conflict_name(loser.name, loser.device)
    # e.g., "report (conflicted copy from Device-A 2025-11-12).pdf"

    save_conflict_copy(loser, conflict_name)
    return winner
```

### Delta Sync Optimization

**Problem:** Large files take long to sync

**Solution:** Binary diff algorithm (rsync-style)

```python
def sync_file_delta(old_version, new_version):
    # 1. Calculate block checksums for old version
    old_checksums = calculate_rolling_checksums(old_version)

    # 2. Client sends checksums to server
    # 3. Server identifies matching blocks
    matching_blocks = []
    new_blocks = []

    for block in new_version.blocks:
        if block.checksum in old_checksums:
            matching_blocks.append(block.checksum)
        else:
            new_blocks.append(block)

    # 4. Client downloads only new blocks
    # 5. Reconstruct file using old blocks + new blocks
```

## 8. Scalability & Performance

### Horizontal Scaling

**API Servers:**
- Stateless design
- Add more instances behind load balancer
- Auto-scaling based on CPU/memory

**Block Servers:**
- Partition by hash range
- Consistent hashing for distribution
- Each server handles subset of chunk hashes

**Database Scaling:**
- **Read Replicas**: Route read queries to replicas
- **Sharding**: Partition by user_id
  - Shard 1: users 0-99M
  - Shard 2: users 100-199M
  - etc.
- **Caching**: Redis for hot metadata queries

### Caching Strategy

**L1 Cache (Client):**
- Local metadata cache
- Recently accessed files
- Chunk checksums

**L2 Cache (Server - Redis):**
```
Key: user:{user_id}:files
Value: JSON list of file metadata
TTL: 5 minutes

Key: chunk:{chunk_hash}:location
Value: S3 path
TTL: 1 hour

Key: user:{user_id}:quota
Value: {used: 1.5GB, total: 2GB}
TTL: 10 minutes
```

### Performance Optimizations

1. **Chunk Deduplication:**
   - Average deduplication ratio: 30-40%
   - Saves storage and bandwidth

2. **Compression:**
   - Compress chunks before storage
   - gzip for text, skip for already compressed (images, videos)

3. **Batch Operations:**
   - Batch chunk uploads
   - Batch metadata updates

4. **Connection Pooling:**
   - Reuse HTTP connections
   - Database connection pools

5. **Async Processing:**
   - Message queue for non-critical tasks
   - Thumbnail generation
   - Virus scanning
   - Usage analytics

### CDN Integration

**Use Case:** Speed up downloads for global users

**Implementation:**
```
Client Request
    ↓
CDN Edge Location (nearest)
    ↓ (cache miss)
Origin (S3)
```

**Cache Strategy:**
- Cache frequently accessed files at edge
- Cache chunks with high ref_count
- Use CloudFront or Akamai

## 9. Advanced Features

### Version History

**Storage:**
- Keep last N versions (e.g., 30 days or 10 versions)
- Store only deltas for versions (not full copies)

**API:**
```http
GET /api/v1/files/versions?path=/Documents/report.pdf

Response:
{
  "versions": [
    {
      "version_id": "v3",
      "modified_time": "2025-11-12T10:30:00Z",
      "size": 2048576,
      "modified_by": "device_123"
    },
    {
      "version_id": "v2",
      "modified_time": "2025-11-10T15:20:00Z",
      "size": 2040000
    }
  ]
}

POST /api/v1/files/restore
Body: {"path": "/Documents/report.pdf", "version_id": "v2"}
```

### File Sharing

**Public Link Sharing:**
```python
# Generate shareable link
share_token = generate_secure_token()
share_url = f"https://dropbox.com/s/{share_token}"

# Store in database
db.create_share(
    file_id=file.id,
    token=share_token,
    permission='read',
    expires_at='2025-12-12'
)

# Access link
GET /s/{share_token}
→ Download file (no auth required if link valid)
```

**User-to-User Sharing:**
- Send invitation email
- Recipient sees shared folder in their account
- Permissions: read-only or read-write

### Offline Mode

**Strategy:**
- Client maintains local copy of files
- Queue operations while offline
- Sync when connection restored

**Implementation:**
```python
class OfflineManager:
    def __init__(self):
        self.pending_operations = []

    def on_offline(self):
        # Save operations to local queue
        self.pending_operations.append(operation)
        save_to_disk(self.pending_operations)

    def on_online(self):
        # Sync pending operations
        for op in self.pending_operations:
            try:
                api.execute(op)
            except ConflictError:
                resolve_conflict(op)

        # Clear queue
        self.pending_operations = []
```

## 10. Trade-offs

### Consistency vs. Availability

**Strong Consistency:**
- ✅ No conflicts, always latest version
- ❌ Higher latency
- ❌ Requires coordination between servers

**Eventual Consistency:**
- ✅ Lower latency, better availability
- ✅ Works well offline
- ❌ Potential conflicts
- ❌ Need conflict resolution

**Decision:** Eventual consistency with conflict resolution (Dropbox approach)

### Chunking: Fixed vs. Variable Size

**Fixed Size (4 MB):**
- ✅ Simple implementation
- ✅ Predictable performance
- ❌ Less efficient deduplication

**Variable Size (CDC):**
- ✅ Better deduplication (50% vs 30%)
- ✅ Handles file edits better
- ❌ More complex
- ❌ Slightly higher CPU usage

**Decision:** Fixed size for simplicity, consider CDC for large-scale deployment

### Metadata: SQL vs. NoSQL

**MySQL:**
- ✅ ACID transactions
- ✅ Complex queries
- ✅ Strong consistency
- ❌ Harder to scale horizontally

**Cassandra:**
- ✅ Massive scalability
- ✅ High write throughput
- ❌ Eventually consistent
- ❌ Limited query flexibility

**Decision:** Hybrid approach
- MySQL: User accounts, permissions, shares
- Cassandra: File metadata, version history

## 11. Security

### Encryption

**In Transit:**
- TLS 1.3 for all communications
- Certificate pinning in mobile apps

**At Rest:**
- S3 server-side encryption (SSE-S3)
- Optional client-side encryption (E2EE)

**Client-Side Encryption (Advanced):**
```python
# Encrypt before upload
def upload_encrypted(file_path, user_key):
    # 1. Generate random file key
    file_key = generate_random_key(256)

    # 2. Encrypt file with file key
    encrypted_data = AES.encrypt(file_data, file_key)

    # 3. Encrypt file key with user's master key
    encrypted_file_key = RSA.encrypt(file_key, user_key)

    # 4. Upload encrypted data
    upload(encrypted_data)

    # 5. Store encrypted file key in metadata
    db.store_metadata(file_id, encrypted_file_key)
```

### Authentication & Authorization

- OAuth 2.0 for third-party apps
- JWT tokens for API authentication
- Device authentication with device-specific keys
- Rate limiting: 1000 requests/hour per user

## 12. Follow-up Questions

1. **How do you handle very large files (> 10 GB)?**
   - Use larger chunk size (16 MB)
   - Implement parallel chunk uploads
   - Show progress bar with resume capability
   - Consider streaming protocols for video files

2. **How would you implement selective sync (choose which folders to sync)?**
   - Client maintains "sync rules" configuration
   - API: `POST /api/v1/sync/rules` with folder paths to include/exclude
   - Client watcher ignores excluded paths
   - Server sends updates only for included paths

3. **What happens if two users edit a shared file simultaneously?**
   - Both create new versions with different version_ids
   - Server detects conflict (same parent version, different content)
   - Creates conflict copies for both users
   - Notifies users to manually merge

4. **How do you prevent abuse (e.g., uploading 1 million tiny files)?**
   - Rate limiting: Max 1000 files per hour
   - File count quota: Max 100k files per user
   - API throttling: Exponential backoff for excessive requests
   - Monitor and flag suspicious patterns

5. **How would you implement folder sharing with different permissions?**
   - Inherit permissions from parent folder
   - Allow per-user permission overrides
   - Check: `SELECT permission FROM file_shares WHERE file_id IN (ancestors) AND user_id = ?`
   - Cache permission checks in Redis

6. **How do you handle file deletions? Soft delete or hard delete?**
   - Soft delete: Mark `deleted=true`, keep for 30 days
   - Move to trash folder visible in UI
   - Hard delete after 30 days (background job)
   - Decrement chunk ref_count, delete chunks with ref_count=0

7. **How would you migrate a user's data to a different data center?**
   - Background job: Copy chunks to new region
   - Update metadata with new storage paths
   - Atomic switch: Update user's home_region
   - Client automatically connects to new region

8. **How do you ensure data durability (no data loss)?**
   - S3 replication across 3+ availability zones
   - Database master-slave replication
   - Daily automated backups
   - Checksum verification on upload/download

9. **How would you implement team/business accounts with shared spaces?**
   - Add `teams` table with team_id
   - Add `team_folders` with shared storage quota
   - Permissions at team level, inherited by members
   - Admin can view all team files

10. **How do you handle mobile sync differently from desktop?**
    - **Desktop**: Sync all files automatically
    - **Mobile**:
      - Selective sync (favorites only)
      - WiFi-only uploads
      - Thumbnail previews instead of full files
      - Lazy loading: Download file when opened

## Complexity Analysis

- **Time Complexity:**
  - Upload: O(n/c) where n = file size, c = chunk size
  - Download: O(n/c)
  - Sync check: O(m) where m = number of modified files
  - Conflict resolution: O(1) per file

- **Space Complexity:**
  - Total: O(u × f × s) where u = users, f = files/user, s = avg file size
  - With deduplication: ~0.6 × original (40% savings)
  - Metadata: O(u × f) × metadata_size

## References

- [How We've Scaled Dropbox (Dropbox Tech Blog)](https://dropbox.tech/)
- [Dropbox System Design (High Scalability)](http://highscalability.com/blog/2011/2/2/dropbox-architecture.html)
- [Content-Defined Chunking](https://en.wikipedia.org/wiki/Rolling_hash)
- [rsync Algorithm](https://rsync.samba.org/tech_report/)
- [Conflict-Free Replicated Data Types (CRDTs)](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)
