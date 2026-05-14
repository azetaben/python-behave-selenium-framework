"""
Logging utility for the framework.

Provides configured logger instances per module.
"""
import logging
from datetime import date
from pathlib import Path

from doc.config.config import settings

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logging.Logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(settings.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(settings.log_level)
        console_formatter = logging.Formatter(settings.log_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = logs_dir / f"test_{date.today()}.log"
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(settings.log_level)
        file_formatter = logging.Formatter(settings.log_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Initialize root logger
logging.basicConfig(
    level=settings.log_level,
    format=settings.log_format,
)
