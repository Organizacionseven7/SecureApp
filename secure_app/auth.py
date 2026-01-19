"""
Authentication utilities for SecureApp
"""
import secrets
import time
from typing import Optional, Dict
from datetime import datetime, timedelta


class Token:
    """Represents an authentication token"""
    
    def __init__(self, value: str, expires_at: datetime):
        self.value = value
        self.expires_at = expires_at
        self.created_at = datetime.now()
    
    def is_expired(self) -> bool:
        """Check if token is expired"""
        return datetime.now() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if token is valid"""
        return not self.is_expired()


class AuthManager:
    """Manage authentication and session tokens"""
    
    def __init__(self):
        self._sessions: Dict[str, Token] = {}
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """
        Generate a secure random token
        
        Args:
            length: Length of the token
            
        Returns:
            Secure random token
        """
        return secrets.token_urlsafe(length)
    
    def create_session(self, user_id: str, expiry_hours: int = 24) -> str:
        """
        Create a new session token for a user
        
        Args:
            user_id: The user identifier
            expiry_hours: Hours until token expires
            
        Returns:
            Session token
        """
        token_value = self.generate_token()
        expires_at = datetime.now() + timedelta(hours=expiry_hours)
        
        token = Token(token_value, expires_at)
        self._sessions[user_id] = token
        
        return token_value
    
    def validate_session(self, user_id: str, token_value: str) -> bool:
        """
        Validate a session token
        
        Args:
            user_id: The user identifier
            token_value: The token to validate
            
        Returns:
            True if valid, False otherwise
        """
        if user_id not in self._sessions:
            return False
        
        token = self._sessions[user_id]
        
        if token.value != token_value:
            return False
        
        if token.is_expired():
            del self._sessions[user_id]
            return False
        
        return True
    
    def revoke_session(self, user_id: str) -> bool:
        """
        Revoke a user's session
        
        Args:
            user_id: The user identifier
            
        Returns:
            True if session was revoked, False if not found
        """
        if user_id in self._sessions:
            del self._sessions[user_id]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions
        
        Returns:
            Number of sessions removed
        """
        expired = [
            user_id for user_id, token in self._sessions.items()
            if token.is_expired()
        ]
        
        for user_id in expired:
            del self._sessions[user_id]
        
        return len(expired)
    
    @staticmethod
    def generate_secure_code(length: int = 6) -> str:
        """
        Generate a secure numeric code (for 2FA, verification, etc.)
        
        Args:
            length: Length of the code
            
        Returns:
            Secure numeric code
        """
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
