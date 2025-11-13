# Design Facebook Messenger

## 1. Problem Overview

Design a cross-platform messaging application like Facebook Messenger that supports messaging, voice/video calls, stories, payments, games, and bots across web, mobile, and desktop with seamless integration into the Facebook ecosystem. The system must handle billions of users with complex features while maintaining high performance and reliability.

**Key Challenges**:
- Multi-platform synchronization (web, iOS, Android, desktop)
- Integration with Facebook social graph
- Voice and video calling infrastructure
- Stories with 24-hour expiry
- In-app payments and marketplace
- Bot platform and business messaging
- Multi-region deployment with data residency
- Advanced AI features (smart replies, translations)

## 2. Requirements

### Functional Requirements
- **Messaging**: 1-on-1 and group chats (up to 250 members)
- **Media Sharing**: Photos, videos, documents, audio, GIFs, stickers
- **Voice/Video Calls**: High-quality calls for individuals and groups
- **Stories**: 24-hour ephemeral content sharing
- **Reactions & Mentions**: Quick reactions, @mentions
- **Message Forwarding**: Forward messages across conversations
- **Secret Conversations**: End-to-end encrypted chats
- **Payments**: Peer-to-peer money transfer
- **Chatbots**: Automated customer service and interactions
- **Games**: In-chat casual games
- **Message Search**: Full-text search across conversations
- **Active Status**: Real-time online/offline indicators
- **Cross-Platform Sync**: Seamless experience across devices
- **Watch Together**: Synchronized video watching

### Non-Functional Requirements
- **Availability**: 99.99% uptime
- **Latency**: < 100ms message delivery, < 200ms for global
- **Scalability**: 3B users, 1.3B DAU, 100B messages/day
- **Consistency**: Message ordering, exactly-once delivery
- **Storage**: Unlimited message history
- **Security**: E2E encryption for secret chats, secure payments
- **Compliance**: GDPR, data residency requirements
- **Performance**: Support 100M concurrent connections

### Out of Scope
- Facebook feed integration
- Instagram Direct integration details
- Advanced business tools (Ads Manager)
- WhatsApp Business integration

## 3. Scale Estimation

### Traffic Estimates
- **Total Users**: 3 billion
- **Daily Active Users (DAU)**: 1.3 billion (43%)
- **Monthly Active Users (MAU)**: 2 billion
- **Average messages per user per day**: 80
- **Total daily messages**: 104 billion
- **Messages per second**: 1.2M QPS (average)
- **Peak QPS**: 3.6M (3x average)
- **Video calls**: 100M daily
- **Voice calls**: 200M daily
- **Stories posted**: 500M daily

### Storage Estimates
- **Text message**: 500 bytes (with metadata)
- **Daily text storage**: 80B × 500 bytes = 40 TB/day
- **Yearly text storage**: 14.6 PB/year
- **Media**: 40% of messages = 40B/day × 2 MB (avg) = 80 PB/day
- **Yearly media storage**: ~29 EB (with compression and deduplication: ~10 EB)
- **Stories**: 500M × 5 MB = 2.5 PB/day (deleted after 24h)

### Bandwidth Estimates
- **Incoming messages**: 1.2M QPS × 500 bytes = 600 MB/s
- **Media uploads**: 40B / 86400 × 2 MB ≈ 925 GB/s
- **Total incoming**: ~925 GB/s
- **Outgoing**: Higher due to fanout = ~2.8 TB/s
- **Video calling**: 100M concurrent × 2 Mbps = 200 Tbps

### Infrastructure Estimates
- **Gateway servers**: 100K servers (10K connections each)
- **Application servers**: 50K servers
- **Database servers**: 10K shards
- **Media storage**: 50 EB capacity
- **Cache servers**: 20K Redis instances

## 4. High-Level Design

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Client Applications                               │
│     (iOS, Android, Web, Desktop, Portal, VR, Smart Displays)             │
└────────────────────┬────────────────────────────────┬────────────────────┘
                     │                                │
          ┌──────────┴──────────┐          ┌─────────┴──────────┐
          │   Edge Network      │          │   Media CDN        │
          │  (PoPs worldwide)   │          │  (Photos/Videos)   │
          └──────────┬──────────┘          └────────────────────┘
                     │
          ┌──────────┴──────────────────────┐
          │   Global Load Balancer          │
          │  (Geographic routing)           │
          └──────────┬──────────────────────┘
                     │
     ┌───────────────┼───────────────┬───────────────────┐
     │               │               │                   │
     ▼               ▼               ▼                   ▼
┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────────────┐
│ Gateway  │  │    API    │  │   Call     │  │    Stories       │
│ Service  │  │  Gateway  │  │  Gateway   │  │    Service       │
│(WebSocket)│  │   (HTTP)  │  │  (WebRTC)  │  │                  │
└─────┬────┘  └─────┬─────┘  └─────┬──────┘  └────────┬─────────┘
      │             │               │                  │
      └─────────────┴───────────────┴──────────────────┘
                          │
         ┌────────────────┼────────────────────────────────┐
         │                │                                │
         ▼                ▼                                ▼
┌────────────────┐ ┌──────────────┐             ┌─────────────────┐
│   Message      │ │  Social Graph│             │   AI Services   │
│   Router       │ │   Service    │             │ (ML, Translation)│
└───────┬────────┘ └──────────────┘             └─────────────────┘
        │
        ├──────────┬──────────┬──────────┬──────────┬──────────────┐
        ▼          ▼          ▼          ▼          ▼              ▼
┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│ Message │ │  Group   │ │Payment │ │  Bot   │ │ Stories │ │  Presence│
│ Service │ │ Service  │ │Service │ │Platform│ │ Service │ │  Service │
└────┬────┘ └────┬─────┘ └───┬────┘ └───┬────┘ └────┬────┘ └────┬─────┘
     │           │            │          │           │           │
     └───────────┴────────────┴──────────┴───────────┴───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐      ┌─────────────┐      ┌─────────────┐
│   MySQL       │      │  Cassandra  │      │    Redis    │
│   Cluster     │      │   Cluster   │      │   Cluster   │
│ (Metadata)    │      │  (Messages) │      │   (Cache)   │
└───────────────┘      └─────────────┘      └─────────────┘
        │
        ▼
┌───────────────────────┐
│    Object Storage     │
│   (Photos, Videos)    │
└───────────────────────┘
```

## 5. API Design

### WebSocket Events

#### Message Event
```json
{
  "type": "message",
  "data": {
    "message_id": "mid.$cAAJQ7M...",
    "thread_id": "t_123456789",
    "sender": {
      "id": "user_123",
      "name": "John Doe",
      "profile_pic": "https://..."
    },
    "text": "Hello!",
    "attachments": [],
    "timestamp": 1699876543000,
    "is_forwarded": false,
    "replied_to": null
  }
}
```

#### Typing Indicator
```json
{
  "type": "typing",
  "data": {
    "thread_id": "t_123456789",
    "user_id": "user_456",
    "is_typing": true
  }
}
```

#### Delivery Receipt
```json
{
  "type": "delivery",
  "data": {
    "message_id": "mid.$cAAJQ7M...",
    "user_id": "user_456",
    "status": "delivered",
    "timestamp": 1699876544000
  }
}
```

#### Story Update
```json
{
  "type": "story_update",
  "data": {
    "user_id": "user_123",
    "story_id": "story_789",
    "action": "added",  // added, viewed, deleted
    "timestamp": 1699876543000
  }
}
```

### REST APIs

#### Send Message
```
POST /v1/messages
{
  "recipient_id": "user_456",  // or thread_id
  "text": "Hello!",
  "attachments": [
    {
      "type": "image",
      "url": "https://...",
      "width": 1920,
      "height": 1080
    }
  ],
  "reply_to_message_id": null,
  "is_forwarded": false
}

Response:
{
  "message_id": "mid.$cAAJQ7M...",
  "thread_id": "t_123456789",
  "timestamp": 1699876543000,
  "status": "sent"
}
```

#### Get Conversations
```
GET /v1/conversations
Query Parameters:
  - limit: 20
  - before: timestamp
  - filter: unread, groups, archived

Response:
{
  "conversations": [
    {
      "thread_id": "t_123456789",
      "participants": [
        {"id": "user_123", "name": "John"},
        {"id": "user_456", "name": "Jane"}
      ],
      "last_message": {
        "text": "See you tomorrow",
        "timestamp": 1699876543000,
        "sender_id": "user_456"
      },
      "unread_count": 3,
      "muted": false,
      "archived": false
    }
  ],
  "paging": {
    "next": "..."
  }
}
```

#### Get Message History
```
GET /v1/threads/{thread_id}/messages
Query Parameters:
  - limit: 50
  - before: message_id
  - after: message_id

