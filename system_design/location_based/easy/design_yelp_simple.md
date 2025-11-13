# Design a Simple Nearby Businesses Service

## 1. Problem Overview

Design a basic service like Yelp that allows users to search for nearby businesses based on their location. The system should support adding businesses, searching for businesses within a radius, and retrieving business details. This is a simplified version focusing on core proximity search functionality.

**Key Challenge**: Efficiently find businesses near a given location (latitude, longitude) within a specified radius.

## 2. Requirements

### Functional Requirements
- **Add Business**: Add new businesses with name, location (lat/long), and category
- **Search Nearby**: Find businesses within X kilometers of a location
- **Get Business Details**: Retrieve information about a specific business
- **Filter by Category**: Search for specific types of businesses (restaurant, cafe, etc.)

### Non-Functional Requirements
- **Low Latency**: < 500ms for search queries
- **Scalability**: Support 100M businesses, 1M daily active users
- **Availability**: 99.9% uptime
- **Read-Heavy**: 95% reads, 5% writes

### Out of Scope
- User reviews and ratings
- Business photos
- Business hours and details
- Real-time updates
- Recommendation algorithm
- User accounts

## 3. Scale Estimation

### Data Estimates
- **Total businesses**: 100 million
- **Average business data size**: 500 bytes
- **Total storage**: 100M × 500 bytes = 50 GB
- **With indexing and replication**: 200 GB

### Traffic Estimates
- **Daily Active Users**: 1 million
- **Searches per user per day**: 5
- **Total daily searches**: 5 million
- **Search QPS**: 5M / 86400 ≈ 58 QPS (average)
- **Peak QPS**: 58 × 5 ≈ 290 QPS

## 4. High-Level Design

```
┌─────────────┐
│   Client    │
│  (Mobile/   │
│    Web)     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Load Balancer   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   API Server     │
│  (Business       │
│   Logic)         │
└──────┬───────────┘
       │
       ├──────────────┬─────────────────┐
       ▼              ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌─────────────┐
│  Business   │  │   Geospatial │  │    Redis    │
│  Database   │  │    Index     │  │   (Cache)   │
│(PostgreSQL) │  │  (PostGIS)   │  └─────────────┘
└─────────────┘  └──────────────┘
```

## 5. API Design

### Add Business
```
POST /api/v1/businesses
{
  "name": "Starbucks Coffee",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "category": "cafe",
  "address": "123 Main St, San Francisco, CA",
  "phone": "+1-415-555-0123"
}

Response:
{
  "business_id": "biz_abc123",
  "name": "Starbucks Coffee",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "category": "cafe",
  "created_at": "2024-11-12T12:34:56Z"
}
```

### Search Nearby Businesses
```
GET /api/v1/businesses/search
Query Parameters:
  - latitude: 37.7749
  - longitude: -122.4194
  - radius_km: 2 (default: 5)
  - category: cafe (optional)
  - limit: 20 (default: 50)

Response:
{
  "results": [
    {
      "business_id": "biz_abc123",
      "name": "Starbucks Coffee",
      "location": {
        "latitude": 37.7749,
        "longitude": -122.4194
      },
      "category": "cafe",
      "distance_km": 0.3,
      "address": "123 Main St, San Francisco, CA"
    },
    {
      "business_id": "biz_def456",
      "name": "Blue Bottle Coffee",
      "location": {
        "latitude": 37.7739,
        "longitude": -122.4185
      },
      "category": "cafe",
      "distance_km": 0.5,
      "address": "456 Market St, San Francisco, CA"
    }
  ],
  "count": 2,
  "search_params": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "radius_km": 2
  }
}
```

### Get Business Details
```
GET /api/v1/businesses/{business_id}

Response:
{
  "business_id": "biz_abc123",
  "name": "Starbucks Coffee",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "category": "cafe",
  "address": "123 Main St, San Francisco, CA",
  "phone": "+1-415-555-0123",
  "created_at": "2024-11-12T12:34:56Z"
}
```

## 6. Data Models

