# Distributed Rate Limiter - Global Rate Limiting

## 1. Problem Statement

Design a distributed rate limiting system that can enforce rate limits across multiple servers and data centers with high accuracy, low latency, and fault tolerance. The system should support multiple rate limiting algorithms, handle millions of requests per second, and provide both per-user and per-API rate limiting with minimal coordination overhead.

## 2. Requirements

### Functional Requirements
- **Multiple algorithms**: Token bucket, leaky bucket, fixed window, sliding window
- **Multi-dimensional limits**: Per user, per API, per IP, per tenant
- **Distributed coordination**: Consistent limits across all nodes
- **Dynamic configuration**: Update limits without restart
- **Burst handling**: Allow controlled burst traffic
- **Grace periods**: Soft vs hard limits
- **Rate limit headers**: Return limit status in response headers
- **Allow-listing**: Bypass limits for certain users/IPs

### Non-Functional Requirements
- **Latency**: P99 < 1ms for rate limit check
- **Throughput**: Handle 10 million requests/second
- **Accuracy**: 95%+ accuracy for rate limits
- **Availability**: 99.99% uptime
- **Scalability**: Support 1 billion unique limiters
- **Consistency**: Eventual consistency acceptable (within 100ms)
- **Cost**: Minimize cross-datacenter traffic

### Out of Scope
- DDoS attack mitigation (separate system)
- Application-level authentication
- Request routing and load balancing

## 3. Capacity Estimation

### Scale Assumptions
- Total requests: 10 million/second
- Unique users: 100 million
- API endpoints: 10,000
- Rate limiters: 1 billion (user × API combinations)
- Average rate limit: 1000 req/hour per user per API
- Rate limiter nodes: 100
- Data centers: 3

### Memory Estimation
```
Per rate limiter state:
- User ID: 8 bytes
- API ID: 4 bytes
- Token count: 4 bytes
- Last update time: 8 bytes
- Total: 24 bytes

Active limiters (in memory):
- Assume 1% active at any time
- 1B × 0.01 = 10M active limiters
- Memory: 10M × 24 bytes = 240 MB

Per node (100 nodes):
- 240 MB / 100 = 2.4 MB per node
- With overhead and caching: ~100 MB per node
```

### Network Bandwidth
```
Per request overhead:
- Rate limit check: 100 bytes
- 10M req/sec × 100 bytes = 1 GB/sec = 8 Gbps

Cross-DC sync:
- Sync every 100ms
- Aggregate counters per sync: 10KB
- Bandwidth: 10KB × 10/sec × 3 DCs = 300 KB/sec (negligible)
```

## 4. High-Level Design

```
┌──────────────────────────────────────────────┐
│          Client Applications                 │
└───────────────┬──────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│         API Gateway / Load Balancer           │
└───────┬───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────┐
│       Rate Limiter Middleware                 │
│  - Extract user/API info                      │
│  - Check rate limit                           │
│  - Update counters                            │
└───────┬───────────────────────────────────────┘
        │
        ├──── Allow ────► Backend Service
        │
        └──── Block ────► 429 Too Many Requests

Rate Limiter Architecture:

┌───────────────────────────────────────────────┐
│         Rate Limiter Cluster                  │
│                                               │
│  ┌─────────────────────────────────────────┐│
│  │     Local Rate Limiter                  ││
│  │  - Token bucket per user/API            ││
│  │  - In-memory counters                   ││
│  │  - Fast local checks (P99 < 1ms)        ││
│  └──────────┬──────────────────────────────┘│
│             │                                 │
│             ▼                                 │
│  ┌─────────────────────────────────────────┐│
│  │     Global Coordinator                  ││
│  │  - Aggregate counters                   ││
│  │  - Periodic sync (every 100ms)          ││
│  │  - Distribute quota                     ││
│  └──────────┬──────────────────────────────┘│
│             │                                 │
└─────────────┼─────────────────────────────────┘
              │
              ▼
   ┌──────────────────────────────┐
   │   Distributed Storage        │
   │   (Redis Cluster)            │
   │  - Persistent rate limits    │
   │  - Configuration             │
   └──────────────────────────────┘

   ┌──────────────────────────────┐
   │   Configuration Service      │
   │  - Rate limit rules          │
   │  - Dynamic updates           │
   └──────────────────────────────┘
```

