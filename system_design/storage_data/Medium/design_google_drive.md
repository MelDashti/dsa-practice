# Design Google Drive (File Sharing, Collaboration, Permissions)

**Difficulty:** Medium

## 1. Problem Statement

Design a cloud storage and collaboration platform like Google Drive that allows users to store files, share them with granular permissions, collaborate in real-time on documents, and organize files with folders. The system should support various file types, provide search functionality, and integrate with collaborative editing tools.

**Key Features:**
- File storage and organization
- Advanced sharing with granular permissions
- Real-time collaboration on documents
- File search and filtering
- Folder hierarchy and management
- Integration with productivity tools (Docs, Sheets, Slides)

## 2. Requirements

### Functional Requirements
1. **File Management**: Upload, download, delete, move, copy files
2. **Folder Organization**: Create nested folder hierarchies
3. **Sharing & Permissions**:
   - Share with specific users or groups
   - Permissions: view, comment, edit
   - Share via link with access controls
4. **Search**: Full-text search across file names and content
5. **Version History**: Track changes, restore previous versions
6. **Collaboration**: Multiple users editing same document
7. **Comments**: Add comments to files/documents
8. **Activity Tracking**: View who accessed/modified files
9. **Storage Quota**: Per-user storage limits

### Non-Functional Requirements
1. **Availability**: 99.99% uptime
2. **Consistency**: Strong consistency for permissions, eventual for content
3. **Scalability**: 1 billion users, 10 billion files
4. **Performance**:
   - Search results < 500ms
   - File upload/download < 2 seconds per 10MB
   - Real-time collaboration latency < 200ms
5. **Security**: End-to-end encryption, access auditing
6. **Reliability**: 99.999999999% durability

### Out of Scope
- Video conferencing integration
- Advanced AI features (Smart Compose, etc.)
- Third-party app ecosystem

## 3. Storage Estimation

### Assumptions
- **Total Users**: 1 billion
- **Active Users**: 200 million daily active users
- **Files per User**: 500 files average
- **Average File Size**: 2 MB
- **Storage per User**: 15 GB average (Google Drive free tier)
- **Shared Files**: 30% of files are shared
- **Collaborative Documents**: 10% of total files

### Calculations

**Total Storage:**
```
1B users × 15 GB = 15 billion GB = 15 Exabytes (EB)
With replication (3x): 45 EB
```

**Total Files:**
```
1B users × 500 files = 500 billion files
```

**Shared Files:**
```
500B files × 30% = 150 billion shared files
```

**Daily Operations:**
```
Uploads: 200M DAU × 5 uploads/day = 1B uploads/day = 11,574 uploads/sec
Downloads: 200M DAU × 20 downloads/day = 4B downloads/day = 46,296 downloads/sec
Shares: 200M DAU × 2 shares/day = 400M shares/day = 4,629 shares/sec
```

**Bandwidth:**
```
Upload: 11,574 uploads/sec × 2 MB = 23 GB/sec average
Download: 46,296 downloads/sec × 2 MB = 92 GB/sec average
Peak (10x): 230 GB/sec upload, 920 GB/sec download
```

**Metadata Storage:**
```
Per file: 2 KB (path, permissions, versions, comments)
500B files × 2 KB = 1 Petabyte (PB) metadata
```

**Database QPS:**
```
Read: 46,296 downloads × 5 queries = 231,480 QPS
Write: 11,574 uploads × 3 queries = 34,722 QPS
Permission checks: 50,000 QPS
Total: ~300,000 QPS
```

## 4. High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     Client Layer                           │
│   ┌──────────┐  ┌──────────┐  ┌────────────────────┐    │
│   │Web Client│  │Mobile App│  │Desktop Sync Client │    │
│   └──────────┘  └──────────┘  └────────────────────┘    │
└────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS / WebSocket
                           ▼
                  ┌───────────────────┐
                  │  Global CDN       │
                  │  (CloudFront)     │
                  └─────────┬─────────┘
                           │
                  ┌────────┴────────┐
                  │ Load Balancer   │
                  │ (Geo-aware)     │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│API Gateway   │  │ Collaboration│  │   Search     │
│              │  │   Service    │  │   Service    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       │     ┌───────────┴──────────────────┘
       │     │
       ▼     ▼
