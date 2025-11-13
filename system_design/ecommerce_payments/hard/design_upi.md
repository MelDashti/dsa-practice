# Design UPI / Real-Time Payment System (UPI/Venmo)

## 1. Problem Statement

Design a real-time peer-to-peer payment system like India's UPI (Unified Payments Interface) or Venmo that enables instant money transfers between bank accounts. The system must handle high transaction volumes, ensure strong consistency, prevent double-spending, support multiple banks, provide real-time notifications, and maintain a transaction ledger for reconciliation.

**Key Features:**
- Instant peer-to-peer money transfers
- Virtual Payment Address (VPA) / username
- QR code payments
- Bank account linking
- Request money
- Split bills
- Transaction history and statements
- Real-time notifications
- Multi-bank support
- Merchant payments
- Recurring payments/mandates

## 2. Requirements

### Functional Requirements

1. **User Management**
   - Registration with phone number
   - Bank account linking (multiple accounts)
   - Virtual Payment Address (VPA) creation (e.g., user@bank)
   - Profile management
   - Set default account

2. **Payment Initiation**
   - Send money to VPA/phone/account number
   - Send money via QR code scan
   - Request money from contacts
   - Split bills among group
   - Scheduled payments
   - Recurring payments/autopay

3. **Transaction Processing**
   - Real-time fund transfer (< 5 seconds)
   - Transaction validation
   - Balance checks
   - Fraud detection
   - Transaction limits (daily, per transaction)

4. **Transaction Management**
   - Transaction history
   - Search and filter
   - Download statements
   - Dispute resolution
   - Transaction cancellation (if not settled)

5. **Notifications**
   - Real-time push notifications
   - SMS notifications
   - Email receipts
   - Transaction confirmations

6. **Merchant Payments**
   - QR code generation for merchants
   - Payment collection
   - Settlement reports
   - Refunds

7. **Security**
   - PIN/biometric authentication
   - OTP verification
   - Device binding
   - Fraud monitoring
   - Transaction limits

### Non-Functional Requirements

1. **Performance**
   - Transaction completion < 5 seconds (p95)
   - API response time < 100ms
   - Handle 10K TPS
   - Peak: 50K TPS (festival seasons)

2. **Availability**
   - 99.99% uptime
   - 24/7 operation
   - No scheduled downtime

3. **Consistency**
   - Strong consistency for transactions
   - Exactly-once processing
   - No double-spending
   - ACID guarantees

4. **Scalability**
   - Support 500M+ users
   - 10B+ transactions per year
   - Multiple banks (100+)
   - Horizontal scaling

5. **Security**
   - End-to-end encryption
   - PCI DSS compliance
   - Two-factor authentication
   - Device fingerprinting
   - Fraud detection

6. **Reliability**
   - No transaction loss
   - Automated reconciliation
   - Disaster recovery (RPO < 1 min, RTO < 5 min)

## 3. Scale Estimation

### Traffic Estimates
- **Registered users:** 500 million
- **Active users (monthly):** 200 million
- **Daily active users:** 50 million
- **Transactions per day:** 100 million
- **Average TPS:** 1,157
- **Peak TPS:** 10,000 (during festivals)

### Transaction Estimates
- **Average transaction value:** $10
- **Daily transaction volume:** $1 billion
- **Annual transaction volume:** $365 billion
- **Success rate:** 95%
- **Failed transactions:** 5% (insufficient balance, limits)

### Storage Estimates
- **Users:** 500M × 5 KB = 2.5 TB
- **Bank accounts:** 1B accounts × 2 KB = 2 TB
- **Transactions:** 100M/day × 365 days × 3 KB = 109 TB/year
- **Ledger entries:** 200M entries/day × 1 KB = 200 GB/day = 73 TB/year
- **Total (Year 1):** ~186 TB

### Bandwidth Estimates
- **Incoming:** 100M transactions × 5 KB = 500 GB/day
- **Outgoing:** 100M responses × 3 KB = 300 GB/day
- **Notifications:** 200M (2 per txn) × 1 KB = 200 GB/day
- **Total:** ~1 TB/day

### Database Estimates
- **Read:Write ratio:** 30:70 (write-heavy during transactions)
- **Queries per second:** 50K (reads) + 10K (writes)
- **Database connections:** 10K concurrent

