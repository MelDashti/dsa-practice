# Design Slack

## 1. Problem Overview

Design a team collaboration platform like Slack that supports workspaces, channels, direct messages, threaded conversations, file sharing, and powerful search. The system must handle millions of teams with real-time messaging, rich integrations, and comprehensive search across all content.

**Key Challenges**:
- Multi-workspace and channel organization
- Threaded conversations within channels
- Full-text search across messages, files, and integrations
- File storage and sharing
- Real-time updates for all channel members
- Integration platform (bots, webhooks, apps)

## 2. Requirements

### Functional Requirements
- **Workspaces**: Organizations can create isolated workspaces
- **Channels**: Public, private, and shared channels
- **Direct Messages**: 1-on-1 and group DMs
- **Threads**: Threaded replies to messages
- **File Sharing**: Upload and share files (images, documents, videos)
- **Search**: Full-text search across messages, files, and people
- **Reactions**: Emoji reactions to messages
- **Mentions**: @user and @channel mentions
- **Notifications**: Desktop, mobile, and email notifications
- **Integrations**: Bots, webhooks, slash commands, apps
- **Message Formatting**: Rich text, code blocks, links

### Non-Functional Requirements
- **Availability**: 99.99% uptime
- **Latency**: < 200ms message delivery
- **Scalability**: 10M+ DAU, 100K+ organizations
- **Consistency**: Strong consistency within channels
- **Storage**: Unlimited message history
- **Search Performance**: < 1 second search results
- **Reliability**: No message loss

### Out of Scope
- Voice/video calls (Huddles)
- Screen sharing
- Canvas documents
- Slack Connect (cross-organization)
- Advanced analytics

## 3. Scale Estimation

### Traffic Estimates
- **Organizations**: 100,000
- **Total Users**: 50 million
- **Daily Active Users (DAU)**: 10 million (20%)
- **Average channels per user**: 10
- **Average messages per user per day**: 100
- **Total daily messages**: 1 billion
- **Messages per second**: 1B / 86400 ≈ 11,600 QPS (average)
- **Peak QPS**: 35,000 (3x average)
- **File uploads**: 5% of messages = 50M files/day

### Storage Estimates
- **Text message**: 500 bytes average (with formatting)
- **Daily message storage**: 1B × 500 bytes = 500 GB/day
- **Yearly message storage**: 180 TB/year
- **Files**: 50M/day × 1 MB (avg) = 50 TB/day
- **Yearly file storage**: 18 PB/year
- **Search indexes**: 2x message storage = 360 TB/year

### Bandwidth Estimates
- **Incoming messages**: 11,600 × 500 bytes = 5.8 MB/s
- **File uploads**: 50M / 86400 × 1 MB ≈ 580 MB/s
- **Total incoming**: ~585 MB/s
- **Outgoing**: Higher due to channel fanout (5x) = ~2.9 GB/s

### Memory Estimates
- **Active connections**: 10M concurrent users
- **Connection memory**: 10M × 64 KB = 640 GB
- **Recent message cache**: 10M users × 10 channels × 50 msgs × 500 bytes = 2.5 TB
- **Search index cache**: 100 GB

## 4. High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                         │
│        (Web, Desktop, Mobile Apps)                       │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   Load Balancer      │
         │   (WebSocket & HTTP) │
         └──────────┬───────────┘
                    │
        ┌───────────┴────────────┬────────────────┐
        ▼                        ▼                ▼
┌───────────────┐      ┌──────────────────┐  ┌──────────────┐
│   Gateway     │      │   API Gateway    │  │  CDN/Static  │
│   (WebSocket) │      │   (REST APIs)    │  │   Assets     │
└───────┬───────┘      └─────────┬────────┘  └──────────────┘
        │                        │
        └────────┬───────────────┘
                 │
    ┌────────────┴─────────────────────────────────┐
    │                                              │
    ▼                                              ▼
