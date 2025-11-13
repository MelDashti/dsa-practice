# Design Stock Exchange / Trading Platform

## 1. Problem Statement

Design a real-time stock trading platform like NASDAQ or NYSE that enables users to buy and sell stocks, bonds, and other securities. The system must handle high-frequency trading with ultra-low latency, maintain an order book, execute trades using a matching engine, ensure fairness, provide real-time market data, handle settlements, and comply with financial regulations.

**Key Features:**
- Order placement (market, limit, stop-loss)
- Order book management
- Trade matching engine
- Real-time market data streaming
- Portfolio management
- Trade settlement and clearing
- Risk management
- Regulatory compliance
- Historical data and analytics
- Market surveillance (fraud detection)

## 2. Requirements

### Functional Requirements

1. **Trading**
   - Place orders (market, limit, stop-loss, trailing stop)
   - Cancel/modify pending orders
   - Match buy and sell orders
   - Execute trades
   - Support multiple asset types (stocks, bonds, futures, options)

2. **Order Book**
   - Maintain buy/sell order book per symbol
   - Real-time order book updates
   - Price-time priority matching
   - Order book depth (Level 2 data)

3. **Market Data**
   - Real-time quotes (bid/ask)
   - Trade execution feed
   - Candlestick data (OHLCV)
   - Market depth
   - Top of book (best bid/ask)

4. **Portfolio Management**
   - View holdings
   - Track P&L (Profit & Loss)
   - Transaction history
   - Performance analytics

5. **Risk Management**
   - Position limits
   - Margin requirements
   - Circuit breakers (halt trading)
   - Pre-trade risk checks

6. **Settlement & Clearing**
   - T+2 settlement
   - Fund transfers
   - Share transfers
   - Clearing house integration

7. **Regulatory & Compliance**
   - Trade reporting
   - Audit logs
   - Market surveillance
   - KYC/AML checks
   - Insider trading detection

### Non-Functional Requirements

1. **Performance**
   - Order placement latency: < 1ms (p99)
   - Matching engine latency: < 100 microseconds
   - Market data latency: < 10ms
   - Handle 100K orders per second
   - Support 1M concurrent users

2. **Availability**
   - 99.99% uptime during market hours
   - No data loss
   - Disaster recovery (RPO < 1s, RTO < 1 min)

3. **Consistency**
   - Strong consistency for order matching
   - ACID transactions for trades
   - Exactly-once order execution
   - No double execution

4. **Scalability**
   - Support 10K+ symbols
   - 100M+ orders per day
   - Petabytes of historical data
   - Global deployment

5. **Latency**
   - Ultra-low latency (microseconds)
   - Co-location for HFT (High-Frequency Trading)
   - Deterministic performance

6. **Fairness**
   - Price-time priority
   - No preferential treatment
   - Market surveillance
   - Level playing field

## 3. Scale Estimation

### Traffic Estimates
- **Active traders:** 10 million
- **Concurrent users:** 1 million (peak)
- **Orders per day:** 100 million
- **Trades per day:** 50 million
- **Peak order rate:** 100K orders/second

### Market Data
- **Symbols traded:** 10,000
- **Market data updates:** 1M per second
- **WebSocket connections:** 1M concurrent

### Storage Estimates
- **Orders:** 100M/day × 365 days × 500 bytes = 18 TB/year
- **Trades:** 50M/day × 365 days × 1 KB = 18 TB/year
- **Market data (tick):** 1M updates/sec × 100 bytes × 86400 sec = 8.6 TB/day
- **User data:** 10M users × 10 KB = 100 GB
- **Historical data:** 100 TB (multi-year)
- **Total (Year 1):** ~3.5 PB

### Latency Requirements
- **Order submission to acknowledgment:** < 1ms
- **Order to matching:** < 100 microseconds
- **Matching to execution:** < 100 microseconds
- **Execution to market data:** < 1ms
- **End-to-end:** < 3ms

## 4. High-Level Architecture

