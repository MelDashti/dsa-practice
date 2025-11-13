# Event-Driven Architecture: Event Sourcing and CQRS Patterns

## 1. Problem Statement

How do we build systems that react to changes in real-time, maintain complete audit history, and scale independently for reads and writes? Event-Driven Architecture (EDA) treats state changes as immutable events, enabling loose coupling, scalability, and powerful patterns like Event Sourcing and CQRS (Command Query Responsibility Segregation).

## 2. Requirements

### Functional Requirements
- Capture all state changes as immutable events
- Support event replay and time-travel queries
- Enable asynchronous processing and reactions
- Provide audit trail of all changes
- Support eventual consistency between services
- Enable independent scaling of reads and writes

### Non-functional Requirements
- **Throughput:** 100K+ events/second
- **Latency:** <10ms for event publication
- **Event Ordering:** Guaranteed per aggregate
- **Event Durability:** Zero data loss
- **Recovery Time:** Replay events in <1 hour
- **Storage:** Handle billions of events

## 3. Capacity Estimation

### Example: E-commerce Platform

**Event Volume:**
- Daily active users: 10M
- Events per user per day: 50 (views, clicks, purchases, etc.)
- Total events per day: 500M
- Events per second: ~5,800
- Peak: 3x average = ~17,400 events/second

**Storage:**
- Average event size: 1 KB
- Daily storage: 500M * 1 KB = 500 GB/day
- Annual storage: 500 GB * 365 = 180 TB/year
- With compression (3:1): ~60 TB/year

**Read/Write Patterns:**
- Write model: 17K events/sec
- Read model: 100K reads/sec (materialized views)
- Event replay: 1M events/second (bulk)

## 4. High-Level Design

### Event-Driven Architecture Components

```
                    Commands
                       │
                       ↓
              ┌─────────────────┐
              │  Command Handler│
              │  (Write Model)  │
              └────────┬────────┘
                       │
                  Validates
                       │
                       ↓
              ┌─────────────────┐
              │   Event Store   │
              │  (Append-Only)  │
              └────────┬────────┘
                       │
                  Publishes
                       │
                       ↓
              ┌─────────────────┐
              │   Event Bus     │
              │  (Kafka/RabbitMQ)│
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ↓              ↓              ↓
   ┌────────┐    ┌────────┐    ┌────────┐
   │Projection│  │Handler │  │Handler │
   │ Builder │  │Service1│  │Service2│
   └────┬───┘    └────────┘  └────────┘
        │
        ↓
   ┌────────────┐
   │Read Model  │
   │(Materialized)│
   └────────────┘
        │
        ↓
    Query API
```

### Event Sourcing Pattern

```
Traditional State Storage:
┌──────────────────┐
│  Current State   │
│                  │
│  user_id: 123    │
│  balance: $100   │
│  status: active  │
└──────────────────┘

Event Sourcing:
┌──────────────────────────────────┐
│        Event Stream              │
├──────────────────────────────────┤
│ 1. UserCreated                   │
│    {user_id: 123}                │
├──────────────────────────────────┤
│ 2. FundsDeposited                │
│    {user_id: 123, amount: 100}   │
├──────────────────────────────────┤
│ 3. FundsWithdrawn                │
│    {user_id: 123, amount: 20}    │
├──────────────────────────────────┤
│ 4. AccountActivated              │
│    {user_id: 123}                │
└──────────────────────────────────┘
         │
         ↓ Replay
┌──────────────────┐
│  Current State   │
│  balance: $80    │
│  status: active  │
└──────────────────┘
```

## 5. API Design

### Command API (Write Model)

```
POST /api/v1/commands/create-order
Request: {
  "command_id": "cmd-uuid-123",
  "aggregate_id": "order-456",
  "user_id": "user-789",
  "items": [
    {"product_id": "p1", "quantity": 2, "price": 29.99}
  ],
  "timestamp": "2025-11-12T10:30:00Z"
}
Response: {
  "status": "accepted",
  "events": [
    {
      "event_id": "evt-uuid-123",
      "event_type": "OrderCreated",
      "aggregate_id": "order-456",
      "version": 1,
      "timestamp": "2025-11-12T10:30:00.123Z"
    }
  ]
}

POST /api/v1/commands/process-payment
Request: {
  "command_id": "cmd-uuid-124",
  "order_id": "order-456",
  "payment_method": "credit_card",
  "amount": 59.98
}
```

