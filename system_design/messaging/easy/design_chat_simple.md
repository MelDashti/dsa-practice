# Design a Basic 1-on-1 Chat System

## 1. Problem Overview

Design a simple chat application that allows two users to send and receive text messages in real-time. This is the foundation for more complex messaging systems and focuses on core messaging functionality without advanced features like group chats, media sharing, or encryption.

**Key Challenge**: Enable real-time message delivery between two users with minimal latency and high reliability.

## 2. Requirements

### Functional Requirements
- Users can send text messages to another user
- Users can receive messages in real-time
- Messages are stored persistently
- Users can view their chat history
- Users can see when messages are delivered
- Users can see when the other user is online/offline

### Non-Functional Requirements
- **Low latency**: Messages delivered in < 200ms
- **High availability**: 99.9% uptime
- **Consistency**: Messages delivered in order
- **Scalability**: Support 10M daily active users
- **Reliability**: No message loss

### Out of Scope
- Group chats
- Media sharing (images, videos, files)
- End-to-end encryption
- Message editing/deletion
- Voice/video calls
- Read receipts

## 3. Scale Estimation

### Traffic Estimates
- **Daily Active Users (DAU)**: 10M
- **Average messages per user per day**: 50
- **Total daily messages**: 500M
- **Messages per second**: 500M / 86400 ≈ 5,800 QPS (average)
- **Peak QPS**: 5,800 × 3 ≈ 17,400 QPS

### Storage Estimates
- **Average message size**: 100 bytes (text only)
- **Daily storage**: 500M × 100 bytes = 50 GB/day
- **Yearly storage**: 50 GB × 365 ≈ 18 TB/year
- **With replication (3x)**: 54 TB/year

### Bandwidth Estimates
- **Incoming**: 5,800 × 100 bytes = 580 KB/s (average)
- **Outgoing**: Similar to incoming
- **Peak bandwidth**: ~1.74 MB/s

## 4. High-Level Design

```
┌─────────┐                    ┌──────────────┐
│ User A  │◄──────WebSocket────┤              │
└─────────┘                    │              │
                               │   Gateway    │
┌─────────┐                    │   Server     │
│ User B  │◄──────WebSocket────┤              │
└─────────┘                    └──────┬───────┘
                                      │
                          ┌───────────┴────────────┐
                          │                        │
                    ┌─────▼──────┐        ┌───────▼────────┐
                    │  Message   │        │   Presence     │
                    │  Service   │        │   Service      │
                    └─────┬──────┘        └───────┬────────┘
                          │                       │
                    ┌─────▼──────┐        ┌───────▼────────┐
                    │  Message   │        │    Redis       │
                    │  Database  │        │   (Online)     │
                    └────────────┘        └────────────────┘
```

### Components
1. **Gateway Server**: Maintains WebSocket connections with clients
2. **Message Service**: Handles message sending, storage, and retrieval
3. **Presence Service**: Tracks user online/offline status
4. **Message Database**: Persistent storage for messages
5. **Redis Cache**: Stores online user status and temporary data

## 5. API Design

### WebSocket Events

#### Send Message
```json
{
  "event": "send_message",
  "data": {
    "recipient_id": "user_456",
    "message": "Hello!",
    "client_timestamp": 1699876543210
  }
}
```

#### Receive Message
```json
{
  "event": "receive_message",
  "data": {
    "message_id": "msg_789",
    "sender_id": "user_123",
    "message": "Hello!",
    "timestamp": 1699876543211,
    "status": "delivered"
  }
}
```

#### Delivery Acknowledgment
```json
{
  "event": "message_delivered",
  "data": {
    "message_id": "msg_789",
    "delivered_at": 1699876543212
  }
}
```

### REST APIs

#### Get Chat History
```
GET /api/v1/messages/{user_id}
Query Parameters:
  - before: timestamp (for pagination)
  - limit: integer (default: 50)

Response:
{
  "messages": [
    {
      "message_id": "msg_789",
      "sender_id": "user_123",
      "recipient_id": "user_456",
      "message": "Hello!",
      "timestamp": 1699876543211,
      "status": "delivered"
    }
  ],
  "has_more": true
}
```

#### Get User Status
```
GET /api/v1/users/{user_id}/status

Response:
{
  "user_id": "user_456",
  "status": "online",
  "last_seen": 1699876543000
}
```

## 6. Data Models

### Message Table
```sql
CREATE TABLE messages (
    message_id VARCHAR(64) PRIMARY KEY,
    sender_id VARCHAR(64) NOT NULL,
    recipient_id VARCHAR(64) NOT NULL,
    message TEXT NOT NULL,
    timestamp BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL, -- sent, delivered, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_sender_recipient_timestamp (sender_id, recipient_id, timestamp),
    INDEX idx_recipient_sender_timestamp (recipient_id, sender_id, timestamp)
);
```

