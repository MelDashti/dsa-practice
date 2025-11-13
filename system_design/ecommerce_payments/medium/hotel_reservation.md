# Design Hotel Reservation System

## 1. Problem Statement

Design a hotel booking platform like Booking.com or Expedia that allows users to search for hotels, view availability, check room details, make reservations, and manage bookings. The system must handle concurrent bookings, prevent overbooking, support dynamic pricing, and integrate with multiple hotels and payment providers.

**Key Features:**
- Search hotels by location, dates, guests
- Filter by amenities, price, rating
- View room types and availability
- Real-time pricing
- Booking and payment
- Booking management (modify, cancel)
- Reviews and ratings
- Hotel management dashboard
- Multi-currency support

## 2. Requirements

### Functional Requirements

1. **Search & Discovery**
   - Search hotels by city, address, landmarks
   - Filter by price, star rating, amenities, guest rating
   - Sort by price, rating, distance, popularity
   - Map view with location
   - Date and guest count selection

2. **Hotel & Room Management**
   - Hotel details (name, address, amenities, policies)
   - Multiple room types (single, double, suite)
   - Room features and amenities
   - High-quality images
   - Check-in/check-out times
   - Cancellation policies

3. **Availability & Pricing**
   - Real-time room availability
   - Dynamic pricing (season, demand, duration)
   - Discounts and deals
   - Group booking rates
   - Taxes and fees breakdown

4. **Booking Flow**
   - Select dates and rooms
   - View total price breakdown
   - Guest information
   - Special requests
   - Payment processing
   - Booking confirmation
   - E-ticket/voucher generation

5. **Booking Management**
   - View booking details
   - Modify booking (dates, rooms)
   - Cancel booking
   - Partial cancellations
   - Refund processing

6. **Reviews & Ratings**
   - Post-stay reviews
   - Rating categories (cleanliness, service, value)
   - Photo uploads
   - Verified bookings
   - Hotel responses

7. **User Management**
   - User registration and login
   - Profile management
   - Booking history
   - Saved hotels (wishlist)
   - Loyalty programs

8. **Hotel Partner Dashboard**
   - Inventory management
   - Pricing updates
   - Booking notifications
   - Revenue analytics
   - Review management

### Non-Functional Requirements

1. **Performance**
   - Search results < 500ms
   - Booking completion < 2 seconds
   - Support 100K concurrent users
   - Handle 1M searches per day

2. **Availability**
   - 99.95% uptime
   - Multi-region deployment
   - Graceful degradation

3. **Consistency**
   - Strong consistency for bookings (no overbooking)
   - Eventual consistency for hotel listings
   - ACID transactions for payments

4. **Scalability**
   - Support 500K+ hotels
   - 10M+ rooms
   - 50M+ users
   - Peak season traffic (3-5x)

5. **Reliability**
   - No double bookings
   - Data durability (11 nines)
   - Automated backups
   - Disaster recovery

6. **Security**
   - PCI DSS compliance
   - Data encryption
   - Fraud detection
   - GDPR compliance

## 3. Scale Estimation

### Traffic Estimates
- **Daily Active Users (DAU):** 5 million
- **Monthly Active Users (MAU):** 20 million
- **Peak concurrent users:** 50K
- **Searches per day:** 10 million
- **Bookings per day:** 500K

### Transaction Estimates
- **Conversion rate:** 5% (search to booking)
- **Average nights:** 3
- **Average room rate:** $150/night
- **Average booking value:** $450
- **Daily GMV:** $225 million
- **Commission (15%):** $33.75 million/day

### Storage Estimates
- **Hotels:** 500K hotels × 100 KB = 50 GB
- **Rooms:** 10M rooms × 50 KB = 500 GB
- **Images:** 10M rooms × 5 images × 500 KB = 25 TB
- **Users:** 20M users × 5 KB = 100 GB
- **Bookings:** 500K/day × 365 days × 20 KB = 3.6 TB/year
- **Reviews:** 10M reviews × 2 KB = 20 GB
- **Total (Year 1):** ~30 TB

