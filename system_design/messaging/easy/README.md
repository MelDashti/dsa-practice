# Easy - Messaging Systems

This directory contains foundational messaging system design problems that focus on core concepts and basic implementations.

## Problems

### 1. Basic 1-on-1 Chat (`design_chat_simple.md`)
Design a simple chat application for two users to exchange text messages in real-time.

**Key Concepts**:
- WebSocket connections for real-time communication
- Message persistence and retrieval
- User presence tracking (online/offline)
- Basic message delivery guarantees

**Learning Objectives**:
- Understand real-time communication patterns
- Learn about persistent connections vs HTTP polling
- Design simple message storage and retrieval
- Implement basic scalability patterns

**Prerequisites**:
- Understanding of HTTP and WebSocket protocols
- Basic database design
- Caching concepts (Redis)
- Load balancing fundamentals

## Common Patterns in Easy Messaging Problems

### Real-time Communication
- WebSocket for bidirectional communication
- Heartbeat mechanism for connection health
- Reconnection strategies

### Message Storage
- Relational database for ordered messages
- Indexing by sender/recipient and timestamp
- Simple pagination for chat history

### Presence Management
- Redis for online user tracking
- TTL-based expiration
- Last seen timestamps

### Basic Architecture
```
Client ←→ Gateway Server ←→ Message Service ←→ Database
                ↓
           Presence Service
```

## Progression to Medium Level

After mastering easy problems, medium-level problems introduce:
- Group messaging and conversations
- Media sharing (images, videos, files)
- End-to-end encryption
- Advanced features (reactions, threads, search)
- Higher scale requirements
- Multi-region deployment

## Tips for System Design Interviews

1. **Start Simple**: Begin with core functionality before adding features
2. **Ask Clarifying Questions**: Understand scale, features, and constraints
3. **Draw Diagrams**: Visual representations help communicate design
4. **Discuss Trade-offs**: Explain why you chose specific technologies
5. **Consider Scale**: Think about how design changes at different scales

## Additional Resources

- WebSocket Protocol: RFC 6455
- Message Queue Patterns
- Database Indexing Strategies
- Caching Best Practices
- Real-time System Design Patterns