### User Table
```sql
CREATE TABLE users (
    user_id VARCHAR(64) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen BIGINT
);
```

### Redis Schema
```
# Online user tracking
Key: user:online:{user_id}
Value: {
  "connection_id": "conn_abc123",
  "gateway_server": "gateway-01",
  "connected_at": 1699876543000
}
TTL: 5 minutes (renewed with heartbeat)

# User connections (for multiple devices)
Key: user:connections:{user_id}
Value: Set of connection_ids
```

## 7. Core Services Design

### Gateway Server
**Responsibilities**:
- Maintain WebSocket connections with clients
- Handle connection lifecycle (connect, disconnect, heartbeat)
- Route messages to Message Service
- Deliver messages to connected users

**Key Operations**:
```python
class GatewayServer:
    def on_connect(self, user_id, connection):
        # Store connection
        self.connections[user_id] = connection

        # Update presence
        self.presence_service.mark_online(user_id, self.server_id)

        # Send pending messages
        self.send_pending_messages(user_id)

    def on_message(self, user_id, message_data):
        # Validate and enrich message
        message = {
            "message_id": generate_id(),
            "sender_id": user_id,
            "recipient_id": message_data["recipient_id"],
            "message": message_data["message"],
            "timestamp": current_timestamp()
        }

        # Send to Message Service
        self.message_service.send_message(message)

    def deliver_message(self, recipient_id, message):
        # Check if user is connected to this gateway
        if recipient_id in self.connections:
            self.connections[recipient_id].send(message)
            return True
        return False
```

### Message Service
**Responsibilities**:
- Store messages persistently
- Handle message delivery logic
- Provide message history

**Key Operations**:
```python
class MessageService:
    def send_message(self, message):
        # Store message in database
        self.db.save_message(message)

        # Try to deliver to recipient
        recipient_status = self.presence_service.get_user_status(
            message["recipient_id"]
        )

        if recipient_status["online"]:
            # Find gateway server handling the recipient
            gateway_server = recipient_status["gateway_server"]

            # Send message to gateway
            self.send_to_gateway(gateway_server, message)

        # Send delivery confirmation to sender
        self.confirm_to_sender(message)

    def get_chat_history(self, user_id, other_user_id, before_ts, limit):
        return self.db.get_messages(
            user_id, other_user_id, before_ts, limit
        )
```

### Presence Service
**Responsibilities**:
- Track user online/offline status
- Maintain user-to-gateway mapping

**Key Operations**:
```python
class PresenceService:
    def mark_online(self, user_id, gateway_server):
        user_data = {
            "status": "online",
            "gateway_server": gateway_server,
            "last_seen": current_timestamp()
        }

        self.redis.setex(
            f"user:online:{user_id}",
            300,  # 5 minutes TTL
            json.dumps(user_data)
        )

    def mark_offline(self, user_id):
        self.redis.delete(f"user:online:{user_id}")

        # Update last_seen in database
        self.db.update_last_seen(user_id, current_timestamp())

    def get_user_status(self, user_id):
        data = self.redis.get(f"user:online:{user_id}")

        if data:
            return json.loads(data)
        else:
            last_seen = self.db.get_last_seen(user_id)
            return {"status": "offline", "last_seen": last_seen}
```

## 8. Real-time Communication (WebSockets)

### Why WebSockets?
- **Full-duplex communication**: Server can push messages to clients
- **Low latency**: Persistent connection eliminates handshake overhead
- **Efficient**: Less overhead than HTTP polling

### Connection Management
```
Client                    Gateway Server
  │                             │
  ├──── Connect ───────────────►│
  │                             ├─ Store connection
  │                             ├─ Mark user online
  │◄──── Connection ACK ────────┤
  │                             │
  │◄──── Heartbeat (ping) ──────┤
  ├──── Heartbeat (pong) ──────►│
  │                             │
  ├──── Send Message ──────────►│
  │                             ├─ Process message
  │◄──── Message ACK ───────────┤
  │                             │
  │◄──── Receive Message ───────┤ (from other user)
  ├──── Delivery ACK ──────────►│
  │                             │
```

### Handling Connection Failures
1. **Client disconnection**:
   - Mark user offline after grace period (30 seconds)
   - Store undelivered messages

2. **Gateway server failure**:
   - Clients reconnect to different gateway
   - Retrieve pending messages

3. **Network issues**:
   - Clients implement exponential backoff
   - Messages queued locally until reconnection

