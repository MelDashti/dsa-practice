# Design Payment System (Stripe/PayPal)

## 1. Problem Statement

Design a payment processing platform like Stripe or PayPal that enables businesses to accept payments online. The system must handle payment processing, fraud detection, multi-currency support, reconciliation, compliance (PCI DSS), webhooks, and provide SDKs for integration. It should support high transaction volumes with strong consistency guarantees and handle distributed transactions across multiple parties.

**Key Features:**
- Payment processing (credit cards, debit cards, bank transfers)
- Multi-currency support
- Fraud detection and prevention
- Payment reconciliation
- Webhooks for event notifications
- Developer APIs and SDKs
- Merchant onboarding and KYC
- Settlement and payouts
- Refunds and disputes
- PCI DSS Level 1 compliance
- Analytics and reporting

## 2. Requirements

### Functional Requirements

1. **Payment Processing**
   - Accept credit/debit cards (Visa, Mastercard, Amex)
   - Bank transfers (ACH, wire)
   - Alternative payment methods (Apple Pay, Google Pay)
   - Tokenization of payment methods
   - 3D Secure authentication
   - Recurring payments/subscriptions

2. **Merchant Management**
   - Merchant onboarding
   - KYC (Know Your Customer)
   - API key management
   - Webhook configuration
   - Dashboard for analytics

3. **Transaction Management**
   - Payment authorization
   - Payment capture
   - Partial capture
   - Refunds (full/partial)
   - Disputes and chargebacks
   - Transaction history

4. **Multi-Currency Support**
   - 135+ currencies
   - Real-time exchange rates
   - Currency conversion
   - Settlement in merchant currency

5. **Fraud Detection**
   - Real-time fraud scoring
   - Machine learning models
   - Risk rules engine
   - Velocity checks
   - 3D Secure integration

6. **Settlement & Payouts**
   - Automated settlements
   - Configurable payout schedules
   - Reserve accounts
   - Split payments
   - Platform fees

7. **Compliance & Security**
   - PCI DSS Level 1 compliance
   - Strong Customer Authentication (SCA)
   - AML (Anti-Money Laundering)
   - GDPR compliance
   - Audit logs

8. **Developer Tools**
   - RESTful APIs
   - SDKs (JavaScript, Python, Ruby, etc.)
   - Webhooks
   - Testing environment
   - Documentation

### Non-Functional Requirements

1. **Reliability**
   - 99.99% uptime (4 nines)
   - No data loss (11 nines durability)
   - Exactly-once payment processing
   - No double charging

2. **Performance**
   - Payment authorization < 300ms (p95)
   - API response time < 100ms (p95)
   - Handle 10K TPS (transactions per second)
   - Peak: 50K TPS

3. **Consistency**
   - Strong consistency for financial transactions
   - ACID guarantees
   - Distributed transaction support
   - Idempotency

4. **Security**
   - End-to-end encryption
   - Tokenization (no card storage)
   - PCI DSS Level 1 compliance
   - HSM (Hardware Security Module) for keys
   - Regular security audits

5. **Scalability**
   - Handle millions of merchants
   - Billions of transactions per year
   - Global deployment (multi-region)
   - Horizontal scaling

6. **Compliance**
   - PCI DSS
   - PSD2 (Europe)
   - GDPR
   - AML/KYC regulations
   - Regional compliance (varies by country)

## 3. Scale Estimation

### Traffic Estimates
- **Active merchants:** 5 million
- **Transactions per day:** 100 million
- **Transactions per second (avg):** 1,157 TPS
- **Peak TPS:** 10,000 TPS
- **API calls per day:** 500 million

### Transaction Estimates
- **Average transaction value:** $50
- **Daily payment volume:** $5 billion
- **Annual payment volume:** $1.8 trillion
- **Transaction fee (2.9% + $0.30):** ~$52 billion/year revenue

### Storage Estimates
- **Merchants:** 5M × 10 KB = 50 GB
- **Transactions:** 100M/day × 365 days × 5 KB = 182 TB/year
- **Payment methods:** 20M cards × 1 KB = 20 GB (tokenized)
- **Logs/audit:** 100M events/day × 2 KB = 200 GB/day = 73 TB/year
- **Total (Year 1):** ~256 TB

### Bandwidth Estimates
- **Incoming:** 100M transactions × 5 KB = 500 GB/day
- **Outgoing:** 500M API responses × 3 KB = 1.5 TB/day
- **Webhooks:** 100M events × 2 KB = 200 GB/day
- **Total:** ~2.2 TB/day