┌─────────────────┐                    ┌──────────────────────┐
│  Message Router │                    │   Service Layer      │
└────────┬────────┘                    └──────────┬───────────┘
         │                                        │
    ┌────┴────────┬──────────┬──────────┬────────┴────┐
    ▼             ▼          ▼          ▼             ▼
┌─────────┐  ┌─────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│Message  │  │Channel  │ │Thread  │ │  File   │ │  Search  │
│Service  │  │Service  │ │Service │ │ Service │ │  Service │
└────┬────┘  └────┬────┘ └───┬────┘ └────┬────┘ └─────┬────┘
     │            │           │           │            │
     └────────────┴───────────┴───────────┴────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │ PostgreSQL │  │    S3      │  │Elasticsearch│
       │ (Messages) │  │   (Files)  │  │  (Search)  │
       └────────────┘  └────────────┘  └────────────┘
              ▼
       ┌────────────┐
       │   Redis    │
       │  (Cache)   │
       └────────────┘
```

## 5. API Design

### WebSocket Events

#### Message Sent to Channel
```json
{
  "type": "message",
  "channel_id": "C123456",
  "user": "U789",
  "text": "Hello team!",
  "ts": "1699876543.123456",
  "thread_ts": null,  // null if not a thread reply
  "attachments": []
}
```

#### Thread Reply
```json
{
  "type": "message",
  "channel_id": "C123456",
  "user": "U789",
  "text": "Reply in thread",
  "ts": "1699876544.123456",
  "thread_ts": "1699876543.123456",  // Parent message timestamp
  "reply_count": 2
}
```

#### Reaction Added
```json
{
  "type": "reaction_added",
  "user": "U789",
  "item": {
    "type": "message",
    "channel": "C123456",
    "ts": "1699876543.123456"
  },
  "reaction": "thumbsup"
}
```

#### Typing Indicator
```json
{
  "type": "user_typing",
  "channel_id": "C123456",
  "user": "U789"
}
```

### REST APIs

#### Send Message
```
POST /api/chat.postMessage
{
  "channel": "C123456",
  "text": "Hello team!",
  "thread_ts": null,  // Optional: parent message for thread
  "attachments": [],  // Rich formatting
  "blocks": []        // Block Kit formatting
}

Response:
{
  "ok": true,
  "channel": "C123456",
  "ts": "1699876543.123456",
  "message": {
    "text": "Hello team!",
    "user": "U789",
    "ts": "1699876543.123456"
  }
}
```

#### Get Channel History
```
GET /api/conversations.history
Query Parameters:
  - channel: C123456
  - oldest: 1699800000.000000 (timestamp)
  - limit: 100
  - inclusive: true

Response:
{
  "ok": true,
  "messages": [
    {
      "type": "message",
      "user": "U789",
      "text": "Hello!",
      "ts": "1699876543.123456",
      "reactions": [
        {"name": "thumbsup", "count": 3, "users": ["U1", "U2", "U3"]}
      ]
    }
  ],
  "has_more": true
}
```

#### Get Thread Replies
```
GET /api/conversations.replies
Query Parameters:
  - channel: C123456
  - ts: 1699876543.123456  (parent message timestamp)
  - limit: 50

Response:
{
  "ok": true,
  "messages": [
    {
      "type": "message",
      "user": "U789",
      "text": "Thread reply",
      "thread_ts": "1699876543.123456",
      "ts": "1699876544.123456"
    }
  ]
}
```

#### Create Channel
```
POST /api/conversations.create
{
  "name": "project-alpha",
  "is_private": false,
  "description": "Project Alpha discussions"
}

Response:
{
  "ok": true,
  "channel": {
    "id": "C123456",
    "name": "project-alpha",
    "is_private": false,
    "created": 1699876543,
    "creator": "U789"
  }
}
```

#### Search Messages
```
GET /api/search.messages
Query Parameters:
  - query: "deployment"
  - sort: timestamp
  - sort_dir: desc
  - count: 20
  - page: 1