```
                    ┌──────────────────────┐
                    │   Trading Client     │
                    │  (Desktop/Mobile)    │
                    └──────────┬───────────┘
                               │ WebSocket/FIX
                               ▼
                    ┌──────────────────────┐
                    │    API Gateway       │
                    │  (Order Validation)  │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐      ┌───────────────┐    ┌───────────────┐
│     Order     │      │   Matching    │    │  Market Data  │
│  Management   │      │    Engine     │    │   Service     │
│   Service     │      │ (In-Memory)   │    │               │
└───────┬───────┘      └───────┬───────┘    └───────┬───────┘
        │                      │                     │
        ▼                      ▼                     ▼
┌───────────────┐      ┌───────────────┐    ┌───────────────┐
│   Portfolio   │      │  Settlement   │    │  Risk Mgmt    │
│   Service     │      │   Service     │    │   Service     │
└───────────────┘      └───────────────┘    └───────────────┘
        │                      │                     │
        ▼                      ▼                     ▼
┌───────────────┐      ┌───────────────┐    ┌───────────────┐
│  Historical   │      │ Surveillance  │    │  Compliance   │
│Data Service   │      │   Service     │    │   Service     │
└───────────────┘      └───────────────┘    └───────────────┘

                        Data Layer
┌──────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Redis   │  │PostgreSQL│  │TimescaleDB│ │  Kafka   │ │
│  │(OrderBook)│ │ (Orders) │  │(MarketData)│ │ (Events) │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Cassandra │  │   S3     │  │ElasticCache│ │MemoryDB  │ │
│  │ (Trades) │  │ (Archive)│  │  (Cache)  │  │ (HotData)│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────┘
```

## 5. API Design

### Order APIs (FIX Protocol)

```
POST /api/v1/orders
Request:
{
  "symbol": "AAPL",
  "side": "BUY", // BUY or SELL
  "orderType": "LIMIT", // MARKET, LIMIT, STOP_LOSS, TRAILING_STOP
  "quantity": 100,
  "price": 175.50, // for LIMIT orders
  "timeInForce": "DAY", // DAY, GTC (Good Till Cancelled), IOC (Immediate or Cancel)
  "accountId": "uuid"
}
Response: 201 Created
{
  "orderId": "uuid",
  "clientOrderId": "client-123",
  "symbol": "AAPL",
  "side": "BUY",
  "orderType": "LIMIT",
  "quantity": 100,
  "price": 175.50,
  "status": "PENDING", // PENDING, OPEN, PARTIAL_FILL, FILLED, CANCELLED
  "filledQuantity": 0,
  "remainingQuantity": 100,
  "timestamp": "2025-11-12T09:30:00.123456Z"
}

DELETE /api/v1/orders/{orderId}
Response: 200 OK
{
  "orderId": "uuid",
  "status": "CANCELLED"
}

PATCH /api/v1/orders/{orderId}
Request:
{
  "quantity": 150, // modify quantity
  "price": 176.00  // modify price
}
```

### Market Data APIs

```
GET /api/v1/market-data/quote/{symbol}
Response: 200 OK
{
  "symbol": "AAPL",
  "bid": 175.50,
  "ask": 175.51,
  "bidSize": 1000,
  "askSize": 800,
  "lastPrice": 175.50,
  "lastSize": 100,
  "volume": 1234567,
  "timestamp": "2025-11-12T09:30:00.123456Z"
}

GET /api/v1/market-data/order-book/{symbol}?depth=10
Response: 200 OK
{
  "symbol": "AAPL",
  "bids": [
    {"price": 175.50, "quantity": 1000},
    {"price": 175.49, "quantity": 500},
    ...
  ],
  "asks": [
    {"price": 175.51, "quantity": 800},
    {"price": 175.52, "quantity": 300},
    ...
  ],
  "timestamp": "2025-11-12T09:30:00.123456Z"
}

WebSocket: wss://api.example.com/market-data/stream
Subscribe:
{
  "action": "subscribe",
  "symbols": ["AAPL", "GOOGL", "MSFT"],
  "channels": ["trades", "quotes", "orderbook"]
}

Stream Events:
{
  "type": "trade",
  "symbol": "AAPL",
  "price": 175.50,
  "quantity": 100,
  "timestamp": "2025-11-12T09:30:00.123456Z"
}
```

