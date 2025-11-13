# Hard E-Commerce & Payments Problems

This directory contains advanced system design problems related to financial systems, payment processing, and high-frequency trading. These problems require deep understanding of distributed systems, strong consistency, ultra-low latency, regulatory compliance, and financial domain knowledge.

## Problems

### [Design Payment System (Stripe/PayPal)](./design_payment_system.md)

**Difficulty:** Hard

**Key Concepts:**
- Payment processing infrastructure
- PCI DSS Level 1 compliance
- Tokenization and vault
- Fraud detection (ML-based)
- Multi-currency support
- Webhooks and events
- Merchant onboarding
- Settlement and reconciliation
- Double-entry bookkeeping
- Idempotency and exactly-once processing

**What You'll Learn:**
- Building payment gateway from scratch
- PCI compliance requirements
- Fraud detection algorithms
- Webhook delivery guarantees
- Ledger system design
- Two-phase commit
- Saga pattern for distributed transactions
- Payment network integration

**Estimated Time:** 90-120 minutes

---

### [Design UPI / Real-Time Payment System](./design_upi.md)

**Difficulty:** Hard

**Key Concepts:**
- Peer-to-peer instant payments
- Virtual Payment Address (VPA)
- Real-time fund transfers (< 5 seconds)
- Multi-bank integration
- Strong consistency
- Double-entry ledger
- Settlement (instant for user, T+1 for banks)
- Fraud detection
- QR code payments

**What You'll Learn:**
- Real-time payment architecture
- Bank integration and settlement
- Instant payment vs batch settlement trade-off
- Double-entry bookkeeping
- Distributed ledger consistency
- Velocity checks and fraud prevention
- Reconciliation at scale
- UPI/Venmo-like system design

**Estimated Time:** 90-120 minutes

---

### [Design Digital Wallet](./digital_wallet.md)

**Difficulty:** Hard

**Key Concepts:**
- Wallet balance management
- Multi-currency support
- Add money / Withdraw money
- P2P transfers
- Merchant payments
- Currency conversion
- Rewards and cashback
- Transaction history
- Strong consistency for balances

**What You'll Learn:**
- Wallet architecture
- Balance calculation strategies (denormalized vs calculated)
- Currency conversion and exchange rates
- Cashback and rewards engine
- Multi-currency wallet design
- Double-entry bookkeeping for wallets
- Fraud detection for wallet transactions
- Settlement with banks

**Estimated Time:** 90-120 minutes

---

### [Design Stock Exchange / Trading Platform](./stock_exchange.md)

**Difficulty:** Hard

**Key Concepts:**
- Ultra-low latency (microseconds)
- Order matching engine
- Order book management
- Price-time priority
- Real-time market data streaming
- High-frequency trading (HFT)
- Settlement and clearing
- Risk management
- Regulatory compliance
- Market surveillance

**What You'll Learn:**
- Matching engine algorithms
- In-memory order book design
- Ultra-low latency optimization (C++)
- WebSocket streaming at scale
- Lock-free data structures
- Circuit breakers
- T+2 settlement
- Insider trading detection
- NUMA-aware programming
- Co-location architecture

**Estimated Time:** 120-150 minutes

---

## Common Themes

### Financial Domain Knowledge

All hard problems require understanding of:

1. **Double-Entry Bookkeeping:**
   - Every transaction has equal debits and credits
   - Ledger is the source of truth
   - Immutable entries (audit trail)
   - Balance calculation from ledger

2. **Strong Consistency:**
   - ACID transactions are non-negotiable
   - No eventual consistency for money
   - Distributed transactions (Saga pattern)
   - Idempotency for exactly-once semantics

3. **Regulatory Compliance:**
   - PCI DSS (payment card industry)
   - AML/KYC (anti-money laundering, know your customer)
   - GDPR (data privacy)
   - SOX (financial reporting)
   - Regional regulations

4. **Fraud Detection:**
   - Real-time risk scoring
   - Machine learning models
   - Velocity checks
   - Device fingerprinting
   - Behavioral analysis

5. **Reconciliation:**
   - Daily reconciliation
   - Bank reconciliation
   - Ledger balance verification
   - Discrepancy resolution

### Ultra-Low Latency

Stock exchange and HFT require:
- **Sub-millisecond latency** (< 1ms)
- **C/C++** for critical paths
- **Lock-free data structures**
- **In-memory processing**
- **CPU pinning and NUMA**
- **Co-location** (servers near exchange)

### Exactly-Once Processing

