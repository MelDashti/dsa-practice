# Design Uber (Ride-Hailing Service)

## 1. Problem Overview

Design a ride-hailing service like Uber that connects riders with drivers in real-time. The system must efficiently match riders with nearby drivers, track real-time locations, calculate ETAs, determine dynamic pricing, process payments, and provide trip history.

**Key Challenges**:
- Real-time location tracking for millions of drivers
- Efficient rider-driver matching algorithm
- Dynamic pricing (surge pricing)
- ETA calculation and route optimization
- Payment processing and split fares
- Scalable architecture for global operations

## 2. Requirements

### Functional Requirements
- **User Management**: Riders and drivers can register/login
- **Real-time Tracking**: Track driver locations continuously
- **Request Ride**: Riders can request rides with pickup location
- **Driver Matching**: Match riders with nearby available drivers
- **ETA Calculation**: Estimate arrival time for driver
- **Ride Tracking**: Track ongoing rides in real-time
- **Pricing**: Calculate fare based on distance, time, and demand
- **Payments**: Process payments, split fares, tipping
- **Ride History**: Store and retrieve past rides
- **Ratings**: Riders and drivers can rate each other

### Non-Functional Requirements
- **Availability**: 99.99% uptime
- **Latency**: < 3 seconds for driver matching
- **Scalability**: Support 100M+ users, 10M+ drivers
- **Consistency**: Eventually consistent for most data
- **Reliability**: No ride request loss
- **Real-time**: Location updates every 3-5 seconds

### Out of Scope
- Food delivery (Uber Eats)
- Package delivery
- Uber Pool (shared rides)
- Advanced driver scheduling

## 3. Scale Estimation

### Traffic Estimates
- **Total users**: 100 million
- **Total drivers**: 10 million
- **Daily active users**: 20 million
- **Daily active drivers**: 2 million
- **Average rides per day**: 10 million
- **Rides per second**: 10M / 86400 ≈ 116 RPS (average)
- **Peak RPS**: 350 RPS (3x average)

### Location Updates
- **Active drivers**: 2 million
- **Update frequency**: Every 4 seconds
- **Location updates per second**: 2M / 4 = 500K updates/sec

### Storage Estimates
- **Ride data**: 500 bytes per ride
- **Daily ride storage**: 10M × 500 bytes = 5 GB/day
- **Yearly storage**: 1.8 TB/year
- **Location history**: Store for 7 days = 35 GB

### Bandwidth Estimates
- **Location updates**: 500K/sec × 50 bytes = 25 MB/sec incoming
- **Real-time tracking**: Broadcast to riders = 25 MB/sec outgoing
- **Total**: ~50 MB/sec

## 4. High-Level Design

```
┌──────────────────────────────────────────────────────────────────┐
│                      Client Applications                          │
│              (Rider App, Driver App)                             │
└───────────────────┬──────────────────────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │   Load Balancer     │
         └──────────┬───────────┘
                    │
        ┌───────────┼────────────┬────────────────┐
        │           │            │                │
        ▼           ▼            ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│  User    │  │ Location │  │  Ride    │  │   Payment    │
│ Service  │  │ Service  │  │ Service  │  │   Service    │
└─────┬────┘  └─────┬────┘  └─────┬────┘  └───────┬──────┘
      │             │             │                │
      └─────────────┴─────────────┴────────────────┘
                    │
    ┌───────────────┼────────────────┬─────────────┐
    │               │                │             │
    ▼               ▼                ▼             ▼
┌─────────┐  ┌────────────┐  ┌────────────┐  ┌─────────┐
│ Matching│  │  Pricing   │  │Navigation  │  │ Notif.  │
│ Service │  │  Service   │  │ & Maps     │  │ Service │
└────┬────┘  └─────┬──────┘  └─────┬──────┘  └────┬────┘
     │             │               │              │
     └─────────────┴───────────────┴──────────────┘
                   │
       ┌───────────┼───────────────────┐
       ▼           ▼                   ▼
┌───────────┐  ┌──────────┐    ┌──────────────┐
│PostgreSQL │  │  Redis   │    │   Kafka      │
│(Metadata) │  │(Location)│    │(Events/Logs) │
└───────────┘  └──────────┘    └──────────────┘
```

## 5. API Design