### Core Components
1. **Local Rate Limiter**: Fast in-memory checks
2. **Global Coordinator**: Aggregates and syncs across nodes
3. **Storage Layer**: Persistent state and configuration
4. **Sync Protocol**: Efficient state synchronization
5. **Configuration Manager**: Dynamic limit updates
6. **Monitoring**: Track limit violations and usage

## 5. API Design

### Rate Limiter API

```python
class RateLimiter:
    def check_limit(
        self,
        key: str,              # e.g., "user:123:api:/users"
        limit: int,             # Max requests
        window_seconds: int     # Time window
    ) -> RateLimitResult:
        """
        Check if request should be allowed
        Returns: {
            allowed: bool,
            remaining: int,
            reset_time: int,
            retry_after: int
        }
        """
        pass

    def consume(
        self,
        key: str,
        tokens: int = 1
    ) -> bool:
        """
        Consume tokens from bucket
        Returns: True if allowed, False if limit exceeded
        """
        pass

    def get_status(self, key: str) -> RateLimitStatus:
        """
        Get current status of rate limiter
        Returns: current tokens, limit, window
        """
        pass

    def reset(self, key: str):
        """Reset rate limiter for key"""
        pass

    def update_limit(self, key: str, new_limit: int):
        """Dynamically update limit"""
        pass
```

### Configuration API

```python
class RateLimitConfig:
    def create_rule(self, rule: RateLimitRule) -> str:
        """
        Create rate limit rule
        RateLimitRule: {
            name: str,
            dimension: str,  # user, ip, tenant, api
            limit: int,
            window: int,
            algorithm: str,  # token_bucket, fixed_window, sliding_window
            burst_limit: int,  # Allow burst traffic
            priority: int
        }
        """
        pass

    def update_rule(self, rule_id: str, updates: RateLimitRule):
        """Update existing rule"""
        pass

    def delete_rule(self, rule_id: str):
        """Delete rule"""
        pass

    def add_allowlist(self, key: str):
        """Add key to allow-list (bypass limits)"""
        pass
```

## 6. Component Design

### Token Bucket Algorithm

```python
class TokenBucket:
    """
    Token bucket rate limiter
    - Tokens refill at constant rate
    - Burst traffic allowed up to bucket capacity
    - Most flexible algorithm
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: Max tokens in bucket
        refill_rate: Tokens per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def try_consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens
        Returns True if allowed, False if rate limited
        """
        with self.lock:
            # Refill tokens based on time elapsed
            now = time.time()
            elapsed = now - self.last_refill

            # Add tokens (rate limited by capacity)
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

            # Try to consume
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False

    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Calculate wait time until tokens available
        """
        with self.lock:
            if self.tokens >= tokens:
                return 0

            tokens_needed = tokens - self.tokens
            return tokens_needed / self.refill_rate

    def peek(self) -> float:
        """Get current token count without consuming"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            tokens_to_add = elapsed * self.refill_rate
            return min(self.capacity, self.tokens + tokens_to_add)
```

**Time Complexity**: O(1)
**Space Complexity**: O(1) per limiter

### Sliding Window Counter

```python
class SlidingWindowCounter:
    """
    Sliding window rate limiter
    - More accurate than fixed window
    - Prevents burst at window boundaries
    - Uses weighted count from previous window
    """

    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.current_window_start = 0
        self.current_count = 0
        self.previous_count = 0
        self.lock = threading.Lock()

    def try_consume(self) -> bool:
        """Check and consume request"""
        with self.lock:
            now = time.time()
            current_window = int(now // self.window_seconds)

            # New window started
            if current_window > self.current_window_start:
                self.previous_count = self.current_count
                self.current_count = 0
                self.current_window_start = current_window

            # Calculate weighted count
            window_progress = (now % self.window_seconds) / self.window_seconds
            weighted_count = (
                self.previous_count * (1 - window_progress) +
                self.current_count
            )

            # Check limit
            if weighted_count < self.limit:
                self.current_count += 1
                return True
            else:
                return False

    def get_remaining(self) -> int:
        """Get remaining quota"""
        with self.lock:
            now = time.time()
            window_progress = (now % self.window_seconds) / self.window_seconds
            weighted_count = (
                self.previous_count * (1 - window_progress) +
                self.current_count
            )
            return max(0, self.limit - int(weighted_count))
```

