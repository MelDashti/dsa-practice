# Design a Large-Scale Notification Service

## 1. Problem Overview

Design a unified notification system that can send billions of notifications daily across multiple channels (push notifications, SMS, email, in-app) to millions of users. The system must support various notification types, user preferences, delivery guarantees, rate limiting, and analytics while maintaining high throughput and low latency.

**Key Challenges**:
- Handle billions of notifications per day
- Support multiple delivery channels (push, SMS, email, in-app, webhooks)
- Respect user preferences and quiet hours
- Implement priority-based delivery
- Ensure at-least-once delivery without excessive duplicates
- Rate limiting and throttling
- Track delivery status and analytics
- Scale horizontally across regions
- Handle third-party provider failures

## 2. Requirements

### Functional Requirements
- **Multi-Channel Delivery**: Push, SMS, email, in-app, webhooks
- **Notification Types**: Transactional, promotional, system alerts
- **User Preferences**: Channel preferences, frequency, quiet hours
- **Priority Levels**: Critical, high, normal, low
- **Scheduling**: Send immediately or at specified time
- **Templating**: Support dynamic content with variables
- **Delivery Tracking**: Track sent, delivered, read, clicked
- **Batching**: Group similar notifications
- **Retry Logic**: Retry failed deliveries with exponential backoff
- **Deduplication**: Prevent sending duplicates
- **User Segmentation**: Target specific user groups
- **A/B Testing**: Test different notification variants

### Non-Functional Requirements
- **Throughput**: 10M notifications per second at peak
- **Latency**: < 1 second for critical notifications
- **Availability**: 99.99% uptime
- **Scalability**: Support 1B users
- **Reliability**: At-least-once delivery guarantee
- **Durability**: No notification loss
- **Compliance**: GDPR, CAN-SPAM, TCPA
- **Cost-Effective**: Optimize third-party API costs

### Out of Scope
- Notification content generation (handled by services)
- User authentication (handled by auth service)
- Analytics dashboard UI (focus on backend)

## 3. Scale Estimation

### Traffic Estimates
- **Total Users**: 1 billion
- **Daily Active Users**: 300 million
- **Notifications per user per day**: 20
- **Total daily notifications**: 6 billion
- **Average QPS**: 6B / 86400 ≈ 69,450
- **Peak QPS**: 10M (special events, breaking news)
- **Channel distribution**:
  - Push: 70% (4.2B)
  - Email: 20% (1.2B)
  - SMS: 5% (300M)
  - In-app: 5% (300M)

### Storage Estimates
- **Notification metadata**: 500 bytes
- **Daily storage**: 6B × 500 bytes = 3 TB/day
- **Yearly storage**: ~1 PB/year
- **Retention**: 90 days = 270 TB
- **User preferences**: 1M users × 2 KB = 2 GB

### Infrastructure Estimates
- **Worker nodes**: 5,000 servers (2000 notifications/sec each)
- **Database shards**: 1,000
- **Message queue partitions**: 10,000
- **Cache servers**: 500 Redis instances

### Cost Estimates (monthly)
- **Push notifications**: Free (APNS/FCM)
- **SMS**: 300M × $0.01 = $3M
- **Email**: 1.2B × $0.0001 = $120K
- **Infrastructure**: $500K
- **Total**: ~$3.6M/month

## 4. High-Level Design

