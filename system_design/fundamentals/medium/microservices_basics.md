# Microservices Basics: Architecture, Communication, and Trade-offs

## 1. Problem Statement

How do we structure a large application to enable independent development, deployment, and scaling of different functionalities? Monolithic applications become difficult to maintain, deploy, and scale as they grow. Microservices architecture decomposes applications into small, independent services that communicate via well-defined APIs.

## 2. Requirements

### Functional Requirements
- Independent service deployment
- Service-to-service communication
- Service discovery and registration
- API gateway for external access
- Data management per service
- Cross-service transactions
- Centralized logging and monitoring

### Non-functional Requirements
- **Scalability:** Independent scaling of services
- **Availability:** 99.9%+ per service
- **Latency:** <100ms for inter-service calls
- **Fault Isolation:** Service failure doesn't crash system
- **Development Velocity:** Teams can deploy independently
- **Observability:** End-to-end request tracing

## 3. Capacity Estimation

### Example: E-commerce Platform

**Services:**
- User Service: 1,000 requests/sec
- Product Catalog: 5,000 requests/sec
- Shopping Cart: 2,000 requests/sec
- Order Service: 500 requests/sec
- Payment Service: 400 requests/sec
- Inventory Service: 1,500 requests/sec
- Notification Service: 3,000 requests/sec

**Inter-Service Communication:**
- Average: Each request triggers 3 downstream calls
- Total internal calls: 12,000 * 3 = 36,000 requests/sec
- Network bandwidth: ~360 MB/sec (assuming 10KB per call)

**Infrastructure:**
```
Per service: 2-10 instances (based on load)
Total instances: ~50
Load balancers: 1 per service = 7
API Gateway: 3 instances (HA)
Service mesh proxies: 2 per instance = 100
```

## 4. High-Level Design

### Microservices Architecture

```
                          Internet
                             │
                             ↓
                    ┌────────────────┐
                    │  API Gateway   │
                    │  (Kong/NGINX)  │
                    └────────┬───────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
   │  User    │        │ Product  │        │  Order   │
   │ Service  │◄──────►│ Service  │◄──────►│ Service  │
   └────┬─────┘        └────┬─────┘        └────┬─────┘
        │                   │                    │
   ┌────▼─────┐        ┌───▼──────┐        ┌────▼─────┐
   │  User    │        │ Product  │        │  Order   │
   │  DB      │        │  DB      │        │  DB      │
   └──────────┘        └──────────┘        └──────────┘

        │                   │                    │
        └───────────────────┼────────────────────┘
                            │
                   ┌────────▼─────────┐
                   │  Message Queue   │
                   │  (RabbitMQ/Kafka)│
                   └──────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼──────┐      ┌────▼──────┐      ┌────▼──────┐
   │ Payment   │      │Inventory  │      │Notification│
   │ Service   │      │ Service   │      │  Service   │
   └───────────┘      └───────────┘      └────────────┘
```

### Monolith vs Microservices

```
MONOLITH:
┌────────────────────────────────┐
│      Single Application        │
│  ┌──────────────────────────┐  │
│  │     Presentation Layer   │  │
│  ├──────────────────────────┤  │
│  │     Business Logic       │  │
│  │  - User Management       │  │
│  │  - Product Catalog       │  │
│  │  - Order Processing      │  │
│  │  - Payment Processing    │  │
│  ├──────────────────────────┤  │
│  │     Data Access Layer    │  │
│  └──────────────────────────┘  │
└────────────────┬───────────────┘
                 │
         ┌───────▼────────┐
         │  Single Database│
         └─────────────────┘

MICROSERVICES:
┌─────────┐  ┌─────────┐  ┌─────────┐
│  User   │  │ Product │  │  Order  │
│ Service │  │ Service │  │ Service │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
┌────▼───┐   ┌───▼────┐   ┌───▼────┐
│User DB │   │Product │   │Order DB│
└────────┘   │  DB    │   └────────┘
             └────────┘
```

