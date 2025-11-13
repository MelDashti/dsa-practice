# Design Digital Wallet

## 1. Problem Statement

Design a digital wallet system like PayPal, Apple Pay, or Google Pay that allows users to store money, make payments, transfer funds, and manage multiple payment methods. The system must support wallet-to-wallet transfers, merchant payments, currency conversion, transaction history, and integration with banks and card networks while ensuring strong consistency, security, and compliance.

**Key Features:**
- Wallet balance management
- Add money from bank/card
- Withdraw to bank account
- Peer-to-peer transfers
- Merchant payments (online/offline)
- QR code payments
- Multiple currencies
- Transaction history
- Cashback and rewards
- Recurring payments
- Split payments
- Request money

## 2. Requirements

### Functional Requirements

1. **Wallet Management**
   - Create wallet account
   - Add money from bank account/card
   - Withdraw to bank account
   - View balance (multiple currencies)
   - Transaction limits

2. **Payment Methods**
   - Link bank accounts
   - Add credit/debit cards
   - Set default payment method
   - Remove/update payment methods

3. **Transfers**
   - Wallet-to-wallet transfer
   - Send money to email/phone
   - Request money
   - Split bills
   - Scheduled transfers

4. **Merchant Payments**
   - Pay merchants (online/offline)
   - QR code scanning
   - One-click checkout
   - Payment integration APIs

5. **Currency Management**
   - Multi-currency wallets
   - Currency conversion
   - Real-time exchange rates
   - Auto-conversion

6. **Transaction Management**
   - Transaction history
   - Search and filter
   - Export statements
   - Receipts and invoices
   - Refunds and reversals

7. **Rewards & Offers**
   - Cashback
   - Loyalty points
   - Promotional offers
   - Referral bonuses

8. **Security**
   - PIN/biometric authentication
   - Two-factor authentication
   - Transaction alerts
   - Fraud detection
   - Account freeze

### Non-Functional Requirements

1. **Performance**
   - Transaction processing < 2 seconds (p95)
   - API response time < 100ms
   - Handle 50K TPS
   - Real-time balance updates

2. **Availability**
   - 99.99% uptime
   - Multi-region deployment
   - No data loss
   - Disaster recovery

3. **Consistency**
   - Strong consistency for wallet balance
   - ACID transactions
   - No double-spending
   - Exactly-once processing

4. **Scalability**
   - Support 1B+ users
   - 100B+ transactions per year
   - Multi-currency (150+ currencies)
   - Global deployment

5. **Security**
   - PCI DSS compliance
   - End-to-end encryption
   - Fraud detection (ML-based)
   - AML/KYC compliance
   - Tokenization

6. **Reliability**
   - Data durability (11 nines)
   - Automated backups
   - Reconciliation
   - Audit logs

## 3. Scale Estimation

### Traffic Estimates
- **Active users:** 1 billion
- **Daily active users:** 200 million
- **Transactions per day:** 500 million
- **Average TPS:** 5,787
- **Peak TPS:** 50,000

### Transaction Estimates
- **Average transaction value:** $25
- **Daily transaction volume:** $12.5 billion
- **Annual transaction volume:** $4.5 trillion
- **Wallet balance (total):** $500 billion

### Storage Estimates
- **Users:** 1B × 5 KB = 5 TB
- **Wallets:** 1B × 10 KB = 10 TB
- **Payment methods:** 2B cards × 1 KB = 2 TB
- **Transactions:** 500M/day × 365 days × 5 KB = 912 TB/year
- **Ledger:** 1B entries/day × 1 KB = 365 TB/year
- **Total (Year 1):** ~1.3 PB

### Bandwidth Estimates
- **Incoming:** 500M transactions × 5 KB = 2.5 TB/day
- **Outgoing:** 1B API calls × 3 KB = 3 TB/day
- **Total:** ~5.5 TB/day

### Database Estimates
- **Reads per second:** 200K
- **Writes per second:** 50K
- **Database size:** 1.5 PB
- **Hot data (cached):** 50 TB

## 4. High-Level Architecture

