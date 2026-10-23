import logging


def configure_logging() -> None:
    """Configure concise application-wide logging without message contents."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