Response:
{
  "ok": true,
  "query": "deployment",
  "messages": {
    "total": 156,
    "matches": [
      {
        "channel": {"id": "C123", "name": "engineering"},
        "user": "U789",
        "username": "john",
        "text": "Starting <em>deployment</em> now",
        "ts": "1699876543.123456",
        "permalink": "https://slack.com/..."
      }
    ]
  }
}
```

#### Upload File
```
POST /api/files.upload
Content-Type: multipart/form-data

Fields:
  - file: <binary>
  - channels: C123456,C789012
  - title: "Architecture Diagram"
  - initial_comment: "Here's the updated diagram"

Response:
{
  "ok": true,
  "file": {
    "id": "F123456",
    "name": "architecture.png",
    "mimetype": "image/png",
    "size": 204800,
    "url_private": "https://files.slack.com/...",
    "permalink": "https://slack.com/files/..."
  }
}
```

## 6. Data Models

### Workspace Table (PostgreSQL)
```sql
CREATE TABLE workspaces (
    workspace_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subdomain VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_id UUID NOT NULL,
    plan_type VARCHAR(20), -- free, standard, plus, enterprise
    max_members INT,
    settings JSONB
);

CREATE INDEX idx_subdomain ON workspaces(subdomain);
```

### User Table (PostgreSQL)
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(workspace_id),
    email VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    real_name VARCHAR(100),
    avatar_url TEXT,
    status_text VARCHAR(100),
    status_emoji VARCHAR(50),
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT false,
    is_bot BOOLEAN DEFAULT false,

    UNIQUE(workspace_id, email)
);

CREATE INDEX idx_workspace_users ON users(workspace_id);
CREATE INDEX idx_email ON users(email);
```

### Channel Table (PostgreSQL)
```sql
CREATE TABLE channels (
    channel_id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(workspace_id),
    name VARCHAR(80) NOT NULL,
    topic TEXT,
    purpose TEXT,
    is_private BOOLEAN DEFAULT false,
    is_archived BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(workspace_id, name)
);

CREATE INDEX idx_workspace_channels ON channels(workspace_id, is_archived);
```

### Channel Membership Table (PostgreSQL)
```sql
CREATE TABLE channel_members (
    channel_id UUID REFERENCES channels(channel_id),
    user_id UUID REFERENCES users(user_id),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) DEFAULT 'member', -- admin, member
    muted BOOLEAN DEFAULT false,

    PRIMARY KEY (channel_id, user_id)
);

CREATE INDEX idx_user_channels ON channel_members(user_id);
```

### Message Table (PostgreSQL with Partitioning)
```sql
CREATE TABLE messages (
    message_id UUID PRIMARY KEY,
    channel_id UUID REFERENCES channels(channel_id),
    user_id UUID REFERENCES users(user_id),
    text TEXT,
    ts DECIMAL(20, 6) NOT NULL, -- Slack's timestamp format
    thread_ts DECIMAL(20, 6),    -- Parent message for threads
    reply_count INT DEFAULT 0,
    reply_users_count INT DEFAULT 0,
    latest_reply DECIMAL(20, 6),
    edited_at TIMESTAMP,
    deleted_at TIMESTAMP,
    attachments JSONB,
    blocks JSONB,  -- Block Kit formatting

    UNIQUE(channel_id, ts)
) PARTITION BY RANGE (ts);

-- Create partitions by month
CREATE TABLE messages_2024_01 PARTITION OF messages
    FOR VALUES FROM (1704067200.000000) TO (1706745600.000000);

CREATE INDEX idx_channel_ts ON messages(channel_id, ts DESC);
CREATE INDEX idx_thread ON messages(channel_id, thread_ts, ts);
CREATE INDEX idx_user_messages ON messages(user_id, ts DESC);
```