### Request Ride
```
POST /api/v1/rides/request
{
  "rider_id": "user_123",
  "pickup_location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "address": "123 Main St, SF"
  },
  "dropoff_location": {
    "latitude": 37.7849,
    "longitude": -122.4294,
    "address": "456 Market St, SF"
  },
  "ride_type": "uber_x",  // uber_x, uber_xl, uber_black
  "payment_method_id": "pm_abc123"
}

Response:
{
  "ride_id": "ride_xyz789",
  "status": "searching",
  "estimated_wait_time": 3,  // minutes
  "estimated_price": {
    "min": 12.50,
    "max": 16.50,
    "currency": "USD",
    "surge_multiplier": 1.0
  }
}
```

### Update Driver Location
```
POST /api/v1/drivers/location
{
  "driver_id": "driver_456",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "bearing": 45,  // degrees
  "speed": 25,  // km/h
  "timestamp": 1699876543000
}

Response:
{
  "success": true
}
```

### Accept Ride (Driver)
```
POST /api/v1/rides/{ride_id}/accept
{
  "driver_id": "driver_456"
}

Response:
{
  "ride_id": "ride_xyz789",
  "rider": {
    "name": "John Doe",
    "phone": "+1-415-555-0123",
    "rating": 4.8
  },
  "pickup_location": {...},
  "dropoff_location": {...},
  "estimated_earnings": 15.00
}
```

### Track Ride (WebSocket)
```json
// Subscribe
{
  "action": "subscribe",
  "ride_id": "ride_xyz789",
  "user_id": "user_123"
}

// Location Updates
{
  "type": "location_update",
  "ride_id": "ride_xyz789",
  "driver_location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "eta": 2,  // minutes
  "timestamp": 1699876543000
}

// Status Updates
{
  "type": "status_update",
  "ride_id": "ride_xyz789",
  "status": "driver_arrived",  // driver_assigned, driver_arriving, driver_arrived, in_progress, completed
  "timestamp": 1699876543000
}
```

### Complete Ride
```
POST /api/v1/rides/{ride_id}/complete
{
  "driver_id": "driver_456",
  "final_location": {
    "latitude": 37.7849,
    "longitude": -122.4294
  },
  "distance_km": 5.2,
  "duration_minutes": 15
}

Response:
{
  "ride_id": "ride_xyz789",
  "fare": {
    "base_fare": 2.50,
    "distance_fare": 6.50,
    "time_fare": 3.00,
    "surge_multiplier": 1.0,
    "subtotal": 12.00,
    "tax": 1.20,
    "total": 13.20,
    "currency": "USD"
  },
  "payment_status": "processed"
}
```

## 6. Data Models

### User Table (PostgreSQL)
```sql
CREATE TABLE users (
    user_id VARCHAR(64) PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(100),
    user_type VARCHAR(10), -- rider, driver
    rating DECIMAL(3, 2),
    total_rides INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_phone ON users(phone_number);
CREATE INDEX idx_user_type ON users(user_type);
```

### Driver Table (PostgreSQL)
```sql
CREATE TABLE drivers (
    driver_id VARCHAR(64) PRIMARY KEY REFERENCES users(user_id),
    license_number VARCHAR(50) UNIQUE NOT NULL,
    vehicle_type VARCHAR(20), -- sedan, suv, premium
    vehicle_make VARCHAR(50),
    vehicle_model VARCHAR(50),
    vehicle_year INT,
    license_plate VARCHAR(20),
    status VARCHAR(20) DEFAULT 'offline', -- offline, online, on_ride
    current_location_lat DECIMAL(10, 8),
    current_location_lon DECIMAL(11, 8),
    last_location_update TIMESTAMP
);

CREATE INDEX idx_driver_status ON drivers(status);
```

