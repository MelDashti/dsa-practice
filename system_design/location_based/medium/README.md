# Medium - Location-Based Services

This directory contains intermediate-level location-based system design problems that build on foundational concepts and introduce real-time tracking, matching algorithms, and complex business logic.

## Problems

### 1. Uber (`design_uber.md`)
Design a ride-hailing service with real-time driver tracking, rider-driver matching, ETA calculation, dynamic pricing, and payments.

**Key Concepts**:
- Real-time location tracking (500K updates/sec)
- Efficient matching algorithms
- Redis Geospatial for driver locations
- Dynamic pricing (surge pricing)
- ETA calculation and routing
- Payment processing
- WebSocket for real-time updates

**Advanced Topics**:
- Geographic sharding
- Matching optimization
- Fraud detection
- Multi-region deployment

### 2. Full Yelp (`design_yelp.md`)
Design a comprehensive business discovery platform with advanced search, reviews, photos, and recommendations.

**Key Concepts**:
- Elasticsearch for full-text search
- Advanced filtering (category, price, rating, distance, hours)
- Review and rating systems
- Photo storage and CDN
- Personalized recommendations
- Fraud detection for reviews

**Advanced Topics**:
- Search ranking algorithms
- Review moderation at scale
- Image recognition
- A/B testing

### 3. Generic Proximity Service (`proximity_service.md`)
Design a reusable service for finding nearby entities that can power multiple applications.

**Key Concepts**:
- Redis Geospatial indexing
- QuadTree data structure
- Geohash encoding
- S2 Geometry (Google's approach)
- Horizontal sharding strategies
- Batch processing

**Advanced Topics**:
- Multiple indexing approaches
- Geofencing
- K-nearest neighbors
- Cross-shard queries

## Common Patterns

### Real-time Location Tracking
```python
# Continuous location updates
def update_driver_location(driver_id, lat, lon):
    # Update Redis geospatial index (fast, in-memory)
    redis.geoadd("drivers:online", lon, lat, driver_id)

    # Store metadata
    redis.hset(f"driver:{driver_id}", mapping={
        "latitude": lat,
        "longitude": lon,
        "timestamp": time.time(),
        "status": "available"
    })

    # Set TTL for cleanup
    redis.expire(f"driver:{driver_id}", 300)
```

### Matching Algorithms
- **Greedy**: Assign nearest available
- **Batch**: Optimize multiple assignments
- **Auction-based**: Drivers bid
- **ML-based**: Predict best match

### Dynamic Pricing
```python
def calculate_surge_multiplier(location):
    # Demand: Active ride requests
    demand = count_requests_in_area(location)

    # Supply: Available drivers
    supply = count_drivers_in_area(location)

    # Ratio determines surge
    ratio = demand / max(supply, 1)

    if ratio < 1: return 1.0
    elif ratio < 2: return 1.5
    elif ratio < 3: return 2.0
    else: return 2.5
```

### Advanced Search
```
Elasticsearch Query:
- Multi-field matching
- Geospatial filtering
- Faceted search
- Ranking/scoring
- Autocomplete
- Spell correction
```

## Architectural Patterns

### Typical Architecture
```
Client Apps
    │
Load Balancer
    │
┌───┴────────┬──────────┬──────────┐
│            │          │          │
Location   Business   Search    Payment
Service    Service    Service   Service
│            │          │          │
└───┬────────┴──────────┴──────────┘
    │
┌───┴─────────────┬─────────────┐
│                 │             │
Redis          PostgreSQL   Elasticsearch
(Geospatial)   (Metadata)   (Search)
```

### Data Storage Strategy
- **Hot Data** (active locations): Redis
- **Warm Data** (recent history): PostgreSQL
- **Cold Data** (archives): S3/Data Lake
- **Search Index**: Elasticsearch

### Caching Strategy
- **Location queries**: 1-5 minutes
- **Business data**: 1 hour
- **Search results**: 5 minutes
- **User profiles**: 30 minutes

## Scale Considerations

### Traffic Patterns
- **Location updates**: Continuous, high volume (500K/sec)
- **Search queries**: Bursty, moderate volume (5K/sec)
- **Ride matching**: Latency-sensitive (< 3 sec)
- **Reviews/ratings**: Low volume, spiky

### Geographic Distribution
- **Single Region**: Simplest, higher latency for distant users
- **Multi-Region**: Lower latency, complex consistency
- **Edge Locations**: CDN, static assets

### Sharding Strategies
- **By Geography**: City, region, grid
- **By Entity Type**: Drivers, riders, businesses
- **By Time**: Historical data partitioning
- **Hybrid**: Combine multiple strategies

## Key Technical Decisions

### Location Storage
| Option | Use Case | Pros | Cons |
|--------|----------|------|------|
| Redis Geospatial | Hot, active data | Fast, scalable | Not persistent |
| PostgreSQL PostGIS | Persistent data | ACID, complex queries | Slower |
| MongoDB Geospatial | Flexible schema | Good balance | Eventual consistency |
| S2/QuadTree | Custom needs | Full control | Complex implementation |

### Real-time Communication
| Technology | Use Case | Pros | Cons |
|------------|----------|------|------|
| WebSocket | Bidirectional | Real-time, efficient | Stateful |
| Server-Sent Events | Uni-directional | Simple | One-way only |
| Redis Pub/Sub | Internal | Fast, simple | Not durable |
| Kafka | Event streaming | Durable, scalable | Complex |

## Interview Tips

### Structure Your Answer
1. **Clarify Requirements** (5 min)
   - Scale (users, entities, QPS)
   - Latency requirements
   - Consistency needs
   - Special features

2. **High-Level Design** (10 min)
   - Draw architecture diagram
   - Identify key components
   - Data flow

3. **Deep Dive** (20 min)
   - Choose 2-3 components
   - API design
   - Data models
   - Algorithms

4. **Scale & Trade-offs** (10 min)
   - Bottlenecks
   - Scaling strategies
   - Alternative approaches

### Common Follow-ups
1. **How would you reduce latency?**
   - Regional deployment
   - Better indexing
   - Caching
   - Pre-computation

2. **How would you handle 10x scale?**
   - More shards
   - Better partitioning
   - Separate read/write paths
   - Caching layers

3. **How would you ensure accuracy?**
   - Coordinate validation
   - Distance verification
   - Data quality checks
   - Monitoring

4. **How would you handle failures?**
   - Redundancy
   - Failover
   - Circuit breakers
   - Graceful degradation

## Additional Resources

- **Papers**: Uber's Geospatial Index, Google S2
- **Tech Blogs**: Uber Engineering, Lyft Engineering, Yelp Engineering
- **Tools**: Redis, PostGIS, Elasticsearch, S2 Library
- **Algorithms**: QuadTree, R-tree, Geohash, Haversine