## 4. High-Level Architecture

```
                          ┌──────────────┐
                          │  Mobile App  │
                          │   (User)     │
                          └──────┬───────┘
                                 │ HTTPS
                                 ▼
                          ┌──────────────┐
                          │  API Gateway │
                          │  (Auth, Rate │
                          │   Limiting)  │
                          └──────┬───────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│     User      │        │   Payment     │      │     Bank      │
│   Service     │        │   Service     │      │   Service     │
└───────┬───────┘        └───────┬───────┘      └───────┬───────┘
        │                        │                       │
        ▼                        ▼                       ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│   Account     │        │   Ledger      │      │  Settlement   │
│   Service     │        │   Service     │      │   Service     │
└───────────────┘        └───────┬───────┘      └───────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│     Fraud     │        │ Notification  │      │Reconciliation │
│   Detection   │        │   Service     │      │   Service     │
└───────────────┘        └───────────────┘      └───────────────┘

                        Data Layer
┌──────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │PostgreSQL│  │PostgreSQL│  │PostgreSQL│  │  Redis   │ │
│  │  (Users) │  │(Payments)│  │ (Ledger) │  │ (Cache)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Kafka   │  │   SQS    │  │   S3     │  │TimescaleDB│
│  │ (Events) │  │(Async)   │  │  (Logs)  │  │ (Metrics) │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────┘

                    Bank Integration
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Bank A  │  │  Bank B  │  │  Bank C  │  │  NPCI    │
│   API    │  │   API    │  │   API    │  │ (Switch) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 5. API Design

### User APIs

```
POST /api/v1/users/register
Request:
{
  "phone": "+919876543210",
  "name": "John Doe",
  "email": "john@example.com",
  "pin": "1234" // hashed
}
Response: 201 Created
{
  "userId": "uuid",
  "phone": "+919876543210",
  "vpa": "john@paytm", // auto-generated
  "status": "active"
}

POST /api/v1/users/link-bank
Request:
{
  "userId": "uuid",
  "bankCode": "HDFC",
  "accountNumber": "12345678901234",
  "ifscCode": "HDFC0001234",
  "accountHolderName": "John Doe"
}
Response: 201 Created
{
  "accountId": "uuid",
  "bankName": "HDFC Bank",
  "accountNumber": "***1234", // masked
  "status": "pending_verification"
}

POST /api/v1/users/verify-bank
Request:
{
  "accountId": "uuid",
  "otp": "123456" // sent to registered mobile
}
Response: 200 OK
{
  "accountId": "uuid",
  "status": "verified"
}

GET /api/v1/users/{userId}/accounts
Response: 200 OK
{
  "accounts": [
    {
      "accountId": "uuid",
      "bankName": "HDFC Bank",
      "accountNumber": "***1234",
      "isDefault": true,
      "status": "verified"
    }
  ]
}
```

### Payment APIs

```
POST /api/v1/payments/send
Request:
{
  "fromAccountId": "uuid",
  "toVpa": "receiver@paytm", // or phone, account number
  "amount": 1000.00,
  "currency": "INR",
  "note": "Dinner split",
  "pin": "1234" // encrypted
}
Response: 201 Created
{
  "transactionId": "uuid",
  "utr": "123456789012", // Unique Transaction Reference
  "status": "processing", // processing, success, failed
  "amount": 1000.00,
  "fromAccount": "***1234",
  "toVpa": "receiver@paytm",
  "timestamp": "2025-11-12T10:00:00Z"
}

GET /api/v1/payments/{transactionId}
Response: 200 OK
{
  "transactionId": "uuid",
  "utr": "123456789012",
  "status": "success",
  "amount": 1000.00,
  "fromAccount": "***1234",
  "toVpa": "receiver@paytm",
  "note": "Dinner split",
  "timestamp": "2025-11-12T10:00:00Z",
  "completedAt": "2025-11-12T10:00:03Z"
}

POST /api/v1/payments/request
Request:
{
  "fromVpa": "payer@paytm",
  "amount": 500.00,
  "note": "Rent payment"
}
Response: 201 Created
{
  "requestId": "uuid",
  "status": "pending",
  "expiresAt": "2025-11-13T10:00:00Z"
}

