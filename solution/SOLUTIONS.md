# Solution Guide — Bug Fixes

> **DO NOT OPEN until you've completed the lab!**  
> This file reveals all bug fixes and solutions.

---

## Bug #1 — Null Discount Crash

**Location:**
- Python: `app/service/checkout_service.py` line ~28
- Java: `service/CheckoutService.java` line ~42

**Root Cause:**
`DiscountClient.getDiscount()` returns `None`/`null` for odd user IDs (no-discount customers).  
`CheckoutService` does `amount - discount` without null checking, causing `TypeError` (Python) or `NullPointerException` (Java).

**Fix:**
```python
# Python — before
final_amount = amount - discount

# Python — after
discount = discount if discount is not None else 0.0
final_amount = amount - discount
```

```java
// Java — before
double finalAmount = amount - discount;

// Java — after
double safeDiscount = (discount != null) ? discount : 0.0;
double finalAmount = amount - safeDiscount;
```

---

## Bug #2 — Missing Await (Race Condition)

**Location:**
- Python: `app/service/checkout_service.py` line ~37
- Java: `service/CheckoutService.java` line ~52

**Root Cause:**
Payment is started as a background task but never awaited. Checkout returns `{"status": "processing"}` before knowing if payment succeeded or failed. Payment failures are completely invisible to the checkout flow.

**Fix:**
```python
# Python — before
payment_task = asyncio.create_task(self.payment_client.process_payment(...))
return {"status": "processing", ...}

# Python — after
payment_result = await self.payment_client.process_payment(...)
if payment_result.get("status") != "success":
    return {"status": "failed"}
return {"status": "success", ...}
```

```java
// Java — before
paymentClient.processPayment(userId, finalAmount);  // void @Async
return ... "processing" ...

// Java — after
CompletableFuture<String> future = paymentClient.processPaymentAsync(userId, finalAmount);
String paymentStatus = future.get(5, TimeUnit.SECONDS);
if (!"success".equals(paymentStatus)) return "failed" response;
```

---

## Bug #3 — Swallowed Exceptions

**Location:**
- Python: `app/service/checkout_service.py` line ~46
- Java: `service/CheckoutService.java` line ~59

**Root Cause:**
`except Exception:` catches but does not log the exception details. Developers see `"Checkout failed"` with no stack trace, no context, no user ID, and no error message.

**Fix:**
```python
# Python — before
except Exception:
    logger.error("Checkout failed")

# Python — after
except Exception as e:
    logger.error(f"Checkout failed for user_id={user_id} amount={amount}: {e}", exc_info=True)
```

```java
// Java — before
} catch (Exception e) {
    logger.error("Checkout failed for userId={}", userId);

// Java — after
} catch (Exception e) {
    logger.error("Checkout failed for userId={} amount={}", userId, amount, e);
```

---

## Bug #4 — Timeout Not Enforced

**Location:**
- Python: `config.yaml` (timeout: 1) + `app/client/payment_client.py`
- Java: `application.yml` (timeout-ms: 1000) + `client/PaymentClient.java`

**Root Cause:**
Config sets timeout to 1 second but the timeout value is never actually used in the code. The payment gateway's p99 latency is 3 seconds. Additionally, the configured value is too low even if it were enforced.

**Fix:**
```yaml
# config.yaml — before
timeout: 1

# config.yaml — after
timeout: 5
```

```python
# Python — enforce with asyncio.wait_for
result = await asyncio.wait_for(
    self._call_payment_gateway(user_id, amount),
    timeout=TIMEOUT
)
```

---

## Bug #5 — No Retry Logic

**Location:**
- Python: `app/client/payment_client.py`
- Java: `client/PaymentClient.java`

**Root Cause:**
`retry_count: 0` in config means any transient payment gateway failure is permanent. The external payment gateway has ~2% transient failure rate, but without retry, this becomes 2% of ALL checkouts failing.

**Fix:**
```python
# Python — add retry loop
for attempt in range(1, RETRY_COUNT + 1):
    try:
        result = await asyncio.wait_for(gateway_call(), timeout=TIMEOUT)
        return {"status": "success", ...}
    except Exception as e:
        if attempt < RETRY_COUNT:
            await asyncio.sleep(0.5)
return {"status": "error", "reason": last_error}
```

---

## Reference Solution Files

- Python: `solution/python/checkout_service_fixed.py`
- Python: `solution/python/payment_client_fixed.py`
- Java: `solution/java/CheckoutServiceFixed.java`
- Java: `solution/java/PaymentClientFixed.java`