### Portfolio APIs

```
GET /api/v1/portfolio/{accountId}
Response: 200 OK
{
  "accountId": "uuid",
  "cash": 100000.00,
  "buyingPower": 200000.00, // with margin
  "totalValue": 250000.00,
  "positions": [
    {
      "symbol": "AAPL",
      "quantity": 100,
      "averagePrice": 150.00,
      "currentPrice": 175.50,
      "marketValue": 17550.00,
      "unrealizedPL": 2550.00,
      "unrealizedPLPercent": 17.00
    }
  ]
}

GET /api/v1/orders?accountId={accountId}&status={status}
GET /api/v1/trades?accountId={accountId}&fromDate={date}
```

## 6. Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    kyc_status VARCHAR(20) DEFAULT 'pending',
    account_type VARCHAR(20) DEFAULT 'retail', -- retail, institutional
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);
```

### Accounts Table
```sql
CREATE TABLE accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    account_type VARCHAR(20) DEFAULT 'cash', -- cash, margin
    cash_balance DECIMAL(20, 2) DEFAULT 0.00,
    buying_power DECIMAL(20, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'active',
    version INT DEFAULT 0, -- optimistic locking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    CONSTRAINT chk_cash CHECK (cash_balance >= 0)
);
```

### Orders Table
```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_order_id VARCHAR(255) UNIQUE,
    account_id UUID NOT NULL REFERENCES accounts(account_id),
    symbol VARCHAR(10) NOT NULL,
    side VARCHAR(4) NOT NULL, -- BUY, SELL
    order_type VARCHAR(20) NOT NULL, -- MARKET, LIMIT, STOP_LOSS
    quantity INT NOT NULL,
    price DECIMAL(20, 6), -- null for MARKET orders
    filled_quantity INT DEFAULT 0,
    remaining_quantity INT,
    status VARCHAR(20) DEFAULT 'PENDING',
    /* PENDING, OPEN, PARTIAL_FILL, FILLED, CANCELLED, REJECTED */
    time_in_force VARCHAR(10) DEFAULT 'DAY',
    created_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
    updated_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
    INDEX idx_account (account_id),
    INDEX idx_symbol_status (symbol, status),
    INDEX idx_created (created_at),
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_filled CHECK (filled_quantity <= quantity)
);
```

### Trades Table (Cassandra for write throughput)
```
CREATE TABLE trades (
    trade_id UUID,
    order_id UUID,
    symbol TEXT,
    side TEXT,
    quantity INT,
    price DECIMAL,
    buyer_account_id UUID,
    seller_account_id UUID,
    executed_at TIMESTAMP,
    settlement_date DATE,
    settlement_status TEXT,
    PRIMARY KEY ((symbol, executed_at), trade_id)
) WITH CLUSTERING ORDER BY (trade_id DESC);

// Index for account queries
CREATE TABLE trades_by_account (
    account_id UUID,
    executed_at TIMESTAMP,
    trade_id UUID,
    symbol TEXT,
    side TEXT,
    quantity INT,
    price DECIMAL,
    PRIMARY KEY (account_id, executed_at, trade_id)
) WITH CLUSTERING ORDER BY (executed_at DESC, trade_id DESC);
```

### Positions Table
```sql
CREATE TABLE positions (
    position_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(account_id),
    symbol VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    average_price DECIMAL(20, 6) NOT NULL,
    realized_pl DECIMAL(20, 2) DEFAULT 0.00,
    version INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(account_id, symbol),
    INDEX idx_account (account_id),
    INDEX idx_symbol (symbol)
);
```

### Market_Data_Tick Table (TimescaleDB)
```sql
CREATE TABLE market_data_tick (
    symbol VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP(6) NOT NULL,
    price DECIMAL(20, 6) NOT NULL,
    quantity INT NOT NULL,
    side VARCHAR(4), -- BUY, SELL
    PRIMARY KEY (symbol, timestamp)
);