### Ride Table (PostgreSQL)
```sql
CREATE TABLE rides (
    ride_id VARCHAR(64) PRIMARY KEY,
    rider_id VARCHAR(64) REFERENCES users(user_id),
    driver_id VARCHAR(64) REFERENCES drivers(driver_id),
    status VARCHAR(20) NOT NULL, -- requested, assigned, in_progress, completed, cancelled
    ride_type VARCHAR(20),

    pickup_lat DECIMAL(10, 8) NOT NULL,
    pickup_lon DECIMAL(11, 8) NOT NULL,
    pickup_address TEXT,

    dropoff_lat DECIMAL(10, 8),
    dropoff_lon DECIMAL(11, 8),
    dropoff_address TEXT,

    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    distance_km DECIMAL(10, 2),
    duration_minutes INT,
    fare_amount DECIMAL(10, 2),
    surge_multiplier DECIMAL(3, 2) DEFAULT 1.0,

    payment_method_id VARCHAR(64),
    payment_status VARCHAR(20)
);

CREATE INDEX idx_rider_rides ON rides(rider_id, requested_at DESC);
CREATE INDEX idx_driver_rides ON rides(driver_id, requested_at DESC);
CREATE INDEX idx_status ON rides(status);
```

### Redis Schemas

#### Driver Location (Geospatial)
```
# Redis Geospatial for driver locations
GEOADD drivers:online {longitude} {latitude} {driver_id}

# Example:
GEOADD drivers:online -122.4194 37.7749 driver_456

# Search nearby drivers
GEORADIUS drivers:online -122.4194 37.7749 5 km WITHDIST

# Driver metadata
Key: driver:{driver_id}:location
Value: {
  "latitude": 37.7749,
  "longitude": -122.4194,
  "bearing": 45,
  "speed": 25,
  "timestamp": 1699876543000,
  "status": "online"
}
TTL: 30 seconds (refreshed with each update)
```

#### Active Rides
```
Key: ride:{ride_id}
Value: {
  "status": "in_progress",
  "rider_id": "user_123",
  "driver_id": "driver_456",
  "pickup_location": {...},
  "dropoff_location": {...},
  "started_at": 1699876543000
}
TTL: 24 hours

# Driver's current ride
Key: driver:{driver_id}:current_ride
Value: ride_id
TTL: 24 hours
```

#### Ride Matching Queue
```
Key: matching_queue:{city}:{ride_type}
Value: List of ride_ids (sorted by request time)
```

## 7. Core Services Design

### Location Service
```python
class LocationService:
    def update_driver_location(self, driver_id, latitude, longitude, metadata):
        # Validate coordinates
        if not self.is_valid_coordinates(latitude, longitude):
            raise ValidationError("Invalid coordinates")

        # Update Redis geospatial index
        self.redis.geoadd(
            "drivers:online",
            longitude, latitude, driver_id
        )

        # Store detailed location data
        location_data = {
            "latitude": latitude,
            "longitude": longitude,
            "bearing": metadata.get("bearing"),
            "speed": metadata.get("speed"),
            "timestamp": current_timestamp_ms(),
            "status": self.get_driver_status(driver_id)
        }

        self.redis.setex(
            f"driver:{driver_id}:location",
            30,  # 30 seconds TTL
            json.dumps(location_data)
        )

        # If driver is on a ride, broadcast to rider
        current_ride = self.get_current_ride(driver_id)
        if current_ride:
            self.broadcast_location_to_rider(
                current_ride.rider_id,
                location_data
            )

        # Update database periodically (every minute)
        if self.should_persist_location(driver_id):
            self.db.execute("""
                UPDATE drivers
                SET current_location_lat = %s,
                    current_location_lon = %s,
                    last_location_update = NOW()
                WHERE driver_id = %s
            """, (latitude, longitude, driver_id))

    def find_nearby_drivers(self, latitude, longitude, radius_km, ride_type):
        # Search Redis geospatial index
        nearby = self.redis.georadius(
            "drivers:online",
            longitude, latitude,
            radius_km, "km",
            withdist=True,
            count=20  # Top 20 closest
        )

        # Filter by ride type and status
        available_drivers = []
        for driver_id, distance in nearby:
            # Check if driver is truly available
            driver_data = self.get_driver_data(driver_id)

            if (driver_data["status"] == "online" and
                driver_data.get("ride_type") == ride_type and
                not self.has_active_ride(driver_id)):

                available_drivers.append({
                    "driver_id": driver_id,
                    "distance_km": distance,
                    "location": {
                        "latitude": driver_data["latitude"],
                        "longitude": driver_data["longitude"]
                    },
                    "rating": driver_data.get("rating", 0)
                })

        # Sort by distance and rating
        available_drivers.sort(
            key=lambda d: (d["distance_km"], -d["rating"])
        )

        return available_drivers
```

