# Design Discord

## 1. Problem Overview

Design a communication platform like Discord that supports text, voice, and video chat organized into servers and channels. The system must handle real-time communication for gaming communities with features like voice channels, screen sharing, and low-latency messaging optimized for group interactions.

**Key Challenges**:
- Real-time voice and video communication
- Server-based organization with multiple channels
- Low-latency messaging for gaming
- Scalable voice channel architecture
- Rich presence and activity tracking
- Bot and integration platform

## 2. Requirements

### Functional Requirements
- **Servers**: Users can create and join servers (communities)
- **Channels**: Text, voice, and announcement channels per server
- **Text Messaging**: Real-time chat in text channels
- **Voice Communication**: Real-time voice chat in voice channels
- **Video Streaming**: Video calls and screen sharing
- **Roles & Permissions**: Granular permission system
- **Direct Messages**: Private 1-on-1 and group DMs
- **Rich Presence**: Game activity, custom status
- **Bot Integration**: Bots with commands and automation
- **Nitro Features**: Enhanced features for premium users

### Non-Functional Requirements
- **Latency**: < 50ms for voice, < 100ms for messages
- **Availability**: 99.95% uptime
- **Scalability**: 150M+ MAU, 19M+ concurrent voice users
- **Reliability**: No message loss, voice quality maintenance
- **Performance**: Handle 15M concurrent users in voice
- **Security**: Secure voice/video streams, encrypted DMs

### Out of Scope
- Game store and library
- Nitro gift subscriptions
- Server templates and discovery
- Stage channels
- Forum channels

## 3. Scale Estimation

### Traffic Estimates
- **Total Users**: 150 million
- **Daily Active Users (DAU)**: 50 million (33%)
- **Concurrent peak users**: 20 million
- **Concurrent voice users (peak)**: 3 million
- **Servers per user**: 5 average
- **Messages per user per day**: 30
- **Daily messages**: 1.5 billion
- **Messages per second**: 17,400 QPS (average)
- **Peak QPS**: 52,000

### Voice Estimates
- **Concurrent voice users**: 3 million
- **Average voice session**: 2 hours
- **Voice bitrate**: 64 kbps per user
- **Bandwidth per user**: 64 kbps upload + (N-1) × 64 kbps download
- **Total voice bandwidth**: ~400 Gbps

### Storage Estimates
- **Text message**: 200 bytes
- **Daily text storage**: 1.5B × 200 bytes = 300 GB/day
- **Yearly text storage**: 110 TB/year
- **Voice recordings**: Minimal (not stored by default)
- **Images/files**: 20% of messages = 300M files/day × 500 KB = 150 TB/day

### Memory Estimates
- **Active connections**: 20M users × 10 KB = 200 GB
- **Voice state**: 3M users × 50 KB = 150 GB
- **Recent message cache**: 50M users × 5 servers × 20 msgs × 200 bytes = 10 TB
- **Presence data**: 20M users × 1 KB = 20 GB

## 4. High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│        (Desktop, Mobile, Web, Game Overlay)                  │
└────────────────────┬───────────────────────────┬────────────┘
                     │                           │
         ┌───────────┴─────────────┐    ┌────────┴────────────┐
         │  Gateway (Text/Events)  │    │ Voice Gateway       │
         │     (WebSocket)         │    │  (WebRTC/UDP)       │
         └────────────┬────────────┘    └─────────┬───────────┘
                      │                           │
        ┌─────────────┴──────────────┐            │
        │                            │            │
        ▼                            ▼            ▼
┌───────────────┐          ┌──────────────────┐  ┌─────────────┐
│   API Layer   │          │  Event Dispatch  │  │   Voice     │
│  (REST APIs)  │          │                  │  │  Servers    │
└───────┬───────┘          └────────┬─────────┘  └──────┬──────┘
        │                           │                   │
        └───────────────┬───────────┘                   │
                        │                               │
    ┌───────────────────┼────────────────┬──────────────┤
    │                   │                │              │
    ▼                   ▼                ▼              ▼
┌─────────┐      ┌──────────┐    ┌────────────┐  ┌──────────┐
│ Message │      │  Server  │    │  Presence  │  │   Voice  │
│ Service │      │ Service  │    │  Service   │  │  Service │
└────┬────┘      └────┬─────┘    └─────┬──────┘  └────┬─────┘
     │                │                 │              │
     └────────────────┴─────────────────┴──────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐   ┌────────────┐   ┌───────────────┐
