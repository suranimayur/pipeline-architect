"""
Logging utilities for Pipeline Architect.

This module provides centralized logging configuration and utility functions
for consistent logging across the application.
"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", format_string: Optional[str] = None, log_file: Optional[str] = None):
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Log message format
        log_file: Optional file to write logs to
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Prevent duplicate logs
    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def sanitize_log_message(message: str) -> str:
    """
    Sanitize log messages to remove sensitive information.
    
    Args:
        message: Original log message
        
    Returns:
        Sanitized log message
    """
    # Replace common API keys and secrets
    import re
    
    # Replace API keys
    message = re.sub(r'api[_-]?key["\']?\s*[:=]\s*["\']?[^"\s]+', 'api_key=***', message, flags=re.IGNORECASE)
    
    # Replace tokens
    message = re.sub(r'token["\']?\s*[:=]\s*["\']?[^"\s]+', 'token=***', message, flags=re.IGNORECASE)
    
    # Replace passwords
    message = re.sub(r'password["\']?\s*[:=]\s*["\']?[^"\s]+', 'password=***', message, flags=re.IGNORECASE)
    
    # Replace URLs with tokens
    message = re.sub(r'http[s]?://[^/\s]+:[^@\s]+@', 'http://***:***@', message)
    
    return message


class SanitizedLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that sanitizes sensitive information from log messages.
    """
    
    def process(self, msg, kwargs):
        """Process log message to sanitize sensitive information."""
        sanitized_msg = sanitize_log_message(str(msg))
        return sanitized_msg, kwargs


def get_sanitized_logger(name: str, extra: Optional[dict] = None) -> SanitizedLoggerAdapter:
    """
    Get a sanitized logger instance.
    
    Args:
        name: Logger name
        extra: Additional fields to include in log records
        
    Returns:
        Sanitized logger adapter
    """
    logger = get_logger(name)
    return SanitizedLoggerAdapter(logger, extra or {})


__all__ = [
    "setup_logging",
    "get_logger", 
    "sanitize_log_message",
    "SanitizedLoggerAdapter",
    "get_sanitized_logger"
]