### Matching Service
```python
class MatchingService:
    def match_ride(self, ride_request):
        ride_id = ride_request["ride_id"]
        pickup_location = ride_request["pickup_location"]
        ride_type = ride_request["ride_type"]

        # Find nearby available drivers
        nearby_drivers = self.location_service.find_nearby_drivers(
            pickup_location["latitude"],
            pickup_location["longitude"],
            radius_km=5,  # Start with 5km radius
            ride_type=ride_type
        )

        if not nearby_drivers:
            # Expand search radius
            nearby_drivers = self.location_service.find_nearby_drivers(
                pickup_location["latitude"],
                pickup_location["longitude"],
                radius_km=10,
                ride_type=ride_type
            )

        if not nearby_drivers:
            # No drivers available
            return None

        # Try to assign to drivers in order
        for driver in nearby_drivers[:5]:  # Try top 5
            success = self.offer_ride_to_driver(
                ride_id,
                driver["driver_id"],
                timeout=15  # 15 seconds to accept
            )

            if success:
                return driver["driver_id"]

        # If no driver accepts, return to queue
        return None

    def offer_ride_to_driver(self, ride_id, driver_id, timeout):
        # Send push notification to driver
        self.notification_service.send_ride_offer(driver_id, ride_id)

        # Wait for driver response (async)
        response = self.wait_for_driver_response(
            driver_id,
            ride_id,
            timeout
        )

        if response and response["accepted"]:
            # Driver accepted
            self.assign_ride(ride_id, driver_id)
            return True

        return False

    def assign_ride(self, ride_id, driver_id):
        # Update ride status
        self.db.execute("""
            UPDATE rides
            SET driver_id = %s,
                status = 'assigned',
                assigned_at = NOW()
            WHERE ride_id = %s
        """, (driver_id, ride_id))

        # Update driver status
        self.db.execute("""
            UPDATE drivers
            SET status = 'on_ride'
            WHERE driver_id = %s
        """, (driver_id,))

        # Store in Redis
        self.redis.setex(
            f"driver:{driver_id}:current_ride",
            86400,  # 24 hours
            ride_id
        )

        # Notify rider
        ride = self.get_ride(ride_id)
        driver = self.get_driver(driver_id)

        self.notification_service.notify_rider_driver_assigned(
            ride.rider_id,
            driver,
            estimated_eta=self.calculate_eta(
                driver["current_location"],
                ride["pickup_location"]
            )
        )
```

### Pricing Service
```python
class PricingService:
    def calculate_fare(self, ride):
        # Base fare by ride type
        base_fares = {
            "uber_x": 2.50,
            "uber_xl": 4.00,
            "uber_black": 8.00
        }

        base_fare = base_fares.get(ride["ride_type"], 2.50)

        # Distance fare
        distance_rate = 1.25  # per km
        distance_fare = ride["distance_km"] * distance_rate

        # Time fare
        time_rate = 0.20  # per minute
        time_fare = ride["duration_minutes"] * time_rate

        # Get surge multiplier
        surge = self.get_surge_multiplier(
            ride["pickup_location"],
            ride["requested_at"]
        )

        # Calculate subtotal
        subtotal = (base_fare + distance_fare + time_fare) * surge

        # Add taxes
        tax_rate = 0.10
        tax = subtotal * tax_rate

        total = subtotal + tax

        return {
            "base_fare": base_fare,
            "distance_fare": distance_fare,
            "time_fare": time_fare,
            "surge_multiplier": surge,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "currency": "USD"
        }

    def get_surge_multiplier(self, location, timestamp):
        # Get current demand in area (geohash)
        geohash = self.get_geohash(location, precision=5)

        # Count active ride requests in area
        active_requests = self.redis.get(
            f"surge:{geohash}:requests"
        ) or 0

        # Count available drivers in area
        available_drivers = self.redis.get(
            f"surge:{geohash}:drivers"
        ) or 1

        # Calculate demand/supply ratio
        ratio = int(active_requests) / max(int(available_drivers), 1)

        # Determine surge multiplier
        if ratio < 1:
            return 1.0
        elif ratio < 2:
            return 1.5
        elif ratio < 3:
            return 2.0
        elif ratio < 5:
            return 2.5
        else:
            return 3.0

    def estimate_fare(self, pickup, dropoff, ride_type):
        # Calculate distance and duration using external routing API
        route_info = self.navigation_service.get_route(pickup, dropoff)

        estimated_ride = {
            "ride_type": ride_type,
            "distance_km": route_info["distance_km"],
            "duration_minutes": route_info["duration_minutes"],
            "pickup_location": pickup,
            "requested_at": datetime.now()
        }

        fare = self.calculate_fare(estimated_ride)

        # Return range due to uncertainty
        return {
            "min": fare["total"] * 0.9,
            "max": fare["total"] * 1.1,
            "currency": fare["currency"],
            "surge_multiplier": fare["surge_multiplier"]
        }
```