┌──────────────────────────────────────────┐
│          Application Services            │
│  ┌────────────┐  ┌─────────────────┐   │
│  │File Service│  │Permission Service│   │
│  └────────────┘  └─────────────────┘   │
│  ┌────────────┐  ┌─────────────────┐   │
│  │Share Service  │Activity Service │   │
│  └────────────┘  └─────────────────┘   │
└───────────┬──────────────────────────────┘
            │
    ┌───────┴────────┬──────────────┐
    │                │              │
    ▼                ▼              ▼
┌──────────┐  ┌──────────────┐  ┌────────────┐
│ Metadata │  │    Cache     │  │Message Queue│
│   DB     │  │   (Redis)    │  │  (Kafka)   │
│(Spanner) │  └──────────────┘  └────────────┘
└────┬─────┘
     │
     ▼
┌────────────────────────────────────────┐
│      Storage Layer                     │
│  ┌────────────┐  ┌──────────────────┐ │
│  │   Blob     │  │  Search Index    │ │
│  │  Storage   │  │(Elasticsearch)   │ │
│  │ (Colossus) │  └──────────────────┘ │
│  └────────────┘                        │
└────────────────────────────────────────┘
```

### Key Components

1. **Client Applications**: Web, mobile, desktop sync clients
2. **Global CDN**: Edge caching for static content and file downloads
3. **API Gateway**: Request routing, authentication, rate limiting
4. **Collaboration Service**: Real-time document editing (WebSocket)
5. **Search Service**: Full-text search using Elasticsearch
6. **File Service**: File operations (CRUD)
7. **Permission Service**: Access control and authorization
8. **Share Service**: Sharing management
9. **Activity Service**: Audit logs and activity tracking
10. **Metadata DB**: Google Spanner (distributed SQL)
11. **Cache**: Redis for hot data
12. **Message Queue**: Async task processing
13. **Blob Storage**: Google Cloud Storage (Colossus)
14. **Search Index**: Elasticsearch for file search

## 5. API Design

### File Operations

#### Upload File
```http
POST /api/v1/files
Authorization: Bearer {token}
Content-Type: multipart/form-data

Request:
{
  "file": binary,
  "name": "presentation.pptx",
  "parent_folder_id": "folder_123",
  "metadata": {
    "description": "Q4 Results"
  }
}

Response (201 Created):
{
  "file_id": "file_abc123",
  "name": "presentation.pptx",
  "size": 5242880,
  "mime_type": "application/vnd.ms-powerpoint",
  "created_time": "2025-11-12T10:30:00Z",
  "modified_time": "2025-11-12T10:30:00Z",
  "owner": {
    "user_id": "user_123",
    "email": "user@example.com"
  },
  "parent_folder_id": "folder_123",
  "web_view_link": "https://drive.google.com/file/d/file_abc123/view",
  "download_link": "https://drive.google.com/uc?id=file_abc123"
}
```

#### Get File Metadata
```http
GET /api/v1/files/{file_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "file_id": "file_abc123",
  "name": "presentation.pptx",
  "size": 5242880,
  "mime_type": "application/vnd.ms-powerpoint",
  "created_time": "2025-11-12T10:30:00Z",
  "modified_time": "2025-11-12T10:30:00Z",
  "owner": {...},
  "permissions": [
    {"user_id": "user_456", "role": "reader"},
    {"user_id": "user_789", "role": "editor"}
  ],
  "shared": true,
  "version": "v5",
  "parent_folder_id": "folder_123"
}
```

#### List Files
```http
GET /api/v1/files?folder_id=folder_123&page_size=50&page_token=xyz
Authorization: Bearer {token}

Response (200 OK):
{
  "files": [
    {
      "file_id": "file_abc",
      "name": "report.pdf",
      "size": 1048576,
      "mime_type": "application/pdf",
      "modified_time": "2025-11-12T10:30:00Z",
      "thumbnail_link": "https://cdn.example.com/thumb/abc.jpg"
    }
  ],
  "next_page_token": "abc123",
  "total_count": 237
}
```

#### Move/Copy File
```http
POST /api/v1/files/{file_id}/move
Authorization: Bearer {token}

Request:
{
  "target_folder_id": "folder_456"
}