```
                          ┌──────────────┐
                          │   Mobile/    │
                          │     Web      │
                          └──────┬───────┘
                                 │ HTTPS
                                 ▼
                          ┌──────────────┐
                          │  API Gateway │
                          │ (Auth, Rate  │
                          │  Limiting)   │
                          └──────┬───────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│    Wallet     │        │   Payment     │      │     User      │
│   Service     │        │   Service     │      │   Service     │
└───────┬───────┘        └───────┬───────┘      └───────┬───────┘
        │                        │                       │
        ▼                        ▼                       ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│    Ledger     │        │  Transaction  │      │  Merchant     │
│   Service     │        │   Service     │      │   Service     │
└───────┬───────┘        └───────┬───────┘      └───────────────┘
        │                        │
        ▼                        ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│   Currency    │        │     Fraud     │      │  Notification │
│   Service     │        │   Detection   │      │   Service     │
└───────────────┘        └───────────────┘      └───────────────┘
        │
        ▼
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│   Rewards     │        │  Settlement   │      │Reconciliation │
│   Service     │        │   Service     │      │   Service     │
└───────────────┘        └───────────────┘      └───────────────┘

                        Data Layer
┌──────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │PostgreSQL│  │PostgreSQL│  │PostgreSQL│  │  Redis   │ │
│  │ (Wallets)│  │(Payments)│  │ (Ledger) │  │ (Cache)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Kafka   │  │   SQS    │  │    S3    │  │TimescaleDB│
│  │ (Events) │  │ (Queue)  │  │  (Docs)  │  │ (Metrics) │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────┘

                External Services
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   Bank   │  │   Card   │  │ Exchange │  │   KYC    │
│   APIs   │  │ Networks │  │   Rate   │  │ Service  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 5. API Design

### Wallet APIs

```
POST /api/v1/wallets
Request:
{
  "userId": "uuid",
  "currency": "USD",
  "type": "personal" // personal, business
}
Response: 201 Created
{
  "walletId": "uuid",
  "userId": "uuid",
  "balance": 0.00,
  "currency": "USD",
  "status": "active"
}

GET /api/v1/wallets/{walletId}
Response: 200 OK
{
  "walletId": "uuid",
  "balance": 1250.50,
  "currency": "USD",
  "availableBalance": 1250.50,
  "pendingBalance": 0.00,
  "createdAt": "2025-01-01T00:00:00Z"
}

POST /api/v1/wallets/{walletId}/add-money
Request:
{
  "amount": 100.00,
  "currency": "USD",
  "source": {
    "type": "card", // or "bank_account"
    "paymentMethodId": "pm_xxx"
  },
  "description": "Add money to wallet"
}
Response: 201 Created
{
  "transactionId": "uuid",
  "status": "processing",
  "amount": 100.00,
  "currency": "USD",
  "estimatedCompletion": "2025-11-12T10:05:00Z"
}

POST /api/v1/wallets/{walletId}/withdraw
Request:
{
  "amount": 50.00,
  "currency": "USD",
  "destination": {
    "type": "bank_account",
    "bankAccountId": "ba_xxx"
  }
}
Response: 201 Created
{
  "transactionId": "uuid",
  "status": "processing",
  "amount": 50.00,
  "fee": 1.00,
  "netAmount": 49.00,
  "estimatedArrival": "2025-11-15T00:00:00Z"
}
```

### Payment Method APIs

```
POST /api/v1/payment-methods
Request:
{
  "type": "card",
  "card": {
    "number": "4242424242424242",
    "expMonth": 12,
    "expYear": 2025,
    "cvc": "123"
  },
  "billingAddress": {...}
}
Response: 201 Created
{
  "paymentMethodId": "pm_xxx",
  "type": "card",
  "card": {
    "brand": "visa",
    "last4": "4242",
    "expMonth": 12,
    "expYear": 2025
  },
  "status": "active"
}

GET /api/v1/payment-methods
Response: 200 OK
{
  "paymentMethods": [
    {
      "paymentMethodId": "pm_xxx",
      "type": "card",
      "card": {...},
      "isDefault": true
    },
    {
      "paymentMethodId": "ba_xxx",
      "type": "bank_account",
      "bankAccount": {...},
      "isDefault": false
    }
  ]
}