### Cache Estimates
- **Merchant configs:** 100K active × 10 KB = 1 GB
- **Exchange rates:** 135 currencies × 1 KB = 135 KB
- **Fraud rules:** 10K rules × 5 KB = 50 MB
- **API rate limits:** 5M merchants × 1 KB = 5 GB
- **Total cache:** ~7 GB

## 4. High-Level Architecture

```
                           ┌──────────────┐
                           │   Merchant   │
                           │  Application │
                           └──────┬───────┘
                                  │ HTTPS
                                  ▼
                           ┌──────────────┐
                           │  Payment API │
                           │   Gateway    │
                           │  (API Keys)  │
                           └──────┬───────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐         ┌───────────────┐       ┌───────────────┐
│  Tokenization │         │   Payment     │       │     Fraud     │
│    Service    │         │  Processing   │       │   Detection   │
└───────┬───────┘         │   Service     │       │   Service     │
        │                 └───────┬───────┘       └───────┬───────┘
        │                         │                       │
        ▼                         ▼                       ▼
┌───────────────┐         ┌───────────────┐       ┌───────────────┐
│   Vault       │         │ Authorization │       │  Risk Engine  │
│   (HSM)       │         │   Service     │       │  (ML Model)   │
└───────────────┘         └───────┬───────┘       └───────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐         ┌───────────────┐       ┌───────────────┐
│  Settlement   │         │   Webhook     │       │ Reconciliation│
│   Service     │         │   Service     │       │   Service     │
└───────┬───────┘         └───────────────┘       └───────────────┘
        │
        ▼
┌───────────────┐
│    Bank       │
│  Integration  │
└───────────────┘

                        Data Layer
┌──────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │PostgreSQL│  │PostgreSQL│  │PostgreSQL│  │  Redis   │ │
│  │(Merchants)│ │(Payments)│  │ (Ledger) │  │ (Cache)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Kafka   │  │   SQS    │  │    S3    │  │ TimescaleDB│
│  │ (Events) │  │ (Queue)  │  │  (Logs)  │  │ (Metrics) │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────┘

                External Services
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   Card   │  │   Bank   │  │   KYC    │  │ Exchange │
│ Networks │  │  (ACH)   │  │ Service  │  │  Rates   │
│Visa/MC/Amex│ │          │  │          │  │   API    │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 5. API Design

### Payment APIs

```
POST /v1/payment_intents
Description: Create a payment intent (authorize payment)
Headers:
  Authorization: Bearer sk_live_xxx
  Idempotency-Key: uuid
Request:
{
  "amount": 5000, // cents
  "currency": "usd",
  "payment_method": "pm_xxx", // token
  "customer": "cus_xxx",
  "description": "Order #12345",
  "metadata": {
    "order_id": "12345",
    "customer_email": "user@example.com"
  },
  "capture_method": "automatic" // or "manual"
}
Response: 201 Created
{
  "id": "pi_xxx",
  "object": "payment_intent",
  "amount": 5000,
  "currency": "usd",
  "status": "requires_payment_method", // or "succeeded", "requires_action"
  "client_secret": "pi_xxx_secret_yyy",
  "created": 1699876543,
  "payment_method": "pm_xxx",
  "charges": {
    "data": [
      {
        "id": "ch_xxx",
        "amount": 5000,
        "status": "succeeded",
        "created": 1699876543
      }
    ]
  },
  "next_action": null // or 3D Secure redirect
}

POST /v1/payment_intents/{id}/confirm
Description: Confirm payment intent
Request:
{
  "payment_method": "pm_xxx",
  "return_url": "https://example.com/return"
}
Response: 200 OK

POST /v1/payment_intents/{id}/capture
Description: Capture authorized payment (for manual capture)
Request:
{
  "amount_to_capture": 5000 // can be less than authorized (partial capture)
}
Response: 200 OK

GET /v1/payment_intents/{id}
Response: 200 OK (payment intent object)
```

### Refund APIs

```
POST /v1/refunds
Request:
{
  "payment_intent": "pi_xxx",
  "amount": 5000, // optional, defaults to full refund
  "reason": "requested_by_customer", // or "duplicate", "fraudulent"
  "metadata": {
    "refund_reason": "Customer not satisfied"
  }
}
Response: 201 Created
{
  "id": "re_xxx",
  "object": "refund",
  "amount": 5000,
  "currency": "usd",
  "payment_intent": "pi_xxx",
  "status": "pending", // pending, succeeded, failed, cancelled
  "created": 1699876543,
  "reason": "requested_by_customer"
}