-- Create hypertable (TimescaleDB)
SELECT create_hypertable('market_data_tick', 'timestamp');

-- Continuous aggregate for OHLCV
CREATE MATERIALIZED VIEW ohlcv_1min
WITH (timescaledb.continuous) AS
SELECT
    symbol,
    time_bucket('1 minute', timestamp) AS bucket,
    first(price, timestamp) AS open,
    max(price) AS high,
    min(price) AS low,
    last(price, timestamp) AS close,
    sum(quantity) AS volume
FROM market_data_tick
GROUP BY symbol, bucket;
```

### ACID Considerations

1. **Order Placement:**
   - Atomically check balance and create order
   - Update account buying power
   - Prevent over-leveraging

2. **Trade Execution:**
   - Atomic match and execution
   - Update both buyer and seller
   - No partial failures

3. **Settlement:**
   - Transfer funds atomically
   - Update positions
   - Maintain audit trail

## 7. Core Components

### 7.1 Matching Engine (Ultra Low-Latency)

**In-Memory Order Book:**

```cpp
// C++ for ultra-low latency
class OrderBook {
private:
    std::map<double, std::deque<Order*>, std::greater<double>> bids;  // sorted descending
    std::map<double, std::deque<Order*>> asks;  // sorted ascending
    std::string symbol;

public:
    void addOrder(Order* order) {
        if (order->side == Side::BUY) {
            matchBuyOrder(order);
        } else {
            matchSellOrder(order);
        }
    }

    void matchBuyOrder(Order* buyOrder) {
        // Match against best asks (lowest price first)
        while (!asks.empty() && buyOrder->remainingQuantity > 0) {
            auto& [price, orders] = *asks.begin();

            // Check if can match
            if (buyOrder->orderType == OrderType::MARKET ||
                (buyOrder->orderType == OrderType::LIMIT && buyOrder->price >= price)) {

                Order* sellOrder = orders.front();
                int matchedQty = std::min(buyOrder->remainingQuantity,
                                         sellOrder->remainingQuantity);

                // Execute trade
                executeTrade(buyOrder, sellOrder, price, matchedQty);

                // Update orders
                buyOrder->remainingQuantity -= matchedQty;
                buyOrder->filledQuantity += matchedQty;
                sellOrder->remainingQuantity -= matchedQty;
                sellOrder->filledQuantity += matchedQty;

                // Remove filled order
                if (sellOrder->remainingQuantity == 0) {
                    orders.pop_front();
                    if (orders.empty()) {
                        asks.erase(asks.begin());
                    }
                }
            } else {
                break;  // No more matches possible
            }
        }

        // If order not fully filled, add to book
        if (buyOrder->remainingQuantity > 0 && buyOrder->orderType != OrderType::MARKET) {
            bids[buyOrder->price].push_back(buyOrder);
        }
    }

    void executeTrade(Order* buy, Order* sell, double price, int quantity) {
        Trade trade{
            .tradeId = generateUUID(),
            .buyOrderId = buy->orderId,
            .sellOrderId = sell->orderId,
            .symbol = symbol,
            .price = price,
            .quantity = quantity,
            .timestamp = std::chrono::high_resolution_clock::now()
        };

        // Publish trade to downstream services
        publishTrade(trade);
    }
};
```

**Matching Algorithm (Price-Time Priority):**
1. Orders sorted by price (best price first)
2. At same price, sorted by time (FIFO)
3. Match incoming order against best opposite orders
4. Execute trades
5. Update order book

**Optimizations:**
- Keep order book in memory (RAM)
- Use efficient data structures (sorted maps, deques)
- Lock-free data structures for concurrency
- NUMA-aware memory allocation
- CPU pinning for deterministic latency

### 7.2 Market Data Service

**Real-time Streaming:**

```python
def publish_market_data(trade):
    # 1. Update quote
    quote = {
        'symbol': trade.symbol,
        'lastPrice': trade.price,
        'lastSize': trade.quantity,
        'timestamp': trade.timestamp
    }
    redis.publish(f'quote:{trade.symbol}', json.dumps(quote))

    # 2. Update order book snapshot
    order_book = get_order_book(trade.symbol)
    redis.set(f'orderbook:{trade.symbol}', json.dumps(order_book))

    # 3. Publish to WebSocket clients
    websocket_publish(f'trades:{trade.symbol}', trade)

    # 4. Persist tick data
    kafka.produce('market-data-ticks', trade)

    # 5. Update OHLCV (candlestick)
    update_candlestick(trade)
