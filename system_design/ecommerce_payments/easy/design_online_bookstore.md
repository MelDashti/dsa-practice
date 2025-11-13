# Design Online Bookstore

## 1. Problem Statement

Design a basic online bookstore that allows users to browse books, add them to a shopping cart, and complete purchases. The system should handle user authentication, product catalog management, shopping cart functionality, and basic order processing.

**Key Features:**
- Browse and search books
- User registration and authentication
- Shopping cart management
- Order placement and checkout
- Basic payment processing
- Order history

## 2. Requirements

### Functional Requirements

1. **User Management**
   - User registration and login
   - Profile management
   - Password reset functionality

2. **Product Catalog**
   - Browse books by category
   - Search books by title, author, ISBN
   - View book details (title, author, description, price, stock)
   - Filter and sort results

3. **Shopping Cart**
   - Add/remove items to cart
   - Update quantities
   - View cart total
   - Cart persistence across sessions

4. **Order Management**
   - Checkout process
   - Order confirmation
   - View order history
   - Order status tracking

5. **Payment Processing**
   - Support multiple payment methods
   - Payment confirmation
   - Invoice generation

### Non-Functional Requirements

1. **Performance**
   - Page load time < 2 seconds
   - Search results < 1 second
   - Support 1000 concurrent users

2. **Availability**
   - 99.9% uptime
   - Graceful degradation during peak times

3. **Security**
   - Encrypted password storage
   - Secure payment processing (PCI DSS compliance)
   - HTTPS for all transactions
   - Protection against SQL injection, XSS

4. **Scalability**
   - Handle growing product catalog (100K+ books)
   - Support seasonal traffic spikes

5. **Usability**
   - Intuitive user interface
   - Mobile-responsive design

## 3. Scale Estimation

### Traffic Estimates
- **Daily Active Users (DAU):** 10,000
- **Monthly Active Users (MAU):** 50,000
- **Peak hours:** 2x average traffic
- **Concurrent users:** 1,000

### Transaction Estimates
- **Conversion rate:** 5%
- **Daily orders:** 500
- **Average cart value:** $50
- **Daily revenue:** $25,000

### Storage Estimates
- **Books catalog:** 100,000 books
  - Average metadata: 2 KB per book
  - Total: 200 MB
- **Images:** 100,000 books × 3 images × 100 KB = 30 GB
- **Users:** 50,000 users × 1 KB = 50 MB
- **Orders:** 500 orders/day × 365 days × 5 KB = 912 MB/year
- **Total storage (Year 1):** ~35 GB

### Bandwidth Estimates
- **Reads:** 10,000 users × 20 pages × 500 KB = 100 GB/day
- **Writes:** 500 orders × 10 KB = 5 MB/day
- **Read-heavy:** 99.9% reads, 0.1% writes

## 4. High-Level Architecture

```
┌─────────────┐
│   Client    │ (Web Browser / Mobile App)
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────┐
│      Load Balancer (NGINX)          │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│ Web Server  │  │ Web Server  │
│   (Node.js) │  │   (Node.js) │
└──────┬──────┘  └──────┬──────┘
       │                │
       └────────┬───────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌─────────┐
│  Auth  │ │Product │ │  Order  │
│Service │ │Service │ │ Service │
└───┬────┘ └───┬────┘ └────┬────┘
    │          │           │
    └──────────┼───────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌──────────────┐
│   Primary   │  │    Cache     │
│  Database   │  │    (Redis)   │
│  (PostgreSQL)│ │              │
└─────────────┘  └──────────────┘
       │
       ▼
┌─────────────┐
│   Replica   │
│  Database   │
└─────────────┘

External Services:
┌──────────────┐  ┌──────────────┐
│   Payment    │  │     Email    │
│   Gateway    │  │   Service    │
│  (Stripe)    │  │  (SendGrid)  │
└──────────────┘  └──────────────┘
```

