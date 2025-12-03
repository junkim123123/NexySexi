"""
Structured logging utilities for NexSupply.
Provides consistent, structured logging across the application.
"""

import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime


# =============================================================================
# STRUCTURED LOGGING HELPER
# =============================================================================

def log_structured(
    logger: logging.Logger,
    level: int,
    message: str,
    context: Optional[Dict[str, Any]] = None,
    error: Optional[Exception] = None,
    **kwargs
) -> None:
    """
    Log a structured message with context.
    
    Args:
        logger: Logger instance
        level: Logging level (logging.ERROR, logging.WARNING, etc.)
        message: Main log message
        context: Additional context dictionary
        error: Exception object (if logging an error)
        **kwargs: Additional fields to include in log
    """
    # Build structured log data
    log_data = {
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    
    # Add context if provided
    if context:
        log_data["context"] = context
    
    # Add error information if provided
    if error:
        log_data["error"] = {
            "type": type(error).__name__,
            "message": str(error),
        }
        if hasattr(error, '__traceback__'):
            import traceback
            log_data["error"]["traceback"] = traceback.format_exception(
                type(error), error, error.__traceback__
            )
    
    # Add any additional kwargs
    log_data.update(kwargs)
    
    # Format as JSON for structured logging
    # In production, this could be sent to a log aggregation service
    formatted_message = f"{message}"
    if context or error or kwargs:
        # Append structured data as JSON (for log parsers)
        structured_part = json.dumps(
            {k: v for k, v in log_data.items() if k != "message"},
            default=str,
            ensure_ascii=False
        )
        formatted_message = f"{message} | {structured_part}"
    
    logger.log(level, formatted_message, exc_info=error if error else None)


def log_error(
    logger: logging.Logger,
    message: str,
    error: Optional[Exception] = None,
    context: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """Log an error with structured context."""
    log_structured(logger, logging.ERROR, message, context, error, **kwargs)


def log_warning(
    logger: logging.Logger,
    message: str,
    context: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """Log a warning with structured context."""
    log_structured(logger, logging.WARNING, message, context, None, **kwargs)


def log_info(
    logger: logging.Logger,
    message: str,
    context: Optional[Dict[str, Any]] = None,
    **kwargs
) -> None:
    """Log an info message with structured context."""
    log_structured(logger, logging.INFO, message, context, None, **kwargs)


# =============================================================================
# CONTEXT BUILDERS
# =============================================================================

def build_analysis_context(
    query: str,
    mode: str,
    user_email: Optional[str] = None
) -> Dict[str, Any]:
    """Build context dictionary for analysis-related logs."""
    return {
        "operation": "analysis",
        "query": query[:100] if query else None,  # Truncate for privacy
        "mode": mode,
        "has_email": user_email is not None,
    }


def build_email_context(
    recipient: str,
    email_type: str,
    success: bool
) -> Dict[str, Any]:
    """Build context dictionary for email-related logs."""
    return {
        "operation": "email",
        "email_type": email_type,
        "recipient_domain": recipient.split("@")[-1] if "@" in recipient else None,
        "success": success,
    }


def build_db_context(
    operation: str,
    table: str,
    record_id: Optional[int] = None
) -> Dict[str, Any]:
    """Build context dictionary for database-related logs."""
    return {
        "operation": "database",
        "db_operation": operation,
        "table": table,
        "record_id": record_id,
    }