Response:
{
  "messages": [...],
  "participants": [...],
  "paging": {...}
}
```

#### Initiate Call
```
POST /v1/calls
{
  "recipient_id": "user_456",
  "call_type": "video"  // audio, video
}

Response:
{
  "call_id": "call_abc123",
  "token": "rtc_token_xyz...",
  "ice_servers": [
    {
      "urls": "stun:stun.messenger.com:3478"
    },
    {
      "urls": "turn:turn.messenger.com:3478",
      "username": "...",
      "credential": "..."
    }
  ]
}
```

#### Post Story
```
POST /v1/stories
{
  "media_url": "https://...",
  "media_type": "image",  // image, video
  "duration": 5,  // seconds
  "privacy": "friends",  // friends, custom, public
  "allowed_viewers": []
}

Response:
{
  "story_id": "story_789",
  "expires_at": 1699962943000,
  "view_count": 0
}
```

#### Send Payment
```
POST /v1/payments
{
  "recipient_id": "user_456",
  "amount": 25.00,
  "currency": "USD",
  "note": "Lunch yesterday",
  "payment_method_id": "pm_abc123"
}

Response:
{
  "payment_id": "pay_xyz789",
  "status": "pending",
  "created_at": 1699876543000
}
```

#### Search Messages
```
GET /v1/search
Query Parameters:
  - query: "dinner plans"
  - thread_id: optional
  - from_user: optional
  - limit: 20

Response:
{
  "results": [
    {
      "message": {...},
      "thread": {...},
      "highlights": ["<em>dinner plans</em> for Friday"],
      "score": 0.95
    }
  ],
  "total_count": 156
}
```

## 6. Data Models

### User Table (MySQL - Sharded)
```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    facebook_id BIGINT UNIQUE,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    display_name VARCHAR(100),
    profile_picture_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_facebook_id ON users(facebook_id);
CREATE INDEX idx_phone ON users(phone_number);
```

### Thread Table (MySQL - Sharded)
```sql
CREATE TABLE threads (
    thread_id BIGINT PRIMARY KEY,
    thread_type VARCHAR(20), -- ONE_TO_ONE, GROUP, SECRET
    name VARCHAR(100),  -- For group chats
    image_url TEXT,
    created_by BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_id VARCHAR(100),
    last_message_timestamp BIGINT,
    message_count BIGINT DEFAULT 0
);

CREATE INDEX idx_last_message ON threads(last_message_timestamp DESC);
```

### Thread Participants Table (MySQL - Sharded)
```sql
CREATE TABLE thread_participants (
    thread_id BIGINT,
    user_id BIGINT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    left_at TIMESTAMP,
    role VARCHAR(20) DEFAULT 'member',  -- admin, member
    muted BOOLEAN DEFAULT false,
    archived BOOLEAN DEFAULT false,
    last_read_message_id VARCHAR(100),
    last_read_timestamp BIGINT,

    PRIMARY KEY (thread_id, user_id)
);

CREATE INDEX idx_user_threads ON thread_participants(user_id, last_read_timestamp DESC);
```

### Message Table (Cassandra)
```cql
CREATE TABLE messages (
    thread_id BIGINT,
    message_id TEXT,
    sender_id BIGINT,
    text TEXT,
    timestamp BIGINT,
    message_type VARCHAR(20), -- text, media, payment, game, system
    attachments LIST<TEXT>,  -- JSON serialized
    replied_to_message_id TEXT,
    forwarded_from_message_id TEXT,
    deleted_at BIGINT,
    edited_at BIGINT,

    PRIMARY KEY (thread_id, timestamp, message_id)
) WITH CLUSTERING ORDER BY (timestamp DESC, message_id DESC);

CREATE INDEX idx_sender ON messages(sender_id);
```

### Message Status Table (Cassandra)
```cql
CREATE TABLE message_status (
    message_id TEXT,
    user_id BIGINT,
    status VARCHAR(20),  -- sent, delivered, read
    timestamp BIGINT,

    PRIMARY KEY (message_id, user_id)
);
```

### Story Table (Cassandra)
```cql
CREATE TABLE stories (
    user_id BIGINT,
    story_id TEXT,
    media_url TEXT,
    media_type VARCHAR(20),
    duration INT,
    created_at BIGINT,
    expires_at BIGINT,
    view_count INT,
    viewers LIST<BIGINT>,

    PRIMARY KEY (user_id, created_at, story_id)
) WITH CLUSTERING ORDER BY (created_at DESC)
     AND default_time_to_live = 86400;  -- 24 hours
