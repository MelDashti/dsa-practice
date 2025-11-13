# CDN Design: Content Delivery Network Architecture

## 1. Problem Statement

How do we deliver static and dynamic content to users globally with minimal latency? Users across the world expect fast page loads regardless of their geographic location relative to origin servers. A Content Delivery Network (CDN) caches and serves content from locations close to end users, reducing latency and origin server load.

## 2. Requirements

### Functional Requirements
- Cache and serve static content (images, CSS, JS, videos)
- Support dynamic content with intelligent caching
- Handle cache invalidation and purging
- Provide SSL/TLS termination
- Support multiple origin servers
- Enable geographic routing
- Provide DDoS protection and security

### Non-functional Requirements
- **Latency:** <50ms to nearest edge server
- **Availability:** 99.99% uptime
- **Cache Hit Ratio:** >85% for static content
- **Throughput:** 10+ Tbps aggregate bandwidth
- **Geographic Coverage:** Presence in 200+ cities globally
- **Failover Time:** <1 second to alternate edge server

## 3. Capacity Estimation

### Example: Video Streaming Platform

**Traffic:**
- 100M daily active users
- Average: 2 hours of video per user per day
- Peak concurrent users: 10M
- Average video bitrate: 5 Mbps
- Total bandwidth at peak: 10M * 5 Mbps = 50 Tbps

**Storage:**
- Total videos: 1M
- Average video size: 500 MB
- Total storage needed: 500 TB
- Cache top 10% videos: 50 TB per edge location
- 200 edge locations: 10 PB total edge storage

**Edge Server Calculations:**
```
Per edge server capacity: 10 Gbps
Peak traffic per region: 250 Gbps (500M users / 200 regions)
Servers per edge location: 250 / 10 = 25 servers
Total servers globally: 25 * 200 = 5,000 edge servers
```

## 4. High-Level Design

### CDN Architecture

```
                         ┌──────────────────┐
                         │   DNS Server     │
                         │  (GeoDNS)        │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
              US Region      EU Region     Asia Region
                    │             │             │
            ┌───────▼──────┐ ┌────▼──────┐ ┌───▼───────┐
            │  PoP (Point  │ │  PoP      │ │  PoP      │
            │  of Presence)│ │           │ │           │
            └───────┬──────┘ └────┬──────┘ └───┬───────┘
                    │             │             │
        ┌───────────┼─────────┐   │             │
        │           │         │   │             │
    ┌───▼───┐  ┌───▼───┐ ┌───▼───┐             │
    │Edge 1 │  │Edge 2 │ │Edge 3 │  ...        │
    └───┬───┘  └───┬───┘ └───┬───┘             │
        │          │         │                 │
        └──────────┴─────────┴─────────────────┘
                          │
                          ↓
                    Cache Miss
                          │
                ┌─────────▼──────────┐
                │   Origin Servers   │
                │   (Your Backend)   │
                └────────────────────┘
```

### Request Flow

```
1. User requests: https://cdn.example.com/video.mp4

2. DNS Resolution:
   - GeoDNS returns IP of nearest edge server
   - Based on user's geographic location

3. Edge Server Processing:
   ┌─────────────────────────────────┐
   │ Check local cache               │
   │   ├─ HIT → Serve from cache     │
   │   └─ MISS → Request from origin │
   │      ├─ Cache response          │
   │      └─ Serve to user           │
   └─────────────────────────────────┘

4. Origin Shield (Optional):
   - Regional cache between edge and origin
   - Reduces origin load
   - Improves cache hit ratio
```

## 5. API Design

### CDN Management API