**Components:**
- **Load Balancer:** Distributes traffic across web servers
- **Web Servers:** Handle HTTP requests, business logic
- **Services:** Microservices for different domains
- **Cache:** Redis for session data and frequently accessed data
- **Database:** PostgreSQL for persistent storage with read replicas
- **CDN:** Serve static assets (images, CSS, JS)
- **External Services:** Payment gateway, email notifications

## 5. API Design

### User APIs

```
POST /api/v1/auth/register
Request:
{
  "email": "user@example.com",
  "password": "hashedPassword",
  "name": "John Doe",
  "phone": "+1234567890"
}
Response: 201 Created
{
  "userId": "uuid",
  "token": "jwt_token"
}

POST /api/v1/auth/login
Request:
{
  "email": "user@example.com",
  "password": "password"
}
Response: 200 OK
{
  "userId": "uuid",
  "token": "jwt_token",
  "expiresIn": 3600
}

GET /api/v1/users/{userId}
Response: 200 OK
{
  "userId": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "createdAt": "2025-01-01T00:00:00Z"
}
```

### Product APIs

```
GET /api/v1/books?page=1&limit=20&category=fiction&sort=price_asc
Response: 200 OK
{
  "books": [
    {
      "bookId": "uuid",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0-7432-7356-5",
      "price": 14.99,
      "stock": 50,
      "category": "fiction",
      "imageUrl": "https://cdn.example.com/images/book1.jpg",
      "description": "..."
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}

GET /api/v1/books/{bookId}
Response: 200 OK
{
  "bookId": "uuid",
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "978-0-7432-7356-5",
  "price": 14.99,
  "stock": 50,
  "category": "fiction",
  "description": "A classic American novel...",
  "publisher": "Scribner",
  "publishedDate": "2004-09-30",
  "pages": 180,
  "language": "English",
  "images": ["url1", "url2", "url3"]
}

GET /api/v1/books/search?q=gatsby&page=1&limit=20
Response: 200 OK (same as GET /books with filtered results)
```

### Cart APIs

```
POST /api/v1/cart/items
Request:
{
  "bookId": "uuid",
  "quantity": 2
}
Response: 201 Created
{
  "cartId": "uuid",
  "items": [
    {
      "bookId": "uuid",
      "title": "The Great Gatsby",
      "price": 14.99,
      "quantity": 2,
      "subtotal": 29.98
    }
  ],
  "total": 29.98
}

GET /api/v1/cart
Response: 200 OK
{
  "cartId": "uuid",
  "userId": "uuid",
  "items": [...],
  "total": 29.98,
  "updatedAt": "2025-01-01T00:00:00Z"
}

PUT /api/v1/cart/items/{bookId}
Request:
{
  "quantity": 3
}
Response: 200 OK (updated cart)

DELETE /api/v1/cart/items/{bookId}
Response: 204 No Content
```

### Order APIs

```
POST /api/v1/orders
Request:
{
  "cartId": "uuid",
  "shippingAddress": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001",
    "country": "USA"
  },
  "paymentMethod": {
    "type": "credit_card",
    "token": "stripe_token"
  }
}
Response: 201 Created
{
  "orderId": "uuid",
  "orderNumber": "ORD-2025-00001",
  "status": "pending",
  "total": 29.98,
  "createdAt": "2025-01-01T00:00:00Z"
}

GET /api/v1/orders/{orderId}
Response: 200 OK
{
  "orderId": "uuid",
  "orderNumber": "ORD-2025-00001",
  "userId": "uuid",
  "status": "confirmed",
  "items": [...],
  "subtotal": 29.98,
  "tax": 2.40,
  "shipping": 5.00,
  "total": 37.38,
  "shippingAddress": {...},
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-01T00:05:00Z"
}

GET /api/v1/users/{userId}/orders?page=1&limit=10
Response: 200 OK
{
  "orders": [...],
  "pagination": {...}
}
```