DELETE /api/v1/payment-methods/{id}
```

### Transfer APIs

```
POST /api/v1/transfers
Request:
{
  "fromWalletId": "uuid",
  "toIdentifier": "user@email.com", // or phone, walletId
  "amount": 25.00,
  "currency": "USD",
  "note": "Lunch money",
  "pin": "1234" // encrypted
}
Response: 201 Created
{
  "transferId": "uuid",
  "status": "completed",
  "amount": 25.00,
  "fee": 0.00,
  "recipient": {
    "name": "Jane Doe",
    "identifier": "user@email.com"
  },
  "completedAt": "2025-11-12T10:00:01Z"
}

POST /api/v1/transfers/request
Request:
{
  "fromIdentifier": "payer@email.com",
  "amount": 50.00,
  "currency": "USD",
  "note": "Rent payment"
}
Response: 201 Created
{
  "requestId": "uuid",
  "status": "pending",
  "expiresAt": "2025-11-19T10:00:00Z"
}

POST /api/v1/transfers/requests/{requestId}/fulfill
POST /api/v1/transfers/requests/{requestId}/decline
```

### Merchant Payment APIs

```
POST /api/v1/payments
Request:
{
  "walletId": "uuid",
  "merchantId": "merchant_xxx",
  "amount": 99.99,
  "currency": "USD",
  "orderId": "order_123",
  "description": "Purchase from Store XYZ"
}
Response: 201 Created
{
  "paymentId": "uuid",
  "status": "success",
  "amount": 99.99,
  "cashback": 1.00,
  "finalAmount": 98.99,
  "receipt": "https://receipts.example.com/xxx.pdf"
}

POST /api/v1/payments/{paymentId}/refund
Request:
{
  "amount": 99.99, // full or partial
  "reason": "Customer request"
}
Response: 200 OK
{
  "refundId": "uuid",
  "status": "processing",
  "amount": 99.99,
  "estimatedCompletion": "2025-11-14T00:00:00Z"
}
```

### Transaction APIs

```
GET /api/v1/wallets/{walletId}/transactions?page=1&limit=20&type=sent,received
Response: 200 OK
{
  "transactions": [
    {
      "transactionId": "uuid",
      "type": "sent",
      "amount": 25.00,
      "currency": "USD",
      "counterparty": {
        "name": "Jane Doe",
        "identifier": "user@email.com"
      },
      "status": "completed",
      "timestamp": "2025-11-12T10:00:00Z"
    }
  ],
  "pagination": {...}
}

GET /api/v1/transactions/{id}
POST /api/v1/transactions/export
```

### Currency APIs

```
GET /api/v1/currencies/rates?base=USD&target=EUR,GBP,INR
Response: 200 OK
{
  "base": "USD",
  "rates": {
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.12
  },
  "timestamp": "2025-11-12T10:00:00Z"
}

POST /api/v1/wallets/{walletId}/convert
Request:
{
  "fromCurrency": "USD",
  "toCurrency": "EUR",
  "amount": 100.00
}
Response: 200 OK
{
  "conversionId": "uuid",
  "fromAmount": 100.00,
  "fromCurrency": "USD",
  "toAmount": 92.00,
  "toCurrency": "EUR",
  "exchangeRate": 0.92,
  "fee": 1.00
}
```

## 6. Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    name VARCHAR(255) NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    kyc_status VARCHAR(20) DEFAULT 'pending',
    kyc_verified_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_phone (phone)
);
```

### Wallets Table
```sql
CREATE TABLE wallets (
    wallet_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    currency VARCHAR(3) NOT NULL,
    balance DECIMAL(20, 2) DEFAULT 0.00,
    available_balance DECIMAL(20, 2) DEFAULT 0.00,
    pending_balance DECIMAL(20, 2) DEFAULT 0.00,
    wallet_type VARCHAR(20) DEFAULT 'personal', -- personal, business, merchant
    status VARCHAR(20) DEFAULT 'active',
    daily_limit DECIMAL(20, 2) DEFAULT 10000.00,
    version INT DEFAULT 0, -- for optimistic locking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, currency),
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    CONSTRAINT chk_balance CHECK (balance >= 0),
    CONSTRAINT chk_available_balance CHECK (available_balance >= 0)
);
```