```
┌──────────────────────────────────────────────────────────────────┐
│                        Service Layer                              │
│  (User Service, Order Service, Social Service, etc.)             │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ Notification Request
                         │
                         ▼
              ┌──────────────────────┐
              │   API Gateway        │
              │  (Rate Limiting,     │
              │   Authentication)    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Notification API    │
              │  (Validation,        │
              │   Enrichment)        │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Message Queue      │
              │   (Kafka/Pulsar)     │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┬───────────────┐
         │               │               │               │
         ▼               ▼               ▼               ▼
    ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
    │Priority│     │Priority│     │Priority│     │Priority│
    │Critical│     │  High  │     │ Normal │     │  Low   │
    │ Queue  │     │ Queue  │     │ Queue  │     │ Queue  │
    └────┬───┘     └────┬───┘     └────┬───┘     └────┬───┘
         │              │               │               │
         └──────────────┴───────────────┴───────────────┘
                         │
         ┌───────────────┼────────────────────────────┐
         │               │                            │
         ▼               ▼                            ▼
┌─────────────────┐ ┌──────────────┐     ┌────────────────────┐
│   Preference    │ │  Deduplication│     │   Rate Limiter     │
│    Filter       │ │    Service    │     │                    │
└────────┬────────┘ └──────┬───────┘     └─────────┬──────────┘
         │                 │                        │
         └─────────────────┴────────────────────────┘
                           │
         ┌─────────────────┼──────────────────────┐
         │                 │                      │
         ▼                 ▼                      ▼
┌────────────────┐  ┌─────────────┐     ┌────────────────┐
│  Push Worker   │  │ SMS Worker  │     │  Email Worker  │
│   (FCM/APNS)   │  │  (Twilio)   │     │  (SendGrid)    │
└────────┬───────┘  └──────┬──────┘     └───────┬────────┘
         │                 │                     │
         └─────────────────┴─────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Delivery Tracking   │
                │   & Analytics        │
                └──────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Database & Storage  │
                │  (Notifications,     │
                │   Preferences, Logs) │
                └──────────────────────┘
```

## 5. API Design

### Send Notification
```
POST /api/v1/notifications/send
{
  "user_ids": ["user_123", "user_456"],  // or user_segment
  "channels": ["push", "email"],  // preferred channels
  "priority": "high",  // critical, high, normal, low
  "notification": {
    "title": "New message from {{sender_name}}",
    "body": "{{message_preview}}",
    "template_id": "new_message",
    "data": {
      "sender_name": "John",
      "message_preview": "Hey, are you free?",
      "deep_link": "app://chat/123"
    },
    "image_url": "https://...",
    "action_buttons": [
      {"label": "Reply", "action": "reply"},
      {"label": "View", "action": "open_chat"}
    ]
  },
  "scheduled_at": null,  // Unix timestamp, null for immediate
  "ttl": 3600,  // seconds
  "collapse_key": "chat_123",  // for deduplication
  "idempotency_key": "req_abc123"
}

Response:
{
  "notification_id": "notif_xyz789",
  "status": "queued",
  "estimated_delivery": "2024-11-12T12:35:00Z",
  "recipient_count": 2
}
```

### Batch Send
```
POST /api/v1/notifications/batch
{
  "notifications": [
    {"user_id": "user_123", "notification": {...}},
    {"user_id": "user_456", "notification": {...}}
  ],
  "priority": "normal"
}

Response:
{
  "batch_id": "batch_abc123",
  "notification_ids": ["notif_1", "notif_2"],
  "status": "queued"
}
```

### Get Notification Status
```
GET /api/v1/notifications/{notification_id}/status

Response:
{
  "notification_id": "notif_xyz789",
  "status": "delivered",
  "created_at": "2024-11-12T12:34:00Z",
  "sent_at": "2024-11-12T12:34:01Z",
  "delivered_at": "2024-11-12T12:34:02Z",
  "read_at": "2024-11-12T12:35:00Z",
  "channel": "push",
  "provider": "fcm",
  "attempts": 1
}
```

### Update User Preferences
```
PUT /api/v1/users/{user_id}/preferences
{
  "channels": {
    "push": {
      "enabled": true,
      "categories": {
        "messages": true,
        "marketing": false,
        "system": true
      }
    },
    "email": {
      "enabled": true,
      "categories": {
        "messages": true,
        "marketing": true,
        "system": true
      }
    },
    "sms": {
      "enabled": false
    }
  },
  "quiet_hours": {
    "enabled": true,
    "start": "22:00",
    "end": "08:00",
    "timezone": "America/New_York"
  },
  "frequency_limit": {
    "max_per_day": 50,
    "max_per_hour": 10
  }
}
```

### Get Analytics
```
GET /api/v1/analytics/notifications
Query Parameters:
  - start_date: 2024-11-01
  - end_date: 2024-11-12
  - user_segment: premium_users
  - channel: push

Response:
{
  "metrics": {
    "sent": 1000000,
    "delivered": 950000,
    "failed": 50000,
    "read": 500000,
    "clicked": 200000,
    "unsubscribed": 1000
  },
  "rates": {
    "delivery_rate": 0.95,
    "open_rate": 0.526,
    "click_rate": 0.21,
    "unsubscribe_rate": 0.001
  },
  "by_channel": {
    "push": {...},
    "email": {...},
    "sms": {...}
  }
}
```