POST /api/v1/payments/requests/{requestId}/pay
POST /api/v1/payments/requests/{requestId}/decline

GET /api/v1/users/{userId}/transactions?page={page}&limit={limit}
Response: 200 OK
{
  "transactions": [
    {
      "transactionId": "uuid",
      "type": "sent", // sent, received
      "amount": 1000.00,
      "counterparty": "receiver@paytm",
      "status": "success",
      "timestamp": "2025-11-12T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

### QR Code APIs

```
POST /api/v1/qr/generate
Request:
{
  "accountId": "uuid",
  "amount": 1000.00, // optional, can be dynamic
  "note": "Payment for order #123"
}
Response: 201 Created
{
  "qrCode": "base64-encoded-image",
  "qrData": "upi://pay?pa=merchant@paytm&pn=Merchant&am=1000&cu=INR",
  "expiresAt": "2025-11-12T11:00:00Z"
}

POST /api/v1/qr/scan
Request:
{
  "qrData": "upi://pay?pa=merchant@paytm&pn=Merchant&am=1000&cu=INR",
  "fromAccountId": "uuid"
}
Response: 200 OK
{
  "payee": {
    "vpa": "merchant@paytm",
    "name": "Merchant Name"
  },
  "amount": 1000.00,
  "note": "Payment for order #123"
}
// User confirms and pays
```

### Merchant APIs

```
POST /api/v1/merchant/register
POST /api/v1/merchant/settlements
GET /api/v1/merchant/analytics
```

## 6. Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    vpa VARCHAR(100) UNIQUE NOT NULL, -- virtual payment address
    pin_hash VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    kyc_status VARCHAR(20) DEFAULT 'pending',
    daily_limit DECIMAL(15, 2) DEFAULT 100000.00,
    per_transaction_limit DECIMAL(15, 2) DEFAULT 100000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_vpa (vpa),
    INDEX idx_status (status)
);
```

### Bank_Accounts Table
```sql
CREATE TABLE bank_accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    bank_code VARCHAR(10) NOT NULL,
    bank_name VARCHAR(255) NOT NULL,
    account_number VARCHAR(50) NOT NULL, -- encrypted
    ifsc_code VARCHAR(20) NOT NULL,
    account_holder_name VARCHAR(255) NOT NULL,
    account_type VARCHAR(20) DEFAULT 'savings', -- savings, current
    is_default BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, verified, blocked
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, account_number),
    INDEX idx_user (user_id),
    INDEX idx_account (account_number),
    INDEX idx_status (status)
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    utr VARCHAR(50) UNIQUE NOT NULL, -- Unique Transaction Reference
    idempotency_key VARCHAR(255) UNIQUE,
    payer_user_id UUID NOT NULL REFERENCES users(user_id),
    payer_account_id UUID NOT NULL REFERENCES bank_accounts(account_id),
    payee_user_id UUID NOT NULL REFERENCES users(user_id),
    payee_account_id UUID NOT NULL REFERENCES bank_accounts(account_id),
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    status VARCHAR(20) DEFAULT 'initiated',
    /* Statuses: initiated, processing, success, failed, reversed */
    transaction_type VARCHAR(20) DEFAULT 'p2p', -- p2p, merchant, request
    note TEXT,
    failure_reason TEXT,
    risk_score INT,
    payer_balance_before DECIMAL(15, 2),
    payer_balance_after DECIMAL(15, 2),
    payee_balance_before DECIMAL(15, 2),
    payee_balance_after DECIMAL(15, 2),
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_utr (utr),
    INDEX idx_payer (payer_user_id),
    INDEX idx_payee (payee_user_id),
    INDEX idx_status (status),
    INDEX idx_initiated (initiated_at),
    INDEX idx_idempotency (idempotency_key),
    CONSTRAINT chk_amount CHECK (amount > 0)
);
```

### Ledger Table (Double-entry bookkeeping)
```sql
CREATE TABLE ledger_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL REFERENCES transactions(transaction_id),
    account_id UUID NOT NULL REFERENCES bank_accounts(account_id),
    debit DECIMAL(15, 2) DEFAULT 0,
    credit DECIMAL(15, 2) DEFAULT 0,
    balance DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    entry_type VARCHAR(20) NOT NULL, -- payment, reversal, fee
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction (transaction_id),
    INDEX idx_account (account_id),
    INDEX idx_created (created_at),
    CONSTRAINT chk_debit_or_credit CHECK (
        (debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)
    )
);
```

### Payment_Requests Table
```sql
CREATE TABLE payment_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requester_user_id UUID NOT NULL REFERENCES users(user_id),
    payer_user_id UUID NOT NULL REFERENCES users(user_id),
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    note TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, declined, expired
    transaction_id UUID REFERENCES transactions(transaction_id),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_requester (requester_user_id),
    INDEX idx_payer (payer_user_id),
    INDEX idx_status (status),
    INDEX idx_expires (expires_at)
);
```

### Mandates Table (Recurring payments)
```sql
CREATE TABLE mandates (
    mandate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payer_user_id UUID NOT NULL REFERENCES users(user_id),
    payer_account_id UUID NOT NULL REFERENCES bank_accounts(account_id),
    payee_vpa VARCHAR(100) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    frequency VARCHAR(20) NOT NULL, -- daily, weekly, monthly
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'active', -- active, paused, cancelled
    next_execution_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_payer (payer_user_id),
    INDEX idx_status (status),
    INDEX idx_next_execution (next_execution_date)
);
```

### Dispute Table
```sql
CREATE TABLE disputes (
    dispute_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL REFERENCES transactions(transaction_id),
    raised_by_user_id UUID NOT NULL REFERENCES users(user_id),
    reason VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'open', -- open, under_review, resolved, rejected
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    INDEX idx_transaction (transaction_id),
    INDEX idx_user (raised_by_user_id),
    INDEX idx_status (status)
);
```

### Fraud_Logs Table
```sql
CREATE TABLE fraud_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID REFERENCES transactions(transaction_id),
    user_id UUID REFERENCES users(user_id),
    fraud_type VARCHAR(50), -- velocity, amount_spike, geo_anomaly
    risk_score INT,
    details JSONB,
    action_taken VARCHAR(20), -- allowed, blocked, flagged
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction (transaction_id),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at)
);
```

### ACID Considerations

1. **Transaction Processing:**
   - SERIALIZABLE isolation level
   - No partial debits/credits
   - Atomic balance updates

2. **Double-Entry Bookkeeping:**
   - Every transaction creates 2 ledger entries
   - Sum of debits = Sum of credits (always)

3. **Idempotency:**
   - Prevent duplicate transactions
   - Use idempotency keys

4. **Balance Consistency:**
   - Verify balance before debit
   - Lock account during transaction

## 7. Core Components

### 7.1 Payment Service
**Core Transaction Flow:**

```python
def process_payment(payer_id, payee_id, amount, note, idempotency_key):
    # 1. Check idempotency
    existing_txn = check_idempotency(idempotency_key)
    if existing_txn:
        return existing_txn

    # 2. Validate users and accounts
    payer = get_user(payer_id)
    payee = get_user(payee_id)
    payer_account = get_default_account(payer_id)
    payee_account = get_default_account(payee_id)

    # 3. Check limits
    if not check_daily_limit(payer_id, amount):
        raise LimitExceededError()

    if not check_per_transaction_limit(payer_id, amount):
        raise LimitExceededError()

    # 4. Fraud check
    risk_score = fraud_detection_service.calculate_risk(
        payer_id, payee_id, amount
    )
    if risk_score > 80:
        raise FraudSuspectedError()

    # 5. BEGIN TRANSACTION
    with database.transaction(isolation='serializable'):
        # Lock accounts
        lock_account(payer_account.id)
        lock_account(payee_account.id)

        # Check balance
        balance = get_balance(payer_account.id)
        if balance < amount:
            raise InsufficientBalanceError()

        # Create transaction record
        txn = create_transaction(
            payer_id, payer_account.id,
            payee_id, payee_account.id,
            amount, status='processing'
        )

        # Debit payer
        debit_ledger_entry = create_ledger_entry(
            transaction_id=txn.id,
            account_id=payer_account.id,
            debit=amount,
            balance=balance - amount
        )

        # Credit payee
        payee_balance = get_balance(payee_account.id)
        credit_ledger_entry = create_ledger_entry(
            transaction_id=txn.id,
            account_id=payee_account.id,
            credit=amount,
            balance=payee_balance + amount
        )

        # Update transaction status
        update_transaction(txn.id, status='success')

        # COMMIT

    # 6. Post-processing (async)
    send_notification(payer_id, 'payment_sent', txn)
    send_notification(payee_id, 'payment_received', txn)

    # Update bank (if real-time integration)
    notify_bank_settlement(txn)

    return txn