### Bandwidth Estimates
- **Incoming:** 500K bookings × 50 KB = 25 GB/day
- **Outgoing:**
  - Search results: 10M searches × 200 KB = 2 TB/day
  - Images (CDN): 50M requests × 500 KB = 25 TB/day
- **Total:** ~27 TB/day

### Cache Estimates
- **Hot hotels:** 10K hotels × 100 KB = 1 GB
- **Popular searches:** 100K searches × 50 KB = 5 GB
- **Room availability:** 100K rooms × 10 KB = 1 GB
- **User sessions:** 50K sessions × 20 KB = 1 GB
- **Total cache:** ~8 GB

## 4. High-Level Architecture

```
                          ┌──────────────┐
                          │    Client    │
                          │ (Web/Mobile) │
                          └──────┬───────┘
                                 │
                          ┌──────▼───────┐
                          │     CDN      │
                          │  CloudFront  │
                          └──────┬───────┘
                                 │
                          ┌──────▼───────┐
                          │     API      │
                          │   Gateway    │
                          └──────┬───────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
 ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
 │    Search     │      │   Booking     │      │     User      │
 │   Service     │      │   Service     │      │   Service     │
 └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
         │                       │                       │
         ▼                       ▼                       ▼
 ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
 │    Hotel      │      │   Inventory   │      │  Pricing      │
 │   Service     │      │   Service     │      │  Service      │
 └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
         │                       │                       │
         ▼                       ▼                       ▼
 ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
 │    Review     │      │   Payment     │      │ Notification  │
 │   Service     │      │   Service     │      │   Service     │
 └───────────────┘      └───────────────┘      └───────────────┘

                        Data Layer
┌──────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │PostgreSQL│  │PostgreSQL│  │PostgreSQL│  │  Redis   │ │
│  │ (Hotels) │  │(Bookings)│  │  (Users) │  │ (Cache)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   S3     │  │  Kafka   │  │   SQS    │  │Elasticsearch│
│  │ (Images) │  │ (Events) │  │ (Queue)  │  │ (Search) │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────┘

                External Services
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Stripe  │  │  Email   │  │   SMS    │  │   Maps   │
│ Payment  │  │ Service  │  │ Service  │  │  (Google)│
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 5. API Design

### Search APIs

```
GET /api/v1/hotels/search
Query Parameters:
  - city: string (required)
  - checkIn: date (required, YYYY-MM-DD)
  - checkOut: date (required)
  - guests: int (default: 1)
  - rooms: int (default: 1)
  - minPrice: decimal
  - maxPrice: decimal
  - starRating: int[] (e.g., [3,4,5])
  - amenities: string[] (e.g., ["wifi", "pool", "parking"])
  - sort: string (price_asc, price_desc, rating, distance)
  - page: int
  - limit: int

Response: 200 OK
{
  "searchId": "uuid",
  "checkIn": "2025-11-15",
  "checkOut": "2025-11-18",
  "nights": 3,
  "results": [
    {
      "hotelId": "uuid",
      "name": "Grand Hotel NYC",
      "starRating": 4,
      "guestRating": 8.5,
      "reviewCount": 1234,
      "address": "123 5th Ave, New York, NY 10001",
      "latitude": 40.7589,
      "longitude": -73.9851,
      "thumbnail": "url",
      "amenities": ["wifi", "pool", "gym", "parking"],
      "lowestPrice": 299.99,
      "currency": "USD",
      "available": true,
      "distance": 2.5 // km from search center
    }
  ],
  "totalResults": 245,
  "page": 1,
  "filters": {
    "priceRange": {"min": 50, "max": 500},
    "starRatings": [
      {"rating": 5, "count": 20},
      {"rating": 4, "count": 80}
    ],
    "amenities": [
      {"name": "wifi", "count": 200},
      {"name": "pool", "count": 150}
    ]
  }
}

