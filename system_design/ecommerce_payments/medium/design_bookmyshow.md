# Design BookMyShow (Ticket Booking System)

## 1. Problem Statement

Design a movie and event ticket booking platform like BookMyShow that allows users to search for movies/events, view showtimes/venues, select seats, make payments, and manage bookings. The system must handle high concurrency during popular releases, prevent double-booking, and support real-time seat availability.

**Key Features:**
- Search movies/events by location, genre, language
- View theaters and showtimes
- Interactive seat selection
- Real-time seat locking
- Payment processing
- Booking confirmation and tickets
- Cancellation and refunds
- Reviews and ratings

## 2. Requirements

### Functional Requirements

1. **User Management**
   - User registration and login
   - Profile management
   - Booking history
   - Saved payment methods

2. **Movie/Event Management**
   - Browse movies/events
   - Search and filter (genre, language, location, date)
   - View details (cast, duration, rating, trailer)
   - Theater/venue listings
   - Showtime/event schedule

3. **Booking Flow**
   - Select city, movie, theater, showtime
   - View seat layout
   - Select seats (with real-time availability)
   - Apply promo codes/offers
   - Make payment
   - Receive confirmation and ticket

4. **Seat Management**
   - Interactive seat map
   - Different seat types (regular, premium, recliner)
   - Real-time seat locking (10-minute hold)
   - Block seats for maintenance
   - Wheelchair accessible seats

5. **Payment**
   - Multiple payment methods
   - Payment gateway integration
   - Wallet/credits
   - Refund processing

6. **Post-Booking**
   - View/download tickets
   - QR code for entry
   - Cancellation (with refund policy)
   - Modify booking (if allowed)
   - Food & beverage add-ons

7. **Admin Features**
   - Theater onboarding
   - Show/event creation
   - Pricing management
   - Analytics dashboard
   - Revenue reports

### Non-Functional Requirements

1. **Performance**
   - Page load time < 1 second
   - Seat selection response < 200ms
   - Support 10K concurrent bookings
   - Handle 100K requests per second (peak)

2. **Availability**
   - 99.9% uptime
   - No downtime during releases
   - Graceful degradation

3. **Consistency**
   - Strong consistency for seat booking (no double-booking)
   - Eventual consistency for movie listings
   - ACID transactions for payments

4. **Scalability**
   - Support 1000+ cities
   - 10,000+ theaters
   - 100M+ users
   - Peak traffic during blockbuster releases (10x normal)

5. **Concurrency**
   - Handle race conditions in seat booking
   - Prevent overselling
   - Fair booking (FIFO where possible)

6. **Security**
   - Secure payment processing
   - Prevent ticket fraud (unique QR codes)
   - Bot prevention
   - PCI DSS compliance

## 3. Scale Estimation

### Traffic Estimates
- **Daily Active Users (DAU):** 10 million
- **Monthly Active Users (MAU):** 40 million
- **Peak concurrent users:** 100K (during blockbuster releases)
- **Average session duration:** 10 minutes

### Transaction Estimates
- **Searches per day:** 50 million
- **Bookings per day:** 2 million
- **Tickets per booking:** 2.5 (average)
- **Total tickets per day:** 5 million
- **Average ticket price:** $10
- **Daily GMV:** $50 million

### Booking Distribution
- **Peak hours:** 50% of bookings (evening/weekend)
- **Peak events:** 10x traffic (movie releases, concerts)
- **Conversion rate:** 4% (searches to bookings)

### Storage Estimates
- **Movies:** 10,000 active movies × 100 KB = 1 GB
- **Theaters:** 10,000 theaters × 50 KB = 500 MB
- **Shows:** 100K daily shows × 10 KB = 1 GB/day = 365 GB/year
- **Bookings:** 2M bookings/day × 5 KB = 10 GB/day = 3.6 TB/year
- **Users:** 40M users × 2 KB = 80 GB
- **Images/videos:** 10K movies × 10 MB = 100 GB
- **Total (Year 1):** ~4.2 TB