```

### 7.2 Balance Management
**Real-time Balance:**

```sql
-- Calculate balance from ledger (source of truth)
SELECT SUM(credit) - SUM(debit) AS balance
FROM ledger_entries
WHERE account_id = ?;

-- Cached balance (Redis) for faster reads
SET balance:account:{account_id} {balance}
EXPIRE balance:account:{account_id} 300 -- 5 minutes

-- Balance validation before transaction
def get_balance(account_id):
    # Try cache first
    cached = redis.get(f'balance:account:{account_id}')
    if cached:
        return Decimal(cached)

    # Fallback to ledger
    balance = calculate_balance_from_ledger(account_id)

    # Update cache
    redis.setex(f'balance:account:{account_id}', 300, str(balance))

    return balance
```

### 7.3 Fraud Detection Service
**Real-time Risk Scoring:**

```python
def calculate_risk_score(payer_id, payee_id, amount):
    score = 0

    # 1. Velocity check (transactions per hour)
    recent_txns = count_recent_transactions(payer_id, hours=1)
    if recent_txns > 10:
        score += 30

    # 2. Amount anomaly
    avg_amount = get_average_transaction_amount(payer_id)
    if amount > avg_amount * 5:
        score += 25

    # 3. New payee
    if not is_frequent_payee(payer_id, payee_id):
        score += 15

    # 4. Geolocation anomaly
    current_location = get_user_location(payer_id)
    usual_location = get_usual_location(payer_id)
    if distance(current_location, usual_location) > 500:  # km
        score += 20

    # 5. Time anomaly (unusual hours)
    current_hour = datetime.now().hour
    if current_hour < 6 or current_hour > 22:
        score += 10

    # 6. ML model prediction
    ml_score = fraud_model.predict({
        'payer_id': payer_id,
        'amount': amount,
        'hour': current_hour,
        'payee_known': is_frequent_payee(payer_id, payee_id),
        ...
    })
    score += ml_score * 50

    return min(score, 100)
