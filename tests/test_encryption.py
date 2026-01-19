"""
Tests for encryption utilities
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from secure_app.encryption import EncryptionManager


def test_key_generation():
    """Test encryption key generation"""
    key = EncryptionManager.generate_key()
    assert key is not None
    assert isinstance(key, bytes)
    assert len(key) > 0


def test_key_derivation_from_password():
    """Test key derivation from password"""
    password = "MySecurePassword123!"
    key, salt = EncryptionManager.derive_key_from_password(password)
    
    assert key is not None
    assert salt is not None
    assert isinstance(key, bytes)
    assert isinstance(salt, bytes)
    
    # Same password and salt should produce same key
    key2, _ = EncryptionManager.derive_key_from_password(password, salt)
    assert key == key2


def test_encryption_decryption():
    """Test encryption and decryption"""
    manager = EncryptionManager()
    key = manager.generate_key()
    manager.set_key(key)
    
    original = "This is a secret message!"
    encrypted = manager.encrypt(original)
    decrypted = manager.decrypt(encrypted)
    
    assert original == decrypted
    assert encrypted != original.encode()


def test_encryption_without_key():
    """Test that encryption fails without key"""
    manager = EncryptionManager()
    
    try:
        manager.encrypt("test")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "key not set" in str(e).lower()


def test_password_hashing():
    """Test password hashing"""
    password = "MySecurePassword123!"
    hashed = EncryptionManager.hash_password(password)
    
    assert hashed is not None
    assert isinstance(hashed, str)
    assert hashed != password


def test_password_verification():
    """Test password verification"""
    password = "MySecurePassword123!"
    hashed = EncryptionManager.hash_password(password)
    
    # Correct password should verify
    assert EncryptionManager.verify_password(password, hashed) is True
    
    # Wrong password should not verify
    assert EncryptionManager.verify_password("WrongPassword", hashed) is False


if __name__ == "__main__":
    test_key_generation()
    test_key_derivation_from_password()
    test_encryption_decryption()
    test_encryption_without_key()
    test_password_hashing()
    test_password_verification()
    
    print("✓ All encryption tests passed!")
