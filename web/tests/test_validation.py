"""
Unit tests for input validation.
Tests all validation functions.
"""

import pytest
from utils.validation import (
    validate_query,
    validate_email,
    validate_name,
    validate_message,
    validate_uploaded_file,
    validate_analysis_input,
    validate_consultation_input,
)


def test_validate_query_valid():
    """Test valid query validation."""
    is_valid, error = validate_query("I need 5000 units of toys")
    assert is_valid is True
    assert error is None


def test_validate_query_empty():
    """Test empty query validation."""
    is_valid, error = validate_query("")
    assert is_valid is False
    assert error is not None
    assert "empty" in error.lower() or "cannot" in error.lower()


def test_validate_query_too_long():
    """Test query length validation."""
    long_query = "a" * 10000
    is_valid, error = validate_query(long_query)
    assert is_valid is False
    assert "too long" in error.lower()


def test_validate_query_xss_attempt():
    """Test XSS pattern detection."""
    malicious_query = "<script>alert('xss')</script>"
    is_valid, error = validate_query(malicious_query)
    assert is_valid is False
    assert "invalid" in error.lower()


def test_validate_email_valid():
    """Test valid email validation."""
    is_valid, error = validate_email("test@example.com")
    assert is_valid is True
    assert error is None


def test_validate_email_invalid_format():
    """Test invalid email format."""
    is_valid, error = validate_email("not-an-email")
    assert is_valid is False
    assert "valid" in error.lower()


def test_validate_email_empty():
    """Test empty email validation."""
    is_valid, error = validate_email("")
    assert is_valid is False
    assert "required" in error.lower()


def test_validate_name_optional():
    """Test that name is optional."""
    is_valid, error = validate_name("")
    assert is_valid is True
    assert error is None or error == ""


def test_validate_name_valid():
    """Test valid name validation."""
    is_valid, error = validate_name("John Doe")
    assert is_valid is True
    assert error is None or error == "John Doe"


def test_validate_analysis_input_valid():
    """Test valid analysis input."""
    is_valid, error = validate_analysis_input(
        product_query="toys",
        context_query="Need 5000 units",
        uploaded_file=None
    )
    assert is_valid is True
    assert error is None


def test_validate_analysis_input_no_input():
    """Test analysis input with no query or file."""
    is_valid, error = validate_analysis_input(
        product_query="",
        context_query=None,
        uploaded_file=None
    )
    assert is_valid is False
    assert "provide" in error.lower() or "query" in error.lower()


def test_validate_consultation_input_valid():
    """Test valid consultation input."""
    is_valid, error = validate_consultation_input(
        email="test@example.com",
        name="John Doe",
        message="I need help"
    )
    assert is_valid is True
    assert error is None


def test_validate_consultation_input_invalid_email():
    """Test consultation input with invalid email."""
    is_valid, error = validate_consultation_input(
        email="invalid-email",
        name="John Doe",
        message="I need help"
    )
    assert is_valid is False
    assert "email" in error.lower()

