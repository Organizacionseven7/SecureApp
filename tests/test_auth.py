"""
Tests for authentication utilities
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from secure_app.auth import AuthManager, Token
from datetime import datetime, timedelta
import time


def test_token_generation():
    """Test secure token generation"""
    token1 = AuthManager.generate_token()
    token2 = AuthManager.generate_token()
    
    assert token1 != token2
    assert len(token1) > 0
    assert isinstance(token1, str)


def test_token_expiry():
    """Test token expiration"""
    # Create expired token
    expires_at = datetime.now() - timedelta(hours=1)
    token = Token("test_token", expires_at)
    
    assert token.is_expired() is True
    assert token.is_valid() is False
    
    # Create valid token
    expires_at = datetime.now() + timedelta(hours=1)
    token = Token("test_token", expires_at)
    
    assert token.is_expired() is False
    assert token.is_valid() is True


def test_session_creation():
    """Test session creation"""
    auth = AuthManager()
    user_id = "user123"
    
    token = auth.create_session(user_id)
    
    assert token is not None
    assert len(token) > 0
    assert auth.validate_session(user_id, token) is True


def test_session_validation():
    """Test session validation"""
    auth = AuthManager()
    user_id = "user123"
    
    token = auth.create_session(user_id)
    
    # Valid token
    assert auth.validate_session(user_id, token) is True
    
    # Invalid token
    assert auth.validate_session(user_id, "wrong_token") is False
    
    # Non-existent user
    assert auth.validate_session("nonexistent", token) is False


def test_session_revocation():
    """Test session revocation"""
    auth = AuthManager()
    user_id = "user123"
    
    token = auth.create_session(user_id)
    assert auth.validate_session(user_id, token) is True
    
    # Revoke session
    result = auth.revoke_session(user_id)
    assert result is True
    assert auth.validate_session(user_id, token) is False
    
    # Try to revoke non-existent session
    result = auth.revoke_session("nonexistent")
    assert result is False


def test_secure_code_generation():
    """Test secure code generation"""
    code1 = AuthManager.generate_secure_code()
    code2 = AuthManager.generate_secure_code()
    
    assert len(code1) == 6
    assert code1.isdigit()
    assert code1 != code2  # Very likely to be different


def test_cleanup_expired_sessions():
    """Test cleanup of expired sessions"""
    auth = AuthManager()
    
    # Create some sessions
    auth.create_session("user1", expiry_hours=24)
    auth.create_session("user2", expiry_hours=24)
    
    # No expired sessions yet
    count = auth.cleanup_expired_sessions()
    assert count == 0
    
    # Sessions should still be valid
    assert len(auth._sessions) == 2


if __name__ == "__main__":
    test_token_generation()
    test_token_expiry()
    test_session_creation()
    test_session_validation()
    test_session_revocation()
    test_secure_code_generation()
    test_cleanup_expired_sessions()
    
    print("✓ All authentication tests passed!")