## 6. Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);
```

### Books Table
```sql
CREATE TABLE books (
    book_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    isbn VARCHAR(13) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    category VARCHAR(100),
    publisher VARCHAR(255),
    published_date DATE,
    pages INT,
    language VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_isbn (isbn),
    INDEX idx_category (category),
    CONSTRAINT chk_price CHECK (price >= 0),
    CONSTRAINT chk_stock CHECK (stock_quantity >= 0)
);
```

### Book_Images Table
```sql
CREATE TABLE book_images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    display_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_book_id (book_id)
);
```

### Carts Table
```sql
CREATE TABLE carts (
    cart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id),
    INDEX idx_user_id (user_id)
);
```

### Cart_Items Table
```sql
CREATE TABLE cart_items (
    cart_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID NOT NULL REFERENCES carts(cart_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 1,
    price_at_addition DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, book_id),
    INDEX idx_cart_id (cart_id),
    CONSTRAINT chk_quantity CHECK (quantity > 0)
);
```

### Orders Table
```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(user_id),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    subtotal DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) NOT NULL DEFAULT 0,
    shipping_fee DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    shipping_address JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    CONSTRAINT chk_status CHECK (status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
    CONSTRAINT chk_payment_status CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded'))
);
```

### Order_Items Table
```sql
CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES books(book_id),
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    CONSTRAINT chk_quantity CHECK (quantity > 0)
);
```

### Payments Table
```sql
CREATE TABLE payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(order_id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_gateway VARCHAR(50),
    transaction_id VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_transaction_id (transaction_id),
    CONSTRAINT chk_status CHECK (status IN ('pending', 'completed', 'failed', 'refunded'))
);
```

### ACID Considerations

1. **Atomicity**
   - Order creation must be atomic: create order, create order items, process payment
   - Use database transactions to ensure all-or-nothing execution

2. **Consistency**
   - Foreign key constraints maintain referential integrity
   - Check constraints ensure valid data (price >= 0, quantity > 0)
   - Status enum constraints prevent invalid states

3. **Isolation**
   - Use appropriate isolation levels to prevent race conditions
   - SELECT FOR UPDATE when checking/updating stock
   - Serializable isolation for critical payment transactions

4. **Durability**
   - All committed transactions are persisted
   - Regular database backups
   - Write-ahead logging (WAL) in PostgreSQL

## 7. Core Components

### 7.1 Authentication Service
- **Responsibility:** User registration, login, JWT token generation
- **Key Functions:**
  - Password hashing (bcrypt)
  - JWT token generation and validation
  - Session management
  - Password reset functionality

### 7.2 Product Catalog Service
- **Responsibility:** Manage book inventory and search
- **Key Functions:**
  - CRUD operations for books
  - Search and filtering (Elasticsearch integration)
  - Category management
  - Stock tracking
- **Caching Strategy:**
  - Cache popular book details (TTL: 1 hour)
  - Cache search results (TTL: 15 minutes)
  - Cache-aside pattern

### 7.3 Shopping Cart Service
- **Responsibility:** Manage user shopping carts
- **Key Functions:**
  - Add/remove items
  - Update quantities
  - Calculate totals
  - Cart persistence
- **Implementation:**
  - Session-based carts (Redis)
  - Persistent carts (database) for logged-in users
  - Cart expiration (30 days of inactivity)

### 7.4 Order Management Service
- **Responsibility:** Handle order lifecycle
- **Key Functions:**
  - Order creation
  - Status tracking
  - Order history
  - Inventory reservation
- **Workflow:**
  1. Validate cart items and stock
  2. Create order record
  3. Process payment
  4. Update inventory
  5. Send confirmation email

### 7.5 Payment Service
- **Responsibility:** Process payments
- **Key Functions:**
  - Integration with payment gateway (Stripe)
  - Payment validation
  - Refund processing
  - Transaction logging
- **Security:**
  - Never store credit card details
  - Use payment gateway tokens
  - PCI DSS compliance

### 7.6 Inventory Management
- **Responsibility:** Track and manage stock
- **Key Functions:**
  - Stock updates
  - Low stock alerts
  - Inventory reservation during checkout
- **Concurrency Control:**
  - Optimistic locking with version numbers
  - Or pessimistic locking with SELECT FOR UPDATE

### 7.7 Notification Service
- **Responsibility:** Send email/SMS notifications
- **Key Functions:**
  - Order confirmation
  - Shipping updates
  - Payment receipts
  - Marketing emails
- **Implementation:**
  - Message queue (RabbitMQ) for async processing
  - Integration with email service (SendGrid)

## 8. Transaction Management & Consistency

### Order Creation Flow (Critical Transaction)

```sql
BEGIN TRANSACTION;