```
POST /api/v1/content/purge
Request: {
  "urls": [
    "https://cdn.example.com/images/logo.png",
    "https://cdn.example.com/css/*"
  ],
  "purge_type": "invalidate"  // or "delete"
}

POST /api/v1/cache/configure
Request: {
  "path": "/videos/*",
  "ttl": 86400,
  "cache_key_rules": {
    "include_query_string": false,
    "headers": ["Accept-Encoding"]
  },
  "compression": "gzip",
  "origin": "https://origin.example.com"
}

GET /api/v1/analytics
Query: ?start=2025-11-01&end=2025-11-12
Response: {
  "requests": 1000000000,
  "bandwidth_gb": 5000000,
  "cache_hit_ratio": 0.89,
  "top_content": [
    {"url": "/video1.mp4", "requests": 50000000},
    {"url": "/video2.mp4", "requests": 30000000}
  ],
  "geographic_distribution": {
    "us-east": 0.40,
    "eu-west": 0.35,
    "ap-south": 0.25
  }
}

POST /api/v1/origin/configure
Request: {
  "primary": "https://origin1.example.com",
  "failover": ["https://origin2.example.com", "https://origin3.example.com"],
  "health_check": {
    "path": "/health",
    "interval": 10,
    "timeout": 5
  }
}

GET /api/v1/edge-servers/status
Response: {
  "total_servers": 5000,
  "healthy": 4987,
  "degraded": 13,
  "offline": 0,
  "regions": [
    {
      "name": "us-east-1",
      "servers": 25,
      "load_percent": 65,
      "cache_hit_ratio": 0.91
    }
  ]
}
```

## 6. Database Schema

### CDN Configuration Database

```sql
CREATE TABLE edge_locations (
    id VARCHAR(50) PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(50),
    continent VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    capacity_gbps INT,
    status ENUM('active', 'maintenance', 'offline'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_country (country),
    INDEX idx_status (status)
);

CREATE TABLE edge_servers (
    id VARCHAR(100) PRIMARY KEY,
    location_id VARCHAR(50),
    ip_address VARCHAR(45),
    capacity_gbps INT,
    current_load_percent INT,
    storage_tb INT,
    storage_used_tb DECIMAL(10,2),
    status ENUM('healthy', 'degraded', 'offline'),
    last_heartbeat TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES edge_locations(id),
    INDEX idx_location (location_id),
    INDEX idx_status (status)
);

CREATE TABLE cache_rules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    path_pattern VARCHAR(255),
    ttl_seconds INT,
    cache_key_query_params TEXT, -- JSON array
    cache_key_headers TEXT, -- JSON array
    compression ENUM('none', 'gzip', 'brotli'),
    origin_url VARCHAR(255),
    priority INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_path (path_pattern),
    INDEX idx_priority (priority)
);

CREATE TABLE cache_entries (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    edge_server_id VARCHAR(100),
    cache_key VARCHAR(255),
    content_hash VARCHAR(64),
    size_bytes BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count BIGINT DEFAULT 0,
    FOREIGN KEY (edge_server_id) REFERENCES edge_servers(id),
    INDEX idx_cache_key (cache_key),
    INDEX idx_expires (expires_at),
    INDEX idx_server (edge_server_id)
);

CREATE TABLE cdn_analytics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edge_location_id VARCHAR(50),
    requests_count BIGINT,
    cache_hits BIGINT,
    cache_misses BIGINT,
    bandwidth_gb DECIMAL(15,2),
    avg_response_time_ms INT,
    error_4xx_count INT,
    error_5xx_count INT,
    FOREIGN KEY (edge_location_id) REFERENCES edge_locations(id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_location (edge_location_id)
);

CREATE TABLE purge_requests (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    request_id VARCHAR(100) UNIQUE,
    urls TEXT, -- JSON array
    purge_type ENUM('invalidate', 'delete'),
    status ENUM('pending', 'in_progress', 'completed', 'failed'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);
```

## 7. Detailed Component Design

### Edge Server Components