GET /api/v1/hotels/{hotelId}
Response: 200 OK
{
  "hotelId": "uuid",
  "name": "Grand Hotel NYC",
  "description": "...",
  "starRating": 4,
  "guestRating": 8.5,
  "reviewCount": 1234,
  "address": {...},
  "location": {"latitude": 40.7589, "longitude": -73.9851},
  "amenities": [...],
  "policies": {
    "checkIn": "15:00",
    "checkOut": "11:00",
    "cancellation": "Free cancellation until 24 hours before check-in",
    "childPolicy": "Children of all ages welcome",
    "petPolicy": "Pets not allowed"
  },
  "images": ["url1", "url2", ...],
  "contactInfo": {
    "phone": "+1-212-555-0100",
    "email": "info@grandhotel.com",
    "website": "www.grandhotel.com"
  },
  "nearbyAttractions": [
    {"name": "Central Park", "distance": 0.5}
  ]
}

GET /api/v1/hotels/{hotelId}/rooms?checkIn={date}&checkOut={date}&guests={int}
Response: 200 OK
{
  "hotelId": "uuid",
  "checkIn": "2025-11-15",
  "checkOut": "2025-11-18",
  "nights": 3,
  "rooms": [
    {
      "roomTypeId": "uuid",
      "name": "Deluxe King Room",
      "description": "Spacious room with king bed",
      "maxOccupancy": 2,
      "bedType": "1 King Bed",
      "size": 35, // square meters
      "amenities": ["wifi", "tv", "minibar", "safe"],
      "images": ["url1", "url2"],
      "available": 5, // number of rooms available
      "pricing": {
        "basePrice": 299.99,
        "nightlyRates": [
          {"date": "2025-11-15", "price": 299.99},
          {"date": "2025-11-16", "price": 299.99},
          {"date": "2025-11-17", "price": 349.99}
        ],
        "subtotal": 949.97,
        "taxes": 94.99,
        "fees": 30.00,
        "total": 1074.96,
        "currency": "USD"
      },
      "cancellationPolicy": "Free until 2025-11-14 23:59"
    }
  ]
}
```

### Booking APIs

```
POST /api/v1/bookings
Request:
{
  "hotelId": "uuid",
  "roomTypeId": "uuid",
  "checkIn": "2025-11-15",
  "checkOut": "2025-11-18",
  "rooms": [
    {
      "adults": 2,
      "children": 0,
      "guests": [
        {
          "firstName": "John",
          "lastName": "Doe",
          "email": "john@example.com",
          "phone": "+1234567890"
        }
      ]
    }
  ],
  "specialRequests": "Late check-in",
  "paymentMethod": {
    "type": "credit_card",
    "token": "pm_xxx"
  },
  "promoCode": "SAVE10"
}

Response: 201 Created
{
  "bookingId": "uuid",
  "confirmationNumber": "BKG-2025-001234",
  "status": "confirmed",
  "hotel": {...},
  "room": {...},
  "checkIn": "2025-11-15",
  "checkOut": "2025-11-18",
  "nights": 3,
  "guests": [...],
  "pricing": {
    "subtotal": 949.97,
    "discount": 94.99,
    "taxes": 94.99,
    "fees": 30.00,
    "total": 979.97,
    "currency": "USD"
  },
  "paymentStatus": "completed",
  "cancellationDeadline": "2025-11-14T23:59:00Z",
  "voucher": "base64-pdf",
  "bookedAt": "2025-11-12T10:00:00Z"
}

GET /api/v1/bookings/{bookingId}
Response: 200 OK (same as create response)

GET /api/v1/users/{userId}/bookings?status={status}&page={page}
Response: 200 OK
{
  "bookings": [...],
  "pagination": {...}
}

PUT /api/v1/bookings/{bookingId}
Request:
{
  "checkIn": "2025-11-16", // modified
  "checkOut": "2025-11-19"  // modified
}
Response: 200 OK (updated booking)

POST /api/v1/bookings/{bookingId}/cancel
Request:
{
  "reason": "Change of plans"
}
Response: 200 OK
{
  "bookingId": "uuid",
  "status": "cancelled",
  "refundAmount": 949.97,
  "refundStatus": "processing",
  "cancelledAt": "2025-11-13T10:00:00Z"
}
```

### Review APIs

```
POST /api/v1/hotels/{hotelId}/reviews
Request:
{
  "bookingId": "uuid",
  "overallRating": 8.5,
  "ratings": {
    "cleanliness": 9,
    "service": 8,
    "value": 8,
    "location": 9
  },
  "title": "Great stay!",
  "comment": "...",
  "images": ["base64..."]
}
Response: 201 Created

