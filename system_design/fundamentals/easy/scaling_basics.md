# Scaling Basics: Vertical vs Horizontal Scaling

## 1. Problem Statement

How do we handle increasing load on our system? As traffic grows, our application needs to handle more requests, process more data, and serve more users. Understanding when and how to scale is fundamental to building robust systems.

## 2. Requirements

### Functional Requirements
- System must handle increasing traffic load
- Maintain consistent performance as demand grows
- Support scaling up or scaling out based on needs
- Enable cost-effective growth

### Non-functional Requirements
- High availability during scaling operations
- Minimal downtime when scaling
- Cost efficiency
- Easy to maintain and monitor
- Flexible enough to handle unpredictable traffic patterns

## 3. Capacity Estimation

### Example Scenario: Web Application
- Current: 1,000 requests/second (RPS)
- Growth: 50% per quarter
- Target: Support 10,000 RPS within 1 year

**Resource Requirements:**
- CPU: ~4 cores per 1,000 RPS
- Memory: ~8GB per 1,000 RPS
- Network: ~100 Mbps per 1,000 RPS
- Storage: Depends on data persistence needs

## 4. High-Level Design

### Vertical Scaling (Scale Up)
```
┌─────────────────┐         ┌──────────────────────┐
│   Server v1     │         │    Server v2         │
│   4 CPU cores   │  ──────>│    16 CPU cores      │
│   8 GB RAM      │         │    32 GB RAM         │
│   100 GB SSD    │         │    500 GB SSD        │
└─────────────────┘         └──────────────────────┘
```

### Horizontal Scaling (Scale Out)
```
┌─────────────┐         ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Server 1   │         │  Server 1   │  │  Server 2   │  │  Server 3   │
│  4 cores    │  ────>  │  4 cores    │  │  4 cores    │  │  4 cores    │
│  8 GB RAM   │         │  8 GB RAM   │  │  8 GB RAM   │  │  8 GB RAM   │
└─────────────┘         └─────────────┘  └─────────────┘  └─────────────┘
                                 │              │               │
                                 └──────────────┴───────────────┘
                                          Load Balancer
```

## 5. API Design

### Monitoring APIs
```
GET /api/v1/metrics/cpu
Response: {
  "usage_percent": 75,
  "cores": 4,
  "threshold": 80
}

GET /api/v1/metrics/memory
Response: {
  "used_gb": 6.5,
  "total_gb": 8,
  "usage_percent": 81.25
}

GET /api/v1/health
Response: {
  "status": "healthy",
  "instances": 3,
  "load_per_instance": "balanced"
}
```

### Auto-scaling Configuration
```
POST /api/v1/autoscaling/configure
Request: {
  "min_instances": 2,
  "max_instances": 10,
  "cpu_threshold": 70,
  "scale_up_cooldown": 300,
  "scale_down_cooldown": 600
}
```

## 6. Database Schema

### Scaling Metrics Table
```sql
CREATE TABLE scaling_events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type ENUM('scale_up', 'scale_down', 'scale_out', 'scale_in'),
    resource_type VARCHAR(50), -- 'cpu', 'memory', 'instance'
    old_value INT,
    new_value INT,
    trigger_reason TEXT,
    status ENUM('initiated', 'in_progress', 'completed', 'failed'),
    INDEX idx_timestamp (timestamp),
    INDEX idx_event_type (event_type)
);

CREATE TABLE instance_metrics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    instance_id VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    request_count INT,
    response_time_ms INT,
    INDEX idx_instance_timestamp (instance_id, timestamp)
);
```

## 7. Detailed Component Design

### Vertical Scaling

#### Advantages
1. **Simplicity**: Single machine to manage
2. **No Application Changes**: Code doesn't need to be distributed
3. **Data Consistency**: No distributed data issues
4. **Lower Latency**: Inter-process communication is faster

#### Disadvantages
1. **Hardware Limits**: Physical/cloud instance size limits
2. **Single Point of Failure**: One machine down = entire service down
3. **Expensive**: High-end hardware costs more per unit of capacity
4. **Downtime Required**: Usually requires reboot
5. **Limited Scalability**: Eventually hit ceiling

#### When to Use
- Early-stage applications with predictable growth
- Databases that benefit from single-machine performance
- Applications not designed for distribution
- When operational simplicity is priority

### Horizontal Scaling

#### Advantages
1. **No Upper Limit**: Add machines indefinitely
2. **High Availability**: Multiple instances provide redundancy
3. **Cost Effective**: Use commodity hardware
4. **Fault Tolerance**: Instance failure doesn't crash system
5. **Geographic Distribution**: Deploy across regions

#### Disadvantages
1. **Complexity**: Need load balancers, service discovery
2. **Data Consistency**: Distributed systems challenges
3. **Application Changes**: Code must be stateless
4. **Network Overhead**: Inter-service communication costs
5. **Operational Overhead**: More machines to monitor

#### When to Use
- Web applications with variable traffic
- Microservices architecture
- Global applications needing geographic distribution
- Systems requiring high availability

## 8. Trade-offs and Considerations

### Cost Analysis

**Vertical Scaling Cost Model:**
```
Single Large Server:
- 32 cores, 128GB RAM: $500/month
- Utilization: 60% average
- Effective cost per core: $15.625/month
```

