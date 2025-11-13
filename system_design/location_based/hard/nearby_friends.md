# Design Nearby Friends (Real-time Location Tracking)

## 1. Problem Overview

Design a feature like Facebook's "Nearby Friends" or Apple's "Find My Friends" that allows users to share their real-time location with friends and see friends nearby. The system must handle continuous location updates, privacy controls, real-time notifications, and battery-efficient tracking.

**Key Challenges**:
- Continuous real-time location tracking
- Privacy and consent management
- Battery efficiency on mobile devices
- Scalable architecture for millions of users
- Real-time notifications when friends are nearby
- Location history and timeline

## 2. Requirements

### Functional Requirements
- **Location Sharing**: Users can enable/disable location sharing
- **Friend List**: View which friends are sharing location
- **Nearby Detection**: Alert when friends are nearby (e.g., within 1km)
- **Location Precision**: Control sharing precision (exact, approximate city)
- **Time Limit**: Share for specific duration (1 hour, 24 hours, until turned off)
- **Location History**: View own location timeline
- **Geofencing**: Alert when friend enters/leaves specific area
- **Battery Optimization**: Adaptive update frequency

### Non-Functional Requirements
- **Availability**: 99.9% uptime
- **Latency**: < 5 seconds for location updates to propagate
- **Privacy**: Strong encryption, granular controls
- **Scalability**: 100M users, 50M concurrent sharers
- **Battery**: < 5% battery drain per hour
- **Accuracy**: 10-50 meter precision

### Out of Scope
- Turn-by-turn navigation
- Group location sharing (family plans)
- Lost device finding
- Historical analytics

## 3. Scale Estimation

### Traffic Estimates
- **Total Users**: 100 million
- **Active Sharers (at any time)**: 50 million (50%)
- **Location update frequency**: Every 30 seconds (adaptive)
- **Updates per second**: 50M / 30 = 1.67M updates/sec
- **Nearby queries**: Every 2 minutes
- **Nearby QPS**: 50M / 120 = 417K QPS

### Storage Estimates
- **Location update**: 100 bytes
- **Daily updates per user**: 2,880 updates (every 30 sec × 86400 sec/day)
- **Daily storage**: 50M × 2,880 × 100 bytes = 14.4 TB/day
- **Retention (30 days)**: 432 TB
- **With compression**: 150 TB

### Bandwidth Estimates
- **Incoming**: 1.67M updates/sec × 100 bytes = 167 MB/s
- **Outgoing**: Similar + notifications = 200 MB/s

## 4. High-Level Design

```
┌──────────────────────────────────────────────────────────┐
│                    Client Apps                            │
│            (iOS, Android - Background Service)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS/WebSocket
                     ▼
          ┌──────────────────────┐
          │   Load Balancer      │
          └──────────┬───────────┘
                     │
      ┌──────────────┼──────────────┬──────────────┐
      │              │              │              │
      ▼              ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐
│ Location  │  │  Nearby   │  │  Friend  │  │  Notif.  │
│  Update   │  │  Service  │  │  Service │  │  Service │
│  Service  │  └─────┬─────┘  └────┬─────┘  └────┬─────┘
└─────┬─────┘        │             │             │
      │              │             │             │
      └──────────────┴─────────────┴─────────────┘
                     │
    ┌────────────────┼────────────────┬───────────┐
    │                │                │           │
    ▼                ▼                ▼           ▼
┌─────────┐   ┌────────────┐   ┌──────────┐  ┌──────────┐
│  Redis  │   │ PostgreSQL │   │  Kafka   │  │   S3     │
│(Geospatial)│ │ (Metadata) │   │ (Stream) │  │(History) │
└─────────┘   └────────────┘   └──────────┘  └──────────┘
```

## 5. API Design

### Enable Location Sharing
```
POST /api/v1/location/enable
{
  "duration_seconds": 3600,  // 1 hour, null for indefinite
  "precision": "exact",  // exact, approximate, city
  "visible_to": "friends"  // friends, specific_friends, family
}

Response:
{
  "session_id": "session_abc123",
  "enabled": true,
  "expires_at": "2024-11-12T13:34:56Z"
}
```

