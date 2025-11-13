# Design Amazon

## 1. Problem Statement

Design a large-scale e-commerce platform like Amazon that handles millions of products, thousands of sellers, personalized recommendations, and membership programs (Prime). The system must support high traffic, real-time inventory management, product search, reviews, and order fulfillment across multiple warehouses.

**Key Features:**
- Multi-vendor marketplace
- Product catalog with millions of SKUs
- Advanced search and filters
- Personalized recommendations
- Shopping cart and wishlist
- Order management and tracking
- Prime membership (fast delivery, video streaming)
- Reviews and ratings
- Seller dashboard
- Inventory management across warehouses

## 2. Requirements

### Functional Requirements

1. **User Management**
   - User registration and authentication
   - Multiple user roles (buyer, seller, admin)
   - Profile management
   - Address book
   - Prime membership management

2. **Product Catalog**
   - Browse products by category/department
   - Advanced search with filters (price, rating, brand, etc.)
   - Product details (images, description, specifications, variants)
   - Product variations (size, color, etc.)
   - Seller information

3. **Search & Discovery**
   - Full-text search with autocomplete
   - Faceted search/filtering
   - Search ranking (relevance, popularity, price)
   - Personalized product recommendations
   - "Customers who bought this also bought"

4. **Shopping Experience**
   - Add to cart / Add to wishlist
   - Save for later
   - Quantity updates
   - Cart synchronization across devices
   - Guest checkout

5. **Order Management**
   - Multi-address checkout
   - Multiple payment methods
   - Order tracking
   - Order history
   - Cancel/return/refund
   - Invoice generation

6. **Prime Membership**
   - Subscription management
   - Fast delivery options
   - Access to Prime Video/Music
   - Prime-exclusive deals

7. **Seller Platform**
   - Product listing
   - Inventory management
   - Order fulfillment
   - Analytics dashboard
   - Payment/settlement

8. **Reviews & Ratings**
   - Product reviews
   - Review ratings (helpful/not helpful)
   - Verified purchase badge
   - Review moderation

### Non-Functional Requirements

1. **Performance**
   - Search results < 200ms (p99)
   - Page load time < 1 second
   - API response time < 100ms (p95)
   - Support 10M+ concurrent users

2. **Availability**
   - 99.99% uptime (4 nines)
   - No single point of failure
   - Graceful degradation
   - Multi-region deployment

3. **Scalability**
   - Handle 100M+ products
   - 1M+ sellers
   - 100K+ orders per minute
   - Black Friday traffic spikes (10-20x)

4. **Consistency**
   - Strong consistency for inventory and orders
   - Eventual consistency for product catalog updates
   - Eventual consistency for recommendations

5. **Security**
   - PCI DSS compliance
   - Data encryption (at rest and in transit)
   - DDoS protection
   - Fraud detection

6. **Reliability**
   - Data durability 99.999999999% (11 nines)
   - Automated backups
   - Disaster recovery (RPO < 1 hour, RTO < 4 hours)

## 3. Scale Estimation

### Traffic Estimates
- **Daily Active Users (DAU):** 50 million
- **Monthly Active Users (MAU):** 200 million
- **Concurrent users:** 10 million (peak)
- **Requests per second (RPS):** 500K (peak: 5M)

### Transaction Estimates
- **Products viewed per day:** 500 million
- **Searches per day:** 100 million
- **Orders per day:** 5 million
- **Average cart value:** $100
- **Daily GMV:** $500 million

### Storage Estimates
- **Products:** 100M products
  - Metadata: 10 KB per product = 1 TB
  - Images: 100M × 5 images × 200 KB = 100 TB
- **Users:** 200M users × 2 KB = 400 GB
- **Orders:** 5M orders/day × 365 days × 10 KB = 18 TB/year
- **Reviews:** 100M reviews × 1 KB = 100 GB
- **Total storage (Year 1):** ~120 TB

### Bandwidth Estimates
- **Incoming:** 5M orders × 100 KB = 500 GB/day
- **Outgoing:**
  - Product pages: 500M × 500 KB = 250 TB/day
  - Images (CDN): 2 billion requests × 200 KB = 400 TB/day