```

### Call Table (MySQL)
```sql
CREATE TABLE calls (
    call_id VARCHAR(64) PRIMARY KEY,
    thread_id BIGINT,
    initiator_id BIGINT,
    call_type VARCHAR(20),  -- audio, video
    status VARCHAR(20),  -- ringing, active, ended, missed
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    duration INT,  -- seconds
    participants JSONB
);

CREATE INDEX idx_thread_calls ON calls(thread_id, started_at DESC);
```

### Payment Table (MySQL - Separate DB)
```sql
CREATE TABLE payments (
    payment_id VARCHAR(64) PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    recipient_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- pending, completed, failed, refunded
    payment_method_id VARCHAR(64),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    thread_id BIGINT,
    message_id VARCHAR(100)
);

CREATE INDEX idx_sender ON payments(sender_id, created_at DESC);
CREATE INDEX idx_recipient ON payments(recipient_id, created_at DESC);
```

### Redis Schemas

#### Online Presence
```
Key: presence:{user_id}
Value: {
  "status": "active",  // active, idle, offline
  "last_active": 1699876543000,
  "platforms": ["ios", "web"],
  "current_thread": "t_123456789"
}
TTL: 5 minutes
```

#### Active Connections
```
Key: connections:{user_id}
Value: Set of {
  "connection_id": "conn_abc",
  "platform": "ios",
  "gateway_server": "gw-us-east-1"
}
```

#### Unread Counts
```
Key: unread:{user_id}
Value: Hash {
  "t_123456789": "5",
  "t_987654321": "12",
  "_total": "17"
}
```

#### Story View Cache
```
Key: story:{story_id}:viewers
Value: Set of user_ids
TTL: 24 hours
```

## 7. Core Services Design

### Message Service
```python
class MessageService:
    def send_message(self, sender_id, recipient_id, message_data):
        # Get or create thread
        thread = self.get_or_create_thread(sender_id, recipient_id)

        # Generate message ID (snowflake)
        message_id = self.generate_message_id()

        message = {
            "message_id": message_id,
            "thread_id": thread.id,
            "sender_id": sender_id,
            "text": message_data.get("text"),
            "timestamp": current_timestamp_ms(),
            "attachments": message_data.get("attachments", []),
            "replied_to": message_data.get("reply_to_message_id")
        }

        # Store in Cassandra
        self.cassandra.insert_message(message)

        # Update thread metadata
        self.update_thread_last_message(thread.id, message)

        # Get recipient's devices
        recipients = self.thread_service.get_thread_participants(thread.id)
        recipients.remove(sender_id)

        # Send to online recipients
        for recipient_id in recipients:
            devices = self.presence_service.get_user_devices(recipient_id)

            if devices:
                for device in devices:
                    self.gateway_service.send_to_device(device, {
                        "type": "message",
                        "data": message
                    })
            else:
                # Send push notification
                self.push_service.send_notification(
                    recipient_id,
                    f"{self.get_user_name(sender_id)}: {message['text']}"
                )

            # Update unread count
            self.redis.hincrby(f"unread:{recipient_id}", thread.id, 1)
            self.redis.hincrby(f"unread:{recipient_id}", "_total", 1)

        # AI processing (async)
        self.ai_service.process_message_async(message)

        return message

    def get_or_create_thread(self, user1_id, user2_id):
        # Check if thread exists
        thread = self.db.query("""
            SELECT t.*
            FROM threads t
            JOIN thread_participants tp1 ON t.thread_id = tp1.thread_id
            JOIN thread_participants tp2 ON t.thread_id = tp2.thread_id
            WHERE tp1.user_id = ? AND tp2.user_id = ?
              AND t.thread_type = 'ONE_TO_ONE'
            LIMIT 1
        """, (user1_id, user2_id))

        if thread:
            return thread

        # Create new thread
        thread_id = self.generate_thread_id()
        thread = {
            "thread_id": thread_id,
            "thread_type": "ONE_TO_ONE",
            "created_by": user1_id
        }

        self.db.insert_thread(thread)

        # Add participants
        self.add_participant(thread_id, user1_id)
        self.add_participant(thread_id, user2_id)

        return thread