### Reaction Table (PostgreSQL)
```sql
CREATE TABLE reactions (
    reaction_id UUID PRIMARY KEY,
    message_id UUID REFERENCES messages(message_id),
    user_id UUID REFERENCES users(user_id),
    emoji VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(message_id, user_id, emoji)
);

CREATE INDEX idx_message_reactions ON reactions(message_id);
```

### File Table (PostgreSQL)
```sql
CREATE TABLE files (
    file_id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(workspace_id),
    user_id UUID REFERENCES users(user_id),
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    mimetype VARCHAR(100),
    size BIGINT,
    s3_key TEXT NOT NULL,
    url_private TEXT,
    thumb_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT false
);

CREATE INDEX idx_workspace_files ON files(workspace_id, created_at DESC);
CREATE INDEX idx_user_files ON files(user_id, created_at DESC);
```

### File Share Table (PostgreSQL)
```sql
CREATE TABLE file_shares (
    file_id UUID REFERENCES files(file_id),
    channel_id UUID REFERENCES channels(channel_id),
    message_id UUID REFERENCES messages(message_id),
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (file_id, channel_id)
);

CREATE INDEX idx_channel_files ON file_shares(channel_id, shared_at DESC);
```

### Redis Schemas

#### Online Users
```
Key: online:workspace:{workspace_id}
Value: Set of user_ids
TTL: None (managed manually)

Key: presence:{user_id}
Value: {
  "status": "active",  // active, away
  "last_active": 1699876543000,
  "connection_ids": ["conn_1", "conn_2"]
}
TTL: 5 minutes
```

#### Typing Indicators
```
Key: typing:{channel_id}
Value: Set of user_ids
TTL: 10 seconds per user
```

#### Unread Counts
```
Key: unread:{user_id}:{channel_id}
Value: {
  "count": 5,
  "last_read_ts": "1699876543.123456",
  "mention_count": 1
}
```

### Elasticsearch Schema
```json
{
  "mappings": {
    "properties": {
      "workspace_id": {"type": "keyword"},
      "channel_id": {"type": "keyword"},
      "channel_name": {"type": "keyword"},
      "user_id": {"type": "keyword"},
      "username": {"type": "keyword"},
      "text": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {"type": "keyword"}
        }
      },
      "ts": {"type": "double"},
      "thread_ts": {"type": "double"},
      "created_at": {"type": "date"},
      "attachments": {"type": "nested"},
      "has_files": {"type": "boolean"}
    }
  }
}
```

## 7. Core Services Design

### Gateway Service
**Responsibilities**:
- Maintain WebSocket connections
- Authenticate users
- Route real-time events
- Manage connection lifecycle

```python
class GatewayService:
    def on_connect(self, workspace_id, user_id, connection):
        # Authenticate user
        if not self.authenticate(workspace_id, user_id):
            connection.close(1008, "Unauthorized")
            return

        # Store connection
        self.connection_manager.add(user_id, connection)

        # Mark user as online
        self.presence_service.mark_online(workspace_id, user_id)

        # Send initial data
        self.send_initial_state(connection, workspace_id, user_id)

        # Join user to their channel rooms
        channels = self.channel_service.get_user_channels(user_id)
        for channel in channels:
            self.subscribe_to_channel(connection, channel.id)

    def on_message_received(self, user_id, data):
        workspace_id = self.get_workspace_id(user_id)

        # Validate permissions
        if not self.can_post_message(user_id, data["channel_id"]):
            return {"error": "forbidden"}

        # Process message
        message = self.message_service.create_message({
            "workspace_id": workspace_id,
            "channel_id": data["channel_id"],
            "user_id": user_id,
            "text": data["text"],
            "thread_ts": data.get("thread_ts")
        })

        # Broadcast to channel members
        self.broadcast_to_channel(data["channel_id"], {
            "type": "message",
            "message": message
        })

        return message

    def broadcast_to_channel(self, channel_id, event):
        # Get all members of the channel
        members = self.channel_service.get_channel_members(channel_id)

        # Send to all online members
        for member_id in members:
            connections = self.connection_manager.get_connections(member_id)
            for conn in connections:
                conn.send_json(event)
```