```

**Actions:**
- 0-40: Allow
- 41-70: Challenge (ask for OTP)
- 71-100: Block

### 7.4 Bank Integration Service
**Settlement with Banks:**

In UPI, transactions happen in two layers:
1. **Instant UPI Layer:** User sees instant credit
2. **Bank Settlement:** Actual bank-to-bank transfer (T+1)

```python
def settle_with_banks_daily():
    # Run at end of day
    for bank in all_banks:
        net_position = calculate_net_position(bank)

        if net_position > 0:
            # Bank owes us money (net credits > debits)
            request_settlement(bank, net_position)
        else:
            # We owe bank money (net debits > credits)
            initiate_payment(bank, abs(net_position))

def calculate_net_position(bank):
    # All transactions involving this bank
    credits = sum_credits_from_bank(bank)
    debits = sum_debits_to_bank(bank)
    return credits - debits
```

### 7.5 Notification Service
**Real-time Notifications:**

```python
def send_transaction_notification(user_id, event_type, transaction):
    # 1. Push notification (FCM)
    fcm.send(
        user_id=user_id,
        title='Payment Successful' if event_type == 'payment_sent' else 'Money Received',
        body=f'₹{transaction.amount} to {transaction.payee_vpa}',
        data={'transaction_id': transaction.id}
    )

    # 2. SMS (for high-value transactions)
    if transaction.amount > 10000:
        sms.send(
            phone=get_user_phone(user_id),
            message=f'Transaction of ₹{transaction.amount} completed. UTR: {transaction.utr}'
        )

    # 3. Email receipt
    email_queue.publish({
        'user_id': user_id,
        'template': 'transaction_receipt',
        'data': transaction
    })