**Time Complexity**: O(1)
**Space Complexity**: O(1) per limiter

### Fixed Window Counter

```python
class FixedWindowCounter:
    """
    Fixed window rate limiter
    - Simplest algorithm
    - Allows burst at window boundaries
    - Most memory efficient
    """

    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.window_start = int(time.time() // window_seconds)
        self.count = 0
        self.lock = threading.Lock()

    def try_consume(self) -> bool:
        """Check and consume request"""
        with self.lock:
            now = time.time()
            current_window = int(now // self.window_seconds)

            # Reset if new window
            if current_window > self.window_start:
                self.window_start = current_window
                self.count = 0

            # Check limit
            if self.count < self.limit:
                self.count += 1
                return True
            else:
                return False

    def get_remaining(self) -> int:
        """Get remaining quota"""
        with self.lock:
            return max(0, self.limit - self.count)

    def get_reset_time(self) -> int:
        """Get time when window resets"""
        return (self.window_start + 1) * self.window_seconds
```

**Time Complexity**: O(1)
**Space Complexity**: O(1) per limiter

### Distributed Rate Limiter

```python
class DistributedRateLimiter:
    """
    Distributed rate limiter with local + global coordination
    Strategy: Optimistic local limiting with periodic sync
    """

    def __init__(self):
        self.local_limiters = {}  # key -> LocalLimiter
        self.redis = RedisClient()
        self.sync_interval = 0.1  # 100ms
        self.last_sync = time.time()

    async def check_limit(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> RateLimitResult:
        """
        Check rate limit with distributed coordination
        """
        # 1. Fast local check (optimistic)
        local_limiter = self.get_local_limiter(key, limit, window_seconds)

        if not local_limiter.try_consume():
            # Locally rate limited
            return RateLimitResult(
                allowed=False,
                remaining=0,
                reset_time=local_limiter.get_reset_time()
            )

        # 2. Periodic global sync (asynchronous)
        if time.time() - self.last_sync > self.sync_interval:
            asyncio.create_task(self.sync_to_global())

        # 3. Occasionally verify with global state
        if random.random() < 0.01:  # 1% of requests
            global_allowed = await self.check_global_limit(key, limit, window_seconds)
            if not global_allowed:
                # Adjust local limiter
                local_limiter.throttle()
                return RateLimitResult(allowed=False, remaining=0)

        return RateLimitResult(
            allowed=True,
            remaining=local_limiter.get_remaining()
        )

    def get_local_limiter(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> TokenBucket:
        """Get or create local limiter"""
        if key not in self.local_limiters:
            # Allocate portion of global limit to this node
            local_limit = limit // self.get_node_count()

            # Add buffer for burst traffic
            capacity = int(local_limit * 1.2)

            self.local_limiters[key] = TokenBucket(
                capacity=capacity,
                refill_rate=local_limit / window_seconds
            )

        return self.local_limiters[key]

    async def sync_to_global(self):
        """Sync local state to global Redis"""
        self.last_sync = time.time()

        # Aggregate local counts
        updates = {}
        for key, limiter in self.local_limiters.items():
            # Get consumed tokens since last sync
            consumed = limiter.get_consumed_since_sync()
            if consumed > 0:
                updates[key] = consumed

        if updates:
            # Batch update to Redis
            await self.redis.increment_batch(updates)

            # Reset local sync counters
            for key in updates:
                self.local_limiters[key].reset_sync_counter()

    async def check_global_limit(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> bool:
        """Check global rate limit in Redis"""
        # Use Redis for global counter
        global_key = f"ratelimit:{key}"

        # Sliding window using sorted set
        now = time.time()
        window_start = now - window_seconds

        # Remove old entries
        await self.redis.zremrangebyscore(global_key, 0, window_start)

        # Count current requests
        current_count = await self.redis.zcard(global_key)

        if current_count >= limit:
            return False

        # Add current request
        await self.redis.zadd(global_key, {str(uuid.uuid4()): now})

        # Set expiration
        await self.redis.expire(global_key, window_seconds * 2)

        return True
```

