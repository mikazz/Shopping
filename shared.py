import logging

logger = logging.getLogger(__name__)


def init():
    try:
        connect(config.mongodb.pop("name", "sales"), **config.mongodb, tz_aware=True)
    except Exception as exc:
        logger.critical("Failed to connect to MongoDB: %s", str(exc))
        raise exc
    logger.info("SQLLite connected")