### Message Service
**Responsibilities**:
- Create and store messages
- Handle message updates and deletions
- Manage thread operations
- Trigger search indexing

```python
class MessageService:
    def create_message(self, message_data):
        # Generate timestamp (Slack format: seconds.microseconds)
        ts = self.generate_timestamp()

        message = {
            "message_id": uuid.uuid4(),
            "workspace_id": message_data["workspace_id"],
            "channel_id": message_data["channel_id"],
            "user_id": message_data["user_id"],
            "text": message_data["text"],
            "ts": ts,
            "thread_ts": message_data.get("thread_ts"),
            "attachments": message_data.get("attachments", []),
            "blocks": message_data.get("blocks", [])
        }

        # Store in database
        self.db.insert_message(message)

        # Update thread metadata if this is a reply
        if message["thread_ts"]:
            self.update_thread_metadata(
                message["channel_id"],
                message["thread_ts"],
                message["user_id"]
            )

        # Index for search
        self.search_service.index_message(message)

        # Check for mentions
        mentions = self.extract_mentions(message["text"])
        if mentions:
            self.notification_service.send_mention_notifications(
                message, mentions
            )

        # Update unread counts
        self.update_unread_counts(message)

        return message

    def update_thread_metadata(self, channel_id, thread_ts, reply_user_id):
        # Increment reply count
        self.db.execute("""
            UPDATE messages
            SET reply_count = reply_count + 1,
                latest_reply = %s,
                reply_users_count = (
                    SELECT COUNT(DISTINCT user_id)
                    FROM messages
                    WHERE channel_id = %s
                      AND thread_ts = %s
                )
            WHERE channel_id = %s AND ts = %s
        """, (current_timestamp(), channel_id, thread_ts,
              channel_id, thread_ts))

    def get_channel_messages(self, channel_id, oldest_ts, limit):
        messages = self.db.query("""
            SELECT m.*, u.display_name, u.avatar_url,
                   array_agg(
                       json_build_object(
                           'emoji', r.emoji,
                           'count', COUNT(*),
                           'users', array_agg(r.user_id)
                       )
                   ) as reactions
            FROM messages m
            JOIN users u ON m.user_id = u.user_id
            LEFT JOIN reactions r ON m.message_id = r.message_id
            WHERE m.channel_id = %s
              AND m.ts > %s
              AND m.deleted_at IS NULL
              AND m.thread_ts IS NULL
            GROUP BY m.message_id, u.display_name, u.avatar_url
            ORDER BY m.ts DESC
            LIMIT %s
        """, (channel_id, oldest_ts, limit))

        return messages

    def update_unread_counts(self, message):
        # Get all channel members except sender
        members = self.channel_service.get_channel_members(
            message["channel_id"]
        )
        members.remove(message["user_id"])

        # Increment unread count for each member
        for member_id in members:
            self.redis.hincrby(
                f"unread:{member_id}:{message['channel_id']}",
                "count",
                1
            )

            # Check if user is mentioned
            if self.is_mentioned(member_id, message["text"]):
                self.redis.hincrby(
                    f"unread:{member_id}:{message['channel_id']}",
                    "mention_count",
                    1
                )
```

### Channel Service
**Responsibilities**:
- Manage channel creation and settings
- Handle channel membership
- Control permissions

