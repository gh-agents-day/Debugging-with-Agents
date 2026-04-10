"""
Logging configuration — intentionally minimal to simulate production issue.
"""
import logging


def setup_logging():
    # BUG: No structured logging, no correlation IDs, no trace context
    # This makes it impossible to correlate a checkout request across services
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
