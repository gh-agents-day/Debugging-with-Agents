package com.shopsphere.checkout.client;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.util.Random;
import java.util.concurrent.CompletableFuture;

/**
 * SOLUTION: Fixed PaymentClient — Java
 * Fixes: retry logic, proper return type, exception propagation.
 */
@Component
public class PaymentClientFixed {

    private static final Logger logger = LoggerFactory.getLogger(PaymentClientFixed.class);
    private static final int MAX_RETRIES = 3;
    private final Random random = new Random();

    // FIX 2 + FIX 5: Return CompletableFuture so caller can await and check result
    @Async
    public CompletableFuture<String> processPaymentAsync(int userId, double amount) {
        String lastError = null;

        // FIX 5: Retry loop
        for (int attempt = 1; attempt <= MAX_RETRIES; attempt++) {
            try {
                logger.info("Payment attempt {}/{} for userId={} amount={}", attempt, MAX_RETRIES, userId, amount);

                // FIX 4: Timeout would be enforced by the caller using CompletableFuture.get(timeout)
                Thread.sleep(2000);

                if (random.nextBoolean()) {
                    throw new RuntimeException("Payment gateway error: connection refused");
                }

                logger.info("Payment successful for userId={} after {} attempt(s)", userId, attempt);
                return CompletableFuture.completedFuture("success");

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logger.error("Payment interrupted for userId={}", userId, e);
                return CompletableFuture.completedFuture("interrupted");

            } catch (Exception e) {
                lastError = e.getMessage();
                logger.warn("Payment attempt {} failed for userId={}: {}", attempt, userId, e.getMessage());

                if (attempt < MAX_RETRIES) {
                    try {
                        Thread.sleep(500); // backoff
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
        }

        // FIX 6: Return failure status instead of silently swallowing
        logger.error("Payment failed after {} attempts for userId={}: {}", MAX_RETRIES, userId, lastError);
        return CompletableFuture.completedFuture("failed");
    }
}
