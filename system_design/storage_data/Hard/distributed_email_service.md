# Design Distributed Email Service (Gmail-scale)

**Difficulty:** Hard

## 1. Problem Statement

Design a large-scale email system like Gmail that handles billions of emails per day, provides reliable delivery, spam filtering, search capabilities, and stores emails durably. The system should support features like conversations, labels, attachments, and real-time notifications while maintaining high availability and low latency.

**Scale:** 
- 2 billion users
- 500 billion emails stored
- 10 billion emails sent/received daily
- 99.99% availability
- < 100ms search latency

## 2. Requirements

### Functional Requirements
1. **Send Email**: Compose and send emails with attachments
2. **Receive Email**: Receive emails from internal/external sources
3. **Storage**: Store emails reliably with attachments
4. **Search**: Full-text search across email content
5. **Organization**:
   - Labels (not folders - emails can have multiple labels)
   - Conversations (threading)
   - Archive/delete
6. **Spam Filtering**: Detect and filter spam
7. **Attachments**: Support files up to 25 MB
8. **Real-time Sync**: Push notifications for new emails
9. **Contacts**: Address book management

### Non-Functional Requirements
1. **Availability**: 99.99% uptime
2. **Durability**: No email loss (99.999999999%)
3. **Scalability**: 2B users, 500B emails
4. **Performance**:
   - Send latency: < 1 second
   - Inbox load: < 200ms
   - Search: < 100ms
5. **Consistency**: Eventual consistency acceptable
6. **Security**: Encryption at rest and in transit

## 3. Storage Estimation

### Assumptions
- **Total Users**: 2 billion
- **Active Users**: 500 million daily
- **Emails per User**: 250 emails average
- **Average Email Size**: 50 KB (including metadata)
- **Attachment Rate**: 20% of emails
- **Average Attachment**: 2 MB
- **Daily Emails Sent**: 10 billion

### Calculations

**Total Email Storage:**
```
2B users × 250 emails × 50 KB = 25 Petabytes (PB)
Attachments: 2B × 250 × 20% × 2 MB = 200 PB
Total: 225 PB
With replication (3x): 675 PB
```

**Daily Storage Growth:**
```
10B emails/day × 50 KB = 500 TB/day
Attachments: 10B × 20% × 2 MB = 4 PB/day
Total: 4.5 PB/day growth
```

**Metadata Storage:**
```
Per email: 10 KB (sender, recipients, subject, labels, timestamps)
500B emails × 10 KB = 5 PB metadata
```

**Request Load:**
```
500M daily active users
- Send emails: 10B/day ÷ 86,400 = 115,740 emails/sec
- Read inbox: 500M users × 10 checks/day = 5B/day = 57,870/sec
- Search: 500M × 5 searches/day = 2.5B/day = 28,935/sec
```

**Bandwidth:**
```
Send: 115,740 emails/sec × 50 KB = 5.7 GB/sec
Receive: Similar to send
Attachments: 115,740 × 20% × 2 MB = 46 GB/sec
Peak (10x): 517 GB/sec
```

## 4. High-Level Architecture

```
┌────────────────────────────────────────────────────────┐
│                   Client Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │Web Client│  │Mobile App│  │ Desktop  │           │
│  │          │  │(iOS/And.)│  │  Client  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└────────────────────────────────────────────────────────┘
                       │
                       │ HTTPS / IMAP / SMTP
                       ▼
            ┌──────────────────────┐
            │   Load Balancer      │
            │  (Global Anycast)    │
            └──────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  SMTP        │ │  API         │ │  WebSocket   │
│  Gateway     │ │  Gateway     │ │  Server      │
│  (Receive)   │ │  (REST)      │ │  (Push)      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐         ┌─────────────────────┐
│   Application   │         │  Background Jobs    │
│    Services     │         │  ┌──────────────┐   │
│                 │         │  │ Spam Filter  │   │
│┌───────────────┐│         │  └──────────────┘   │
││ Mail Service  ││         │  ┌──────────────┐   │
│└───────────────┘│         │  │ Indexer      │   │
│┌───────────────┐│         │  └──────────────┘   │
││Search Service ││         │  ┌──────────────┐   │
│└───────────────┘│         │  │ Virus Scan   │   │
│┌───────────────┐│         │  └──────────────┘   │
││Contact Service││         └─────────────────────┘
│└───────────────┘│                   │
└─────────┬───────┘                   │
          │                           │
    ┌─────┴──────┬────────────────────┘
    │            │
    ▼            ▼
┌─────────┐  ┌────────────┐
│Metadata │  │  Message   │
│   DB    │  │  Queue     │
│(Spanner)│  │  (Kafka)   │
└────┬────┘  └────────────┘
     │
     ▼
┌────────────────────────────────────────────┐
│          Storage Layer                     │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │Email Storage │  │  Search Index    │   │
│  │ (Bigtable)   │  │(Elasticsearch)   │   │
│  └──────────────┘  └──────────────────┘   │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │ Attachments  │  │  Spam Models     │   │
│  │ (GCS/S3)     │  │  (ML Storage)    │   │
│  └──────────────┘  └──────────────────┘   │
└────────────────────────────────────────────┘
```