### Bandwidth Estimates
- **API calls:** 100K RPS × 10 KB = 1 GB/s = 86 TB/day
- **Media (CDN):** 10M users × 20 MB = 200 TB/day
- **Total:** ~286 TB/day

### Cache Estimates
- **Hot movies:** 1000 movies × 100 KB = 100 MB
- **Popular shows:** 10K shows × 10 KB = 100 MB
- **Seat maps (active):** 10K shows × 50 KB = 500 MB
- **User sessions:** 100K sessions × 10 KB = 1 GB
- **Total cache:** ~2 GB

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
  │    Movie      │      │   Booking     │      │     User      │
  │   Service     │      │   Service     │      │   Service     │
  └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
          │                       │                       │
          ▼                       ▼                       ▼
  ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
  │   Theater     │      │     Seat      │      │     Auth      │
  │   Service     │      │   Service     │      │   Service     │
  └───────┬───────┘      └───────┬───────┘      └───────────────┘
          │                       │
          ▼                       ▼
  ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
  │    Search     │      │   Payment     │      │ Notification  │
  │   Service     │      │   Service     │      │   Service     │
  │(Elasticsearch)│      └───────────────┘      └───────────────┘
  └───────────────┘

                        Data Layer
┌───────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │PostgreSQL│  │PostgreSQL│  │  Redis   │  │  Redis   │  │
│  │ (Movies) │  │(Bookings)│  │  (Cache) │  │ (Locks)  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   S3     │  │  Kafka   │  │   SQS    │  │Elasticsearch│
│  │ (Media)  │  │ (Events) │  │ (Queue)  │  │  (Search)  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└───────────────────────────────────────────────────────────┘

                External Services
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Stripe  │  │  Twilio  │  │ SendGrid │  │ Analytics│
│  Payment │  │   SMS    │  │  Email   │  │ DataDog  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 5. API Design

### Movie/Event APIs

```
GET /api/v1/cities
Response: 200 OK
{
  "cities": [
    {"cityId": "uuid", "name": "New York", "state": "NY"},
    {"cityId": "uuid", "name": "Los Angeles", "state": "CA"}
  ]
}

GET /api/v1/movies?cityId={cityId}&date={date}&language={language}
Response: 200 OK
{
  "movies": [
    {
      "movieId": "uuid",
      "title": "Inception",
      "language": "English",
      "genre": ["Sci-Fi", "Thriller"],
      "duration": 148,
      "rating": "PG-13",
      "releaseDate": "2010-07-16",
      "posterUrl": "url",
      "averageRating": 4.5,
      "formats": ["2D", "3D", "IMAX"]
    }
  ]
}

GET /api/v1/movies/{movieId}
Response: 200 OK
{
  "movieId": "uuid",
  "title": "Inception",
  "description": "...",
  "cast": ["Leonardo DiCaprio", "Tom Hardy"],
  "director": "Christopher Nolan",
  "duration": 148,
  "language": "English",
  "genre": ["Sci-Fi", "Thriller"],
  "rating": "PG-13",
  "releaseDate": "2010-07-16",
  "posterUrl": "url",
  "trailerUrl": "url",
  "averageRating": 4.5,
  "reviewCount": 1234
}

GET /api/v1/movies/{movieId}/shows?cityId={cityId}&date={date}
Response: 200 OK
{
  "date": "2025-11-12",
  "theaters": [
    {
      "theaterId": "uuid",
      "name": "AMC Empire 25",
      "address": "234 W 42nd St, New York, NY 10036",
      "shows": [
        {
          "showId": "uuid",
          "time": "14:00",
          "format": "IMAX 3D",
          "language": "English",
          "availableSeats": 45,
          "totalSeats": 300,
          "pricing": {
            "regular": 15.99,
            "premium": 19.99,
            "recliner": 24.99
          }
        }
      ]
    }
  ]
}
```

### Seat Selection APIs