```

### 7.6 Reconciliation Service
**Daily Reconciliation:**

```python
def daily_reconciliation():
    # 1. Verify ledger balance
    for account in all_accounts:
        ledger_balance = calculate_ledger_balance(account.id)
        expected_balance = account.balance  # cached

        if ledger_balance != expected_balance:
            alert('Balance mismatch', account.id, ledger_balance, expected_balance)

    # 2. Verify transaction totals
    total_credits = sum_all_ledger_credits(today)
    total_debits = sum_all_ledger_debits(today)

    if total_credits != total_debits:
        alert('Ledger imbalance', total_credits, total_debits)

    # 3. Bank reconciliation
    for bank in all_banks:
        our_records = get_bank_transactions(bank, today)
        bank_statement = fetch_bank_statement(bank, today)

        diff = reconcile(our_records, bank_statement)
        if diff:
            alert('Bank reconciliation issue', bank, diff)
```

### 7.7 QR Code Service
**QR Code Generation:**

```python
def generate_qr_code(account_id, amount=None, note=None):
    user = get_user_by_account(account_id)

    # UPI URL format
    qr_data = f'upi://pay?pa={user.vpa}&pn={user.name}'

    if amount:
        qr_data += f'&am={amount}&cu=INR'

    if note:
        qr_data += f'&tn={urllib.parse.quote(note)}'

    # Generate QR code image
    qr_image = qrcode.make(qr_data)

    # Upload to CDN
    qr_url = cdn.upload(qr_image)

    return {
        'qr_code': qr_url,
        'qr_data': qr_data,
        'expires_at': datetime.now() + timedelta(hours=1)
    }
```

## 8. Transaction Management & Consistency

### Payment Transaction (Atomic)

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Lock accounts (prevent concurrent updates)
SELECT account_id, user_id
FROM bank_accounts
WHERE account_id IN (:payer_account_id, :payee_account_id)
FOR UPDATE;

-- 2. Check payer balance
SELECT SUM(credit) - SUM(debit) AS balance
FROM ledger_entries
WHERE account_id = :payer_account_id;

-- Application checks: if balance < amount, ROLLBACK

-- 3. Create transaction record
INSERT INTO transactions (
    utr, payer_user_id, payer_account_id,
    payee_user_id, payee_account_id,
    amount, status
)
VALUES (
    :utr, :payer_user_id, :payer_account_id,
    :payee_user_id, :payee_account_id,
    :amount, 'processing'
)
RETURNING transaction_id;

-- 4. Debit payer (ledger entry)
INSERT INTO ledger_entries (
    transaction_id, account_id, debit, balance
)
VALUES (
    :transaction_id, :payer_account_id, :amount,
    :payer_balance - :amount
);

-- 5. Credit payee (ledger entry)
INSERT INTO ledger_entries (
    transaction_id, account_id, credit, balance
)
VALUES (
    :transaction_id, :payee_account_id, :amount,
    :payee_balance + :amount
);

-- 6. Update transaction status
UPDATE transactions
SET status = 'success', completed_at = NOW()
WHERE transaction_id = :transaction_id;

COMMIT;

-- 7. Invalidate cached balances
DELETE FROM redis WHERE key IN (
    'balance:account:{payer_account_id}',
    'balance:account:{payee_account_id}'
);

-- 8. Queue notifications (async)
```

### Handling Concurrency

**Scenario:** Two transactions from same account simultaneously

```
Transaction A: Send $100 to Alice (balance: $200)
Transaction B: Send $150 to Bob (concurrent)

With SERIALIZABLE isolation:
1. Transaction A locks account
2. Transaction B waits for lock
3. Transaction A debits $100 (balance now $100)
4. Transaction A commits
5. Transaction B acquires lock
6. Transaction B checks balance ($100 < $150)
7. Transaction B fails with insufficient balance
```

### Reversal Transaction

```sql
-- If transaction needs to be reversed
BEGIN TRANSACTION;

-- 1. Create reversal transaction
INSERT INTO transactions (
    utr, payer_user_id, payer_account_id,
    payee_user_id, payee_account_id,
    amount, status, transaction_type
)
VALUES (
    :reversal_utr, :original_payee, :original_payee_account,
    :original_payer, :original_payer_account,
    :amount, 'success', 'reversal'
);

-- 2. Reverse ledger entries
-- Credit original payer
INSERT INTO ledger_entries (
    transaction_id, account_id, credit, balance
)
VALUES (...);

-- Debit original payee
INSERT INTO ledger_entries (
    transaction_id, account_id, debit, balance
)
VALUES (...);

-- 3. Update original transaction
UPDATE transactions
SET status = 'reversed'
WHERE transaction_id = :original_transaction_id;

COMMIT;
```