**Horizontal Scaling Cost Model:**
```
Multiple Small Servers:
- 4 cores, 16GB RAM: $80/month each
- 8 instances: $640/month
- Utilization: 80% average
- Effective cost per core: $10/month
- But: +$50/month for load balancer
- Total: $690/month
```

### Performance Considerations

**Vertical Scaling:**
- Read latency: ~1ms (local memory)
- Write latency: ~10ms (local disk)
- Network: Not a factor for single machine

**Horizontal Scaling:**
- Read latency: ~5-10ms (network + cache)
- Write latency: ~50ms (distributed consensus)
- Network bandwidth becomes critical

### Hybrid Approach

Most systems use both:
1. **Vertical scaling** for databases (to a point)
2. **Horizontal scaling** for application servers
3. **Vertical scaling** as first step, horizontal when limits reached

```
                    Load Balancer
                          |
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   App Server 1      App Server 2      App Server 3
   (Medium Size)     (Medium Size)     (Medium Size)
        │                 │                 │
        └─────────────────┼─────────────────┘
                          |
                  Database Server
                  (Large Size - Vertical)
```

## 9. Scalability & Bottlenecks

### Common Bottlenecks

#### CPU Bound
- **Symptoms**: High CPU usage, slow processing
- **Vertical Solution**: More powerful CPU
- **Horizontal Solution**: Distribute compute tasks

#### Memory Bound
- **Symptoms**: High memory usage, swapping
- **Vertical Solution**: Add more RAM
- **Horizontal Solution**: Partition data across instances

#### I/O Bound
- **Symptoms**: Disk wait times, slow queries
- **Vertical Solution**: Faster storage (SSD, NVMe)
- **Horizontal Solution**: Distributed storage, caching

#### Network Bound
- **Symptoms**: High network latency, packet loss
- **Vertical Solution**: Better network interface
- **Horizontal Solution**: CDN, regional deployment

### Scaling Strategy Decision Tree

```
High Load?
    │
    ├─ YES ─> Is this temporary spike?
    │           │
    │           ├─ YES ─> Vertical scaling (quick, reversible)
    │           │
    │           └─ NO ──> Expected to continue growing?
    │                       │
    │                       ├─ YES ─> Horizontal scaling
    │                       │
    │                       └─ NO ──> Optimize first, then decide
    │
    └─ NO ──> Monitor and optimize
```

### Auto-scaling Implementation

```python
class AutoScaler:
    def __init__(self, min_instances=2, max_instances=10):
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.current_instances = min_instances

    def should_scale_out(self, metrics):
        """Decide if we need more instances"""
        avg_cpu = sum(m['cpu'] for m in metrics) / len(metrics)
        avg_memory = sum(m['memory'] for m in metrics) / len(metrics)

        # Scale out if average resource usage > 70%
        if avg_cpu > 70 or avg_memory > 70:
            return True

        # Scale out if any instance > 90%
        if any(m['cpu'] > 90 or m['memory'] > 90 for m in metrics):
            return True

        return False

    def should_scale_in(self, metrics):
        """Decide if we can remove instances"""
        avg_cpu = sum(m['cpu'] for m in metrics) / len(metrics)
        avg_memory = sum(m['memory'] for m in metrics) / len(metrics)

        # Scale in if average usage < 30% for sustained period
        if avg_cpu < 30 and avg_memory < 30:
            # But keep minimum instances
            return self.current_instances > self.min_instances

        return False
```

## 10. Follow-up Questions

1. **How do you handle session state in horizontal scaling?**
   - Use sticky sessions (session affinity)
   - Store sessions in distributed cache (Redis)
   - Use stateless authentication (JWT tokens)

2. **What metrics trigger auto-scaling decisions?**
   - CPU utilization
   - Memory usage
   - Request queue length
   - Response time
   - Custom application metrics

3. **How do you prevent scaling thrashing?**
   - Cooldown periods between scaling events
   - Use predictive scaling based on patterns
   - Set hysteresis thresholds (different up/down triggers)

4. **How does database scaling differ from application scaling?**
   - Databases are often stateful (harder to scale horizontally)
   - Read replicas for read-heavy workloads
   - Sharding for write-heavy workloads
   - Vertical scaling often preferred initially

5. **What are the networking considerations for horizontal scaling?**
   - Load balancer capacity
   - Inter-service communication bandwidth
   - Geographic distribution and latency
   - Service mesh for complex microservices

6. **How do you handle rolling updates in horizontally scaled systems?**
   - Blue-green deployment
   - Canary releases
   - Rolling updates with health checks
   - Gradual traffic shifting

7. **What role does caching play in scaling strategy?**
   - Reduces database load (enables vertical scaling of DB)
   - Reduces response time (better user experience)
   - Can delay need for horizontal scaling
   - Different cache layers (CDN, application, database)

8. **How do you estimate costs for different scaling strategies?**
   - Calculate resource requirements at peak
   - Factor in redundancy needs
   - Include operational costs (monitoring, management)
   - Consider reserved vs. on-demand pricing

9. **What are the security implications of horizontal scaling?**
   - More instances = larger attack surface
   - Need consistent security across instances
   - Network security between instances
   - Secrets management in distributed environment

10. **How do you test scaling strategies?**
    - Load testing to find bottlenecks
    - Chaos engineering to test fault tolerance
    - Performance benchmarking
    - Cost modeling and projection
