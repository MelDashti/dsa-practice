# Design a Generic Proximity Service

## 1. Problem Overview

Design a reusable proximity service that can efficiently find nearby entities (users, drivers, restaurants, stores, etc.) within a given radius. This service should be generic enough to power multiple applications like Uber, Yelp, Tinder, Find My Friends, etc.

**Key Challenge**: Build a scalable, low-latency service for proximity queries that can handle millions of entities with frequent location updates.

## 2. Requirements

### Functional Requirements
- **Add/Update Location**: Store entity location (lat/long)
- **Remove Location**: Delete entity from index
- **Search Nearby**: Find entities within radius
- **Batch Updates**: Handle bulk location updates
- **Category Filtering**: Filter results by type/category
- **Radius Search**: Support variable radius (100m - 50km)

### Non-Functional Requirements
- **Latency**: < 100ms for proximity queries
- **Throughput**: 100K location updates/sec, 50K queries/sec
- **Scalability**: Support 100M+ active entities
- **Availability**: 99.99% uptime
- **Accuracy**: Within 10 meters

## 3. High-Level Design

```
┌──────────────┐
│   Clients    │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Load Balancer   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────────┐
│ Proximity API    │─────►│  Redis Cluster  │
│                  │      │  (Geospatial)   │
└──────────────────┘      └─────────────────┘
       │
       ▼
┌──────────────────┐
│  PostgreSQL      │
│  (Metadata)      │
└──────────────────┘
```

## 4. API Design

### Update Location
```
PUT /api/v1/locations
{
  "entity_id": "ent_123",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "category": "driver",
  "metadata": {
    "status": "available",
    "type": "uber_x"
  }
}

Response: {"success": true}
```

### Search Nearby
```
GET /api/v1/locations/nearby
Query:
  - latitude: 37.7749
  - longitude: -122.4194
  - radius_m: 5000
  - category: driver
  - limit: 20

Response:
{
  "entities": [
    {
      "entity_id": "ent_123",
      "latitude": 37.7739,
      "longitude": -122.4185,
      "distance_m": 145,
      "category": "driver",
      "metadata": {...}
    }
  ],
  "count": 15
}
```

### Remove Location
```
DELETE /api/v1/locations/{entity_id}
Response: {"success": true}
```

## 5. Core Implementation

### Redis Geospatial
```python
class ProximityService:
    def update_location(self, entity_id, lat, lon, category, metadata):
        # Add to geospatial index (by category)
        self.redis.geoadd(
            f"locations:{category}",
            lon, lat, entity_id
        )

        # Store metadata separately
        self.redis.hset(
            f"entity:{entity_id}",
            mapping={
                "latitude": lat,
                "longitude": lon,
                "category": category,
                "metadata": json.dumps(metadata),
                "updated_at": time.time()
            }
        )

        # Set TTL for inactive cleanup
        self.redis.expire(f"entity:{entity_id}", 3600)

    def search_nearby(self, lat, lon, radius_m, category, limit):
        # Search Redis geospatial index
        results = self.redis.georadius(
            f"locations:{category}",
            lon, lat,
            radius_m, "m",
            withdist=True,
            withcoord=True,
            count=limit,
            sort="ASC"
        )

        # Enrich with metadata
        entities = []
        for entity_id, distance, coords in results:
            metadata = self.redis.hgetall(f"entity:{entity_id}")
            if metadata:
                entities.append({
                    "entity_id": entity_id,
                    "latitude": float(coords[1]),
                    "longitude": float(coords[0]),
                    "distance_m": round(distance, 2),
                    "category": category,
                    "metadata": json.loads(metadata.get("metadata", "{}"))
                })

        return entities

    def remove_location(self, entity_id, category):
        # Remove from geospatial index
        self.redis.zrem(f"locations:{category}", entity_id)

        # Remove metadata
        self.redis.delete(f"entity:{entity_id}")
```

## 6. Geospatial Indexing

### Redis Geospatial (Recommended)
**Pros**:
- Fast in-memory operations
- Built-in geospatial commands
- Simple to use
- Supports radius queries

**Cons**:
- Limited to single server capacity per index
- Requires partitioning for huge datasets

### QuadTree Implementation
```python
class QuadTreeNode:
    def __init__(self, bounds, capacity=100):
        self.bounds = bounds  # (min_lat, max_lat, min_lon, max_lon)
        self.capacity = capacity
        self.entities = []
        self.divided = False
        self.children = [None, None, None, None]  # NW, NE, SW, SE

    def insert(self, entity):
        if not self.contains(entity):
            return False

        if len(self.entities) < self.capacity:
            self.entities.append(entity)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(entity):
                return True

    def query_radius(self, center, radius):
        results = []

        if not self.intersects_circle(center, radius):
            return results

        for entity in self.entities:
            if self.distance(center, entity.location) <= radius:
                results.append(entity)

        if self.divided:
            for child in self.children:
                results.extend(child.query_radius(center, radius))

        return results
```

### S2 Geometry (Google's Solution)
- **Cell-based indexing** at multiple levels
- **Hierarchical coverage** for efficient queries
- **Complex but powerful** for global scale

### Geohash
```python
import geohash2 as gh

# Encode location
hash = gh.encode(37.7749, -122.4194, precision=7)

# Get neighbors
neighbors = gh.neighbors(hash)

# Decode
lat, lon = gh.decode(hash)
```