```python
class EdgeServer:
    def __init__(self, location, capacity_gbps, storage_tb):
        self.location = location
        self.cache = LRUCache(capacity_tb=storage_tb)
        self.origin_connector = OriginConnector()
        self.request_router = RequestRouter()

    async def handle_request(self, request):
        """Main request handling logic"""

        # 1. Generate cache key
        cache_key = self.generate_cache_key(request)

        # 2. Check cache
        cached_response = await self.cache.get(cache_key)
        if cached_response and not cached_response.is_expired():
            self.metrics.record_cache_hit()
            return self.add_cdn_headers(cached_response, hit=True)

        # 3. Cache miss - fetch from origin
        self.metrics.record_cache_miss()

        # 4. Check if another request is already fetching
        if await self.request_deduplication.is_pending(cache_key):
            # Wait for the other request to complete
            return await self.request_deduplication.wait_for(cache_key)

        # 5. Fetch from origin
        try:
            self.request_deduplication.mark_pending(cache_key)
            response = await self.fetch_from_origin(request)

            # 6. Cache the response
            if self.should_cache(response):
                await self.cache.set(
                    cache_key,
                    response,
                    ttl=self.get_ttl(request, response)
                )

            return self.add_cdn_headers(response, hit=False)

        finally:
            self.request_deduplication.mark_complete(cache_key)

    def generate_cache_key(self, request):
        """Generate unique cache key based on request"""
        cache_rule = self.get_cache_rule(request.path)

        components = [request.url]

        # Include query params if configured
        if cache_rule.include_query_params:
            components.append(request.query_string)

        # Include specific headers if configured
        for header in cache_rule.cache_key_headers:
            if header in request.headers:
                components.append(f"{header}:{request.headers[header]}")

        return hashlib.sha256("|".join(components).encode()).hexdigest()

    def should_cache(self, response):
        """Determine if response should be cached"""
        # Don't cache errors (except 404s sometimes)
        if response.status_code >= 500:
            return False

        # Check cache-control headers
        cache_control = response.headers.get('Cache-Control', '')
        if 'no-store' in cache_control or 'private' in cache_control:
            return False

        # Check content type
        if response.headers.get('Content-Type', '').startswith('text/html'):
            # Be careful with HTML - might be dynamic
            return self.is_static_html(response)

        return True

    def get_ttl(self, request, response):
        """Calculate TTL for cached response"""
        # 1. Check custom cache rules
        rule = self.get_cache_rule(request.path)
        if rule and rule.ttl:
            return rule.ttl

        # 2. Check response headers
        cache_control = response.headers.get('Cache-Control', '')
        if 'max-age=' in cache_control:
            max_age = int(cache_control.split('max-age=')[1].split(',')[0])
            return max_age

        # 3. Default TTL based on content type
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            return 86400 * 30  # 30 days
        elif 'video' in content_type:
            return 86400 * 7  # 7 days
        elif 'javascript' in content_type or 'css' in content_type:
            return 86400  # 1 day
        else:
            return 3600  # 1 hour
```

### Intelligent Caching

```python
class IntelligentCacheManager:
    def __init__(self):
        self.access_patterns = {}
        self.prefetch_queue = PriorityQueue()

    def record_access(self, url, user_context):
        """Record access patterns for predictive caching"""
        if url not in self.access_patterns:
            self.access_patterns[url] = {
                'count': 0,
                'last_accessed': [],
                'correlated_urls': {}
            }

        pattern = self.access_patterns[url]
        pattern['count'] += 1
        pattern['last_accessed'].append(time.time())

        # Track URL correlation
        if user_context.previous_url:
            prev = user_context.previous_url
            if prev not in pattern['correlated_urls']:
                pattern['correlated_urls'][prev] = 0
            pattern['correlated_urls'][prev] += 1

    def should_prefetch(self, url):
        """Determine if URL should be prefetched"""
        if url not in self.access_patterns:
            return False

        pattern = self.access_patterns[url]

        # Prefetch if frequently accessed
        if pattern['count'] > 1000:
            return True

        # Prefetch if strong correlation with current page
        # (e.g., CSS/JS needed for HTML page)
        for correlated_url, count in pattern['correlated_urls'].items():
            if count > 10:  # Strong correlation
                return True

        return False

    async def prefetch_correlated_content(self, url):
        """Prefetch content likely to be requested next"""
        if url not in self.access_patterns:
            return

        pattern = self.access_patterns[url]

        # Prefetch highly correlated URLs
        for correlated_url, count in pattern['correlated_urls'].items():
            if count > 5:  # Correlation threshold
                if not await self.cache.exists(correlated_url):
                    self.prefetch_queue.put(
                        (-count, correlated_url)  # Higher count = higher priority
                    )

        # Process prefetch queue in background
        asyncio.create_task(self.process_prefetch_queue())
```

### Cache Invalidation