### Key Components

1. **SMTP Gateway**: Receive incoming emails (SMTP protocol)
2. **API Gateway**: REST APIs for web/mobile clients
3. **WebSocket Server**: Real-time push notifications
4. **Mail Service**: Email CRUD operations
5. **Search Service**: Full-text search (Elasticsearch)
6. **Spam Filter**: ML-based spam detection
7. **Virus Scanner**: Attachment scanning
8. **Indexer**: Background email indexing
9. **Metadata DB**: Google Spanner for email metadata
10. **Email Storage**: Bigtable for email bodies
11. **Attachment Storage**: GCS/S3 for large files
12. **Message Queue**: Kafka for async processing

## 5. API Design

### Send Email
```http
POST /api/v1/emails/send
Authorization: Bearer {token}

Request:
{
  "to": ["user@example.com", "user2@example.com"],
  "cc": ["cc@example.com"],
  "bcc": ["bcc@example.com"],
  "subject": "Meeting Tomorrow",
  "body": "Let's meet at 10am",
  "body_html": "<p>Let's meet at 10am</p>",
  "attachments": [
    {
      "filename": "document.pdf",
      "content_type": "application/pdf",
      "size": 1048576,
      "upload_id": "upload_abc123"
    }
  ],
  "labels": ["work"],
  "in_reply_to": "email_xyz789" // For threading
}

Response (201 Created):
{
  "email_id": "email_abc123",
  "thread_id": "thread_xyz",
  "sent_at": "2025-11-12T12:00:00Z",
  "status": "sent"
}
```

### List Inbox
```http
GET /api/v1/emails?label=inbox&page_size=50&page_token=xyz
Authorization: Bearer {token}

Response (200 OK):
{
  "emails": [
    {
      "email_id": "email_abc",
      "thread_id": "thread_xyz",
      "from": {"email": "sender@example.com", "name": "John Doe"},
      "to": ["user@example.com"],
      "subject": "Meeting Tomorrow",
      "snippet": "Let's meet at 10am for the...",
      "labels": ["inbox", "important"],
      "has_attachment": true,
      "unread": true,
      "received_at": "2025-11-12T11:00:00Z",
      "size_bytes": 51200
    }
  ],
  "next_page_token": "token_abc",
  "total_count": 4523
}
```

### Get Email
```http
GET /api/v1/emails/{email_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "email_id": "email_abc",
  "thread_id": "thread_xyz",
  "from": {"email": "sender@example.com", "name": "John Doe"},
  "to": [{"email": "user@example.com", "name": "Jane"}],
  "cc": [],
  "bcc": [],
  "subject": "Meeting Tomorrow",
  "body_text": "Let's meet at 10am",
  "body_html": "<p>Let's meet at 10am</p>",
  "labels": ["inbox"],
  "attachments": [
    {
      "attachment_id": "att_123",
      "filename": "document.pdf",
      "content_type": "application/pdf",
      "size": 1048576,
      "download_url": "https://mail.example.com/attachments/att_123"
    }
  ],
  "received_at": "2025-11-12T11:00:00Z",
  "read": false
}
```

### Search Emails
```http
GET /api/v1/emails/search?q=from:john+meeting&after=2025-01-01&has:attachment
Authorization: Bearer {token}

Response (200 OK):
{
  "results": [
    {
      "email_id": "email_abc",
      "subject": "Meeting Tomorrow",
      "snippet": "...meeting at 10am...",
      "relevance_score": 0.95
    }
  ],
  "total_results": 42,
  "search_time_ms": 87
}
```