All systems must guarantee:
- **Idempotency keys** prevent duplicates
- **Distributed locks** prevent race conditions
- **Transaction boundaries** clear
- **Retry logic** with exponential backoff
- **Compensation logic** for failures

### Multi-Currency

Payment systems and wallets need:
- **Real-time exchange rates**
- **Currency conversion**
- **Settlement in multiple currencies**
- **Foreign exchange risk**

## Technical Deep Dives

### 1. Payment Processing Flow

```
User initiates payment
  ↓
Tokenize card data (vault)
  ↓
Fraud check (ML model)
  ↓
Authorize with card network
  ↓
Create ledger entries (double-entry)
  ↓
Send webhook to merchant
  ↓
Settlement (T+1 or T+2)
```

### 2. Order Matching Algorithm

```
Incoming order arrives
  ↓
Pre-trade risk checks
  ↓
Add to order book
  ↓
Match against opposite orders (price-time priority)
  ↓
Execute trades (atomic)
  ↓
Update positions and accounts
  ↓
Publish market data
  ↓
Settlement (T+2)
```

### 3. Wallet Transaction

```
Check balance (ledger)
  ↓
Validate limits
  ↓
BEGIN TRANSACTION
  ↓
Lock wallets
  ↓
Create transaction record
  ↓
Debit sender (ledger entry)
  ↓
Credit recipient (ledger entry)
  ↓
COMMIT
  ↓
Invalidate cache
  ↓
Send notifications
```

## Database Design Patterns

### 1. Ledger Table (Double-Entry)

```sql
CREATE TABLE ledger_entries (
    entry_id UUID PRIMARY KEY,
    transaction_id UUID NOT NULL,
    account_id UUID NOT NULL,
    debit DECIMAL(20, 2) DEFAULT 0,
    credit DECIMAL(20, 2) DEFAULT 0,
    balance DECIMAL(20, 2) NOT NULL,
    created_at TIMESTAMP,
    CONSTRAINT chk_debit_or_credit CHECK (
        (debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)
    )
);
```

### 2. Optimistic Locking

```sql
UPDATE accounts
SET balance = balance - ?,
    version = version + 1
WHERE account_id = ?
  AND version = ?;  -- Expected version

-- If rows affected = 0, retry transaction
```

### 3. Idempotency Keys

```sql
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    idempotency_key VARCHAR(255) UNIQUE,
    ...
);

-- Before processing, check:
SELECT * FROM transactions WHERE idempotency_key = ?;
-- If exists, return existing (don't create duplicate)
```

## Scalability Strategies

### 1. Sharding

**Payment System:**
- Merchants: Shard by merchant_id
- Transactions: Co-locate with merchant
- Ledger: Separate cluster (high write volume)

**Stock Exchange:**
- Order Book: One instance per symbol
- Trades: Shard by symbol + time
- Market Data: Replicate for read scaling

### 2. Caching

**Multi-Level Caching:**
```
L1: Application (in-memory)
L2: Redis Cluster
L3: CDN (for static data)
```

**Cache Invalidation:**
- Invalidate on write
- TTL for read-mostly data
- Write-through for critical data

### 3. Event-Driven Architecture

**Kafka Topics:**
- `payments.initiated`
- `payments.completed`
- `payments.failed`
- `trades.executed`
- `market-data.ticks`

**Benefits:**
- Decoupled services
- Event sourcing
- Replay capability
- Real-time analytics

## Security & Compliance

### PCI DSS Compliance

**Requirements:**
1. **Never store** CVV/CVC
2. **Tokenize** all card data
3. **Encrypt** at rest (AES-256)
4. **Network segmentation** (CDE isolation)
5. **Regular audits** (quarterly ASV scans, annual assessment)
6. **Access control** (least privilege)
7. **Logging** (all access to cardholder data)

### Fraud Detection

**Real-time Checks:**
```python
def calculate_fraud_score(transaction):
    score = 0

    # Velocity (transactions per hour)
    if count_recent_txns(user, 1h) > 10:
        score += 30

    # Amount anomaly
    if transaction.amount > avg_amount * 5:
        score += 25

    # Geolocation
    if distance(current_location, usual_location) > 500km:
        score += 20

    # Device fingerprint
    if not is_known_device(transaction.device_id):
        score += 15

    # ML model
    score += ml_model.predict(transaction) * 30

    return min(score, 100)
```

**Actions:**
- 0-40: Allow
- 41-70: Challenge (OTP)
- 71-100: Block

### AML/KYC

**Know Your Customer:**
1. Identity verification (government ID)
2. Address verification
3. Source of funds
4. Risk assessment
5. Ongoing monitoring