GET /api/v1/hotels/{hotelId}/reviews?page={page}&sort={sort}
Response: 200 OK
{
  "hotelId": "uuid",
  "averageRating": 8.5,
  "totalReviews": 1234,
  "ratingBreakdown": {
    "5": 500,
    "4": 400,
    "3": 200,
    "2": 100,
    "1": 34
  },
  "reviews": [
    {
      "reviewId": "uuid",
      "userId": "uuid",
      "userName": "John D.",
      "overallRating": 8.5,
      "ratings": {...},
      "title": "Great stay!",
      "comment": "...",
      "images": ["url1"],
      "verifiedBooking": true,
      "stayDate": "2025-10-15",
      "createdAt": "2025-10-20T10:00:00Z",
      "helpfulCount": 15,
      "hotelResponse": {
        "comment": "Thank you for your feedback!",
        "respondedAt": "2025-10-21T10:00:00Z"
      }
    }
  ],
  "pagination": {...}
}
```

### Hotel Partner APIs

```
POST /api/v1/partner/hotels
PUT /api/v1/partner/hotels/{hotelId}
POST /api/v1/partner/hotels/{hotelId}/rooms
PUT /api/v1/partner/rooms/{roomTypeId}/inventory
PUT /api/v1/partner/rooms/{roomTypeId}/pricing
GET /api/v1/partner/bookings?hotelId={hotelId}
GET /api/v1/partner/analytics/revenue
```

## 6. Database Schema

### Hotels Table
```sql
CREATE TABLE hotels (
    hotel_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    description TEXT,
    star_rating INT,
    address JSONB NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    amenities JSONB, -- ["wifi", "pool", "gym"]
    policies JSONB,
    contact_info JSONB,
    average_rating DECIMAL(3, 2) DEFAULT 0,
    review_count INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    partner_id UUID REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_location (latitude, longitude),
    INDEX idx_status (status),
    INDEX idx_partner (partner_id),
    FULLTEXT idx_search (name, description)
);
```

### Hotel_Images Table
```sql
CREATE TABLE hotel_images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    image_type VARCHAR(20), -- exterior, lobby, room, amenity
    display_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_hotel (hotel_id)
);
```

### Room_Types Table
```sql
CREATE TABLE room_types (
    room_type_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    max_occupancy INT NOT NULL,
    bed_type VARCHAR(100),
    size_sqm DECIMAL(10, 2),
    amenities JSONB,
    total_rooms INT NOT NULL, -- total inventory for this room type
    base_price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_hotel (hotel_id),
    INDEX idx_status (status),
    CONSTRAINT chk_occupancy CHECK (max_occupancy > 0),
    CONSTRAINT chk_rooms CHECK (total_rooms > 0)
);
```

### Room_Type_Images Table
```sql
CREATE TABLE room_type_images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_type_id UUID NOT NULL REFERENCES room_types(room_type_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    display_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_room_type (room_type_id)
);
```

### Room_Inventory Table (Daily availability)
```sql
CREATE TABLE room_inventory (
    inventory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_type_id UUID NOT NULL REFERENCES room_types(room_type_id),
    date DATE NOT NULL,
    available_rooms INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL, -- dynamic price for this date
    min_stay_nights INT DEFAULT 1,
    max_stay_nights INT,
    status VARCHAR(20) DEFAULT 'available', -- available, blocked
    version INT DEFAULT 0, -- for optimistic locking
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(room_type_id, date),
    INDEX idx_room_date (room_type_id, date),
    INDEX idx_date (date),
    CONSTRAINT chk_available CHECK (available_rooms >= 0)
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    booking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    confirmation_number VARCHAR(50) UNIQUE NOT NULL,
    user_id UUID REFERENCES users(user_id),
    hotel_id UUID NOT NULL REFERENCES hotels(hotel_id),
    room_type_id UUID NOT NULL REFERENCES room_types(room_type_id),
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    nights INT NOT NULL,
    num_rooms INT NOT NULL DEFAULT 1,
    num_adults INT NOT NULL,
    num_children INT DEFAULT 0,
    guest_info JSONB NOT NULL,
    special_requests TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    subtotal DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    taxes DECIMAL(10, 2) NOT NULL,
    fees DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    promo_code VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending',
    cancellation_deadline TIMESTAMP,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    refund_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_hotel (hotel_id),
    INDEX idx_dates (check_in, check_out),
    INDEX idx_status (status),
    INDEX idx_confirmation (confirmation_number),
    CONSTRAINT chk_dates CHECK (check_out > check_in),
    CONSTRAINT chk_nights CHECK (nights = check_out - check_in),
    CONSTRAINT chk_status CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed', 'no_show'))
);
```

### Booking_Rooms Table (For multi-room bookings)
```sql
CREATE TABLE booking_rooms (
    booking_room_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    room_number VARCHAR(20), -- assigned by hotel
    adults INT NOT NULL,
    children INT DEFAULT 0,
    guest_names JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_booking (booking_id)
);
```

### Payments Table
```sql
CREATE TABLE payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL REFERENCES bookings(booking_id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(50) NOT NULL,
    payment_gateway VARCHAR(50),
    transaction_id VARCHAR(255) UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_booking (booking_id),
    INDEX idx_transaction (transaction_id),
    INDEX idx_status (status)
);
```

### Reviews Table
```sql
CREATE TABLE reviews (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL REFERENCES hotels(hotel_id),
    user_id UUID NOT NULL REFERENCES users(user_id),
    booking_id UUID NOT NULL REFERENCES bookings(booking_id),
    overall_rating DECIMAL(3, 2) NOT NULL,
    cleanliness_rating INT,
    service_rating INT,
    value_rating INT,
    location_rating INT,
    title VARCHAR(255),
    comment TEXT,
    verified_booking BOOLEAN DEFAULT TRUE,
    stay_date DATE,
    helpful_count INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(booking_id), -- one review per booking
    INDEX idx_hotel (hotel_id),
    INDEX idx_user (user_id),
    INDEX idx_rating (overall_rating),
    INDEX idx_created (created_at),
    CONSTRAINT chk_rating CHECK (overall_rating BETWEEN 0 AND 10)
);
```

### Review_Images Table
```sql
CREATE TABLE review_images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    review_id UUID NOT NULL REFERENCES reviews(review_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_review (review_id)
);
```

### Promo_Codes Table
```sql
CREATE TABLE promo_codes (
    promo_code_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    discount_type VARCHAR(20), -- percentage, flat
    discount_value DECIMAL(10, 2) NOT NULL,
    min_nights INT,
    min_amount DECIMAL(10, 2),
    max_discount DECIMAL(10, 2),
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    usage_limit INT,
    used_count INT DEFAULT 0,
    applicable_hotels JSONB, -- specific hotels or null for all
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_dates (valid_from, valid_until)
);
```

### ACID Considerations

1. **Booking Transaction:**
   - Check availability
   - Create booking
   - Decrement inventory
   - Process payment
   - All atomic

2. **Inventory Management:**
   - Optimistic locking with version numbers
   - Prevent overbooking
   - Handle concurrent reservations

3. **Cancellation:**
   - Update booking status
   - Release inventory
   - Process refund
   - Audit trail

4. **Pricing Updates:**
   - Eventual consistency acceptable
   - Validate price at booking time
   - Lock price during checkout

## 7. Core Components

### 7.1 Search Service
**Technology:** Elasticsearch

**Features:**
- Location-based search
- Full-text search
- Faceted filtering
- Geo-spatial queries
- Sorting and ranking

**Index Schema:**
```json
{
  "hotels": {
    "hotelId": "uuid",
    "name": "Grand Hotel",
    "location": {"lat": 40.7589, "lon": -73.9851},
    "starRating": 4,
    "guestRating": 8.5,
    "amenities": ["wifi", "pool"],
    "lowestPrice": 299.99,
    "available": true
  }
}
```

**Query Example:**
```json
{
  "query": {
    "bool": {
      "must": [
        {"geo_distance": {
          "distance": "10km",
          "location": {"lat": 40.7589, "lon": -73.9851}
        }}
      ],
      "filter": [
        {"range": {"lowestPrice": {"gte": 100, "lte": 500}}},
        {"terms": {"starRating": [4, 5]}},
        {"term": {"available": true}}
      ]
    }
  },
  "sort": [
    {"_geo_distance": {"location": {"lat": 40.7589, "lon": -73.9851}, "order": "asc"}}
  ]
}
```

### 7.2 Hotel Service
**Responsibilities:**
- Hotel CRUD operations
- Hotel details
- Amenities management
- Partner onboarding

**Caching:**
- Cache hotel details (TTL: 1 hour)
- Cache amenities list (TTL: 1 day)

### 7.3 Inventory Service
**Critical Component** - Manages room availability

**Key Challenges:**
- Concurrent bookings
- Prevent overbooking
- Real-time availability

**Availability Check:**
```sql
SELECT ri.date, ri.available_rooms, ri.price
FROM room_inventory ri
WHERE ri.room_type_id = ?
  AND ri.date >= ?
  AND ri.date < ?
  AND ri.status = 'available'
  AND ri.available_rooms > 0