## 5. API Design

### Service APIs

```
// User Service API
GET    /api/v1/users/{userId}
POST   /api/v1/users
PUT    /api/v1/users/{userId}
DELETE /api/v1/users/{userId}

// Product Service API
GET    /api/v1/products?category={category}&page={page}
GET    /api/v1/products/{productId}
POST   /api/v1/products
PUT    /api/v1/products/{productId}

// Order Service API
POST   /api/v1/orders
GET    /api/v1/orders/{orderId}
GET    /api/v1/orders/user/{userId}
PUT    /api/v1/orders/{orderId}/status

// Service Discovery API
GET    /api/v1/services
Response: {
  "services": [
    {
      "name": "user-service",
      "instances": [
        {"id": "user-1", "host": "10.0.1.5", "port": 8080, "status": "healthy"},
        {"id": "user-2", "host": "10.0.1.6", "port": 8080, "status": "healthy"}
      ]
    }
  ]
}

POST   /api/v1/services/register
Request: {
  "service_name": "user-service",
  "instance_id": "user-1",
  "host": "10.0.1.5",
  "port": 8080,
  "health_check_url": "http://10.0.1.5:8080/health"
}
```

### Inter-Service Communication

```
// Synchronous (REST)
GET /api/v1/users/{userId}
Response: {
  "user_id": "123",
  "username": "john_doe",
  "email": "john@example.com"
}

// Asynchronous (Message Queue)
Event: "order.created"
Payload: {
  "order_id": "ORD-123",
  "user_id": "123",
  "items": [...],
  "total": 99.99,
  "timestamp": "2025-11-12T10:30:00Z"
}
```

## 6. Database Schema

### Service Registry

```sql
CREATE TABLE services (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    service_name VARCHAR(100) NOT NULL,
    version VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_service_version (service_name, version)
);

CREATE TABLE service_instances (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    service_id BIGINT,
    instance_id VARCHAR(100) UNIQUE NOT NULL,
    host VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    status ENUM('healthy', 'unhealthy', 'starting', 'stopping'),
    last_heartbeat TIMESTAMP,
    metadata JSON, -- Custom instance metadata
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(id),
    INDEX idx_service (service_id),
    INDEX idx_status (status)
);

CREATE TABLE api_gateway_routes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    path_pattern VARCHAR(255) NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    method ENUM('GET', 'POST', 'PUT', 'DELETE', 'PATCH'),
    rate_limit_per_minute INT,
    timeout_ms INT DEFAULT 30000,
    retry_attempts INT DEFAULT 3,
    circuit_breaker_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_path (path_pattern)
);
```

### Example Service Database (User Service)

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- Each service owns its data
-- NO foreign keys to other services' databases
```

## 7. Detailed Component Design

### Service Communication Patterns

#### 1. Synchronous Communication (REST/gRPC)

```python
class UserService:
    def __init__(self):
        self.http_client = HTTPClient()
        self.circuit_breaker = CircuitBreaker()
        self.service_discovery = ServiceDiscovery()

    async def get_user_with_orders(self, user_id):
        """Get user info and their orders from different services"""

        # Call user service (same service)
        user = await self.get_user(user_id)

        # Call order service
        try:
            # Discover order service instances
            order_service_url = await self.service_discovery.get_service_url('order-service')

            # Make call with circuit breaker
            orders = await self.circuit_breaker.call(
                self.http_client.get,
                f"{order_service_url}/api/v1/orders/user/{user_id}",
                timeout=2.0
            )

            return {
                'user': user,
                'orders': orders
            }

        except CircuitBreakerOpen:
            # Fallback: Return user without orders
            return {
                'user': user,
                'orders': [],
                'orders_unavailable': True
            }
        except TimeoutError:
            # Timeout fallback
            return {
                'user': user,
                'orders': [],
                'timeout': True
            }
