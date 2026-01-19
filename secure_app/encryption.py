"""
Encryption utilities for SecureApp
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
import bcrypt


class EncryptionManager:
    """Manage encryption and decryption operations"""
    
    def __init__(self):
        self._cipher = None
    
    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a new encryption key
        
        Returns:
            Encryption key as bytes
        """
        return Fernet.generate_key()
    
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes = None) -> tuple:
        """
        Derive an encryption key from a password
        
        Args:
            password: The password to derive key from
            salt: Optional salt, if None a new one is generated
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def set_key(self, key: bytes):
        """
        Set the encryption key
        
        Args:
            key: The encryption key
        """
        self._cipher = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        """
        Encrypt data
        
        Args:
            data: The data to encrypt
            
        Returns:
            Encrypted data as bytes
            
        Raises:
            ValueError: If key is not set
        """
        if not self._cipher:
            raise ValueError("Encryption key not set. Call set_key() first.")
        
        return self._cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Decrypt data
        
        Args:
            encrypted_data: The encrypted data
            
        Returns:
            Decrypted data as string
            
        Raises:
            ValueError: If key is not set
        """
        if not self._cipher:
            raise ValueError("Encryption key not set. Call set_key() first.")
        
        return self._cipher.decrypt(encrypted_data).decode()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: The password to hash
            
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against a hash
        
        Args:
            password: The password to verify
            hashed: The hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode(), hashed.encode())
