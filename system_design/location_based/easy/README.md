# Easy - Location-Based Services

This directory contains foundational location-based system design problems that focus on core geospatial concepts and basic proximity search.

## Problems

### 1. Simple Nearby Businesses (`design_yelp_simple.md`)
Design a basic service to find businesses near a given location.

**Key Concepts**:
- Geospatial data storage
- Proximity search algorithms
- PostGIS spatial indexing
- Latitude/Longitude coordinates
- Distance calculations (Haversine formula)

**Learning Objectives**:
- Understanding geospatial indexing
- PostGIS vs Geohash approaches
- Basic proximity queries
- Caching location-based searches

**Prerequisites**:
- Basic SQL and database design
- Understanding of coordinates (lat/long)
- Indexing concepts
- API design

## Common Patterns in Easy Location Problems

### Geospatial Data Storage
- **PostGIS Extension**: PostgreSQL with spatial capabilities
- **GEOGRAPHY vs GEOMETRY**: Geography for Earth coordinates
- **Point Data Type**: Store latitude/longitude as point

### Spatial Indexing
- **GIST Index**: Generalized Search Tree for spatial data
- **Bounding Box**: Quick filtering before distance calculation
- **R-tree**: Underlying structure for spatial index

### Distance Calculation
```sql
-- Using PostGIS
ST_Distance(
    location1::geography,
    location2::geography
) / 1000  -- Convert meters to kilometers
```

### Proximity Search
```sql
-- Find points within radius
ST_DWithin(
    location::geography,
    search_point::geography,
    radius_in_meters
)
```

### Alternative: Geohash
- **Geohash Encoding**: Convert lat/long to base32 string
- **Precision Levels**: Higher precision = smaller area
- **Neighbor Finding**: Get adjacent geohash cells
- **Prefix Matching**: Quick proximity filter

## Basic Architecture
```
Client → Load Balancer → API Server → Database (PostGIS)
                                    → Redis Cache
```

## Key SQL Patterns

### Create Spatial Table
```sql
CREATE EXTENSION postgis;

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location GEOGRAPHY(POINT, 4326),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

-- Spatial index
CREATE INDEX idx_location ON locations USING GIST(location);
```

### Insert Location
```sql
INSERT INTO locations (name, location, latitude, longitude)
VALUES (
    'Starbucks',
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326),
    37.7749,
    -122.4194
);
```

### Search Within Radius
```sql
SELECT
    name,
    ST_Distance(
        location::geography,
        ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography
    ) / 1000 AS distance_km
FROM locations
WHERE ST_DWithin(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
    5000  -- 5km in meters
)
ORDER BY distance_km
LIMIT 20;
```

## Progression to Medium Level

After mastering easy problems, medium-level problems introduce:
- Real-time location tracking
- Moving entities (drivers, vehicles)
- Matching algorithms (riders to drivers)
- Route optimization
- Complex business logic (pricing, ETA)
- Higher scale requirements

## Tips for System Design Interviews

1. **Clarify Coordinates**: Confirm using lat/long (WGS84)
2. **Distance Units**: Specify kilometers or miles
3. **Earth is Not Flat**: Use geography, not geometry
4. **Index Everything**: Spatial indexes are crucial
5. **Cache Smartly**: Location searches are cacheable
6. **Round Coordinates**: For better cache hit rates

## Common Interview Questions

### Basic Questions
- How do you store geospatial data?
- How do you find nearby points efficiently?
- What is a spatial index?
- How do you calculate distance between two points?

### Performance Questions
- How do you optimize proximity searches?
- When would you use caching?
- How do you handle millions of locations?
- What's the complexity of spatial queries?

## Additional Resources

- PostGIS Documentation
- Geohash Algorithm
- Haversine Formula
- R-tree Data Structure
- Spatial Database Patterns
