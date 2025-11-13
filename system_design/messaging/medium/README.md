# Medium - Messaging Systems

This directory contains intermediate-level messaging system design problems that build upon foundational concepts and introduce advanced features like encryption, group messaging, voice/video, and complex architectures.

## Problems

### 1. WhatsApp (`design_whatsapp.md`)
Design a mobile messaging platform with end-to-end encryption, group chats, and media sharing.

**Key Concepts**:
- End-to-end encryption (Signal Protocol)
- Group message fanout
- Multi-device synchronization
- Media storage and CDN
- Message status tracking (sent, delivered, read)

**Complexity Additions**:
- Security and encryption at scale
- Cross-device message sync
- Large media file handling
- Efficient group messaging

### 2. Slack (`design_slack.md`)
Design a team collaboration platform with workspaces, channels, threads, and powerful search.

**Key Concepts**:
- Workspace and channel organization
- Threaded conversations
- Full-text search (Elasticsearch)
- File sharing and indexing
- Integration platform (webhooks, bots)
- Rich message formatting

**Complexity Additions**:
- Multi-tenancy (workspaces)
- Search at scale
- Permission systems
- Thread management

### 3. Discord (`design_discord.md`)
Design a communication platform with text, voice, and video optimized for gaming communities.

**Key Concepts**:
- Server-based organization
- Real-time voice channels (WebRTC)
- Low-latency messaging
- Rich presence system
- Role-based permissions
- Voice server infrastructure

**Complexity Additions**:
- Voice and video at scale
- WebRTC media servers
- Regional voice routing
- Gaming activity tracking

## Common Patterns in Medium Messaging Problems

### Advanced Communication
- **WebRTC**: Peer-to-peer voice/video
- **Media Servers**: Mixing and forwarding audio/video
- **Adaptive Bitrate**: Quality adjustment based on bandwidth
- **End-to-End Encryption**: Signal Protocol, DTLS-SRTP

### Organization & Structure
- **Multi-tenancy**: Isolated workspaces/servers
- **Hierarchical Channels**: Categories and channels
- **Threads**: Nested conversations
- **Roles & Permissions**: Fine-grained access control

### Search & Discovery
- **Elasticsearch**: Full-text search across messages
- **Indexing Strategy**: Async indexing, sharding
- **Relevance Ranking**: Boost fields, filters
- **Search Permissions**: Filter by user access

### Media Handling
- **S3/Blob Storage**: Scalable file storage
- **CDN**: Fast global content delivery
- **Thumbnail Generation**: Async processing
- **Signed URLs**: Temporary secure access

### Scalability Patterns
- **Database Sharding**: By workspace/server/conversation
- **Cassandra for Messages**: High write throughput
- **Redis Pub/Sub**: Event broadcasting
- **Message Queues**: Async processing (Kafka, RabbitMQ)

## Architectural Comparison

| Feature | WhatsApp | Slack | Discord |
|---------|----------|-------|---------|
| **Organization** | Individual users | Workspaces | Servers (Guilds) |
| **Primary Use** | Personal messaging | Work collaboration | Gaming communities |
| **Encryption** | E2E (Signal) | In-transit | In-transit |
| **Voice/Video** | Calls (separate) | Huddles | Built-in channels |
| **Search** | Client-side only | Full-text (server) | Full-text (server) |
| **Message DB** | Cassandra | PostgreSQL | Cassandra |
| **Scale Focus** | Billions of users | Millions of teams | Millions of servers |

## Progression to Hard Level

After mastering medium problems, hard-level problems introduce:
- Cross-platform integration (web, mobile, desktop)
- Multi-region deployment with data replication
- Advanced features (stories, payments, AI)
- Even higher scale (billions of users, millions of concurrent)
- Complex notification systems
- Advanced security and compliance

## Key Technical Decisions

### 1. Database Choice
- **PostgreSQL**: Metadata, strong consistency, complex queries
- **Cassandra**: Messages, high write throughput, time-series data
- **Redis**: Real-time state, caching, pub/sub

### 2. Real-time Communication
- **WebSocket**: Bidirectional text messaging
- **WebRTC**: Peer-to-peer voice/video
- **UDP**: Low-latency voice (custom protocols)

### 3. Search Implementation
- **Elasticsearch**: Powerful, scalable, flexible
- **PostgreSQL Full-text**: Simpler, consistent, limited features
- **Client-side Search**: Privacy (E2E encrypted)

### 4. Media Storage
- **S3/Cloud Storage**: Scalable, durable
- **CDN**: Fast global delivery
- **Lifecycle Policies**: Cost optimization

## Interview Tips for Medium Problems

1. **Discuss Trade-offs**: Explain why you chose specific technologies
2. **Security Considerations**: Encryption, authentication, authorization
3. **Scale Calculations**: Estimate QPS, storage, bandwidth
4. **Component Design**: Deep dive into specific services
5. **Failure Scenarios**: How to handle failures and edge cases
6. **Monitoring**: Metrics and observability
7. **Performance**: Caching, indexing, optimization strategies

## Common Interview Questions

### Functional
- How would you add feature X? (reactions, polls, etc.)
- How would you implement search?
- How would you handle file sharing?
- How would you implement notifications?

### Non-Functional
- How would you scale to 10x users?
- How would you reduce latency?
- How would you ensure message ordering?
- How would you handle database failures?

### Security
- How would you implement E2E encryption?
- How would you prevent spam/abuse?
- How would you secure voice channels?
- How would you handle data privacy?

## Additional Resources

- Signal Protocol Documentation
- WebRTC API and Architecture
- Elasticsearch Best Practices
- Cassandra Data Modeling
- Redis Pub/Sub Patterns
- S3 and CDN Optimization
- Discord Engineering Blog
- Slack Engineering Blog
