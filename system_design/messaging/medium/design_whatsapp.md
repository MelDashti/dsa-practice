# Design WhatsApp

## 1. Problem Overview

Design a messaging application like WhatsApp that supports one-on-one and group messaging with end-to-end encryption, media sharing, delivery/read receipts, and multi-device support. The system must handle billions of messages daily while maintaining security and privacy.

**Key Challenges**:
- End-to-end encryption for all messages
- Efficient group message delivery
- Media storage and sharing
- Multi-device synchronization
- High scalability (2B+ users)

## 2. Requirements

### Functional Requirements
- **Messaging**: One-on-one and group chats (up to 256 members)
- **Media Sharing**: Send/receive images, videos, documents, audio
- **End-to-End Encryption**: All messages encrypted
- **Message Status**: Sent, delivered, read receipts (double check marks)
- **User Presence**: Online/offline, last seen, typing indicators
- **Multi-device**: Support multiple devices per user
- **Message History**: Persistent storage, cloud backup
- **Profile Management**: Display name, profile picture, status

### Non-Functional Requirements
- **Availability**: 99.99% uptime
- **Latency**: < 100ms message delivery
- **Scalability**: 2B users, 100B messages/day
- **Security**: End-to-end encryption, no message storage on servers
- **Consistency**: Message ordering within conversations
- **Storage**: Efficient media storage and CDN delivery
- **Bandwidth**: Optimize for mobile networks

### Out of Scope
- Voice/video calls (separate system)
- Stories/Status updates
- Payments
- Business accounts
- Channels/Broadcasts

## 3. Scale Estimation

### Traffic Estimates
- **Total Users**: 2 billion
- **Daily Active Users (DAU)**: 500 million (25%)
- **Average messages per user per day**: 50
- **Total daily messages**: 25 billion
- **Messages per second**: 25B / 86400 ≈ 289,000 QPS (average)
- **Peak QPS**: 867,000 (3x average)
- **Group messages**: 20% of total
- **Media messages**: 30% of total

### Storage Estimates
- **Text message**: 100 bytes average
- **Media metadata**: 500 bytes
- **Image**: 200 KB average
- **Video**: 2 MB average
- **Daily text storage**: 17.5B × 100 bytes = 1.75 TB/day
- **Daily media storage**: 7.5B × 300 KB (avg) = 2.25 PB/day
- **Yearly storage**: ~800 PB (with compression and deduplication)

### Bandwidth Estimates
- **Incoming**: 289K QPS × 100 bytes = 28.9 MB/s (text only)
- **Media upload**: 7.5B / 86400 × 300 KB ≈ 26 GB/s
- **Total incoming**: ~26 GB/s
- **Outgoing**: Similar (slightly higher due to group fanout)

### Memory Estimates
- **Active connections**: 100M concurrent users
- **Connection memory**: 100M × 64 KB = 6.4 TB (distributed)
- **Recent message cache**: 100M users × 100 messages × 500 bytes = 5 TB

## 4. High-Level Design

```
┌──────────────────────────────────────────────────────────────────┐
│                         Client Devices                            │
│  (iOS, Android, Web, Desktop - End-to-End Encrypted)             │
└─────────────┬────────────────────────────────┬───────────────────┘
              │                                │
              │ WebSocket/HTTP2                │ HTTPS
              ▼                                ▼
┌─────────────────────────┐        ┌──────────────────────┐
│   Gateway/Connection    │        │    Media Upload      │
│       Cluster           │        │      Service         │
│   (WebSocket Mgmt)      │        └──────────┬───────────┘
└──────────┬──────────────┘                   │
           │                                  │
           ▼                                  ▼
┌──────────────────────────┐        ┌──────────────────────┐
│   Message Router         │        │   Media Storage      │
│   (Routing Logic)        │        │   (S3, CDN)          │
└──────────┬───────────────┘        └──────────────────────┘
           │
           ├─────────────┬──────────────┬──────────────────┐
           ▼             ▼              ▼                  ▼
┌──────────────┐  ┌─────────────┐  ┌────────────┐  ┌──────────────┐
│   Message    │  │  Presence   │  │   Group    │  │  Receipt     │
│   Service    │  │  Service    │  │  Service   │  │  Service     │
└──────┬───────┘  └──────┬──────┘  └─────┬──────┘  └──────┬───────┘
       │                 │                │                │
       ▼                 ▼                ▼                ▼
┌─────────────┐   ┌────────────┐  ┌────────────┐  ┌──────────────┐
│  Cassandra  │   │   Redis    │  │  Postgres  │  │   Redis      │
│  (Messages) │   │ (Presence) │  │  (Groups)  │  │  (Receipts)  │
└─────────────┘   └────────────┘  └────────────┘  └──────────────┘
```