### Business Table (PostgreSQL with PostGIS)
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE businesses (
    business_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,  -- PostGIS type
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    category VARCHAR(50),
    address TEXT,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Spatial index for fast proximity queries
CREATE INDEX idx_business_location ON businesses USING GIST(location);

-- Regular index for category filtering
CREATE INDEX idx_category ON businesses(category);
```

### Redis Cache Schema
```
Key: business:{business_id}
Value: {
  "name": "Starbucks Coffee",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "category": "cafe",
  "address": "..."
}
TTL: 1 hour

Key: search:{lat}:{lon}:{radius}:{category}
Value: [
  {"business_id": "biz_abc", "distance": 0.3},
  {"business_id": "biz_def", "distance": 0.5}
]
TTL: 5 minutes
```

## 7. Core Services Design

### Business Service
```python
class BusinessService:
    def add_business(self, business_data):
        # Validate input
        if not self.validate_coordinates(
            business_data["latitude"],
            business_data["longitude"]
        ):
            raise ValidationError("Invalid coordinates")

        # Generate business ID
        business_id = self.generate_id()

        # Create business record
        business = {
            "business_id": business_id,
            "name": business_data["name"],
            "latitude": business_data["latitude"],
            "longitude": business_data["longitude"],
            "category": business_data["category"],
            "address": business_data.get("address"),
            "phone": business_data.get("phone")
        }

        # Store in database
        self.db.execute("""
            INSERT INTO businesses (
                business_id, name, location, latitude, longitude,
                category, address, phone
            )
            VALUES (
                %s, %s,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                %s, %s, %s, %s, %s
            )
        """, (
            business["business_id"],
            business["name"],
            business["longitude"],  # Note: PostGIS uses lon, lat order
            business["latitude"],
            business["latitude"],
            business["longitude"],
            business["category"],
            business["address"],
            business["phone"]
        ))

        # Cache the business
        self.cache_business(business)

        return business

    def search_nearby(self, latitude, longitude, radius_km, category, limit):
        # Check cache first
        cache_key = f"search:{latitude}:{longitude}:{radius_km}:{category}"
        cached_results = self.redis.get(cache_key)

        if cached_results:
            return json.loads(cached_results)

        # Query database using PostGIS
        query = """
            SELECT
                business_id,
                name,
                latitude,
                longitude,
                category,
                address,
                ST_Distance(
                    location::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
                ) / 1000 AS distance_km
            FROM businesses
            WHERE ST_DWithin(
                location::geography,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                %s  -- radius in meters
            )
        """

        params = [longitude, latitude, longitude, latitude, radius_km * 1000]

        # Add category filter if specified
        if category:
            query += " AND category = %s"
            params.append(category)

        query += """
            ORDER BY distance_km
            LIMIT %s
        """
        params.append(limit)

        # Execute query
        results = self.db.query(query, params)

        # Format results
        formatted_results = [
            {
                "business_id": row["business_id"],
                "name": row["name"],
                "location": {
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"])
                },
                "category": row["category"],
                "distance_km": round(float(row["distance_km"]), 2),
                "address": row["address"]
            }
            for row in results
        ]

        # Cache results for 5 minutes
        self.redis.setex(
            cache_key,
            300,
            json.dumps(formatted_results)
        )

        return formatted_results

    def get_business(self, business_id):
        # Check cache
        cached = self.redis.get(f"business:{business_id}")
        if cached:
            return json.loads(cached)

        # Query database
        business = self.db.query_one("""
            SELECT business_id, name, latitude, longitude,
                   category, address, phone, created_at
            FROM businesses
            WHERE business_id = %s
        """, (business_id,))

        if not business:
            raise NotFoundError("Business not found")

        # Cache business
        self.cache_business(business)

        return business

    def cache_business(self, business):
        self.redis.setex(
            f"business:{business['business_id']}",
            3600,  # 1 hour
            json.dumps(business)
        )
```

## 8. Geospatial Indexing

### Understanding PostGIS
PostGIS is a spatial database extension for PostgreSQL that adds support for geographic objects.

**Key Functions**:
- `ST_MakePoint(longitude, latitude)`: Creates a point
- `ST_SetSRID(geom, srid)`: Sets coordinate system (4326 = WGS84)
- `ST_DWithin(geog1, geog2, distance)`: Checks if within distance
- `ST_Distance(geog1, geog2)`: Calculates distance between points
- `GIST Index`: Spatial index for fast proximity searches

### How Proximity Search Works

```sql
-- Find businesses within 5km of a point
SELECT *
FROM businesses
WHERE ST_DWithin(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
    5000  -- 5km in meters
)
ORDER BY ST_Distance(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography
)
LIMIT 20;
```

**How it works**:
1. `ST_DWithin` uses the GIST index to quickly filter businesses
2. It creates a bounding box around the search point
3. Only checks businesses within that box
4. `ST_Distance` calculates exact distances for ordering
5. Results sorted by distance, limited to top N

### Alternative: Geohash

For simpler implementations without PostGIS:

```python
import geohash

def add_business_with_geohash(business):
    # Generate geohash (precision 6 ≈ 1.2km)
    gh = geohash.encode(
        business["latitude"],
        business["longitude"],
        precision=6
    )

    business["geohash"] = gh

    # Store in database
    db.execute("""
        INSERT INTO businesses (business_id, name, latitude,
                              longitude, geohash, category)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (business["business_id"], business["name"],
          business["latitude"], business["longitude"],
          business["geohash"], business["category"]))

    # Also index by geohash prefix
    for i in range(1, 7):
        prefix = gh[:i]
        redis.sadd(f"geohash:{prefix}", business["business_id"])

def search_nearby_geohash(latitude, longitude, radius_km):
    # Calculate geohash precision needed
    precision = calculate_geohash_precision(radius_km)

    # Get geohash of search point
    search_gh = geohash.encode(latitude, longitude, precision)

    # Get neighbors (9 cells: center + 8 neighbors)
    neighbors = geohash.neighbors(search_gh)
    neighbors.append(search_gh)

    # Query all businesses in these geohash cells
    businesses = []
    for gh in neighbors:
        business_ids = redis.smembers(f"geohash:{gh}")
        for bid in business_ids:
            business = get_business(bid)
            distance = calculate_distance(
                latitude, longitude,
                business["latitude"], business["longitude"]
            )
            if distance <= radius_km:
                business["distance_km"] = distance
                businesses.append(business)

    # Sort by distance
    businesses.sort(key=lambda b: b["distance_km"])

    return businesses
```

### Haversine Distance Formula

```python
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points on Earth (in km)
    """
    R = 6371  # Earth's radius in kilometers

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)

    c = 2 * math.asin(math.sqrt(a))

    distance = R * c

    return distance
```

## 9. Scalability & Performance

### Database Optimization
- **Spatial Indexing**: GIST index on location column
- **Category Index**: B-tree index on category
- **Read Replicas**: Route search queries to replicas
- **Connection Pooling**: Reuse database connections

### Caching Strategy
```
Search Results Cache (5 min TTL):
- Cache key: "search:{lat}:{lon}:{radius}:{category}"
- Round coordinates to 3 decimal places for cache hits
- Store business IDs + distances

Business Details Cache (1 hour TTL):
- Cache key: "business:{business_id}"
- Store full business object
```

### Horizontal Scaling
- **Database Sharding**: Shard by geohash prefix
  - Businesses starting with 'a' → Shard 1
  - Businesses starting with 'b' → Shard 2
  - etc.
- **API Servers**: Stateless, scale horizontally
- **Load Balancer**: Distribute traffic evenly

## 10. Trade-offs

### PostGIS vs Geohash
**Chosen: PostGIS (for simplicity at small scale)**
- Pros: Built-in, accurate, efficient with GIST index
- Cons: Requires PostgreSQL, harder to shard
- Alternative: Geohash (simpler, easier to shard, less accurate)

### SQL vs NoSQL
**Chosen: PostgreSQL with PostGIS**
- Pros: ACID, spatial functions, proven
- Cons: Harder to scale horizontally
- Alternative: MongoDB with geospatial queries, Cassandra with geohash

### Caching Strategy
**Chosen: Redis for both search results and business details**
- Pros: Fast, simple, TTL support
- Cons: Cache invalidation complexity
- Alternative: No caching (simpler, slower)

## 11. Follow-up Questions

### Functional Enhancements
1. **How would you add business ratings and reviews?**
   - Add `reviews` table with foreign key to business
   - Store rating, text, user_id, timestamp
   - Calculate average rating
   - Index by business_id and timestamp

2. **How would you implement real-time updates?**
   - WebSocket connections for live updates
   - Publish/subscribe pattern (Redis Pub/Sub)
   - Update cache on business changes
   - Invalidate search caches

3. **How would you add business photos?**
   - Store images in S3/Cloud Storage
   - Store URLs in database
   - Thumbnail generation
   - CDN for fast delivery

### Scale & Performance
4. **How would you handle 1 billion businesses?**
   - Database sharding by geohash
   - Separate read/write clusters
   - More aggressive caching
   - Elasticsearch for search

5. **How would you reduce search latency?**
   - Increase cache TTL
   - Pre-compute popular searches
   - Use faster database (SSD)
   - Add more read replicas

6. **How would you handle hot spots (popular cities)?**
   - Cache hot regions more aggressively
   - Dedicated shards for hot regions
   - Load balancer with geographic routing
   - CDN for static data

### Advanced Features
7. **How would you implement "search along route"?**
   - Accept list of coordinates (route polyline)
   - Create buffer around route
   - Find businesses within buffer
   - Use `ST_Buffer` and `ST_Within` in PostGIS

8. **How would you rank search results?**
   - Consider distance (primary)
   - Business rating/popularity
   - User preferences
   - Time of day (open/closed)
   - Sponsored results (ads)

9. **How would you implement autocomplete for business names?**
   - Trie data structure
   - Elasticsearch with prefix matching
   - Cache popular queries
   - Return top 10 suggestions

### Monitoring & Operations
10. **What metrics would you track?**
    - Search query latency (p50, p95, p99)
    - Cache hit rate
    - Database query performance
    - API endpoint response times
    - Error rates
    - QPS (queries per second)

11. **How would you debug slow queries?**
    - Query execution plans (EXPLAIN ANALYZE)
    - Database slow query log
    - Check index usage
    - Monitor cache hit rates
    - Distributed tracing

12. **How would you handle database failures?**
    - Read replicas for failover
    - Health checks
    - Automatic failover to replica
    - Circuit breaker pattern
    - Graceful degradation (cached results only)
