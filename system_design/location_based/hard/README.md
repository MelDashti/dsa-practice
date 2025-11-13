# Hard - Location-Based Services

This directory contains advanced location-based system design problems that involve complex algorithms, massive scale, real-time processing, and sophisticated infrastructure. These problems require deep understanding of geospatial systems, distributed architectures, and optimization techniques.

## Problems

### 1. Google Maps (`design_google_maps.md`)
Design a comprehensive mapping and navigation service with global coverage, real-time traffic, and turn-by-turn directions.

**Key Concepts**:
- Map tile generation and serving (vector/raster)
- Road network graph storage and querying
- A* and Contraction Hierarchies routing algorithms
- Real-time traffic data collection and processing
- ETA prediction with machine learning
- S2 Geometry for global indexing
- Multi-modal routing (car, transit, bike, walk)
- Street View and satellite imagery

**Extreme Scale**:
- 1B+ users, 50M+ QPS
- Petabytes of map data
- Global coverage with regional optimization
- Real-time traffic from millions of sources

### 2. Nearby Friends (`nearby_friends.md`)
Design a real-time location sharing feature that tracks friends' locations with privacy controls and battery optimization.

**Key Concepts**:
- Continuous real-time location tracking
- Adaptive update frequency for battery optimization
- Privacy and consent management
- Geofencing and proximity alerts
- Location history and timeline
- WebSocket for real-time updates
- Activity recognition (walking, driving, stationary)

**Challenges**:
- 50M concurrent location sharers
- 1.67M location updates/second
- Sub-5-second propagation latency
- Battery efficiency (< 5% drain/hour)
- Privacy and security at scale

## Common Patterns in Hard Location Problems

### Advanced Geospatial Indexing

#### S2 Geometry (Google's Approach)
```python
from s2geometry import S2CellId, S2LatLng, S2RegionCoverer

# Hierarchical cell-based indexing
def index_location_s2(lat, lon, level=15):
    latlng = S2LatLng.FromDegrees(lat, lon)
    cell = S2CellId.FromLatLng(latlng).parent(level)
    return cell.id()

# Query with cell covering
def query_nearby_s2(lat, lon, radius_m):
    center = S2LatLng.FromDegrees(lat, lon)
    cap = S2Cap.FromAxisAngle(center, radius_m)

    coverer = S2RegionCoverer()
    covering = coverer.GetCovering(cap)

    # Query all covered cells
    results = []
    for cell in covering:
        results.extend(db.query_cell(cell.id()))

    return results
```

#### QuadTree for Hierarchical Partitioning
```python
class QuadTree:
    def __init__(self, bounds, capacity=100, depth=0, max_depth=8):
        self.bounds = bounds
        self.capacity = capacity
        self.depth = depth
        self.max_depth = max_depth
        self.entities = []
        self.divided = False
        self.children = [None, None, None, None]

    def insert(self, entity):
        if not self.contains(entity):
            return False

        if len(self.entities) < self.capacity or self.depth >= self.max_depth:
            self.entities.append(entity)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(entity):
                return True

    def query_range(self, range_bbox):
        results = []

        if not self.intersects(range_bbox):
            return results

        for entity in self.entities:
            if range_bbox.contains(entity):
                results.append(entity)

        if self.divided:
            for child in self.children:
                results.extend(child.query_range(range_bbox))

        return results
```

### Routing Algorithms

#### A* with Heuristic
```python
def a_star(start, goal, graph):
    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in graph.neighbors(current):
            tentative_g = g_score[current] + graph.weight(current, neighbor)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                open_set.put((f_score[neighbor], neighbor))

    return None

def heuristic(node, goal):
    # Haversine distance (great-circle distance)
    return haversine_distance(
        node.lat, node.lon,
        goal.lat, goal.lon
    )
```

#### Contraction Hierarchies (Production Optimization)
```python
# Preprocessing: Contract graph
def preprocess_ch(graph):
    # Order nodes by importance (e.g., degree)
    order = compute_node_ordering(graph)

    shortcuts = []
    for node in order:
        # Find all node pairs connected through this node
        for u in graph.incoming(node):
            for v in graph.outgoing(node):
                if u == v:
                    continue

                # Check if path through node is shortest
                direct_dist = graph.distance(u, v)
                via_node_dist = graph.distance(u, node) + graph.distance(node, v)

                if direct_dist > via_node_dist:
                    # Add shortcut
                    shortcuts.append((u, v, via_node_dist))

        # Remove node from graph
        graph.remove_node(node)

    return shortcuts

# Query: Bidirectional search on hierarchical graph
def ch_query(start, goal, ch_graph):
    # Forward search from start (upward only)
    forward = dijkstra_upward(start, ch_graph)

    # Backward search from goal (upward only)
    backward = dijkstra_upward(goal, ch_graph.reverse())

    # Find minimum distance node
    best_dist = float('inf')
    best_node = None

    for node in set(forward.keys()) & set(backward.keys()):
        dist = forward[node] + backward[node]
        if dist < best_dist:
            best_dist = dist
            best_node = node

    # Reconstruct path
    return reconstruct_ch_path(start, goal, best_node, forward, backward)
```