### Update Location
```
POST /api/v1/location/update
{
  "session_id": "session_abc123",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "accuracy_m": 10,
  "timestamp": 1699876543000,
  "battery_level": 45,
  "speed_mps": 5.5
}

Response:
{
  "success": true,
  "nearby_friends": [
    {
      "friend_id": "user_456",
      "distance_m": 250,
      "last_updated": 1699876540000
    }
  ]
}
```

### Get Nearby Friends
```
GET /api/v1/nearby-friends
Query:
  - radius_m: 5000 (default: 1000)

Response:
{
  "nearby_friends": [
    {
      "user_id": "user_456",
      "name": "Jane Doe",
      "profile_picture": "https://...",
      "location": {
        "latitude": 37.7739,
        "longitude": -122.4185
      },
      "distance_m": 250,
      "accuracy": "exact",
      "last_updated": 1699876540000,
      "is_moving": true
    }
  ],
  "count": 5
}
```

### Get Friend Location History
```
GET /api/v1/users/{user_id}/location-history
Query:
  - start_time: 1699800000
  - end_time: 1699886400
  - limit: 100

Response:
{
  "locations": [
    {
      "latitude": 37.7749,
      "longitude": -122.4194,
      "timestamp": 1699876543000,
      "activity": "walking"
    }
  ]
}
```

### Set Geofence Alert
```
POST /api/v1/geofence
{
  "name": "Home",
  "center": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "radius_m": 500,
  "alert_on": "enter",  // enter, exit, both
  "friends": ["user_456", "user_789"]
}

Response:
{
  "geofence_id": "geo_abc123",
  "active": true
}
```

## 6. Data Models

### User Location (Redis)
```
# Current location (hot data)
Key: location:{user_id}
Value: {
  "latitude": 37.7749,
  "longitude": -122.4194,
  "accuracy_m": 10,
  "timestamp": 1699876543000,
  "session_id": "session_abc",
  "precision": "exact",
  "battery_level": 45,
  "speed_mps": 5.5
}
TTL: 5 minutes (refreshed on update)

# Geospatial index (for proximity queries)
GEOADD user_locations -122.4194 37.7749 user_123
```

### Location Sharing Session (PostgreSQL)
```sql
CREATE TABLE location_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    enabled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    precision VARCHAR(20), -- exact, approximate, city
    visible_to VARCHAR(20), -- friends, specific_friends
    specific_friends JSONB,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_user_active ON location_sessions(user_id, is_active);
```

### Friendship (PostgreSQL)
```sql
CREATE TABLE friendships (
    user_id VARCHAR(64),
    friend_id VARCHAR(64),
    status VARCHAR(20), -- pending, accepted, blocked
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, friend_id)
);

CREATE INDEX idx_user_friends ON friendships(user_id, status);
```

### Location History (Time-series DB / S3)
```sql
-- TimescaleDB or similar
CREATE TABLE location_history (
    user_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    accuracy_m INT,
    activity VARCHAR(20), -- walking, driving, stationary
    battery_level INT
);

SELECT create_hypertable('location_history', 'timestamp');
CREATE INDEX idx_user_time ON location_history(user_id, timestamp DESC);
```

### Geofence (PostgreSQL)
```sql
CREATE TABLE geofences (
    geofence_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    name VARCHAR(100),
    center_lat DECIMAL(10, 8),
    center_lon DECIMAL(11, 8),
    radius_m INT,
    alert_on VARCHAR(20), -- enter, exit, both
    friends JSONB,
    is_active BOOLEAN DEFAULT true
);
```

## 7. Core Services Design