ORDER BY ri.date;

-- All dates must have availability
-- If any date missing or 0 rooms, not available
```

**Inventory Reservation:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Check and lock inventory for all dates
SELECT inventory_id, available_rooms, version
FROM room_inventory
WHERE room_type_id = ?
  AND date >= ?
  AND date < ?
FOR UPDATE;

-- Verify all dates have availability
-- If not, ROLLBACK

-- Decrement inventory for each date
UPDATE room_inventory
SET available_rooms = available_rooms - :num_rooms,
    version = version + 1,
    updated_at = NOW()
WHERE room_type_id = ?
  AND date = ?
  AND available_rooms >= :num_rooms
  AND version = :expected_version;

-- If affected rows != expected, ROLLBACK (someone else booked)

COMMIT;
```

**Inventory Release (Cancellation):**
```sql
UPDATE room_inventory
SET available_rooms = available_rooms + :num_rooms,
    updated_at = NOW()
WHERE room_type_id = ?
  AND date >= :check_in
  AND date < :check_out;
```

### 7.4 Pricing Service
**Responsibilities:**
- Dynamic pricing
- Seasonal pricing
- Demand-based pricing
- Promo code application

**Pricing Factors:**
- Base price
- Season (peak/off-peak)
- Occupancy rate
- Days until check-in
- Length of stay
- Special events