Response (200 OK):
{
  "file_id": "file_abc123",
  "parent_folder_id": "folder_456"
}
```

### Sharing & Permissions

#### Share File
```http
POST /api/v1/files/{file_id}/permissions
Authorization: Bearer {token}

Request:
{
  "type": "user", // or "group", "domain", "anyone"
  "role": "reader", // "reader", "commenter", "writer", "owner"
  "email": "collaborator@example.com",
  "send_notification": true,
  "message": "Please review this document"
}

Response (200 OK):
{
  "permission_id": "perm_123",
  "type": "user",
  "role": "reader",
  "email": "collaborator@example.com",
  "granted_time": "2025-11-12T10:30:00Z"
}
```

#### Update Permission
```http
PATCH /api/v1/files/{file_id}/permissions/{permission_id}
Authorization: Bearer {token}

Request:
{
  "role": "writer"
}

Response (200 OK):
{
  "permission_id": "perm_123",
  "role": "writer"
}
```

#### Remove Permission
```http
DELETE /api/v1/files/{file_id}/permissions/{permission_id}
Authorization: Bearer {token}

Response (204 No Content)
```

#### Create Shareable Link
```http
POST /api/v1/files/{file_id}/share_link
Authorization: Bearer {token}

Request:
{
  "role": "reader",
  "allow_download": true,
  "expires_at": "2025-12-12T00:00:00Z"
}

Response (200 OK):
{
  "share_link": "https://drive.google.com/file/d/abc123/view?usp=sharing",
  "link_id": "link_789",
  "role": "reader",
  "expires_at": "2025-12-12T00:00:00Z"
}
```

### Search

#### Search Files
```http
GET /api/v1/files/search?q=quarterly+report&type=pdf&modified_after=2025-01-01
Authorization: Bearer {token}

Response (200 OK):
{
  "results": [
    {
      "file_id": "file_abc",
      "name": "Q3_Quarterly_Report.pdf",
      "snippet": "...quarterly revenue increased by 15%...",
      "modified_time": "2025-10-15T10:00:00Z",
      "relevance_score": 0.95
    }
  ],
  "total_results": 42,
  "search_time_ms": 187
}
```

### Version History

#### List Versions
```http
GET /api/v1/files/{file_id}/versions
Authorization: Bearer {token}

Response (200 OK):
{
  "versions": [
    {
      "version_id": "v5",
      "modified_time": "2025-11-12T10:30:00Z",
      "modified_by": "user_123",
      "size": 5242880,
      "is_current": true
    },
    {
      "version_id": "v4",
      "modified_time": "2025-11-11T15:20:00Z",
      "modified_by": "user_456",
      "size": 5240000
    }
  ]
}
```

#### Restore Version
```http
POST /api/v1/files/{file_id}/versions/{version_id}/restore
Authorization: Bearer {token}

Response (200 OK):
{
  "file_id": "file_abc123",
  "current_version": "v6", // new version created from v4
  "restored_from": "v4"
}
```

### Comments

#### Add Comment
```http
POST /api/v1/files/{file_id}/comments
Authorization: Bearer {token}

Request:
{
  "content": "Please update the Q3 numbers",
  "anchor": {
    "page": 5,
    "position": {"x": 100, "y": 200}
  },
  "mentions": ["user_456"]
}

Response (201 Created):
{
  "comment_id": "comment_123",
  "content": "Please update the Q3 numbers",
  "author": {
    "user_id": "user_123",
    "name": "John Doe"
  },
  "created_time": "2025-11-12T10:30:00Z",
  "anchor": {...}
}
```

### Activity

#### Get File Activity
```http
GET /api/v1/files/{file_id}/activity
Authorization: Bearer {token}

