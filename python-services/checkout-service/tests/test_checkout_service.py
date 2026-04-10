"""
Tests for CheckoutService — currently incomplete.
Participants will use Copilot to complete these.
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock


class TestCheckoutService:

    def test_checkout_with_even_user_applies_discount(self):
        """GIVEN an even user_id, WHEN checkout is called, THEN discount is applied."""
        # TODO: Implement with Copilot Agent → test-generator-agent
        pass

    def test_checkout_with_odd_user_fails(self):
        """GIVEN an odd user_id, WHEN checkout is called, THEN it should NOT crash."""
        # TODO: This test should currently FAIL — exposing Bug #1
        pass

    def test_payment_failure_is_surfaced(self):
        """GIVEN payment fails, WHEN checkout returns, THEN status should be 'failed'."""
        # TODO: This test should currently FAIL — exposing Bug #2
        pass

    def test_checkout_returns_correct_status(self):
        """GIVEN all services healthy, WHEN checkout completes, THEN status is 'success'."""
        # TODO: Implement with Copilot Agent
        pass