### Location Update Service
```python
class LocationUpdateService:
    def update_location(self, user_id, location_data):
        # Validate session
        session = self.get_active_session(user_id)
        if not session:
            raise UnauthorizedError("No active location sharing session")

        # Check if session expired
        if session.expires_at and session.expires_at < datetime.now():
            self.disable_session(session.session_id)
            raise SessionExpiredError()

        # Apply precision filter
        if session.precision == "approximate":
            # Round to 2 decimal places (~1km precision)
            location_data["latitude"] = round(location_data["latitude"], 2)
            location_data["longitude"] = round(location_data["longitude"], 2)
        elif session.precision == "city":
            # Return only city center
            location_data = self.get_city_center(
                location_data["latitude"],
                location_data["longitude"]
            )

        # Update Redis (current location)
        self.redis.setex(
            f"location:{user_id}",
            300,  # 5 minutes TTL
            json.dumps(location_data)
        )

        # Update geospatial index
        self.redis.geoadd(
            "user_locations",
            location_data["longitude"],
            location_data["latitude"],
            user_id
        )

        # Store in history (async)
        self.kafka.produce("location_updates", {
            "user_id": user_id,
            "location": location_data,
            "timestamp": current_timestamp_ms()
        })

        # Check geofences
        self.check_geofences(user_id, location_data)

        # Find nearby friends
        nearby = self.find_nearby_friends(user_id, location_data)

        return {"success": True, "nearby_friends": nearby}

    def check_geofences(self, user_id, location):
        # Get user's geofences
        geofences = self.get_active_geofences(user_id)

        for geo in geofences:
            distance = haversine_distance(
                location["latitude"],
                location["longitude"],
                geo.center_lat,
                geo.center_lon
            )

            # Check if crossed boundary
            prev_location = self.get_previous_location(user_id)
            prev_distance = haversine_distance(
                prev_location["latitude"],
                prev_location["longitude"],
                geo.center_lat,
                geo.center_lon
            ) if prev_location else float('inf')

            # Entered geofence
            if (distance <= geo.radius_m and
                prev_distance > geo.radius_m and
                geo.alert_on in ["enter", "both"]):

                self.send_geofence_alert(geo, user_id, "entered")

            # Exited geofence
            if (distance > geo.radius_m and
                prev_distance <= geo.radius_m and
                geo.alert_on in ["exit", "both"]):

                self.send_geofence_alert(geo, user_id, "exited")
```

### Nearby Friends Service
```python
class NearbyFriendsService:
    def find_nearby_friends(self, user_id, location, radius_m=1000):
        # Get user's friends who are sharing location
        friends = self.get_sharing_friends(user_id)

        # Search Redis geospatial index
        nearby = self.redis.georadius(
            "user_locations",
            location["longitude"],
            location["latitude"],
            radius_m, "m",
            withdist=True,
            count=50
        )

        # Filter to friends only
        nearby_friends = []
        for friend_id, distance in nearby:
            if friend_id in friends:
                friend_location = self.get_location(friend_id)

                if friend_location:
                    nearby_friends.append({
                        "user_id": friend_id,
                        "name": self.get_user_name(friend_id),
                        "location": {
                            "latitude": friend_location["latitude"],
                            "longitude": friend_location["longitude"]
                        },
                        "distance_m": round(distance, 2),
                        "accuracy": friend_location.get("accuracy_m", 0),
                        "last_updated": friend_location.get("timestamp"),
                        "is_moving": friend_location.get("speed_mps", 0) > 1
                    })

        # Check if any new friends became nearby (send notification)
        self.check_new_nearby_friends(user_id, nearby_friends)

        return nearby_friends

    def check_new_nearby_friends(self, user_id, current_nearby):
        # Get previously nearby friends
        prev_nearby = self.redis.smembers(f"nearby:{user_id}")

        # Find new nearby friends
        current_ids = {f["user_id"] for f in current_nearby}
        new_nearby = current_ids - prev_nearby

        # Send notifications for new nearby friends
        for friend_id in new_nearby:
            friend = next(f for f in current_nearby if f["user_id"] == friend_id)
            self.notification_service.send_nearby_alert(
                user_id,
                friend_id,
                friend["distance_m"]
            )

        # Update cache
        if current_ids:
            self.redis.delete(f"nearby:{user_id}")
            self.redis.sadd(f"nearby:{user_id}", *current_ids)
            self.redis.expire(f"nearby:{user_id}", 600)
```

## 8. Real-time Communication (WebSockets)

```python
class LocationWebSocketHandler:
    def on_connect(self, user_id, connection):
        # Store connection
        self.connections[user_id] = connection

        # Subscribe to friend location updates
        friends = self.get_friends(user_id)
        for friend_id in friends:
            self.redis.subscribe(f"location_updates:{friend_id}")

    def on_location_update(self, user_id, location):
        # Broadcast to friends
        friends = self.get_friends(user_id)

        for friend_id in friends:
            if friend_id in self.connections:
                # Check if friend can see this user
                if self.can_see_location(friend_id, user_id):
                    self.connections[friend_id].send({
                        "type": "friend_location_update",
                        "user_id": user_id,
                        "location": location,
                        "timestamp": current_timestamp_ms()
                    })
```

