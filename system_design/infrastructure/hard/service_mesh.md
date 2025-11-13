# Service Mesh Architecture

## 1. Problem Statement

Design a service mesh infrastructure layer (similar to Istio, Linkerd, or Consul Connect) that provides service-to-service communication, observability, security, and traffic management for microservices without requiring application code changes. The system should handle thousands of services with millions of requests per second while maintaining low latency overhead.

## 2. Requirements

### Functional Requirements
- **Service discovery**: Automatic discovery of service instances
- **Load balancing**: Intelligent request distribution
- **Traffic routing**: Advanced routing (canary, A/B testing, blue-green)
- **Circuit breaking**: Fault isolation and cascading failure prevention
- **Retries & timeouts**: Automatic retry with backoff
- **Mutual TLS (mTLS)**: Encrypted service-to-service communication
- **Access control**: Fine-grained authorization policies
- **Observability**: Metrics, logs, and distributed tracing
- **Rate limiting**: Per-service rate limits
- **Fault injection**: Chaos engineering support

### Non-Functional Requirements
- **Latency overhead**: <2ms P99 latency addition
- **Throughput**: Handle 10 million req/sec across mesh
- **Scalability**: Support 10,000+ services
- **Availability**: 99.99% uptime
- **Resource overhead**: <50MB memory per sidecar
- **Configuration**: Dynamic configuration without restart
- **Multi-tenancy**: Isolate different environments/teams

### Out of Scope
- Service implementation logic
- Database management
- CI/CD pipeline
- Container orchestration (assumes Kubernetes)

## 3. Capacity Estimation

### Scale Assumptions
- Number of services: 10,000
- Service instances: 100,000 (avg 10 instances per service)
- Requests per second: 10 million
- Average request size: 10 KB
- Average response size: 50 KB
- mTLS enabled: Yes
- Tracing sample rate: 1%

### Resource Estimation per Sidecar
```
Memory:
- Connection pool: 10 MB
- Configuration cache: 5 MB
- Metrics buffer: 5 MB
- TLS certificates: 1 MB
- Runtime overhead: 20 MB
Total: ~40 MB per sidecar

CPU:
- Idle: 0.1 cores
- Under load (100 req/sec): 0.3 cores
- With mTLS: 0.5 cores

Total CPU: 100K sidecars × 0.5 cores = 50K cores
Total Memory: 100K sidecars × 40 MB = 4 TB
```

### Control Plane Resources
```
Configuration storage:
- 10K services × 10 KB config = 100 MB
- Certificates: 100K instances × 1 KB = 100 MB
- Total: ~200 MB

Control plane instances: 10 (for HA)
Memory per instance: 4 GB
Total: 40 GB
```

## 4. High-Level Design

```
┌─────────────────────────────────────────────────────┐
│              Service Mesh Architecture              │
└─────────────────────────────────────────────────────┘

Data Plane (Sidecar Proxies):

┌────────────────────────────────────────────────────┐
│  Service A Pod                                     │
│  ┌──────────────┐         ┌──────────────────────┐│
│  │  Container   │  :8080  │  Envoy Sidecar      ││
│  │  (Service A) │◄────────┤  - Intercepts       ││
│  │              │         │  - Routes           ││
│  └──────────────┘         │  - Observes         ││
│                           │  - Secures          ││
│                           └─────┬────────────────┘│
└─────────────────────────────────┼──────────────────┘
                                  │ mTLS
                                  │
                                  ▼
┌─────────────────────────────────┼──────────────────┐
│  Service B Pod                  │                  │
│  ┌──────────────────────┐       │                  │
│  │  Envoy Sidecar       │◄──────┘                  │
│  │                      │  :15001                  │
│  └─────┬────────────────┘                          │
│        │ :8080                                     │
│  ┌─────▼──────────┐                                │
│  │  Container     │                                │
│  │  (Service B)   │                                │
│  └────────────────┘                                │
└────────────────────────────────────────────────────┘

Control Plane:

┌────────────────────────────────────────────────────┐
│             Control Plane Services                 │
│                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐│
│  │   Pilot      │  │   Citadel    │  │  Galley  ││
│  │              │  │              │  │          ││
│  │ - Service    │  │ - Cert       │  │ - Config ││
│  │   Discovery  │  │   Management │  │   Valid. ││
│  │ - Config     │  │ - Key        │  │ - Policy ││
│  │   Distribution│  │   Rotation   │  │   Mgmt   ││
│  └──────┬───────┘  └──────┬───────┘  └────┬─────┘│
│         │                 │                │      │
│         └─────────────────┼────────────────┘      │
│                           │                       │
│                           ▼                       │
│  ┌────────────────────────────────────────────┐  │
│  │    Configuration Store (etcd/Kubernetes)   │  │
│  └────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│             Observability Stack                    │
│  ┌──────────┐  ┌───────────┐  ┌───────────────┐  │
│  │Prometheus│  │   Jaeger  │  │  Grafana      │  │
│  │(Metrics) │  │ (Tracing) │  │ (Dashboards)  │  │
│  └──────────┘  └───────────┘  └───────────────┘  │
└────────────────────────────────────────────────────┘
```