### Real-time Stream Processing

#### Traffic Data Pipeline
```python
# Kafka + Flink for real-time traffic processing
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import TumblingEventTimeWindows

env = StreamExecutionEnvironment.get_execution_environment()

# Kafka source
traffic_stream = env.add_source(
    FlinkKafkaConsumer(
        topics=['gps_updates'],
        deserialization_schema=JsonSchema(),
        properties={'bootstrap.servers': 'kafka:9092'}
    )
)

# Map GPS points to road segments
traffic_stream = traffic_stream.map(
    lambda gps: map_to_road_segment(gps)
)

# Window and aggregate
traffic_stats = traffic_stream \
    .key_by(lambda x: x['segment_id']) \
    .window(TumblingEventTimeWindows.of(Time.minutes(2))) \
    .aggregate(TrafficAggregator())

# Sink to update graph weights
traffic_stats.add_sink(update_graph_weights)

env.execute("Traffic Processing")
```

### ML for ETA Prediction
```python
import tensorflow as tf

class ETAPredictor:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        # Neural network for ETA prediction
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(feature_dim,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1)  # Predicted travel time
        ])

        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )

        return model

    def extract_features(self, route, departure_time):
        features = []

        for segment in route:
            # Historical data
            hist_speed = get_historical_speed(
                segment.id,
                departure_time.hour,
                departure_time.weekday()
            )

            # Current conditions
            current_speed = get_current_speed(segment.id)
            traffic_level = get_traffic_level(segment.id)

            # Contextual features
            weather = get_weather(segment.location)
            is_rush_hour = departure_time.hour in [7, 8, 9, 17, 18, 19]
            day_of_week = departure_time.weekday()

            features.append([
                segment.distance,
                segment.speed_limit,
                hist_speed,
                current_speed,
                traffic_level,
                weather.temperature,
                weather.precipitation,
                is_rush_hour,
                day_of_week
            ])

        return np.array(features)

    def predict_eta(self, route, departure_time):
        features = self.extract_features(route, departure_time)

        # Predict time for each segment
        segment_times = self.model.predict(features)

        # Sum for total ETA
        total_time = np.sum(segment_times)

        return {
            "eta": departure_time + timedelta(seconds=total_time),
            "duration_seconds": int(total_time),
            "confidence": self.calculate_confidence(segment_times)
        }
```

## Architectural Patterns

### Multi-Region Architecture
```
Region: US-EAST          Region: EU-WEST         Region: ASIA-PAC
┌──────────────┐         ┌──────────────┐        ┌──────────────┐
│ Map Tiles    │         │ Map Tiles    │        │ Map Tiles    │
│ Routing      │◄────────┤ Routing      │───────►│ Routing      │
│ Traffic      │  Sync   │ Traffic      │  Sync  │ Traffic      │
└──────────────┘         └──────────────┘        └──────────────┘
       │                        │                       │
       └────────────────────────┴───────────────────────┘
                                │
                         ┌──────▼──────┐
                         │ Global CDN  │
                         └─────────────┘
```

### Lambda Architecture for Traffic
```
┌─────────────────┐
│  GPS Sources    │
└────────┬────────┘
         │
    ┌────┴─────┐
    │  Kafka   │
    └────┬─────┘
         │
    ┌────┴─────────────────┐
    │                      │
    ▼                      ▼
┌──────────┐          ┌──────────┐
│  Speed   │          │  Batch   │
│  Layer   │          │  Layer   │
│ (Flink)  │          │ (Spark)  │
└────┬─────┘          └────┬─────┘
     │                     │
     └──────────┬──────────┘
                ▼
         ┌─────────────┐
         │  Serving    │
         │   Layer     │
         └─────────────┘
```

## Key Technical Decisions

### Map Storage & Serving
| Aspect | Choice | Reasoning |
|--------|--------|-----------|
| Tile Format | Vector (Protocol Buffers) | Smaller size, client styling, smooth zoom |
| Storage | S3 + CloudFront CDN | Scalable, durable, global delivery |
| Generation | Pre-rendered + On-demand | Balance performance and flexibility |

