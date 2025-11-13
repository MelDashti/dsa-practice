# Design Google Maps

## 1. Problem Overview

Design a comprehensive mapping and navigation service like Google Maps that provides map data, turn-by-turn navigation, real-time traffic information, ETA calculations, route optimization, and location search. The system must serve billions of requests daily with accurate, real-time information.

**Key Challenges**:
- Store and serve global map data (roads, buildings, terrain)
- Real-time traffic data collection and processing
- Efficient route calculation (A* algorithm, Dijkstra's)
- ETA prediction with ML
- Map tile generation and serving
- Points of Interest (POI) search
- Multi-modal routing (driving, walking, transit, biking)

## 2. Requirements

### Functional Requirements
- **Map Display**: Show maps at multiple zoom levels
- **Navigation**: Turn-by-turn directions with voice guidance
- **Route Planning**: Calculate optimal routes (fastest, shortest, avoid tolls)
- **Real-time Traffic**: Show current traffic conditions
- **ETA Calculation**: Predict arrival time accurately
- **Location Search**: Find addresses, POIs, businesses
- **Street View**: 360° panoramic views
- **Satellite/Terrain Views**: Multiple map layers
- **Offline Maps**: Download maps for offline use

### Non-Functional Requirements
- **Availability**: 99.99% uptime
- **Latency**: < 200ms for map tiles, < 1s for routing
- **Scalability**: Handle 1B+ users, 50M+ QPS
- **Accuracy**: < 10 meter location accuracy, < 5% ETA error
- **Storage**: Petabytes of map data
- **Freshness**: Traffic updates every 1-2 minutes

## 3. Scale Estimation

### Traffic Estimates
- **Daily Active Users**: 1 billion
- **Map tile requests**: 50 billion/day
- **Routing requests**: 5 billion/day
- **Map tile QPS**: 50B / 86400 ≈ 580K QPS
- **Routing QPS**: 5B / 86400 ≈ 58K QPS
- **Peak**: 3x average = 1.7M tile QPS, 170K routing QPS

### Storage Estimates
- **Road network data**: ~10 TB (compressed)
- **Map tiles (all zoom levels)**: ~1 PB
- **Street View imagery**: ~100 PB
- **Satellite imagery**: ~50 PB
- **Traffic data (30 days)**: ~100 TB
- **Total**: ~150 PB

### Bandwidth Estimates
- **Map tiles**: 580K QPS × 50 KB (avg) = 29 GB/s
- **Routing responses**: 58K QPS × 5 KB = 290 MB/s
- **Total outbound**: ~30 GB/s

## 4. High-Level Design

```
┌───────────────────────────────────────────────────────────────┐
│                        Client Apps                             │
│            (Mobile, Web, Automotive, APIs)                     │
└────────────────────────┬──────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │    Global CDN       │
              │  (CloudFront/Akamai)│
              └──────────┬───────────┘
                         │
              ┌──────────┴──────────┐
              │  Load Balancer      │
              │ (Geographic Routing)│
              └──────────┬───────────┘
                         │
     ┌───────────────────┼──────────────────┬────────────────┐
     │                   │                  │                │
     ▼                   ▼                  ▼                ▼
┌──────────┐      ┌────────────┐    ┌────────────┐  ┌────────────┐
│   Map    │      │  Routing   │    │  Traffic   │  │   Search   │
│  Tiles   │      │  Service   │    │  Service   │  │  Service   │
│ Service  │      └─────┬──────┘    └──────┬─────┘  │(Geocoding) │
└────┬─────┘            │                  │        └──────┬─────┘
     │                  │                  │               │
     └──────────────────┴──────────────────┴───────────────┘
                        │
       ┌────────────────┼─────────────────────┬────────────┐
       ▼                ▼                     ▼            ▼
┌────────────┐   ┌────────────┐      ┌────────────┐  ┌─────────┐
│   Tile     │   │  Road      │      │  Traffic   │  │ POI DB  │
│  Storage   │   │  Network   │      │   Stream   │  │(Search) │
│   (S3)     │   │  Graph DB  │      │  (Kafka)   │  └─────────┘
└────────────┘   └────────────┘      └────────────┘
```

## 5. Core Components

### 1. Map Tile Service
- **Tile Generation**: Pre-render tiles at multiple zoom levels (0-22)
- **Tile Format**: Protocol Buffers (vector tiles) or PNG/JPG (raster)
- **Tile Addressing**: Slippy map tilenames (zoom/x/y)
- **Storage**: S3/Object storage with CDN
- **Dynamic Generation**: Render custom styles on-demand

### 2. Routing Service
- **Graph Database**: Store road network as weighted graph
- **Algorithms**: A*, Dijkstra's, Contraction Hierarchies
- **Multi-modal**: Different graphs for car, bike, walking, transit
- **Real-time Updates**: Incorporate live traffic data
- **Alternative Routes**: Calculate multiple route options

### 3. Traffic Service
- **Data Collection**: GPS from users, sensors, cameras
- **Processing**: Real-time stream processing (Kafka + Flink)
- **Prediction**: ML models for traffic forecasting
- **Aggregation**: Average speeds per road segment
- **Distribution**: Publish to routing service

### 4. ETA Service
- **Historical Data**: Travel times by time-of-day/day-of-week
- **Real-time Traffic**: Current conditions
- **ML Models**: Predict future conditions
- **Factors**: Weather, events, accidents, road closures

### 5. Search/Geocoding Service
- **Forward Geocoding**: Address → Coordinates
- **Reverse Geocoding**: Coordinates → Address
- **POI Search**: Find businesses, landmarks
- **Autocomplete**: Search suggestions
- **Elasticsearch**: Full-text search

## 6. Data Models

### Road Network Graph
```
Nodes (Intersections):
{
  "node_id": "node_12345",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "edges": ["edge_1", "edge_2", "edge_3"]
}

Edges (Road Segments):
{
  "edge_id": "edge_1",
  "from_node": "node_12345",
  "to_node": "node_67890",
  "distance_m": 150,
  "speed_limit_kmh": 50,
  "road_type": "residential",
  "one_way": false,
  "lanes": 2,
  "restrictions": ["no_trucks"],
  "average_speed_kmh": 35,
  "current_speed_kmh": 25
}
```

### Map Tiles
```
Tile Addressing: {z}/{x}/{y}.pbf
- z: Zoom level (0-22)
- x: Column (0 to 2^z - 1)
- y: Row (0 to 2^z - 1)

Zoom 0: 1 tile (whole world)
Zoom 10: 1,048,576 tiles
Zoom 18: 68.7 billion tiles
```

### Traffic Data
```
{
  "segment_id": "seg_abc123",
  "timestamp": 1699876543,
  "average_speed_kmh": 25,
  "sample_count": 45,
  "confidence": 0.85,
  "incidents": ["accident", "construction"]
}
```

## 7. Routing Algorithm

### A* Algorithm
```python
def a_star_routing(start_node, end_node, graph):
    open_set = PriorityQueue()
    open_set.put((0, start_node))

    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: heuristic(start_node, end_node)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == end_node:
            return reconstruct_path(came_from, current)

        for neighbor in graph.get_neighbors(current):
            # Calculate tentative g_score
            edge_weight = graph.get_edge_weight(current, neighbor)
            tentative_g = g_score[current] + edge_weight

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end_node)

                if neighbor not in [item[1] for item in open_set.queue]:
                    open_set.put((f_score[neighbor], neighbor))

    return None  # No path found

def heuristic(node1, node2):
    # Haversine distance (straight-line distance)
    return haversine_distance(
        node1.latitude, node1.longitude,
        node2.latitude, node2.longitude
    )
```

### Contraction Hierarchies (Optimization)
```python
# Pre-process graph to create shortcuts
def preprocess_graph(graph):
    # Contract nodes in order of importance
    # Create shortcuts to maintain shortest paths
    # Result: Hierarchical graph for faster queries

# Query using bidirectional search
def ch_route(start, end, ch_graph):
    # Forward search from start (upward)
    # Backward search from end (upward)
    # Meet in the middle
    # Much faster than plain A*
```

## 8. Real-time Traffic Processing

### Data Collection
```python
# Collect GPS points from users
class TrafficCollector:
    def process_gps_point(self, user_id, lat, lon, speed, timestamp):
        # Match to road segment
        segment = self.map_matcher.match_to_road(lat, lon)

        # Send to Kafka
        self.kafka.produce("traffic_data", {
            "segment_id": segment.id,
            "speed_kmh": speed,
            "timestamp": timestamp,
            "user_id": hash(user_id)  # Anonymized
        })
```

### Real-time Processing
```python
# Flink stream processing
def process_traffic_stream():
    # Tumbling window: 2 minutes
    stream = kafka_source("traffic_data")

    traffic_stats = stream \
        .key_by(lambda x: x["segment_id"]) \
        .window(TumblingEventTimeWindows.of(Time.minutes(2))) \
        .aggregate(AverageSpeedAggregator()) \
        .filter(lambda x: x["sample_count"] >= 10)  # Min samples

    # Update graph edge weights
    traffic_stats.add_sink(update_routing_graph)
```

### ETA Prediction with ML
```python
def predict_eta(route, departure_time):
    features = []

    for segment in route.segments:
        # Historical speed for this time
        hist_speed = get_historical_speed(
            segment.id,
            departure_time.hour,
            departure_time.weekday()
        )

        # Current traffic
        current_speed = get_current_speed(segment.id)

        # Weather, events, etc.
        contextual = get_contextual_features(segment, departure_time)

        features.append({
            "segment_id": segment.id,
            "distance": segment.distance,
            "hist_speed": hist_speed,
            "current_speed": current_speed,
            **contextual
        })

    # ML model predicts travel time for each segment
    segment_times = ml_model.predict(features)

    # Sum up total time
    total_time = sum(segment_times)

    return {
        "eta": departure_time + timedelta(seconds=total_time),
        "duration_seconds": total_time,
        "confidence": calculate_confidence(segment_times)
    }
```

## 9. Geospatial Indexing

### S2 Geometry (Google's Approach)
```python
from s2geometry import S2CellId, S2LatLng

# Index road segments by S2 cells
def index_road_segment(segment):
    # Get S2 cell at appropriate level
    start_latlng = S2LatLng.FromDegrees(
        segment.start_lat,
        segment.start_lon
    )

    cell = S2CellId.FromLatLng(start_latlng).parent(15)  # Level 15

    # Store in database
    db.index_segment(cell.id(), segment.id)

# Query nearby roads
def get_nearby_roads(lat, lon, radius_m):
    center = S2LatLng.FromDegrees(lat, lon)

    # Get covering cells
    cells = S2RegionCoverer.GetCovering(
        S2Cap.FromAxisAngle(center, radius_m)
    )

    # Query all cells
    segment_ids = []
    for cell in cells:
        segment_ids.extend(db.get_segments_in_cell(cell.id()))

    return segment_ids
```

### Tile Generation
```python
def generate_map_tile(zoom, x, y):
    # Calculate bounding box for tile
    bbox = tile_to_bbox(zoom, x, y)

    # Query road segments in bbox
    roads = db.query_roads_in_bbox(bbox)

    # Query POIs
    pois = db.query_pois_in_bbox(bbox)

    # Generate vector tile (Protocol Buffers)
    tile = mapbox_vector_tile.encode([
        {
            "name": "roads",
            "features": [road_to_feature(r) for r in roads]
        },
        {
            "name": "pois",
            "features": [poi_to_feature(p) for p in pois]
        }
    ])

    # Cache in S3
    s3.put_object(
        Bucket="map-tiles",
        Key=f"v1/{zoom}/{x}/{y}.pbf",
        Body=tile,
        ContentType="application/x-protobuf"
    )

    return tile
```

## 10. Scalability & Performance

### CDN Strategy
- **Edge Caching**: Cache tiles at edge locations (99% hit rate)
- **Regional Origins**: Tile servers in each region
- **Cache Headers**: Long TTL (1 year) with versioning
- **Pre-warming**: Pre-cache popular tiles

### Graph Partitioning
- **Geographic Partitioning**: Partition by region
- **Hierarchical Structure**: Country → State → City
- **Cross-partition Routes**: Handle edge cases
- **Replication**: Replicate border regions

### Database Optimization
- **Spatial Indexes**: R-tree, QuadTree for POI queries
- **Graph Database**: Neo4j, JanusGraph for road network
- **Time-series DB**: InfluxDB for traffic data
- **Caching**: Redis for hot segments

## 11. Trade-offs

### Vector Tiles vs Raster Tiles
**Chosen: Vector Tiles (Protocol Buffers)**
- Pros: Smaller size, client-side styling, smooth zoom
- Cons: More complex rendering
- Alternative: Raster (simpler, larger, fixed style)

### A* vs Contraction Hierarchies
**Chosen: Contraction Hierarchies for production**
- Pros: 1000x faster queries
- Cons: Complex pre-processing, storage overhead
- Alternative: A* (simpler, slower, no pre-processing)

### Real-time vs Batch Traffic Processing
**Chosen: Real-time with Lambda architecture**
- Pros: Fresh data, responsive
- Cons: Complex, expensive
- Alternative: Batch (simpler, delayed)

## 12. Follow-up Questions

1. **How would you handle map updates?**
   - Incremental updates from data providers
   - Crowdsourced corrections
   - Versioning system
   - Gradual rollout

2. **How would you implement turn-by-turn navigation?**
   - Calculate route
   - Generate instructions from graph
   - Voice synthesis
   - Re-routing on deviation

3. **How would you add public transit routing?**
   - GTFS data import
   - Time-dependent graph
   - Multi-modal routing
   - Real-time updates

4. **How would you detect traffic incidents automatically?**
   - Anomaly detection on speed drops
   - User reports
   - External data (police, news)
   - Computer vision on cameras

5. **How would you optimize for offline use?**
   - Download tile packages by region
   - Compressed road network graph
   - Pre-computed routes
   - Delta updates

6. **How would you scale to Mars?**
   - Different coordinate system
   - No real-time traffic
   - Limited connectivity
   - Terrain challenges
   - Navigation algorithms adapted for low gravity

7. **What metrics would you track?**
   - Tile load time (p50, p95, p99)
   - Route calculation time
   - ETA accuracy (MAPE)
   - Traffic data freshness
   - Navigation accuracy
   - User engagement

8. **How would you ensure accuracy?**
   - Multiple data sources
   - Crowdsourced verification
   - Manual review
   - ML quality checks
   - A/B testing