**Calculation:**
```python
def calculate_price(room_type, check_in, check_out):
    base_price = room_type.base_price
    prices = []

    for date in date_range(check_in, check_out):
        # Check inventory table for date-specific price
        daily_price = get_inventory_price(room_type.id, date)

        if not daily_price:
            # Calculate dynamic price
            daily_price = base_price
            daily_price *= get_seasonal_multiplier(date)
            daily_price *= get_demand_multiplier(room_type.id, date)
            daily_price *= get_advance_booking_multiplier(days_until(date))

        prices.append((date, daily_price))

    subtotal = sum(price for _, price in prices)
    return {
        "nightlyRates": prices,
        "subtotal": subtotal,
        "taxes": subtotal * 0.10,
        "fees": 30.00,
        "total": subtotal + taxes + fees
    }
```

### 7.5 Booking Service
**Workflow:**

```
1. Validate Inputs
   - Check dates (check_in < check_out)
   - Verify hotel and room type exist
   - Validate guest info

2. Check Availability
   - Query inventory service
   - Verify rooms available for all dates

3. Calculate Pricing
   - Get latest prices
   - Apply promo code
   - Calculate taxes and fees

4. BEGIN TRANSACTION
   a. Create booking record
   b. Reserve inventory (decrement)
   c. Process payment
   d. Generate confirmation
   e. Create voucher
5. COMMIT (or ROLLBACK on failure)

6. Post-Booking (Async)
   - Send confirmation email
   - Send SMS
   - Notify hotel
   - Update analytics
```

**Idempotency:**
- Use request ID to prevent duplicate bookings
- Store in Redis with 24-hour TTL