### Modify Labels
```http
POST /api/v1/emails/{email_id}/labels
Authorization: Bearer {token}

Request:
{
  "add_labels": ["important", "work"],
  "remove_labels": ["inbox"]
}

Response (200 OK):
{
  "email_id": "email_abc",
  "labels": ["important", "work", "archived"]
}
```

## 6. Email Delivery Flow

### Sending Email (Outbound)

```
1. Client sends via API
   ↓
2. Mail Service receives request
   ↓
3. Validation
   ├─→ Validate recipients
   ├─→ Check send quota
   └─→ Scan attachments for viruses
   ↓
4. Store in Sent folder (local user)
   ↓
5. Determine delivery path
   ├─→ Internal recipient? → Direct delivery
   └─→ External recipient? → SMTP relay
   ↓
6. Publish to Kafka: "email_send" event
   ↓
7. SMTP Worker consumes event
   ↓
8. Deliver to recipient
   ├─→ Internal: Write to recipient's inbox
   └─→ External: Send via SMTP to recipient's MX server
   ↓
9. Update delivery status
```

### Receiving Email (Inbound)

```
1. External SMTP server connects
   ↓
2. SMTP Gateway receives email
   ↓
3. Initial validation
   ├─→ SPF/DKIM/DMARC check
   ├─→ Rate limiting
   └─→ Recipient exists?
   ↓
4. Publish to Kafka: "email_received" event
   ↓
5. Processing Pipeline (async)
   ├─→ Spam filter (ML model)
   ├─→ Virus scan (ClamAV)
   ├─→ Phishing detection
   └─→ Auto-labeling
   ↓
6. Store email
   ├─→ Body → Bigtable
   ├─→ Metadata → Spanner
   └─→ Attachments → GCS
   ↓
7. Index for search (Elasticsearch)
   ↓
8. Update inbox
   ↓
9. Send push notification (WebSocket)
```

## 7. Storage Strategy

### Email Body Storage (Bigtable)

**Schema:**
```
Row Key: {user_id}#{email_id}
Column Family: email
Columns:
  - email:from
  - email:to
  - email:subject
  - email:body_text
  - email:body_html
  - email:received_at
  - email:size

Why Bigtable?
- Wide-column store
- Petabyte scale
- Low latency (< 10ms)
- Time-series optimized
```

### Metadata Storage (Google Spanner)

**Schema:**
```sql
CREATE TABLE emails (
    user_id STRING(36) NOT NULL,
    email_id STRING(36) NOT NULL,
    thread_id STRING(36) NOT NULL,
    from_email STRING(255) NOT NULL,
    from_name STRING(255),
    subject STRING(1000),
    snippet STRING(500),
    size_bytes INT64,
    has_attachment BOOL DEFAULT FALSE,
    unread BOOL DEFAULT TRUE,
    received_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,

    PRIMARY KEY (user_id, email_id)
) INTERLEAVE IN PARENT users ON DELETE CASCADE;

CREATE INDEX idx_thread ON emails(user_id, thread_id, received_at DESC);
CREATE INDEX idx_received ON emails(user_id, received_at DESC);

CREATE TABLE email_labels (
    user_id STRING(36) NOT NULL,
    email_id STRING(36) NOT NULL,
    label STRING(50) NOT NULL,

    PRIMARY KEY (user_id, email_id, label),
    FOREIGN KEY (user_id, email_id) REFERENCES emails(user_id, email_id)
);

CREATE INDEX idx_label_time ON email_labels(user_id, label, received_at DESC);

CREATE TABLE threads (
    user_id STRING(36) NOT NULL,
    thread_id STRING(36) NOT NULL,
    subject STRING(1000),
    participants ARRAY<STRING(255)>,
    email_count INT64 DEFAULT 1,
    last_email_at TIMESTAMP,
    unread_count INT64 DEFAULT 0,

    PRIMARY KEY (user_id, thread_id)
);

CREATE TABLE attachments (
    attachment_id STRING(36) PRIMARY KEY,
    email_id STRING(36) NOT NULL,
    filename STRING(500) NOT NULL,
    content_type STRING(100),
    size_bytes INT64,
    storage_path STRING(1000), -- GCS path
    checksum STRING(64),

    FOREIGN KEY (email_id) REFERENCES emails(email_id)
);
```

### Attachment Storage (GCS/S3)