### Message Delivery Flow
```
Sender                Gateway-A         Message Service      Gateway-B         Recipient
  │                       │                    │                  │                │
  ├─ Send Message ───────►│                    │                  │                │
  │                       ├─ Forward ─────────►│                  │                │
  │                       │                    ├─ Store in DB     │                │
  │                       │                    ├─ Get recipient   │                │
  │                       │                    │   gateway        │                │
  │◄─── ACK ──────────────┤◄─── Confirm ───────┤                  │                │
  │                       │                    ├─ Forward ───────►│                │
  │                       │                    │                  ├─ Deliver ─────►│
  │                       │                    │◄─── Delivered ───┤◄─── ACK ───────┤
  │◄─ Delivered ──────────┤◄─── Notify ────────┤                  │                │
```

## 9. Scalability & Performance

### Horizontal Scaling
- **Gateway Servers**: Scale by adding more servers behind load balancer
- **Message Service**: Stateless, can scale horizontally
- **Database**: Shard by user_id (partition key)

### Database Optimization
- **Indexing**: Create composite indexes on (sender_id, recipient_id, timestamp)
- **Partitioning**: Partition by conversation_id or time range
- **Archiving**: Move old messages (>1 year) to cold storage

### Caching Strategy
- **Recent messages**: Cache last 50 messages per conversation in Redis
- **User status**: Always cached in Redis with TTL
- **User profiles**: Cache frequently accessed profiles

### Load Balancing
- **Sticky sessions**: Route same user to same gateway when possible
- **Consistent hashing**: Distribute users evenly across gateways
- **Health checks**: Remove unhealthy gateways from rotation

## 10. Trade-offs

### WebSocket vs HTTP Polling
**Chosen: WebSocket**
- Pros: Lower latency, efficient, real-time
- Cons: More complex, harder to scale
- Alternative: HTTP long polling (simpler but higher latency)

### Message Storage
**Chosen: Relational Database (PostgreSQL)**
- Pros: ACID guarantees, strong consistency, good for ordered queries
- Cons: Harder to scale horizontally
- Alternative: NoSQL (Cassandra) for better scalability, eventual consistency

### Single vs Multi-region Deployment
**Chosen: Single region (for simplicity)**
- Pros: Simpler, consistent, lower latency within region
- Cons: Higher latency for distant users
- Alternative: Multi-region with data replication

### Message Ordering
**Chosen: Server timestamp**
- Pros: Prevents client time sync issues
- Cons: Small clock skew between servers
- Alternative: Lamport timestamps or vector clocks

## 11. Follow-up Questions

### Functional Extensions
1. **How would you add group chat functionality?**
   - Create conversation/group table
   - Store group membership
   - Fan-out messages to all group members
   - Handle member joins/leaves

2. **How would you support message editing and deletion?**
   - Add soft delete flag
   - Store message edit history
   - Send edit/delete events to all participants

3. **How would you implement read receipts?**
   - Track last_read_message_id per user per conversation
   - Send read event when user views messages
   - Update UI to show read status

### Scale & Performance
4. **How would you handle 1 billion users?**
   - Implement database sharding by user_id
   - Use consistent hashing for gateway routing
   - Deploy across multiple regions
   - Use CDN for static assets

5. **How would you optimize for very high message volume?**
   - Use message queue (Kafka) for async processing
   - Batch message writes to database
   - Implement write-through cache
   - Use SSD storage for hot data

6. **How would you reduce latency for global users?**
   - Multi-region deployment
   - Edge servers closer to users
   - Message routing optimization
   - CDN for media content

### Reliability & Security
7. **How would you ensure no message loss?**
   - Implement at-least-once delivery with idempotency
   - Use message queue for durability
   - Client-side retry with exponential backoff
   - Store-and-forward pattern

8. **How would you handle message encryption?**
   - End-to-end encryption (E2EE) using Signal protocol
   - Store only encrypted messages
   - Key exchange during connection setup
   - Perfect forward secrecy

9. **How would you detect and prevent spam?**
   - Rate limiting per user
   - ML-based spam detection
   - User reporting and blocking
   - Message content filtering

### Monitoring & Operations
10. **What metrics would you track?**
    - Message delivery latency (p50, p99)
    - WebSocket connection count
    - Message delivery success rate
    - Gateway server load
    - Database query performance
    - Error rates by type

11. **How would you handle schema migrations with zero downtime?**
    - Blue-green deployment
    - Backward-compatible schema changes
    - Feature flags for new columns
    - Gradual rollout

12. **How would you debug message delivery issues?**
    - Distributed tracing (message_id tracking)
    - Centralized logging
    - Message delivery timeline
    - Connection state monitoring