### Event Store API

```
GET /api/v1/events/{aggregate_id}
Query: ?from_version=0
Response: {
  "aggregate_id": "order-456",
  "events": [
    {
      "event_id": "evt-uuid-123",
      "event_type": "OrderCreated",
      "version": 1,
      "data": {...},
      "timestamp": "2025-11-12T10:30:00.123Z"
    },
    {
      "event_id": "evt-uuid-124",
      "event_type": "PaymentProcessed",
      "version": 2,
      "data": {...},
      "timestamp": "2025-11-12T10:30:05.456Z"
    }
  ]
}

POST /api/v1/events/append
Request: {
  "aggregate_id": "order-456",
  "expected_version": 2,
  "events": [
    {
      "event_type": "OrderShipped",
      "data": {"tracking_number": "ABC123"},
      "timestamp": "2025-11-12T11:00:00Z"
    }
  ]
}

GET /api/v1/events/stream
Response: (Server-Sent Events)
event: OrderCreated
data: {"order_id": "order-456", ...}

event: PaymentProcessed
data: {"order_id": "order-456", ...}
```

### Query API (Read Model)

```
GET /api/v1/query/orders/{user_id}
Response: {
  "user_id": "user-789",
  "orders": [
    {
      "order_id": "order-456",
      "status": "shipped",
      "total": 59.98,
      "items_count": 2,
      "created_at": "2025-11-12T10:30:00Z",
      "updated_at": "2025-11-12T11:00:00Z"
    }
  ]
}

GET /api/v1/query/order-details/{order_id}
Response: {
  "order_id": "order-456",
  "status": "shipped",
  "timeline": [
    {"event": "created", "timestamp": "2025-11-12T10:30:00Z"},
    {"event": "paid", "timestamp": "2025-11-12T10:30:05Z"},
    {"event": "shipped", "timestamp": "2025-11-12T11:00:00Z"}
  ],
  "items": [...],
  "total": 59.98
}
```

## 6. Database Schema

### Event Store

```sql
CREATE TABLE events (
    event_id VARCHAR(36) PRIMARY KEY,
    aggregate_id VARCHAR(100) NOT NULL,
    aggregate_type VARCHAR(50) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    version BIGINT NOT NULL,
    event_data JSON NOT NULL,
    metadata JSON,
    timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),

    UNIQUE KEY unique_aggregate_version (aggregate_id, version),
    INDEX idx_aggregate (aggregate_id, version),
    INDEX idx_event_type (event_type),
    INDEX idx_timestamp (timestamp)
);

CREATE TABLE snapshots (
    aggregate_id VARCHAR(100) PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    version BIGINT NOT NULL,
    state_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_version (version)
);

CREATE TABLE event_subscriptions (
    subscription_id VARCHAR(36) PRIMARY KEY,
    subscriber_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(100),
    last_processed_event_id VARCHAR(36),
    last_processed_timestamp TIMESTAMP,
    status ENUM('active', 'paused', 'failed'),
    INDEX idx_subscriber (subscriber_name)
);

-- Idempotency table for command handling
CREATE TABLE processed_commands (
    command_id VARCHAR(36) PRIMARY KEY,
    aggregate_id VARCHAR(100),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result JSON,
    INDEX idx_aggregate (aggregate_id),
    INDEX idx_processed_at (processed_at)
);
```

### Read Model (Materialized Views)

```sql
-- Example: Order summary read model
CREATE TABLE order_summary (
    order_id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    status VARCHAR(50),
    total_amount DECIMAL(10,2),
    items_count INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_event_version BIGINT,
    INDEX idx_user_status (user_id, status),
    INDEX idx_created (created_at)
);

-- Example: User activity read model
CREATE TABLE user_activity (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL,
    activity_type VARCHAR(50),
    activity_data JSON,
    occurred_at TIMESTAMP,
    INDEX idx_user_time (user_id, occurred_at)
);

-- Projection checkpoint
CREATE TABLE projection_checkpoints (
    projection_name VARCHAR(100) PRIMARY KEY,
    last_event_id VARCHAR(36),
    last_event_timestamp TIMESTAMP,
    events_processed BIGINT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 7. Detailed Component Design

### Event Sourcing Implementation

```python
class Event:
    """Base event class"""
    def __init__(self, aggregate_id, version, timestamp=None):
        self.event_id = str(uuid.uuid4())
        self.aggregate_id = aggregate_id
        self.version = version
        self.timestamp = timestamp or datetime.utcnow()