### Core Components

**Data Plane:**
1. **Sidecar Proxy** (Envoy): Intercepts all traffic
2. **Traffic Management**: Routing, load balancing
3. **Security**: mTLS, authentication, authorization
4. **Observability**: Metrics, logs, traces

**Control Plane:**
1. **Pilot**: Service discovery and configuration
2. **Citadel**: Certificate and key management
3. **Galley**: Configuration validation and distribution
4. **Mixer** (optional): Policy enforcement and telemetry

## 5. API Design

### Traffic Management API

```yaml
# Virtual Service (routing rules)
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10  # Canary 10%
```

### Destination Rules API

```yaml
# Destination Rule (load balancing, circuit breaking)
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: reviews-destination
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN  # or ROUND_ROBIN, RANDOM
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 2
    outlierDetection:  # Circuit breaker
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Security Policy API

```yaml
# Authorization Policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: reviews-policy
spec:
  selector:
    matchLabels:
      app: reviews
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/productpage"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/reviews/*"]
```

### Observability API

```python
class ServiceMeshObservability:
    def get_service_metrics(
        self,
        service: str,
        metrics: List[str],  # request_count, latency_p99, error_rate
        start_time: int,
        end_time: int
    ) -> MetricsResponse:
        """Query service metrics"""
        pass

    def get_service_topology(self) -> ServiceGraph:
        """Get service dependency graph"""
        pass

    def get_trace(self, trace_id: str) -> DistributedTrace:
        """Get distributed trace by ID"""
        pass
```

## 6. Component Design

### Sidecar Proxy (Envoy)

```python
class SidecarProxy:
    """
    Sidecar proxy that intercepts all inbound/outbound traffic
    Based on Envoy proxy
    """

    def __init__(self, service_name: str, config: ProxyConfig):
        self.service_name = service_name
        self.config = config

        # Connection pools
        self.upstream_connections = ConnectionPool()
        self.downstream_connections = ConnectionPool()

        # Traffic management
        self.load_balancer = LoadBalancer()
        self.circuit_breaker = CircuitBreaker()
        self.retry_policy = RetryPolicy()

        # Security
        self.tls_context = TLSContext()
        self.auth_manager = AuthorizationManager()

        # Observability
        self.metrics_collector = MetricsCollector()
        self.trace_exporter = TraceExporter()

    async def handle_request(self, request: Request) -> Response:
        """Main request handling pipeline"""
        span = self.start_trace(request)

        try:
            # 1. Inbound processing
            await self.process_inbound(request)

            # 2. Authorization
            if not await self.authorize_request(request):
                return Response(status=403, body="Forbidden")

            # 3. Rate limiting
            if not await self.check_rate_limit(request):
                return Response(status=429, body="Too Many Requests")

            # 4. Route selection
            upstream_cluster = await self.select_upstream(request)

            # 5. Circuit breaker check
            if self.circuit_breaker.is_open(upstream_cluster):
                return Response(status=503, body="Service Unavailable")

            # 6. Load balancing
            upstream_host = self.load_balancer.choose(upstream_cluster)

            # 7. Retry logic
            response = await self.send_with_retry(upstream_host, request)

            # 8. Outbound processing
            await self.process_outbound(response)

            # 9. Record metrics
            self.record_metrics(request, response)

            return response

        except Exception as e:
            self.record_error(e)
            span.set_error(e)
            raise

        finally:
            span.finish()

    async def send_with_retry(
        self,
        upstream_host: str,
        request: Request
    ) -> Response:
        """Send request with automatic retry"""
        max_retries = self.retry_policy.max_retries
        backoff = self.retry_policy.initial_backoff

        for attempt in range(max_retries + 1):
            try:
                # Establish connection (with mTLS)
                conn = await self.get_connection(upstream_host)

                # Send request
                response = await conn.send(request)

                # Check if retryable
                if not self.is_retryable(response):
                    return response

                # Record retry
                self.circuit_breaker.record_failure(upstream_host)

            except Exception as e:
                if attempt == max_retries:
                    raise

                # Exponential backoff
                await asyncio.sleep(backoff)
                backoff *= 2

        raise MaxRetriesExceededError()

    async def get_connection(self, host: str) -> Connection:
        """Get connection with mTLS"""
        # Check if connection exists
        conn = self.upstream_connections.get(host)

        if conn and conn.is_alive():
            return conn

        # Create new connection with mTLS
        ssl_context = self.tls_context.create_client_context(
            cert_file=self.config.client_cert,
            key_file=self.config.client_key,
            ca_file=self.config.ca_cert
        )

        conn = await asyncio.open_connection(
            host=host,
            port=self.config.upstream_port,
            ssl=ssl_context
        )

        self.upstream_connections.add(host, conn)
        return conn