```
gs://gmail-attachments/
├── {user_id}/
│   └── {year}/
│       └── {month}/
│           └── {email_id}/
│               ├── attachment_1.pdf
│               └── attachment_2.jpg
```

## 8. Spam Filtering

### ML-Based Spam Detection

**Features:**
```python
def extract_spam_features(email):
    features = {
        # Sender features
        'sender_reputation': get_sender_reputation(email.from_email),
        'sender_in_contacts': is_in_contacts(email.from_email),
        'sender_domain_age': get_domain_age(email.from_email),
        
        # Content features
        'has_suspicious_keywords': check_keywords(email.subject + email.body),
        'capitalization_ratio': count_caps(email.subject) / len(email.subject),
        'url_count': count_urls(email.body),
        'external_link_count': count_external_links(email.body),
        
        # Technical features
        'spf_pass': email.spf_result == 'pass',
        'dkim_pass': email.dkim_result == 'pass',
        'has_attachment': email.has_attachment,
        
        # Behavioral features
        'sender_previous_spam_rate': get_spam_rate(email.from_email),
        'bulk_email': email.to_count > 50,
        
        # Text analysis
        'sentiment_score': analyze_sentiment(email.body),
        'language': detect_language(email.body)
    }
    
    return features
```

**Classification:**
```python
class SpamFilter:
    def __init__(self):
        self.model = load_model('spam_classifier_v5.pkl')
    
    def classify(self, email):
        features = extract_spam_features(email)
        
        # ML model prediction
        spam_probability = self.model.predict_proba([features])[0][1]
        
        # Thresholds
        if spam_probability > 0.9:
            return 'spam'
        elif spam_probability > 0.5:
            return 'suspicious'
        else:
            return 'legitimate'
    
    def apply_label(self, email, classification):
        if classification == 'spam':
            email.labels.add('spam')
            email.labels.remove('inbox')
        elif classification == 'suspicious':
            email.labels.add('possibly_spam')
```

### User Feedback Loop

```python
def user_marks_spam(email_id):
    # Update training data
    training_data.add({
        'email_id': email_id,
        'label': 'spam',
        'user_action': 'marked_spam'
    })
    
    # Retrain model periodically
    if training_data.size() > 10000:
        retrain_spam_model()

def retrain_spam_model():
    # Batch job (daily)
    X = training_data.get_features()
    y = training_data.get_labels()
    
    model = GradientBoostingClassifier()
    model.fit(X, y)
    
    deploy_model(model, version='v6')
```

## 9. Search Implementation

### Elasticsearch Indexing

**Index Structure:**
```json
{
  "mappings": {
    "properties": {
      "user_id": {"type": "keyword"},
      "email_id": {"type": "keyword"},
      "from": {"type": "keyword"},
      "to": {"type": "keyword"},
      "subject": {
        "type": "text",
        "analyzer": "standard",
        "fields": {"keyword": {"type": "keyword"}}
      },
      "body": {
        "type": "text",
        "analyzer": "standard"
      },
      "labels": {"type": "keyword"},
      "has_attachment": {"type": "boolean"},
      "received_at": {"type": "date"},
      "attachments": {
        "type": "nested",
        "properties": {
          "filename": {"type": "text"},
          "content": {"type": "text"}  // Extracted text
        }
      }
    }
  }
}
```

**Indexing Pipeline:**
```python
def index_email(email):
    # Extract attachment content
    attachment_content = []
    for attachment in email.attachments:
        if attachment.content_type == 'application/pdf':
            text = extract_pdf_text(attachment)
            attachment_content.append({
                'filename': attachment.filename,
                'content': text
            })
    
    # Index document
    es_doc = {
        'user_id': email.user_id,
        'email_id': email.email_id,
        'from': email.from_email,
        'to': email.to_emails,
        'subject': email.subject,
        'body': email.body_text,
        'labels': email.labels,
        'has_attachment': len(email.attachments) > 0,
        'received_at': email.received_at,
        'attachments': attachment_content
    }
    
    es.index(
        index=f'emails_{email.user_id % 10}',  # Sharded by user
        id=email.email_id,
        document=es_doc
    )
```

