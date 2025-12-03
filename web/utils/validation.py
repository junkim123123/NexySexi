"""
Input validation utilities for NexSupply.
Provides centralized validation functions for user inputs.
"""

import re
from typing import Tuple, Optional
import streamlit as st


# =============================================================================
# VALIDATION CONSTANTS
# =============================================================================

# Query validation
MAX_QUERY_LENGTH = 5000
MIN_QUERY_LENGTH = 1
MAX_CONTEXT_LENGTH = 3000

# Email validation
MAX_EMAIL_LENGTH = 254  # RFC 5321
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Name validation
MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 1

# Message validation
MAX_MESSAGE_LENGTH = 5000
MIN_MESSAGE_LENGTH = 1

# File validation
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_FILE_TYPES = ["png", "jpg", "jpeg", "pdf"]
ALLOWED_MIME_TYPES = [
    "image/png",
    "image/jpeg",
    "image/jpg",
    "application/pdf"
]

# Dangerous patterns (XSS, SQL injection attempts)
DANGEROUS_PATTERNS = [
    r'<script[^>]*>',
    r'javascript:',
    r'on\w+\s*=',
    r'SELECT\s+.*\s+FROM',
    r'INSERT\s+INTO',
    r'DELETE\s+FROM',
    r'DROP\s+TABLE',
    r'UNION\s+SELECT',
]


# =============================================================================
# QUERY VALIDATION
# =============================================================================

def validate_query(query: str, max_length: int = MAX_QUERY_LENGTH) -> Tuple[bool, Optional[str]]:
    """
    Validate user query input.
    
    Args:
        query: User query string
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not query:
        return False, "Query cannot be empty"
    
    query = query.strip()
    
    if len(query) < MIN_QUERY_LENGTH:
        return False, f"Query must be at least {MIN_QUERY_LENGTH} character(s)"
    
    if len(query) > max_length:
        return False, f"Query too long (max {max_length} characters). Please shorten your query."
    
    # Check for dangerous patterns
    query_lower = query.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return False, "Query contains invalid characters. Please use plain text only."
    
    return True, None


def validate_context(context: str) -> Tuple[bool, Optional[str]]:
    """
    Validate context/requirements input.
    
    Args:
        context: Context string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not context or not context.strip():
        # Context is optional, so empty is valid
        return True, None
    
    context = context.strip()
    
    if len(context) > MAX_CONTEXT_LENGTH:
        return False, f"Context too long (max {MAX_CONTEXT_LENGTH} characters)"
    
    # Check for dangerous patterns
    context_lower = context.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, context_lower, re.IGNORECASE):
            return False, "Context contains invalid characters. Please use plain text only."
    
    return True, None


# =============================================================================
# EMAIL VALIDATION
# =============================================================================

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format.
    
    Args:
        email: Email address string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email address is required"
    
    email = email.strip()
    
    if len(email) > MAX_EMAIL_LENGTH:
        return False, f"Email address too long (max {MAX_EMAIL_LENGTH} characters)"
    
    if not EMAIL_PATTERN.match(email):
        return False, "Please enter a valid email address (e.g., your@email.com)"
    
    # Additional checks
    if email.count('@') != 1:
        return False, "Email address must contain exactly one @ symbol"
    
    local, domain = email.split('@')
    if len(local) == 0 or len(domain) == 0:
        return False, "Invalid email address format"
    
    if '..' in email:
        return False, "Email address cannot contain consecutive dots"
    
    return True, None


# =============================================================================
# NAME VALIDATION
# =============================================================================

def validate_name(name: str, required: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate user name input.
    
    Args:
        name: Name string
        required: Whether name is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        if required:
            return False, "Name is required"
        return True, None  # Optional field
    
    name = name.strip()
    
    if len(name) < MIN_NAME_LENGTH:
        return False, f"Name must be at least {MIN_NAME_LENGTH} character(s)"
    
    if len(name) > MAX_NAME_LENGTH:
        return False, f"Name too long (max {MAX_NAME_LENGTH} characters)"
    
    # Check for dangerous patterns
    name_lower = name.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, name_lower, re.IGNORECASE):
            return False, "Name contains invalid characters"
    
    return True, None


# =============================================================================
# MESSAGE VALIDATION
# =============================================================================

def validate_message(message: str, required: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate message/comment input.
    
    Args:
        message: Message string
        required: Whether message is required
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message or not message.strip():
        if required:
            return False, "Message is required"
        return True, None  # Optional field
    
    message = message.strip()
    
    if len(message) < MIN_MESSAGE_LENGTH:
        return False, f"Message must be at least {MIN_MESSAGE_LENGTH} character(s)"
    
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"
    
    # Check for dangerous patterns
    message_lower = message.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return False, "Message contains invalid characters. Please use plain text only."
    
    return True, None


# =============================================================================
# FILE VALIDATION
# =============================================================================

def validate_uploaded_file(uploaded_file) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if uploaded_file is None:
        return True, None  # File upload is optional
    
    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        size_mb = uploaded_file.size / (1024 * 1024)
        return False, f"File too large ({size_mb:.1f} MB). Maximum size is {MAX_FILE_SIZE_MB} MB."
    
    # Check file type by extension
    file_name = uploaded_file.name.lower()
    file_ext = file_name.split('.')[-1] if '.' in file_name else ''
    
    if file_ext not in ALLOWED_FILE_TYPES:
        return False, f"File type not allowed. Please upload: {', '.join(ALLOWED_FILE_TYPES).upper()}"
    
    # Check MIME type if available
    if hasattr(uploaded_file, 'type') and uploaded_file.type:
        if uploaded_file.type not in ALLOWED_MIME_TYPES:
            return False, f"File type not allowed. Please upload: {', '.join(ALLOWED_FILE_TYPES).upper()}"
    
    # Check filename for dangerous characters
    if any(char in file_name for char in ['<', '>', ':', '"', '|', '?', '*', '\\', '/']):
        return False, "Filename contains invalid characters"
    
    return True, None


# =============================================================================
# COMBINED VALIDATION
# =============================================================================

def validate_analysis_input(
    product_query: str,
    context_query: Optional[str] = None,
    uploaded_file = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate complete analysis input (query + context + file).
    
    Args:
        product_query: Main product query
        context_query: Optional context/requirements
        uploaded_file: Optional uploaded file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate product query
    is_valid, error = validate_query(product_query)
    if not is_valid:
        return False, error
    
    # Validate context if provided
    if context_query:
        is_valid, error = validate_context(context_query)
        if not is_valid:
            return False, error
    
    # Validate file if provided
    if uploaded_file:
        is_valid, error = validate_uploaded_file(uploaded_file)
        if not is_valid:
            return False, error
    
    # At least one input must be provided
    has_query = bool(product_query and product_query.strip())
    has_file = uploaded_file is not None
    
    if not has_query and not has_file:
        return False, "Please provide a product query or upload a file"
    
    return True, None


def validate_consultation_input(
    email: str,
    name: Optional[str] = None,
    message: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validate consultation request input.
    
    Args:
        email: User email (required)
        name: User name (optional)
        message: Message (optional)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate email (required)
    is_valid, error = validate_email(email)
    if not is_valid:
        return False, error
    
    # Validate name if provided
    if name:
        is_valid, error = validate_name(name, required=False)
        if not is_valid:
            return False, error
    
    # Validate message if provided
    if message:
        is_valid, error = validate_message(message, required=False)
        if not is_valid:
            return False, error
    
    return True, None




