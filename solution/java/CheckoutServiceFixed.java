package com.shopsphere.checkout.service;

import com.shopsphere.checkout.client.DiscountClient;
import com.shopsphere.checkout.client.PaymentClient;
import com.shopsphere.checkout.model.CheckoutResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

/**
 * SOLUTION: Fixed CheckoutService — Java
 * All 5 bugs resolved.
 */
@Service
public class CheckoutServiceFixed {

    private static final Logger logger = LoggerFactory.getLogger(CheckoutServiceFixed.class);

    @Autowired
    private PaymentClient paymentClient;

    @Autowired
    private DiscountClient discountClient;

    public CheckoutResponse processCheckout(int userId, double amount) {
        logger.info("Processing checkout for userId={} amount={}", userId, amount);

        try {
            // Step 1: Get discount
            Double discount = discountClient.getDiscount(userId);

            // FIX 1: Handle null discount — treat as 0.0 (no discount)
            double safeDiscount = (discount != null) ? discount : 0.0;
            double finalAmount = amount - safeDiscount;

            logger.info("Discount={} finalAmount={} for userId={}", safeDiscount, finalAmount, userId);

            // FIX 2: Await the async payment result with timeout
            CompletableFuture<String> paymentFuture = paymentClient.processPaymentAsync(userId, finalAmount);
            String paymentStatus = paymentFuture.get(5, TimeUnit.SECONDS);  // FIX 4: enforce timeout

            if (!"success".equals(paymentStatus)) {
                logger.error("Payment failed for userId={} status={}", userId, paymentStatus);
                return CheckoutResponse.builder()
                        .status("failed")
                        .userId(userId)
                        .build();
            }

            return CheckoutResponse.builder()
                    .status("success")
                    .userId(userId)
                    .amount(finalAmount)
                    .discountApplied(safeDiscount)
                    .transactionId("TXN-" + userId + "-" + System.currentTimeMillis())
                    .build();

        } catch (Exception e) {
            // FIX 3: Log exception with full context and stack trace
            logger.error("Checkout failed for userId={} amount={}", userId, amount, e);
            return CheckoutResponse.builder()
                    .status("failed")
                    .userId(userId)
                    .build();
        }
    }
}
