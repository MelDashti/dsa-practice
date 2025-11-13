# Medium E-Commerce & Payments Problems

This directory contains intermediate system design problems related to e-commerce and payment systems. These problems introduce complex challenges like concurrency control, inventory management, search optimization, and multi-vendor platforms.

## Problems

### [Design Amazon](./design_amazon.md)

**Difficulty:** Medium

**Key Concepts:**
- Multi-vendor marketplace
- Advanced search (Elasticsearch)
- Recommendation engine (ML)
- Product catalog at scale (100M+ products)
- Prime membership
- Inventory across warehouses
- Seller platform

**What You'll Learn:**
- Polyglot persistence
- Search service architecture
- Machine learning integration
- Saga pattern for distributed transactions
- Microservices at scale
- Event-driven architecture

**Estimated Time:** 60-90 minutes

---

### [Design BookMyShow](./design_bookmyshow.md)

**Difficulty:** Medium

**Key Concepts:**
- Ticket booking system
- Real-time seat selection
- Concurrency control (prevent double-booking)
- Seat locking mechanism
- High traffic during popular releases
- QR code generation and validation

**What You'll Learn:**
- Pessimistic vs optimistic locking
- Distributed locks with Redis
- Race condition handling
- Seat reservation flow
- Queue systems for peak traffic
- Transaction isolation levels
- Idempotency in distributed systems

**Estimated Time:** 60-90 minutes

---

### [Hotel Reservation System](./hotel_reservation.md)

**Difficulty:** Medium

**Key Concepts:**
- Multi-day booking
- Room inventory management
- Dynamic pricing
- Availability calculation across date ranges
- Cancellation and refund policies
- Location-based search

**What You'll Learn:**
- Inventory management for date ranges
- Preventing overbooking with transactions
- Dynamic pricing strategies
- Geo-spatial search
- Complex booking workflows
- Saga pattern for bookings
- Cancellation handling

**Estimated Time:** 60-90 minutes

---

## Common Themes

### Concurrency Control
All medium problems require handling concurrent requests:
- **Amazon:** Multiple users buying the last item
- **BookMyShow:** Multiple users selecting the same seat
- **Hotel Booking:** Multiple users booking the last room

**Solutions:**
1. **Optimistic Locking:** Version numbers, compare-and-swap
2. **Pessimistic Locking:** SELECT FOR UPDATE
3. **Distributed Locks:** Redis Redlock, Zookeeper

### Inventory Management
Managing limited resources is critical:
- **Product stock** (Amazon)
- **Seats** (BookMyShow)
- **Rooms** (Hotels)

**Key Challenges:**
- Prevent overselling
- Handle reservations
- Release expired locks
- Audit trail

### Search & Discovery
All systems need robust search:
- **Elasticsearch** for full-text search
- Faceted filtering
- Geo-spatial queries
- Ranking algorithms
- Autocomplete

### Transaction Management
Complex multi-step operations require:
- ACID guarantees for critical paths
- Saga pattern for distributed transactions
- Compensation logic for failures
- Idempotency for retries

### Payment Processing
All systems integrate payments:
- Payment gateway integration (Stripe, PayPal)
- PCI DSS compliance
- Fraud detection
- Refund processing
- Multi-currency support

## Learning Path

After completing easy problems, tackle these in order:

1. **Start with BookMyShow** if you want to focus on:
   - Concurrency control
   - Distributed locking
   - Real-time systems

2. **Start with Hotel Booking** if you want to focus on:
   - Complex inventory management
   - Dynamic pricing
   - Date-range queries

3. **Start with Amazon** if you want to focus on:
   - Large-scale architecture
   - Microservices
   - Machine learning integration
   - Multi-vendor platforms

## Key Technical Skills

### Database Design
- Proper indexing strategies
- Optimistic vs pessimistic locking
- Transaction isolation levels
- Sharding strategies
- Read replicas

### Distributed Systems
- Saga pattern
- Event-driven architecture
- Message queues (SQS, Kafka)
- Distributed locks
- CAP theorem trade-offs

### Search & Performance
- Elasticsearch cluster design
- Caching strategies (multi-level)
- CDN usage
- API optimization
- Database query optimization

### Scalability
- Horizontal scaling
- Auto-scaling strategies
- Load balancing
- Database sharding
- Microservices architecture

## Common Patterns

### 1. Saga Pattern
For distributed transactions:
```
Step 1: Action + Compensation
Step 2: Action + Compensation
Step 3: Action + Compensation
```

### 2. Event-Driven Architecture
```
Order Placed Event
  ├─> Update Inventory (async)
  ├─> Send Email (async)
  ├─> Update Analytics (async)
  └─> Update Recommendations (async)
```

### 3. CQRS (Command Query Responsibility Segregation)
- Separate read and write models
- Optimize each independently
- Eventual consistency

### 4. Cache-Aside Pattern
```
1. Check cache
2. If miss, query database
3. Store in cache
4. Return result
```

### 5. Circuit Breaker
```
1. Track failures
2. Open circuit after threshold
3. Fail fast during open state
4. Half-open to test recovery
5. Close when healthy
```

## Interview Tips

### For Amazon Design
- Focus on one component deeply (recommendations OR search OR inventory)
- Discuss polyglot persistence rationale
- Explain why microservices over monolith
- Talk about seller platform separately

### For BookMyShow Design
- Emphasize seat locking mechanism
- Discuss isolation levels clearly
- Explain queue system for high demand
- Consider fairness (FIFO) vs performance

### For Hotel Booking Design
- Focus on multi-day inventory logic
- Explain dynamic pricing strategy
- Discuss date-range availability calculation
- Talk about cancellation policy trade-offs

### General Tips
1. **Clarify requirements early** - Ask about scale, features, priorities
2. **Start high-level** - Architecture diagram first
3. **Go deep on 2-3 components** - Show expertise
4. **Discuss trade-offs** - Every decision has pros/cons
5. **Consider failure scenarios** - What happens when payment fails?
6. **Think about monitoring** - How do you detect issues?
7. **Scalability from day one** - But don't over-engineer

## Common Mistakes to Avoid

1. **Not handling concurrency properly**
   - Race conditions in inventory
   - Double booking
   - Lost updates

2. **Weak consistency where strong is needed**
   - Inventory must be strongly consistent
   - Orders must be atomic
   - Payments must be transactional

3. **Ignoring edge cases**
   - What if payment succeeds but email fails?
   - What if user abandons during checkout?
   - What if show/flight is cancelled?

4. **Over-engineering early**
   - Don't shard on day one
   - Don't build custom solutions for solved problems
   - Use managed services initially

5. **Forgetting about operational concerns**
   - Monitoring and alerting
   - Logging and debugging
   - Disaster recovery
   - Database backups

6. **Not considering user experience**
   - Fast checkout is critical
   - Clear error messages
   - Booking confirmation UX
   - Mobile optimization

## Related Hard Problems

Once comfortable with medium problems, progress to:
- [Payment System](../hard/design_payment_system.md) - Build Stripe/PayPal
- [UPI System](../hard/design_upi.md) - Real-time payments
- [Digital Wallet](../hard/digital_wallet.md) - Wallet with transactions
- [Stock Exchange](../hard/stock_exchange.md) - High-frequency trading

## Additional Resources

- Designing Data-Intensive Applications (Martin Kleppmann)
- System Design Interview (Alex Xu)
- Database transaction isolation levels
- Distributed systems patterns
- Elasticsearch documentation
- Microservices patterns
- Event-driven architecture
- SAGA pattern
- Circuit breaker pattern
- Rate limiting strategies
