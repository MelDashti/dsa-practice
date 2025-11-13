# Fundamentals: Medium Level

## Overview

This section covers intermediate system design concepts that require deeper understanding of distributed systems. These topics are common in mid-to-senior level interviews and represent real-world challenges in scaling production systems.

## Topics Covered

### 1. Database Scaling (database_scaling.md)
**Concept:** Replication, Sharding, and Partitioning

Master techniques for scaling databases beyond single-server limits:
- **Primary-Replica Replication:** Read scaling and high availability
- **Multi-Primary Replication:** Multi-region writes with conflict resolution
- **Sharding Strategies:** Range-based, hash-based, consistent hashing
- **Partitioning:** Horizontal, vertical, and functional partitioning
- **SAGA Pattern:** Distributed transactions across shards

**Key Metrics:**
- Read replicas can improve read throughput 10x
- Sharding enables horizontal scaling to petabytes
- Proper sharding key critical (avoid hotspots)

### 2. CDN Design (cdn_design.md)
**Concept:** Content Delivery Network Architecture

Learn how CDNs deliver content globally with minimal latency:
- **Edge Server Architecture:** Geographic distribution
- **Caching Strategies:** Pull vs Push CDN
- **Cache Invalidation:** Purging and version management
- **Origin Shield:** Regional caching layer
- **Dynamic Content:** ESI, edge computing

**Impact:** CDNs reduce latency from 500ms+ to <50ms globally and offload 80-90% of origin traffic.

### 3. Microservices Basics (microservices_basics.md)
**Concept:** Microservices vs Monolith Architecture

Understand when and how to decompose monoliths into microservices:
- **Service Communication:** Sync (REST/gRPC) vs Async (Message queues)
- **Service Discovery:** Dynamic routing and load balancing
- **API Gateway:** Single entry point pattern
- **SAGA Pattern:** Distributed transactions
- **Service Mesh:** Infrastructure layer for service communication

**Decision Framework:** Use microservices when team > 50 people, need independent deployment, or different scaling requirements per service.

## Complexity Comparison

| Aspect | Easy Level | Medium Level |
|--------|-----------|--------------|
| **Scope** | Single component | Multiple interacting systems |
| **State** | Usually stateless | Stateful, distributed state |
| **Consistency** | Strong consistency | Eventual consistency |
| **Failure Handling** | Simple retry | Circuit breakers, SAGA |
| **Scale** | Thousands of requests | Millions of requests |

## Real-World Examples

### Database Scaling
- **Instagram:** Sharded PostgreSQL by user ID, 1000+ database servers
- **Twitter:** Cassandra for tweets (eventually consistent)
- **Spotify:** Cassandra + PostgreSQL hybrid approach

### CDN
- **Netflix:** Custom CDN (Open Connect) in 1000+ ISP locations
- **Cloudflare:** 250+ cities, handles 10% of internet traffic
- **YouTube:** Google's global CDN with edge caching

### Microservices
- **Amazon:** 2-pizza teams owning services (pioneered microservices)
- **Uber:** 2000+ microservices
- **Airbnb:** Monolith → Microservices migration

## Interview Deep-Dive Topics

### Database Scaling
- **Q:** "How would you shard a user database?"
  - Consider shard key (user_id, geographic region)
  - Discuss rebalancing strategies
  - Handle celebrity users (hotspot problem)

- **Q:** "What happens during a network partition in multi-primary setup?"
  - Conflict detection (vector clocks)
  - Conflict resolution (LWW, merge, CRDT)
  - CAP theorem trade-offs

### CDN
- **Q:** "How do you invalidate cache across 200+ edge locations?"
  - Purge API fan-out pattern
  - Cache tags for bulk invalidation
  - TTL vs explicit purge trade-offs

- **Q:** "How would you optimize video streaming?"
  - Adaptive bitrate (HLS/DASH)
  - Segment-based caching
  - Range request support

### Microservices
- **Q:** "How do you handle transactions across services?"
  - SAGA pattern (choreography vs orchestration)
  - 2-phase commit limitations
  - Eventual consistency patterns

- **Q:** "How do you debug a failed request across 10 services?"
  - Distributed tracing (Jaeger, Zipkin)
  - Correlation IDs
  - Centralized logging

## Common Pitfalls

### Database Scaling
❌ Sharding too early (premature optimization)
❌ Wrong shard key (causes hotspots)
❌ Not planning for resharding

✅ Vertical scale first, shard when necessary
✅ Choose high-cardinality shard key
✅ Use consistent hashing for flexibility

### CDN
❌ Caching everything blindly
❌ Not handling cache stampede
❌ Ignoring geographic distribution

✅ Cache based on access patterns
✅ Use request coalescing
✅ Place PoPs near users

### Microservices
❌ Too many small services (nano-services)
❌ Synchronous calls creating cascading failures
❌ Shared databases between services

✅ Right-sized services (bounded contexts)
✅ Async communication where possible
✅ Database per service pattern

## Hands-On Practice

1. **Database Scaling Exercise:**
   - Design a sharding strategy for 100M users
   - Plan for 10x growth
   - Handle hotspot users (celebrities)

2. **CDN Exercise:**
   - Design caching strategy for a video platform
   - Calculate cache hit ratio improvement
   - Plan for global deployment

3. **Microservices Exercise:**
   - Decompose an e-commerce monolith
   - Design API gateway
   - Plan service communication

## Prerequisites

Before tackling medium-level topics, ensure you understand:
- ✅ Vertical and horizontal scaling (Easy)
- ✅ Caching fundamentals (Easy)
- ✅ Load balancing (Easy)
- ✅ Basic database concepts (ACID, indexes)
- ✅ HTTP/REST APIs

## Next Steps

After mastering medium-level concepts:
1. **Hard Level:** CAP theorem, Distributed consensus, Event-driven architecture
2. **Apply to Problems:** Use these patterns in core component designs
3. **Read Case Studies:** How companies like Netflix, Uber scale

## Quick Reference

| Pattern | Best For | Complexity | Scale |
|---------|----------|------------|-------|
| **Read Replicas** | Read-heavy workload | Low | 10x reads |
| **Sharding** | Storage/write scaling | High | Unlimited |
| **CDN** | Static content delivery | Medium | Global |
| **Microservices** | Large teams, independent deployment | Very High | Team scale |

---

**Difficulty Rating:** ⭐⭐⭐ (3/5) - Requires understanding of distributed systems and trade-offs
