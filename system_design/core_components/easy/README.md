# Core Components: Easy Level

## Overview

This section contains classic system design problems that are frequently asked in interviews. These problems help you apply fundamental concepts to real-world scenarios. Each design is complete with requirements, capacity estimation, APIs, database schemas, and implementation details.

## Problems Covered

### 1. URL Shortener (url_shortener.md) ✅ COMPLETE
**Design TinyURL / bit.ly**

A classic entry-level system design problem that tests your understanding of:
- Unique ID generation (Base62 encoding)
- Database design for billions of URLs
- Read-heavy system optimization (caching)
- Analytics and tracking

**Key Components:**
- Short code generation algorithm
- Redirection service
- Analytics tracking
- Custom alias support

**Scale:** 100M URLs/month, 10B redirects/month

**Difficulty:** ⭐⭐ (2/5) - Great starting problem

---

### 2. Parking Lot System (parking_lot.md)
**Design a multi-level parking lot management system**

Tests object-oriented design and state management:
- Multiple vehicle types (car, truck, motorcycle)
- Multiple spot sizes (compact, regular, large)
- Real-time availability tracking
- Payment processing
- Entry/exit management

**Key Components:**
- Parking spot allocation algorithm
- Vehicle tracking
- Payment calculation
- Availability API

**Scale:** 1000 spots, 10K vehicles/day

**Difficulty:** ⭐⭐ (2/5) - OOP design focus

---

### 3. Vending Machine (vending_machine.md)
**Design a vending machine system**

Tests state machine design and transaction handling:
- Product inventory management
- Payment processing (cash, card)
- Change dispensing
- State transitions
- Concurrent access handling

**Key Components:**
- State machine (Idle → Selection → Payment → Dispensing)
- Inventory management
- Payment validation
- Change calculation algorithm

**Scale:** Single machine, 100 products, 500 transactions/day

**Difficulty:** ⭐⭐ (2/5) - State management focus

---

## Common Patterns Across Problems

### Pattern 1: Unique ID Generation
**Used in:** URL Shortener
```
Approaches:
1. Auto-increment (simple, predictable)
2. Base62 encoding (compact representation)
3. Hash-based (distributed generation)
4. UUID (guaranteed uniqueness, longer)

Choose based on:
- Length requirements
- Predictability concerns
- Distribution needs
```

### Pattern 2: State Machine Design
**Used in:** Vending Machine, Parking Lot
```
States → Transitions → Actions
- Define valid states
- Define valid transitions
- Handle invalid transitions
- Consider concurrent state changes
```

### Pattern 3: Real-time Availability
**Used in:** Parking Lot
```
Challenges:
- Concurrency (multiple users checking availability)
- Consistency (spot allocated only once)
- Performance (fast availability checks)

Solutions:
- Optimistic locking
- Database transactions
- Distributed locks
```

## Interview Approach

### Step 1: Clarify Requirements (5 minutes)
**Example (URL Shortener):**
- "Do we need analytics?"
- "Should URLs expire?"
- "Do we support custom aliases?"
- "What's the expected scale?"

### Step 2: Capacity Estimation (5-10 minutes)
**Always calculate:**
- QPS (queries per second)
- Storage (over 5-10 years)
- Bandwidth (read + write)
- Cache size (20% hot data)

### Step 3: High-Level Design (10-15 minutes)
- Draw boxes and arrows
- Identify major components
- Show data flow
- Discuss load balancing, caching

### Step 4: Deep Dive (15-20 minutes)
- API design
- Database schema
- Core algorithms
- Failure scenarios

### Step 5: Trade-offs and Bottlenecks (5-10 minutes)
- Discuss alternatives
- Identify bottlenecks
- Suggest improvements
- Answer follow-up questions

## Comparison Table

| Problem | Primary Focus | Scale | Key Challenge |
|---------|--------------|-------|---------------|
| **URL Shortener** | Distributed systems | Billions of URLs | Unique ID generation |
| **Parking Lot** | OOP design, state | 1000s of spots | Concurrent allocation |
| **Vending Machine** | State machine | Single machine | State transitions |

## Code Structure Tips

### URL Shortener
```python
class URLShortener:
    def shorten(long_url) -> short_url
    def expand(short_url) -> long_url
    def track_click(short_url) -> analytics
    def generate_short_code() -> code
```

### Parking Lot
```python
class ParkingLot:
    def find_spot(vehicle_type) -> spot
    def park_vehicle(vehicle, spot) -> ticket
    def remove_vehicle(ticket) -> fee
    def get_availability() -> counts
```

### Vending Machine
```python
class VendingMachine:
    states = [IDLE, SELECTING, PAYMENT, DISPENSING]
    def select_product(product_id)
    def insert_money(amount)
    def dispense_product()
    def return_change()
```

## Common Mistakes

### URL Shortener
❌ Not considering collision handling
❌ Using timestamps (predictable)
❌ Not planning for scale
❌ Forgetting analytics

✅ Use Base62 or hash with collision resolution
✅ Calculate capacity for years
✅ Implement caching (99% hit rate)
✅ Async analytics processing

### Parking Lot
❌ Not handling concurrency
❌ Poor spot allocation algorithm
❌ No support for vehicle types

✅ Use database transactions
✅ Nearest/smallest available spot
✅ Different spot sizes

### Vending Machine
❌ No invalid state transition handling
❌ Not handling concurrent operations
❌ Poor change calculation

✅ Validate all transitions
✅ Use locks/transactions
✅ Greedy algorithm for change

## Extending the Problems

### URL Shortener Extensions
1. Add authentication and user accounts
2. Implement rate limiting
3. Add QR code generation
4. Support link expiration
5. Provide detailed analytics dashboard

### Parking Lot Extensions
1. Add reservation system
2. Implement dynamic pricing (surge pricing)
3. Add electric vehicle charging spots
4. Mobile app for finding/paying
5. Multi-location management

### Vending Machine Extensions
1. Add remote monitoring
2. Support multiple payment types
3. Implement loyalty programs
4. Add recommendations based on purchase history
5. Support online ordering with pickup

## Practice Tips

1. **Time Yourself:** 45-minute limit per problem
2. **Draw Diagrams:** Practice on whiteboard
3. **Explain Out Loud:** Verbalize your thought process
4. **Code Key Components:** Implement core algorithms
5. **Consider Failure Scenarios:** What if database fails? Network partition?

## Success Criteria

You've mastered easy-level problems when you can:
- ✅ Complete design in 45 minutes
- ✅ Estimate capacity accurately
- ✅ Design scalable APIs
- ✅ Identify bottlenecks
- ✅ Discuss trade-offs confidently
- ✅ Handle follow-up questions
- ✅ Code critical algorithms

## Next Steps

After mastering easy-level problems:
1. **Medium Level:** Rate limiter, Notification system, Autocomplete
2. **Hard Level:** Distributed ID generator, Consistent hashing, Distributed lock
3. **Full Systems:** Design Twitter, Design Uber, Design Netflix

## Additional Resources

### Video Tutorials
- Search for "[Problem Name] system design" on YouTube
- Watch multiple solutions to see different approaches

### Practice Platforms
- **Pramp:** Mock interviews with peers
- **Interviewing.io:** Anonymous mock interviews
- **LeetCode Premium:** System design discussions

### Books
- "System Design Interview" by Alex Xu (Volumes 1 & 2)
- "Grokking the System Design Interview" course

---

**Pro Tip:** These "easy" problems appear in 60%+ of entry-to-mid level interviews. Master these before attempting harder problems.

**Estimated Study Time:** 2-3 days for all three problems (with implementation)