```

### Stories Service
```python
class StoriesService:
    def post_story(self, user_id, media_url, media_type, privacy, options):
        story_id = self.generate_story_id()

        story = {
            "story_id": story_id,
            "user_id": user_id,
            "media_url": media_url,
            "media_type": media_type,
            "duration": options.get("duration", 5),
            "created_at": current_timestamp_ms(),
            "expires_at": current_timestamp_ms() + 86400000,  # 24 hours
            "view_count": 0,
            "viewers": [],
            "privacy": privacy,
            "allowed_viewers": options.get("allowed_viewers", [])
        }

        # Store in Cassandra (with 24h TTL)
        self.cassandra.insert_story(story)

        # Get friends based on privacy settings
        if privacy == "friends":
            friends = self.social_graph.get_friends(user_id)
        elif privacy == "custom":
            friends = story["allowed_viewers"]
        else:
            friends = []

        # Notify friends
        for friend_id in friends:
            self.notification_service.send_story_notification(
                friend_id,
                user_id,
                story_id
            )

        # Schedule deletion
        self.scheduler.schedule_deletion(story_id, expires_at=story["expires_at"])

        return story

    def view_story(self, story_id, viewer_id):
        # Check if already viewed
        if self.redis.sismember(f"story:{story_id}:viewers", viewer_id):
            return

        # Add to viewers
        self.redis.sadd(f"story:{story_id}:viewers", viewer_id)

        # Update Cassandra (async)
        self.queue.publish("story_views", {
            "story_id": story_id,
            "viewer_id": viewer_id,
            "viewed_at": current_timestamp_ms()
        })

        # Notify story owner
        story = self.get_story(story_id)
        self.notification_service.send_story_view(
            story["user_id"],
            viewer_id
        )

    def get_active_stories(self, user_id):
        # Get friends
        friends = self.social_graph.get_friends(user_id)

        # Get stories from friends (last 24 hours)
        stories = []
        for friend_id in friends:
            friend_stories = self.cassandra.query("""
                SELECT * FROM stories
                WHERE user_id = ?
                  AND created_at > ?
            """, (friend_id, current_timestamp_ms() - 86400000))

            if friend_stories:
                # Check viewer list
                for story in friend_stories:
                    story["viewed_by_me"] = self.redis.sismember(
                        f"story:{story['story_id']}:viewers",
                        user_id
                    )
                stories.extend(friend_stories)

        return sorted(stories, key=lambda x: x["created_at"], reverse=True)
```

### Payment Service
```python
class PaymentService:
    def send_payment(self, sender_id, recipient_id, amount, currency, note):
        # Validate payment method
        payment_method = self.get_user_payment_method(sender_id)
        if not payment_method:
            raise NoPaymentMethodError()

        # Create payment record
        payment_id = self.generate_payment_id()

        payment = {
            "payment_id": payment_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "amount": amount,
            "currency": currency,
            "status": "pending",
            "note": note,
            "payment_method_id": payment_method.id
        }

        # Store in database
        self.db.insert_payment(payment)

        # Process payment (async)
        self.payment_processor.charge(
            payment_method.id,
            amount,
            currency,
            metadata={"payment_id": payment_id}
        )

        # Send as message
        thread = self.message_service.get_or_create_thread(
            sender_id,
            recipient_id
        )

        self.message_service.send_message(sender_id, recipient_id, {
            "text": note,
            "message_type": "payment",
            "attachments": [{
                "type": "payment",
                "payment_id": payment_id,
                "amount": amount,
                "currency": currency
            }]
        })

        return payment

    def handle_payment_webhook(self, event):
        # Payment processor webhook
        if event.type == "charge.succeeded":
            payment_id = event.metadata["payment_id"]

            # Update payment status
            self.db.execute("""
                UPDATE payments
                SET status = 'completed',
                    completed_at = NOW()
                WHERE payment_id = ?
            """, (payment_id,))

            # Notify sender and recipient
            payment = self.get_payment(payment_id)
            self.notification_service.send_payment_notification(
                payment["recipient_id"],
                payment
            )
