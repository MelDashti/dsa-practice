# Load Balancing 101: Algorithms, Health Checks, and Distribution

## 1. Problem Statement

How do we distribute incoming network traffic across multiple servers to ensure high availability, prevent server overload, and provide optimal performance? Load balancing is essential for scaling applications horizontally and maintaining system reliability.

## 2. Requirements

### Functional Requirements
- Distribute traffic across multiple backend servers
- Detect and route around unhealthy servers
- Support different routing algorithms
- Handle connection persistence (sticky sessions) when needed
- Provide SSL/TLS termination
- Support multiple protocols (HTTP, HTTPS, TCP, UDP)

### Non-functional Requirements
- High availability: 99.99% uptime
- Low latency overhead: <5ms
- High throughput: 100K+ requests/second
- Automatic failover: <1 second
- Horizontal scalability: Support 1000+ backend servers
- Health check frequency: Every 2-10 seconds

## 3. Capacity Estimation

### Example: E-commerce Platform

**Traffic:**
- Peak traffic: 50,000 requests/second
- Average request size: 5 KB
- Average response size: 50 KB
- Bandwidth required: 50,000 * 55 KB = 2.75 GB/s

**Backend Servers:**
- Each server handles: 500 RPS
- Servers needed: 50,000 / 500 = 100 servers
- With redundancy (N+2): 102 servers

**Load Balancer Capacity:**
```
Connections per second: 50,000
Concurrent connections: ~100,000
Network throughput: 3 GB/s (with overhead)
Health checks: 102 servers * 1 check/2s = 51 checks/second
Memory for connection tracking: ~500 MB
```

## 4. High-Level Design

### Load Balancer Architecture

```
                    Internet
                       │
                       ↓
            ┌──────────────────────┐
            │   DNS (Round Robin)  │
            └──────────┬───────────┘
                       │
           ┌───────────┴───────────┐
           ↓                       ↓
    ┌─────────────┐         ┌─────────────┐
    │ Load        │         │ Load        │
    │ Balancer 1  │←───────→│ Balancer 2  │
    │ (Active)    │ Heartbeat│ (Standby)  │
    └──────┬──────┘         └─────────────┘
           │
    ┌──────┴──────────────────────┐
    │    Connection Pool          │
    └─┬────┬────┬────┬────┬──────┘
      │    │    │    │    │
      ↓    ↓    ↓    ↓    ↓
    ┌───┐┌───┐┌───┐┌───┐┌───┐
    │WS1││WS2││WS3││WS4││WS5│  Web Servers
    └───┘└───┘└───┘└───┘└───┘
```

### Multi-Layer Load Balancing

```
Client Request
      │
      ↓
[Layer 4 Load Balancer] ← TCP/UDP level
      │
      ↓
[Layer 7 Load Balancer] ← HTTP/Application level
      │
      ↓
[Application Servers]
      │
      ↓
[Database Load Balancer] ← DB connection pooling
      │
      ↓
[Database Servers]
```

## 5. API Design

### Load Balancer Configuration API

```
POST /api/v1/backend/register
Request: {
  "host": "10.0.1.15",
  "port": 8080,
  "weight": 100,
  "max_connections": 1000,
  "health_check_path": "/health"
}

DELETE /api/v1/backend/{server_id}

GET /api/v1/backend/list
Response: {
  "backends": [
    {
      "id": "srv1",
      "host": "10.0.1.15",
      "port": 8080,
      "status": "healthy",
      "current_connections": 245,
      "total_requests": 1500000,
      "weight": 100
    }
  ]
}

PUT /api/v1/backend/{server_id}/weight
Request: {
  "weight": 150
}

GET /api/v1/stats
Response: {
  "total_requests": 10000000,
  "active_connections": 5000,
  "requests_per_second": 12500,
  "bytes_sent": 500000000000,
  "bytes_received": 50000000000,
  "backend_health": {
    "healthy": 98,
    "unhealthy": 2,
    "total": 100
  }
}

POST /api/v1/health-check/configure
Request: {
  "interval_seconds": 5,
  "timeout_seconds": 2,
  "unhealthy_threshold": 3,
  "healthy_threshold": 2,
  "path": "/health",
  "expected_status": 200
}
```

## 6. Database Schema

### Load Balancer Configuration