```

### Load Balancing

```python
class LoadBalancer:
    """Load balancing strategies"""

    def __init__(self, strategy: str = 'round_robin'):
        self.strategy = strategy
        self.endpoints = {}  # cluster -> list of endpoints
        self.current_index = {}  # For round robin
        self.connections = {}  # For least connections

    def choose(self, cluster: str) -> str:
        """Choose endpoint for cluster"""
        endpoints = self.endpoints.get(cluster, [])

        if not endpoints:
            raise NoHealthyEndpointsError(cluster)

        if self.strategy == 'round_robin':
            return self.round_robin(cluster, endpoints)
        elif self.strategy == 'least_conn':
            return self.least_connections(cluster, endpoints)
        elif self.strategy == 'random':
            return random.choice(endpoints)
        elif self.strategy == 'weighted':
            return self.weighted_round_robin(cluster, endpoints)

    def round_robin(self, cluster: str, endpoints: List[str]) -> str:
        """Round robin load balancing"""
        if cluster not in self.current_index:
            self.current_index[cluster] = 0

        index = self.current_index[cluster]
        endpoint = endpoints[index % len(endpoints)]

        self.current_index[cluster] = (index + 1) % len(endpoints)
        return endpoint

    def least_connections(self, cluster: str, endpoints: List[str]) -> str:
        """Least connections load balancing"""
        # Get connection counts
        counts = [
            (endpoint, self.connections.get(endpoint, 0))
            for endpoint in endpoints
        ]

        # Sort by connection count
        counts.sort(key=lambda x: x[1])

        return counts[0][0]

    def weighted_round_robin(
        self,
        cluster: str,
        endpoints: List[Tuple[str, int]]  # (endpoint, weight)
    ) -> str:
        """Weighted round robin based on endpoint weights"""
        # Build weighted list
        weighted_endpoints = []
        for endpoint, weight in endpoints:
            weighted_endpoints.extend([endpoint] * weight)

        return self.round_robin(cluster, weighted_endpoints)