```python
class CacheInvalidationManager:
    def __init__(self, edge_servers):
        self.edge_servers = edge_servers
        self.invalidation_queue = Queue()

    async def purge_content(self, urls, purge_type='invalidate'):
        """
        Purge content from all edge servers

        purge_type:
        - 'invalidate': Mark as stale, revalidate on next request
        - 'delete': Remove from cache immediately
        """
        purge_id = str(uuid.uuid4())

        # Create purge task
        purge_task = {
            'id': purge_id,
            'urls': urls,
            'type': purge_type,
            'timestamp': time.time(),
            'status': {}
        }

        # Fan out to all edge servers
        tasks = []
        for edge_server in self.edge_servers:
            task = self.purge_on_edge(edge_server, urls, purge_type)
            tasks.append(task)

        # Wait for all edge servers to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Track success/failure per edge
        for edge_server, result in zip(self.edge_servers, results):
            if isinstance(result, Exception):
                purge_task['status'][edge_server.id] = 'failed'
            else:
                purge_task['status'][edge_server.id] = 'completed'

        return purge_task

    async def purge_on_edge(self, edge_server, urls, purge_type):
        """Purge content on a single edge server"""
        for url in urls:
            # Support wildcards
            if '*' in url:
                pattern = url.replace('*', '.*')
                cache_keys = edge_server.cache.find_keys(pattern)
            else:
                cache_keys = [edge_server.cache.generate_key(url)]

            for cache_key in cache_keys:
                if purge_type == 'delete':
                    await edge_server.cache.delete(cache_key)
                elif purge_type == 'invalidate':
                    await edge_server.cache.mark_stale(cache_key)

        return True

    async def purge_by_tag(self, tags):
        """Purge content by cache tags"""
        # Tags allow grouping related content
        # E.g., tag all product images with "product:12345"
        urls = await self.get_urls_by_tags(tags)
        return await self.purge_content(urls)
```

### Origin Shield

```python
class OriginShield:
    """
    Regional cache layer between edge servers and origin
    Reduces origin load by consolidating requests
    """
    def __init__(self, origin_url, region):
        self.origin_url = origin_url
        self.region = region
        self.cache = LRUCache(capacity_tb=100)
        self.pending_requests = {}

    async def fetch(self, request):
        """Fetch content, using shield cache"""
        cache_key = self.generate_cache_key(request)

        # Check shield cache
        cached = await self.cache.get(cache_key)
        if cached and not cached.is_expired():
            return cached

        # Request coalescing - if multiple edge servers
        # request same content, only fetch once
        if cache_key in self.pending_requests:
            # Wait for pending request
            return await self.pending_requests[cache_key]

        # Fetch from origin
        try:
            # Create future for other waiting requests
            future = asyncio.Future()
            self.pending_requests[cache_key] = future

            response = await self.fetch_from_origin(request)

            # Cache in shield
            await self.cache.set(cache_key, response, ttl=3600)

            # Notify waiting requests
            future.set_result(response)

            return response

        finally:
            # Cleanup
            if cache_key in self.pending_requests:
                del self.pending_requests[cache_key]
```

## 8. Trade-offs and Considerations

### Push vs Pull CDN

#### Pull CDN (Origin Pull)
```
Edge server doesn't have content → Pulls from origin → Caches
```
**Advantages:**
- Automatic: No manual uploading
- Only caches requested content
- Easy to set up

**Disadvantages:**
- First request is slow (cache miss)
- Origin must be always available
- Unpredictable origin load

#### Push CDN
```
Content uploaded directly to CDN → Distributed to edges
```
**Advantages:**
- First request is fast (pre-cached)
- Lower origin load
- Predictable performance

**Disadvantages:**
- Manual upload process
- Caches all content (might be wasteful)
- Requires invalidation management

### Dynamic Content Caching

**Challenges:**
- Personalized content
- Frequently changing content
- User-specific data

**Solutions:**

1. **Edge Side Includes (ESI):**
```html
<html>
  <body>
    <!-- Cached for everyone -->
    <header>Site Header</header>

    <!-- User-specific, not cached -->
    <esi:include src="/api/user/profile" />

    <!-- Cached for everyone -->
    <footer>Site Footer</footer>
  </body>
</html>
```