GET /v1/refunds/{id}
Response: 200 OK
```

### Customer & Payment Method APIs

```
POST /v1/customers
Request:
{
  "email": "user@example.com",
  "name": "John Doe",
  "description": "Customer for order #12345",
  "metadata": {
    "user_id": "12345"
  }
}
Response: 201 Created
{
  "id": "cus_xxx",
  "object": "customer",
  "email": "user@example.com",
  "name": "John Doe",
  "created": 1699876543
}

POST /v1/payment_methods
Request:
{
  "type": "card",
  "card": {
    "number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  },
  "billing_details": {
    "name": "John Doe",
    "address": {...}
  }
}
Response: 201 Created
{
  "id": "pm_xxx",
  "object": "payment_method",
  "type": "card",
  "card": {
    "brand": "visa",
    "last4": "4242",
    "exp_month": 12,
    "exp_year": 2025,
    "fingerprint": "xxx" // for duplicate detection
  },
  "created": 1699876543
}

POST /v1/payment_methods/{id}/attach
Request:
{
  "customer": "cus_xxx"
}
Response: 200 OK
```

### Webhook APIs

```
POST /v1/webhook_endpoints
Request:
{
  "url": "https://example.com/webhook",
  "enabled_events": [
    "payment_intent.succeeded",
    "payment_intent.payment_failed",
    "charge.refunded"
  ],
  "description": "Production webhook"
}
Response: 201 Created
{
  "id": "we_xxx",
  "object": "webhook_endpoint",
  "url": "https://example.com/webhook",
  "enabled_events": [...],
  "status": "enabled",
  "secret": "whsec_xxx" // for signature verification
}

Webhook Payload (sent to merchant):
POST https://example.com/webhook
Headers:
  Stripe-Signature: t=timestamp,v1=signature
Body:
{
  "id": "evt_xxx",
  "object": "event",
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      // payment_intent object
    }
  },
  "created": 1699876543
}
```

### Payout APIs

```
POST /v1/payouts
Request:
{
  "amount": 100000, // cents
  "currency": "usd",
  "destination": "ba_xxx", // bank account
  "description": "Weekly payout",
  "metadata": {...}
}
Response: 201 Created
{
  "id": "po_xxx",
  "object": "payout",
  "amount": 100000,
  "currency": "usd",
  "status": "pending", // pending, paid, failed, cancelled
  "arrival_date": 1700000000,
  "created": 1699876543
}
```

## 6. Database Schema

### Merchants Table
```sql
CREATE TABLE merchants (
    merchant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    business_name VARCHAR(500) NOT NULL,
    business_type VARCHAR(100),
    country VARCHAR(3) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'pending', -- pending, active, suspended, closed
    kyc_status VARCHAR(20) DEFAULT 'pending',
    kyc_verified_at TIMESTAMP,
    api_key_live VARCHAR(255) UNIQUE,
    api_key_test VARCHAR(255) UNIQUE,
    webhook_url VARCHAR(500),
    webhook_secret VARCHAR(255),
    payout_schedule VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly, manual
    reserve_percentage DECIMAL(5, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_api_key_live (api_key_live)
);
```

### Customers Table
```sql
CREATE TABLE customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES merchants(merchant_id),
    external_id VARCHAR(255), -- merchant's customer ID
    email VARCHAR(255),
    name VARCHAR(255),
    phone VARCHAR(20),
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(merchant_id, external_id),
    INDEX idx_merchant (merchant_id),
    INDEX idx_email (email)
);
```

### Payment_Methods Table
```sql
CREATE TABLE payment_methods (
    payment_method_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(customer_id),
    type VARCHAR(20) NOT NULL, -- card, bank_account
    token VARCHAR(255) UNIQUE NOT NULL, -- tokenized, no raw card data
    card_brand VARCHAR(20),
    card_last4 VARCHAR(4),
    card_exp_month INT,
    card_exp_year INT,
    card_fingerprint VARCHAR(255), -- for duplicate detection
    bank_account_last4 VARCHAR(4),
    bank_routing_number VARCHAR(20),
    billing_details JSONB,
    is_default BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_token (token),
    INDEX idx_fingerprint (card_fingerprint)
);
```

### Payment_Intents Table
```sql
CREATE TABLE payment_intents (
    payment_intent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key VARCHAR(255) UNIQUE,
    merchant_id UUID NOT NULL REFERENCES merchants(merchant_id),
    customer_id UUID REFERENCES customers(customer_id),
    payment_method_id UUID REFERENCES payment_methods(payment_method_id),
    amount BIGINT NOT NULL, -- in cents
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(30) DEFAULT 'requires_payment_method',
    /* Statuses: requires_payment_method, requires_confirmation, requires_action,
       processing, requires_capture, cancelled, succeeded */
    capture_method VARCHAR(20) DEFAULT 'automatic', -- automatic, manual
    amount_capturable BIGINT DEFAULT 0,
    amount_received BIGINT DEFAULT 0,
    description TEXT,
    metadata JSONB,
    client_secret VARCHAR(255),
    last_payment_error JSONB,
    next_action JSONB, -- for 3D Secure redirects
    charges JSONB, -- array of charge IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_merchant (merchant_id),
    INDEX idx_customer (customer_id),
    INDEX idx_status (status),
    INDEX idx_idempotency (idempotency_key),
    INDEX idx_created (created_at),
    CONSTRAINT chk_amount CHECK (amount > 0)
);
```

### Charges Table
```sql
CREATE TABLE charges (
    charge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_intent_id UUID NOT NULL REFERENCES payment_intents(payment_intent_id),
    merchant_id UUID NOT NULL REFERENCES merchants(merchant_id),
    customer_id UUID REFERENCES customers(customer_id),
    payment_method_id UUID NOT NULL REFERENCES payment_methods(payment_method_id),
    amount BIGINT NOT NULL,
    amount_refunded BIGINT DEFAULT 0,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL, -- succeeded, pending, failed
    failure_code VARCHAR(50),
    failure_message TEXT,
    network_transaction_id VARCHAR(255), -- from card network
    authorization_code VARCHAR(20),
    captured BOOLEAN DEFAULT FALSE,
    refunded BOOLEAN DEFAULT FALSE,
    disputed BOOLEAN DEFAULT FALSE,
    risk_score INT, -- 0-100
    risk_level VARCHAR(20), -- low, medium, high
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_payment_intent (payment_intent_id),
    INDEX idx_merchant (merchant_id),
    INDEX idx_customer (customer_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);
```

### Refunds Table
```sql
CREATE TABLE refunds (
    refund_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    charge_id UUID NOT NULL REFERENCES charges(charge_id),
    payment_intent_id UUID NOT NULL REFERENCES payment_intents(payment_intent_id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, succeeded, failed, cancelled
    reason VARCHAR(50), -- requested_by_customer, duplicate, fraudulent
    failure_reason TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_charge (charge_id),
    INDEX idx_payment_intent (payment_intent_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);
```

### Disputes Table
```sql
CREATE TABLE disputes (
    dispute_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    charge_id UUID NOT NULL REFERENCES charges(charge_id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    reason VARCHAR(50), -- fraudulent, general, unrecognized
    status VARCHAR(20) DEFAULT 'warning_needs_response',
    /* Statuses: warning_needs_response, warning_under_review, warning_closed,
       needs_response, under_review, charge_refunded, won, lost */
    evidence_details JSONB,
    is_charge_refundable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_charge (charge_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);
```

### Ledger Table (Double-entry bookkeeping)
```sql
CREATE TABLE ledger_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL,
    account_id UUID NOT NULL, -- merchant account, platform account, etc.
    debit BIGINT DEFAULT 0,
    credit BIGINT DEFAULT 0,
    currency VARCHAR(3) NOT NULL,
    balance BIGINT NOT NULL, -- running balance
    entry_type VARCHAR(50) NOT NULL, -- payment, refund, fee, payout
    reference_type VARCHAR(50), -- charge, refund, payout
    reference_id UUID,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id),
    INDEX idx_created (created_at),
    CONSTRAINT chk_debit_or_credit CHECK ((debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0))
);
```

### Payouts Table
```sql
CREATE TABLE payouts (
    payout_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES merchants(merchant_id),
    amount BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    destination_account VARCHAR(255) NOT NULL, -- bank account ID
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_transit, paid, failed, cancelled
    arrival_date TIMESTAMP,
    failure_code VARCHAR(50),
    failure_message TEXT,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_merchant (merchant_id),
    INDEX idx_status (status),
    INDEX idx_arrival_date (arrival_date),
    INDEX idx_created (created_at)
);
```

### Webhook_Events Table
```sql
CREATE TABLE webhook_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES merchants(merchant_id),
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed
    attempts INT DEFAULT 0,
    last_attempt_at TIMESTAMP,
    next_attempt_at TIMESTAMP,
    response_code INT,
    response_body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_merchant (merchant_id),
    INDEX idx_status (status),
    INDEX idx_next_attempt (next_attempt_at)
);
```

### Fraud_Rules Table
```sql
CREATE TABLE fraud_rules (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(merchant_id), -- null for global rules
    name VARCHAR(255) NOT NULL,
    rule_type VARCHAR(50) NOT NULL, -- velocity, amount, country, ip
    condition JSONB NOT NULL, -- rule conditions
    action VARCHAR(20) NOT NULL, -- block, review, allow
    enabled BOOLEAN DEFAULT TRUE,
    priority INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_merchant (merchant_id),
    INDEX idx_enabled (enabled),
    INDEX idx_priority (priority)
);
```

### ACID Considerations

1. **Payment Processing:**
   - Use SERIALIZABLE isolation
   - Idempotency keys prevent duplicates
   - Exactly-once semantics

2. **Ledger Entries:**
   - Double-entry bookkeeping
   - Balance must always match sum(credit) - sum(debit)
   - Immutable entries (no updates, only inserts)

3. **Distributed Transactions:**
   - Two-phase commit with card networks
   - Saga pattern for multi-step flows
   - Compensation logic

4. **Refunds:**
   - Must be atomic with ledger update
   - Cannot refund more than charged
   - Maintain audit trail

## 7. Core Components

### 7.1 Tokenization Service
**Responsibility:** Convert sensitive card data to tokens

**Flow:**
```
1. Receive card data (HTTPS only)
2. Validate card (Luhn algorithm)
3. Generate unique token
4. Encrypt card data
5. Store in vault (HSM)
6. Return token to client
7. All subsequent requests use token
```

**Security:**
- Never log card numbers
- HSM for key storage
- Encryption at rest (AES-256)
- Encrypted in transit (TLS 1.3)
- PCI DSS Level 1 compliance

### 7.2 Authorization Service
**Responsibility:** Authorize payments with card networks

**Flow:**
```
1. Receive payment request with token
2. Decrypt card data from vault
3. Check fraud score
4. Send authorization request to card network
5. Receive authorization response
6. Create charge record
7. Return authorization result
```

**Card Network Integration:**
- Visa, Mastercard, Amex gateways
- 3D Secure (if required)
- Network transaction IDs
- Authorization codes

**Response Codes:**
- Approved
- Declined (insufficient funds, card declined)
- Fraud (suspected fraud)
- Error (network error)

### 7.3 Fraud Detection Service
**Technology:** Machine Learning + Rules Engine

**Real-time Scoring:**
```python
def calculate_fraud_score(transaction):
    score = 0

    # ML model prediction
    ml_score = fraud_model.predict(transaction_features)
    score += ml_score * 50

    # Rule-based checks
    if velocity_check(transaction):
        score += 20

    if country_mismatch(transaction):
        score += 15

    if amount_unusual(transaction):
        score += 10

    if device_fingerprint_mismatch(transaction):
        score += 5

    return min(score, 100)
```

**Features for ML Model:**
- Transaction amount
- Merchant category
- Customer location vs card location
- Time of day
- Device fingerprint
- Previous transaction history
- Velocity (transactions per hour)
- Card BIN (Bank Identification Number)

**Actions Based on Score:**
- 0-30: Allow
- 31-60: Review (flag for manual review)
- 61-100: Block (decline transaction)

**Velocity Checks:**
- Transactions per card per hour
- Transactions per IP per hour
- High-value transactions per merchant per day

### 7.4 Payment Processing Service
**Idempotency:**
```python
def process_payment(request, idempotency_key):
    # Check if already processed
    existing = get_payment_by_idempotency_key(idempotency_key)
    if existing:
        return existing  # return same result

    # Process payment
    try:
        payment_intent = create_payment_intent(request)
        charge = authorize_payment(payment_intent)

        if charge.status == 'succeeded':
            # Update ledger
            record_ledger_entry(charge)

            # Trigger webhooks
            queue_webhook_event(merchant_id, 'payment_intent.succeeded', payment_intent)

        return payment_intent

    except Exception as e:
        # Log error, return failure
        payment_intent.status = 'failed'
        payment_intent.last_payment_error = str(e)
        return payment_intent
```

**State Machine:**
```
requires_payment_method
  ↓
requires_confirmation
  ↓
requires_action (3D Secure)
  ↓
processing
  ↓
requires_capture (manual capture)
  ↓
succeeded

Any state can transition to:
  - cancelled (by merchant)
  - failed (payment failed)
```

### 7.5 Settlement Service
**Responsibility:** Transfer funds to merchants

**Settlement Flow:**
```
1. Calculate merchant balance (charges - refunds - fees)
2. Apply reserve percentage (hold for chargebacks)
3. Schedule payout based on payout_schedule
4. Create payout record
5. Initiate bank transfer (ACH, wire)
6. Update ledger
7. Send payout confirmation
```

**Calculation:**
```sql
-- Daily settlement calculation
SELECT
    merchant_id,
    SUM(amount) - SUM(fee_amount) - SUM(refund_amount) AS net_amount
FROM (
    SELECT
        merchant_id,
        amount,
        amount * 0.029 + 30 AS fee_amount, -- 2.9% + $0.30
        0 AS refund_amount
    FROM charges
    WHERE status = 'succeeded'
      AND created_at >= CURRENT_DATE
      AND created_at < CURRENT_DATE + INTERVAL '1 day'

    UNION ALL

    SELECT
        c.merchant_id,
        0 AS amount,
        0 AS fee_amount,
        r.amount AS refund_amount
    FROM refunds r
    JOIN charges c ON r.charge_id = c.charge_id
    WHERE r.status = 'succeeded'
      AND r.created_at >= CURRENT_DATE
      AND r.created_at < CURRENT_DATE + INTERVAL '1 day'
) AS transactions
GROUP BY merchant_id;
```

**Reserve Account:**
- Hold percentage of funds (e.g., 10%)
- Release after chargeback window (90-120 days)
- Buffer for disputes and refunds

### 7.6 Webhook Service
**Responsibility:** Notify merchants of events

**Events:**
- payment_intent.succeeded
- payment_intent.payment_failed
- charge.succeeded
- charge.failed
- charge.refunded
- charge.dispute.created
- payout.paid
- payout.failed

**Delivery Guarantees:**
```python
def send_webhook(event):
    max_attempts = 5
    backoff = [1, 5, 15, 60, 300]  # seconds

    for attempt in range(max_attempts):
        try:
            # Sign payload
            signature = generate_signature(event.payload, webhook_secret)

            # Send POST request
            response = requests.post(
                merchant.webhook_url,
                json=event.payload,
                headers={
                    'Content-Type': 'application/json',
                    'Stripe-Signature': f't={timestamp},v1={signature}'
                },
                timeout=10
            )

            if response.status_code == 200:
                update_event_status(event.id, 'sent')
                return

        except Exception as e:
            log_error(e)

        # Exponential backoff
        if attempt < max_attempts - 1:
            sleep(backoff[attempt])

    # Failed after all attempts
    update_event_status(event.id, 'failed')
    alert_merchant(event)
```

**Signature Verification (Merchant side):**
```python
def verify_webhook_signature(payload, signature, secret):
    timestamp, sig = parse_signature_header(signature)

    # Prevent replay attacks (timestamp > 5 minutes old)
    if time.time() - timestamp > 300:
        return False

    # Verify signature
    expected_sig = hmac.new(
        secret.encode(),
        f'{timestamp}.{payload}'.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(sig, expected_sig)
```

### 7.7 Reconciliation Service
**Responsibility:** Ensure ledger accuracy

**Daily Reconciliation:**
```sql
-- Verify sum of all ledger entries = 0 (double-entry)
SELECT SUM(debit) - SUM(credit) AS difference
FROM ledger_entries
WHERE DATE(created_at) = CURRENT_DATE;

-- Should always be 0
-- If not, alert for investigation
```

**Bank Reconciliation:**
- Compare internal ledger with bank statements
- Match payouts with bank transfers
- Identify discrepancies
- Generate reconciliation reports

### 7.8 Compliance Service
**Responsibilities:**
- KYC (Know Your Customer)
- AML (Anti-Money Laundering)
- Transaction monitoring
- Regulatory reporting

**KYC Process:**
```
1. Collect merchant information
2. Verify identity (government ID)
3. Verify business (registration documents)
4. Risk assessment
5. Ongoing monitoring
```

**AML Checks:**
- Sanctions screening (OFAC)
- PEP (Politically Exposed Persons) screening
- Transaction pattern analysis
- Suspicious activity reporting (SAR)

## 8. Transaction Management & Consistency

### Payment Processing Transaction

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Check idempotency
SELECT payment_intent_id FROM payment_intents
WHERE idempotency_key = ?;

-- If exists, return existing (idempotent)

-- 2. Create payment intent
INSERT INTO payment_intents (
    idempotency_key, merchant_id, amount, currency, status
)
VALUES (?, ?, ?, ?, 'processing')
RETURNING payment_intent_id;

-- 3. Authorize with card network (external call, compensate if fails)
-- authorization_response = card_network.authorize(...)

-- 4. Create charge
INSERT INTO charges (
    payment_intent_id, merchant_id, amount, currency,
    status, network_transaction_id, authorization_code
)
VALUES (?, ?, ?, ?, 'succeeded', ?, ?)
RETURNING charge_id;

-- 5. Update payment intent
UPDATE payment_intents
SET status = 'succeeded',
    amount_received = amount
WHERE payment_intent_id = ?;

-- 6. Record ledger entries (double-entry)
-- Debit: Merchant account (receivable)
INSERT INTO ledger_entries (
    transaction_id, account_id, debit, currency, entry_type, reference_id
)
VALUES (?, 'merchant_' || ?, ?, ?, 'payment', ?);

-- Credit: Platform account
INSERT INTO ledger_entries (
    transaction_id, account_id, credit, currency, entry_type, reference_id
)
VALUES (?, 'platform', ?, ?, 'payment', ?);

COMMIT;

-- 7. Queue webhook (async, outside transaction)
INSERT INTO webhook_events (merchant_id, event_type, payload, status)
VALUES (?, 'payment_intent.succeeded', ?, 'pending');
```

### Refund Transaction

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Verify charge can be refunded
SELECT c.charge_id, c.amount, c.amount_refunded, c.disputed
FROM charges c
WHERE c.charge_id = ?
  AND c.status = 'succeeded'
  AND c.amount - c.amount_refunded >= ?  -- requested refund amount
FOR UPDATE;

-- If disputed, cannot refund (must be < 0 rows)

-- 2. Create refund record
INSERT INTO refunds (
    charge_id, payment_intent_id, amount, currency, status, reason
)
VALUES (?, ?, ?, ?, 'processing', ?)
RETURNING refund_id;

-- 3. Update charge
UPDATE charges
SET amount_refunded = amount_refunded + ?,
    refunded = (amount_refunded + ? = amount)
WHERE charge_id = ?;

-- 4. Process refund with card network
-- refund_response = card_network.refund(...)

-- 5. Update refund status
UPDATE refunds
SET status = 'succeeded'
WHERE refund_id = ?;

-- 6. Record ledger entries
-- Debit: Platform account
INSERT INTO ledger_entries (
    transaction_id, account_id, debit, currency, entry_type, reference_id
)
VALUES (?, 'platform', ?, ?, 'refund', ?);

-- Credit: Merchant account (reduce receivable)
INSERT INTO ledger_entries (
    transaction_id, account_id, credit, currency, entry_type, reference_id
)
VALUES (?, 'merchant_' || ?, ?, ?, 'refund', ?);

COMMIT;
```

### Handling Failures

**Payment Authorization Failure:**
```
1. External call to card network fails
2. Transaction rolls back
3. Payment intent status = 'failed'
4. Return error to merchant
5. No ledger entries created
6. Idempotency key allows retry
```

**Partial Refund:**
```
1. Merchant requests partial refund
2. Verify remaining amount >= refund amount
3. Create refund record
4. Update charge.amount_refunded
5. Ledger reflects partial refund
6. charge.refunded = false (not fully refunded)
```

## 9. Security Considerations

### PCI DSS Compliance

**Level 1 Requirements:**
- Never store CVV/CVC
- Never store full magnetic stripe data
- Tokenize all card data
- Encrypt cardholder data at rest
- Use HSM for key management
- Quarterly ASV scans
- Annual on-site audit

**Network Segmentation:**
```
Public Internet
  ↓ (Firewall)
DMZ (API Gateway, Load Balancers)
  ↓ (Firewall)
Application Layer (Non-PCI servers)
  ↓ (Firewall)
Card Data Environment (CDE)
  ├─ Tokenization Service
  ├─ Vault (HSM)
  └─ Key Management
```

### Encryption

**At Rest:**
- AES-256 for database
- HSM for card data and keys
- Encrypted backups

**In Transit:**
- TLS 1.3 for all connections
- Certificate pinning for card networks
- mTLS for internal services

### Authentication & Authorization

**API Keys:**
- Publishable key (client-side): pk_live_xxx
- Secret key (server-side): sk_live_xxx
- Separate test keys: pk_test_xxx, sk_test_xxx

**Key Rotation:**
- Support multiple active keys
- Gradual rotation (announce, grace period, deprecate)

**Permissions:**
- Restrict keys by IP address
- Rate limiting per key
- Audit logs for all API calls

### Fraud Prevention

**3D Secure:**
- Redirect user to bank for authentication
- SCA (Strong Customer Authentication) for EU
- Shifts liability to card issuer

**Device Fingerprinting:**
- Collect browser/device metadata
- Detect bot activity
- Track suspicious patterns

**IP Geolocation:**
- Compare card BIN country vs IP country
- Flag mismatches

**Velocity Checks:**
- Limit transactions per card/hour
- Limit high-value transactions
- Alert on sudden spikes

## 10. Scalability

### Database Scaling

**Sharding Strategy:**
```
Merchants: Shard by merchant_id (consistent hashing)
Payments: Co-locate with merchant shard
Charges: Co-locate with merchant shard
Ledger: Separate cluster (high write volume)
```

**Read Replicas:**
- Analytics queries to replicas
- Dashboard queries to replicas
- Transactional writes to primary

**Time-Series Data:**
- Use TimescaleDB for metrics
- Partition by time (monthly)
- Compress old data

### Caching Strategy

```
Redis Cluster:
- API rate limits (1 hour TTL)
- Merchant configs (1 hour TTL)
- Exchange rates (5 min TTL)
- Fraud rules (10 min TTL)
- Session data (ephemeral)
```

### Queue-Based Architecture

**Async Processing:**
- Webhook delivery (SQS)
- Payout processing (SQS)
- Fraud model updates (Kafka)
- Analytics events (Kafka)

**Benefits:**
- Decoupled services
- Better fault tolerance
- Horizontal scaling

### Global Deployment

**Multi-Region:**
```
US-East: Primary region
US-West: Failover
EU: Compliance (GDPR)
APAC: Latency reduction
```

**Data Residency:**
- EU data stays in EU (GDPR)
- Replicate globally for read performance
- Writes to local region

### Rate Limiting

**Per API Key:**
- 100 requests/second
- Burst: 200 requests/second
- Sliding window algorithm

**Per IP:**
- 1000 requests/minute
- DDoS protection (Cloudflare)

## 11. Trade-offs

### 1. Immediate vs Delayed Capture

**Immediate (automatic):**
- Pro: Simpler flow, faster settlement
- Con: Harder to cancel, inventory issues

**Delayed (manual):**
- Pro: Verify before capture, avoid fraud
- Con: More complex, auth expires

### 2. Strong vs Eventual Consistency

**Strong (payments):**
- Pro: Accurate balances, no double-charging
- Con: Higher latency, lower availability

**Eventual (analytics):**
- Pro: Better performance
- Con: Dashboard may be slightly stale

### 3. Synchronous vs Asynchronous Webhooks

**Synchronous:**
- Pro: Immediate notification
- Con: Merchant downtime blocks our system

**Asynchronous:**
- Pro: Fault tolerant, retry logic
- Con: Eventual delivery

### 4. PCI Compliance: Build vs Buy

**Build (in-house vault):**
- Pro: Full control, lower cost at scale
- Con: Complex, requires certification

**Buy (third-party):**
- Pro: Faster to market, certified
- Con: Vendor dependency, recurring cost

## 12. Follow-up Questions

1. How would you handle currency conversion?
2. How would you implement recurring billing/subscriptions?
3. How would you handle chargebacks?
4. How would you implement split payments (marketplaces)?
5. How would you handle card network downtime?
6. How would you implement payment plans (buy now, pay later)?
7. How would you handle international payments (cross-border)?
8. How would you implement dynamic 3D Secure (based on risk)?
9. How would you handle payment retries for failed payments?
10. How would you implement real-time balance tracking?
11. How would you handle cryptocurrency payments?
12. How would you implement instant payouts?
13. How would you handle merchant reserves and holds?
14. How would you implement invoice payments?
15. How would you handle tax calculation and reporting?
16. How would you implement fraud model retraining?
17. How would you handle payment orchestration (multiple processors)?
18. How would you implement payment links (no code integration)?
19. How would you handle regulatory reporting (different countries)?
20. How would you scale to 100K TPS?

---

**Key Takeaways:**
- PCI DSS compliance is non-negotiable
- Idempotency prevents duplicate charges
- Double-entry bookkeeping ensures accuracy
- Fraud detection is critical
- Webhooks enable real-time integration
- Reconciliation catches discrepancies early
- Distributed transactions require saga pattern
- Security and compliance first
