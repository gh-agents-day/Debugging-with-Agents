# ShopSphere Platform — Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT                              │
│              (Web / Mobile / B2B API)                   │
└──────────────────────┬──────────────────────────────────┘
                       │ POST /api/v1/checkout
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   API GATEWAY                            │
│            Rate limiting · Auth · Routing               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              CHECKOUT SERVICE (Port 8001/8081)           │
│                                                          │
│  CheckoutAPI → CheckoutService                          │
│                     │                                    │
│            ┌────────┴────────┐                          │
│            ▼                 ▼                          │
│    DiscountClient      PaymentClient                    │
└────────┬───────────────────────┬────────────────────────┘
         │                       │
         ▼                       ▼
┌────────────────┐   ┌──────────────────────────┐
│ DISCOUNT SVC   │   │     PAYMENT SERVICE       │
│  Port 8003     │   │      Port 8002            │
│                │   │                           │
│ getDiscount()  │   │  processPayment()         │
│                │   │  → External Gateway       │
└────────────────┘   └──────────────────────────┘
```

## Service Responsibilities

### Checkout Service
- **Primary entry point** for all checkout operations
- Orchestrates discount calculation and payment processing
- Returns order confirmation to client

### Discount Service
- Returns discount amounts per customer
- Business rule: even userId → $10 discount; odd userId → no discount
- **Known contract issue:** Returns `null` instead of `0.0` when no discount applies (JIRA-4821)

### Payment Service
- Processes payments via external payment gateway
- External gateway SLA: 3 seconds p99 latency
- Configured timeout: **1 second** (KNOWN BUG — too low)
- No retry logic configured (KNOWN BUG)

## Data Flow

```
1. Client sends POST /api/v1/checkout { user_id, amount }
2. CheckoutService calls DiscountClient.getDiscount(user_id)
3. discount = null if no discount (BUG: should be 0.0)
4. CheckoutService computes final_amount = amount - discount (CRASH if null)
5. CheckoutService calls PaymentClient.processPayment() [ASYNC, unawaited]
6. CheckoutService returns {"status": "processing"} immediately (RACE CONDITION)
7. Payment runs in background, may fail silently
```

## Known Issues (Workshop Scope)

| ID | Severity | Description | File |
|----|----------|-------------|------|
| BUG-001 | P0 | Null discount crashes checkout for odd user IDs | `checkout_service.py:28` |
| BUG-002 | P0 | Payment result not awaited — silent failures | `checkout_service.py:37` |
| BUG-003 | P1 | Swallowed exceptions with no context | `checkout_service.py:46` |
| BUG-004 | P1 | Config timeout too low (1s vs 3s SLA) | `config.yaml:4` |
| BUG-005 | P1 | No retry on transient payment failures | `payment_client.py:22` |

## Technology Stack

| Layer | Python | Java |
|-------|--------|------|
| Framework | FastAPI | Spring Boot 3.2 |
| Async | asyncio | @Async / CompletableFuture |
| Config | config.yaml | application.yml |
| Tests | pytest | JUnit 5 + Mockito |
| Logging | Python logging | SLF4J + Logback |