class OrderCreated(Event):
    def __init__(self, order_id, user_id, items, version):
        super().__init__(order_id, version)
        self.user_id = user_id
        self.items = items


class PaymentProcessed(Event):
    def __init__(self, order_id, amount, payment_method, version):
        super().__init__(order_id, version)
        self.amount = amount
        self.payment_method = payment_method


class Aggregate:
    """Base aggregate root"""
    def __init__(self, aggregate_id):
        self.aggregate_id = aggregate_id
        self.version = 0
        self.uncommitted_events = []

    def apply_event(self, event):
        """Apply event to update aggregate state"""
        # Delegate to specific handler
        handler_name = f"apply_{event.__class__.__name__}"
        handler = getattr(self, handler_name, None)
        if handler:
            handler(event)
        self.version = event.version

    def load_from_history(self, events):
        """Reconstruct aggregate from event history"""
        for event in events:
            self.apply_event(event)

    def get_uncommitted_events(self):
        """Get events that haven't been persisted yet"""
        return self.uncommitted_events

    def mark_events_as_committed(self):
        """Clear uncommitted events after persistence"""
        self.uncommitted_events = []


class Order(Aggregate):
    """Order aggregate"""
    def __init__(self, order_id):
        super().__init__(order_id)
        self.user_id = None
        self.items = []
        self.status = None
        self.total = 0

    def create(self, user_id, items):
        """Command: Create order"""
        if self.status is not None:
            raise ValueError("Order already exists")

        event = OrderCreated(
            order_id=self.aggregate_id,
            user_id=user_id,
            items=items,
            version=self.version + 1
        )

        self.apply_event(event)
        self.uncommitted_events.append(event)

    def apply_OrderCreated(self, event):
        """Event handler: OrderCreated"""
        self.user_id = event.user_id
        self.items = event.items
        self.status = 'created'
        self.total = sum(item['price'] * item['quantity'] for item in items)

    def process_payment(self, amount, payment_method):
        """Command: Process payment"""
        if self.status != 'created':
            raise ValueError(f"Cannot process payment for order in status: {self.status}")

        if amount != self.total:
            raise ValueError("Payment amount doesn't match order total")

        event = PaymentProcessed(
            order_id=self.aggregate_id,
            amount=amount,
            payment_method=payment_method,
            version=self.version + 1
        )

        self.apply_event(event)
        self.uncommitted_events.append(event)

    def apply_PaymentProcessed(self, event):
        """Event handler: PaymentProcessed"""
        self.status = 'paid'