### Ride Service
```python
class RideService:
    def request_ride(self, ride_request):
        # Create ride record
        ride_id = self.generate_ride_id()

        ride = {
            "ride_id": ride_id,
            "rider_id": ride_request["rider_id"],
            "status": "requested",
            "ride_type": ride_request["ride_type"],
            "pickup_lat": ride_request["pickup_location"]["latitude"],
            "pickup_lon": ride_request["pickup_location"]["longitude"],
            "pickup_address": ride_request["pickup_location"]["address"],
            "dropoff_lat": ride_request["dropoff_location"]["latitude"],
            "dropoff_lon": ride_request["dropoff_location"]["longitude"],
            "dropoff_address": ride_request["dropoff_location"]["address"],
            "payment_method_id": ride_request["payment_method_id"]
        }

        # Store in database
        self.db.insert_ride(ride)

        # Get fare estimate
        fare_estimate = self.pricing_service.estimate_fare(
            ride_request["pickup_location"],
            ride_request["dropoff_location"],
            ride_request["ride_type"]
        )

        # Add to matching queue
        self.redis.lpush(
            f"matching_queue:{self.get_city(ride['pickup_lat'])}:{ride['ride_type']}",
            ride_id
        )

        # Trigger matching (async)
        self.matching_service.match_ride_async(ride)

        return {
            "ride_id": ride_id,
            "status": "searching",
            "estimated_price": fare_estimate,
            "estimated_wait_time": self.estimate_wait_time(ride)
        }

    def complete_ride(self, ride_id, completion_data):
        # Update ride record
        self.db.execute("""
            UPDATE rides
            SET status = 'completed',
                completed_at = NOW(),
                distance_km = %s,
                duration_minutes = %s
            WHERE ride_id = %s
        """, (
            completion_data["distance_km"],
            completion_data["duration_minutes"],
            ride_id
        ))

        # Get ride details
        ride = self.get_ride(ride_id)

        # Calculate final fare
        fare = self.pricing_service.calculate_fare(ride)

        # Process payment
        payment_result = self.payment_service.charge(
            ride["rider_id"],
            fare["total"],
            ride["payment_method_id"]
        )

        # Update payment status
        self.db.execute("""
            UPDATE rides
            SET fare_amount = %s,
                payment_status = %s
            WHERE ride_id = %s
        """, (fare["total"], payment_result["status"], ride_id))

        # Update driver status
        self.db.execute("""
            UPDATE drivers
            SET status = 'online'
            WHERE driver_id = %s
        """, (ride["driver_id"],))

        # Clear Redis cache
        self.redis.delete(f"driver:{ride['driver_id']}:current_ride")

        return {
            "ride_id": ride_id,
            "fare": fare,
            "payment_status": payment_result["status"]
        }
```

## 8. Real-time Communication (WebSockets)

```python
class RideTrackingGateway:
    def on_connect(self, user_id, connection):
        # Store connection
        self.connections[user_id] = connection

        # If user has active ride, start sending updates
        active_ride = self.get_active_ride(user_id)
        if active_ride:
            self.subscribe_to_ride_updates(user_id, active_ride.ride_id)

    def subscribe_to_ride_updates(self, user_id, ride_id):
        # Subscribe to Redis pub/sub for ride updates
        self.redis.subscribe(f"ride:{ride_id}:updates")

    def broadcast_location_update(self, ride_id, location):
        # Publish to Redis
        self.redis.publish(
            f"ride:{ride_id}:updates",
            json.dumps({
                "type": "location_update",
                "location": location,
                "timestamp": current_timestamp_ms()
            })
        )

        # Send to connected clients
        ride = self.get_ride(ride_id)
        for user_id in [ride.rider_id, ride.driver_id]:
            if user_id in self.connections:
                self.connections[user_id].send(location)
```

