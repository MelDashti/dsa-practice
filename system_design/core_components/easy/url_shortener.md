# URL Shortener Design: TinyURL / bit.ly

## 1. Problem Statement

Design a URL shortening service like TinyURL or bit.ly that converts long URLs into short, unique aliases. Users should be able to create short URLs and redirect to the original URL when accessed. The system must handle millions of URLs and billions of redirects.

## 2. Requirements

### Functional Requirements
- Generate short and unique URLs for given long URLs
- Redirect users from short URL to original long URL
- Support custom aliases (if available)
- Track basic analytics (click count, creation time)
- URLs should never expire (or configurable expiration)
- Support URL deletion/deactivation

### Non-functional Requirements
- **Availability:** 99.99% uptime
- **Latency:** <50ms for redirection
- **Scalability:** 100M URL shortenings per month
- **Read-Heavy:** 100:1 read-to-write ratio
- **URL Length:** 6-8 characters for short URL
- **Uniqueness:** No collisions, globally unique short URLs

## 3. Capacity Estimation

### Traffic Estimates

**Write (URL Creation):**
- 100M new URLs per month
- URLs per second: 100M / (30 * 24 * 3600) = ~40 URLs/sec
- Peak (3x average): ~120 URLs/sec

**Read (Redirects):**
- 100:1 read-to-write ratio
- Redirects per second: 40 * 100 = 4,000 redirects/sec
- Peak: ~12,000 redirects/sec

### Storage Estimates

**URL Storage:**
- Total URLs in 5 years: 100M * 12 * 5 = 6 billion URLs
- Per URL storage:
  - Short URL: 7 bytes
  - Long URL: 500 bytes (average)
  - Metadata: 100 bytes
  - Total per URL: ~600 bytes
- Total storage: 6B * 600 bytes = 3.6 TB

**With Caching:**
- Following 80-20 rule: Cache 20% of hot URLs
- Cache size: 3.6 TB * 0.20 = 720 GB

### Bandwidth Estimates

**Incoming:**
- 40 URLs/sec * 500 bytes = 20 KB/sec
- Peak: 60 KB/sec

**Outgoing:**
- 4,000 redirects/sec * 600 bytes = 2.4 MB/sec
- Peak: 7.2 MB/sec

## 4. High-Level Design

### System Architecture

```
                    Users/Browsers
                          │
                          ↓
                   Load Balancer
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ↓                 ↓                 ↓
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │   API   │      │   API   │      │   API   │
   │ Server 1│      │ Server 2│      │ Server 3│
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                 │
        └────────────────┼─────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ↓               ↓               ↓
    ┌────────┐     ┌─────────┐    ┌──────────┐
    │ Cache  │     │ Database│    │ Analytics│
    │ (Redis)│     │(MySQL)  │    │ Service  │
    └────────┘     └─────────┘    └──────────┘
```

## 5. API Design

### REST API

```
POST /api/v1/shorten
Request:
{
  "long_url": "https://www.example.com/very/long/url/path",
  "custom_alias": "my-link",  // Optional
  "expiration_date": "2025-12-31"  // Optional
}

Response:
{
  "short_url": "https://short.ly/abc123",
  "long_url": "https://www.example.com/very/long/url/path",
  "created_at": "2025-11-12T10:30:00Z",
  "expires_at": "2025-12-31T23:59:59Z"
}

GET /{short_code}
Response: 302 Redirect to long URL
Location: https://www.example.com/very/long/url/path

GET /api/v1/stats/{short_code}
Response:
{
  "short_code": "abc123",
  "long_url": "https://www.example.com/very/long/url/path",
  "clicks": 12345,
  "created_at": "2025-11-12T10:30:00Z",
  "last_accessed": "2025-11-12T15:45:30Z"
}

DELETE /api/v1/url/{short_code}
Request Headers:
Authorization: Bearer <token>

Response:
{
  "status": "deleted",
  "short_code": "abc123"
}
```

## 6. Database Schema