### Redis-Based Implementation

```python
class RedisRateLimiter:
    """
    Redis-based rate limiter using Lua scripts for atomicity
    Good for distributed systems where local caching isn't needed
    """

    def __init__(self, redis_client):
        self.redis = redis_client

        # Lua script for atomic rate limit check
        self.sliding_window_script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local limit = tonumber(ARGV[3])

        local clear_before = now - window

        -- Remove old entries
        redis.call('ZREMRANGEBYSCORE', key, 0, clear_before)

        -- Count current entries
        local current = redis.call('ZCARD', key)

        if current < limit then
            -- Add new entry
            redis.call('ZADD', key, now, now .. math.random())
            redis.call('EXPIRE', key, window * 2)
            return {1, limit - current - 1}
        else
            return {0, 0}
        end
        """

        self.token_bucket_script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local capacity = tonumber(ARGV[2])
        local rate = tonumber(ARGV[3])
        local requested = tonumber(ARGV[4])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_update')
        local tokens = tonumber(bucket[1]) or capacity
        local last_update = tonumber(bucket[2]) or now

        -- Refill tokens
        local elapsed = now - last_update
        tokens = math.min(capacity, tokens + elapsed * rate)

        -- Try to consume
        if tokens >= requested then
            tokens = tokens - requested
            redis.call('HMSET', key, 'tokens', tokens, 'last_update', now)
            redis.call('EXPIRE', key, 3600)
            return {1, math.floor(tokens)}
        else
            return {0, math.floor(tokens)}
        end
        """

    async def check_limit_sliding_window(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> Tuple[bool, int]:
        """
        Check rate limit using sliding window
        Returns: (allowed, remaining)
        """
        result = await self.redis.eval(
            self.sliding_window_script,
            keys=[f"ratelimit:{key}"],
            args=[time.time(), window_seconds, limit]
        )

        return result[0] == 1, result[1]

    async def check_limit_token_bucket(
        self,
        key: str,
        capacity: int,
        rate: float,
        tokens: int = 1
    ) -> Tuple[bool, int]:
        """
        Check rate limit using token bucket
        Returns: (allowed, remaining_tokens)
        """
        result = await self.redis.eval(
            self.token_bucket_script,
            keys=[f"ratelimit:{key}"],
            args=[time.time(), capacity, rate, tokens]
        )

        return result[0] == 1, result[1]
```

### Multi-Dimensional Rate Limiting

```python
class MultiDimensionalRateLimiter:
    """
    Support rate limiting across multiple dimensions
    Example: 1000 req/hour per user + 10000 req/hour per API
    """

    def __init__(self):
        self.limiters = {}
        self.rules = []  # List of rate limit rules

    async def check_limits(self, request: Request) -> RateLimitResult:
        """
        Check all applicable rate limit rules
        Request is allowed only if all limits are satisfied
        """
        # Extract dimensions
        user_id = request.user_id
        api_path = request.path
        ip_address = request.ip
        tenant_id = request.tenant_id

        # Check each applicable rule
        for rule in self.rules:
            key = self.build_key(rule, user_id, api_path, ip_address, tenant_id)

            if rule.dimension in ['user', 'ip', 'tenant', 'api']:
                result = await self.check_single_limit(
                    key,
                    rule.limit,
                    rule.window,
                    rule.algorithm
                )

                if not result.allowed:
                    return result

        # All limits satisfied
        return RateLimitResult(allowed=True)

    def build_key(
        self,
        rule: RateLimitRule,
        user_id: str,
        api_path: str,
        ip_address: str,
        tenant_id: str
    ) -> str:
        """Build rate limit key from dimensions"""
        parts = [rule.name]

        if rule.dimension == 'user':
            parts.append(f"user:{user_id}")
        elif rule.dimension == 'api':
            parts.append(f"api:{api_path}")
        elif rule.dimension == 'ip':
            parts.append(f"ip:{ip_address}")
        elif rule.dimension == 'tenant':
            parts.append(f"tenant:{tenant_id}")
        elif rule.dimension == 'user_api':
            parts.extend([f"user:{user_id}", f"api:{api_path}"])

        return ":".join(parts)

    async def check_single_limit(
        self,
        key: str,
        limit: int,
        window: int,
        algorithm: str
    ) -> RateLimitResult:
        """Check single rate limit"""
        if algorithm == 'token_bucket':
            return await self.check_token_bucket(key, limit, window)
        elif algorithm == 'sliding_window':
            return await self.check_sliding_window(key, limit, window)
        elif algorithm == 'fixed_window':
            return await self.check_fixed_window(key, limit, window)
```