```sql
CREATE TABLE backend_servers (
    id VARCHAR(50) PRIMARY KEY,
    host VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    weight INT DEFAULT 100,
    max_connections INT DEFAULT 1000,
    status ENUM('healthy', 'unhealthy', 'draining', 'disabled') DEFAULT 'healthy',
    health_check_path VARCHAR(255) DEFAULT '/health',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    UNIQUE KEY unique_host_port (host, port)
);

CREATE TABLE health_check_results (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    backend_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('success', 'failure'),
    response_time_ms INT,
    status_code INT,
    error_message TEXT,
    FOREIGN KEY (backend_id) REFERENCES backend_servers(id),
    INDEX idx_backend_timestamp (backend_id, timestamp)
);

CREATE TABLE lb_statistics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    backend_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_requests BIGINT,
    active_connections INT,
    requests_per_second INT,
    avg_response_time_ms INT,
    error_count INT,
    bytes_sent BIGINT,
    bytes_received BIGINT,
    FOREIGN KEY (backend_id) REFERENCES backend_servers(id),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE connection_tracking (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    client_ip VARCHAR(45),
    backend_id VARCHAR(50),
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id),
    INDEX idx_client (client_ip)
);
```

## 7. Detailed Component Design

### Load Balancing Algorithms

#### 1. Round Robin

**Algorithm:**
```python
class RoundRobinBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0

    def get_next_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

**Characteristics:**
- Simple and fair distribution
- Equal weight to all servers
- No consideration of server load
- Works well when servers are identical

**Best For:** Homogeneous server pools, stateless applications

#### 2. Weighted Round Robin

**Algorithm:**
```python
class WeightedRoundRobinBalancer:
    def __init__(self, servers):
        # servers = [(server1, weight1), (server2, weight2), ...]
        self.weighted_list = []
        for server, weight in servers:
            self.weighted_list.extend([server] * weight)
        self.current = 0

    def get_next_server(self):
        server = self.weighted_list[self.current]
        self.current = (self.current + 1) % len(self.weighted_list)
        return server
```

**Characteristics:**
- Accounts for different server capacities
- Higher weight = more requests
- Still deterministic

**Best For:** Heterogeneous server pools

#### 3. Least Connections

**Algorithm:**
```python
class LeastConnectionsBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.connections = {server: 0 for server in servers}

    def get_next_server(self):
        # Select server with fewest active connections
        return min(self.connections.items(), key=lambda x: x[1])[0]

    def track_connection(self, server, increment=True):
        if increment:
            self.connections[server] += 1
        else:
            self.connections[server] -= 1
```

**Characteristics:**
- Dynamic load distribution
- Considers current server load
- Better for long-lived connections

**Best For:** Variable request processing times, WebSocket connections

#### 4. Weighted Least Connections

**Algorithm:**
```python
class WeightedLeastConnectionsBalancer:
    def __init__(self, servers):
        # servers = [(server1, weight1), (server2, weight2), ...]
        self.servers = dict(servers)
        self.connections = {server: 0 for server, _ in servers}

    def get_next_server(self):
        # Select server with lowest connection/weight ratio
        ratios = {
            server: self.connections[server] / self.servers[server]
            for server in self.servers
        }
        return min(ratios.items(), key=lambda x: x[1])[0]
```

**Best For:** Heterogeneous servers with variable processing times

#### 5. IP Hash

**Algorithm:**
```python
import hashlib

class IPHashBalancer:
    def __init__(self, servers):
        self.servers = servers

    def get_next_server(self, client_ip):
        # Hash client IP to consistently route to same server
        hash_value = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        index = hash_value % len(self.servers)
        return self.servers[index]
```

**Characteristics:**
- Same client → same server
- Natural session persistence
- No state required in load balancer
- Can cause uneven distribution

**Best For:** Session-based applications without sticky sessions

#### 6. Least Response Time

**Algorithm:**
```python
class LeastResponseTimeBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.response_times = {server: [] for server in servers}

    def get_next_server(self):
        # Select server with lowest average response time
        avg_times = {
            server: sum(times) / len(times) if times else 0
            for server, times in self.response_times.items()
        }
        return min(avg_times.items(), key=lambda x: x[1])[0]

    def record_response_time(self, server, time_ms):
        # Keep last 100 response times
        self.response_times[server].append(time_ms)
        if len(self.response_times[server]) > 100:
            self.response_times[server].pop(0)
