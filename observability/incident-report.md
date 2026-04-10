# ShopSphere Production Incident — Error Report
# Incident ID: INC-20260410-0247
# Severity: P0 | Started: 2026-04-10 02:47 UTC

## Summary
Checkout endpoint experiencing intermittent failures.
Failure rate: ~60% of requests failing.
Revenue impact: $12,000/minute.

## Observed Symptoms
- Some users report "checkout failed" with no error details
- Payments sometimes not charged but order says "processing"
- No obvious pattern — some orders succeed, most fail
- Logs show errors but provide zero context about root cause

## Stack Traces Captured

### Error 1 (Python Service)
```
TypeError: unsupported operand type(s) for -: 'float' and 'NoneType'
  File "app/service/checkout_service.py", line 28, in process_checkout
    final_amount = amount - discount
```

### Error 2 (Java Service)
```
java.lang.NullPointerException: Cannot unbox the value of a null Double
    at com.shopsphere.checkout.service.CheckoutService.processCheckout(CheckoutService.java:42)
    at com.shopsphere.checkout.controller.CheckoutController.checkout(CheckoutController.java:28)
```

### Error 3 (Payment — silent)
```
[No stack trace — exception was swallowed]
2026-04-10 02:47:22 ERROR payment-client Payment processing failed
```

## What We Know
- Issue started after the config.yaml was updated (commit: a3f92c1)
- Only certain user IDs fail consistently
- Payment failures produce no actionable log output
- Monitoring shows timeout config was recently changed

## What We Don't Know
- Root cause of TypeError
- Why payment failures are not surfaced to checkout
- Whether payments are being charged but orders failing, or neither