### Payment_Methods Table
```sql
CREATE TABLE payment_methods (
    payment_method_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    type VARCHAR(20) NOT NULL, -- card, bank_account
    token VARCHAR(255) UNIQUE NOT NULL, -- tokenized
    card_brand VARCHAR(20),
    card_last4 VARCHAR(4),
    card_exp_month INT,
    card_exp_year INT,
    bank_name VARCHAR(255),
    bank_account_last4 VARCHAR(4),
    bank_routing_number VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_token (token),
    INDEX idx_status (status)
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key VARCHAR(255) UNIQUE,
    transaction_type VARCHAR(30) NOT NULL,
    /* Types: add_money, withdraw, transfer, merchant_payment, refund, conversion */
    from_wallet_id UUID REFERENCES wallets(wallet_id),
    to_wallet_id UUID REFERENCES wallets(wallet_id),
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    fee DECIMAL(20, 2) DEFAULT 0.00,
    net_amount DECIMAL(20, 2) NOT NULL,
    exchange_rate DECIMAL(20, 10),
    status VARCHAR(20) DEFAULT 'initiated',
    /* Statuses: initiated, processing, completed, failed, reversed */
    payment_method_id UUID REFERENCES payment_methods(payment_method_id),
    merchant_id UUID,
    order_id VARCHAR(255),
    description TEXT,
    metadata JSONB,
    failure_reason TEXT,
    risk_score INT,
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_from_wallet (from_wallet_id),
    INDEX idx_to_wallet (to_wallet_id),
    INDEX idx_status (status),
    INDEX idx_merchant (merchant_id),
    INDEX idx_idempotency (idempotency_key),
    INDEX idx_initiated (initiated_at),
    CONSTRAINT chk_amount CHECK (amount > 0)
);
```

### Ledger Table (Double-entry bookkeeping)
```sql
CREATE TABLE ledger_entries (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL REFERENCES transactions(transaction_id),
    wallet_id UUID NOT NULL REFERENCES wallets(wallet_id),
    debit DECIMAL(20, 2) DEFAULT 0.00,
    credit DECIMAL(20, 2) DEFAULT 0.00,
    balance DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    entry_type VARCHAR(30) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction (transaction_id),
    INDEX idx_wallet (wallet_id),
    INDEX idx_created (created_at),
    CONSTRAINT chk_debit_or_credit CHECK (
        (debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)
    )
);
```

### Money_Requests Table
```sql
CREATE TABLE money_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requester_user_id UUID NOT NULL REFERENCES users(user_id),
    payer_user_id UUID REFERENCES users(user_id),
    payer_identifier VARCHAR(255) NOT NULL, -- email or phone
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    note TEXT,
    status VARCHAR(20) DEFAULT 'pending',
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

### Rewards Table
```sql
CREATE TABLE rewards (
    reward_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    wallet_id UUID NOT NULL REFERENCES wallets(wallet_id),
    reward_type VARCHAR(30) NOT NULL, -- cashback, referral, promotional
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    source_transaction_id UUID REFERENCES transactions(transaction_id),
    status VARCHAR(20) DEFAULT 'pending',
    credited_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_wallet (wallet_id),
    INDEX idx_status (status)
);
```

### Merchants Table
```sql
CREATE TABLE merchants (
    merchant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name VARCHAR(500) NOT NULL,
    business_email VARCHAR(255) UNIQUE NOT NULL,
    wallet_id UUID NOT NULL REFERENCES wallets(wallet_id),
    merchant_category VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    api_key VARCHAR(255) UNIQUE,
    settlement_frequency VARCHAR(20) DEFAULT 'daily',
    commission_rate DECIMAL(5, 2) DEFAULT 2.5, -- percentage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_wallet (wallet_id),
    INDEX idx_api_key (api_key)
);
```

### Currency_Conversion_Rates Table
```sql
CREATE TABLE currency_rates (
    rate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate DECIMAL(20, 10) NOT NULL,
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(base_currency, target_currency, valid_from),
    INDEX idx_currencies (base_currency, target_currency),
    INDEX idx_valid (valid_from, valid_until)
);
```

### ACID Considerations

1. **Wallet Balance Updates:**
   - Optimistic locking with version numbers
   - Prevent negative balances
   - Atomic debit-credit operations

2. **Double-Entry Ledger:**
   - Every transaction creates 2+ ledger entries
   - Sum of all debits = Sum of all credits
   - Immutable (no updates, only inserts)

3. **Idempotency:**
   - Use idempotency keys
   - Prevent duplicate transactions
   - Return same result for duplicate requests

## 7. Core Components

### 7.1 Wallet Service
**Balance Management:**

```python
def get_wallet_balance(wallet_id):
    # Check cache first
    cached = redis.get(f'wallet:balance:{wallet_id}')
    if cached:
        return Decimal(cached)

    # Calculate from ledger (source of truth)
    balance = db.execute("""
        SELECT SUM(credit) - SUM(debit) AS balance
        FROM ledger_entries
        WHERE wallet_id = %s
    """, [wallet_id])[0]['balance']

    # Update cache
    redis.setex(f'wallet:balance:{wallet_id}', 300, str(balance))

    return balance