```
GET /api/v1/shows/{showId}/seats
Response: 200 OK
{
  "showId": "uuid",
  "layout": {
    "rows": 15,
    "columns": 20,
    "seats": [
      {
        "seatId": "uuid",
        "row": "A",
        "number": 1,
        "type": "regular",
        "price": 15.99,
        "status": "available" // available, locked, booked, blocked
      },
      {
        "seatId": "uuid",
        "row": "A",
        "number": 2,
        "type": "regular",
        "price": 15.99,
        "status": "locked",
        "lockedUntil": "2025-11-12T14:10:00Z"
      }
    ],
    "aisles": [5, 15], // column numbers that are aisles
    "wheelchairSeats": ["A1", "A20"]
  }
}

POST /api/v1/shows/{showId}/seats/lock
Request:
{
  "seatIds": ["seat-uuid-1", "seat-uuid-2"],
  "sessionId": "user-session-uuid"
}
Response: 200 OK
{
  "lockId": "uuid",
  "expiresAt": "2025-11-12T14:10:00Z",
  "seats": [...]
}

POST /api/v1/shows/{showId}/seats/unlock
Request:
{
  "lockId": "uuid"
}
Response: 204 No Content
```

### Booking APIs

```
POST /api/v1/bookings
Request:
{
  "showId": "uuid",
  "seats": ["seat-uuid-1", "seat-uuid-2"],
  "lockId": "uuid",
  "contactInfo": {
    "email": "user@example.com",
    "phone": "+1234567890"
  },
  "paymentMethod": {
    "type": "credit_card",
    "token": "pm_xxx"
  },
  "promoCode": "FIRST10"
}
Response: 201 Created
{
  "bookingId": "uuid",
  "bookingNumber": "BMS20251112001",
  "status": "confirmed",
  "seats": [...],
  "totalAmount": 31.98,
  "discount": 3.20,
  "finalAmount": 28.78,
  "qrCode": "base64-encoded-qr",
  "tickets": [
    {
      "ticketId": "uuid",
      "seat": "A-1",
      "qrCode": "unique-qr-per-ticket"
    }
  ]
}

GET /api/v1/bookings/{bookingId}
Response: 200 OK
{
  "bookingId": "uuid",
  "bookingNumber": "BMS20251112001",
  "status": "confirmed",
  "movie": {...},
  "show": {...},
  "theater": {...},
  "seats": [...],
  "amount": 28.78,
  "paymentStatus": "completed",
  "bookedAt": "2025-11-12T14:00:00Z"
}

GET /api/v1/users/{userId}/bookings?page=1&limit=10
Response: 200 OK
{
  "bookings": [...],
  "pagination": {...}
}

POST /api/v1/bookings/{bookingId}/cancel
Request:
{
  "reason": "Change of plans"
}
Response: 200 OK
{
  "bookingId": "uuid",
  "status": "cancelled",
  "refundAmount": 25.90, // after cancellation fee
  "refundStatus": "processing"
}
```

### Admin APIs

```
POST /api/v1/admin/movies
POST /api/v1/admin/theaters
POST /api/v1/admin/shows

GET /api/v1/admin/shows/{showId}/bookings
GET /api/v1/admin/analytics/revenue
```