### 7.6 Payment Service
**Features:**
- Multiple payment methods
- Multi-currency support
- Payment gateway integration
- Refund processing
- PCI compliance

**Payment Flow:**
1. Client gets payment token from Stripe
2. Server creates booking with "pending" payment
3. Charge payment gateway
4. Update payment status
5. Update booking status
6. Send confirmation

**Refund Logic:**
```python
def process_refund(booking):
    # Check cancellation policy
    if booking.cancelled_at > booking.cancellation_deadline:
        refund_amount = 0  # No refund
    elif booking.check_in - booking.cancelled_at > 7 days:
        refund_amount = booking.total  # Full refund
    else:
        refund_amount = booking.total * 0.8  # 20% fee

    # Process refund via payment gateway
    payment = get_payment(booking.id)
    refund = stripe.Refund.create(
        payment_intent=payment.transaction_id,
        amount=refund_amount * 100  # cents
    )

    # Update booking
    update_booking(booking.id, {
        "status": "cancelled",
        "refund_amount": refund_amount
    })

    return refund_amount
```

### 7.7 Review Service
**Responsibilities:**
- Review submission
- Review moderation
- Rating aggregation
- Review responses (hotel)

**Rating Aggregation:**
```sql
-- Update hotel rating after new review
UPDATE hotels
SET average_rating = (
    SELECT AVG(overall_rating)
    FROM reviews
    WHERE hotel_id = ? AND status = 'published'
),
review_count = (
    SELECT COUNT(*)
    FROM reviews
    WHERE hotel_id = ? AND status = 'published'
)
WHERE hotel_id = ?;
```

**Moderation:**
- AI-based spam detection
- Profanity filter
- Manual review queue

### 7.8 Notification Service
**Triggers:**
- Booking confirmation
- Payment receipt
- Pre-arrival reminder (24 hours)
- Check-in instructions
- Cancellation confirmation
- Review request (post-stay)

**Channels:**
- Email (SendGrid)
- SMS (Twilio)
- Push notifications
- In-app notifications

## 8. Transaction Management & Consistency

### Booking Transaction (Critical Path)

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Validate room availability with lock
SELECT date, available_rooms, version
FROM room_inventory
WHERE room_type_id = :room_type_id
  AND date >= :check_in
  AND date < :check_out
FOR UPDATE;

-- Application validates all dates have availability

-- 2. Create booking
INSERT INTO bookings (
    confirmation_number, user_id, hotel_id, room_type_id,
    check_in, check_out, nights, num_rooms,
    subtotal, taxes, fees, total, status, payment_status
)
VALUES (
    :confirmation, :user_id, :hotel_id, :room_type_id,
    :check_in, :check_out, :nights, :num_rooms,
    :subtotal, :taxes, :fees, :total, 'pending', 'pending'
)
RETURNING booking_id;

-- 3. Decrement inventory for each date
UPDATE room_inventory
SET available_rooms = available_rooms - :num_rooms,
    version = version + 1,
    updated_at = NOW()
WHERE room_type_id = :room_type_id
  AND date >= :check_in
  AND date < :check_out
  AND available_rooms >= :num_rooms;

-- Check rows affected matches number of nights
-- If not, ROLLBACK

-- 4. Create booking rooms
INSERT INTO booking_rooms (booking_id, adults, children, guest_names)
VALUES (:booking_id, :adults, :children, :guest_names);

-- 5. Process payment (within transaction or saga pattern)
INSERT INTO payments (booking_id, amount, payment_method, status)
VALUES (:booking_id, :total, :payment_method, 'processing');

COMMIT;

-- 6. Call payment gateway (outside transaction)
-- 7. Update payment and booking status
-- 8. Send notifications (async)
```

### Handling Concurrent Bookings

**Scenario:** Two users try to book the last room simultaneously

**Solution 1: Pessimistic Locking**
```sql
-- First transaction acquires lock
SELECT * FROM room_inventory WHERE ... FOR UPDATE;
-- Second transaction waits

-- First transaction books
UPDATE room_inventory SET available_rooms = 0;
COMMIT;