**Search Query:**
```python
def search_emails(user_id, query, filters):
    es_query = {
        "bool": {
            "must": [
                {"term": {"user_id": user_id}},
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "subject^3",  # Boost subject matches
                            "body",
                            "from",
                            "attachments.content"
                        ],
                        "type": "best_fields"
                    }
                }
            ],
            "filter": []
        }
    }
    
    # Add filters
    if filters.get('from'):
        es_query["bool"]["filter"].append(
            {"term": {"from": filters['from']}}
        )
    
    if filters.get('has_attachment'):
        es_query["bool"]["filter"].append(
            {"term": {"has_attachment": True}}
        )
    
    if filters.get('after_date'):
        es_query["bool"]["filter"].append(
            {"range": {"received_at": {"gte": filters['after_date']}}}
        )
    
    results = es.search(
        index=f'emails_{user_id % 10}',
        query=es_query,
        size=50,
        sort=[{"received_at": "desc"}]
    )
    
    return results['hits']['hits']
```

## 10. Threading & Conversations

### Email Threading Algorithm

```python
class EmailThreading:
    def find_or_create_thread(self, email):
        # Check if reply (has In-Reply-To header)
        if email.in_reply_to:
            parent_email = self.get_email(email.in_reply_to)
            if parent_email:
                return parent_email.thread_id
        
        # Check if References header matches existing thread
        if email.references:
            for ref_id in email.references:
                ref_email = self.get_email(ref_id)
                if ref_email:
                    return ref_email.thread_id
        
        # Subject-based matching (fuzzy)
        normalized_subject = self.normalize_subject(email.subject)
        
        # Search recent threads with similar subject
        recent_threads = self.db.query("""
            SELECT thread_id FROM threads
            WHERE user_id = ?
            AND normalized_subject = ?
            AND last_email_at > ?
            LIMIT 1
        """, (email.user_id, normalized_subject, now() - timedelta(days=7)))
        
        if recent_threads:
            return recent_threads[0].thread_id
        
        # Create new thread
        return self.create_thread(email)
    
    def normalize_subject(self, subject):
        # Remove Re:, Fwd:, etc.
        subject = re.sub(r'^(Re|Fwd|RE|FW):\s*', '', subject, flags=re.IGNORECASE)
        subject = subject.strip().lower()
        return subject
```

### Thread View

```python
def get_thread(thread_id, user_id):
    # Get all emails in thread
    emails = db.query("""
        SELECT * FROM emails
        WHERE user_id = ? AND thread_id = ?
        ORDER BY received_at ASC
    """, (user_id, thread_id))
    
    # Build conversation structure
    thread = {
        'thread_id': thread_id,
        'subject': emails[0].subject,
        'participants': set(),
        'emails': []
    }
    
    for email in emails:
        thread['participants'].add(email.from_email)
        thread['participants'].update(email.to_emails)
        thread['emails'].append(email)
    
    return thread
```

## 11. Scalability & Performance

### Database Sharding

**User-based Sharding:**
```
Shard by user_id hash:
- Shard 0: user_id % 100 == 0-9
- Shard 1: user_id % 100 == 10-19
- ...
- Shard 9: user_id % 100 == 90-99

Benefits:
- User's emails co-located
- Inbox queries hit single shard
- Linear scalability
```

### Caching Strategy

```python
# Redis cache for hot data
class EmailCache:
    def get_inbox(self, user_id, page=1):
        cache_key = f"inbox:{user_id}:page:{page}"
        cached = redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # Cache miss
        emails = db.query_inbox(user_id, page)
        redis.setex(cache_key, 300, json.dumps(emails))  # 5 min TTL
        
        return emails
    
    def invalidate_inbox(self, user_id):
        # Invalidate all inbox pages
        pattern = f"inbox:{user_id}:*"
        keys = redis.keys(pattern)
        redis.delete(*keys)
```

### Connection Pooling

```python
# Database connection pool
db_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=10,
    maxconn=100,
    host='db.gmail.com',
    database='gmail'
)

# Elasticsearch connection pool
es = Elasticsearch(
    ['es1.gmail.com', 'es2.gmail.com'],
    max_retries=3,
    timeout=10
)
```

## 12. Real-Time Notifications

### WebSocket Push

