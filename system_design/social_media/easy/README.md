# Easy Social Media System Design Problems

This directory contains simplified versions of social media platform designs, focusing on core features and basic architecture patterns.

## Overview

Easy-level system design problems help you understand fundamental concepts before tackling complex distributed systems. These designs focus on:
- Basic feature sets
- Simple architecture patterns
- Core database schemas
- Essential APIs
- Minimal scalability considerations

## Problems in This Section

### 1. Instagram MVP (Minimum Viable Product)
**File:** `design_instagram_mvp.md`

A simplified photo-sharing platform focusing on essential features only.

**Key Features:**
- User registration and profiles
- Photo upload and storage
- Basic feed (chronological)
- Simple likes and comments
- Following users

**Learning Objectives:**
- Understanding media storage patterns
- Basic feed generation
- Simple database design
- RESTful API design
- CDN integration basics

**Complexity Level:** Beginner-friendly
**Estimated Time:** 30-45 minutes

## How to Approach Easy Problems

1. **Start with Requirements:** Clearly define what features are in scope
2. **Keep It Simple:** Avoid over-engineering; focus on core functionality
3. **Basic Calculations:** Understand storage and bandwidth needs
4. **Simple Architecture:** Start with monolithic or simple client-server patterns
5. **Learn Patterns:** Focus on understanding fundamental design patterns

## Key Concepts to Master

### 1. Basic Architecture Patterns
- Client-server model
- Three-tier architecture (Presentation, Application, Data)
- Basic load balancing

### 2. Storage Fundamentals
- Relational database design
- File storage vs database storage
- Basic indexing strategies

### 3. Media Handling
- Image upload and storage
- CDN basics
- Thumbnail generation

### 4. API Design
- RESTful principles
- CRUD operations
- Basic authentication

### 5. Simple Caching
- Application-level caching
- Database query caching
- Static content caching

## Common Patterns in Easy Designs

### Database Choice
For easy-level designs, start with:
- **PostgreSQL/MySQL:** For structured data (users, posts, relationships)
- **S3/Object Storage:** For media files
- **Redis:** For simple caching

### Architecture Pattern
```
[Client] -> [Load Balancer] -> [Web Servers] -> [Application Servers]
                                                      |
                                                      v
                                              [Database + Cache]
                                                      |
                                                      v
                                              [Object Storage/CDN]
```

## Progression Path

After mastering easy problems:
1. Review your design and identify bottlenecks
2. Think about what would break at scale
3. Consider additional features that would complicate the design
4. Move to Medium difficulty problems that add:
   - Multiple services
   - Complex algorithms (recommendations, trending)
   - Advanced caching strategies
   - Sharding and replication
   - Real-time features

## Interview Tips for Easy Problems

1. **Clarify Requirements Early:** Don't assume; ask questions
2. **State Assumptions:** Be explicit about scale expectations
3. **Draw Diagrams:** Visual representations help communicate ideas
4. **Explain Trade-offs:** Even simple designs have trade-offs
5. **Start Simple, Then Iterate:** Get the basic design right first

## Additional Resources

- **Books:**
  - "Designing Data-Intensive Applications" by Martin Kleppmann (Chapters 1-3)
  - "System Design Interview" by Alex Xu (Chapter 1-4)

- **Online:**
  - High Scalability Blog (highscalability.com)
  - AWS Architecture Center
  - System Design Primer (GitHub)

## Next Steps

Once comfortable with easy problems:
- Move to `/medium/` directory for more complex designs
- Focus on distributed systems concepts
- Learn about microservices architecture
- Study advanced data storage patterns
- Explore real-time communication systems

---

**Note:** These designs are educational and simplified. Production systems require significantly more complexity, security considerations, and operational excellence practices.