- **Total:** ~650 TB/day

### Cache Estimates
- **Hot products:** 1M products × 10 KB = 10 GB
- **Search results:** 100M searches × 5 KB = 500 GB
- **User sessions:** 10M users × 10 KB = 100 GB
- **Total cache:** ~610 GB

## 4. High-Level Architecture

```
                                    ┌──────────────┐
                                    │    Client    │
                                    │ (Web/Mobile) │
                                    └──────┬───────┘
                                           │
                                    ┌──────▼───────┐
                                    │     CDN      │
                                    │ (CloudFront) │
                                    └──────┬───────┘
                                           │
                                    ┌──────▼───────┐
                                    │     API      │
                                    │   Gateway    │
                                    └──────┬───────┘
                                           │
        ┌──────────────────────────────────┼────────────────────────────────┐
        │                                  │                                │
        ▼                                  ▼                                ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│    Product    │              │     Order     │              │     User      │
│   Service     │              │   Service     │              │   Service     │
└───────┬───────┘              └───────┬───────┘              └───────┬───────┘
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│   Inventory   │              │   Payment     │              │     Auth      │
│   Service     │              │   Service     │              │   Service     │
└───────┬───────┘              └───────┬───────┘              └───────┬───────┘
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│    Search     │              │  Shipping     │              │     Prime     │
│   Service     │              │   Service     │              │   Service     │
│(Elasticsearch)│              └───────────────┘              └───────────────┘
└───────┬───────┘
        │
        ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│Recommendation │              │    Review     │              │    Seller     │
│   Service     │              │   Service     │              │   Service     │
│  (ML Model)   │              └───────────────┘              └───────────────┘
└───────────────┘

                        Data Layer
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │PostgreSQL│  │PostgreSQL│  │PostgreSQL│  │  Redis   │         │
│  │ (Users)  │  │(Products)│  │ (Orders) │  │ (Cache)  │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
│                                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Cassandra │  │   S3     │  │   SQS    │  │  Kafka   │         │
│  │(Reviews) │  │ (Images) │  │ (Queue)  │  │(EventBus)│         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────────────────────────────────────────────────────┘

                    External Services
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Stripe  │  │  Email   │  │   SMS    │  │ Analytics│
│ Payment  │  │ Service  │  │ Service  │  │(DataDog) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 5. API Design

### Product APIs

```
GET /api/v1/products?category={category}&page={page}&limit={limit}&sort={sort}
Response: 200 OK
{
  "products": [
    {
      "productId": "uuid",
      "title": "iPhone 15 Pro",
      "brand": "Apple",
      "price": 999.99,
      "rating": 4.5,
      "reviewCount": 1234,
      "thumbnail": "url",
      "primeEligible": true,
      "inStock": true
    }
  ],
  "pagination": {...},
  "filters": {
    "brands": ["Apple", "Samsung"],
    "priceRanges": [...],
    "ratings": [...]
  }
}

GET /api/v1/products/{productId}
Response: 200 OK
{
  "productId": "uuid",
  "title": "iPhone 15 Pro",
  "description": "...",
  "brand": "Apple",
  "category": "Electronics > Phones",
  "price": 999.99,
  "listPrice": 1099.99,
  "discount": 9,
  "variants": [
    {
      "variantId": "uuid",
      "attributes": {"color": "Natural Titanium", "storage": "256GB"},
      "price": 999.99,
      "sku": "IPHONE15-PRO-256-TI",
      "stock": 50
    }
  ],
  "images": ["url1", "url2"],
  "specifications": {...},
  "seller": {
    "sellerId": "uuid",
    "name": "Amazon",
    "rating": 4.8
  },
  "shipping": {
    "primeDelivery": "Tomorrow",
    "standardDelivery": "3-5 days",
    "freeShipping": true
  },
  "rating": 4.5,
  "reviewCount": 1234
}