```python
class PushNotificationService:
    def __init__(self):
        self.connections = {}  # user_id → WebSocket connection
        self.kafka_consumer = KafkaConsumer('email_events')
    
    async def handle_connection(self, websocket, user_id):
        # Store connection
        self.connections[user_id] = websocket
        
        try:
            # Keep connection alive
            await websocket.wait_closed()
        finally:
            del self.connections[user_id]
    
    async def consume_events(self):
        async for message in self.kafka_consumer:
            event = json.loads(message.value)
            
            if event['type'] == 'new_email':
                user_id = event['user_id']
                
                # Check if user connected
                if user_id in self.connections:
                    ws = self.connections[user_id]
                    await ws.send(json.dumps({
                        'type': 'new_email',
                        'email_id': event['email_id'],
                        'from': event['from'],
                        'subject': event['subject'],
                        'snippet': event['snippet']
                    }))
```

### Mobile Push Notifications

```python
def send_mobile_push(user_id, email):
    # Get user's device tokens
    devices = db.get_user_devices(user_id)
    
    for device in devices:
        if device.platform == 'ios':
            apns.send(
                device_token=device.token,
                payload={
                    'aps': {
                        'alert': {
                            'title': email.from_name,
                            'body': email.snippet
                        },
                        'badge': get_unread_count(user_id),
                        'sound': 'default'
                    },
                    'email_id': email.email_id
                }
            )
        elif device.platform == 'android':
            fcm.send(
                device_token=device.token,
                notification={
                    'title': email.from_name,
                    'body': email.snippet
                },
                data={
                    'email_id': email.email_id
                }
            )
```

## 13. Security & Privacy

### Encryption

**At Rest:**
```python
def encrypt_email_body(body, user_key):
    # Per-user encryption key
    cipher = AES.new(user_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(body.encode())
    
    return {
        'ciphertext': base64.b64encode(ciphertext),
        'nonce': base64.b64encode(cipher.nonce),
        'tag': base64.b64encode(tag)
    }
```

**In Transit:**
- TLS 1.3 for all connections
- STARTTLS for SMTP

### Authentication

```python
# OAuth 2.0
def authenticate_user(access_token):
    # Verify JWT token
    payload = jwt.decode(
        access_token,
        public_key,
        algorithms=['RS256']
    )
    
    user_id = payload['sub']
    scopes = payload['scope']
    
    return user_id, scopes
```

### Rate Limiting

```python
def check_send_quota(user_id):
    # Daily send limit: 500 emails
    today_count = redis.get(f"send_count:{user_id}:{date.today()}")
    
    if today_count and int(today_count) >= 500:
        raise QuotaExceeded("Daily send limit reached")
    
    redis.incr(f"send_count:{user_id}:{date.today()}")
    redis.expire(f"send_count:{user_id}:{date.today()}", 86400)
```

## 14. Trade-offs

### Consistency vs. Latency

**Strong Consistency:**
- ✅ Always latest data
- ❌ Higher latency

**Eventual Consistency:**
- ✅ Lower latency
- ❌ Brief inconsistency

**Decision:** Eventual (acceptable for email)

### Storage: Normalized vs. Denormalized

**Normalized:**
- ✅ No duplication
- ❌ More joins

**Denormalized:**
- ✅ Faster reads
- ❌ Storage overhead

**Decision:** Denormalize for performance

## 15. Follow-up Questions

1. **How do you handle email recalls?**
   - Mark as recalled in metadata
   - Can't recall if already read
   - Replace with "This email was recalled"

2. **How would you implement vacation auto-reply?**
   - Store auto-reply rule in user settings
   - Check on inbound email
   - Send auto-reply (once per sender per day)
   - Track sent auto-replies to avoid duplicates

3. **How do you detect phishing emails?**
   - ML model similar to spam filter
   - Check: URL mismatch, sender spoofing
   - Warn user with banner

4. **How would you implement email forwarding?**
   - Store forwarding rule: forward_to address
   - On receive, duplicate email to forward_to
   - Preserve original sender

5. **How do you handle attachments > 25 MB?**
   - Reject at upload
   - Or: Use Google Drive link instead

## Complexity Analysis

- **Time Complexity:**
  - Send: O(1) for write, O(n) for n recipients
  - Inbox load: O(k) where k = page size
  - Search: O(log n) with indexing

- **Space Complexity:**
  - Total: O(u × e × s) where u = users, e = emails/user, s = size
  - Indexes: O(u × e × i) where i = index size

## References

- [Gmail Architecture](https://www.youtube.com/watch?v=oRYGUGp6T2I)
- [SMTP Protocol](https://tools.ietf.org/html/rfc5321)
- [Email Threading](https://www.jwz.org/doc/threading.html)
- [Spam Detection](https://research.google/pubs/pub37368/)