```

### Circuit Breaker

```python
class CircuitBreaker:
    """Circuit breaker pattern for fault isolation"""

    def __init__(self):
        self.states = {}  # host -> CircuitState
        self.error_threshold = 5  # Consecutive errors to open
        self.timeout = 30  # Seconds before trying half-open
        self.success_threshold = 2  # Successes to close

    def is_open(self, host: str) -> bool:
        """Check if circuit is open"""
        state = self.get_state(host)

        if state.status == 'open':
            # Check if timeout elapsed
            if time.time() - state.opened_at > self.timeout:
                # Transition to half-open
                state.status = 'half-open'
                return False
            return True

        return False

    def record_success(self, host: str):
        """Record successful request"""
        state = self.get_state(host)

        if state.status == 'half-open':
            state.success_count += 1

            if state.success_count >= self.success_threshold:
                # Close circuit
                state.status = 'closed'
                state.error_count = 0
                state.success_count = 0
        elif state.status == 'closed':
            # Reset error count on success
            state.error_count = 0

    def record_failure(self, host: str):
        """Record failed request"""
        state = self.get_state(host)

        if state.status == 'closed':
            state.error_count += 1

            if state.error_count >= self.error_threshold:
                # Open circuit
                state.status = 'open'
                state.opened_at = time.time()
                logger.warning(f"Circuit breaker opened for {host}")

        elif state.status == 'half-open':
            # Single failure in half-open returns to open
            state.status = 'open'
            state.opened_at = time.time()

    def get_state(self, host: str) -> CircuitState:
        """Get circuit state for host"""
        if host not in self.states:
            self.states[host] = CircuitState()
        return self.states[host]

class CircuitState:
    def __init__(self):
        self.status = 'closed'  # closed, open, half-open
        self.error_count = 0
        self.success_count = 0
        self.opened_at = 0
```

### Service Discovery

```python
class ServiceDiscovery:
    """
    Service discovery integrated with Kubernetes
    Watches Kubernetes endpoints and updates proxy configuration
    """

    def __init__(self, k8s_client):
        self.k8s_client = k8s_client
        self.service_endpoints = {}  # service -> list of endpoints
        self.watchers = []

    async def start(self):
        """Start watching Kubernetes endpoints"""
        async for event in self.k8s_client.watch_endpoints():
            await self.handle_endpoint_event(event)

    async def handle_endpoint_event(self, event):
        """Handle endpoint change event"""
        service = event.service
        action = event.action  # ADDED, MODIFIED, DELETED

        if action == 'ADDED' or action == 'MODIFIED':
            # Update endpoints
            endpoints = self.extract_endpoints(event.object)
            self.service_endpoints[service] = endpoints

            # Notify proxies
            await self.notify_proxy_update(service, endpoints)

        elif action == 'DELETED':
            # Remove service
            self.service_endpoints.pop(service, None)
            await self.notify_proxy_update(service, [])

    def extract_endpoints(self, endpoint_object) -> List[str]:
        """Extract endpoint addresses from Kubernetes object"""
        endpoints = []

        for subset in endpoint_object.subsets:
            for address in subset.addresses:
                ip = address.ip
                for port in subset.ports:
                    endpoints.append(f"{ip}:{port.port}")

        return endpoints

    async def notify_proxy_update(self, service: str, endpoints: List[str]):
        """Notify all proxies of endpoint changes"""
        update = {
            'service': service,
            'endpoints': endpoints,
            'timestamp': time.time()
        }

        # Publish to all sidecars via control plane
        await self.control_plane.push_config_update(update)
```

### Certificate Management (mTLS)

```python
class CertificateAuthority:
    """
    Certificate Authority for issuing service certificates
    Enables mutual TLS between services
    """

    def __init__(self):
        self.root_ca_cert = self.load_root_cert()
        self.root_ca_key = self.load_root_key()
        self.issued_certs = {}  # service -> certificate
        self.cert_ttl = 86400  # 24 hours

    async def issue_certificate(self, service_name: str) -> Certificate:
        """Issue certificate for service"""
        # Generate key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Create certificate signing request
        csr = x509.CertificateSigningRequestBuilder().subject_name(
            x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, service_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ServiceMesh"),
            ])
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(service_name),
                x509.DNSName(f"{service_name}.default.svc.cluster.local"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())

        # Sign certificate
        certificate = x509.CertificateBuilder().subject_name(
            csr.subject
        ).issuer_name(
            self.root_ca_cert.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(seconds=self.cert_ttl)
        ).add_extension(
            csr.extensions[0].value,
            critical=False,
        ).sign(self.root_ca_key, hashes.SHA256())

        # Store and return
        cert_data = Certificate(
            cert=certificate,
            key=private_key,
            expiry=time.time() + self.cert_ttl
        )

        self.issued_certs[service_name] = cert_data

        return cert_data

    async def rotate_certificates(self):
        """Background task to rotate expiring certificates"""
        while True:
            current_time = time.time()

            for service, cert in list(self.issued_certs.items()):
                # Rotate if expiring in next hour
                if cert.expiry - current_time < 3600:
                    new_cert = await self.issue_certificate(service)

                    # Notify service of new certificate
                    await self.notify_cert_update(service, new_cert)

            await asyncio.sleep(300)  # Check every 5 minutes