### Routing
| Aspect | Choice | Reasoning |
|--------|--------|-----------|
| Algorithm | Contraction Hierarchies | 1000x faster than A* |
| Graph Storage | Distributed graph DB | Scalable, partitionable |
| Updates | Incremental with versioning | No downtime, rollback capability |

### Real-time Location
| Aspect | Choice | Reasoning |
|--------|--------|-----------|
| Storage | Redis Geospatial | Fast, in-memory, built-in geo commands |
| Updates | Adaptive frequency | Battery efficiency |
| Sync | WebSocket | Real-time, bidirectional |

## Performance Optimization Techniques

### 1. Tile Pre-generation and Caching
- Pre-render tiles for zoom levels 0-14
- On-demand for 15-22
- CDN caching with 1-year TTL
- Lazy loading and progressive enhancement

### 2. Route Caching
```python
def get_route(start, end, options):
    # Cache key includes rounded coordinates
    cache_key = f"route:{round_coords(start)}:{round_coords(end)}:{options}"

    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    route = calculate_route(start, end, options)

    # Cache for 5 minutes
    redis.setex(cache_key, 300, json.dumps(route))

    return route
```

### 3. Graph Partitioning
- Partition by geographic region
- Replicate border areas
- Route planning across partitions
- Minimize cross-partition queries

### 4. Location Update Batching
```python
# Batch multiple updates
def batch_location_updates(updates):
    pipeline = redis.pipeline()

    for update in updates:
        pipeline.geoadd(
            "user_locations",
            update['longitude'],
            update['latitude'],
            update['user_id']
        )

        pipeline.setex(
            f"location:{update['user_id']}",
            300,
            json.dumps(update)
        )

    pipeline.execute()
```

## Interview Tips for Hard Problems

### 1. Start with Scope (5-10 min)
- **Clarify scale**: Millions vs billions of users
- **Geographic scope**: City, country, global
- **Real-time requirements**: Seconds vs minutes
- **Accuracy requirements**: Meters vs kilometers

### 2. High-Level Architecture (10-15 min)
- **Draw comprehensive diagram**
- **Identify all major components**
- **Show data flow**
- **Label technologies**

### 3. Deep Dive (20-25 min)
Choose 2-3 areas for detailed design:
- **Algorithms**: Routing, matching, prediction
- **Data structures**: Graphs, spatial indexes
- **Scalability**: Sharding, caching, CDN
- **Real-time**: Stream processing, WebSockets

### 4. Advanced Topics (10-15 min)
- **ML integration**: ETA prediction, traffic forecasting
- **Edge cases**: Border crossing, multi-region
- **Failure scenarios**: Partition tolerance, graceful degradation
- **Cost optimization**: CDN, storage tiering

### 5. Metrics & Operations (5 min)
- **Performance metrics**: Latency, throughput, accuracy
- **Business metrics**: User engagement, completion rates
- **Operational metrics**: Error rates, system health

## Common Follow-up Questions

### Algorithmic
1. **Compare A* vs Dijkstra vs Contraction Hierarchies**
2. **How to handle dynamic road closures in real-time?**
3. **How to optimize multi-stop route planning?**

### Scale
4. **How to scale to 10x traffic?**
5. **How to reduce latency for global users?**
6. **How to handle Black Friday / major event traffic spikes?**

### Advanced
7. **How to implement multi-modal routing (car + train)?**
8. **How to predict traffic 1 hour in advance?**
9. **How to detect and avoid traffic congestion proactively?**

### Privacy & Security
10. **How to ensure location data privacy?**
11. **How to detect and prevent location spoofing?**
12. **How to comply with GDPR for location data?**

## Additional Resources

### Papers & Articles
- "Contraction Hierarchies: Faster and Simpler Hierarchical Routing"
- "Google's S2 Library: Spherical Geometry"
- "Uber's H3: Hexagonal hierarchical spatial index"
- "OpenStreetMap: Collaborative Mapping"

### Technologies
- **Routing**: OSRM, GraphHopper, Valhalla
- **Map Rendering**: Mapbox GL, OpenLayers
- **Spatial Databases**: PostGIS, MongoDB Geospatial
- **Stream Processing**: Apache Flink, Kafka Streams
- **Graph Databases**: Neo4j, JanusGraph

### Industry Blogs
- Google Maps Platform Blog
- Uber Engineering Blog
- Lyft Engineering Blog
- Apple Maps Engineering

## Progression Path

1. **Easy**: Understand basic proximity search
2. **Medium**: Add real-time tracking and matching
3. **Hard**: Global scale with routing, traffic, ML
4. **Expert**: Autonomous vehicles, 3D mapping, AR navigation
