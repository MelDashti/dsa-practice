# Fundamentals: Easy Level

## Overview

This section covers foundational system design concepts that every software engineer should understand. These topics are frequently asked in entry-level to mid-level interviews and form the building blocks for more complex system designs.

## Topics Covered

### 1. Scaling Basics (scaling_basics.md)
**Concept:** Vertical vs Horizontal Scaling

Learn when to scale up (add more resources to a single machine) versus scale out (add more machines). This document covers:
- Vertical scaling advantages and limitations
- Horizontal scaling patterns and challenges
- Cost analysis and trade-offs
- Auto-scaling strategies
- Real-world examples

**Key Takeaway:** Horizontal scaling provides better fault tolerance and unlimited growth potential, while vertical scaling is simpler but has hardware limits.

### 2. Caching Fundamentals (caching_fundamentals.md)
**Concept:** Cache Strategies and Eviction Policies

Master the art of caching to improve system performance and reduce database load. Topics include:
- Cache-aside, write-through, write-behind patterns
- LRU, LFU, FIFO eviction policies
- Cache stampede problem and solutions
- Distributed caching with Redis/Memcached
- Cache consistency challenges

**Key Takeaway:** Effective caching can improve response times from seconds to milliseconds and reduce database load by 80-90%.

### 3. Load Balancing 101 (load_balancing_101.md)
**Concept:** Load Balancing Algorithms and Health Checks

Understand how to distribute traffic across multiple servers efficiently. Learn about:
- Round robin, weighted round robin, least connections algorithms
- Layer 4 vs Layer 7 load balancing
- Health check mechanisms
- Session persistence (sticky sessions)
- Load balancer high availability

**Key Takeaway:** Load balancers are critical for horizontal scaling and high availability, distributing millions of requests across server fleets.

## How to Use These Documents

Each document follows a consistent structure:

1. **Problem Statement** - What problem are we solving?
2. **Requirements** - Functional and non-functional requirements
3. **Capacity Estimation** - Back-of-the-envelope calculations
4. **High-Level Design** - Architecture diagrams and components
5. **API Design** - REST/RPC interface specifications
6. **Database Schema** - Data models and relationships
7. **Detailed Component Design** - Deep dive into algorithms and implementations
8. **Trade-offs and Considerations** - Pros, cons, and when to use
9. **Scalability & Bottlenecks** - How to scale and common pitfalls
10. **Follow-up Questions** - Interview-style discussion points

## Interview Tips

**For Easy-Level Topics:**
- Be able to explain concepts in simple terms
- Draw clear diagrams showing data flow
- Discuss real-world examples (e.g., "Netflix uses caching for...")
- Quantify impact (e.g., "Caching reduced latency from 200ms to 5ms")
- Know when NOT to use each pattern

**Common Questions:**
- "Design a system that can handle 10x traffic growth"
- "How would you improve response time for a slow API?"
- "What happens when a cache server fails?"
- "How do you prevent a single server from becoming a bottleneck?"

## Progression Path

After mastering these easy-level concepts:
1. Move to **Medium** level: Database scaling, CDN design, Microservices
2. Then tackle **Hard** level: CAP theorem, Distributed consensus, Event-driven architecture
3. Apply these fundamentals to **Core Components** design problems

## Additional Resources

- **Books:**
  - "Designing Data-Intensive Applications" by Martin Kleppmann
  - "System Design Interview" by Alex Xu

- **Practice:**
  - Design a caching layer for your favorite website
  - Implement a simple load balancer
  - Calculate capacity for your most-used app

## Quick Reference

| Concept | Use When | Avoid When |
|---------|----------|------------|
| **Vertical Scaling** | Early stage, simple apps | Need unlimited scale |
| **Horizontal Scaling** | Need high availability | Simple apps, stateful systems |
| **Caching** | Read-heavy workloads | Data must be 100% fresh |
| **Load Balancing** | Multiple servers | Single server sufficient |

---

**Next Steps:** Once comfortable with these topics, proceed to the Medium difficulty fundamentals to learn about database scaling strategies and microservices architecture.