-- 1. Lock cart items
SELECT ci.book_id, ci.quantity, b.stock_quantity, b.price
FROM cart_items ci
JOIN books b ON ci.book_id = b.book_id
WHERE ci.cart_id = ?
FOR UPDATE;

-- 2. Validate stock availability
-- (Application logic checks if stock >= quantity for all items)

-- 3. Create order
INSERT INTO orders (order_number, user_id, status, subtotal, tax, shipping_fee, total, shipping_address)
VALUES (?, ?, 'pending', ?, ?, ?, ?, ?);

-- 4. Create order items
INSERT INTO order_items (order_id, book_id, quantity, price_at_purchase, subtotal)
SELECT ?, book_id, quantity, price, (quantity * price)
FROM cart_items
WHERE cart_id = ?;

-- 5. Update inventory (decrement stock)
UPDATE books b
SET stock_quantity = stock_quantity - ci.quantity,
    updated_at = CURRENT_TIMESTAMP
FROM cart_items ci
WHERE b.book_id = ci.book_id
  AND ci.cart_id = ?;

-- 6. Create payment record
INSERT INTO payments (order_id, amount, payment_method, status)
VALUES (?, ?, ?, 'pending');

-- 7. Clear cart
DELETE FROM cart_items WHERE cart_id = ?;

COMMIT;
```

### Handling Payment Processing

```
1. Create order with status='pending' and payment_status='pending'
2. Call payment gateway API (Stripe)
3. If payment succeeds:
   - Update payment_status='completed'
   - Update order status='confirmed'
   - Send confirmation email
4. If payment fails:
   - Update payment_status='failed'
   - Rollback inventory (add stock back)
   - Update order status='cancelled'
   - Notify user