```

### AI Service
```python
class AIService:
    def process_message_async(self, message):
        # Queue for async processing
        self.queue.publish("ai_processing", message)

    def process_message(self, message):
        # Generate smart replies
        smart_replies = self.generate_smart_replies(message["text"])

        # Store in cache for quick access
        self.redis.setex(
            f"smart_replies:{message['message_id']}",
            300,  # 5 minutes
            json.dumps(smart_replies)
        )

        # Translate if needed
        if self.should_translate(message):
            translations = self.translate_message(message)
            self.redis.setex(
                f"translations:{message['message_id']}",
                3600,
                json.dumps(translations)
            )

        # Content moderation
        if self.is_inappropriate(message["text"]):
            self.moderation_service.flag_message(message)

    def generate_smart_replies(self, text):
        # Use ML model to generate contextual replies
        replies = self.ml_model.predict(text, num_replies=3)
        return replies
```

## 8. Real-time Communication (WebSockets)

### Multi-Region Gateway Architecture
```
      Region: US-East           Region: EU-West           Region: Asia-Pacific
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐
│  Gateway Cluster       │  │  Gateway Cluster       │  │  Gateway Cluster       │
│  ┌──────────────────┐  │  │  ┌──────────────────┐  │  │  ┌──────────────────┐  │
│  │  Gateway Servers │  │  │  │  Gateway Servers │  │  │  │  Gateway Servers │  │
│  │  (10K servers)   │  │  │  │  (8K servers)    │  │  │  │  (12K servers)   │  │
│  └──────────────────┘  │  │  └──────────────────┘  │  │  └──────────────────┘  │
│          │             │  │          │             │  │          │             │
│          ▼             │  │          ▼             │  │          ▼             │
│  ┌──────────────────┐  │  │  ┌──────────────────┐  │  │  ┌──────────────────┐  │
│  │ Message Router   │  │  │  │ Message Router   │  │  │  │ Message Router   │  │
│  └──────────────────┘  │  │  └──────────────────┘  │  │  └──────────────────┘  │
└────────────────────────┘  └────────────────────────┘  └────────────────────────┘
            │                          │                          │
            └──────────────────────────┴──────────────────────────┘
                                       │
                            ┌──────────▼──────────┐
                            │  Global Message Bus │
                            │    (Kafka/Pulsar)   │
                            └─────────────────────┘
```

### Cross-Region Message Delivery
```
User A (US) → Gateway (US) → Router (US) → Kafka → Router (EU) → Gateway (EU) → User B (EU)
   100ms           10ms          20ms        50ms      20ms          10ms          100ms
                            Total: ~310ms (acceptable for global)
```

## 9. Geospatial Indexing

While Messenger is primarily a messaging platform, it does use location for:
- Nearby Friends feature
- Location sharing in chats
- Business discovery

### Location Sharing
```python
class LocationService:
    def share_location(self, user_id, thread_id, lat, lon):
        # Create location message
        location_data = {
            "type": "location",
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            },
            "address": self.geocode(lat, lon),
            "timestamp": current_timestamp_ms()
        }

        # Send as message attachment
        self.message_service.send_message(user_id, thread_id, {
            "text": "Shared a location",
            "attachments": [location_data]
        })

        # Store in geospatial index (if Nearby Friends enabled)
        if self.is_nearby_friends_enabled(user_id):
            self.update_user_location(user_id, lat, lon)

    def update_user_location(self, user_id, lat, lon):
        # Store in Redis with geospatial index
        self.redis.geoadd(
            "user_locations",
            lon, lat, user_id
        )

        # Set expiry
        self.redis.expire(f"user_location:{user_id}", 3600)

    def get_nearby_friends(self, user_id, radius_km):
        # Get user's location
        location = self.redis.geopos("user_locations", user_id)

        if not location:
            return []

        # Find nearby users
        nearby = self.redis.georadius(
            "user_locations",
            location[0], location[1],
            radius_km, "km",
            withdist=True
        )

        # Filter to friends only
        friends = self.social_graph.get_friends(user_id)
        nearby_friends = [
            u for u in nearby if u["user_id"] in friends
        ]

        return nearby_friends