```

**Characteristics:**
- Performance-based routing
- Adapts to server performance
- More complex to implement

**Best For:** Variable server performance, mixed workloads

#### 7. Random

**Algorithm:**
```python
import random

class RandomBalancer:
    def __init__(self, servers):
        self.servers = servers

    def get_next_server(self):
        return random.choice(self.servers)
```

**Characteristics:**
- Simplest implementation
- Good distribution over time
- No state maintenance

**Best For:** Simple scenarios, quick implementation

### Health Checks

#### Active Health Checks

```python
class HealthChecker:
    def __init__(self, servers, config):
        self.servers = servers
        self.config = config
        self.health_status = {server: True for server in servers}
        self.failure_counts = {server: 0 for server in servers}

    async def check_health(self, server):
        """Perform health check on a server"""
        try:
            start = time.time()
            response = await http_client.get(
                f"http://{server}{self.config['path']}",
                timeout=self.config['timeout']
            )
            duration = (time.time() - start) * 1000

            success = response.status == self.config['expected_status']

            if success:
                self.on_health_check_success(server)
            else:
                self.on_health_check_failure(server)

            return {
                'server': server,
                'success': success,
                'duration_ms': duration,
                'status_code': response.status
            }

        except Exception as e:
            self.on_health_check_failure(server)
            return {
                'server': server,
                'success': False,
                'error': str(e)
            }

    def on_health_check_success(self, server):
        """Mark server as healthy after threshold"""
        self.failure_counts[server] = 0
        if not self.health_status[server]:
            # Was unhealthy, check if can be marked healthy
            # (may require multiple successful checks)
            self.health_status[server] = True
            self.log_server_recovered(server)

    def on_health_check_failure(self, server):
        """Mark server as unhealthy after threshold"""
        self.failure_counts[server] += 1
        if self.failure_counts[server] >= self.config['unhealthy_threshold']:
            if self.health_status[server]:
                self.health_status[server] = False
                self.log_server_failed(server)

    async def run_health_checks(self):
        """Continuously run health checks"""
        while True:
            tasks = [self.check_health(server) for server in self.servers]
            results = await asyncio.gather(*tasks)

            # Log results
            for result in results:
                self.log_health_check(result)

            await asyncio.sleep(self.config['interval'])
```

**Health Check Types:**

1. **HTTP Health Checks:**
```
GET /health
Expected: 200 OK
Response: {"status": "healthy", "version": "1.2.3"}
```

2. **TCP Health Checks:**
```python
async def tcp_health_check(host, port, timeout=2):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False
```

3. **Deep Health Checks:**
```
GET /health/deep
Checks:
- Database connectivity
- Cache connectivity
- External API availability
- Disk space
- Memory usage
```

#### Passive Health Checks

Monitor actual traffic and mark servers unhealthy based on errors:

```python
class PassiveHealthChecker:
    def __init__(self, error_threshold=10, time_window=60):
        self.error_threshold = error_threshold
        self.time_window = time_window
        self.error_counts = {}

    def record_request(self, server, success):
        now = time.time()
        if server not in self.error_counts:
            self.error_counts[server] = []

        if not success:
            self.error_counts[server].append(now)

        # Remove old errors outside time window
        self.error_counts[server] = [
            t for t in self.error_counts[server]
            if now - t < self.time_window
        ]

    def is_healthy(self, server):
        if server not in self.error_counts:
            return True
        return len(self.error_counts[server]) < self.error_threshold
```

## 8. Trade-offs and Considerations

### Layer 4 vs Layer 7 Load Balancing

#### Layer 4 (Transport Layer)
```
Client → LB → Server
         │
         └→ Routes based on IP and Port
```

**Advantages:**
- Faster (less processing)
- Lower latency
- Higher throughput
- Protocol agnostic
- Lower resource usage

**Disadvantages:**
- No content-based routing
- No HTTP-specific features
- Limited request inspection
- Can't do SSL termination (unless in passthrough mode)

**Best For:** TCP/UDP services, high-performance needs

#### Layer 7 (Application Layer)
```
Client → LB → Server
         │
         └→ Routes based on URL, Headers, Cookies, etc.