## 6. Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);
```

### Cities Table
```sql
CREATE TABLE cities (
    city_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    timezone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, country)
);
```

### Movies Table
```sql
CREATE TABLE movies (
    movie_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    language VARCHAR(50) NOT NULL,
    genre JSONB, -- ["Sci-Fi", "Thriller"]
    duration INT NOT NULL, -- in minutes
    rating VARCHAR(10), -- PG-13, R, etc.
    release_date DATE NOT NULL,
    director VARCHAR(255),
    cast JSONB, -- ["Actor 1", "Actor 2"]
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    average_rating DECIMAL(3, 2) DEFAULT 0,
    review_count INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active', -- active, coming_soon, archived
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_release_date (release_date),
    INDEX idx_status (status),
    FULLTEXT idx_search (title, description)
);
```

### Theaters Table
```sql
CREATE TABLE theaters (
    theater_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    city_id UUID NOT NULL REFERENCES cities(city_id),
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    facilities JSONB, -- ["Parking", "Food Court", "Wheelchair Access"]
    screens INT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city_id),
    INDEX idx_location (latitude, longitude),
    INDEX idx_status (status)
);
```

### Screens Table
```sql
CREATE TABLE screens (
    screen_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    theater_id UUID NOT NULL REFERENCES theaters(theater_id),
    screen_number INT NOT NULL,
    screen_type VARCHAR(50), -- IMAX, 4DX, Standard
    total_seats INT NOT NULL,
    layout JSONB NOT NULL, -- seat configuration
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(theater_id, screen_number),
    INDEX idx_theater (theater_id)
);
```

### Seats Table
```sql
CREATE TABLE seats (
    seat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    screen_id UUID NOT NULL REFERENCES screens(screen_id),
    row_name VARCHAR(5) NOT NULL,
    seat_number INT NOT NULL,
    seat_type VARCHAR(20) NOT NULL, -- regular, premium, recliner, wheelchair
    status VARCHAR(20) DEFAULT 'active', -- active, blocked, maintenance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(screen_id, row_name, seat_number),
    INDEX idx_screen (screen_id),
    INDEX idx_type (seat_type)
);
```

### Shows Table
```sql
CREATE TABLE shows (
    show_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    movie_id UUID NOT NULL REFERENCES movies(movie_id),
    screen_id UUID NOT NULL REFERENCES screens(screen_id),
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    format VARCHAR(50), -- 2D, 3D, IMAX, 4DX
    language VARCHAR(50),
    pricing JSONB NOT NULL, -- {"regular": 15.99, "premium": 19.99}
    status VARCHAR(20) DEFAULT 'active', -- active, cancelled
    booking_opens_at TIMESTAMP,
    booking_closes_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_movie (movie_id),
    INDEX idx_screen (screen_id),
    INDEX idx_date_time (show_date, show_time),
    INDEX idx_status (status),
    CONSTRAINT chk_times CHECK (booking_opens_at < booking_closes_at)
);
```

### Show_Seats Table (Seat availability per show)
```sql
CREATE TABLE show_seats (
    show_seat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    show_id UUID NOT NULL REFERENCES shows(show_id),
    seat_id UUID NOT NULL REFERENCES seats(seat_id),
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'available', -- available, locked, booked, blocked
    locked_by VARCHAR(255), -- session ID
    locked_until TIMESTAMP,
    booking_id UUID REFERENCES bookings(booking_id),
    version INT DEFAULT 0, -- for optimistic locking
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(show_id, seat_id),
    INDEX idx_show (show_id),
    INDEX idx_status (status),
    INDEX idx_locked (locked_by, locked_until),
    CONSTRAINT chk_status CHECK (status IN ('available', 'locked', 'booked', 'blocked'))
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    booking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_number VARCHAR(50) UNIQUE NOT NULL,
    user_id UUID REFERENCES users(user_id),
    show_id UUID NOT NULL REFERENCES shows(show_id),
    num_seats INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    final_amount DECIMAL(10, 2) NOT NULL,
    promo_code VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, cancelled
    payment_status VARCHAR(20) DEFAULT 'pending',
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    refund_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_show (show_id),
    INDEX idx_status (status),
    INDEX idx_booking_number (booking_number),
    INDEX idx_booked_at (booked_at),
    CONSTRAINT chk_amounts CHECK (final_amount = total_amount - discount)
);
```

### Tickets Table
```sql
CREATE TABLE tickets (
    ticket_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL REFERENCES bookings(booking_id),
    show_seat_id UUID NOT NULL REFERENCES show_seats(show_seat_id),
    qr_code VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'valid', -- valid, used, cancelled
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_booking (booking_id),
    INDEX idx_qr_code (qr_code),
    INDEX idx_status (status)
);
```

### Payments Table
```sql
CREATE TABLE payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL REFERENCES bookings(booking_id),
    amount DECIMAL(10, 2) NOT NULL,
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

### Promo_Codes Table
```sql
CREATE TABLE promo_codes (
    promo_code_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    discount_type VARCHAR(20), -- percentage, flat
    discount_value DECIMAL(10, 2) NOT NULL,
    min_amount DECIMAL(10, 2),
    max_discount DECIMAL(10, 2),
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    usage_limit INT,
    used_count INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_status_dates (status, valid_from, valid_until)
);
```

