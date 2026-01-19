"""
Tests for input sanitization
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from secure_app.sanitizer import InputSanitizer


def test_html_sanitization():
    """Test HTML sanitization"""
    sanitizer = InputSanitizer()
    
    # Test XSS prevention
    result = sanitizer.sanitize_html("<script>alert('XSS')</script>")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
    
    # Test normal text
    result = sanitizer.sanitize_html("Hello World")
    assert result == "Hello World"


def test_sql_sanitization():
    """Test SQL injection prevention"""
    sanitizer = InputSanitizer()
    
    # Test SQL keyword removal
    result = sanitizer.sanitize_sql("'; DROP TABLE users; --")
    assert "DROP" not in result
    assert "--" not in result
    
    # Test normal text
    result = sanitizer.sanitize_sql("john_doe")
    assert result == "john_doe"


def test_filename_sanitization():
    """Test filename sanitization"""
    sanitizer = InputSanitizer()
    
    # Test directory traversal prevention
    result = sanitizer.sanitize_filename("../../etc/passwd")
    assert ".." not in result
    assert "/" not in result
    assert result == "etcpasswd"
    
    # Test valid filename
    result = sanitizer.sanitize_filename("document.pdf")
    assert result == "document.pdf"


def test_email_validation():
    """Test email validation"""
    sanitizer = InputSanitizer()
    
    # Valid emails
    assert sanitizer.validate_email("test@example.com") is True
    assert sanitizer.validate_email("user.name@domain.co.uk") is True
    
    # Invalid emails
    assert sanitizer.validate_email("invalid.email") is False
    assert sanitizer.validate_email("@domain.com") is False
    assert sanitizer.validate_email("") is False


def test_path_sanitization():
    """Test path sanitization"""
    sanitizer = InputSanitizer()
    
    # Test directory traversal prevention
    result = sanitizer.sanitize_path("../../../etc/passwd")
    assert result is None
    
    # Test absolute path prevention
    result = sanitizer.sanitize_path("/etc/passwd")
    assert result is None
    
    # Test valid relative path
    result = sanitizer.sanitize_path("documents/file.txt")
    assert result == "documents/file.txt"


if __name__ == "__main__":
    test_html_sanitization()
    test_sql_sanitization()
    test_filename_sanitization()
    test_email_validation()
    test_path_sanitization()
    
    print("✓ All sanitizer tests passed!")