```

**Advantages:**
- Immediate response
- Simple request-response model
- Easy to debug

**Disadvantages:**
- Tight coupling
- Cascading failures
- Lower availability

#### 2. Asynchronous Communication (Message Queues)

```python
class OrderService:
    def __init__(self):
        self.message_queue = MessageQueue()
        self.db = Database()

    async def create_order(self, order_data):
        """Create order and publish events"""

        # 1. Validate and create order
        order = await self.db.create_order(order_data)

        # 2. Publish event (fire and forget)
        await self.message_queue.publish(
            exchange='orders',
            routing_key='order.created',
            message={
                'order_id': order.id,
                'user_id': order.user_id,
                'items': order.items,
                'total': order.total,
                'timestamp': order.created_at
            }
        )

        return order

class InventoryService:
    def __init__(self):
        self.message_queue = MessageQueue()

    async def start_event_listener(self):
        """Listen for order events"""

        await self.message_queue.subscribe(
            exchange='orders',
            routing_key='order.created',
            callback=self.handle_order_created
        )

    async def handle_order_created(self, message):
        """Reserve inventory when order is created"""
        order_id = message['order_id']
        items = message['items']

        # Reserve inventory
        for item in items:
            await self.reserve_inventory(
                product_id=item['product_id'],
                quantity=item['quantity'],
                order_id=order_id
            )

        # Publish inventory reserved event
        await self.message_queue.publish(
            exchange='inventory',
            routing_key='inventory.reserved',
            message={'order_id': order_id, 'status': 'reserved'}
        )
```

**Advantages:**
- Loose coupling
- Better fault tolerance
- Asynchronous processing

**Disadvantages:**
- Complexity (eventual consistency)
- Harder to debug
- Message ordering challenges

#### 3. Service Mesh (Sidecar Pattern)

```
┌─────────────────────────────────┐
│      User Service Pod           │
│  ┌──────────┐  ┌─────────────┐  │
│  │  User    │  │   Envoy     │  │
│  │ Service  │◄─┤   Proxy     │  │
│  │ :8080    │  │  (Sidecar)  │  │
│  └──────────┘  └──────┬──────┘  │
└─────────────────────│────────────┘
                      │
              Network (mTLS)
                      │
┌─────────────────────│────────────┐
│      Order Service Pod           │
│  ┌──────────┐  ┌───▼─────────┐  │
│  │  Order   │  │   Envoy     │  │
│  │ Service  │◄─┤   Proxy     │  │
│  │ :8080    │  │  (Sidecar)  │  │
│  └──────────┘  └─────────────┘  │
└─────────────────────────────────┘
```

**Service Mesh Features:**
- Automatic mTLS encryption
- Load balancing
- Retries and circuit breaking
- Observability (metrics, tracing)
- Traffic routing and canary deployments

### API Gateway

```python
class APIGateway:
    def __init__(self):
        self.routes = {}
        self.rate_limiter = RateLimiter()
        self.auth_service = AuthService()
        self.service_discovery = ServiceDiscovery()

    async def handle_request(self, request):
        """Handle incoming request from client"""

        # 1. Authentication
        try:
            user = await self.auth_service.authenticate(request)
        except AuthenticationError:
            return Response(status=401, body={'error': 'Unauthorized'})

        # 2. Rate limiting
        if not await self.rate_limiter.allow(user.id, request.path):
            return Response(status=429, body={'error': 'Too many requests'})

        # 3. Route to appropriate service
        route = self.find_route(request.path, request.method)
        if not route:
            return Response(status=404, body={'error': 'Not found'})

        # 4. Service discovery
        service_url = await self.service_discovery.get_service_url(route.service_name)

        # 5. Transform request if needed
        transformed_request = await self.transform_request(request, route)

        # 6. Forward to service
        try:
            response = await self.forward_to_service(
                service_url,
                transformed_request,
                timeout=route.timeout_ms / 1000
            )

            # 7. Transform response
            return await self.transform_response(response, route)

        except Exception as e:
            # Error handling
            return Response(status=500, body={'error': 'Internal server error'})

    def find_route(self, path, method):
        """Find matching route for path and method"""
        for pattern, route in self.routes.items():
            if self.path_matches(pattern, path) and route.method == method:
                return route
        return None