│  Cassandra   │   │   Redis    │   │ Media Servers │
│  (Messages)  │   │  (Cache)   │   │  (WebRTC)     │
└──────────────┘   └────────────┘   └───────────────┘
```

## 5. API Design

### WebSocket Events (Gateway)

#### Message Create
```json
{
  "op": 0,  // Dispatch opcode
  "t": "MESSAGE_CREATE",
  "d": {
    "id": "123456789012345678",
    "channel_id": "987654321098765432",
    "author": {
      "id": "111222333444555666",
      "username": "JohnDoe",
      "avatar": "a1b2c3d4e5f6..."
    },
    "content": "Hello everyone!",
    "timestamp": "2024-11-12T12:34:56.789000+00:00",
    "mentions": [],
    "attachments": []
  }
}
```

#### Voice State Update
```json
{
  "op": 0,
  "t": "VOICE_STATE_UPDATE",
  "d": {
    "guild_id": "555666777888999000",
    "channel_id": "222333444555666777",  // null if disconnected
    "user_id": "111222333444555666",
    "session_id": "abc123def456",
    "deaf": false,
    "mute": false,
    "self_deaf": false,
    "self_mute": false,
    "self_video": false
  }
}
```

#### Presence Update
```json
{
  "op": 0,
  "t": "PRESENCE_UPDATE",
  "d": {
    "user": {
      "id": "111222333444555666"
    },
    "guild_id": "555666777888999000",
    "status": "online",  // online, idle, dnd, offline
    "activities": [
      {
        "name": "Valorant",
        "type": 0,  // 0: Playing, 1: Streaming, 2: Listening, 3: Watching
        "created_at": 1699876543000,
        "timestamps": {
          "start": 1699876543000
        }
      }
    ],
    "client_status": {
      "desktop": "online",
      "mobile": "idle"
    }
  }
}
```

#### Heartbeat
```json
{
  "op": 1,  // Heartbeat opcode
  "d": 251  // Last sequence number received
}
```

### REST APIs

#### Send Message
```
POST /api/v9/channels/{channel_id}/messages
{
  "content": "Hello!",
  "tts": false,
  "embeds": [],
  "allowed_mentions": {"parse": ["users", "roles"]},
  "message_reference": {  // For replies
    "message_id": "123456789"
  }
}

Response:
{
  "id": "123456789012345678",
  "channel_id": "987654321098765432",
  "author": {...},
  "content": "Hello!",
  "timestamp": "2024-11-12T12:34:56.789000+00:00"
}
```

#### Get Messages
```
GET /api/v9/channels/{channel_id}/messages
Query Parameters:
  - limit: 50 (default)
  - before: message_id
  - after: message_id
  - around: message_id

Response:
[
  {
    "id": "123456789012345678",
    "channel_id": "987654321098765432",
    "author": {...},
    "content": "Message text",
    "timestamp": "2024-11-12T12:34:56.789000+00:00"
  }
]
```

#### Create Guild (Server)
```
POST /api/v9/guilds
{
  "name": "My Gaming Server",
  "region": "us-west",
  "icon": "data:image/png;base64,...",
  "verification_level": 1,
  "default_message_notifications": 0,
  "explicit_content_filter": 2
}

Response:
{
  "id": "555666777888999000",
  "name": "My Gaming Server",
  "owner_id": "111222333444555666",
  "region": "us-west",
  "created_at": "2024-11-12T12:34:56.789000+00:00"
}
```

#### Join Voice Channel
```
POST /api/v9/guilds/{guild_id}/voice-states/@me
{
  "channel_id": "222333444555666777",
  "self_mute": false,
  "self_deaf": false
}