## 6. Data Models

### Notification Table (Cassandra)
```cql
CREATE TABLE notifications (
    notification_id UUID,
    user_id BIGINT,
    priority VARCHAR(10),
    status VARCHAR(20),  -- queued, sent, delivered, failed, read
    channel VARCHAR(20),  -- push, email, sms, in_app
    template_id VARCHAR(50),
    title TEXT,
    body TEXT,
    data MAP<TEXT, TEXT>,
    created_at TIMESTAMP,
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    ttl INT,
    attempts INT DEFAULT 0,
    error_message TEXT,

    PRIMARY KEY (user_id, created_at, notification_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

CREATE INDEX ON notifications(status);
CREATE INDEX ON notifications(notification_id);
```

### User Preferences Table (PostgreSQL)
```sql
CREATE TABLE user_notification_preferences (
    user_id BIGINT PRIMARY KEY,
    preferences JSONB NOT NULL,
    quiet_hours JSONB,
    frequency_limits JSONB,
    unsubscribed_categories TEXT[],
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_prefs ON user_notification_preferences
    USING GIN (preferences);
```

### Template Table (PostgreSQL)
```sql
CREATE TABLE notification_templates (
    template_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    channels TEXT[],  -- Supported channels
    title_template TEXT,
    body_template TEXT,
    variables JSONB,  -- Expected variables
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Device Table (PostgreSQL)
```sql
CREATE TABLE user_devices (
    device_id VARCHAR(100) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    platform VARCHAR(20),  -- ios, android, web
    device_token TEXT NOT NULL,  -- FCM/APNS token
    is_active BOOLEAN DEFAULT true,
    last_active TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_devices ON user_devices(user_id, is_active);
CREATE INDEX idx_device_token ON user_devices(device_token);
```

### Delivery Log Table (Cassandra)
```cql
CREATE TABLE delivery_logs (
    notification_id UUID,
    user_id BIGINT,
    channel VARCHAR(20),
    provider VARCHAR(50),  -- fcm, apns, twilio, sendgrid
    status VARCHAR(20),
    response_code INT,
    response_body TEXT,
    timestamp TIMESTAMP,
    latency INT,  -- milliseconds

    PRIMARY KEY (notification_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

### Redis Schemas

#### Deduplication
```
Key: dedup:{collapse_key}:{user_id}
Value: notification_id
TTL: TTL from request (default 1 hour)
```

#### Rate Limiting
```
Key: rate_limit:{user_id}:hour:{timestamp}
Value: count
TTL: 1 hour

Key: rate_limit:{user_id}:day:{date}
Value: count
TTL: 24 hours
```

#### Notification Cache
```
Key: notif:{notification_id}
Value: {
  "status": "delivered",
  "sent_at": 1699876543000,
  "delivered_at": 1699876544000
}
TTL: 7 days
```

## 7. Core Services Design

### Notification API Service
```python
class NotificationAPIService:
    def send_notification(self, request):
        # Validate request
        self.validate_request(request)

        # Check idempotency
        if request.idempotency_key:
            existing = self.check_idempotency(request.idempotency_key)
            if existing:
                return existing

        # Enrich notification
        notification = self.enrich_notification(request)

        # Generate notification IDs for each user
        notifications = []
        for user_id in request.user_ids:
            notif = {
                "notification_id": uuid.uuid4(),
                "user_id": user_id,
                "priority": request.priority,
                "channels": request.channels,
                "notification": notification,
                "scheduled_at": request.scheduled_at,
                "ttl": request.ttl,
                "collapse_key": request.collapse_key
            }
            notifications.append(notif)

        # Store in database
        self.db.batch_insert_notifications(notifications)

        # Publish to message queue
        for notif in notifications:
            queue_name = f"notifications_{notif['priority']}"
            self.kafka.produce(queue_name, notif)

        # Store idempotency key
        if request.idempotency_key:
            self.store_idempotency(
                request.idempotency_key,
                notifications[0]["notification_id"]
            )

        return {
            "notification_ids": [n["notification_id"] for n in notifications],
            "status": "queued"
        }

    def enrich_notification(self, request):
        # Load template if specified
        if request.notification.template_id:
            template = self.template_service.get_template(
                request.notification.template_id
            )

            # Render template with data
            title = self.render_template(
                template.title_template,
                request.notification.data
            )
            body = self.render_template(
                template.body_template,
                request.notification.data
            )

            return {
                **request.notification,
                "title": title,
                "body": body
            }

        return request.notification
```

### Worker Service
```python
class NotificationWorker:
    def __init__(self, channel):
        self.channel = channel  # push, sms, email
        self.provider = self.initialize_provider()

    def process_notification(self, notification):
        user_id = notification["user_id"]

        # Check deduplication
        if self.is_duplicate(notification):
            self.log_dropped(notification, "duplicate")
            return

        # Check user preferences
        if not self.should_send(user_id, notification):
            self.log_dropped(notification, "user_preferences")
            return

        # Check rate limits
        if not self.check_rate_limit(user_id):
            self.log_dropped(notification, "rate_limited")
            # Requeue for later
            self.requeue_notification(notification, delay=300)
            return

        # Check quiet hours
        if self.is_quiet_hours(user_id):
            self.log_dropped(notification, "quiet_hours")
            # Schedule for end of quiet hours
            self.reschedule_notification(notification, user_id)
            return

        # Get user's device tokens
        devices = self.get_user_devices(user_id, self.channel)

        if not devices:
            self.log_dropped(notification, "no_devices")
            return

        # Send to each device
        for device in devices:
            try:
                result = self.send_to_device(device, notification)

                # Update status
                self.update_notification_status(
                    notification["notification_id"],
                    "sent"
                )

                # Track delivery
                self.track_delivery(
                    notification["notification_id"],
                    device,
                    result
                )

            except ProviderError as e:
                # Retry logic
                if self.should_retry(notification):
                    self.retry_notification(notification)
                else:
                    self.mark_failed(notification, str(e))

    def should_send(self, user_id, notification):
        # Load user preferences
        prefs = self.preference_service.get_preferences(user_id)

        # Check if channel is enabled
        channel_prefs = prefs.get("channels", {}).get(self.channel, {})
        if not channel_prefs.get("enabled", True):
            return False

        # Check category preferences
        category = notification.get("category", "system")
        categories = channel_prefs.get("categories", {})
        if not categories.get(category, True):
            return False

        return True

    def check_rate_limit(self, user_id):
        # Get user's rate limits
        prefs = self.preference_service.get_preferences(user_id)
        limits = prefs.get("frequency_limits", {})

        # Check hourly limit
        hourly_limit = limits.get("max_per_hour", 100)
        current_hour = datetime.now().strftime("%Y-%m-%d-%H")
        hourly_key = f"rate_limit:{user_id}:hour:{current_hour}"
        hourly_count = self.redis.incr(hourly_key)

        if hourly_count == 1:
            self.redis.expire(hourly_key, 3600)

        if hourly_count > hourly_limit:
            return False

        # Check daily limit
        daily_limit = limits.get("max_per_day", 500)
        current_date = datetime.now().strftime("%Y-%m-%d")
        daily_key = f"rate_limit:{user_id}:day:{current_date}"
        daily_count = self.redis.incr(daily_key)

        if daily_count == 1:
            self.redis.expire(daily_key, 86400)

        if daily_count > daily_limit:
            return False

        return True

    def is_duplicate(self, notification):
        if not notification.get("collapse_key"):
            return False

        key = f"dedup:{notification['collapse_key']}:{notification['user_id']}"
        existing = self.redis.get(key)

        if existing:
            return True

        # Set dedup key
        self.redis.setex(
            key,
            notification.get("ttl", 3600),
            notification["notification_id"]
        )

        return False

    def send_to_device(self, device, notification):
        if self.channel == "push":
            return self.send_push(device, notification)
        elif self.channel == "sms":
            return self.send_sms(device, notification)
        elif self.channel == "email":
            return self.send_email(device, notification)
```

### Push Notification Worker
```python
class PushNotificationWorker(NotificationWorker):
    def initialize_provider(self):
        # Initialize FCM and APNS clients
        self.fcm_client = FCMClient(api_key=FCM_API_KEY)
        self.apns_client = APNSClient(
            cert_path=APNS_CERT_PATH,
            team_id=APNS_TEAM_ID
        )

    def send_push(self, device, notification):
        if device.platform == "android":
            return self.send_fcm(device, notification)
        elif device.platform == "ios":
            return self.send_apns(device, notification)

    def send_fcm(self, device, notification):
        message = {
            "token": device.device_token,
            "notification": {
                "title": notification["title"],
                "body": notification["body"],
                "image": notification.get("image_url")
            },
            "data": notification.get("data", {}),
            "android": {
                "priority": "high" if notification["priority"] == "critical" else "normal",
                "ttl": notification.get("ttl", 3600)
            }
        }

        try:
            response = self.fcm_client.send(message)
            return response
        except FCMError as e:
            if e.code == "UNREGISTERED":
                # Device token invalid, mark inactive
                self.mark_device_inactive(device.device_id)
            raise

    def send_apns(self, device, notification):
        payload = {
            "aps": {
                "alert": {
                    "title": notification["title"],
                    "body": notification["body"]
                },
                "badge": 1,
                "sound": "default",
                "priority": 10 if notification["priority"] == "critical" else 5
            },
            "data": notification.get("data", {})
        }

        try:
            response = self.apns_client.send_notification(
                device.device_token,
                payload
            )
            return response
        except APNSError as e:
            if e.code == "BadDeviceToken":
                self.mark_device_inactive(device.device_id)
            raise
```

### Deduplication Service
```python
class DeduplicationService:
    def is_duplicate(self, user_id, collapse_key, window_seconds=3600):
        if not collapse_key:
            return False

        key = f"dedup:{collapse_key}:{user_id}"
        exists = self.redis.exists(key)

        if exists:
            return True

        # Set dedup key with expiry
        self.redis.setex(key, window_seconds, "1")
        return False

    def clear_dedup(self, user_id, collapse_key):
        key = f"dedup:{collapse_key}:{user_id}"
        self.redis.delete(key)
```

### Analytics Service
```python
class AnalyticsService:
    def track_event(self, notification_id, event_type, metadata):
        event = {
            "notification_id": notification_id,
            "event_type": event_type,  # sent, delivered, read, clicked
            "timestamp": current_timestamp_ms(),
            "metadata": metadata
        }

        # Store in analytics database
        self.analytics_db.insert_event(event)

        # Update notification status
        self.update_notification_status(notification_id, event_type)

        # Update real-time metrics
        self.update_metrics(event)

    def update_metrics(self, event):
        date = datetime.now().strftime("%Y-%m-%d")
        hour = datetime.now().strftime("%Y-%m-%d-%H")

        # Increment counters
        self.redis.hincrby(f"metrics:daily:{date}", event["event_type"], 1)
        self.redis.hincrby(f"metrics:hourly:{hour}", event["event_type"], 1)

    def get_metrics(self, start_date, end_date, filters):
        # Aggregate from analytics database
        metrics = self.analytics_db.aggregate_metrics(
            start_date,
            end_date,
            filters
        )

        return metrics
```

## 8. Real-time Communication (WebSockets)

For in-app notifications, WebSocket connections are maintained:

```python
class InAppNotificationGateway:
    def on_connect(self, user_id, connection):
        # Store connection
        self.connections[user_id] = connection

        # Subscribe to user's notification channel
        self.redis.subscribe(f"notifications:{user_id}")

        # Send unread notifications
        unread = self.get_unread_notifications(user_id)
        for notif in unread:
            connection.send(notif)

    def on_new_notification(self, user_id, notification):
        # Check if user is connected
        if user_id in self.connections:
            self.connections[user_id].send({
                "type": "notification",
                "data": notification
            })
        else:
            # Store for later delivery
            self.store_unread(user_id, notification)
```

## 9. Geospatial Indexing

Not directly applicable to notification service, but can be used for:
- Location-based notifications
- Timezone-aware scheduling

```python
def send_location_based_notification(lat, lon, radius_km, notification):
    # Find users within radius
    nearby_users = redis.georadius(
        "user_locations",
        lon, lat,
        radius_km, "km"
    )

    # Send notification to nearby users
    for user_id in nearby_users:
        send_notification(user_id, notification)
```

## 10. Scalability & Performance

### Horizontal Scaling
- **Stateless workers**: Easy to add more workers
- **Kafka partitioning**: Partition by user_id for parallelism
- **Database sharding**: Shard by user_id
- **Redis sharding**: Consistent hashing

### Priority Queues
```
Critical Queue (SLA: < 1s)    → 30% of workers
High Queue (SLA: < 5s)        → 40% of workers
Normal Queue (SLA: < 30s)     → 25% of workers
Low Queue (SLA: < 5min)       → 5% of workers
```

### Batch Processing
- Group similar notifications
- Batch database writes
- Bulk API calls to providers

### Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "closed"  # closed, open, half_open
        self.last_failure = None

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.timeout:
                self.state = "half_open"
            else:
                raise CircuitOpenError()

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        self.state = "closed"

    def on_failure(self):
        self.failure_count += 1
        self.last_failure = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
```

## 11. Trade-offs

### Kafka vs SQS
**Chosen: Kafka**
- Pros: High throughput, replay capability, ordering guarantees
- Cons: More complex, operational overhead
- Alternative: SQS (simpler, managed, lower throughput)

### At-Least-Once vs Exactly-Once Delivery
**Chosen: At-least-once with deduplication**
- Pros: Simpler, more reliable, acceptable duplicates
- Cons: May send duplicates
- Alternative: Exactly-once (complex, performance overhead)

### Push vs Pull for Workers
**Chosen: Pull (workers consume from Kafka)**
- Pros: Worker controls rate, easier backpressure
- Cons: Slight latency increase
- Alternative: Push (lower latency, harder backpressure)

### Cassandra vs PostgreSQL
**Chosen: Cassandra for notifications, PostgreSQL for preferences**
- Pros: Cassandra handles write-heavy workload, PostgreSQL for consistency
- Cons: Multiple databases to manage
- Alternative: Single database (simpler, doesn't scale as well)

## 12. Follow-up Questions

### Functional Enhancements
1. **How would you add notification grouping (bundling)?**
   - Group by collapse_key
   - Aggregate similar notifications
   - Send summary instead of individual
   - "3 new messages from John"

2. **How would you implement scheduled notifications?**
   - Separate scheduled queue
   - Cron job to check due notifications
   - Move to regular queue when due
   - Handle timezone conversions

3. **How would you add A/B testing?**
   - Variant assignment service
   - Track variant in notification
   - Compare metrics by variant
   - Statistical significance testing

### Scale & Performance
4. **How would you handle 100M QPS?**
   - More Kafka partitions (10K → 100K)
   - More worker nodes (10K → 100K)
   - Database sharding (1K → 10K shards)
   - Regional clusters

5. **How would you optimize costs?**
   - Batch SMS messages
   - Use cheaper email providers
   - Aggressive deduplication
   - Smart channel selection
   - User preference learning

6. **How would you reduce delivery latency?**
   - Regional deployment
   - Pre-warm connections to providers
   - Parallel delivery to multiple devices
   - Priority queues with dedicated workers

### Reliability & Security
7. **How would you ensure GDPR compliance?**
   - User consent tracking
   - Easy opt-out mechanism
   - Data retention policies
   - Right to deletion
   - Audit logs

8. **How would you handle provider outages?**
   - Multi-provider setup
   - Automatic failover
   - Circuit breaker pattern
   - Retry with exponential backoff
   - Manual provider switching

9. **How would you prevent notification spam?**
   - Rate limiting per user
   - Frequency caps
   - ML-based spam detection
   - User feedback loop
   - Sender reputation system

### Monitoring & Operations
10. **What metrics would you track?**
    - Delivery rate by channel
    - Latency (p50, p95, p99)
    - Provider success rate
    - Queue depth
    - Worker utilization
    - User engagement (open, click rates)
    - Cost per notification

11. **How would you debug failed notifications?**
    - Distributed tracing (notification_id)
    - Delivery logs with provider responses
    - Retry history
    - User device status
    - Provider status dashboard

12. **How would you perform rolling updates?**
    - Blue-green deployment
    - Canary releases (1%, 10%, 50%, 100%)
    - Feature flags
    - Gradual queue drain
    - Rollback capability