```python
class ChannelService:
    def create_channel(self, workspace_id, name, creator_id, is_private):
        # Validate channel name
        if not self.is_valid_channel_name(name):
            raise ValidationError("Invalid channel name")

        # Check if channel exists
        if self.channel_exists(workspace_id, name):
            raise ConflictError("Channel already exists")

        channel = {
            "channel_id": uuid.uuid4(),
            "workspace_id": workspace_id,
            "name": name,
            "is_private": is_private,
            "created_by": creator_id
        }

        # Create channel
        self.db.insert_channel(channel)

        # Add creator as admin
        self.add_member(
            channel["channel_id"],
            creator_id,
            role="admin"
        )

        return channel

    def add_member(self, channel_id, user_id, role="member"):
        # Check if user already in channel
        if self.is_member(channel_id, user_id):
            return

        # Add membership
        self.db.execute("""
            INSERT INTO channel_members (channel_id, user_id, role)
            VALUES (%s, %s, %s)
        """, (channel_id, user_id, role))

        # Notify other members
        self.broadcast_event(channel_id, {
            "type": "member_joined_channel",
            "user": user_id,
            "channel": channel_id
        })

    def get_user_channels(self, user_id):
        channels = self.db.query("""
            SELECT c.*, cm.role, cm.muted
            FROM channels c
            JOIN channel_members cm ON c.channel_id = cm.channel_id
            WHERE cm.user_id = %s
              AND c.is_archived = false
            ORDER BY cm.joined_at DESC
        """, (user_id,))

        # Add unread counts
        for channel in channels:
            unread_data = self.redis.hgetall(
                f"unread:{user_id}:{channel['channel_id']}"
            )
            channel["unread_count"] = int(unread_data.get("count", 0))
            channel["mention_count"] = int(unread_data.get("mention_count", 0))

        return channels
```

### Search Service
**Responsibilities**:
- Index messages in Elasticsearch
- Provide full-text search
- Rank and filter results

```python
class SearchService:
    def index_message(self, message):
        # Prepare document for indexing
        doc = {
            "workspace_id": message["workspace_id"],
            "channel_id": message["channel_id"],
            "channel_name": self.get_channel_name(message["channel_id"]),
            "user_id": message["user_id"],
            "username": self.get_username(message["user_id"]),
            "text": message["text"],
            "ts": message["ts"],
            "thread_ts": message.get("thread_ts"),
            "created_at": datetime.now(),
            "has_files": bool(message.get("attachments"))
        }

        # Index in Elasticsearch
        self.es_client.index(
            index=f"messages-{message['workspace_id']}",
            id=message["message_id"],
            document=doc
        )

    def search_messages(self, workspace_id, user_id, query, filters):
        # Get user's channels for permission filtering
        user_channels = self.channel_service.get_user_channel_ids(user_id)

        # Build Elasticsearch query
        must_clauses = [
            {"term": {"workspace_id": workspace_id}},
            {"terms": {"channel_id": user_channels}},  # Permission filter
            {
                "multi_match": {
                    "query": query,
                    "fields": ["text^2", "username"],  # Boost text field
                    "type": "best_fields"
                }
            }
        ]

        # Add filters
        if filters.get("channel_id"):
            must_clauses.append(
                {"term": {"channel_id": filters["channel_id"]}}
            )

        if filters.get("from_user"):
            must_clauses.append(
                {"term": {"user_id": filters["from_user"]}}
            )

        if filters.get("has_files"):
            must_clauses.append(
                {"term": {"has_files": True}}
            )

        # Execute search
        result = self.es_client.search(
            index=f"messages-{workspace_id}",
            body={
                "query": {"bool": {"must": must_clauses}},
                "sort": [{"ts": "desc"}],
                "size": filters.get("limit", 20),
                "from": filters.get("offset", 0),
                "highlight": {
                    "fields": {"text": {}},
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"]
                }
            }
        )

        return self.format_search_results(result)
```

### File Service
**Responsibilities**:
- Handle file uploads
- Generate thumbnails
- Manage file storage and CDN