### ACID Considerations

1. **Seat Locking:**
   - Use optimistic locking with version numbers
   - Or pessimistic locking with SELECT FOR UPDATE
   - Atomic compare-and-swap operations

2. **Booking Transaction:**
   - Create booking atomically
   - Update seat status
   - Process payment
   - Generate tickets
   - All-or-nothing execution

3. **Cancellation:**
   - Update booking status
   - Release seats
   - Process refund
   - Maintain audit trail

4. **Isolation Levels:**
   - SERIALIZABLE for seat booking
   - READ COMMITTED for queries
   - Prevent phantom reads and lost updates

## 7. Core Components

### 7.1 Movie Service
**Responsibilities:**
- Movie CRUD operations
- Movie search and filtering
- Metadata management
- Integration with content providers

**Caching:**
- Cache popular movies (1 hour TTL)
- Cache movie details (1 hour TTL)
- Invalidate on updates

### 7.2 Theater Service
**Responsibilities:**
- Theater onboarding
- Screen management
- Seat layout configuration
- Show scheduling

**Features:**
- Geographic search (lat/long)
- Filter by facilities
- Capacity management

### 7.3 Search Service
**Technology:** Elasticsearch

**Features:**
- Full-text movie search
- Filter by genre, language, rating
- Location-based theater search
- Autocomplete for movies

**Indexing:**
```json
{
  "movies": {
    "title": "Inception",
    "genre": ["Sci-Fi", "Thriller"],
    "language": "English",
    "rating": "PG-13",
    "release_date": "2010-07-16",
    "average_rating": 4.5
  }
}
```

### 7.4 Seat Service
**Critical Component** - Handles seat locking and concurrency

**Seat Locking Mechanism:**

**Option 1: Optimistic Locking**
```sql
-- Check availability
SELECT status, version FROM show_seats
WHERE show_seat_id = ? AND status = 'available';

-- Try to lock (will fail if version changed)
UPDATE show_seats
SET status = 'locked',
    locked_by = ?,
    locked_until = NOW() + INTERVAL '10 minutes',
    version = version + 1
WHERE show_seat_id = ?
  AND status = 'available'
  AND version = ?; -- original version

-- Check rows affected
-- If 0, someone else locked it (retry or fail)
```

**Option 2: Redis Distributed Lock**
```python
def lock_seats(show_id, seat_ids, session_id):
    lock_keys = [f"seat:{show_id}:{seat_id}" for seat_id in seat_ids]

    # Try to acquire all locks atomically
    with redis.pipeline() as pipe:
        for key in lock_keys:
            pipe.set(key, session_id, nx=True, ex=600)  # 10 min expiry
        results = pipe.execute()

    # Check if all locks acquired
    if all(results):
        return {"lockId": session_id, "expiresAt": ...}
    else:
        # Rollback acquired locks
        release_locks(lock_keys)
        return {"error": "Some seats unavailable"}
```

**Lock Expiry:**
- Background job releases expired locks every minute
- Prevents deadlocks if user abandons booking

### 7.5 Booking Service
**Workflow:**

```
1. Validate lock exists and not expired
2. Verify seats still available
3. Apply promo code (if any)
4. Calculate total amount
5. BEGIN TRANSACTION
   a. Create booking record
   b. Update show_seats status = 'booked'
   c. Create tickets with unique QR codes
   d. Process payment
   e. Send confirmation
6. COMMIT (or ROLLBACK on failure)
```

**Idempotency:**
- Use booking request ID to prevent duplicate bookings
- Store in Redis with short TTL

### 7.6 Payment Service
**Integration:** Stripe, PayPal, Razorpay

**Features:**
- Multiple payment methods
- Wallet integration
- Refund processing
- Payment reconciliation

**Security:**
- PCI DSS compliance
- Tokenization
- 3D Secure authentication