2. **Cache Hierarchies:**
```
- Cache full page for 1 hour
- Cache API responses for 5 minutes
- Don't cache user-specific data
```

3. **Vary Headers:**
```
Cache-Control: public, max-age=3600
Vary: Accept-Encoding, Accept-Language

Different cached versions for:
- gzip vs brotli
- en vs es language
```

## 9. Scalability & Bottlenecks

### Geographic Scaling

**Adding New PoPs:**
```python
def add_new_pop(location, capacity):
    """Add new Point of Presence"""
    # 1. Deploy edge servers
    edge_servers = deploy_servers(location, capacity)

    # 2. Warm cache with popular content
    popular_content = get_popular_content(region=location.region)
    for server in edge_servers:
        server.prefetch(popular_content)

    # 3. Update DNS routing
    update_geodns(location, edge_servers)

    # 4. Gradual traffic shift
    shift_traffic(location, percentage=10)  # Start with 10%
    # Monitor for 24 hours
    shift_traffic(location, percentage=100)  # Full traffic
```

### Capacity Planning

```python
class CapacityPlanner:
    def calculate_required_capacity(self, metrics):
        """Calculate required edge capacity"""

        # Bandwidth calculation
        peak_bandwidth_gbps = metrics.peak_requests_per_second * metrics.avg_response_size_kb / 125000

        # Storage calculation
        unique_objects = metrics.unique_urls
        avg_object_size = metrics.avg_response_size_kb
        cache_hit_ratio_target = 0.85

        # Need to cache 85% of frequently accessed content
        objects_to_cache = unique_objects * cache_hit_ratio_target
        storage_needed_tb = objects_to_cache * avg_object_size / (1024**3)

        return {
            'bandwidth_gbps': peak_bandwidth_gbps * 1.5,  # 50% buffer
            'storage_tb': storage_needed_tb * 1.2  # 20% buffer
        }
```

### Bottlenecks

1. **Origin Server Overwhelmed:**
   - Implement origin shield
   - Use connection pooling
   - Rate limit edge-to-origin requests

2. **Cache Stampede:**
   - Request coalescing
   - Stale-while-revalidate
   - Predictive prefetching

3. **Geographic Coverage:**
   - Add more PoPs in underserved regions
   - Use anycast for routing
   - Multi-tier caching

## 10. Follow-up Questions

1. **How do you handle video streaming with CDN?**
   - Adaptive bitrate streaming (HLS, DASH)
   - Segment caching
   - Range request support
   - Origin shield for popular videos

2. **How do you measure CDN performance?**
   - Cache hit ratio
   - Time to first byte (TTFB)
   - Origin offload percentage
   - Geographic latency
   - Availability per PoP

3. **How do you handle SSL/TLS at scale?**
   - Terminate SSL at edge
   - Use session resumption
   - OCSP stapling
   - HTTP/3 with QUIC

4. **How do you protect against DDoS with CDN?**
   - Rate limiting per IP
   - Challenge-response (CAPTCHA)
   - IP reputation filtering
   - Anycast for traffic distribution
   - WAF (Web Application Firewall)

5. **How do you handle cache versioning?**
   - URL versioning: `/css/style.v123.css`
   - Query string: `/css/style.css?v=123`
   - Hash-based: `/css/style.abc123.css`
   - Immutable content with long TTL

6. **What is the difference between CDN and reverse proxy?**
   - CDN: Geographic distribution, global reach
   - Reverse Proxy: Usually single location, more features
   - CDN: Optimized for static content
   - Reverse Proxy: Can handle complex logic

7. **How do you handle mobile vs desktop content?**
   - Vary header on User-Agent
   - Separate cache keys
   - Responsive images with srcset
   - Dynamic content optimization

8. **How do you optimize for different regions?**
   - Regional origin servers
   - GeoDNS routing
   - Regional cache hierarchies
   - Content localization

9. **How do you handle cache coherency across edges?**
   - Eventually consistent by design
   - Invalidation propagation
   - Version-based caching
   - Accept slight staleness

10. **When should you NOT use a CDN?**
    - Highly dynamic personalized content
    - Very low traffic (cost not justified)
    - Content that must never be cached
    - Regulatory requirements for data location