```

**Add Money to Wallet:**

```python
def add_money_to_wallet(wallet_id, amount, payment_method_id):
    with db.transaction(isolation='serializable'):
        # 1. Charge payment method (via payment gateway)
        charge = payment_gateway.charge(
            payment_method_id,
            amount,
            description='Add money to wallet'
        )

        if charge.status != 'succeeded':
            raise PaymentFailedError()

        # 2. Create transaction
        txn = create_transaction(
            type='add_money',
            to_wallet_id=wallet_id,
            amount=amount,
            payment_method_id=payment_method_id,
            status='completed'
        )

        # 3. Credit wallet (ledger entry)
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=wallet_id,
            credit=amount,
            balance=get_balance(wallet_id) + amount
        )

        # 4. Update wallet balance
        update_wallet_balance(wallet_id, amount, operation='add')

    # Invalidate cache
    redis.delete(f'wallet:balance:{wallet_id}')

    return txn
```

### 7.2 Transfer Service
**Wallet-to-Wallet Transfer:**

```python
def transfer_money(from_wallet_id, to_identifier, amount, note):
    # 1. Resolve recipient
    to_wallet = resolve_wallet(to_identifier)  # email, phone, or wallet_id

    # 2. Fraud check
    risk_score = fraud_service.check_transfer(from_wallet_id, to_wallet.id, amount)
    if risk_score > 80:
        raise FraudSuspectedError()

    # 3. Check limits
    if not check_daily_limit(from_wallet_id, amount):
        raise DailyLimitExceededError()

    # 4. BEGIN TRANSACTION
    with db.transaction(isolation='serializable'):
        # Lock wallets
        lock_wallet(from_wallet_id)
        lock_wallet(to_wallet.id)

        # Check balance
        from_balance = get_wallet_balance(from_wallet_id)
        if from_balance < amount:
            raise InsufficientBalanceError()

        # Create transaction
        txn = create_transaction(
            type='transfer',
            from_wallet_id=from_wallet_id,
            to_wallet_id=to_wallet.id,
            amount=amount,
            note=note,
            status='completed'
        )

        # Debit sender
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=from_wallet_id,
            debit=amount,
            balance=from_balance - amount
        )

        # Credit recipient
        to_balance = get_wallet_balance(to_wallet.id)
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=to_wallet.id,
            credit=amount,
            balance=to_balance + amount
        )

        # Update wallet balances
        update_wallet_balance(from_wallet_id, amount, operation='subtract')
        update_wallet_balance(to_wallet.id, amount, operation='add')

    # Post-processing
    invalidate_balance_cache(from_wallet_id)
    invalidate_balance_cache(to_wallet.id)
    send_notifications(from_wallet_id, to_wallet.id, txn)

    # Check for rewards
    calculate_cashback(txn)

    return txn
