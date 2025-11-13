# System Design - FAANG Interview Preparation

A comprehensive collection of 50+ system design problems and solutions for FAANG/MAANG interviews. Each design includes detailed architecture, scalability considerations, and trade-off analysis.

## 📊 Overview

**Total Designs:** 50+ comprehensive system design documents
**Categories:** 8 major topics
**Difficulty Levels:** Easy, Medium, Hard

### By Difficulty
- 🟢 **Easy:** 8 problems (Fundamentals and simple systems)
- 🟡 **Medium:** 25+ problems (Production-scale systems)
- 🔴 **Hard:** 17+ problems (Complex distributed systems)

## 📚 Categories

| Category | Easy | Medium | Hard | Total | Focus Area |
|----------|------|--------|------|-------|------------|
| [Fundamentals](#fundamentals) | 3 | 3 | 3 | 9 | Core concepts |
| [Core Components](#core-components) | 3 | 4 | 3 | 10 | Building blocks |
| [Social Media](#social-media) | 1 | 4 | 2 | 7 | User-generated content |
| [Messaging](#messaging) | 1 | 3 | 2 | 6 | Real-time communication |
| [Location-Based](#location-based) | 1 | 3 | 2 | 6 | Geospatial services |
| [E-commerce & Payments](#ecommerce--payments) | 1 | 3 | 4 | 8 | Transactions & consistency |
| [Infrastructure](#infrastructure) | 1 | 4 | 4 | 9 | Distributed systems |
| [Storage & Data](#storage--data) | 1 | 5 | 4 | 10 | Data management |

## 🗂️ Repository Structure

```
system_design/
├── README.md (you are here)
├── fundamentals/
│   ├── easy/     (Scaling, Caching, Load Balancing)
│   ├── medium/   (Database Scaling, CDN, Microservices)
│   └── hard/     (CAP Theorem, Consensus, Event-Driven)
├── core_components/
│   ├── easy/     (URL Shortener, Parking Lot, Vending Machine)
│   ├── medium/   (Rate Limiter, Notifications, Autocomplete, Auth)
│   └── hard/     (Unique ID, Consistent Hashing, Distributed Lock)
├── social_media/
│   ├── easy/     (Instagram MVP)
│   ├── medium/   (Instagram, Twitter, Reddit, TikTok)
│   └── hard/     (News Feed Algorithm, Social Graph)
├── messaging/
│   ├── easy/     (Simple Chat)
│   ├── medium/   (WhatsApp, Slack, Discord)
│   └── hard/     (Facebook Messenger, Notification Service)
├── location_based/
│   ├── easy/     (Yelp Simple)
│   ├── medium/   (Uber, Yelp, Proximity Service)
│   └── hard/     (Google Maps, Nearby Friends)
├── ecommerce_payments/
│   ├── easy/     (Online Bookstore)
│   ├── medium/   (Amazon, BookMyShow, Hotel Reservation)
│   └── hard/     (Payment System, UPI, Digital Wallet, Stock Exchange)
├── infrastructure/
│   ├── easy/     (Web Crawler Basics)
│   ├── medium/   (Kafka, Web Crawler, Metrics, Ad Aggregation)
│   └── hard/     (Job Scheduler, Distributed Cache, Rate Limiter, Service Mesh)
└── storage_data/
    ├── easy/     (File Upload Service)
    ├── medium/   (Dropbox, Drive, YouTube, Netflix, Spotify)
    └── hard/     (S3, Key-Value Store, Email Service, Zoom)
```

## 🎯 Most Important Problems

### Must-Know (Top 15)
Based on interview frequency at FAANG companies:

1. **URL Shortener** (Easy) - Entry level, covers many concepts
2. **Rate Limiter** (Medium) - Appears in 80% of interviews
3. **Design Instagram** (Medium) - Social media fundamentals
4. **Design Twitter** (Medium) - Real-time feeds
5. **Design YouTube** (Medium) - Video streaming
6. **Design WhatsApp** (Medium) - Real-time messaging
7. **Design Uber** (Medium) - Location-based services
8. **Design Amazon** (Medium) - E-commerce at scale
9. **News Feed Algorithm** (Hard) - Ranking systems
10. **Payment System** (Hard) - Transaction consistency
11. **Consistent Hashing** (Hard) - Distributed systems
12. **Design Kafka** (Medium) - Message queues
13. **Design Dropbox** (Medium) - File sync
14. **Web Crawler** (Medium) - Data ingestion
15. **Unique ID Generator** (Hard) - Distributed coordination

### By Company Focus

- **Facebook/Meta:** News Feed, Instagram, Messenger, WhatsApp
- **Google:** YouTube, Google Maps, Google Drive, Search Autocomplete
- **Amazon:** E-commerce, AWS S3, DynamoDB (Key-Value Store)
- **Netflix:** Video Streaming, Recommendation System
- **Uber:** Ride Matching, Real-time Tracking, Pricing
- **Twitter:** Tweet Feed, Trending Topics, Timeline

## 📖 Document Format

Each system design document includes:

1. **Problem Statement** - What are we building?
2. **Requirements** (Functional & Non-Functional)
3. **Capacity Estimation** (Traffic, Storage, Bandwidth)
4. **High-Level Design** (Architecture diagrams)
5. **API Design** (RESTful endpoints, WebSocket events)
6. **Database Design** (Schema, indexes, justification)
7. **Detailed Component Design** (Algorithms, pseudocode)
8. **Scalability & Performance** (Bottlenecks, optimizations)
9. **Trade-offs & Alternatives** (Design decisions)
10. **Monitoring & Operations** (Metrics, alerting)
11. **Follow-up Questions** (15-30 interview questions)

## 📈 Study Plans

### 1-Week Crash Course (20-25 hours)
```
Day 1-2:  Fundamentals (all easy + medium)
Day 3-4:  Top 5 must-know problems
Day 5-6:  Focus on your target company's domains
Day 7:    Mock interviews and review
```

### 1-Month Comprehensive (60-80 hours)
```
Week 1:  All Fundamentals + Core Components
Week 2:  Social Media + Messaging (all levels)
Week 3:  Location + E-commerce + Payments
Week 4:  Infrastructure + Storage + Mock interviews
```

### 3-Month Deep Mastery (150-200 hours)
```
Month 1:  Easy and Medium problems (all categories)
Month 2:  Hard problems + deep dives
Month 3:  Practice, mock interviews, refinement
```

## 💡 Key Concepts to Master

### Database Layer
- SQL vs NoSQL trade-offs
- Replication (Primary-Replica, Multi-Primary)
- Sharding and partitioning strategies
- Indexing strategies
- ACID vs BASE

### Caching Layer
- Cache-aside pattern
- Write-through, Write-behind
- Cache invalidation strategies
- CDN usage
- Redis/Memcached patterns

### Application Layer
- Stateless vs stateful services
- Load balancing algorithms
- API design (REST, GraphQL, gRPC)
- Rate limiting
- Authentication & authorization

### Communication
- Synchronous (HTTP, RPC)
- Asynchronous (Message queues)
- Real-time (WebSockets, SSE)
- Protocols (HTTP/2, HTTP/3, WebRTC)

### Distributed Systems
- CAP theorem
- Consistency models
- Consensus algorithms (Paxos, Raft)
- Distributed transactions
- Service mesh

## 🎓 Interview Tips

### Do's ✅
- Ask clarifying questions (5 minutes)
- Define functional and non-functional requirements
- Start with high-level design
- Discuss trade-offs explicitly
- Consider failure scenarios
- Mention monitoring and operations
- Use numbers (back-of-envelope calculations)

### Don'ts ❌
- Jump into details immediately
- Assume requirements
- Ignore scalability
- Design for current scale only
- Forget non-functional requirements
- Overlook trade-offs
- Ignore interviewer feedback

### 4-Step Interview Approach
1. **Clarify Requirements** (5 min) - Ask questions, define scope
2. **High-Level Design** (10-15 min) - Draw architecture, explain flow
3. **Deep Dive** (15-20 min) - Detailed component design
4. **Wrap Up** (5 min) - Bottlenecks, trade-offs, monitoring

## 🏆 Category Details

### Fundamentals
**Path:** `fundamentals/`
**Focus:** Core system design concepts everyone must know

**Easy:** Scaling basics, caching fundamentals, load balancing
**Medium:** Database scaling, CDN design, microservices
**Hard:** CAP theorem, distributed consensus, event-driven architecture

**Start here if:** You're new to system design

### Core Components
**Path:** `core_components/`
**Focus:** Building blocks used in larger systems

**Easy:** URL shortener, parking lot, vending machine
**Medium:** Rate limiter, notification system, autocomplete, authentication
**Hard:** Unique ID generator, consistent hashing, distributed lock

**Start here if:** You want practical, frequently-asked problems

### Social Media
**Path:** `social_media/`
**Focus:** User-generated content platforms

**Easy:** Instagram MVP
**Medium:** Instagram (full), Twitter, Reddit, TikTok
**Hard:** News feed algorithm, social graph service

**Practice if applying to:** Facebook, Instagram, Twitter, TikTok, Snap

### Messaging
**Path:** `messaging/`
**Focus:** Real-time communication systems

**Easy:** Simple 1-on-1 chat
**Medium:** WhatsApp, Slack, Discord
**Hard:** Facebook Messenger, large-scale notification service

**Practice if applying to:** WhatsApp, Slack, Discord, Telegram

### Location-Based
**Path:** `location_based/`
**Focus:** Geospatial services and real-time tracking

**Easy:** Yelp (simple nearby search)
**Medium:** Uber, Yelp (full), proximity service
**Hard:** Google Maps, nearby friends

**Practice if applying to:** Uber, Lyft, DoorDash, Google Maps

### E-commerce & Payments
**Path:** `ecommerce_payments/`
**Focus:** Transactions, consistency, financial systems

**Easy:** Online bookstore
**Medium:** Amazon, BookMyShow, hotel reservation
**Hard:** Payment system, UPI, digital wallet, stock exchange

**Practice if applying to:** Amazon, Stripe, PayPal, trading firms

### Infrastructure
**Path:** `infrastructure/`
**Focus:** Distributed systems and platform services

**Easy:** Web crawler basics
**Medium:** Kafka, web crawler, metrics monitoring, ad aggregation
**Hard:** Job scheduler, distributed cache, rate limiter, service mesh

**Practice if applying to:** Infrastructure/platform teams at any company

### Storage & Data
**Path:** `storage_data/`
**Focus:** Data storage, streaming, and content delivery

**Easy:** File upload service
**Medium:** Dropbox, Google Drive, YouTube, Netflix, Spotify
**Hard:** S3, key-value store, email service, Zoom

**Practice if applying to:** AWS, Google Cloud, storage teams, streaming services

## 📚 Additional Resources

### Books (Highly Recommended)
- **"Designing Data-Intensive Applications"** by Martin Kleppmann (Essential)
- **"System Design Interview Vol 1 & 2"** by Alex Xu (Interview focused)
- **"Database Internals"** by Alex Petrov (Deep technical)
- **"Building Microservices"** by Sam Newman

### Online Resources
- **NeetCode System Design Course** - Video explanations
- **ByteByteGo** - Visual system design explanations
- **High Scalability** - Real-world architectures
- **Engineering Blogs** - Netflix, Uber, Airbnb tech blogs

### Practice Platforms
- **Pramp** - Free mock interviews
- **Interviewing.io** - Anonymous practice with engineers
- **System Design Primer** - GitHub repo with examples

## 🤝 Contributing

This is a living resource. Consider:
- Adding more real-world examples
- Updating with latest technologies
- Sharing interview experiences
- Improving existing designs

---

**Last Updated:** November 12, 2025
**Status:** ✅ All 50+ designs complete with comprehensive documentation
**Ready for FAANG Interviews!** 🚀