```sql
CREATE TABLE urls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    user_id VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_short_code (short_code),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
);

CREATE TABLE url_analytics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code VARCHAR(10) NOT NULL,
    click_count BIGINT DEFAULT 0,
    last_accessed TIMESTAMP,
    FOREIGN KEY (short_code) REFERENCES urls(short_code),
    INDEX idx_short_code (short_code)
);

CREATE TABLE url_clicks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code VARCHAR(10) NOT NULL,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT,
    country VARCHAR(2),
    INDEX idx_short_code_time (short_code, accessed_at)
);

-- For distributed ID generation
CREATE TABLE id_generator (
    id INT PRIMARY KEY AUTO_INCREMENT
);
```

## 7. Detailed Component Design

### URL Encoding Algorithm

#### Approach 1: Base62 Encoding

```python
class Base62Encoder:
    """Encode numbers to base62 string"""
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    BASE = len(ALPHABET)

    @staticmethod
    def encode(num):
        """Encode number to base62 string"""
        if num == 0:
            return Base62Encoder.ALPHABET[0]

        result = []
        while num > 0:
            remainder = num % Base62Encoder.BASE
            result.append(Base62Encoder.ALPHABET[remainder])
            num = num // Base62Encoder.BASE

        return ''.join(reversed(result))

    @staticmethod
    def decode(string):
        """Decode base62 string to number"""
        num = 0
        for char in string:
            num = num * Base62Encoder.BASE + Base62Encoder.ALPHABET.index(char)
        return num


class URLShortener:
    """URL shortening service"""
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
        self.encoder = Base62Encoder()

    async def shorten_url(self, long_url, custom_alias=None, user_id=None):
        """Generate short URL"""

        # Check if custom alias is provided
        if custom_alias:
            # Validate custom alias
            if not self.is_valid_alias(custom_alias):
                raise ValueError("Invalid custom alias")

            # Check if alias already exists
            if await self.alias_exists(custom_alias):
                raise ValueError("Custom alias already taken")

            short_code = custom_alias
        else:
            # Generate unique short code
            short_code = await self.generate_short_code()

        # Store in database
        await self.db.execute(
            """
            INSERT INTO urls (short_code, long_url, user_id)
            VALUES (?, ?, ?)
            """,
            short_code, long_url, user_id
        )

        # Initialize analytics
        await self.db.execute(
            """
            INSERT INTO url_analytics (short_code, click_count)
            VALUES (?, 0)
            """,
            short_code
        )

        return {
            'short_code': short_code,
            'short_url': f"https://short.ly/{short_code}",
            'long_url': long_url
        }

    async def generate_short_code(self):
        """Generate unique short code using auto-increment ID"""
        # Get next ID from database
        result = await self.db.execute(
            "INSERT INTO id_generator VALUES ()"
        )
        id_value = result.last_insert_id

        # Encode ID to base62
        short_code = self.encoder.encode(id_value)

        # Ensure minimum length of 6 characters
        short_code = short_code.rjust(6, '0')

        return short_code

    async def get_long_url(self, short_code):
        """Retrieve long URL from short code"""

        # Try cache first
        cache_key = f"url:{short_code}"
        cached_url = await self.cache.get(cache_key)

        if cached_url:
            # Cache hit
            await self.increment_click_count(short_code)
            return cached_url

        # Cache miss - query database
        result = await self.db.query_one(
            """
            SELECT long_url, expires_at, is_active
            FROM urls
            WHERE short_code = ?
            """,
            short_code
        )

        if not result:
            raise NotFoundError(f"Short URL not found: {short_code}")

        # Check if URL is active
        if not result['is_active']:
            raise ValueError("URL has been deactivated")

        # Check expiration
        if result['expires_at'] and result['expires_at'] < datetime.utcnow():
            raise ValueError("URL has expired")

        long_url = result['long_url']

        # Store in cache
        await self.cache.set(cache_key, long_url, ttl=3600)

        # Track analytics
        await self.increment_click_count(short_code)

        return long_url

    async def increment_click_count(self, short_code):
        """Increment click counter asynchronously"""
        # Use Redis for fast atomic increment
        await self.cache.incr(f"clicks:{short_code}")

        # Async task to sync to database periodically
        asyncio.create_task(self.sync_analytics(short_code))

    async def sync_analytics(self, short_code):
        """Sync click count from cache to database"""
        clicks_key = f"clicks:{short_code}"
        clicks = await self.cache.get(clicks_key)

        if clicks:
            await self.db.execute(
                """
                UPDATE url_analytics
                SET click_count = click_count + ?,
                    last_accessed = NOW()
                WHERE short_code = ?
                """,
                int(clicks), short_code
            )

            # Reset cache counter after sync
            await self.cache.delete(clicks_key)
```