```

### 7.3 Currency Conversion Service

```python
def convert_currency(wallet_id, from_currency, to_currency, amount):
    # 1. Get current exchange rate
    rate = get_exchange_rate(from_currency, to_currency)

    # 2. Calculate converted amount
    converted_amount = amount * rate
    conversion_fee = converted_amount * 0.01  # 1% fee
    net_amount = converted_amount - conversion_fee

    # 3. Check if user has both currency wallets
    from_wallet = get_wallet(wallet_id, from_currency)
    to_wallet = get_or_create_wallet(wallet_id, to_currency)

    # 4. Perform conversion transaction
    with db.transaction(isolation='serializable'):
        # Check balance
        balance = get_wallet_balance(from_wallet.id)
        if balance < amount:
            raise InsufficientBalanceError()

        # Create transaction
        txn = create_transaction(
            type='conversion',
            from_wallet_id=from_wallet.id,
            to_wallet_id=to_wallet.id,
            amount=amount,
            currency=from_currency,
            exchange_rate=rate,
            fee=conversion_fee,
            net_amount=net_amount,
            status='completed'
        )

        # Debit source wallet
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=from_wallet.id,
            debit=amount,
            currency=from_currency,
            balance=balance - amount
        )

        # Credit destination wallet
        to_balance = get_wallet_balance(to_wallet.id)
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=to_wallet.id,
            credit=net_amount,
            currency=to_currency,
            balance=to_balance + net_amount
        )

    return txn
```

### 7.4 Merchant Payment Service

```python
def process_merchant_payment(wallet_id, merchant_id, amount, order_id):
    # 1. Get merchant details
    merchant = get_merchant(merchant_id)

    # 2. Check for cashback offers
    cashback = calculate_merchant_cashback(merchant_id, amount)

    # 3. Final amount after cashback
    final_amount = amount - cashback

    # 4. Process payment
    with db.transaction(isolation='serializable'):
        # Debit customer wallet
        customer_wallet = get_wallet_by_id(wallet_id)
        balance = get_wallet_balance(wallet_id)

        if balance < final_amount:
            raise InsufficientBalanceError()

        txn = create_transaction(
            type='merchant_payment',
            from_wallet_id=wallet_id,
            to_wallet_id=merchant.wallet_id,
            amount=amount,
            merchant_id=merchant_id,
            order_id=order_id,
            status='completed'
        )

        # Ledger entries
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=wallet_id,
            debit=final_amount,
            balance=balance - final_amount
        )

        merchant_balance = get_wallet_balance(merchant.wallet_id)
        create_ledger_entry(
            transaction_id=txn.id,
            wallet_id=merchant.wallet_id,
            credit=final_amount,
            balance=merchant_balance + final_amount
        )

        # Credit cashback if applicable
        if cashback > 0:
            credit_cashback_reward(wallet_id, cashback, txn.id)

    return txn
```

### 7.5 Fraud Detection

```python
def calculate_fraud_score(transaction):
    score = 0

    # Velocity checks
    recent_count = count_recent_transactions(
        transaction.from_wallet_id,
        hours=1
    )
    if recent_count > 20:
        score += 40

    # Amount anomaly
    avg_amount = get_average_transaction_amount(transaction.from_wallet_id)
    if transaction.amount > avg_amount * 10:
        score += 30

    # New recipient
    if not is_known_recipient(transaction.from_wallet_id, transaction.to_wallet_id):
        score += 15

    # Device fingerprint
    if not is_trusted_device(transaction.user_id, transaction.device_id):
        score += 10

    # ML model
    ml_score = fraud_model.predict(transaction)
    score += ml_score * 20

    return min(score, 100)
```

### 7.6 Rewards Service

```python
def calculate_cashback(transaction):
    # Different cashback rates for different merchants
    merchant_id = transaction.merchant_id
    amount = transaction.amount

    cashback_rate = get_merchant_cashback_rate(merchant_id)
    cashback_amount = amount * cashback_rate

    # Cap cashback
    max_cashback = 50.00  # $50 max
    cashback_amount = min(cashback_amount, max_cashback)

    # Create reward
    reward = create_reward(
        user_id=transaction.user_id,
        wallet_id=transaction.from_wallet_id,
        type='cashback',
        amount=cashback_amount,
        source_transaction_id=transaction.id
    )

    # Credit wallet
    credit_reward_to_wallet(reward)

    return reward