```

**WebSocket Server:**

```python
async def handle_market_data_subscription(websocket, path):
    subscriptions = set()

    async for message in websocket:
        data = json.loads(message)

        if data['action'] == 'subscribe':
            for symbol in data['symbols']:
                subscriptions.add(symbol)
                # Send current snapshot
                quote = redis.get(f'quote:{symbol}')
                await websocket.send(quote)

        elif data['action'] == 'unsubscribe':
            for symbol in data['symbols']:
                subscriptions.discard(symbol)

    # Stream updates
    pubsub = redis.pubsub()
    channels = [f'quote:{s}' for s in subscriptions]
    pubsub.subscribe(channels)

    for message in pubsub.listen():
        if message['type'] == 'message':
            await websocket.send(message['data'])
```

### 7.3 Risk Management Service

**Pre-Trade Checks:**

```python
def pre_trade_risk_check(order):
    account = get_account(order.account_id)

    # 1. Check buying power
    required_capital = order.quantity * order.price
    if account.buying_power < required_capital:
        raise InsufficientBuyingPowerError()

    # 2. Check position limits
    current_position = get_position(order.account_id, order.symbol)
    new_position = current_position + order.quantity if order.side == 'BUY' else current_position - order.quantity

    max_position = get_position_limit(order.symbol)
    if abs(new_position) > max_position:
        raise PositionLimitExceededError()

    # 3. Check order value limits
    max_order_value = get_max_order_value(account)
    if required_capital > max_order_value:
        raise OrderValueLimitExceededError()

    # 4. Concentration risk
    portfolio_value = get_portfolio_value(account.account_id)
    position_value = new_position * get_current_price(order.symbol)
    concentration = position_value / portfolio_value

    if concentration > 0.25:  # 25% max
        raise ConcentrationRiskError()

    return True
```

**Circuit Breakers:**

```python
def check_circuit_breaker(symbol, new_price):
    reference_price = get_reference_price(symbol)  # previous close

    price_change_percent = abs((new_price - reference_price) / reference_price)

    # Halt trading if price moves >10% in 5 minutes
    if price_change_percent > 0.10:
        halt_trading(symbol, duration=300)  # 5 minutes
        alert_regulators(symbol, price_change_percent)
        return False

    return True
```

### 7.4 Settlement Service

**T+2 Settlement:**

```python
def settle_trades():
    # Run at end of each trading day
    settlement_date = today() + timedelta(days=2)

    trades_to_settle = get_trades_for_settlement(settlement_date)

    for trade in trades_to_settle:
        with db.transaction():
            # 1. Transfer funds
            transfer_funds(
                from_account=trade.buyer_account_id,
                to_account=trade.seller_account_id,
                amount=trade.price * trade.quantity
            )

            # 2. Transfer shares
            transfer_shares(
                from_account=trade.seller_account_id,
                to_account=trade.buyer_account_id,
                symbol=trade.symbol,
                quantity=trade.quantity
            )

            # 3. Update trade status
            update_trade_status(trade.trade_id, 'SETTLED')

            # 4. Update positions
            update_position(trade.buyer_account_id, trade.symbol, trade.quantity)
            update_position(trade.seller_account_id, trade.symbol, -trade.quantity)