## 9. Geospatial Indexing

### Redis Geospatial Commands
```python
# Add driver location
redis.geoadd("drivers:online", longitude, latitude, driver_id)

# Find nearby drivers within 5km
nearby = redis.georadius(
    "drivers:online",
    -122.4194, 37.7749,  # Search center
    5, "km",             # Radius
    withdist=True,       # Include distance
    count=20             # Limit results
)

# Get driver location
location = redis.geopos("drivers:online", driver_id)

# Calculate distance between two drivers
distance = redis.geodist(
    "drivers:online",
    driver_id_1, driver_id_2,
    "km"
)

# Remove driver (when offline)
redis.zrem("drivers:online", driver_id)
```

### Geohash for Surge Pricing
```python
import geohash2

# Encode location to geohash (precision 5 ≈ 5km×5km)
gh = geohash2.encode(latitude, longitude, precision=5)

# Track demand/supply by geohash
redis.hincrby(f"surge:{gh}", "requests", 1)
redis.hincrby(f"surge:{gh}", "drivers", num_drivers)
```

## 10. Scalability & Performance

### Database Sharding
- **Shard by city/region**: Partition rides by geographic area
- **User sharding**: Partition users by user_id hash
- **Time-based partitioning**: Partition old rides by month

### Redis Optimization
- **Geospatial sharding**: Separate Redis instances per city
- **Read replicas**: For location queries
- **Connection pooling**: Reuse connections

### Load Balancing
- **Geographic routing**: Route to nearest data center
- **Consistent hashing**: For Redis sharding
- **Service mesh**: For inter-service communication

## 11. Trade-offs

### Redis Geospatial vs PostGIS
**Chosen: Redis Geospatial**
- Pros: Fast in-memory, perfect for real-time
- Cons: Limited persistence, no complex queries
- Alternative: PostGIS (persistent, complex queries, slower)

### Matching Algorithm
**Chosen: Sequential offer to nearby drivers**
- Pros: Simple, fair
- Cons: Can be slow if many rejections
- Alternative: Broadcast to all (faster, more complex)

### Payment Processing
**Chosen: Immediate charge on completion**
- Pros: Simple, instant confirmation
- Cons: Can fail, user experience impact
- Alternative: Pre-authorization + settle later

## 12. Follow-up Questions

### Functional Enhancements
1. **How would you implement Uber Pool (shared rides)?**
   - Match multiple riders with similar routes
   - Route optimization for pickups/dropoffs
   - Dynamic pricing based on detour
   - Passenger coordination

2. **How would you add scheduled rides?**
   - Store in database with scheduled time
   - Cron job to trigger matching
   - Pre-assign drivers
   - Confirmation flow

3. **How would you implement driver heat maps?**
   - Aggregate demand data by area
   - Historical analysis
   - Predictive modeling
   - Real-time updates

### Scale & Performance
4. **How would you handle 10x more drivers?**
   - More Redis shards
   - Regional clusters
   - Lazy loading of driver data
   - Better indexing

5. **How would you reduce matching latency?**
   - Pre-compute nearby drivers
   - Parallel driver offers
   - Predictive matching
   - Cache optimization

6. **How would you optimize for emerging markets (low connectivity)?**
   - SMS-based interface
   - Offline mode
   - Data compression
   - Simplified features

### Reliability & Security
7. **How would you prevent fraud?**
   - ML-based anomaly detection
   - GPS validation
   - Driver verification
   - Payment fraud detection

8. **How would you ensure safety?**
   - Real-time trip monitoring
   - Emergency button
   - Share trip with contacts
   - Background checks

9. **How would you handle payment disputes?**
   - Audit trail
   - GPS verification
   - Manual review process
   - Refund policies

### Monitoring & Operations
10. **What metrics would you track?**
    - Matching success rate
    - Average wait time
    - Driver utilization
    - Surge pricing effectiveness
    - Payment success rate
    - Ride completion rate

11. **How would you debug incorrect fare calculations?**
    - Log all fare components
    - Route replay
    - Audit trails
    - Unit tests for edge cases

12. **How would you perform A/B testing on pricing?**
    - User segmentation
    - Treatment/control groups
    - Statistical analysis
    - Gradual rollout