```

### Service Discovery

```python
class ServiceDiscovery:
    """Service registry and discovery"""

    def __init__(self):
        self.registry = {}  # service_name -> [instances]
        self.health_checker = HealthChecker()

    async def register_service(self, service_name, instance_id, host, port):
        """Register service instance"""
        if service_name not in self.registry:
            self.registry[service_name] = []

        instance = {
            'instance_id': instance_id,
            'host': host,
            'port': port,
            'status': 'healthy',
            'registered_at': time.time()
        }

        self.registry[service_name].append(instance)

        # Start health checking
        asyncio.create_task(
            self.health_checker.monitor(service_name, instance)
        )

    async def deregister_service(self, service_name, instance_id):
        """Remove service instance"""
        if service_name in self.registry:
            self.registry[service_name] = [
                i for i in self.registry[service_name]
                if i['instance_id'] != instance_id
            ]

    async def get_service_url(self, service_name):
        """Get URL for a healthy instance (with load balancing)"""
        instances = self.get_healthy_instances(service_name)

        if not instances:
            raise ServiceUnavailable(f"No healthy instances for {service_name}")

        # Simple round-robin load balancing
        instance = random.choice(instances)
        return f"http://{instance['host']}:{instance['port']}"

    def get_healthy_instances(self, service_name):
        """Get all healthy instances of a service"""
        if service_name not in self.registry:
            return []

        return [
            i for i in self.registry[service_name]
            if i['status'] == 'healthy'
        ]
```

### Distributed Transactions (SAGA Pattern)

```python
class OrderSaga:
    """
    Coordinate distributed transaction across services
    using choreography-based saga
    """

    def __init__(self):
        self.message_queue = MessageQueue()

    async def create_order(self, order_data):
        """Start order creation saga"""

        # Step 1: Create order (local transaction)
        order = await self.create_order_record(order_data)

        # Publish event to start saga
        await self.message_queue.publish(
            'orders',
            'order.created',
            {'order_id': order.id, 'user_id': order.user_id, 'items': order.items}
        )

        return order

    # Other services listen and react

class InventoryService:
    async def handle_order_created(self, event):
        """Step 2: Reserve inventory"""
        try:
            await self.reserve_inventory(event['order_id'], event['items'])

            # Success - publish next event
            await self.message_queue.publish(
                'inventory',
                'inventory.reserved',
                {'order_id': event['order_id']}
            )

        except InsufficientInventory:
            # Failure - publish compensating event
            await self.message_queue.publish(
                'inventory',
                'inventory.reservation.failed',
                {'order_id': event['order_id'], 'reason': 'insufficient_inventory'}
            )

class PaymentService:
    async def handle_inventory_reserved(self, event):
        """Step 3: Process payment"""
        try:
            await self.charge_payment(event['order_id'])

            await self.message_queue.publish(
                'payments',
                'payment.completed',
                {'order_id': event['order_id']}
            )

        except PaymentFailed:
            # Compensate: Release inventory
            await self.message_queue.publish(
                'payments',
                'payment.failed',
                {'order_id': event['order_id']}
            )

class OrderService:
    async def handle_payment_completed(self, event):
        """Final step: Mark order as confirmed"""
        await self.update_order_status(event['order_id'], 'confirmed')

    async def handle_payment_failed(self, event):
        """Compensating transaction: Cancel order"""
        await self.update_order_status(event['order_id'], 'cancelled')