```python
class FileService:
    def upload_file(self, workspace_id, user_id, file_data, metadata):
        # Validate file size and type
        if file_data.size > 1_000_000_000:  # 1GB limit
            raise ValidationError("File too large")

        # Generate file ID and S3 key
        file_id = uuid.uuid4()
        s3_key = f"{workspace_id}/{user_id}/{file_id}/{file_data.filename}"

        # Upload to S3
        self.s3_client.upload_fileobj(
            file_data.stream,
            self.bucket_name,
            s3_key,
            ExtraArgs={
                "ContentType": file_data.content_type,
                "Metadata": {
                    "workspace-id": str(workspace_id),
                    "user-id": str(user_id)
                }
            }
        )

        # Generate thumbnail for images/videos
        thumbnail_url = None
        if file_data.content_type.startswith("image/"):
            thumbnail = self.generate_image_thumbnail(file_data)
            thumbnail_key = f"{s3_key}_thumb"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=thumbnail_key,
                Body=thumbnail
            )
            thumbnail_url = self.get_signed_url(thumbnail_key)

        # Generate signed URL
        url_private = self.get_signed_url(s3_key, expires_in=3600)

        # Save metadata to database
        file_record = {
            "file_id": file_id,
            "workspace_id": workspace_id,
            "user_id": user_id,
            "name": file_data.filename,
            "title": metadata.get("title", file_data.filename),
            "mimetype": file_data.content_type,
            "size": file_data.size,
            "s3_key": s3_key,
            "url_private": url_private,
            "thumb_url": thumbnail_url
        }

        self.db.insert_file(file_record)

        # Share to channels if specified
        if metadata.get("channels"):
            for channel_id in metadata["channels"]:
                self.share_to_channel(file_id, channel_id)

        return file_record

    def get_signed_url(self, s3_key, expires_in=3600):
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': s3_key},
            ExpiresIn=expires_in
        )
```

## 8. Real-time Communication (WebSockets)

### Connection Architecture
```
User connects → Load Balancer → Gateway Server
                                     │
                                     ├─ Subscribe to user's channels
                                     ├─ Receive broadcasts for those channels
                                     └─ Send events to user
```

### Event Broadcasting
When a message is sent to a channel:
```
1. User A sends message via WebSocket
2. Gateway validates and forwards to Message Service
3. Message Service saves to database
4. Message Service publishes to Redis Pub/Sub: channel:{channel_id}
5. All Gateway servers subscribed to that channel receive event
6. Each Gateway sends event to connected users in that channel
```

### Redis Pub/Sub Pattern
```python
# Publisher (Message Service)
redis_client.publish(
    f"channel:{channel_id}",
    json.dumps({"type": "message", "data": message})
)

# Subscriber (Gateway Service)
pubsub = redis_client.pubsub()
pubsub.subscribe(f"channel:{channel_id}")

for message in pubsub.listen():
    # Broadcast to all connected users in this channel
    for user_id in self.get_channel_members(channel_id):
        connections = self.get_user_connections(user_id)
        for conn in connections:
            conn.send_json(message["data"])
```

## 9. Scalability & Performance

### Database Optimization
- **Table partitioning**: Partition messages table by timestamp (monthly)
- **Indexing**: Composite indexes on (channel_id, ts) and (channel_id, thread_ts, ts)
- **Read replicas**: Route read queries to replicas
- **Connection pooling**: Reuse database connections

### Caching Strategy
```
L1: Application cache (in-memory)
    - User profiles
    - Channel metadata
    - Recent messages (last 50 per channel)

L2: Redis cache
    - Online presence
    - Typing indicators
    - Unread counts
    - Session data

L3: Database
    - Full message history
    - All user/channel data
```

### Search Optimization
- **Index sharding**: One index per workspace
- **Async indexing**: Index messages asynchronously
- **Caching**: Cache frequent search queries
- **Pagination**: Limit result size, use scroll API for deep pagination

### File Storage
- **S3 lifecycle policies**: Move old files to Glacier
- **CDN**: CloudFront for file distribution
- **Signed URLs**: Temporary access to private files
- **Thumbnail generation**: Async with message queue