## 5. API Design

### WebSocket Events

#### Send Message (Encrypted)
```json
{
  "event": "send_message",
  "data": {
    "message_id": "msg_abc123",
    "recipient_id": "user_456",  // or group_id
    "encrypted_content": "...",   // E2E encrypted
    "sender_key_id": "key_789",
    "timestamp": 1699876543210,
    "media_url": null             // or S3 URL for media
  }
}
```

#### Receive Message
```json
{
  "event": "receive_message",
  "data": {
    "message_id": "msg_abc123",
    "sender_id": "user_123",
    "encrypted_content": "...",
    "sender_key_id": "key_789",
    "timestamp": 1699876543211,
    "media_url": "https://cdn.whatsapp.com/media/abc123"
  }
}
```

#### Delivery/Read Receipt
```json
{
  "event": "receipt",
  "data": {
    "message_id": "msg_abc123",
    "type": "delivered",  // or "read"
    "user_id": "user_456",
    "timestamp": 1699876543212
  }
}
```

#### Typing Indicator
```json
{
  "event": "typing",
  "data": {
    "conversation_id": "conv_789",
    "user_id": "user_456",
    "is_typing": true
  }
}
```

### REST APIs

#### Upload Media
```
POST /api/v1/media/upload
Headers:
  Content-Type: multipart/form-data
  Authorization: Bearer <token>

Body:
  file: <binary>
  encrypted_key: <string>
  media_type: image|video|document|audio

Response:
{
  "media_id": "media_xyz789",
  "upload_url": "https://cdn.whatsapp.com/media/xyz789",
  "thumbnail_url": "https://cdn.whatsapp.com/thumb/xyz789",
  "size": 204800,
  "expiry": 1699963200
}
```

#### Get User Profile
```
GET /api/v1/users/{user_id}/profile

Response:
{
  "user_id": "user_456",
  "phone_number": "+1234567890",
  "display_name": "John Doe",
  "profile_picture_url": "https://cdn.whatsapp.com/profiles/456.jpg",
  "status": "Hey there! I am using WhatsApp",
  "last_seen_privacy": "contacts_only"
}
```

#### Create Group
```
POST /api/v1/groups
{
  "name": "Family Group",
  "member_ids": ["user_123", "user_456", "user_789"],
  "admin_ids": ["user_123"]
}

Response:
{
  "group_id": "group_abc",
  "name": "Family Group",
  "created_at": 1699876543000,
  "invite_link": "https://chat.whatsapp.com/invite/abc123"
}
```

#### Get Message History
```
GET /api/v1/conversations/{conversation_id}/messages
Query Parameters:
  - before: timestamp
  - limit: integer (default: 50)

Response:
{
  "messages": [
    {
      "message_id": "msg_abc123",
      "sender_id": "user_123",
      "encrypted_content": "...",
      "timestamp": 1699876543211,
      "status": "read"
    }
  ],
  "has_more": true
}
```

## 6. Data Models