## 7. Data Structures & Storage

### In-Memory Storage

```python
# Per-limiter state
class RateLimiterState:
    key: str                    # Unique identifier
    tokens: float               # Current tokens (token bucket)
    last_refill: float          # Last refill time
    window_start: int           # Window start (fixed window)
    current_count: int          # Current count (fixed window)
    previous_count: int         # Previous count (sliding window)
```

### Redis Storage

```
Key pattern: ratelimit:{dimension}:{id}:{rule}
Value: Hash or Sorted Set

Token Bucket (Hash):
  tokens: 950.5
  last_update: 1234567890.123

Sliding Window (Sorted Set):
  Score: timestamp
  Member: unique request ID
```

## 8. Fault Tolerance & High Availability

### Graceful Degradation

```python
async def check_limit_with_fallback(self, key: str, limit: int) -> bool:
    """
    Check rate limit with fallback strategies
    """
    try:
        # Try Redis (global state)
        return await self.redis_limiter.check_limit(key, limit)
    except RedisUnavailableError:
        # Fall back to local limiter
        logger.warning("Redis unavailable, using local limiter")
        return self.local_limiter.check_limit(key, limit * 1.2)  # 20% buffer
    except Exception as e:
        # Ultimate fallback: allow request
        logger.error(f"Rate limiter error: {e}")
        return True  # Fail open to avoid service disruption
```

### Consistency vs Availability Trade-off

- **Strong consistency**: Block on Redis, risk availability
- **Eventual consistency (chosen)**: Local limiting + periodic sync
  - 95%+ accuracy
  - Sub-millisecond latency
  - Highly available

## 9. Monitoring & Observability

```python
# Metrics
rate_limit_checks_total = Counter('rate_limit_checks_total', labels=['result'])
rate_limit_violations = Counter('rate_limit_violations', labels=['dimension'])
rate_limit_latency = Histogram('rate_limit_latency_seconds')
rate_limit_accuracy = Gauge('rate_limit_accuracy_percent')
```

## 10. Scalability

- **Horizontal scaling**: Add more rate limiter nodes
- **Sharding**: Partition limiters across Redis shards
- **Local caching**: Reduce Redis load
- **Batching**: Batch Redis updates

## 11. Trade-offs

### Accuracy vs Performance
- **100% accurate**: Centralized, slower
- **95% accurate (chosen)**: Distributed, faster

### Algorithm Choice
- **Token Bucket**: Best for API rate limiting (allows bursts)
- **Sliding Window**: Most accurate, higher overhead
- **Fixed Window**: Simplest, allows boundary bursts

### Local vs Global
- **Pure local**: Fast, inaccurate
- **Pure global**: Accurate, slow
- **Hybrid (chosen)**: Balance of both

## 12. Follow-up Questions

1. How would you handle rate limiting in multi-region deployments?
2. How would you implement rate limiting for WebSocket connections?
3. How would you handle rate limit bypass for premium users?
4. How would you implement adaptive rate limiting based on system load?
5. How would you prevent gaming of rate limits (distributed attacks)?
6. How would you implement hierarchical rate limiting (org → team → user)?
7. How would you handle clock skew across distributed nodes?
8. How would you implement rate limiting for batch/bulk operations?
9. How would you provide real-time rate limit analytics?
10. How would you handle migration from one algorithm to another?