```

## 10. Scalability & Performance

### Database Sharding
- **User sharding**: Shard by user_id (consistent hashing)
- **Thread sharding**: Shard by thread_id
- **Geographic sharding**: Shard by region for compliance
- **Hot shard mitigation**: Detect and split hot shards

### Cassandra for Messages
- **Partition key**: thread_id
- **Clustering key**: timestamp, message_id
- **Replication factor**: 3
- **Consistency level**: QUORUM for writes, ONE for reads
- **Compaction**: Time-window compaction strategy

### Caching Strategy
```
L1: Application cache (in-memory, per server)
- User profiles: 10 minutes
- Thread metadata: 10 minutes

L2: Redis cluster (distributed)
- Recent messages: 50 per thread
- Online presence: 5 minutes
- Unread counts: Real-time
- Smart replies: 5 minutes

L3: Database (source of truth)
```

### CDN for Media
- **Global CDN**: CloudFront, Akamai
- **Origin**: S3 with regional replication
- **Optimization**: WebP/AVIF for images, adaptive bitrate for videos
- **Caching**: Aggressive edge caching (1 year TTL)

### Load Balancing
- **DNS-based**: Route to nearest region
- **Gateway load balancing**: Consistent hashing by user_id
- **Health checks**: Remove unhealthy instances
- **Gradual rollout**: Canary deployments

## 11. Trade-offs

### MySQL vs Cassandra for Messages
**Chosen: Cassandra**
- Pros: High write throughput, time-series optimized, linear scaling
- Cons: Eventual consistency, complex operations, operational overhead
- Alternative: MySQL with sharding (ACID, familiar, harder to scale)

### Multi-Region Active-Active
**Chosen: Multi-region active-active**
- Pros: Lower latency globally, better availability
- Cons: Complex conflict resolution, higher costs
- Alternative: Single region (simpler, higher latency)

### Stories Storage
**Chosen: Cassandra with TTL**
- Pros: Automatic expiry, distributed, scalable
- Cons: Cannot guarantee exact 24h deletion
- Alternative: Separate ephemeral storage (more complex)

### E2E Encryption for All Messages
**Chosen: Optional (Secret Conversations)**
- Pros: Supports AI features, search, multi-device
- Cons: Less privacy than full E2E
- Alternative: Full E2E like WhatsApp (limits features)

## 12. Follow-up Questions

### Functional Enhancements
1. **How would you implement message reactions?**
   - Store reactions in separate Cassandra table
   - Aggregate on read
   - Real-time updates via WebSocket
   - Cache popular reactions

2. **How would you add Instagram Direct integration?**
   - Shared thread infrastructure
   - Unified message format
   - Cross-platform user mapping
   - Separate UI/UX, shared backend

3. **How would you implement watch together?**
   - WebRTC for synchronization
   - Shared playback state
   - Video streaming service integration
   - Pause/play/seek coordination

### Scale & Performance
4. **How would you handle 10B messages/day?**
   - More Cassandra nodes (horizontal scaling)
   - Additional regional clusters
   - Aggressive caching
   - Message batching

5. **How would you reduce global message latency?**
   - More regional data centers
   - Edge computing for routing
   - Optimized network paths
   - Protocol optimization (QUIC)

6. **How would you optimize for low-bandwidth networks?**
   - Message compression
   - Delta sync
   - Image quality reduction
   - Background sync

### Reliability & Security
7. **How would you ensure GDPR compliance?**
   - Data residency (EU data in EU)
   - Right to deletion
   - Data portability
   - Consent management
   - Audit logs

8. **How would you prevent payment fraud?**
   - ML-based fraud detection
   - Multi-factor authentication
   - Transaction limits
   - Velocity checks
   - Manual review for high-risk

9. **How would you handle message encryption for groups?**
   - Sender keys protocol
   - Key rotation on membership changes
   - Pairwise keys for small groups
   - Trade-off: Complexity vs security

### Monitoring & Operations
10. **What metrics would you track?**
    - Message delivery latency (p50, p95, p99)
    - Message delivery success rate
    - Call quality (MOS, packet loss)
    - Active connections per gateway
    - Database query latency
    - Cache hit rate
    - Payment success rate
    - Story view rates

11. **How would you handle data center failure?**
    - Multi-region redundancy
    - Automatic failover
    - Regional read replicas
    - Degraded mode operation
    - Data replication lag monitoring

12. **How would you test at scale?**
    - Load testing in production (shadow traffic)
    - Chaos engineering
    - Gradual rollout (1%, 10%, 50%, 100%)
    - Feature flags
    - Canary deployments
    - A/B testing framework