### 7.7 Notification Service
**Channels:** Email, SMS, Push notifications

**Triggers:**
- Booking confirmation
- Payment receipt
- Show reminders (24 hours before)
- Cancellation confirmation
- Refund status

**Implementation:**
- SQS for async processing
- Template management
- Delivery tracking

### 7.8 QR Code Service
**Responsibilities:**
- Generate unique QR codes per ticket
- Validate QR codes at entry
- Prevent fraud (double-scanning)

**QR Code Format:**
```
{
  "ticketId": "uuid",
  "bookingId": "uuid",
  "showId": "uuid",
  "seat": "A-5",
  "timestamp": "2025-11-12T14:00:00Z",
  "signature": "HMAC-SHA256 signature"
}
```

**Validation:**
- Verify signature
- Check ticket status
- Mark as 'used' on first scan
- Prevent duplicate scans

## 8. Transaction Management & Consistency

### Seat Booking Transaction (Critical)

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Verify lock ownership
SELECT locked_by, locked_until
FROM show_seats
WHERE show_seat_id IN (?, ?, ?)
  AND locked_by = ?
  AND locked_until > NOW()
FOR UPDATE;

-- If not all seats locked by this session, ROLLBACK

-- 2. Create booking
INSERT INTO bookings (booking_number, user_id, show_id, ...)
VALUES (?, ?, ?, ...)
RETURNING booking_id;

-- 3. Update seats to booked
UPDATE show_seats
SET status = 'booked',
    booking_id = ?,
    locked_by = NULL,
    locked_until = NULL,
    updated_at = NOW()
WHERE show_seat_id IN (?, ?, ?)
  AND locked_by = ?;

-- 4. Create tickets with QR codes
INSERT INTO tickets (booking_id, show_seat_id, qr_code, price)
VALUES
  (?, ?, ?, ?),
  (?, ?, ?, ?);

-- 5. Create payment record
INSERT INTO payments (booking_id, amount, payment_method, ...)
VALUES (?, ?, ?, ...);

COMMIT;
```

**Failure Handling:**
```
If payment fails:
  1. Update booking status = 'failed'
  2. Release seats (status = 'available')
  3. DO NOT create tickets
  4. Return error to user

If payment succeeds but email fails:
  1. Booking still confirmed
  2. Retry email async (SQS)
  3. User can view booking in account
```

### Cancellation Transaction

```sql
BEGIN TRANSACTION;

-- 1. Verify booking can be cancelled
SELECT status, show_id, final_amount
FROM bookings
WHERE booking_id = ?
  AND status = 'confirmed'
  AND (SELECT show_date, show_time FROM shows WHERE show_id = bookings.show_id)
      > NOW() + INTERVAL '2 hours'
FOR UPDATE;

-- 2. Update booking status
UPDATE bookings
SET status = 'cancelled',
    cancelled_at = NOW(),
    cancellation_reason = ?,
    refund_amount = ? -- after fee
WHERE booking_id = ?;

-- 3. Release seats
UPDATE show_seats
SET status = 'available',
    booking_id = NULL
WHERE booking_id = ?;

-- 4. Invalidate tickets
UPDATE tickets
SET status = 'cancelled'
WHERE booking_id = ?;

-- 5. Process refund
INSERT INTO payments (booking_id, amount, payment_method, status, ...)
VALUES (?, ?, 'refund', 'processing', ...);

COMMIT;
```

### Distributed Lock Management

**Redis Locks for Seat Selection:**
```python
def lock_seats_distributed(show_id, seat_ids, session_id):
    # Use Redlock algorithm for distributed locks
    lock_manager = Redlock([redis1, redis2, redis3])

    locks = []
    for seat_id in seat_ids:
        lock_key = f"seat:{show_id}:{seat_id}"
        lock = lock_manager.lock(lock_key, 600000)  # 10 min in ms
        if not lock:
            # Failed to acquire lock, release all
            for l in locks:
                lock_manager.unlock(l)
            raise SeatUnavailableError()
        locks.append(lock)

    return locks