## 9. Security Considerations

### Authentication
- **PIN-based:** 4-6 digit PIN (hashed with bcrypt)
- **Biometric:** Fingerprint, Face ID
- **Device binding:** Limit to registered devices
- **OTP:** For high-value or risky transactions

### Encryption
- **At rest:** AES-256 for sensitive data
- **In transit:** TLS 1.3
- **Account numbers:** Encrypted in database
- **PINs:** Bcrypt with high cost factor

### Transaction Security
- **Rate limiting:** Max 10 transactions per hour
- **Amount limits:** Per transaction, daily limits
- **Fraud detection:** ML-based real-time scoring
- **Geofencing:** Alert on location anomalies

### Device Security
- **Device registration:** Link device to account
- **Device fingerprinting:** Track device metadata
- **Jailbreak detection:** Block rooted/jailbroken devices
- **Certificate pinning:** Prevent MITM attacks

### API Security
- **JWT tokens:** Short-lived (15 minutes)
- **Refresh tokens:** Long-lived, rotated
- **Rate limiting:** Per user, per IP
- **Input validation:** Prevent injection attacks

## 10. Scalability

### Database Scaling

**Sharding:**
```
Users: Shard by user_id (consistent hashing)
Transactions: Shard by date (monthly partitions)
Ledger: Co-locate with transactions
```

**Read Replicas:**
- Transaction history to replicas
- Balance queries to cache (Redis)
- Writes to primary only

**Archival:**
- Move old transactions (> 1 year) to cold storage (S3)
- Keep in database for 2 years
- Archive in data warehouse for analytics

### Caching Strategy

```
Redis Cluster:
- User profiles (1 hour TTL)
- Account balances (5 min TTL)
- Recent transactions (15 min TTL)
- Fraud rules (10 min TTL)
- Daily limits tracking (24 hour TTL)
```

### Queue-Based Architecture

**Kafka Topics:**
- `transactions.initiated`
- `transactions.completed`
- `transactions.failed`
- `notifications.push`
- `notifications.sms`

**Benefits:**
- Decouple services
- Retry failed operations
- Event sourcing
- Real-time analytics

### Global Distribution

**Multi-Region:**
- Primary: India (Mumbai)
- Replicas: Delhi, Bangalore
- DR: Singapore

**Data Locality:**
- Transactions processed in user's region
- Replicate for disaster recovery

## 11. Trade-offs

### 1. Real-time vs Delayed Settlement

**UPI Approach:** Instant for user, T+1 for banks
- Pro: Great UX, instant feedback
- Con: Liquidity management, settlement risk

### 2. Strong vs Eventual Consistency

**Decision:** Strong consistency for transactions
- Pro: No double-spending, accurate balances
- Con: Higher latency, lower availability

### 3. Centralized vs Decentralized Ledger

**Centralized:**
- Pro: Simpler, faster, regulatory compliance
- Con: Single point of failure, trust required

### 4. In-app vs Bank Balance

**Decision:** In-app ledger, settle with banks periodically
- Pro: Instant UX, independent of bank APIs
- Con: Requires capital, regulatory oversight

## 12. Follow-up Questions

1. How would you handle cross-border payments?
2. How would you implement offline payments?
3. How would you handle currency conversion?
4. How would you implement autopay/mandates?
5. How would you handle disputes and chargebacks?
6. How would you scale to 100K TPS?
7. How would you implement merchant settlements?
8. How would you handle partial payments?
9. How would you implement multi-currency wallets?
10. How would you handle regulatory compliance (AML/KYC)?
11. How would you implement payment splitting?
12. How would you handle wallet-to-bank transfers?
13. How would you implement cashback and rewards?
14. How would you handle payment reversals?
15. How would you implement bank statement generation?

---

**Key Takeaways:**
- Strong consistency is non-negotiable for payments
- Double-entry bookkeeping ensures accuracy
- Real-time fraud detection prevents losses
- Idempotency prevents duplicate transactions
- Ledger is the source of truth
- Settlement with banks can be async
- Security and compliance are critical