```

### Idempotency

- Use idempotency keys for payment processing
- Prevent duplicate order creation
- Implement request deduplication (track request IDs)

### Eventual Consistency Trade-offs

- **Inventory counts:** May show slightly outdated stock (cached)
- **Order status:** Updates propagate within seconds
- **Search results:** May be eventually consistent (if using Elasticsearch)

## 9. Security Considerations

### Authentication & Authorization
- **Password Security:**
  - Bcrypt hashing with salt (cost factor: 12)
  - Minimum password requirements (8+ chars, uppercase, number, special char)
  - Rate limiting on login attempts
  - Account lockout after failed attempts

- **Session Management:**
  - JWT tokens with short expiration (1 hour)
  - Refresh tokens stored securely
  - Token revocation on logout
  - HTTPS-only cookies

### Data Protection
- **Encryption:**
  - TLS 1.3 for data in transit
  - Encrypt sensitive data at rest (PII)
  - Database encryption (PostgreSQL pgcrypto)

- **PCI DSS Compliance:**
  - Never store CVV/CVC
  - Never store full credit card numbers
  - Use payment gateway tokenization
  - Regular security audits

### Input Validation
- **SQL Injection Prevention:**
  - Parameterized queries
  - ORM usage (Sequelize, TypeORM)
  - Input sanitization

- **XSS Prevention:**
  - Output encoding
  - Content Security Policy headers
  - Sanitize user-generated content

### API Security
- **Rate Limiting:**
  - 100 requests/minute per user
  - 1000 requests/hour per IP
  - DDoS protection (Cloudflare)

- **CORS:**
  - Whitelist allowed origins
  - Restrict methods and headers

### Monitoring & Logging
- **Security Logging:**
  - Failed login attempts
  - Payment failures
  - Suspicious activities
  - Access logs

- **Monitoring:**
  - Real-time alerts for anomalies
  - Regular security scans
  - Penetration testing

## 10. Scalability

### Database Scalability

1. **Read Replicas:**
   - Master-slave replication
   - Route read queries to replicas
   - Route writes to master

2. **Indexing:**
   - B-tree indexes on frequently queried columns
   - Composite indexes for common query patterns
   - Regular index maintenance

3. **Partitioning:**
   - Partition orders table by date (monthly/yearly)
   - Archive old orders to cold storage

4. **Connection Pooling:**
   - PgBouncer for connection management
   - Limit connections per service

### Application Scalability

1. **Horizontal Scaling:**
   - Stateless web servers
   - Auto-scaling based on CPU/memory
   - Load balancer distributes traffic

2. **Caching Strategy:**
   - **Browser caching:** Static assets (1 year)
   - **CDN caching:** Images, CSS, JS
   - **Application caching:** Redis for sessions, popular books
   - **Database query caching**

3. **Async Processing:**
   - Message queues for emails, notifications
   - Background jobs for analytics
   - Separate worker processes

### Content Delivery

1. **CDN:**
   - CloudFront/Cloudflare for static assets
   - Image optimization and compression
   - Geographic distribution

2. **Image Optimization:**
   - Multiple sizes/formats (WebP, JPEG)
   - Lazy loading
   - Responsive images

### Microservices Benefits

- Independent scaling of services
- Technology flexibility
- Fault isolation
- Team autonomy

## 11. Trade-offs

### 1. Consistency vs Availability
- **Choice:** Eventual consistency for non-critical data
- **Trade-off:** Stock counts may be slightly outdated in cache
- **Benefit:** Better performance and availability
- **Mitigation:** TTL on cache, validation during checkout

### 2. Monolith vs Microservices
- **Choice:** Start with modular monolith
- **Trade-off:** Less operational complexity initially
- **Benefit:** Faster development, easier deployment
- **Future:** Migrate to microservices as needed

### 3. SQL vs NoSQL
- **Choice:** PostgreSQL (SQL)
- **Benefit:** ACID guarantees, complex queries, relationships
- **Trade-off:** Harder to scale horizontally
- **Mitigation:** Read replicas, partitioning

### 4. Strong vs Eventual Consistency
- **Critical paths (orders, payments):** Strong consistency
- **Non-critical (product views, reviews):** Eventual consistency
- **Benefit:** Balance between performance and accuracy

### 5. Synchronous vs Asynchronous Processing
- **Synchronous:** Order creation, payment processing
- **Asynchronous:** Email notifications, analytics
- **Benefit:** Fast user experience, better resource utilization

### 6. Caching Trade-offs
- **Aggressive caching:** Better performance
- **Trade-off:** Stale data risk
- **Mitigation:** Appropriate TTLs, cache invalidation strategies

## 12. Follow-up Questions

### Functional Enhancements
1. How would you implement a recommendation engine?
2. How would you add wishlist functionality?
3. How would you implement book reviews and ratings?
4. How would you add discount codes and promotions?
5. How would you implement gift cards?

### Scalability
6. How would you scale to 1 million concurrent users?
7. How would you handle Black Friday traffic (10x normal)?
8. How would you implement global availability (multi-region)?
9. How would you shard the database if it becomes too large?
10. How would you implement real-time inventory updates?

### Features
11. How would you add subscription service (monthly book box)?
12. How would you implement digital book delivery (ebooks)?
13. How would you add marketplace functionality (third-party sellers)?
14. How would you implement pre-orders for upcoming books?
15. How would you add book rental functionality?

### Technical
16. How would you migrate from monolith to microservices?
17. How would you implement full-text search with relevance ranking?
18. How would you handle multi-currency support?
19. How would you implement fraud detection?
20. How would you ensure zero-downtime deployments?

### Business Logic
21. How would you handle returns and refunds?
22. How would you implement dynamic pricing?
23. How would you track inventory across multiple warehouses?
24. How would you implement order tracking and shipping integration?
25. How would you handle taxes for different jurisdictions?

---

**Key Takeaways:**
- Start simple with core functionality
- Focus on ACID properties for transactions
- Plan for scalability from the beginning
- Security is critical for e-commerce
- Choose appropriate trade-offs based on business requirements