```

**Lock Expiry Job:**
```sql
-- Run every minute
UPDATE show_seats
SET status = 'available',
    locked_by = NULL,
    locked_until = NULL
WHERE status = 'locked'
  AND locked_until < NOW();
```

## 9. Security Considerations

### Payment Security
- **PCI DSS compliance**
- **Never store card details**
- **Tokenization** via payment gateway
- **3D Secure** for authentication
- **Fraud detection:**
  - Velocity checks (bookings per user/IP)
  - Geolocation anomalies
  - ML-based fraud scoring

### Ticket Fraud Prevention
- **Unique QR codes** per ticket
- **Digital signatures** (HMAC-SHA256)
- **Single-use tickets** (mark as used after scan)
- **Timestamp validation**
- **Offline verification** capability

### Bot Prevention
- **CAPTCHA** during high-demand shows
- **Rate limiting:**
  - 10 seat lock requests per minute per user
  - 100 requests per minute per IP
- **Device fingerprinting**
- **Behavioral analysis** (rapid clicks, automated patterns)

### Access Control
- **JWT tokens** with short expiration
- **Role-based access:**
  - User: booking, viewing
  - Theater Admin: show management
  - System Admin: full access

### Data Protection
- **Encryption at rest** (AES-256)
- **Encryption in transit** (TLS 1.3)
- **PII protection** (email, phone)
- **GDPR compliance** (right to deletion)

### API Security
- **API rate limiting**
- **Input validation**
- **SQL injection prevention**
- **XSS prevention**
- **CSRF tokens**

## 10. Scalability

### Database Scaling

**Sharding Strategy:**
```
Shows: Shard by (city_id, show_date)
- Each city-date combo on separate shard
- Hot shows isolated
- Easy to scale per city

Bookings: Shard by user_id (consistent hashing)
- User affinity
- Easy user history queries

show_seats: Co-located with shows shard
- Same shard for show and its seats
- Reduces cross-shard queries
```

**Read Replicas:**
- Route reads to replicas
- Write to primary
- Acceptable slight delay for listings

**Caching:**
```
L1: Application cache (in-memory)
  └─> Seat layouts, pricing

L2: Redis
  └─> Movie listings (5 min TTL)
  └─> Show listings (2 min TTL)
  └─> Seat availability (1 min TTL)
  └─> User sessions

L3: CDN
  └─> Movie posters/trailers
  └─> Static assets