**Anti-Money Laundering:**
1. Transaction monitoring
2. Suspicious activity reporting (SAR)
3. Sanctions screening
4. PEP (Politically Exposed Persons) checks

## Interview Strategy

### For Payment System Design

1. **Start with compliance** - PCI DSS is non-negotiable
2. **Focus on tokenization** - Never store raw card data
3. **Explain double-entry** - Show understanding of accounting
4. **Discuss idempotency** - Prevent duplicate charges
5. **Cover fraud detection** - ML models + rules engine
6. **Settlement & reconciliation** - Daily verification

### For UPI/Real-Time Payments

1. **Emphasize strong consistency** - No double-spending
2. **Explain instant UX vs bank settlement** - Trade-off
3. **Focus on ledger** - Source of truth
4. **Discuss fraud at scale** - Real-time checks
5. **Bank integration** - Multiple banks, different APIs
6. **Reconciliation** - Critical at this scale

### For Stock Exchange

1. **Start with latency** - Microseconds matter
2. **Matching engine deep dive** - In-memory, lock-free
3. **Price-time priority** - Standard algorithm
4. **Regulatory compliance** - Trade reporting, surveillance
5. **Risk management** - Circuit breakers, position limits
6. **Settlement** - T+2, clearing house

### General Tips

1. **Clarify the scope** - Focus on one component deeply
2. **Draw the architecture** - Visual representation helps
3. **Discuss numbers** - Show you understand scale
4. **Trade-offs** - No perfect solution, explain choices
5. **Failure scenarios** - What happens when payment fails?
6. **Monitoring** - How do you detect issues?
7. **Testing** - How do you test financial systems?

## Common Mistakes to Avoid

1. **Eventual consistency for money** - Always use strong consistency
2. **Ignoring compliance** - PCI DSS, AML, KYC are required
3. **Storing raw card data** - Use tokenization
4. **Missing idempotency** - Risk of duplicate charges
5. **No fraud detection** - Will lose money quickly
6. **Weak reconciliation** - Discrepancies will accumulate
7. **Poor audit trail** - Regulatory requirement
8. **Ignoring latency** - Critical for stock exchange
9. **No circuit breakers** - Flash crashes can happen
10. **Missing compensation logic** - Distributed transactions fail

## Practice Strategy

### Week 1-2: Payment System
- Understand PCI DSS requirements
- Study Stripe/PayPal architecture
- Implement tokenization flow
- Design fraud detection system
- Practice double-entry bookkeeping

### Week 3-4: Real-Time Payments
- Study UPI/Venmo architecture
- Understand bank settlement
- Design ledger system
- Implement strong consistency
- Practice reconciliation logic

### Week 5-6: Digital Wallet
- Design multi-currency support
- Implement currency conversion
- Design rewards engine
- Practice balance calculation
- Understand wallet regulations

### Week 7-8: Stock Exchange
- Study order matching algorithms
- Learn low-latency optimization
- Understand market microstructure
- Practice risk management
- Study regulatory requirements

## Additional Resources

### Books
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Building Microservices" - Sam Newman
- "Flash Boys" - Michael Lewis (HFT)
- "Payment Systems" - Bruce Summers

### Papers
- "The Matching Engine" - NASDAQ
- "Low-Latency Trading" - various HFT firms
- "Payment System Design" - Federal Reserve

### Standards
- PCI DSS Requirements
- ISO 20022 (financial messaging)
- FIX Protocol (trading)
- ISO 8583 (card transactions)

### APIs to Study
- Stripe API documentation
- PayPal API documentation
- NPCI UPI documentation
- Interactive Brokers API

## Next Steps

After mastering these hard problems:

1. **Implement a prototype** - Build simplified version
2. **Contribute to open source** - Payment/trading projects
3. **Read real-world architectures** - Engineering blogs
4. **Interview at fintech companies** - Apply your knowledge
5. **Stay updated** - Financial regulations change

## Conclusion

Hard problems require:
- **Deep domain knowledge** (finance, payments)
- **Strong consistency** (ACID, distributed transactions)
- **Regulatory compliance** (PCI DSS, AML, KYC)
- **Ultra-low latency** (for trading systems)
- **Fraud detection** (ML + rules)
- **Audit trail** (immutable logs)
- **Reconciliation** (daily verification)

**Remember:** Financial systems are different from other distributed systems. Money requires strong consistency, regulatory compliance, and zero tolerance for errors. Master these principles and you'll excel at fintech system design.