## 7. Scalability Patterns

### Sharding by Geography
```python
# Partition world into regions
def get_shard_for_location(lat, lon):
    # Simple grid-based sharding
    lat_bucket = int((lat + 90) / 10)  # 18 buckets
    lon_bucket = int((lon + 180) / 10)  # 36 buckets
    shard_id = lat_bucket * 36 + lon_bucket
    return shard_id

# Route query to appropriate shard
shard_id = get_shard_for_location(latitude, longitude)
redis_client = redis_cluster.get_client(shard_id)
```

### Consistent Hashing
```python
from hash_ring import HashRing

# Initialize ring with Redis instances
ring = HashRing([
    'redis1:6379',
    'redis2:6379',
    'redis3:6379'
])

# Get server for geohash
server = ring.get_node(geohash_prefix)
```

### Read Replicas
- **Primary** for writes (location updates)
- **Replicas** for reads (proximity queries)
- Eventually consistent

## 8. Performance Optimization

### Caching Strategy
```python
# Cache query results
cache_key = f"nearby:{lat}:{lon}:{radius}:{category}"

# Round coordinates for better cache hits
lat_rounded = round(lat, 3)
lon_rounded = round(lon, 3)

# Check cache
cached = redis.get(cache_key)
if cached:
    return json.loads(cached)

# Query and cache
results = search_nearby(lat, lon, radius, category)
redis.setex(cache_key, 300, json.dumps(results))
```

### Batch Processing
```python
# Batch location updates
def batch_update_locations(updates):
    pipeline = redis.pipeline()

    for update in updates:
        pipeline.geoadd(
            f"locations:{update['category']}",
            update['longitude'],
            update['latitude'],
            update['entity_id']
        )

    pipeline.execute()
```

### Polygon Pre-computation
```python
# Pre-compute popular areas
def precompute_hotspots():
    hotspots = [
        {"name": "downtown_sf", "center": (37.7749, -122.4194), "radius": 2000},
        {"name": "soho_nyc", "center": (40.7234, -73.9977), "radius": 1500}
    ]

    for spot in hotspots:
        results = search_nearby(
            spot["center"][0],
            spot["center"][1],
            spot["radius"],
            "restaurant"
        )

        redis.setex(
            f"hotspot:{spot['name']}",
            1800,  # 30 minutes
            json.dumps(results)
        )
```

## 9. Trade-offs

### Redis vs PostgreSQL PostGIS
| Aspect | Redis | PostGIS |
|--------|-------|---------|
| Speed | Very fast (in-memory) | Slower (disk-based) |
| Persistence | Optional | Strong |
| Scalability | Horizontal (sharding) | Vertical primarily |
| Query Complexity | Simple radius | Complex spatial queries |
| Data Durability | Risk of data loss | ACID guarantees |

**Recommendation**: Use Redis for hot data (active entities), PostgreSQL for persistent storage.

### QuadTree vs Geohash vs S2
| Aspect | QuadTree | Geohash | S2 |
|--------|----------|---------|----|
| Complexity | Medium | Simple | Complex |
| Precision | Good | Good | Excellent |
| Query Speed | Fast | Fast | Very fast |
| Edge Cases | Some issues | Pole/equator issues | Handles well |
| Implementation | Custom | Libraries available | Google library |

**Recommendation**: Start with Redis Geospatial (uses Geohash internally), move to S2 for global scale.

## 10. Follow-up Questions

1. **How would you handle entity movement (e.g., moving vehicles)?**
   - Frequent location updates (every 3-5 seconds)
   - Update Redis geospatial index
   - Notify subscribers via WebSocket/Redis Pub/Sub
   - Clean up stale locations with TTL

2. **How would you implement geofencing (alerts when entering/leaving area)?**
   - Define polygon/circle boundaries
   - Check location against boundaries on update
   - Trigger webhook/notification on entry/exit
   - Use Redis Lua scripts for atomic checks

3. **How would you find K nearest neighbors?**
   ```python
   results = redis.georadius(
       "locations:category",
       lon, lat,
       max_radius, "m",
       count=k,
       sort="ASC"
   )
   ```

4. **How would you handle cross-border searches?**
   - Query multiple shards based on bounding box
   - Merge and sort results by distance
   - Handle edge cases at shard boundaries

5. **How would you scale to 1 billion entities?**
   - More aggressive sharding (1000+ shards)
   - Hierarchical indexing (city → neighborhood → street)
   - Separate active vs inactive entities
   - Time-based partitioning

6. **How would you ensure high availability?**
   - Redis Sentinel for automatic failover
   - Multi-region replication
   - Circuit breakers
   - Graceful degradation

7. **How would you implement polygon search (find entities in custom area)?**
   - Use PostGIS ST_Within
   - Or check if point is inside polygon (ray casting algorithm)
   - Pre-compute for common polygons (neighborhoods)

8. **What metrics would you track?**
   - Query latency (p50, p95, p99)
   - Update throughput
   - Cache hit rate
   - Entity count by category
   - Shard distribution
   - Error rates

9. **How would you test the system?**
   - Unit tests for distance calculations
   - Integration tests for Redis operations
   - Load tests for throughput
   - Chaos tests for failover
   - Accuracy tests for edge cases

10. **How would you handle time zones and coordinate systems?**
    - Always use WGS84 (SRID 4326)
    - Store timestamps in UTC
    - Convert to local time on client
    - Handle date line crossing