```

### 7.5 Surveillance Service

**Insider Trading Detection:**

```python
def detect_insider_trading(trade):
    # Check for suspicious patterns
    account = get_account(trade.account_id)

    # 1. Large trades before news
    upcoming_events = get_upcoming_events(trade.symbol)
    for event in upcoming_events:
        if event['date'] - trade.executed_at < timedelta(days=7):
            if trade.quantity * trade.price > 1000000:  # $1M threshold
                flag_suspicious_activity(trade, 'Large trade before event')

    # 2. Unusual trading patterns
    avg_daily_volume = get_average_daily_volume(account.account_id)
    if trade.quantity > avg_daily_volume * 5:
        flag_suspicious_activity(trade, 'Unusually large trade')

    # 3. Related party trading
    if is_related_to_company(account.user_id, trade.symbol):
        flag_suspicious_activity(trade, 'Related party trade')
```

## 8. Transaction Management & Consistency

### Trade Execution Transaction

```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 1. Lock accounts
SELECT account_id, cash_balance, version
FROM accounts
WHERE account_id IN (?, ?)  -- buyer and seller
FOR UPDATE;

-- 2. Verify buyer has sufficient funds
-- Application checks buyer.cash_balance >= trade_value

-- 3. Create trade record
INSERT INTO trades (
    trade_id, buy_order_id, sell_order_id,
    symbol, price, quantity,
    buyer_account_id, seller_account_id,
    executed_at, settlement_date
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW() + INTERVAL '2 days');

-- 4. Update orders
UPDATE orders
SET filled_quantity = filled_quantity + ?,
    remaining_quantity = remaining_quantity - ?,
    status = CASE
        WHEN remaining_quantity - ? = 0 THEN 'FILLED'
        ELSE 'PARTIAL_FILL'
    END
WHERE order_id = ?;

-- Same for sell order

-- 5. Update buyer account (reserve funds)
UPDATE accounts
SET cash_balance = cash_balance - ?,
    version = version + 1
WHERE account_id = ? AND version = ?;

-- 6. Update seller account (pending settlement)
-- Funds released on T+2

COMMIT;

-- 7. Publish events (async)
PUBLISH trade_executed event to Kafka
```

## 9. Security Considerations

### Authentication
- OAuth 2.0 / API keys
- Two-factor authentication
- Biometric for mobile

### Authorization
- RBAC (Role-Based Access Control)
- Order-level permissions
- IP whitelisting for institutions

### Encryption
- TLS 1.3 for all connections
- Encrypted at rest (database)
- Hardware Security Modules (HSM)

### Audit Trail
- Every action logged
- Immutable audit logs
- Regulatory reporting

### DDoS Protection
- Rate limiting per user
- Cloudflare/AWS Shield
- Geographic filtering

## 10. Scalability

### Matching Engine Scaling
- One matching engine per symbol
- Distributed across servers
- Hot symbols on dedicated hardware
- Co-location for HFT firms

### Database Scaling
- Shard by symbol
- Time-series partitioning
- Read replicas for analytics
- In-memory for hot data

### Market Data Scaling
- CDN for static data
- WebSocket federation
- Kafka for streaming
- Redis pub/sub

## 11. Trade-offs

### 1. Latency vs Throughput
**Ultra-low latency:** Single-threaded, lock-free
**High throughput:** Multi-threaded, batching

### 2. Consistency vs Availability
**Strong consistency:** Required for trading
**Eventual consistency:** Acceptable for analytics

### 3. In-Memory vs Persistent
**In-memory:** Faster, risk of data loss
**Persistent:** Slower, durable

## 12. Follow-up Questions

1. How would you implement dark pools?
2. How would you handle market maker rebates?
3. How would you implement algorithmic trading?
4. How would you handle flash crashes?
5. How would you implement options trading?
6. How would you handle pre-market and after-hours trading?
7. How would you implement cross-exchange arbitrage?
8. How would you handle corporate actions (splits, dividends)?
9. How would you implement margin calls?
10. How would you scale to global markets (24/7 trading)?

---

**Key Takeaways:**
- Ultra-low latency is critical
- Strong consistency for trades
- Price-time priority is standard
- Regulatory compliance is essential
- Risk management prevents disasters
- Surveillance detects fraud