#### Approach 2: Hash-Based (MD5/SHA)

```python
import hashlib

class HashBasedShortener:
    """Generate short code using hash function"""

    def generate_short_code(self, long_url):
        """Generate short code from URL hash"""
        # Generate MD5 hash
        hash_value = hashlib.md5(long_url.encode()).hexdigest()

        # Take first 6 characters
        short_code = hash_value[:6]

        # Handle collisions
        while await self.code_exists(short_code):
            # Append counter and rehash
            long_url += str(random.randint(0, 999))
            hash_value = hashlib.md5(long_url.encode()).hexdigest()
            short_code = hash_value[:6]

        return short_code

    async def code_exists(self, short_code):
        """Check if short code already exists"""
        result = await self.db.query_one(
            "SELECT 1 FROM urls WHERE short_code = ?",
            short_code
        )
        return result is not None
```

### Collision Handling

```python
class CollisionHandler:
    """Handle collisions in short code generation"""

    async def generate_unique_code(self, long_url):
        """Generate code with collision handling"""
        max_attempts = 5

        for attempt in range(max_attempts):
            # Generate candidate short code
            short_code = await self.generate_code(long_url, attempt)

            # Check if available
            if not await self.code_exists(short_code):
                return short_code

        # If all attempts fail, use guaranteed unique method
        return await self.generate_from_auto_increment()

    async def generate_code(self, long_url, attempt):
        """Generate code with attempt number"""
        url_to_hash = f"{long_url}:{attempt}"
        hash_value = hashlib.md5(url_to_hash.encode()).hexdigest()
        return hash_value[:7]
```

### Analytics Service

```python
class AnalyticsService:
    """Track and analyze URL access patterns"""

    def __init__(self, db, message_queue):
        self.db = db
        self.message_queue = message_queue

    async def track_click(self, short_code, request_info):
        """Track individual click asynchronously"""
        click_data = {
            'short_code': short_code,
            'ip_address': request_info.ip,
            'user_agent': request_info.user_agent,
            'referrer': request_info.referrer,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Queue for async processing
        await self.message_queue.publish('url_clicks', click_data)

    async def process_click(self, click_data):
        """Process click data (async worker)"""
        # Enrich with geolocation
        country = await self.get_country_from_ip(click_data['ip_address'])

        # Store detailed click
        await self.db.execute(
            """
            INSERT INTO url_clicks
            (short_code, accessed_at, ip_address, user_agent, referrer, country)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            click_data['short_code'],
            click_data['timestamp'],
            click_data['ip_address'],
            click_data['user_agent'],
            click_data['referrer'],
            country
        )

    async def get_stats(self, short_code):
        """Get analytics for a short URL"""
        # Basic stats
        stats = await self.db.query_one(
            """
            SELECT u.short_code, u.long_url, u.created_at,
                   a.click_count, a.last_accessed
            FROM urls u
            JOIN url_analytics a ON u.short_code = a.short_code
            WHERE u.short_code = ?
            """,
            short_code
        )

        # Geographic distribution
        geo_stats = await self.db.query(
            """
            SELECT country, COUNT(*) as count
            FROM url_clicks
            WHERE short_code = ?
            GROUP BY country
            ORDER BY count DESC
            LIMIT 10
            """,
            short_code
        )

        # Time series (last 7 days)
        time_series = await self.db.query(
            """
            SELECT DATE(accessed_at) as date, COUNT(*) as count
            FROM url_clicks
            WHERE short_code = ?
              AND accessed_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY DATE(accessed_at)
            ORDER BY date
            """,
            short_code
        )

        return {
            **stats,
            'geographic_distribution': geo_stats,
            'daily_clicks': time_series
        }
```

## 8. Trade-offs and Considerations

### Short Code Length vs Capacity

```
Base62 character set: 62 characters (0-9, a-z, A-Z)

6 characters: 62^6 = 56.8 billion URLs
7 characters: 62^7 = 3.5 trillion URLs
8 characters: 62^8 = 218 trillion URLs

For 100M URLs/month:
- 6 chars: 568 months (~47 years)
- 7 chars: 35,000+ months
```

