import logging
from src.core.config import settings

def setup_logging():
    logging.basicConfig(
        level=settings.logging.log_level.upper(),
        format=settings.logging.log_format,
        datefmt=settings.logging.log_date_format,
    )