-- Second transaction now sees 0 rooms, fails gracefully
```

**Solution 2: Optimistic Locking**
```sql
-- Both read simultaneously
SELECT available_rooms, version FROM room_inventory;
-- Both see: available_rooms=1, version=5

-- Transaction 1 updates first
UPDATE room_inventory
SET available_rooms = 0, version = 6
WHERE version = 5;
-- Succeeds, 1 row affected

-- Transaction 2 tries
UPDATE room_inventory
SET available_rooms = 0, version = 6
WHERE version = 5;  -- No longer matches
-- Fails, 0 rows affected

-- Application retries or shows "no longer available"
```

### Saga Pattern for Payment

```
1. Reserve Inventory (compensate: release inventory)
2. Create Booking (compensate: delete booking)
3. Charge Payment (compensate: refund payment)
4. Confirm Booking (compensate: cancel booking)
5. Send Notification (no compensation, best effort)
```

## 9. Security Considerations

### Payment Security
- **PCI DSS Level 1** compliance
- **Tokenization** via Stripe
- **Never store** card details
- **3D Secure** authentication
- **Fraud detection:**
  - Velocity checks
  - Geolocation anomalies
  - Device fingerprinting

### Data Protection
- **Encryption at rest:** AES-256
- **Encryption in transit:** TLS 1.3
- **PII encryption:** Guest information
- **GDPR compliance:**
  - Right to access
  - Right to deletion
  - Data portability

### Access Control
- **JWT authentication**
- **Role-based access:**
  - Guest: booking, reviews
  - Hotel Partner: inventory, pricing
  - Admin: full access

### Fraud Prevention
- **Fake bookings:**
  - Require credit card pre-authorization
  - Flag suspicious patterns
- **Fake reviews:**
  - Verified booking badge
  - Review moderation

## 10. Scalability

### Database Scaling

**Sharding:**
```
Bookings: Shard by user_id (consistent hashing)
Hotels: Shard by geographic region
Inventory: Co-locate with hotels shard
Reviews: Shard by hotel_id
```

**Read Replicas:**
- Route searches to replicas
- Route bookings to primary

**Caching:**
```
Redis Cluster:
- Hotel details (1 hour TTL)
- Search results (5 min TTL)
- Room availability (2 min TTL)
- Pricing (5 min TTL)
```

### Search Scaling

**Elasticsearch Cluster:**
- 3 master nodes
- 10 data nodes
- 5 shards, 2 replicas

**Index Optimization:**
- Separate index for each region
- Alias for global search

### Handling Peak Season

**Strategies:**
1. **Pre-warm caches**
2. **Increase replica count**
3. **Auto-scaling (10x capacity)**
4. **Rate limiting**
5. **Queue system for bookings**

## 11. Trade-offs

### 1. Inventory Consistency

**Decision:** Strong consistency

**Alternatives:**
- Eventual consistency: Risk overbooking
- Strong consistency: Higher latency, acceptable

### 2. Search Freshness

**Decision:** 2-minute cache

**Trade-offs:**
- Real-time: High DB load
- Cached: Better performance, slight staleness
- Mitigation: Validate at booking time

### 3. Price Locking

**Decision:** Lock price during checkout (10 min)

**Alternatives:**
- No lock: Price may change
- Long lock: Inventory held unnecessarily

### 4. Cancellation Policy

**Decision:** Free until 24 hours before

**Trade-offs:**
- Lenient: More cancellations, harder to resell
- Strict: Poor UX, competitive disadvantage

## 12. Follow-up Questions

1. How would you implement group bookings (corporate)?
2. How would you handle multi-hotel chains?
3. How would you implement loyalty programs?
4. How would you add real-time chat support?
5. How would you handle flight+hotel packages?
6. How would you implement waitlists for sold-out hotels?
7. How would you optimize for mobile bookings?
8. How would you handle multi-currency payments?
9. How would you implement split payments?
10. How would you prevent fake reviews?

---

**Key Takeaways:**
- Strong consistency prevents overbooking
- Dynamic pricing maximizes revenue
- Comprehensive cancellation policies balance flexibility and reliability
- Caching optimizes performance without sacrificing accuracy
- Transaction management is critical for inventory