### Base62 vs Hash-Based

| Aspect | Base62 (Auto-increment) | Hash-Based |
|--------|-------------------------|------------|
| **Uniqueness** | Guaranteed | Collisions possible |
| **Predictability** | Sequential (can guess next) | Random |
| **Performance** | Fast | Need collision handling |
| **Distribution** | Requires distributed ID | Independent generation |
| **Storage** | Efficient | May waste due to collisions |

### Caching Strategy

```python
class CachingStrategy:
    """Implement multi-tier caching"""

    def __init__(self):
        self.l1_cache = {}  # Local in-memory
        self.l2_cache = Redis()  # Distributed Redis

    async def get_url(self, short_code):
        # L1: Local cache
        if short_code in self.l1_cache:
            return self.l1_cache[short_code]

        # L2: Redis cache
        url = await self.l2_cache.get(f"url:{short_code}")
        if url:
            self.l1_cache[short_code] = url  # Populate L1
            return url

        # L3: Database
        url = await self.db.get_url(short_code)
        if url:
            await self.l2_cache.set(f"url:{short_code}", url, ttl=3600)
            self.l1_cache[short_code] = url
            return url

        return None
```

## 9. Scalability & Bottlenecks

### Database Sharding

```python
class ShardedURLService:
    """Shard URLs across multiple databases"""

    def __init__(self, num_shards=10):
        self.num_shards = num_shards
        self.shards = [Database(f"shard_{i}") for i in range(num_shards)]

    def get_shard(self, short_code):
        """Determine shard for short code"""
        shard_id = hash(short_code) % self.num_shards
        return self.shards[shard_id]

    async def get_url(self, short_code):
        """Get URL from appropriate shard"""
        shard = self.get_shard(short_code)
        return await shard.query_one(
            "SELECT long_url FROM urls WHERE short_code = ?",
            short_code
        )
```

### Rate Limiting

```python
class RateLimiter:
    """Rate limit URL creation per user/IP"""

    def __init__(self, redis):
        self.redis = redis

    async def check_rate_limit(self, user_id, max_requests=100, window=3600):
        """Check if user is within rate limit"""
        key = f"ratelimit:{user_id}"
        current = await self.redis.incr(key)

        if current == 1:
            # First request in window
            await self.redis.expire(key, window)

        if current > max_requests:
            raise RateLimitExceeded(f"Rate limit exceeded: {max_requests}/{window}s")

        return True
```

## 10. Follow-up Questions

1. **How do you handle distributed ID generation?**
   - Twitter Snowflake algorithm
   - Database with multiple auto-increment ranges
   - UUID (but longer)
   - Zookeeper/etcd for coordination

2. **How do you prevent malicious URLs?**
   - URL validation and sanitization
   - Blacklist of known malicious domains
   - Integrate with safe browsing APIs
   - Rate limiting per IP/user

3. **How do you handle peak traffic?**
   - Aggressive caching (99%+ hit rate)
   - CDN for static redirect pages
   - Read replicas for database
   - Auto-scaling

4. **How do you ensure high availability?**
   - Multi-region deployment
   - Database replication
   - Redis clustering
   - Load balancing across regions

5. **Can you provide the same short URL for the same long URL?**
   - Yes: Hash long URL and check if exists
   - No: Always generate new (better analytics)
   - Trade-off: Storage vs deduplication

6. **How do you handle analytics at scale?**
   - Async processing with message queues
   - Batch writes to database
   - Use time-series database (InfluxDB)
   - Aggregate data periodically

7. **How do you implement custom aliases?**
   - Check availability before assignment
   - Reserve premium/brand names
   - Charge for custom aliases
   - Validate format (no special chars)

8. **What if the database fails?**
   - Replicas for read operations
   - Queue writes during outage
   - Eventual consistency acceptable
   - Graceful degradation

9. **How do you handle URL expiration?**
   - TTL in database
   - Background job to mark expired
   - Return 410 Gone for expired URLs
   - Option to renew before expiration

10. **How do you prevent enumeration attacks?**
    - Use random/hash-based codes (not sequential)
    - Rate limit access attempts
    - CAPTCHA after multiple attempts
    - Monitor for suspicious patterns