```

### Distributed Tracing

```python
class DistributedTracer:
    """Distributed tracing integration (OpenTelemetry)"""

    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
        self.exporter = JaegerExporter()

    def start_span(
        self,
        operation_name: str,
        parent_context: Optional[SpanContext] = None
    ) -> Span:
        """Start new span"""
        if parent_context:
            ctx = trace.set_span_in_context(parent_context)
            span = self.tracer.start_span(operation_name, context=ctx)
        else:
            span = self.tracer.start_span(operation_name)

        return span

    def inject_context(self, span: Span, headers: Dict[str, str]):
        """Inject trace context into request headers"""
        context = trace.set_span_in_context(span)
        propagator = TraceContextTextMapPropagator()
        propagator.inject(headers, context=context)

    def extract_context(self, headers: Dict[str, str]) -> Optional[SpanContext]:
        """Extract trace context from request headers"""
        propagator = TraceContextTextMapPropagator()
        context = propagator.extract(headers)
        return trace.get_current_span(context).get_span_context()

    def record_span_event(
        self,
        span: Span,
        name: str,
        attributes: Dict[str, Any]
    ):
        """Record event in span"""
        span.add_event(name, attributes=attributes)

    def set_span_attributes(self, span: Span, attributes: Dict[str, Any]):
        """Set span attributes"""
        for key, value in attributes.items():
            span.set_attribute(key, value)
```

## 7. Data Structures & Storage

### Configuration Storage

```yaml
# Stored in etcd or Kubernetes ConfigMaps
service_config:
  name: reviews
  endpoints:
    - ip: 10.0.1.5
      port: 8080
    - ip: 10.0.1.6
      port: 8080
  traffic_policy:
    load_balancer: ROUND_ROBIN
    connection_pool:
      max_connections: 100
    circuit_breaker:
      consecutive_errors: 5
      interval: 30s
  security_policy:
    mtls: STRICT
    allowed_principals:
      - "cluster.local/ns/default/sa/productpage"
```

## 8. Fault Tolerance & High Availability

### Control Plane HA

- Run multiple control plane instances
- Leader election for coordination
- State stored in distributed etcd cluster
- Sidecars cache configuration locally

### Data Plane Resilience

- Circuit breakers prevent cascading failures
- Retries with exponential backoff
- Timeout protection
- Load balancing avoids unhealthy instances

## 9. Monitoring & Observability

```python
# Key metrics
request_count = Counter('requests_total', labels=['service', 'method', 'code'])
request_duration = Histogram('request_duration_seconds', labels=['service'])
active_connections = Gauge('active_connections', labels=['service'])
circuit_breaker_state = Gauge('circuit_breaker_state', labels=['service', 'upstream'])
```

## 10. Scalability

- Sidecars scale with service instances
- Control plane horizontally scalable
- Configuration changes pushed incrementally
- Local caching reduces control plane load

## 11. Trade-offs

### Sidecar vs Library
- **Sidecar (chosen)**: Language-agnostic, extra latency/resources
- **Library**: Lower overhead, language-specific

### Centralized vs Decentralized
- **Hybrid**: Centralized control, decentralized data plane

### Performance vs Features
- Each feature adds latency
- mTLS: +1-2ms
- Tracing: +0.5ms
- Total overhead: <5ms

## 12. Follow-up Questions

1. How would you implement service mesh across multiple clusters?
2. How would you handle service mesh in VM environments?
3. How would you implement progressive delivery (canary rollouts)?
4. How would you debug issues in the service mesh?
5. How would you implement rate limiting in the mesh?
6. How would you handle traffic mirroring/shadowing?
7. How would you implement egress gateway for external services?
8. How would you optimize for very high throughput services?
9. How would you implement service-to-service authentication without mTLS?
10. How would you handle service mesh upgrade with zero downtime?