### Message Table (Cassandra)
```cql
CREATE TABLE messages (
    conversation_id UUID,
    message_id UUID,
    sender_id UUID,
    encrypted_content BLOB,
    sender_key_id TEXT,
    media_url TEXT,
    media_type TEXT,
    timestamp BIGINT,
    PRIMARY KEY (conversation_id, timestamp, message_id)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Note: Encrypted content stored temporarily for offline delivery
-- Deleted after all recipients receive
```

### User Table (PostgreSQL)
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    profile_picture_url TEXT,
    status_text VARCHAR(200),
    public_key TEXT,  -- For E2E encryption
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen_at BIGINT
);

CREATE INDEX idx_phone_number ON users(phone_number);
```

### Group Table (PostgreSQL)
```sql
CREATE TABLE groups (
    group_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    group_picture_url TEXT,
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    max_members INT DEFAULT 256
);

CREATE TABLE group_members (
    group_id UUID REFERENCES groups(group_id),
    user_id UUID REFERENCES users(user_id),
    role VARCHAR(20), -- admin, member
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

CREATE INDEX idx_user_groups ON group_members(user_id);
```

### Device Table (PostgreSQL)
```sql
CREATE TABLE devices (
    device_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    device_type VARCHAR(20), -- ios, android, web, desktop
    device_token TEXT,  -- For push notifications
    public_key TEXT,    -- Device-specific E2E key
    last_active TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_user_devices ON devices(user_id, is_active);
```

### Redis Schemas

#### User Presence
```
Key: presence:user:{user_id}
Value: {
  "status": "online",
  "gateway_server": "gw-1.us-east",
  "last_seen": 1699876543000,
  "device_id": "device_abc123"
}
TTL: 5 minutes
```

#### Active Connections
```
Key: connections:{user_id}
Value: Set of {
  "device_id": "device_abc",
  "connection_id": "conn_xyz",
  "gateway_server": "gw-1"
}
```

#### Typing Indicators
```
Key: typing:{conversation_id}:{user_id}
Value: "1"
TTL: 10 seconds
```

#### Message Receipts (Temporary)
```
Key: receipt:{message_id}
Value: {
  "delivered": ["user_456", "user_789"],
  "read": ["user_456"]
}
TTL: 7 days
```

## 7. Core Services Design

### Gateway Service
**Responsibilities**:
- Maintain WebSocket connections
- Handle authentication and authorization
- Route messages to appropriate services
- Manage connection lifecycle

```python
class GatewayService:
    def on_connect(self, user_id, device_id, connection):
        # Authenticate user
        if not self.authenticate(user_id, device_id):
            connection.close()
            return

        # Store connection
        self.connection_manager.add(user_id, device_id, connection)

        # Update presence
        self.presence_service.mark_online(
            user_id, device_id, self.server_id
        )

        # Deliver pending messages
        self.deliver_pending_messages(user_id, device_id)

    def on_message_received(self, user_id, message_data):
        # Validate message
        if not self.validate_message(message_data):
            return

        # Route to message service
        if message_data.get("group_id"):
            self.group_service.send_group_message(message_data)
        else:
            self.message_service.send_message(message_data)

    def deliver_message(self, recipient_id, message):
        # Get all active devices for user
        devices = self.connection_manager.get_user_devices(recipient_id)

        # Deliver to all connected devices
        for device in devices:
            if device.is_connected():
                device.send(message)
```

### Message Service
**Responsibilities**:
- Handle one-on-one message delivery
- Store encrypted messages temporarily
- Manage message status updates
- Coordinate with receipt service

```python
class MessageService:
    def send_message(self, message_data):
        message = {
            "message_id": message_data["message_id"],
            "sender_id": message_data["sender_id"],
            "recipient_id": message_data["recipient_id"],
            "encrypted_content": message_data["encrypted_content"],
            "timestamp": current_timestamp(),
            "media_url": message_data.get("media_url")
        }

        # Store message temporarily (for offline delivery)
        conversation_id = self.get_conversation_id(
            message["sender_id"],
            message["recipient_id"]
        )
        self.store_message(conversation_id, message)

        # Try to deliver to recipient
        recipient_devices = self.presence_service.get_user_devices(
            message["recipient_id"]
        )

        if recipient_devices:
            for device in recipient_devices:
                gateway = device["gateway_server"]
                self.send_to_gateway(gateway, device["device_id"], message)
        else:
            # User offline, send push notification
            self.push_notification_service.send(
                message["recipient_id"],
                message["sender_id"]
            )

        # Confirm to sender
        self.send_status_update(
            message["sender_id"],
            message["message_id"],
            "sent"
        )

    def handle_delivery_receipt(self, message_id, user_id, device_id):
        # Update receipt tracking
        self.receipt_service.mark_delivered(
            message_id, user_id, device_id
        )

        # Get message sender
        message = self.get_message(message_id)

        # Notify sender
        self.send_status_update(
            message["sender_id"],
            message_id,
            "delivered"
        )

        # If all devices received, can delete encrypted message
        if self.receipt_service.all_devices_received(message_id, user_id):
            self.delete_message_content(message_id)
```

### Group Service
**Responsibilities**:
- Manage group membership
- Handle group message fanout
- Coordinate group operations (add/remove members)

```python
class GroupService:
    def send_group_message(self, message_data):
        group_id = message_data["group_id"]

        # Verify sender is member
        if not self.is_member(group_id, message_data["sender_id"]):
            raise UnauthorizedError()

        # Get all group members
        members = self.get_group_members(group_id)

        message = {
            "message_id": message_data["message_id"],
            "sender_id": message_data["sender_id"],
            "group_id": group_id,
            "encrypted_content": message_data["encrypted_content"],
            "timestamp": current_timestamp()
        }

        # Store message
        self.store_message(group_id, message)

        # Fan out to all members (except sender)
        recipients = [m for m in members if m != message_data["sender_id"]]

        # Use message queue for large groups
        if len(recipients) > 50:
            self.message_queue.publish("group_fanout", {
                "message": message,
                "recipients": recipients
            })
        else:
            # Direct delivery for small groups
            for recipient_id in recipients:
                self.message_service.deliver_to_user(recipient_id, message)

    def process_group_fanout(self, fanout_data):
        # Batch delivery worker
        message = fanout_data["message"]
        recipients = fanout_data["recipients"]

        # Batch process in chunks
        for chunk in self.chunk(recipients, 100):
            for recipient_id in chunk:
                self.message_service.deliver_to_user(recipient_id, message)
```

### Media Service
**Responsibilities**:
- Handle media uploads
- Generate thumbnails
- Manage media storage and CDN
- Track media expiry

```python
class MediaService:
    def upload_media(self, user_id, file_data, media_type):
        # Generate unique media ID
        media_id = generate_id()

        # Validate file size and type
        if not self.validate_media(file_data, media_type):
            raise ValidationError()

        # Process media based on type
        if media_type == "image":
            processed = self.process_image(file_data)
            thumbnail = self.generate_thumbnail(file_data)
        elif media_type == "video":
            processed = self.process_video(file_data)
            thumbnail = self.generate_video_thumbnail(file_data)
        else:
            processed = file_data
            thumbnail = None

        # Upload to S3
        media_url = self.s3_client.upload(
            f"media/{media_id}",
            processed,
            metadata={"user_id": user_id, "type": media_type}
        )

        if thumbnail:
            thumbnail_url = self.s3_client.upload(
                f"thumbnails/{media_id}",
                thumbnail
            )
        else:
            thumbnail_url = None

        # Store metadata
        self.db.save_media_metadata({
            "media_id": media_id,
            "user_id": user_id,
            "media_type": media_type,
            "media_url": media_url,
            "thumbnail_url": thumbnail_url,
            "size": len(file_data),
            "uploaded_at": current_timestamp(),
            "expires_at": current_timestamp() + 30 * 86400  # 30 days
        })

        # Invalidate CDN cache and pre-warm
        self.cdn.invalidate(media_url)

        return {
            "media_id": media_id,
            "media_url": media_url,
            "thumbnail_url": thumbnail_url
        }

    def cleanup_expired_media(self):
        # Background job to delete expired media
        expired = self.db.get_expired_media()

        for media in expired:
            self.s3_client.delete(media["media_url"])
            if media["thumbnail_url"]:
                self.s3_client.delete(media["thumbnail_url"])

            self.db.delete_media_metadata(media["media_id"])
```

### Presence Service
**Responsibilities**:
- Track user online/offline status
- Manage last seen timestamps
- Handle typing indicators

```python
class PresenceService:
    def mark_online(self, user_id, device_id, gateway_server):
        presence_data = {
            "status": "online",
            "device_id": device_id,
            "gateway_server": gateway_server,
            "last_seen": current_timestamp()
        }

        # Store in Redis with TTL
        self.redis.setex(
            f"presence:user:{user_id}:{device_id}",
            300,  # 5 minutes
            json.dumps(presence_data)
        )

        # Add to user's active connections set
        self.redis.sadd(f"connections:{user_id}", device_id)

        # Notify contacts about online status
        self.notify_contacts_presence(user_id, "online")

    def mark_offline(self, user_id, device_id):
        # Remove from active connections
        self.redis.srem(f"connections:{user_id}", device_id)
        self.redis.delete(f"presence:user:{user_id}:{device_id}")

        # Update last seen in database
        self.db.update_last_seen(user_id, current_timestamp())

        # Check if user has other active devices
        if self.redis.scard(f"connections:{user_id}") == 0:
            # No active devices, notify contacts
            self.notify_contacts_presence(user_id, "offline")

    def get_user_status(self, user_id, requester_id):
        # Check privacy settings
        privacy = self.get_privacy_settings(user_id)

        if not self.can_see_status(requester_id, privacy):
            return {"status": "unavailable"}

        # Check if any device is online
        active_devices = self.redis.smembers(f"connections:{user_id}")

        if active_devices:
            return {"status": "online"}
        else:
            last_seen = self.db.get_last_seen(user_id)
            return {"status": "offline", "last_seen": last_seen}
```

## 8. Real-time Communication (WebSockets)

### Connection Architecture
```
┌──────────────────────────────────────────────────────┐
│                    Load Balancer                      │
│              (Sticky Session / DNS)                   │
└────────────────────┬─────────────────────────────────┘
                     │
          ┌──────────┴──────────┬──────────────┐
          ▼                     ▼              ▼
    ┌─────────────┐      ┌─────────────┐  ┌─────────────┐
    │ Gateway-1   │      │ Gateway-2   │  │ Gateway-N   │
    │ 1M conns    │      │ 1M conns    │  │ 1M conns    │
    └─────────────┘      └─────────────┘  └─────────────┘
```

### Message Flow with E2E Encryption
```
Sender Device                    Server                    Recipient Device
     │                             │                             │
     ├─ Encrypt with recipient's   │                             │
     │  public key                 │                             │
     ├─ Send encrypted message ───►│                             │
     │                             ├─ Route to recipient ───────►│
     │                             │                             ├─ Decrypt with
     │                             │                             │  private key
     │◄─ Sent ACK ─────────────────┤                             │
     │                             │◄─ Delivered ACK ────────────┤
     │◄─ Delivered notification ───┤                             │
     │                             │◄─ Read ACK ─────────────────┤
     │◄─ Read notification ─────────┤                             │
```

### Multi-Device Synchronization
- Each device has unique encryption keys
- Messages encrypted separately for each device
- Server maintains device list per user
- Sync state across devices using message IDs

### Handling Network Issues
1. **Exponential backoff** for reconnection
2. **Message queue** on client for offline messages
3. **Sync protocol** to fetch missed messages
4. **Delta sync** to minimize bandwidth

## 9. End-to-End Encryption

### Signal Protocol Implementation

**Key Components**:
1. **Identity Keys**: Long-term key pair (public/private)
2. **Signed Pre-keys**: Medium-term keys signed by identity key
3. **One-time Pre-keys**: Single-use keys for forward secrecy
4. **Session Keys**: Derived for each conversation

### Key Exchange Process
```
User A                           Server                        User B
  │                                 │                            │
  │──── Upload Pre-keys ───────────►│                            │
  │                                 │◄─── Upload Pre-keys ───────┤
  │                                 │                            │
  │──── Request B's Pre-keys ──────►│                            │
  │◄─── Return B's Pre-keys ────────┤                            │
  │                                 │                            │
  ├─ Perform X3DH key agreement    │                            │
  ├─ Derive shared secret           │                            │
  │                                 │                            │
  ├─ Encrypt message with           │                            │
  │   shared secret                 │                            │
  │──── Send encrypted message ─────┼───────────────────────────►│
  │                                 │                            ├─ Decrypt using
  │                                 │                            │   shared secret
```

### Message Encryption Format
```json
{
  "version": 1,
  "encrypted_content": "<base64_encrypted_data>",
  "sender_key_id": "key_abc123",
  "recipient_key_id": "key_xyz789",
  "initialization_vector": "<base64_iv>",
  "mac": "<message_authentication_code>"
}
```

### Group Encryption
- **Sender Keys Protocol**: Efficient for group messaging
- Each member has a sender key
- Messages encrypted once with sender key
- Recipients use sender's public key to decrypt

## 10. Scalability & Performance

### Database Sharding Strategy
- **User Sharding**: Shard by user_id hash
- **Message Sharding**: Shard by conversation_id
- **Group Sharding**: Shard by group_id

### Cassandra for Messages
**Why Cassandra?**
- High write throughput
- Linear scalability
- Time-series data (messages sorted by timestamp)
- Tunable consistency

**Schema Design**:
```cql
-- Optimized for read pattern: "Get messages for conversation"
CREATE TABLE messages (
    conversation_id UUID,
    timestamp BIGINT,
    message_id UUID,
    sender_id UUID,
    encrypted_content BLOB,
    media_url TEXT,
    PRIMARY KEY (conversation_id, timestamp, message_id)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

### Caching Strategy
```
┌─────────────────────────────────────────────────┐
│                  Cache Layer                     │
├─────────────────────────────────────────────────┤
│  - Recent messages (last 50 per conversation)   │
│  - User profiles and public keys                │
│  - Group memberships                            │
│  - Online presence                              │
│  - Typing indicators                            │
└─────────────────────────────────────────────────┘

TTL Strategy:
- Messages: 1 hour
- Profiles: 6 hours
- Presence: 5 minutes
- Typing: 10 seconds
```

### Media Storage & CDN
```
┌──────────┐      ┌─────────────┐      ┌──────────────┐
│  Client  │─────►│  Upload to  │─────►│   S3/Blob    │
│          │      │  S3 Direct  │      │   Storage    │
└──────────┘      └─────────────┘      └──────┬───────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │  CloudFront CDN │
                                     │  (Edge Caching) │
                                     └─────────────────┘
```

### Connection Management
- **Gateway servers**: 1M connections per server
- **Connection pooling**: Reuse database connections
- **Heartbeat**: 30-second interval to detect dead connections
- **Graceful shutdown**: Migrate connections before server restart

### Performance Optimizations
1. **Message batching**: Batch delivery for group messages
2. **Protocol buffers**: Use protobuf instead of JSON
3. **Compression**: Gzip compression for media
4. **Image optimization**: WebP format, multiple resolutions
5. **Video streaming**: Adaptive bitrate, HLS protocol
6. **Database connection pooling**: Reduce connection overhead
7. **Async processing**: Use message queues for non-critical paths

## 11. Trade-offs

### End-to-End Encryption vs Search
**Chosen: E2E Encryption (No Server-side Search)**
- Pros: Maximum privacy and security
- Cons: Cannot search messages server-side, no ML features
- Alternative: Client-side search only, slower

### Message Storage Duration
**Chosen: Store until all devices receive + 30 days**
- Pros: Reliable delivery, supports offline users
- Cons: Storage costs
- Alternative: Store for fixed duration (7 days), risk message loss

### Group Size Limit
**Chosen: 256 members**
- Pros: Manageable fanout, reasonable performance
- Cons: Cannot support large communities
- Alternative: Unlimited groups but with degraded features

### Multi-device Synchronization
**Chosen: Each device gets encrypted copy**
- Pros: True E2E encryption, device independence
- Cons: Multiple encryption/decryption operations
- Alternative: Shared device key (weaker security)

### Media Storage
**Chosen: Time-limited storage (30 days) + CDN**
- Pros: Cost-effective, fast delivery
- Cons: Media expires, user must backup
- Alternative: Permanent storage (expensive)

### Database Choice for Messages
**Chosen: Cassandra**
- Pros: High write throughput, scalable
- Cons: Eventual consistency, complex operations
- Alternative: PostgreSQL (simpler, ACID, harder to scale)

## 12. Follow-up Questions

### Functional Enhancements
1. **How would you add voice/video calling?**
   - Use WebRTC for peer-to-peer connections
   - TURN/STUN servers for NAT traversal
   - Media relay servers for poor connections
   - Signaling through existing WebSocket

2. **How would you implement message reactions?**
   - Store reactions as separate records linked to message_id
   - Aggregate reactions client-side
   - Send reaction events through WebSocket
   - Cache popular reactions

3. **How would you support message forwarding?**
   - Re-encrypt message with new recipient's key
   - Maintain forward chain metadata
   - Prevent deep forwarding chains (limit hops)
   - Track forwarded message source

### Scale & Performance
4. **How would you handle 10B users instead of 2B?**
   - More database shards (100+ shards)
   - Multi-region deployment with regional routing
   - Hierarchical caching (L1: local, L2: regional)
   - Separate infrastructure for different regions

5. **How would you reduce latency for global users?**
   - Deploy in multiple regions (US, EU, Asia)
   - Route users to nearest region
   - Cross-region message routing
   - Regional read replicas

6. **How would you optimize for low-bandwidth networks?**
   - Implement delta sync (only changed data)
   - Use smaller protocol (protobuf vs JSON)
   - Progressive image loading
   - Message compression
   - Lower quality media options

### Reliability & Security
7. **How would you ensure exactly-once message delivery?**
   - Use idempotency keys (message_id)
   - Deduplicate at receiver using message_id
   - Atomic operations in database
   - Acknowledgment protocol with retries

8. **How would you handle compromised encryption keys?**
   - Key rotation mechanism
   - Security code verification (out-of-band)
   - Alert users to key changes
   - Option to block user until verification
   - Forward secrecy (new keys for each session)

9. **How would you implement backup and restore?**
   - Client-side encrypted backup to cloud
   - User-controlled encryption key (password-derived)
   - Incremental backups (delta)
   - Restore on new device with key

### Monitoring & Operations
10. **What metrics would you track?**
    - Message delivery latency (p50, p95, p99)
    - Message delivery success rate
    - Active connections per gateway
    - Message throughput (QPS)
    - Media upload/download success rate
    - Encryption/decryption time
    - Database query latency
    - Cache hit rate

11. **How would you handle service degradation?**
    - Circuit breaker pattern
    - Graceful degradation (disable non-critical features)
    - Rate limiting per user
    - Queue messages during downtime
    - Fail-safe to read-only mode

12. **How would you test E2E encryption at scale?**
    - Unit tests for cryptographic primitives
    - Integration tests for key exchange
    - Security audit and penetration testing
    - Canary deployment for encryption changes
    - Monitor decryption failure rates