```

**Advantages:**
- Content-based routing
- SSL/TLS termination
- HTTP header manipulation
- Caching possible
- Advanced routing logic

**Disadvantages:**
- Higher latency
- More CPU intensive
- Lower throughput
- HTTP-specific

**Best For:** Web applications, microservices, content-based routing

### Session Persistence (Sticky Sessions)

#### Cookie-Based Affinity
```python
def route_request(request):
    server_id = request.cookies.get('SERVER_ID')

    if server_id and is_server_healthy(server_id):
        return server_id
    else:
        # Assign new server
        server_id = load_balancer.get_next_server()
        response.set_cookie('SERVER_ID', server_id, max_age=3600)
        return server_id
```

#### IP-Based Affinity
```python
def route_request(request):
    client_ip = request.remote_addr
    return ip_hash_balancer.get_server(client_ip)
```

**Trade-offs:**
- **Pros:** Simple, maintains session state on server
- **Cons:** Uneven load distribution, server failure loses sessions
- **Alternative:** Store sessions in shared storage (Redis, DB)

## 9. Scalability & Bottlenecks

### Scaling Load Balancers

#### Single Load Balancer Limits
- Network bandwidth: ~10 Gbps
- Connections: ~1M concurrent
- Requests: ~100K RPS

#### Solutions

**1. DNS Round Robin:**
```
example.com → 1.2.3.4 (LB1)
            → 1.2.3.5 (LB2)
            → 1.2.3.6 (LB3)
```

**2. Anycast:**
- Multiple LBs share same IP
- Network routes to nearest LB
- Geographic distribution

**3. Load Balancer Clustering:**
```
      ┌──────────┐
      │  DNS LB  │
      └────┬─────┘
           │
    ┌──────┴──────┐
    ↓             ↓
[LB Cluster]  [LB Cluster]
[Region A]    [Region B]
```

### Common Bottlenecks

1. **Network Bandwidth:**
   - Symptom: High packet loss, latency
   - Solution: Upgrade network, add more LBs

2. **Connection Limits:**
   - Symptom: Connection refused errors
   - Solution: Tune OS limits, add LBs

3. **SSL/TLS Overhead:**
   - Symptom: High CPU usage on LB
   - Solution: SSL offloading, hardware acceleration

4. **Health Check Overhead:**
   - Symptom: Too many health check requests
   - Solution: Increase interval, use passive checks

## 10. Follow-up Questions

1. **How do you handle WebSocket connections with load balancing?**
   - Use connection-based algorithms (least connections)
   - Enable sticky sessions
   - Consider dedicated WebSocket servers
   - Use Layer 7 LB with WebSocket support

2. **What happens when a server fails mid-request?**
   - Load balancer detects timeout or connection error
   - Marks server as unhealthy
   - Retries request on different server (if idempotent)
   - Returns error to client if non-idempotent

3. **How do you perform zero-downtime deployments with load balancers?**
   - Rolling deployment: Update servers one by one
   - Blue-green: Switch traffic between environments
   - Canary: Gradually shift percentage of traffic
   - Use "draining" status to stop new connections

4. **How do you prevent cascading failures?**
   - Circuit breakers
   - Request timeouts
   - Connection limits per backend
   - Bulkhead pattern (isolate resources)
   - Graceful degradation

5. **What's the difference between load balancer and reverse proxy?**
   - Load Balancer: Primarily distributes traffic
   - Reverse Proxy: Can do LB + caching + SSL + more
   - Reverse Proxy: More application-aware
   - Often used together

6. **How do you handle geographic load balancing?**
   - GeoDNS routes to nearest region
   - Regional load balancers handle local traffic
   - Cross-region failover for availability
   - Consider data sovereignty

7. **What monitoring metrics are critical for load balancers?**
   - Request rate (per second)
   - Response times (p50, p95, p99)
   - Error rates (5xx errors)
   - Active connections
   - Backend health status
   - Resource utilization (CPU, memory, network)

8. **How do you test load balancer configurations?**
   - Load testing with realistic traffic
   - Chaos testing (kill backends)
   - Verify failover times
   - Test different algorithms
   - Monitor distribution fairness

9. **When would you use multiple load balancer tiers?**
   - Layer 4 for initial routing (geographic, protocol)
   - Layer 7 for application routing (URL, headers)
   - Separate LBs for different services
   - Database connection pooling

10. **How do you handle DDoS attacks at the load balancer level?**
    - Rate limiting per IP
    - Connection limits
    - Request validation
    - Use CDN/DDoS protection service
    - Geographic blocking if needed
    - Challenge-response (CAPTCHA)
