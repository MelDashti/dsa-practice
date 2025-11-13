# Core Components: Medium Level

## Overview

Medium-level system design problems require deeper understanding of distributed systems, real-time processing, and scalability challenges. These problems test your ability to handle millions of users, implement complex algorithms, and make critical trade-off decisions.

## Problems Overview

### 1. Rate Limiter (rate_limiter.md)
**Design a distributed rate limiting system**

Prevent API abuse and ensure fair resource usage:

**Algorithms:**
- **Token Bucket:** Tokens added at fixed rate, consumed per request
- **Leaky Bucket:** Queue requests, process at fixed rate
- **Fixed Window:** Count requests in fixed time windows
- **Sliding Window Log:** Track individual request timestamps
- **Sliding Window Counter:** Hybrid approach, space-efficient

**Key Challenges:**
- Distributed rate limiting (sync across servers)
- Atomic operations in Redis
- Different limits per user/tier
- Rate limit headers (X-RateLimit-Remaining)

**Scale:** 100K requests/sec, millions of users

**Real-World:** AWS API Gateway, Stripe API, Twitter API

---

### 2. Notification System (notification_system.md)
**Design a multi-channel notification service**

Send push notifications, emails, and SMS at scale:

**Components:**
- **Notification Service:** Receives notification requests
- **Channel Handlers:** Push (FCM/APNs), Email (SES), SMS (Twilio)
- **Priority Queue:** Urgent vs normal notifications
- **Delivery Tracking:** Read receipts, delivery status
- **Retry Logic:** Exponential backoff for failures

**Key Challenges:**
- Multi-channel delivery (push, email, SMS)
- User preferences and opt-outs
- Rate limiting per channel
- Template management
- Delivery guarantees

**Scale:** 10M notifications/day, 1M DAU

**Real-World:** Firebase Cloud Messaging, SendGrid, Twilio

---

### 3. Autocomplete / Typeahead (autocomplete.md)
**Design search autocomplete system**

Provide real-time search suggestions as users type:

**Data Structures:**
- **Trie (Prefix Tree):** Fast prefix matching
- **Inverted Index:** Multi-word queries
- **Frequency-based Ranking:** Popular suggestions first

**Optimizations:**
- **Caching:** Cache top queries per prefix
- **Precomputation:** Build suggestions offline
- **Personalization:** User history and location
- **Fuzzy Matching:** Typo tolerance

**Key Challenges:**
- Sub-100ms latency requirement
- Ranking algorithm (popularity + personalization)
- Handling typos and synonyms
- Real-time index updates

**Scale:** 10K queries/sec, 10M search terms

**Real-World:** Google Search, Amazon Search, YouTube

---

### 4. Authentication System (authentication_system.md)
**Design OAuth/JWT authentication system**

Secure user authentication and authorization:

**Components:**
- **Authentication:** Login, signup, password reset
- **Authorization:** Permission checks, role-based access
- **Session Management:** JWT tokens, refresh tokens
- **OAuth 2.0:** Third-party login (Google, Facebook)
- **MFA:** Two-factor authentication

**Security:**
- Password hashing (bcrypt, Argon2)
- Token encryption and signing
- Rate limiting login attempts
- Session invalidation
- CSRF protection

**Key Challenges:**
- Distributed session management
- Token refresh strategy
- SSO (Single Sign-On)
- Account compromise detection

**Scale:** 1M users, 100K logins/day

**Real-World:** Auth0, Okta, AWS Cognito

---

## Difficulty Comparison

| Problem | Primary Challenge | Latency Req | Data Structure |
|---------|------------------|-------------|----------------|
| **Rate Limiter** | Distributed counters | <1ms | Sliding window |
| **Notification** | Multi-channel delivery | Async | Priority queue |
| **Autocomplete** | Sub-second suggestions | <100ms | Trie |
| **Authentication** | Security + scale | <50ms | Token-based |

## Core Algorithms

### Token Bucket (Rate Limiter)
```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()

    def allow_request(self):
        # Refill tokens
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

        # Check if request allowed
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### Trie (Autocomplete)
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class Autocomplete:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency = frequency

    def search(self, prefix, limit=10):
        # Find prefix node
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # DFS to find all completions
        results = []
        self._dfs(node, prefix, results)

        # Sort by frequency and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in results[:limit]]
```

## System Design Patterns

### Pattern 1: Distributed Rate Limiting
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Server 1 │     │ Server 2 │     │ Server 3 │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     └────────────────┼────────────────┘
                      │
              ┌───────▼────────┐
              │  Redis Cluster │  ← Atomic counters
              │  (Distributed) │
              └────────────────┘

Challenges:
- Synchronization across servers
- Race conditions
- Network latency

Solutions:
- Redis atomic operations (INCR)
- Lua scripts for complex logic
- Local cache + periodic sync
```

### Pattern 2: Fanout on Write (Notifications)
```
User posts update
       │
       ↓
 ┌────────────┐
 │  Post API  │
 └─────┬──────┘
       │ Publish event
       ↓
 ┌────────────┐
 │Event Queue │
 └─────┬──────┘
       │
  ┌────┼────┐
  │    │    │
  ↓    ↓    ↓