```

## 8. Transaction Management & Consistency

### Transfer Transaction (Complete Flow)

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Check idempotency
SELECT transaction_id FROM transactions
WHERE idempotency_key = ?;

-- If exists, return (idempotent)

-- 2. Lock wallets
SELECT wallet_id, balance, version
FROM wallets
WHERE wallet_id IN (?, ?)
FOR UPDATE;

-- 3. Verify sender balance
SELECT SUM(credit) - SUM(debit) AS balance
FROM ledger_entries
WHERE wallet_id = ?;

-- Application checks: if balance < amount, ROLLBACK

-- 4. Create transaction
INSERT INTO transactions (
    idempotency_key, transaction_type,
    from_wallet_id, to_wallet_id,
    amount, currency, status
)
VALUES (?, 'transfer', ?, ?, ?, ?, 'completed')
RETURNING transaction_id;

-- 5. Debit sender ledger
INSERT INTO ledger_entries (
    transaction_id, wallet_id, debit, balance, currency
)
VALUES (?, ?, ?, ?, ?);

-- 6. Credit recipient ledger
INSERT INTO ledger_entries (
    transaction_id, wallet_id, credit, balance, currency
)
VALUES (?, ?, ?, ?, ?);

-- 7. Update wallet balances (optimistic locking)
UPDATE wallets
SET balance = balance - ?,
    available_balance = available_balance - ?,
    version = version + 1
WHERE wallet_id = ? AND version = ?;

UPDATE wallets
SET balance = balance + ?,
    available_balance = available_balance + ?,
    version = version + 1
WHERE wallet_id = ? AND version = ?;

COMMIT;

-- 8. Clear cache
-- 9. Send notifications
-- 10. Calculate rewards
```

## 9. Security Considerations

### Authentication
- **PIN/Biometric:** Transaction authentication
- **2FA:** OTP for high-value transactions
- **Device binding:** Limit to registered devices

### Encryption
- **At rest:** AES-256
- **In transit:** TLS 1.3
- **PINs:** Bcrypt with high cost factor
- **Payment methods:** Tokenized

### Fraud Prevention
- **ML-based risk scoring**
- **Velocity limits**
- **Device fingerprinting**
- **Behavioral analysis**
- **Geolocation checks**

### Compliance
- **PCI DSS Level 1**
- **AML/KYC verification**
- **Transaction monitoring**
- **Suspicious activity reporting**

## 10. Scalability

### Database Sharding
- Shard by user_id (consistent hashing)
- Co-locate user's wallets and transactions
- Cross-shard queries minimized

### Caching
- Balance cache (5 min TTL)
- User profiles (1 hour TTL)
- Exchange rates (1 min TTL)
- Fraud rules (10 min TTL)

### Queue-Based Architecture
- Kafka for events
- SQS for async tasks
- Notifications queue
- Rewards calculation queue

## 11. Trade-offs

### 1. Balance Storage
**Denormalized (wallet table) vs Calculated (ledger)**
- Store in wallet: Faster reads
- Calculate from ledger: Guaranteed accuracy
- Solution: Both (wallet for cache, ledger as source of truth)

### 2. Currency Conversion
**Real-time vs Pre-conversion**
- Real-time: Best rates, complex
- Pre-conversion: Simple, rate risk
- Solution: Real-time with caching

### 3. Settlement
**Instant vs Batched**
- Instant: Great UX, complex
- Batched: Simpler, delayed
- Solution: Instant for users, batch settle with banks

## 12. Follow-up Questions

1. How would you implement multi-signature wallets?
2. How would you handle cryptocurrency support?
3. How would you implement savings accounts with interest?
4. How would you handle chargebacks?
5. How would you implement peer-to-peer lending?
6. How would you scale to support 1B+ users?
7. How would you handle regulatory compliance across countries?
8. How would you implement automated investment features?
9. How would you handle wallet freezing/unfreezing?
10. How would you implement bill splitting with multiple users?

---

**Key Takeaways:**
- Double-entry bookkeeping ensures accuracy
- Strong consistency for wallet balances
- Fraud detection is critical
- Multi-currency requires careful design
- Rewards and cashback drive engagement
- Security and compliance are non-negotiable