Response (200 OK):
{
  "activities": [
    {
      "activity_id": "act_123",
      "type": "edit",
      "user": {"user_id": "user_456", "name": "Jane Smith"},
      "timestamp": "2025-11-12T10:30:00Z",
      "details": "Modified 3 pages"
    },
    {
      "activity_id": "act_124",
      "type": "share",
      "user": {"user_id": "user_123", "name": "John Doe"},
      "timestamp": "2025-11-12T09:00:00Z",
      "details": "Shared with user_456"
    }
  ]
}
```

## 6. Storage Strategy

### Blob Storage (Google Cloud Storage / Colossus)

**File Organization:**
```
gs://gdrive-storage/
├── files/
│   ├── user_123/
│   │   ├── file_abc123/
│   │   │   ├── v1 (original)
│   │   │   ├── v2 (delta from v1)
│   │   │   └── v3 (delta from v2)
│   │   └── file_def456/...
│   └── user_456/...
├── thumbnails/
│   └── file_abc123_thumb.jpg
└── temp/ (for chunked uploads in progress)
```

**Optimization Strategies:**

1. **Chunking**: Split large files into 4 MB chunks
2. **Deduplication**: Store identical chunks once
3. **Compression**: gzip for text files
4. **Delta Storage**: Store version differences, not full copies

### Metadata Storage (Google Spanner)

**Why Spanner?**
- Globally distributed with strong consistency
- SQL interface for complex queries
- Automatic sharding and replication
- 99.999% availability SLA

**Schema Design:**

```sql
-- Users table
CREATE TABLE users (
    user_id STRING(36) NOT NULL,
    email STRING(255) NOT NULL,
    name STRING(255),
    storage_used INT64 DEFAULT 0,
    storage_quota INT64 DEFAULT 16106127360, -- 15 GB
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id)
);

-- Files metadata table
CREATE TABLE files (
    file_id STRING(36) NOT NULL,
    owner_id STRING(36) NOT NULL,
    name STRING(1024) NOT NULL,
    mime_type STRING(255),
    size INT64 NOT NULL,
    is_folder BOOL DEFAULT FALSE,
    parent_folder_id STRING(36),
    storage_path STRING(2048),
    checksum STRING(64),
    created_at TIMESTAMP NOT NULL,
    modified_at TIMESTAMP NOT NULL,
    version STRING(36),
    deleted BOOL DEFAULT FALSE,
    deleted_at TIMESTAMP,

    PRIMARY KEY (file_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_folder_id) REFERENCES files(file_id)
) INTERLEAVE IN PARENT users ON DELETE CASCADE;

CREATE INDEX idx_parent_folder ON files(parent_folder_id, deleted, name);
CREATE INDEX idx_owner_modified ON files(owner_id, modified_at DESC);