## 9. Battery Optimization

### Adaptive Update Frequency
```python
class AdaptiveLocationService:
    def determine_update_frequency(self, user_state):
        # Factors:
        # - Battery level
        # - Movement speed
        # - Nearby friends
        # - User preference

        battery = user_state["battery_level"]
        speed = user_state["speed_mps"]
        nearby_count = len(user_state["nearby_friends"])

        # Moving fast: update frequently
        if speed > 10:  # 36 km/h
            return 15  # 15 seconds

        # Nearby friends: update frequently
        if nearby_count > 0:
            return 30  # 30 seconds

        # Low battery: reduce frequency
        if battery < 20:
            return 300  # 5 minutes

        # Stationary: reduce frequency
        if speed < 0.5:  # ~1.8 km/h
            return 120  # 2 minutes

        # Default
        return 60  # 1 minute

    def should_skip_update(self, user_id, new_location):
        # Skip if moved less than threshold
        prev_location = self.get_previous_location(user_id)

        if prev_location:
            distance = haversine_distance(
                prev_location["latitude"],
                prev_location["longitude"],
                new_location["latitude"],
                new_location["longitude"]
            )

            # Skip if moved < 20 meters
            if distance < 20:
                return True

        return False
```

## 10. Scalability & Performance

### Geographic Sharding
```python
# Shard by geohash
def get_shard_for_location(lat, lon):
    geohash = gh.encode(lat, lon, precision=2)  # ~600km cells
    return hash(geohash) % NUM_SHARDS

# Route updates to appropriate shard
shard_id = get_shard_for_location(latitude, longitude)
redis_client = redis_cluster[shard_id]
```

### Caching Strategy
- **Current locations**: Redis (5 min TTL, refreshed on update)
- **Friend lists**: Redis (1 hour TTL)
- **Nearby results**: Redis (2 min TTL)

### Database Optimization
- **Time-series DB**: For location history (TimescaleDB)
- **Automatic archiving**: Move old data to S3 after 30 days
- **Compression**: Compress historical data

## 11. Privacy & Security

### Privacy Controls
- **Granular sharing**: Exact, approximate (city), custom
- **Time limits**: Auto-disable after duration
- **Friend-specific**: Share with specific friends only
- **Pause/Resume**: Temporarily disable without ending session

### Security Measures
- **Encryption**: TLS for transport, encrypted at rest
- **Authentication**: JWT tokens, refresh tokens
- **Anonymization**: Hash identifiers in logs
- **Audit logs**: Track all location access

## 12. Trade-offs

### Real-time Updates vs Battery Life
**Chosen: Adaptive frequency (30-300 seconds)**
- Pros: Balances real-time needs with battery
- Cons: Not truly real-time
- Alternative: Fixed high frequency (drains battery)

### Accuracy vs Privacy
**Chosen: User-controlled precision**
- Pros: User choice, flexible
- Cons: Complexity
- Alternative: Fixed precision (simpler, less flexible)

### Redis vs Database for Current Location
**Chosen: Redis**
- Pros: Fast, handles high write load
- Cons: Risk of data loss
- Alternative: Database (durable, slower)

## 13. Follow-up Questions

1. **How would you implement location history replay?**
   - Store timeline in time-series DB
   - Query by time range
   - Animate on map with timestamps

2. **How would you detect location spoofing?**
   - Validate speed between updates
   - Check GPS accuracy
   - Cross-reference with cell tower/WiFi
   - ML anomaly detection

3. **How would you support family location sharing?**
   - Family groups with automatic sharing
   - Enhanced privacy controls
   - Location history for minors
   - Emergency features

4. **How would you scale to 1B users?**
   - More geographic shards (1000+)
   - Regional deployment
   - Separate hot/cold data
   - Batch processing for analytics

5. **How would you reduce latency for global users?**
   - Multi-region deployment
   - Edge locations
   - Regional routing
   - Data replication

6. **What metrics would you track?**
   - Location update latency
   - Nearby query latency
   - Battery drain per hour
   - Location accuracy
   - User engagement
   - Privacy setting distribution