Response:
{
  "token": "voice_token_abc123",
  "endpoint": "us-west123.discord.media:443",
  "session_id": "session_xyz789"
}
```

#### Create Role
```
POST /api/v9/guilds/{guild_id}/roles
{
  "name": "Moderator",
  "permissions": "8",  // Bitwise permissions
  "color": 3447003,  // RGB color
  "hoist": true,  // Display separately
  "mentionable": true
}
```

## 6. Data Models

### Guild (Server) Table (PostgreSQL)
```sql
CREATE TABLE guilds (
    guild_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    icon_hash VARCHAR(64),
    owner_id BIGINT NOT NULL,
    region VARCHAR(50),
    afk_channel_id BIGINT,
    afk_timeout INT DEFAULT 300,
    verification_level INT DEFAULT 0,
    default_message_notifications INT DEFAULT 0,
    explicit_content_filter INT DEFAULT 0,
    features TEXT[],
    mfa_level INT DEFAULT 0,
    system_channel_id BIGINT,
    premium_tier INT DEFAULT 0,
    member_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_owner ON guilds(owner_id);
```

### Channel Table (PostgreSQL)
```sql
CREATE TABLE channels (
    channel_id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    name VARCHAR(100) NOT NULL,
    type INT NOT NULL, -- 0: text, 2: voice, 4: category, 5: announcement
    position INT,
    topic TEXT,
    nsfw BOOLEAN DEFAULT false,
    last_message_id BIGINT,
    bitrate INT, -- For voice channels
    user_limit INT, -- For voice channels (0 = unlimited)
    rate_limit_per_user INT DEFAULT 0,
    parent_id BIGINT, -- Category ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_guild_channels ON channels(guild_id, position);
CREATE INDEX idx_parent ON channels(parent_id);
```

### Member Table (PostgreSQL)
```sql
CREATE TABLE members (
    guild_id BIGINT,
    user_id BIGINT,
    nick VARCHAR(32),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    premium_since TIMESTAMP,
    deaf BOOLEAN DEFAULT false,
    mute BOOLEAN DEFAULT false,
    pending BOOLEAN DEFAULT false,

    PRIMARY KEY (guild_id, user_id)
);

CREATE INDEX idx_user_guilds ON members(user_id);
```

### Member Roles Table (PostgreSQL)
```sql
CREATE TABLE member_roles (
    guild_id BIGINT,
    user_id BIGINT,
    role_id BIGINT,

    PRIMARY KEY (guild_id, user_id, role_id),
    FOREIGN KEY (guild_id, user_id) REFERENCES members(guild_id, user_id)
);

CREATE INDEX idx_role_members ON member_roles(guild_id, role_id);
```

### Role Table (PostgreSQL)
```sql
CREATE TABLE roles (
    role_id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    name VARCHAR(100) NOT NULL,
    color INT DEFAULT 0,
    hoist BOOLEAN DEFAULT false,
    position INT,
    permissions BIGINT DEFAULT 0, -- Bitwise permissions
    managed BOOLEAN DEFAULT false,
    mentionable BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_guild_roles ON roles(guild_id, position);
```

### Message Table (Cassandra)
```cql
CREATE TABLE messages (
    channel_id BIGINT,
    message_id BIGINT,
    author_id BIGINT,
    content TEXT,
    timestamp TIMESTAMP,
    edited_timestamp TIMESTAMP,
    tts BOOLEAN,
    mention_everyone BOOLEAN,
    mentions LIST<BIGINT>,
    mention_roles LIST<BIGINT>,
    attachments LIST<TEXT>, -- JSON serialized
    embeds LIST<TEXT>, -- JSON serialized
    reactions MAP<TEXT, LIST<BIGINT>>, -- emoji -> user_ids
    pinned BOOLEAN,
    type INT DEFAULT 0,

    PRIMARY KEY (channel_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

### Voice State Table (Redis)
```
Key: voice_state:{guild_id}:{user_id}
Value: {
  "channel_id": "222333444555666777",
  "session_id": "abc123",
  "deaf": false,
  "mute": false,
  "self_deaf": false,
  "self_mute": false,
  "self_video": false,
  "server": "voice-us-west-1"
}
TTL: 30 seconds (renewed with heartbeat)
```

### Presence Table (Redis)
```
Key: presence:{guild_id}:{user_id}
Value: {
  "status": "online",
  "activities": [{...}],
  "client_status": {...}
}
TTL: 5 minutes
```

### Voice Server Mapping (Redis)
```
Key: voice_channel:{channel_id}
Value: Set of {
  "user_id": "111222333444555666",
  "session_id": "abc123",
  "server": "voice-us-west-1"
}
```

## 7. Core Services Design

### Message Service
```python
class MessageService:
    def create_message(self, channel_id, author_id, content, options):
        # Check permissions
        if not self.has_permission(author_id, channel_id, "SEND_MESSAGES"):
            raise ForbiddenError()

        # Generate snowflake ID
        message_id = self.generate_snowflake()

        message = {
            "message_id": message_id,
            "channel_id": channel_id,
            "author_id": author_id,
            "content": content,
            "timestamp": datetime.utcnow(),
            "mentions": self.extract_mentions(content),
            "mention_roles": self.extract_role_mentions(content),
            "attachments": options.get("attachments", []),
            "embeds": options.get("embeds", [])
        }

        # Store in Cassandra
        self.db.insert_message(message)

        # Update last_message_id for channel
        self.redis.set(f"channel:{channel_id}:last_message", message_id)

        # Dispatch event to gateway
        self.event_dispatcher.dispatch({
            "op": 0,
            "t": "MESSAGE_CREATE",
            "d": message
        }, channel_id)

        # Handle mentions
        if message["mentions"]:
            self.notification_service.send_mention_notifications(message)

        return message

    def get_messages(self, channel_id, user_id, limit, before, after):
        # Check read permissions
        if not self.has_permission(user_id, channel_id, "VIEW_CHANNEL"):
            raise ForbiddenError()

        # Query Cassandra
        messages = self.db.query("""
            SELECT * FROM messages
            WHERE channel_id = ?
              AND message_id < ?
            ORDER BY message_id DESC
            LIMIT ?
        """, (channel_id, before or 2**63, limit))

        return messages
```

### Voice Service
```python
class VoiceService:
    def join_voice_channel(self, guild_id, channel_id, user_id):
        # Check permissions
        if not self.has_permission(user_id, channel_id, "CONNECT"):
            raise ForbiddenError()

        # Check channel user limit
        current_users = self.redis.scard(f"voice_channel:{channel_id}")
        channel = self.get_channel(channel_id)

        if channel.user_limit > 0 and current_users >= channel.user_limit:
            raise ChannelFullError()

        # Select voice server (geographically close)
        user_region = self.get_user_region(user_id)
        voice_server = self.select_voice_server(user_region)

        # Generate session
        session_id = uuid.uuid4().hex
        token = self.generate_voice_token(user_id, guild_id, channel_id)

        # Store voice state
        voice_state = {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "user_id": user_id,
            "session_id": session_id,
            "server": voice_server,
            "deaf": False,
            "mute": False,
            "self_deaf": False,
            "self_mute": False
        }

        self.redis.setex(
            f"voice_state:{guild_id}:{user_id}",
            30,  # 30 seconds, renewed by heartbeat
            json.dumps(voice_state)
        )

        # Add to channel set
        self.redis.sadd(f"voice_channel:{channel_id}", user_id)

        # Dispatch voice state update
        self.event_dispatcher.dispatch({
            "op": 0,
            "t": "VOICE_STATE_UPDATE",
            "d": voice_state
        }, guild_id)

        return {
            "token": token,
            "guild_id": guild_id,
            "endpoint": f"{voice_server}.discord.media:443",
            "session_id": session_id
        }

    def select_voice_server(self, region):
        # Get voice servers for region
        servers = self.get_voice_servers(region)

        # Select least loaded server
        server_loads = []
        for server in servers:
            load = self.redis.get(f"voice_server:{server}:load")
            server_loads.append((server, int(load or 0)))

        # Return server with minimum load
        return min(server_loads, key=lambda x: x[1])[0]
```

### Server (Guild) Service
```python
class GuildService:
    def create_guild(self, owner_id, name, options):
        # Generate snowflake ID
        guild_id = self.generate_snowflake()

        guild = {
            "guild_id": guild_id,
            "name": name,
            "owner_id": owner_id,
            "region": options.get("region", "us-central"),
            "verification_level": options.get("verification_level", 0),
            "member_count": 1
        }

        # Create guild
        self.db.insert_guild(guild)

        # Add owner as member
        self.add_member(guild_id, owner_id, is_owner=True)

        # Create default channels
        self.create_default_channels(guild_id)

        # Create @everyone role
        self.create_everyone_role(guild_id)

        return guild

    def create_default_channels(self, guild_id):
        # Create general text channel
        self.channel_service.create_channel(
            guild_id,
            "general",
            channel_type=0  # Text
        )

        # Create general voice channel
        self.channel_service.create_channel(
            guild_id,
            "General",
            channel_type=2  # Voice
        )

    def add_member(self, guild_id, user_id, is_owner=False):
        # Insert member
        self.db.execute("""
            INSERT INTO members (guild_id, user_id)
            VALUES (?, ?)
        """, (guild_id, user_id))

        # Assign @everyone role
        everyone_role = self.get_everyone_role(guild_id)
        self.assign_role(guild_id, user_id, everyone_role.id)

        # Increment member count
        self.db.execute("""
            UPDATE guilds
            SET member_count = member_count + 1
            WHERE guild_id = ?
        """, (guild_id,))

        # Dispatch guild member add event
        self.event_dispatcher.dispatch({
            "op": 0,
            "t": "GUILD_MEMBER_ADD",
            "d": {
                "guild_id": guild_id,
                "user": self.get_user(user_id),
                "joined_at": datetime.utcnow().isoformat()
            }
        }, guild_id)
```

### Presence Service
```python
class PresenceService:
    def update_presence(self, user_id, guild_id, status, activities):
        presence = {
            "user_id": user_id,
            "guild_id": guild_id,
            "status": status,
            "activities": activities,
            "client_status": self.get_client_status(user_id)
        }

        # Store in Redis
        self.redis.setex(
            f"presence:{guild_id}:{user_id}",
            300,  # 5 minutes
            json.dumps(presence)
        )

        # Dispatch presence update to guild
        self.event_dispatcher.dispatch({
            "op": 0,
            "t": "PRESENCE_UPDATE",
            "d": presence
        }, guild_id)

    def get_guild_presences(self, guild_id):
        # Get all members
        members = self.guild_service.get_members(guild_id)

        presences = []
        for member_id in members:
            presence_data = self.redis.get(
                f"presence:{guild_id}:{member_id}"
            )
            if presence_data:
                presences.append(json.loads(presence_data))
            else:
                # Default to offline
                presences.append({
                    "user_id": member_id,
                    "status": "offline"
                })

        return presences
```

## 8. Real-time Communication (WebSockets)

### Gateway Protocol
Discord uses a custom WebSocket protocol with opcodes:
```
0  - Dispatch: Server sending events to client
1  - Heartbeat: Client or server heartbeat
2  - Identify: Client authentication
3  - Presence Update: Update client status
4  - Voice State Update: Join/leave voice channels
6  - Resume: Resume a disconnected session
7  - Reconnect: Server telling client to reconnect
9  - Invalid Session: Invalid session, need to re-identify
10 - Hello: Server greeting with heartbeat interval
11 - Heartbeat ACK: Server acknowledging heartbeat
```

### Connection Flow
```
Client                              Gateway
  │                                    │
  ├──── Connect ──────────────────────►│
  │◄──── Hello (op: 10) ───────────────┤ (heartbeat_interval: 45000)
  │                                    │
  ├──── Identify (op: 2) ─────────────►│ (token, properties)
  │◄──── Ready (op: 0) ────────────────┤ (user info, guilds)
  │                                    │
  ├──── Heartbeat (op: 1) ────────────►│ (every 45 seconds)
  │◄──── Heartbeat ACK (op: 11) ───────┤
  │                                    │
  │◄──── Event (op: 0) ────────────────┤ (MESSAGE_CREATE, etc.)
```

### Voice WebRTC Architecture
```
Client                    Voice Gateway              Media Server
  │                            │                          │
  ├─ Join voice channel ──────►│                          │
  │◄─ Voice server info ───────┤                          │
  │                            │                          │
  ├─ Connect to media ─────────┼─────────────────────────►│
  │                            │                          │
  ├─ WebRTC negotiation ───────┼─────────────────────────►│
  │  (SDP offer/answer)        │                          │
  │                            │                          │
  ├─ DTLS handshake ───────────┼─────────────────────────►│
  │                            │                          │
  ├─ RTP/SRTP audio stream ────┼─────────────────────────►│
  │◄─ Mixed audio from others ─┼──────────────────────────┤
```

## 9. Voice Infrastructure

### Voice Server Architecture
```
┌──────────────────────────────────────────────────┐
│              Voice Region Cluster                 │
├──────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │  Media     │  │  Media     │  │  Media     │ │
│  │  Server 1  │  │  Server 2  │  │  Server N  │ │
│  └────────────┘  └────────────┘  └────────────┘ │
│        │               │               │         │
│        └───────────────┴───────────────┘         │
│                      │                           │
│              ┌───────▼────────┐                  │
│              │  Load Balancer │                  │
│              └────────────────┘                  │
└──────────────────────────────────────────────────┘
```

### Audio Processing Pipeline
1. **Client captures audio** (microphone input)
2. **Encode to Opus** (efficient, low-latency codec)
3. **Encrypt with DTLS-SRTP**
4. **Send UDP packets** to media server
5. **Server decodes** all participant streams
6. **Mix audio** (combine streams)
7. **Re-encode mixed audio**
8. **Send to each participant** (excluding their own voice)

### Optimizations
- **Jitter buffer**: Handle packet reordering and delay
- **Packet loss concealment**: Fill in missing audio
- **Automatic gain control**: Normalize volume levels
- **Echo cancellation**: Remove echo feedback
- **Noise suppression**: Filter background noise
- **Forward error correction**: Recover from packet loss

## 10. Scalability & Performance

### Sharding Strategy
Discord uses sharding to distribute guilds across multiple processes:
```python
shard_id = (guild_id >> 22) % num_shards
```

Each shard handles a subset of guilds, allowing horizontal scaling.

### Database Optimization
- **Guild sharding**: Partition by guild_id
- **Message archiving**: Move old messages to cold storage
- **Cassandra for messages**: High write throughput
- **PostgreSQL for metadata**: Consistency for guilds/channels/members
- **Redis for real-time data**: Presence, voice state, typing

### Caching Strategy
```
- Guild metadata: 1 hour TTL
- Channel metadata: 1 hour TTL
- Member data: 30 minutes TTL
- Messages: Recent 50 per channel
- Presence: 5 minutes TTL
- Voice state: 30 seconds TTL (heartbeat)
```

### Voice Optimization
- **Regional voice servers**: Reduce latency
- **UDP over TCP**: Lower latency, better for real-time
- **Opus codec**: Efficient compression
- **Selective forwarding**: Send only needed streams
- **Simulcast**: Multiple quality levels

## 10. Trade-offs

### Cassandra vs PostgreSQL for Messages
**Chosen: Cassandra**
- Pros: High write throughput, linear scalability
- Cons: Limited query flexibility, eventual consistency
- Alternative: PostgreSQL with partitioning (ACID, complex queries)

### WebRTC vs Custom Protocol
**Chosen: WebRTC**
- Pros: Standard, built-in browser support, NAT traversal
- Cons: More complex, higher overhead
- Alternative: Custom UDP protocol (more control, browser limitations)

### Snowflake IDs vs UUID
**Chosen: Snowflake (Twitter-style)**
- Pros: Sortable, distributed generation, contains timestamp
- Cons: Predictable, reveals creation time
- Alternative: UUIDv4 (random, not sortable)

### Guild Sharding
**Chosen: Shard by guild_id**
- Pros: Even distribution, independent scaling
- Cons: Cross-guild operations complex
- Alternative: No sharding (simpler, doesn't scale)

## 11. Follow-up Questions

### Functional Enhancements
1. **How would you implement screen sharing?**
   - Use WebRTC screen capture API
   - Higher bitrate for screen vs video
   - Selective forwarding for large groups
   - Quality adaptation based on bandwidth

2. **How would you add Stage Channels?**
   - Separate audio mode (speakers vs audience)
   - Permission-based speaking rights
   - Raise hand queue
   - Lower bitrate for audience

3. **How would you implement bot commands?**
   - Webhook infrastructure
   - Rate limiting per bot
   - OAuth2 for bot authorization
   - Interaction handling (buttons, select menus)

### Scale & Performance
4. **How would you handle 1 billion users?**
   - More aggressive sharding (10,000+ shards)
   - Regional data centers
   - Separate voice and text infrastructure
   - Caching at multiple levels

5. **How would you optimize for mobile networks?**
   - Adaptive bitrate for voice
   - Delta compression for events
   - Background connection management
   - Push notifications for offline messages

6. **How would you reduce voice latency below 20ms?**
   - Edge voice servers closer to users
   - UDP optimization (reduce retransmissions)
   - Lower jitter buffer size
   - Direct peer-to-peer for small groups

### Reliability & Security
7. **How would you prevent voice attacks (flooding)?**
   - Rate limiting per user
   - Quality of service (QoS) prioritization
   - Automatic muting for abuse
   - Server-side audio validation

8. **How would you implement end-to-end encryption for voice?**
   - Use DTLS-SRTP (already encrypted in transit)
   - Additional E2E layer with shared keys
   - Key exchange during channel join
   - Trade-off: Cannot do server-side mixing

9. **How would you handle DDoS attacks?**
   - DDoS protection at edge (Cloudflare)
   - Rate limiting at API layer
   - Connection limits per IP
   - Automatic blacklisting

### Monitoring & Operations
10. **What metrics would you track?**
    - Message delivery latency (p50, p95, p99)
    - Voice quality (MOS score)
    - Packet loss rate
    - WebSocket connection count
    - Voice server CPU/bandwidth
    - API endpoint latency
    - Error rates

11. **How would you debug voice quality issues?**
    - Client-side quality metrics
    - Network path tracing
    - Packet capture analysis
    - Server-side audio analysis
    - Regional comparison

12. **How would you perform database migrations?**
    - Shadow traffic for testing
    - Dual-write during migration
    - Gradual cutover by shard
    - Rollback plan
    - Monitoring for anomalies