POST /api/v1/products (Seller only)
Request:
{
  "title": "Product Name",
  "description": "...",
  "category": "categoryId",
  "brand": "Brand Name",
  "price": 99.99,
  "variants": [...],
  "images": ["base64..."],
  "specifications": {...}
}
Response: 201 Created
```

### Search API

```
GET /api/v1/search?q={query}&filters={filters}&page={page}
Request: GET /api/v1/search?q=laptop&filters=brand:Dell,price:500-1000&page=1

Response: 200 OK
{
  "query": "laptop",
  "results": [
    {
      "productId": "uuid",
      "title": "Dell XPS 13",
      "price": 899.99,
      "rating": 4.6,
      "thumbnail": "url",
      "sponsored": false
    }
  ],
  "facets": {
    "brands": [
      {"name": "Dell", "count": 234},
      {"name": "HP", "count": 189}
    ],
    "priceRanges": [
      {"range": "0-500", "count": 45},
      {"range": "500-1000", "count": 123}
    ],
    "ratings": [...]
  },
  "suggestions": ["laptop bag", "laptop stand"],
  "totalResults": 1234,
  "page": 1
}

GET /api/v1/search/autocomplete?q={partial_query}
Response: 200 OK
{
  "suggestions": [
    "iphone 15",
    "iphone 15 pro",
    "iphone 15 case"
  ]
}
```

### Cart APIs

```
POST /api/v1/cart/items
Request:
{
  "productId": "uuid",
  "variantId": "uuid",
  "quantity": 2
}
Response: 201 Created

GET /api/v1/cart
Response: 200 OK
{
  "cartId": "uuid",
  "items": [
    {
      "cartItemId": "uuid",
      "product": {...},
      "variant": {...},
      "quantity": 2,
      "price": 999.99,
      "subtotal": 1999.98,
      "available": true
    }
  ],
  "subtotal": 1999.98,
  "tax": 159.99,
  "shipping": 0,
  "total": 2159.97,
  "savings": 100.00
}

PUT /api/v1/cart/items/{itemId}
DELETE /api/v1/cart/items/{itemId}
```

### Order APIs

```
POST /api/v1/orders
Request:
{
  "items": [
    {
      "productId": "uuid",
      "variantId": "uuid",
      "quantity": 1
    }
  ],
  "shippingAddress": {
    "addressId": "uuid"  // or full address object
  },
  "paymentMethod": {
    "type": "credit_card",
    "token": "pm_xxx"
  },
  "deliverySpeed": "prime_next_day"
}
Response: 201 Created
{
  "orderId": "uuid",
  "orderNumber": "112-1234567-1234567",
  "status": "confirmed",
  "estimatedDelivery": "2025-11-13",
  "total": 2159.97
}

GET /api/v1/orders/{orderId}
GET /api/v1/users/{userId}/orders

POST /api/v1/orders/{orderId}/cancel
POST /api/v1/orders/{orderId}/return
```

### Recommendation API

```
GET /api/v1/recommendations/for-you?userId={userId}
Response: 200 OK
{
  "recommendations": [
    {
      "productId": "uuid",
      "title": "...",
      "reason": "Based on your recent purchases",
      "score": 0.95
    }
  ]
}

GET /api/v1/products/{productId}/related
Response: Products frequently bought together
```

### Prime API

```
GET /api/v1/prime/membership
POST /api/v1/prime/subscribe
POST /api/v1/prime/cancel
```

### Review APIs

```
POST /api/v1/products/{productId}/reviews
Request:
{
  "rating": 5,
  "title": "Great product!",
  "comment": "...",
  "images": ["url1"]
}

GET /api/v1/products/{productId}/reviews?page=1&sort=helpful