class EventStore:
    """Event store for persisting events"""
    def __init__(self, db):
        self.db = db

    async def save_events(self, aggregate_id, events, expected_version):
        """Save events with optimistic concurrency check"""
        # Check current version
        current_version = await self.get_current_version(aggregate_id)

        if current_version != expected_version:
            raise ConcurrencyError(
                f"Expected version {expected_version}, "
                f"but current is {current_version}"
            )

        # Save all events atomically
        async with self.db.transaction():
            for event in events:
                await self.db.execute(
                    """
                    INSERT INTO events (
                        event_id, aggregate_id, aggregate_type,
                        event_type, version, event_data, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    event.event_id,
                    event.aggregate_id,
                    event.aggregate_type,
                    event.__class__.__name__,
                    event.version,
                    json.dumps(event.__dict__),
                    event.timestamp
                )

        # Publish events to event bus
        await self.publish_events(events)

    async def load_events(self, aggregate_id, from_version=0):
        """Load all events for an aggregate"""
        rows = await self.db.query(
            """
            SELECT event_id, event_type, version, event_data, timestamp
            FROM events
            WHERE aggregate_id = ? AND version > ?
            ORDER BY version ASC
            """,
            aggregate_id, from_version
        )

        events = []
        for row in rows:
            event_class = globals()[row['event_type']]
            event_data = json.loads(row['event_data'])
            event = event_class(**event_data)
            events.append(event)

        return events

    async def get_current_version(self, aggregate_id):
        """Get current version of aggregate"""
        result = await self.db.query_one(
            """
            SELECT MAX(version) as version
            FROM events
            WHERE aggregate_id = ?
            """,
            aggregate_id
        )
        return result['version'] if result and result['version'] else 0
```

### CQRS Implementation

```python
class CommandHandler:
    """Handle commands (write operations)"""
    def __init__(self, event_store, repository):
        self.event_store = event_store
        self.repository = repository

    async def handle_create_order(self, command):
        """Handle CreateOrder command"""
        # Check idempotency
        if await self.is_command_processed(command.command_id):
            return await self.get_command_result(command.command_id)

        # Load or create aggregate
        order = Order(command.order_id)

        # Execute command
        order.create(command.user_id, command.items)

        # Save events
        events = order.get_uncommitted_events()
        await self.event_store.save_events(
            order.aggregate_id,
            events,
            expected_version=0  # New aggregate
        )

        # Mark command as processed
        await self.mark_command_processed(command.command_id, events)

        order.mark_events_as_committed()

        return {'status': 'success', 'events': events}

    async def handle_process_payment(self, command):
        """Handle ProcessPayment command"""
        # Load aggregate from event history
        events = await self.event_store.load_events(command.order_id)
        order = Order(command.order_id)
        order.load_from_history(events)

        # Execute command
        order.process_payment(command.amount, command.payment_method)

        # Save new events
        new_events = order.get_uncommitted_events()
        await self.event_store.save_events(
            order.aggregate_id,
            new_events,
            expected_version=order.version - len(new_events)
        )

        return {'status': 'success', 'events': new_events}


class ProjectionBuilder:
    """Build read models from events"""
    def __init__(self, db, event_bus):
        self.db = db
        self.event_bus = event_bus
        self.projection_name = self.__class__.__name__

    async def start(self):
        """Start consuming events and building projection"""
        # Get last checkpoint
        checkpoint = await self.get_checkpoint()

        # Subscribe to events
        await self.event_bus.subscribe(
            self.projection_name,
            from_position=checkpoint,
            handler=self.handle_event
        )

    async def handle_event(self, event):
        """Handle incoming event"""
        # Delegate to specific handler
        handler_name = f"on_{event.event_type}"
        handler = getattr(self, handler_name, None)

        if handler:
            await handler(event)

        # Update checkpoint
        await self.save_checkpoint(event.event_id, event.timestamp)

    async def get_checkpoint(self):
        """Get last processed event position"""
        result = await self.db.query_one(
            """
            SELECT last_event_id, last_event_timestamp
            FROM projection_checkpoints
            WHERE projection_name = ?
            """,
            self.projection_name
        )
        return result if result else None

    async def save_checkpoint(self, event_id, timestamp):
        """Save checkpoint"""
        await self.db.execute(
            """
            INSERT INTO projection_checkpoints
            (projection_name, last_event_id, last_event_timestamp, events_processed)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(projection_name) DO UPDATE SET
                last_event_id = ?,
                last_event_timestamp = ?,
                events_processed = events_processed + 1
            """,
            self.projection_name, event_id, timestamp, event_id, timestamp
        )


class OrderSummaryProjection(ProjectionBuilder):
    """Build order summary read model"""
    async def on_OrderCreated(self, event):
        """Handle OrderCreated event"""
        await self.db.execute(
            """
            INSERT INTO order_summary
            (order_id, user_id, status, total_amount, items_count,
             created_at, updated_at, last_event_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            event.aggregate_id,
            event.user_id,
            'created',
            event.total,
            len(event.items),
            event.timestamp,
            event.timestamp,
            event.version
        )

    async def on_PaymentProcessed(self, event):
        """Handle PaymentProcessed event"""
        await self.db.execute(
            """
            UPDATE order_summary
            SET status = 'paid',
                updated_at = ?,
                last_event_version = ?
            WHERE order_id = ?
            """,
            event.timestamp,
            event.version,
            event.aggregate_id
        )


class QueryHandler:
    """Handle queries (read operations)"""
    def __init__(self, db):
        self.db = db

    async def get_user_orders(self, user_id):
        """Query user's orders from read model"""
        orders = await self.db.query(
            """
            SELECT order_id, status, total_amount, items_count,
                   created_at, updated_at
            FROM order_summary
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            user_id
        )
        return orders

    async def get_order_details(self, order_id):
        """Query order details"""
        order = await self.db.query_one(
            """
            SELECT * FROM order_summary
            WHERE order_id = ?
            """,
            order_id
        )
        return order
```

### Event Bus (Kafka-based)

```python
class EventBus:
    """Distributed event bus using Kafka"""
    def __init__(self, kafka_bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumers = {}

    async def publish(self, event):
        """Publish event to Kafka topic"""
        topic = event.__class__.__name__
        message = {
            'event_id': event.event_id,
            'event_type': event.__class__.__name__,
            'aggregate_id': event.aggregate_id,
            'version': event.version,
            'data': event.__dict__,
            'timestamp': event.timestamp.isoformat()
        }

        await self.producer.send(topic, value=message, key=event.aggregate_id)

    async def subscribe(self, subscriber_name, event_types, handler):
        """Subscribe to events"""
        consumer = KafkaConsumer(
            *event_types,
            bootstrap_servers=self.kafka_bootstrap_servers,
            group_id=subscriber_name,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=False
        )

        self.consumers[subscriber_name] = consumer

        # Process messages
        async for message in consumer:
            event_data = message.value
            await handler(event_data)

            # Commit offset after successful processing
            consumer.commit()
```

### Snapshotting for Performance

```python
class SnapshotStore:
    """Store aggregate snapshots for faster loading"""
    def __init__(self, db):
        self.db = db
        self.snapshot_frequency = 100  # Snapshot every 100 events

    async def save_snapshot(self, aggregate):
        """Save current aggregate state as snapshot"""
        await self.db.execute(
            """
            INSERT INTO snapshots
            (aggregate_id, aggregate_type, version, state_data, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(aggregate_id) DO UPDATE SET
                version = ?,
                state_data = ?,
                created_at = ?
            """,
            aggregate.aggregate_id,
            aggregate.__class__.__name__,
            aggregate.version,
            json.dumps(aggregate.__dict__),
            datetime.utcnow(),
            aggregate.version,
            json.dumps(aggregate.__dict__),
            datetime.utcnow()
        )

    async def load_snapshot(self, aggregate_id, aggregate_class):
        """Load most recent snapshot"""
        row = await self.db.query_one(
            """
            SELECT version, state_data
            FROM snapshots
            WHERE aggregate_id = ?
            """,
            aggregate_id
        )

        if not row:
            return None

        # Reconstruct aggregate from snapshot
        aggregate = aggregate_class(aggregate_id)
        state = json.loads(row['state_data'])
        aggregate.__dict__.update(state)

        return aggregate

    async def load_aggregate(self, aggregate_id, aggregate_class, event_store):
        """Load aggregate using snapshot + subsequent events"""
        # Try to load snapshot first
        aggregate = await self.load_snapshot(aggregate_id, aggregate_class)

        if aggregate:
            # Load events after snapshot
            from_version = aggregate.version
        else:
            # No snapshot - create new aggregate
            aggregate = aggregate_class(aggregate_id)
            from_version = 0

        # Load and apply events since snapshot
        events = await event_store.load_events(aggregate_id, from_version)
        aggregate.load_from_history(events)

        # Create new snapshot if needed
        if aggregate.version - from_version >= self.snapshot_frequency:
            await self.save_snapshot(aggregate)

        return aggregate
```

## 8. Trade-offs and Considerations

### Event Sourcing Advantages

1. **Complete Audit Trail:** Every change is recorded
2. **Time Travel:** Reconstruct past states
3. **Debugging:** Replay events to reproduce bugs
4. **Event Replay:** Rebuild read models from scratch
5. **Temporal Queries:** "What was the state at time T?"

### Event Sourcing Disadvantages

1. **Complexity:** More complex than CRUD
2. **Learning Curve:** Team must understand ES concepts
3. **Event Schema Evolution:** Must handle old event formats
4. **Storage Growth:** Events accumulate over time
5. **Eventual Consistency:** Read models may be stale

### CQRS Trade-offs

| Aspect | Benefit | Cost |
|--------|---------|------|
| **Scalability** | Scale reads/writes independently | More infrastructure |
| **Performance** | Optimized read models | Eventual consistency |
| **Flexibility** | Multiple read models | Complexity |
| **Simplicity** | - | More code to maintain |

### When to Use Event Sourcing

**Good Fit:**
- Need complete audit trail (finance, healthcare)
- Complex domains with rich business logic
- Temporal queries important
- Multiple read models needed
- Collaboration/conflict resolution needed

**Poor Fit:**
- Simple CRUD applications
- Team unfamiliar with pattern
- Strong consistency required everywhere
- Legacy system integration difficult

## 9. Scalability & Bottlenecks

### Event Store Scaling

```python
class PartitionedEventStore:
    """Scale event store using partitioning"""
    def __init__(self, num_partitions=10):
        self.num_partitions = num_partitions
        self.partitions = [EventStore(db) for db in self.get_partition_dbs()]

    def get_partition(self, aggregate_id):
        """Determine partition for aggregate"""
        hash_value = hash(aggregate_id)
        return hash_value % self.num_partitions

    async def save_events(self, aggregate_id, events, expected_version):
        """Save to appropriate partition"""
        partition_idx = self.get_partition(aggregate_id)
        partition = self.partitions[partition_idx]
        await partition.save_events(aggregate_id, events, expected_version)

    async def load_events(self, aggregate_id, from_version=0):
        """Load from appropriate partition"""
        partition_idx = self.get_partition(aggregate_id)
        partition = self.partitions[partition_idx]
        return await partition.load_events(aggregate_id, from_version)
```

### Bottlenecks and Solutions

1. **Event Store Write Throughput:**
   - Solution: Shard by aggregate ID
   - Solution: Use Kafka for event log

2. **Event Replay Performance:**
   - Solution: Snapshots
   - Solution: Parallel replay

3. **Read Model Lag:**
   - Solution: Multiple consumers
   - Solution: Optimize projections
   - Solution: Cache frequently accessed data

4. **Storage Growth:**
   - Solution: Event archiving
   - Solution: Snapshots with event deletion
   - Solution: Compression

## 10. Follow-up Questions

1. **How do you handle event schema evolution?**
   - Versioned events (OrderCreatedV1, OrderCreatedV2)
   - Upcasting: Convert old events to new format on read
   - Weak schema: JSON with optional fields
   - Event transformers: Migrate events in background

2. **How do you ensure event ordering?**
   - Per aggregate: Version numbers
   - Global: Timestamp + UUID
   - Use Kafka partitions by aggregate ID
   - Within partition: Guaranteed order

3. **How do you handle failures in event handlers?**
   - Retry with exponential backoff
   - Dead letter queue for poison messages
   - Idempotent handlers (process multiple times safely)
   - Circuit breaker for downstream failures

4. **Can you delete events?**
   - Generally no (immutable)
   - Exceptions: GDPR/privacy laws
   - Solution: Tombstone events (UserDeleted)
   - Solution: Encryption with key deletion

5. **How do you handle concurrent updates?**
   - Optimistic concurrency (version check)
   - Reject conflicting commands
   - Let user resolve conflict
   - Business rules prevent conflicts

6. **How do you query across aggregates?**
   - Use read models (materialized views)
   - Eventual consistency is acceptable
   - Pre-compute joins in projections
   - Avoid cross-aggregate queries in commands

7. **How do you migrate from traditional CRUD?**
   - Strangler fig pattern
   - Dual writes initially
   - Gradual migration domain by domain
   - Keep old system as read model temporarily

8. **How do you test event-sourced systems?**
   - Given-When-Then: Given events, When command, Then events
   - Test projections: Given events, Then read model state
   - Integration tests with real event store
   - Property-based testing for invariants

9. **What is the difference between Event Sourcing and Change Data Capture?**
   - ES: Application-level, domain events
   - CDC: Database-level, row changes
   - ES: Part of design
   - CDC: Added later, retrofit

10. **How do you monitor event-driven systems?**
    - Event processing lag (time behind real-time)
    - Projection checkpoint lag
    - Event throughput
    - Command processing time
    - Failed event handlers
    - Dead letter queue size