## 10. Trade-offs

### PostgreSQL vs NoSQL for Messages
**Chosen: PostgreSQL with partitioning**
- Pros: ACID, complex queries, consistency
- Cons: Harder horizontal scaling
- Alternative: Cassandra (better write throughput, eventual consistency)

### Elasticsearch vs PostgreSQL Full-text Search
**Chosen: Elasticsearch**
- Pros: Better relevance ranking, faster, more features
- Cons: Additional complexity, eventual consistency
- Alternative: PostgreSQL full-text (simpler, consistent, slower)

### WebSocket vs HTTP Polling
**Chosen: WebSocket**
- Pros: Lower latency, efficient, real-time
- Cons: More complex, stateful servers
- Alternative: HTTP/2 Server-Sent Events (simpler, unidirectional)

### Thread Storage Strategy
**Chosen: Denormalized (thread metadata on parent message)**
- Pros: Fast to display thread indicators
- Cons: Update overhead on replies
- Alternative: Separate thread table (normalized, slower reads)

## 11. Follow-up Questions

### Functional Enhancements
1. **How would you implement Slack Connect (cross-workspace channels)?**
   - Federated architecture with secure channel linking
   - Message replication across workspaces
   - Unified identity and authentication
   - Cross-workspace search considerations

2. **How would you add voice/video calls (Huddles)?**
   - WebRTC for peer-to-peer connections
   - Media servers for group calls (Janus/Jitsi)
   - Signaling through existing WebSocket
   - Recording and transcription services

3. **How would you implement slash commands and integrations?**
   - Webhook infrastructure for outgoing/incoming webhooks
   - OAuth 2.0 for third-party apps
   - Event subscription system
   - Rate limiting and security controls
   - App marketplace

### Scale & Performance
4. **How would you handle 100M DAU?**
   - Shard databases by workspace_id
   - Multi-region deployment
   - Separate read/write database clusters
   - Message queue for async processing
   - More aggressive caching

5. **How would you optimize search for very large workspaces?**
   - Index sharding within workspace
   - Search result caching
   - Pre-computed result pages for common queries
   - Incremental loading
   - Background indexing with eventual consistency

6. **How would you reduce database load?**
   - Write-through cache for recent messages
   - Read replicas for queries
   - Archive old messages to cold storage
   - Batch writes using message queue
   - Materialized views for aggregations

### Reliability & Security
7. **How would you ensure message ordering?**
   - Use Slack's timestamp format (seconds.microseconds)
   - Partition by channel for consistent ordering
   - Lamport clocks for distributed ordering
   - Client-side ordering by timestamp

8. **How would you handle workspace data isolation?**
   - Row-level security in PostgreSQL
   - Separate Elasticsearch indexes per workspace
   - Workspace-scoped authentication tokens
   - Regular security audits
   - Tenant isolation at application layer

9. **How would you implement data retention policies?**
   - Background job to archive/delete old messages
   - S3 lifecycle policies for files
   - Elasticsearch index lifecycle management
   - Legal hold support for compliance
   - Selective retention by channel

### Monitoring & Operations
10. **What metrics would you track?**
    - Message delivery latency (p50, p95, p99)
    - WebSocket connection count
    - Message throughput (QPS)
    - Search query latency
    - File upload success rate
    - Database query performance
    - Cache hit rates
    - Error rates by endpoint

11. **How would you handle database migrations?**
    - Online schema migrations (gh-ost, pt-online-schema-change)
    - Feature flags for new columns
    - Backward-compatible changes
    - Dual-write during migration
    - Gradual rollout

12. **How would you debug message delivery issues?**
    - Distributed tracing (message_id tracking)
    - Centralized logging with correlation IDs
    - Real-time monitoring dashboards
    - Message delivery audit trail
    - Client-side error reporting