```

### Handling Peak Traffic

**Blockbuster Movie Release Strategy:**

1. **Booking Opens Strategy:**
   - Staggered opening (by membership tier)
   - Queue system (virtual waiting room)
   - Rate limiting per user

2. **Pre-warm Caches:**
   - Load popular shows into cache
   - Pre-generate seat maps
   - Warm up DB connections

3. **Auto-scaling:**
   - Scale booking service pods (10x capacity)
   - Increase DB connections
   - Add read replicas temporarily

4. **Circuit Breakers:**
   - Fail fast on timeouts
   - Graceful degradation
   - Queue requests if overloaded

5. **CDN for Static Content:**
   - Serve movie details from CDN
   - Reduce DB load

### Seat Availability at Scale

**Challenge:** 10K concurrent users trying to book same show

**Solution 1: Optimistic Locking**
- Try to lock seats
- If fails, show "seats unavailable"
- Fast failure, good UX

**Solution 2: Queue System**
- User joins queue
- Process FIFO
- Show position in queue
- Better for high-demand shows

**Solution 3: Probabilistic Lock**
- Show "likely available" seats
- Lock on selection
- Some failures acceptable

### Message Queues

**SQS for:**
- Email notifications (async)
- SMS notifications (async)
- Analytics events (async)
- Lock expiry processing

**Kafka for:**
- Booking events (event sourcing)
- Real-time analytics
- Audit logs

## 11. Trade-offs

### 1. Seat Locking Duration

**Decision:** 10-minute lock

**Trade-offs:**
- **Longer (15-20 min):**
  - Pro: More time for user to complete booking
  - Con: Seats locked unnecessarily, lost sales
- **Shorter (5 min):**
  - Pro: Faster seat turnover
  - Con: User pressure, abandoned bookings

**Mitigation:**
- Timer shown to user
- Option to extend lock once (additional 5 min)
- Warning at 2 minutes remaining

### 2. Seat Status Consistency

**Decision:** Strong consistency for seat booking

**Trade-offs:**
- **Strong consistency:**
  - Pro: No double-booking, accurate inventory
  - Con: Higher latency, lower availability
- **Eventual consistency:**
  - Pro: Better performance, higher availability
  - Con: Risk of overselling

**Justification:** Correctness > Performance for bookings

### 3. Cancellation Policy

**Decision:** Allow cancellation until 2 hours before show

**Trade-offs:**
- **More restrictive (24 hours):**
  - Pro: Less last-minute cancellations
  - Con: Poor user experience
- **Less restrictive (30 minutes):**
  - Pro: Better UX, more flexibility
  - Con: Harder to resell seats

**Mitigation:**
- Cancellation fee (10-20%)
- Waitlist for popular shows
- Automatic refund to wallet

### 4. Search: Real-time vs Cached

**Decision:** 2-minute cache TTL for show listings

**Trade-offs:**
- **Real-time:**
  - Pro: Always accurate seat counts
  - Con: High DB load, slower response
- **Longer cache (10 min):**
  - Pro: Better performance
  - Con: Stale data, poor UX

**Mitigation:**
- Cache invalidation on booking
- Real-time check during seat selection

### 5. Payment Processing

**Decision:** Synchronous payment during booking

**Trade-offs:**
- **Synchronous:**
  - Pro: Immediate confirmation, simpler flow
  - Con: Higher perceived latency
- **Asynchronous:**
  - Pro: Faster booking response
  - Con: Complex state management, pending bookings

**Justification:** User expects immediate confirmation

### 6. Database Choice

**Decision:** PostgreSQL for transactional data

**Alternatives:**
- **MySQL:** Similar capabilities
- **NoSQL:** Poor fit for transactions
- **NewSQL (CockroachDB):** Better scaling, more complex

**Justification:**
- ACID guarantees critical
- Complex queries needed
- Mature ecosystem

## 12. Follow-up Questions

### Functional

1. How would you implement a waitlist for sold-out shows?
2. How would you handle group bookings (block booking)?
3. How would you implement food & beverage ordering?
4. How would you add seat selection preferences (aisle, center, etc.)?
5. How would you handle partial cancellations (cancel 2 out of 4 seats)?

### Scalability

6. How would you handle a blockbuster release with 1M concurrent users?
7. How would you scale across multiple countries/currencies?
8. How would you implement a queue system for high-demand shows?
9. How would you handle database hotspots (popular shows)?
10. How would you optimize for mobile users on slow networks?

### Concurrency

11. How would you prevent double-booking with 10K concurrent requests?
12. How would you implement fair seat allocation (FIFO)?
13. How would you handle distributed lock failures?
14. How would you optimize lock contention for popular shows?
15. How would you implement seat selection with 100 users simultaneously?

### Business Logic

16. How would you implement dynamic pricing (surge pricing)?
17. How would you handle theater-specific pricing rules?
18. How would you implement loyalty programs (points/rewards)?
19. How would you handle refunds for show cancellations?
20. How would you prevent ticket scalping/reselling?

### Reliability

21. How would you ensure zero data loss during failures?
22. How would you handle payment gateway downtime?
23. How would you implement graceful degradation?
24. How would you handle split-brain scenarios?
25. How would you ensure audit trail for all bookings?

### Analytics

26. How would you track seat popularity for pricing optimization?
27. How would you implement real-time dashboard for theater owners?
28. How would you analyze user drop-off in booking funnel?
29. How would you implement A/B testing for booking flow?
30. How would you predict show demand for better scheduling?

---

**Key Takeaways:**
- Strong consistency is critical for seat booking
- Distributed locks prevent double-booking
- Time-bound reservations balance UX and inventory
- Queue systems handle peak demand
- Comprehensive security prevents fraud
- Event-driven architecture for scalability