```

## 8. Trade-offs and Considerations

### Monolith vs Microservices

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| **Development** | Simple, single codebase | Complex, multiple repos |
| **Deployment** | All-or-nothing | Independent deployment |
| **Scaling** | Scale entire app | Scale individual services |
| **Testing** | Simpler integration tests | Complex distributed testing |
| **Data Management** | Single database | Database per service |
| **Performance** | In-process calls (fast) | Network calls (slower) |
| **Consistency** | ACID transactions | Eventual consistency |
| **Operations** | Simpler monitoring | Requires distributed tracing |
| **Team Structure** | Shared codebase | Independent teams |
| **Initial Development** | Faster | Slower |

### When to Use Microservices

**Use Microservices When:**
- Large team (>50 developers)
- Different parts scale differently
- Need independent deployment cycles
- Different technologies for different features
- Clear service boundaries exist

**Use Monolith When:**
- Small team (<10 developers)
- Unclear domain boundaries
- Early stage / MVP
- Simple application
- Operational simplicity important

### Data Management Challenges

**Problem:** Each service owns its data
```
Cannot do:
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.id = 123

Must do:
1. user = UserService.getUser(123)
2. orders = OrderService.getOrdersByUser(123)
3. Combine in application layer
```

**Solutions:**
1. **API Composition:** Aggregate data from multiple services
2. **CQRS:** Separate read and write models, materialized views
3. **Event Sourcing:** Rebuild state from events
4. **Data Duplication:** Denormalize where needed

## 9. Scalability & Bottlenecks

### Service Scaling

```python
# Horizontal scaling - add more instances
def scale_service(service_name, desired_instances):
    current = get_instance_count(service_name)

    if desired_instances > current:
        # Scale up
        for i in range(desired_instances - current):
            deploy_instance(service_name)

    elif desired_instances < current:
        # Scale down
        for i in range(current - desired_instances):
            remove_instance(service_name)
```

### Bottlenecks

1. **Chatty Services:**
   - Problem: Too many inter-service calls
   - Solution: API composition, batch APIs, caching

2. **Single Point of Failure:**
   - Problem: All requests through API gateway
   - Solution: Multiple gateway instances, service mesh

3. **Database per Service:**
   - Problem: No JOINs across services
   - Solution: CQRS, data duplication, eventual consistency

4. **Network Latency:**
   - Problem: Network calls slower than in-process
   - Solution: Async communication, caching, service locality

## 10. Follow-up Questions

1. **How do you handle authentication across microservices?**
   - API Gateway handles auth, passes JWT to services
   - Services verify JWT signature
   - Service-to-service: mTLS or service tokens

2. **How do you debug issues in microservices?**
   - Distributed tracing (Jaeger, Zipkin)
   - Correlation IDs across requests
   - Centralized logging (ELK stack)
   - Service dependency maps

3. **How do you handle versioning of microservices?**
   - URL versioning: `/api/v1/users`, `/api/v2/users`
   - Header versioning: `Accept: application/vnd.api.v2+json`
   - Simultaneous versions running
   - Backward compatibility

4. **What is the role of containers in microservices?**
   - Package service with dependencies
   - Consistent environment (dev/prod)
   - Easy deployment and scaling
   - Resource isolation

5. **How do you test microservices?**
   - Unit tests per service
   - Contract testing (Pact)
   - Integration tests with test doubles
   - End-to-end tests (minimal)
   - Chaos testing

6. **How do you handle circuit breakers?**
   - Track failure rate
   - Open circuit after threshold
   - Fail fast without calling service
   - Periodically try again (half-open)
   - Close when service recovers

7. **What is service mesh and when to use it?**
   - Infrastructure layer for service communication
   - Handles routing, security, observability
   - Use when: Many services, complex networking needs
   - Examples: Istio, Linkerd

8. **How do you handle shared code in microservices?**
   - Shared libraries (careful: can create coupling)
   - Code duplication (acceptable for small utils)
   - Sidecar pattern
   - Avoid sharing business logic

9. **How do you migrate from monolith to microservices?**
   - Strangler fig pattern
   - Extract one service at a time
   - Start with clear boundaries
   - Use API gateway for routing
   - Gradual migration, not big bang

10. **What are the operational challenges of microservices?**
    - Monitoring complexity
    - Deployment coordination
    - Debugging distributed issues
    - Increased infrastructure costs
    - Team coordination overhead