[Worker Pools]
  │    │    │
  ↓    ↓    ↓
Users' notification feeds

Trade-off: Write amplification for read performance
```

### Pattern 3: Multi-tier Caching (Autocomplete)
```
Client Request
      │
      ↓
┌───────────┐
│ Browser   │  ← L1: In-memory (10ms)
│ Cache     │
└─────┬─────┘
      │ Miss
      ↓
┌───────────┐
│ CDN Edge  │  ← L2: Edge cache (50ms)
└─────┬─────┘
      │ Miss
      ↓
┌───────────┐
│ Redis     │  ← L3: Distributed (5ms)
└─────┬─────┘
      │ Miss
      ↓
┌───────────┐
│ Database  │  ← L4: Source of truth (50ms)
└───────────┘

95%+ requests served from cache
```

## Trade-off Decisions

### Rate Limiter: Accuracy vs Performance
**Accurate (Sliding Window Log):**
- Store all request timestamps
- Precise rate limiting
- High memory usage

**Fast (Fixed Window Counter):**
- Just count requests per window
- Possible 2x burst at window boundary
- Very low memory usage

**Balanced (Sliding Window Counter):**
- Current + previous window counts
- Weighted calculation
- Good accuracy, low memory

### Notification: Push vs Pull
**Push (Fanout on Write):**
- Write: Slow (N followers)
- Read: Fast (pre-computed)
- Best for: Read-heavy, followers < 1M

**Pull (Fanout on Read):**
- Write: Fast (single write)
- Read: Slow (query N followees)
- Best for: Write-heavy, celebrity users

## Interview Deep Dive

### Rate Limiter
**Q:** "How would you implement distributed rate limiting?"

**Answer Framework:**
1. **Centralized:** Redis with atomic operations
2. **Decentralized:** Local limits + eventual consistency
3. **Hybrid:** Local cache + Redis sync

```python
# Redis Lua script for atomic rate limit check
lua_script = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, window)
end

if current > limit then
    return 0  -- Rate limited
else
    return 1  -- Allowed
end
"""
```

### Notification System
**Q:** "How do you handle failed notifications?"

**Answer Framework:**
1. **Retry Strategy:** Exponential backoff (1s, 2s, 4s, 8s...)
2. **Dead Letter Queue:** After max retries, store for manual review
3. **Circuit Breaker:** Stop sending to failing channel
4. **Fallback:** Try alternative channel (push fails → email)

### Autocomplete
**Q:** "How do you handle typos in autocomplete?"

**Answer Framework:**
1. **Edit Distance:** Levenshtein distance (fuzzy match)
2. **Phonetic:** Soundex, Metaphone (sound-alike)
3. **Keyboard Proximity:** Adjacent key typos
4. **Machine Learning:** Learn common typo patterns

### Authentication
**Q:** "JWT vs Session tokens?"

| Aspect | JWT | Session Token |
|--------|-----|---------------|
| **Storage** | Client-side | Server-side |
| **Scalability** | Stateless (better) | Requires shared state |
| **Revocation** | Hard (need blacklist) | Easy (delete session) |
| **Size** | Large (~500 bytes) | Small (32 bytes) |
| **Use Case** | Microservices, API | Traditional web apps |

## Common Pitfalls

### Rate Limiter
❌ Not handling distributed clock skew
❌ Race conditions in distributed counters
❌ No graceful degradation

✅ Use monotonic time or logical clocks
✅ Atomic operations (Redis Lua)
✅ Degrade to per-server limits if Redis down

### Notification System
❌ No idempotency (duplicate notifications)
❌ Not handling channel-specific failures
❌ No user preference management

✅ Idempotency keys for deduplication
✅ Per-channel retry strategies
✅ User opt-out/preferences table

### Autocomplete
❌ No caching (too slow)
❌ Not handling high-cardinality prefixes
❌ No personalization

✅ Multi-tier caching
✅ Top-K suggestions per prefix
✅ User history and location signals

### Authentication
❌ Weak password policies
❌ No rate limiting on login
❌ Insecure token storage

✅ Strong hashing (bcrypt, scrypt)
✅ Exponential backoff + CAPTCHA
✅ httpOnly cookies or secure storage

## Real-World Scale References

| System | Problem | Scale |
|--------|---------|-------|
| **Stripe API** | Rate Limiter | 100K requests/sec/user |
| **Firebase** | Notifications | 250B messages/month |
| **Google Search** | Autocomplete | 40K searches/second |
| **Auth0** | Authentication | 2.5B logins/month |

## Practice Recommendations

1. **Implement:** Build a working prototype of each system
2. **Benchmark:** Measure latency and throughput
3. **Break It:** Simulate failures and test recovery
4. **Optimize:** Profile and optimize hot paths

## Success Metrics

You've mastered medium-level problems when you can:
- ✅ Design systems handling millions of requests
- ✅ Implement critical algorithms from scratch
- ✅ Make informed trade-off decisions
- ✅ Handle distributed systems challenges
- ✅ Discuss security implications
- ✅ Optimize for latency and throughput

---

**Estimated Study Time:** 1-2 weeks for all four problems (with implementation)

**Interview Frequency:** 80% of mid-to-senior level interviews include at least one of these problems.