POST /api/v1/reviews/{reviewId}/helpful
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
    user_type VARCHAR(20) DEFAULT 'customer', -- customer, seller, admin
    prime_member BOOLEAN DEFAULT FALSE,
    prime_expiry TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_user_type (user_type)
);
```

### Addresses Table
```sql
CREATE TABLE addresses (
    address_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    address_type VARCHAR(20), -- home, work, other
    street VARCHAR(500) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
);
```

### Categories Table
```sql
CREATE TABLE categories (
    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    parent_category_id UUID REFERENCES categories(category_id),
    path VARCHAR(1000), -- e.g., "/Electronics/Computers/Laptops"
    level INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_parent (parent_category_id),
    INDEX idx_path (path)
);
```

### Products Table
```sql
CREATE TABLE products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    seller_id UUID NOT NULL REFERENCES users(user_id),
    category_id UUID NOT NULL REFERENCES categories(category_id),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    brand VARCHAR(255),
    base_price DECIMAL(10, 2) NOT NULL,
    list_price DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'active', -- active, inactive, out_of_stock
    prime_eligible BOOLEAN DEFAULT FALSE,
    average_rating DECIMAL(3, 2) DEFAULT 0,
    review_count INT DEFAULT 0,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_seller (seller_id),
    INDEX idx_category (category_id),
    INDEX idx_brand (brand),
    INDEX idx_status (status),
    INDEX idx_rating (average_rating),
    FULLTEXT idx_search (title, description, brand)
);
```

### Product_Variants Table
```sql
CREATE TABLE product_variants (
    variant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    sku VARCHAR(100) UNIQUE NOT NULL,
    attributes JSONB NOT NULL, -- {"color": "Red", "size": "Large"}
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    warehouse_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product (product_id),
    INDEX idx_sku (sku),
    CONSTRAINT chk_stock CHECK (stock_quantity >= 0)
);
```

### Inventory_Transactions Table (for audit)
```sql
CREATE TABLE inventory_transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(variant_id),
    quantity_change INT NOT NULL,
    transaction_type VARCHAR(50), -- purchase, return, adjustment, sale
    reference_id UUID, -- order_id or other reference
    previous_quantity INT NOT NULL,
    new_quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_variant (variant_id),
    INDEX idx_created_at (created_at)
);
```

### Carts Table
```sql
CREATE TABLE carts (
    cart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    session_id VARCHAR(255), -- for guest users
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_session (session_id)
);
```

### Cart_Items Table
```sql
CREATE TABLE cart_items (
    cart_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID NOT NULL REFERENCES carts(cart_id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(product_id),
    variant_id UUID NOT NULL REFERENCES product_variants(variant_id),
    quantity INT NOT NULL DEFAULT 1,
    price_at_addition DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, variant_id),
    INDEX idx_cart (cart_id),
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
    tax DECIMAL(10, 2) NOT NULL,
    shipping_fee DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    shipping_address JSONB NOT NULL,
    delivery_speed VARCHAR(50), -- standard, prime_2day, prime_next_day
    estimated_delivery DATE,
    actual_delivery TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_order_number (order_number)
);
```

### Order_Items Table
```sql
CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(product_id),
    variant_id UUID NOT NULL REFERENCES product_variants(variant_id),
    seller_id UUID NOT NULL REFERENCES users(user_id),
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, shipped, delivered, returned
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (order_id),
    INDEX idx_seller (seller_id)
);
```

### Reviews Table (Cassandra - optimized for writes)
```
CREATE TABLE reviews (
    review_id UUID,
    product_id UUID,
    user_id UUID,
    order_id UUID,
    rating INT,
    title TEXT,
    comment TEXT,
    verified_purchase BOOLEAN,
    helpful_count INT,
    images LIST<TEXT>,
    created_at TIMESTAMP,
    PRIMARY KEY (product_id, created_at, review_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

// Secondary index for user reviews
CREATE TABLE reviews_by_user (
    user_id UUID,
    review_id UUID,
    product_id UUID,
    rating INT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at, review_id)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

### Prime_Subscriptions Table
```sql
CREATE TABLE prime_subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    plan_type VARCHAR(50), -- monthly, annual
    status VARCHAR(50) DEFAULT 'active',
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    payment_method_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_status (status)
);
```

### ACID Considerations

1. **Order Placement Transaction:**
   - Must be atomic: validate stock, create order, deduct inventory, process payment
   - Use SERIALIZABLE isolation level
   - Implement retry logic with exponential backoff

2. **Inventory Management:**
   - Optimistic locking with version numbers
   - Prevent overselling with CHECK constraints
   - Audit trail with inventory_transactions table

3. **Payment Processing:**
   - Two-phase commit pattern
   - Idempotency keys to prevent duplicate charges
   - Rollback inventory on payment failure

4. **Distributed Transactions:**
   - Use Saga pattern for cross-service transactions
   - Compensating transactions for failures
   - Event sourcing for audit trail

## 7. Core Components

### 7.1 Product Catalog Service
**Responsibilities:**
- Manage product CRUD operations
- Handle product variants and attributes
- Category management
- Product images (S3 integration)

**Key Features:**
- Product versioning
- Bulk upload for sellers
- Product approval workflow
- Image optimization

**Data Store:**
- PostgreSQL for product metadata
- S3 for images
- Elasticsearch for search

### 7.2 Search Service
**Technology:** Elasticsearch

**Features:**
- Full-text search
- Autocomplete/typeahead
- Faceted search
- Search ranking (relevance, popularity, price)
- Search analytics

**Indexing Strategy:**
```json
{
  "mappings": {
    "properties": {
      "productId": {"type": "keyword"},
      "title": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {"type": "keyword"},
          "suggest": {"type": "completion"}
        }
      },
      "brand": {"type": "keyword"},
      "category": {"type": "keyword"},
      "price": {"type": "double"},
      "rating": {"type": "double"},
      "reviewCount": {"type": "integer"},
      "inStock": {"type": "boolean"},
      "primeEligible": {"type": "boolean"}
    }
  }
}
```

**Ranking Algorithm:**
- Text relevance (BM25)
- Popularity score (views, orders)
- User personalization
- Business rules (sponsored products)

### 7.3 Recommendation Engine
**Technology:** Machine Learning (TensorFlow/PyTorch)

**Algorithms:**
1. **Collaborative Filtering:**
   - User-based: Similar users bought these
   - Item-based: Frequently bought together

2. **Content-Based:**
   - Based on product attributes
   - Category similarity

3. **Hybrid Approach:**
   - Combine multiple signals
   - Personalized recommendations

**Real-time Processing:**
- Kafka for event streaming
- Spark for batch processing
- Online learning for model updates

**Recommendation Types:**
- "Recommended for you"
- "Frequently bought together"
- "Customers who bought this also bought"
- "Sponsored products"

### 7.4 Inventory Management Service
**Responsibilities:**
- Track stock across warehouses
- Reserve inventory during checkout
- Handle stock replenishment
- Low stock alerts

**Key Challenges:**
- Prevent overselling
- Handle concurrent orders
- Multi-warehouse allocation

**Implementation:**
```sql
-- Reserve inventory during checkout (with timeout)
BEGIN;
UPDATE product_variants
SET stock_quantity = stock_quantity - :quantity
WHERE variant_id = :variantId
  AND stock_quantity >= :quantity;

-- If rows affected = 0, stock not available
-- Create reservation with expiry
INSERT INTO inventory_reservations
(variant_id, order_id, quantity, expires_at)
VALUES (:variantId, :orderId, :quantity, NOW() + INTERVAL '10 minutes');

COMMIT;
```

**Warehouse Selection:**
- Proximity to customer
- Stock availability
- Fulfillment cost

### 7.5 Order Management Service
**Workflow:**
1. **Validation:**
   - Verify cart items
   - Check stock availability
   - Validate address

2. **Order Creation:**
   - Generate order number
   - Lock inventory
   - Create order record

3. **Payment Processing:**
   - Call payment service
   - Handle 3D Secure
   - Update payment status

4. **Fulfillment:**
   - Assign to warehouse
   - Create shipping label
   - Update tracking

5. **Post-Delivery:**
   - Send review request
   - Handle returns

**State Machine:**
```
pending -> confirmed -> processing -> shipped -> delivered
                     ↓
                  cancelled

delivered -> return_requested -> return_approved -> refunded
```

### 7.6 Payment Service
**Integration:** Stripe, PayPal, Amazon Pay

**Features:**
- Multiple payment methods
- Saved cards (tokenized)
- Fraud detection
- PCI compliance

**Flow:**
1. Client gets payment token from gateway
2. Server validates and creates payment intent
3. Process payment with idempotency key
4. Handle 3D Secure if required
5. Update order status

**Retry Logic:**
- Exponential backoff
- Circuit breaker pattern
- Fallback payment methods

### 7.7 Prime Service
**Features:**
- Membership management
- Fast delivery options
- Prime Video/Music integration
- Exclusive deals

**Benefits Tracking:**
- Delivery savings
- Content access logs
- Deal usage

**Auto-Renewal:**
- Scheduled job for renewals
- Email reminders
- Payment processing

### 7.8 Seller Service
**Features:**
- Seller onboarding
- Product listing
- Inventory management
- Order fulfillment
- Analytics dashboard
- Payment settlement

**Seller Dashboard:**
- Sales metrics
- Inventory levels
- Customer reviews
- Performance metrics

### 7.9 Review Service
**Features:**
- Review submission
- Review moderation (AI + manual)
- Helpful voting
- Verified purchase badge

**Moderation:**
- Spam detection
- Sentiment analysis
- Inappropriate content filter
- Review authenticity

**Storage:** Cassandra for high write throughput

## 8. Transaction Management & Consistency

### Order Placement (Critical Path)

**Saga Pattern Implementation:**

```
1. ValidateCart
   - Success: continue
   - Failure: return error

2. ReserveInventory
   - Success: continue
   - Failure: compensate (none needed)

3. CreateOrder
   - Success: continue
   - Failure: compensate (release inventory)

4. ProcessPayment
   - Success: continue
   - Failure: compensate (cancel order, release inventory)

5. UpdateInventory
   - Success: continue
   - Failure: compensate (refund payment, cancel order)

6. SendConfirmation
   - Fire and forget (eventual consistency)
```

**Compensation Logic:**
```javascript
async function placeOrder(cartId, paymentInfo) {
  const saga = new Saga();

  try {
    // Step 1: Validate cart
    const cart = await saga.execute(
      () => validateCart(cartId),
      () => {} // no compensation
    );

    // Step 2: Reserve inventory
    const reservation = await saga.execute(
      () => inventoryService.reserve(cart.items),
      () => inventoryService.releaseReservation(reservation.id)
    );

    // Step 3: Create order
    const order = await saga.execute(
      () => orderService.create(cart, reservation),
      () => orderService.cancel(order.id)
    );

    // Step 4: Process payment
    const payment = await saga.execute(
      () => paymentService.charge(order.id, paymentInfo),
      () => paymentService.refund(payment.id)
    );

    // Step 5: Confirm inventory
    await saga.execute(
      () => inventoryService.confirmReservation(reservation.id),
      () => inventoryService.addBack(reservation.items)
    );

    // Step 6: Send notifications (async)
    eventBus.publish('order.placed', {orderId: order.id});

    return order;

  } catch (error) {
    await saga.compensate();
    throw error;
  }
}
```

### Eventual Consistency

**Use Cases:**
- Product catalog updates
- Review aggregation
- Recommendation updates
- Analytics data

**Event-Driven Architecture:**
```
Order Placed Event
  ├─> Update Seller Dashboard (async)
  ├─> Send Email Notification (async)
  ├─> Update Recommendation Model (async)
  └─> Update Analytics (async)
```

### Consistency Guarantees

| Operation | Consistency Level | Justification |
|-----------|------------------|---------------|
| Order creation | Strong | Money involved |
| Inventory update | Strong | Prevent overselling |
| Payment | Strong | Financial transaction |
| Product catalog | Eventual | User experience |
| Reviews | Eventual | Not critical |
| Recommendations | Eventual | ML-based |
| Search index | Eventual | Acceptable delay |

## 9. Security Considerations

### Authentication
- **Multi-factor authentication (MFA)**
- **OAuth 2.0** for third-party integrations
- **JWT** with short expiration
- **Refresh tokens** with rotation

### Authorization
- **Role-based access control (RBAC)**
  - Customer, Seller, Admin roles
  - Fine-grained permissions
- **Attribute-based access control (ABAC)**
  - Access based on context

### Data Protection
- **Encryption at rest:** AES-256
- **Encryption in transit:** TLS 1.3
- **PII encryption:** Customer data
- **Tokenization:** Payment information

### Payment Security
- **PCI DSS Level 1** compliance
- **Never store** CVV or full card numbers
- **Tokenization** via payment gateway
- **3D Secure** for authentication
- **Fraud detection:**
  - Velocity checks
  - Device fingerprinting
  - Behavioral analysis
  - ML-based scoring

### API Security
- **Rate limiting:** Per user, per IP
- **API keys** for third-party access
- **CORS** policies
- **Input validation** and sanitization
- **SQL injection** prevention
- **XSS** prevention

### Seller Security
- **Seller verification:**
  - Identity verification
  - Business verification
  - Bank account verification
- **Product approval** workflow
- **Seller rating** system
- **Dispute resolution**

### Infrastructure Security
- **WAF** (Web Application Firewall)
- **DDoS protection**
- **Network segmentation**
- **VPC** with private subnets
- **Security groups** and NACLs
- **Regular security audits**

## 10. Scalability

### Database Scaling

**Sharding Strategy:**
```
Products: Shard by category_id
- Electronics -> Shard 1
- Books -> Shard 2
- Clothing -> Shard 3

Orders: Shard by user_id (consistent hashing)
- Even distribution
- User affinity

Reviews: Time-based partitioning (Cassandra)
- Recent reviews on hot nodes
- Archive old reviews
```

**Read Replicas:**
- Primary for writes
- Multiple replicas for reads
- Read-write splitting in application

**Caching:**
```
L1: Application cache (in-memory)
  └─> Product details, user sessions

L2: Redis cluster
  └─> Search results, recommendations, cart data
  └─> TTL: 15 minutes to 1 hour

L3: CDN (CloudFront)
  └─> Static assets, product images
  └─> TTL: 1 day to 1 month
```

### Service Scaling

**Auto-scaling:**
- **Horizontal pod autoscaling** (Kubernetes)
- **Metrics:** CPU, memory, request rate
- **Scale up:** > 70% utilization
- **Scale down:** < 30% utilization

**Service Priority:**
```
Critical (always available):
- Auth Service
- Payment Service
- Order Service

High (scale first):
- Product Service
- Search Service
- Cart Service

Medium (scale if needed):
- Review Service
- Recommendation Service
- Seller Service
```

### Search Scaling

**Elasticsearch Cluster:**
- 3 master nodes (cluster coordination)
- N data nodes (shard data)
- M ingest nodes (indexing pipeline)

**Index Sharding:**
```
products index
  ├─> 10 primary shards
  └─> 2 replicas per shard

Total: 30 shards across 10 nodes
```

**Query Optimization:**
- Filter before query
- Use appropriate analyzers
- Pagination with search_after
- Cache frequent queries

### CDN & Static Assets

**CloudFront:**
- Multiple edge locations
- Origin failover
- Image optimization (WebP)
- Lazy loading

**S3 Buckets:**
- Versioning enabled
- Lifecycle policies
- Cross-region replication

### Message Queues

**SQS for async tasks:**
- Email notifications
- Image processing
- Analytics events
- Inventory updates

**Kafka for event streaming:**
- Order events
- Inventory changes
- User activity
- Real-time analytics

### Load Balancing

**Application Load Balancer (ALB):**
- Path-based routing
- Health checks
- SSL termination
- Sticky sessions

**Global Load Balancing:**
- Route53 geolocation routing
- Multi-region deployment
- Failover policies

## 11. Trade-offs

### 1. Consistency vs Availability

**Decision:** CAP theorem - Choose AP for most services, CP for critical paths

**Trade-offs:**
- **Product catalog:** Eventual consistency (better availability)
  - Pro: Fast reads, high availability
  - Con: Might show outdated stock momentarily
  - Mitigation: Validate at checkout

- **Orders/Payments:** Strong consistency (better correctness)
  - Pro: No duplicate orders, accurate inventory
  - Con: Lower availability, higher latency
  - Acceptable: Money is involved

### 2. Microservices vs Monolith

**Decision:** Microservices architecture

**Pros:**
- Independent scaling
- Technology flexibility
- Team autonomy
- Fault isolation

**Cons:**
- Distributed system complexity
- Network latency
- Data consistency challenges
- More operational overhead

**Mitigation:**
- Service mesh (Istio)
- API gateway
- Distributed tracing
- Centralized logging

### 3. SQL vs NoSQL

**Decision:** Polyglot persistence

**PostgreSQL for:**
- Users, Orders, Products
- Need: ACID, complex queries, relationships

**Cassandra for:**
- Reviews, Activity logs
- Need: High write throughput, time-series data

**Redis for:**
- Caching, Sessions
- Need: Fast reads, temporary data

### 4. Real-time vs Batch Processing

**Real-time (Kafka + Spark Streaming):**
- Inventory updates
- Fraud detection
- Personalized recommendations

**Batch (Spark):**
- Analytics
- ML model training
- Data warehouse updates

### 5. Search: Build vs Buy

**Decision:** Use Elasticsearch (open-source)

**Alternatives:**
- Algolia (SaaS) - expensive at scale
- AWS CloudSearch - limited customization
- Build custom - reinventing the wheel

**Justification:**
- Full control over ranking
- Cost-effective at scale
- Customizable
- Large community

### 6. Image Storage

**Decision:** S3 + CloudFront

**Alternatives:**
- Self-hosted - operational burden
- Other cloud storage - vendor lock-in

**Optimization:**
- Multiple sizes generated
- WebP for modern browsers
- Lazy loading
- Responsive images

### 7. Inventory Reservations

**Decision:** Time-bound reservations (10 minutes)

**Trade-off:**
- Hold stock during checkout
- Release if not completed
- Prevents overselling
- Might miss some sales

**Alternative:**
- No reservation (risk overselling)
- Longer reservation (stock locked unnecessarily)

## 12. Follow-up Questions

### Functional

1. How would you implement lightning deals (limited quantity, time-bound)?
2. How would you handle pre-orders for upcoming products?
3. How would you implement subscription boxes (monthly deliveries)?
4. How would you add social features (share lists, gift registry)?
5. How would you implement dynamic pricing based on demand?

### Scalability

6. How would you scale to handle Black Friday (20x traffic)?
7. How would you implement multi-region deployment for global expansion?
8. How would you handle database hotspots (celebrity product launches)?
9. How would you scale the recommendation engine for 1B products?
10. How would you implement real-time inventory across 100+ warehouses?

### Performance

11. How would you optimize the checkout flow for mobile (slow networks)?
12. How would you reduce search latency from 200ms to 50ms?
13. How would you implement progressive web app (PWA) for offline browsing?
14. How would you optimize database queries for the seller dashboard?
15. How would you reduce page load time for product detail pages?

### Reliability

16. How would you ensure zero data loss during database failures?
17. How would you implement graceful degradation when services fail?
18. How would you handle split-brain scenarios in distributed systems?
19. How would you implement disaster recovery (RPO/RTO requirements)?
20. How would you prevent cascading failures?

### Advanced Features

21. How would you implement AR try-on for products?
22. How would you add voice shopping (Alexa integration)?
23. How would you implement marketplace seller fraud detection?
24. How would you build a real-time pricing engine?
25. How would you implement personalized homepages (A/B testing)?

### Data & Analytics

26. How would you build a data warehouse for business intelligence?
27. How would you implement real-time analytics for sellers?
28. How would you track attribution for marketing campaigns?
29. How would you implement customer lifetime value prediction?
30. How would you build a recommendation model with cold-start problem?

---

**Key Takeaways:**
- Amazon-scale systems require careful trade-offs
- Polyglot persistence is essential
- Strong consistency where it matters (money)
- Eventual consistency for user experience
- Microservices enable independent scaling
- Machine learning for personalization
- Robust inventory management is critical
- Security and compliance are non-negotiable