-- Permissions table
CREATE TABLE permissions (
    permission_id STRING(36) NOT NULL,
    file_id STRING(36) NOT NULL,
    grantee_type STRING(20) NOT NULL, -- 'user', 'group', 'domain', 'anyone'
    grantee_id STRING(36), -- NULL for 'anyone'
    role STRING(20) NOT NULL, -- 'reader', 'commenter', 'writer', 'owner'
    granted_by STRING(36) NOT NULL,
    granted_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,

    PRIMARY KEY (permission_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);

CREATE INDEX idx_file_permissions ON permissions(file_id, grantee_type, grantee_id);
CREATE INDEX idx_grantee_permissions ON permissions(grantee_id, file_id);

-- Share links table
CREATE TABLE share_links (
    link_id STRING(36) NOT NULL,
    file_id STRING(36) NOT NULL,
    token STRING(64) NOT NULL UNIQUE,
    role STRING(20) NOT NULL,
    allow_download BOOL DEFAULT TRUE,
    password_hash STRING(255),
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,
    access_count INT64 DEFAULT 0,

    PRIMARY KEY (link_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_token ON share_links(token);

-- File versions table
CREATE TABLE file_versions (
    version_id STRING(36) NOT NULL,
    file_id STRING(36) NOT NULL,
    version_number INT64 NOT NULL,
    size INT64 NOT NULL,
    storage_path STRING(2048),
    checksum STRING(64),
    modified_by STRING(36) NOT NULL,
    modified_at TIMESTAMP NOT NULL,
    is_current BOOL DEFAULT FALSE,

    PRIMARY KEY (file_id, version_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);

CREATE INDEX idx_file_current_version ON file_versions(file_id, is_current);

-- Comments table
CREATE TABLE comments (
    comment_id STRING(36) NOT NULL,
    file_id STRING(36) NOT NULL,
    author_id STRING(36) NOT NULL,
    content STRING(MAX) NOT NULL,
    anchor JSON, -- Position in document
    created_at TIMESTAMP NOT NULL,
    modified_at TIMESTAMP,
    deleted BOOL DEFAULT FALSE,
    parent_comment_id STRING(36), -- For replies

    PRIMARY KEY (comment_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);

CREATE INDEX idx_file_comments ON comments(file_id, created_at DESC);

-- Activity log table
CREATE TABLE activity_log (
    activity_id STRING(36) NOT NULL,
    file_id STRING(36) NOT NULL,
    user_id STRING(36) NOT NULL,
    activity_type STRING(50) NOT NULL, -- 'create', 'edit', 'share', 'download', 'delete'
    timestamp TIMESTAMP NOT NULL,
    details JSON,
    ip_address STRING(45),

    PRIMARY KEY (activity_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);

CREATE INDEX idx_file_activity ON activity_log(file_id, timestamp DESC);
CREATE INDEX idx_user_activity ON activity_log(user_id, timestamp DESC);

-- Groups table (for organizational accounts)
CREATE TABLE groups (
    group_id STRING(36) NOT NULL,
    name STRING(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,

    PRIMARY KEY (group_id)
);

-- Group memberships
CREATE TABLE group_members (
    group_id STRING(36) NOT NULL,
    user_id STRING(36) NOT NULL,
    role STRING(20) DEFAULT 'member', -- 'member', 'admin'
    added_at TIMESTAMP NOT NULL,

    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

### Permission Model

**Permission Hierarchy:**
```
Owner > Writer > Commenter > Reader

Owner: Full control (delete, manage permissions)
Writer: Edit, comment, view, download
Commenter: Comment, view, download
Reader: View, download only
```

**Permission Inheritance:**
- Folders can have permissions
- Files inherit from parent folder
- Explicit file permissions override inherited permissions

**Permission Check Algorithm:**
```python
def check_permission(user_id, file_id, required_role):
    # 1. Check if user is owner
    file = db.get_file(file_id)
    if file.owner_id == user_id:
        return True

    # 2. Check direct file permissions
    perm = db.get_permission(file_id, user_id)
    if perm and perm.role >= required_role:
        return True

    # 3. Check inherited permissions from ancestor folders
    ancestors = get_ancestor_folders(file_id)
    for folder in ancestors:
        perm = db.get_permission(folder.id, user_id)
        if perm and perm.role >= required_role:
            return True

    # 4. Check group permissions
    user_groups = db.get_user_groups(user_id)
    for group in user_groups:
        perm = db.get_permission(file_id, group.id, type='group')
        if perm and perm.role >= required_role:
            return True

    return False
```

**Caching Permission Checks:**
```python
# Redis cache for hot permissions
cache_key = f"perm:{user_id}:{file_id}:{role}"
cached = redis.get(cache_key)
if cached:
    return cached == "true"

# Compute and cache
has_permission = check_permission(user_id, file_id, role)
redis.setex(cache_key, 300, "true" if has_permission else "false")  # 5 min TTL
return has_permission
```

## 7. Search Implementation

### Elasticsearch Index

**Index Structure:**
```json
{
  "mappings": {
    "properties": {
      "file_id": {"type": "keyword"},
      "owner_id": {"type": "keyword"},
      "name": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {"type": "keyword"}
        }
      },
      "content": {
        "type": "text",
        "analyzer": "standard"
      },
      "mime_type": {"type": "keyword"},
      "size": {"type": "long"},
      "created_at": {"type": "date"},
      "modified_at": {"type": "date"},
      "tags": {"type": "keyword"},
      "permissions": {
        "type": "nested",
        "properties": {
          "user_id": {"type": "keyword"},
          "role": {"type": "keyword"}
        }
      }
    }
  }
}
```

**Content Extraction:**
- PDF: Apache Tika
- Word/Excel/PowerPoint: Apache POI
- Images: OCR (Google Cloud Vision API)
- Videos: Speech-to-text transcription

**Indexing Pipeline:**
```
File Upload
    ↓
Store in Blob Storage
    ↓
Publish to Kafka topic: "file_created"
    ↓
Indexing Worker consumes event
    ↓
Extract text content
    ↓
Index in Elasticsearch
```

**Search Query Example:**
```python
def search_files(user_id, query, filters):
    # Build Elasticsearch query
    es_query = {
        "bool": {
            "must": [
                {"multi_match": {
                    "query": query,
                    "fields": ["name^3", "content"],  # Boost name matches
                    "fuzziness": "AUTO"
                }}
            ],
            "filter": []
        }
    }

    # Add filters
    if filters.get('mime_type'):
        es_query["bool"]["filter"].append(
            {"term": {"mime_type": filters['mime_type']}}
        )

    if filters.get('modified_after'):
        es_query["bool"]["filter"].append(
            {"range": {"modified_at": {"gte": filters['modified_after']}}}
        )

    # Security: Only return files user has access to
    es_query["bool"]["filter"].append({
        "bool": {
            "should": [
                {"term": {"owner_id": user_id}},
                {"nested": {
                    "path": "permissions",
                    "query": {"term": {"permissions.user_id": user_id}}
                }}
            ]
        }
    })

    # Execute search
    results = es.search(index="files", body={"query": es_query})
    return results
```

## 8. Real-Time Collaboration

### Collaborative Editing Architecture

**Operational Transformation (OT) / CRDT:**

Google Docs uses Operational Transformation:
- Each edit operation transformed relative to concurrent operations
- Ensures consistency across all clients

**Collaboration Flow:**
```
User A types "Hello"
    ↓
Client sends operation: Insert("Hello", position=0)
    ↓
WebSocket → Collaboration Service
    ↓
Apply operation to server document state
    ↓
Broadcast to all other clients (User B, C, D)
    ↓
Clients apply transformed operation
```

**WebSocket Implementation:**
```python
class CollaborationService:
    def __init__(self):
        self.active_sessions = {}  # document_id → list of WebSocket connections
        self.document_states = {}  # document_id → current state

    async def on_connect(self, websocket, document_id, user_id):
        # Add connection to session
        if document_id not in self.active_sessions:
            self.active_sessions[document_id] = []
        self.active_sessions[document_id].append({
            'websocket': websocket,
            'user_id': user_id
        })

        # Send current document state to new client
        current_state = self.document_states.get(document_id)
        await websocket.send(json.dumps({
            'type': 'initial_state',
            'state': current_state
        }))

        # Notify other users
        await self.broadcast(document_id, {
            'type': 'user_joined',
            'user_id': user_id
        }, exclude=websocket)

    async def on_operation(self, document_id, operation, from_websocket):
        # Apply operation to server state
        self.apply_operation(document_id, operation)

        # Broadcast to all other clients
        await self.broadcast(document_id, {
            'type': 'operation',
            'operation': operation
        }, exclude=from_websocket)

        # Async: persist to database
        kafka.publish('document_operations', {
            'document_id': document_id,
            'operation': operation
        })

    async def broadcast(self, document_id, message, exclude=None):
        sessions = self.active_sessions.get(document_id, [])
        for session in sessions:
            if session['websocket'] != exclude:
                await session['websocket'].send(json.dumps(message))
```

**Presence & Cursors:**
```python
# Track active users and cursor positions
presence = {
    'document_id': 'doc_123',
    'users': [
        {
            'user_id': 'user_456',
            'name': 'Jane',
            'cursor_position': {'line': 5, 'column': 10},
            'color': '#FF5733'
        }
    ]
}

# Broadcast cursor movements
await broadcast(document_id, {
    'type': 'cursor_update',
    'user_id': user_id,
    'position': new_position
})
```

## 9. Scalability & Performance

### Horizontal Scaling

**API Servers:**
- Stateless design
- Auto-scaling based on CPU/traffic
- Target: 1000 RPS per server instance

**Collaboration Service:**
- Sticky sessions for WebSocket connections
- Scale by document sharding (hash(document_id) % num_servers)
- Each server handles subset of documents

**Database Scaling:**
- Spanner automatically shards by primary key
- Read replicas in multiple regions
- Cache layer (Redis) for hot data

### Caching Strategy

**Multi-Level Cache:**

```
L1: Client-side cache (browser localStorage)
    ↓ (miss)
L2: CDN edge cache (CloudFront)
    ↓ (miss)
L3: Application cache (Redis)
    ↓ (miss)
L4: Database (Spanner)
```

**Redis Cache Keys:**
```
file:metadata:{file_id} → File metadata (TTL: 5 min)
file:permissions:{file_id}:{user_id} → Permission check result (TTL: 5 min)
user:quota:{user_id} → Storage usage (TTL: 1 min)
folder:children:{folder_id} → List of files in folder (TTL: 2 min)
share_link:{token} → Share link details (TTL: 1 hour)
```

**Cache Invalidation:**
```python
def update_file(file_id, updates):
    # 1. Update database
    db.update_file(file_id, updates)

    # 2. Invalidate caches
    redis.delete(f"file:metadata:{file_id}")

    # Invalidate parent folder cache
    file = db.get_file(file_id)
    if file.parent_folder_id:
        redis.delete(f"folder:children:{file.parent_folder_id}")

    # Invalidate permission caches for all users with access
    permissions = db.get_file_permissions(file_id)
    for perm in permissions:
        redis.delete(f"file:permissions:{file_id}:{perm.user_id}")
```

### Performance Optimizations

1. **Lazy Loading**: Load file list incrementally (pagination)
2. **Thumbnail Generation**: Async background job
3. **Prefetching**: Predict next folder user will open
4. **Connection Pooling**: Reuse DB connections
5. **Batch Operations**: Batch permission checks
6. **CDN**: Serve static assets and files from edge locations

## 10. Advanced Features

### Smart Suggestions

**Suggested Files:**
- Machine learning model predicts files user needs
- Based on: access patterns, time of day, project context
- Example: "You might need Q3_Report.pdf (opened every Monday at 9 AM)"

**Implementation:**
```python
# Track file access patterns
def log_access(user_id, file_id, context):
    features = {
        'user_id': user_id,
        'file_id': file_id,
        'time_of_day': context.hour,
        'day_of_week': context.weekday,
        'recently_accessed': get_recent_files(user_id, limit=10)
    }

    # Store in data warehouse for ML training
    bigquery.insert('file_access_events', features)

# Prediction service
def get_suggested_files(user_id, context):
    # Call ML model API
    response = ml_service.predict({
        'user_id': user_id,
        'time_of_day': context.hour,
        'day_of_week': context.weekday
    })

    file_ids = response['predictions'][:5]  # Top 5
    return db.get_files(file_ids)
```

### Priority Sync

**Problem:** Too many files to sync on limited bandwidth

**Solution:** Prioritize important files

```python
def calculate_sync_priority(file):
    score = 0

    # Recently modified files
    age_hours = (now() - file.modified_at).hours
    score += max(100 - age_hours, 0)

    # Frequently accessed files
    access_count = get_access_count(file.id, days=7)
    score += access_count * 10

    # Starred/important files
    if file.is_starred:
        score += 50

    # Collaborative documents (multiple editors)
    if file.is_collaborative:
        score += 30

    return score

# Sync in priority order
files_to_sync = sorted(files, key=calculate_sync_priority, reverse=True)
for file in files_to_sync:
    sync(file)
```

### Offline Mode

**Progressive Web App (PWA):**
- Service worker caches recently accessed files
- IndexedDB for local metadata storage
- Queue operations while offline

```javascript
// Service Worker
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/v1/files/')) {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  }
});

// Queue offline operations
class OfflineQueue {
  enqueue(operation) {
    const queue = JSON.parse(localStorage.getItem('offline_queue') || '[]');
    queue.push({
      ...operation,
      timestamp: Date.now()
    });
    localStorage.setItem('offline_queue', JSON.stringify(queue));
  }

  async processQueue() {
    const queue = JSON.parse(localStorage.getItem('offline_queue') || '[]');
    for (const operation of queue) {
      try {
        await api.execute(operation);
        this.remove(operation);
      } catch (error) {
        console.error('Failed to process operation:', error);
      }
    }
  }
}
```

## 11. Trade-offs

### Strong Consistency vs. Availability

**Strong Consistency (Google Spanner):**
- ✅ No conflicts, always latest data
- ✅ Simpler application logic
- ❌ Higher latency (global coordination)
- ❌ Reduced availability during partitions

**Eventual Consistency:**
- ✅ Lower latency
- ✅ Higher availability
- ❌ Potential conflicts
- ❌ Complex conflict resolution

**Decision:** Strong consistency for metadata (Spanner), eventual for collaboration

### Operational Transformation vs. CRDT

**OT (Google Docs approach):**
- ✅ Smaller message size
- ✅ More mature technology
- ❌ Complex transformation logic
- ❌ Central server required

**CRDT (Conflict-Free Replicated Data Types):**
- ✅ Simpler logic
- ✅ Decentralized (P2P possible)
- ❌ Larger data structures
- ❌ Less adoption

**Decision:** OT for proven reliability at scale

### File Versioning: Full Copy vs. Delta

**Full Copy:**
- ✅ Simple implementation
- ✅ Fast retrieval
- ❌ Storage expensive (10x storage for 10 versions)

**Delta Storage:**
- ✅ Storage efficient (2-3x total)
- ✅ Reasonable for text documents
- ❌ Slower retrieval (must apply deltas)
- ❌ Complex for binary files

**Decision:** Delta for text, full copy for binary files < 10 MB

## 12. Follow-up Questions

1. **How would you handle a user uploading a 10 GB file?**
   - Multipart upload with 100 MB chunks
   - Resume capability (track uploaded chunks)
   - Progress indicator
   - Background upload (queue for processing)
   - Consider suggesting compression

2. **How do you prevent unauthorized access to shared links?**
   - Cryptographically secure random tokens (128-bit)
   - Optional password protection
   - Expiration dates
   - Track access count and IP addresses
   - Rate limiting on share link access
   - Revoke capability

3. **How would you implement "Shared with me" view efficiently?**
   - Materialized view or denormalized table
   - Index: `CREATE INDEX idx_grantee_files ON permissions(grantee_id, file_id)`
   - Cache in Redis: `shared_with:{user_id}` → list of file_ids
   - Update cache when permissions change

4. **How do you handle folder deletion with thousands of files?**
   - Soft delete: Mark folder as deleted
   - Background job: Recursively delete children
   - Show "Deletion in progress" to user
   - Keep in trash for 30 days
   - Hard delete after retention period

5. **How would you detect and prevent malware uploads?**
   - Virus scan after upload (ClamAV/VirusTotal API)
   - Quarantine suspicious files
   - Block downloads until scan complete
   - Notify file owner if malware detected
   - Machine learning for zero-day detection

6. **How do you handle concurrent edits in different versions?**
   - Version forking: Create separate branches
   - Manual merge required
   - Or: Last-write-wins, save other as "conflicted copy"
   - Notify collaborators of conflict

7. **How would you implement activity notifications?**
   - Notification service subscribed to Kafka topics
   - User preferences: Email, push, in-app
   - Aggregation: "5 new comments" vs. individual notifications
   - Digest mode: Daily summary
   - Real-time via WebSocket for active users

8. **How do you optimize storage costs?**
   - Deduplication: 30-40% savings
   - Compression: 50% for text files
   - Tiered storage: Move old versions to cold storage (Glacier)
   - Retention policies: Auto-delete old versions
   - User quotas

9. **How would you handle a datacenter outage?**
   - Multi-region deployment (US, EU, Asia)
   - Automatic failover to healthy region
   - Spanner's automatic replication
   - CDN serves cached content
   - Graceful degradation: Read-only mode if write replicas unavailable

10. **How do you implement audit logging for compliance?**
    - Log all access/modification events
    - Store in immutable log (Write-Ahead Log)
    - Separate audit database (no deletion possible)
    - Retention: 7 years for regulated industries
    - API for audit queries
    - Real-time alerts for suspicious activity

## Complexity Analysis

- **Time Complexity:**
  - File upload: O(n/c) where n = file size, c = chunk size
  - Permission check: O(d + g) where d = folder depth, g = number of groups
  - Search: O(log n) with proper indexing
  - List files: O(k) where k = number of files in folder

- **Space Complexity:**
  - Total: O(u × f × s) where u = users, f = files/user, s = avg file size
  - With deduplication: ~0.6-0.7 × original
  - Metadata: O(u × f) × 2 KB per file

## References

- [Google Drive Architecture](https://cloud.google.com/blog/products/storage-data-transfer)
- [Google Spanner Paper](https://research.google/pubs/pub39966/)
- [Operational Transformation](https://en.wikipedia.org/wiki/Operational_transformation)
- [CRDT Research](https://crdt.tech/)
- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
