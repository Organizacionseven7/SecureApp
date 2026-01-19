"""
Tests for password utilities
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from secure_app.password_utils import PasswordValidator


def test_password_validator_initialization():
    """Test PasswordValidator initialization"""
    validator = PasswordValidator()
    assert validator.min_length == 8
    
    validator = PasswordValidator(min_length=10)
    assert validator.min_length == 10


def test_empty_password():
    """Test validation of empty password"""
    validator = PasswordValidator()
    result = validator.validate("")
    
    assert result['valid'] is False
    assert 'Password cannot be empty' in result['issues']


def test_weak_password():
    """Test validation of weak password"""
    validator = PasswordValidator()
    result = validator.validate("weak")
    
    assert result['valid'] is False
    assert result['strength'] == 'weak'
    assert len(result['issues']) > 0


def test_medium_password():
    """Test validation of medium strength password"""
    validator = PasswordValidator()
    result = validator.validate("Password123")
    
    assert result['valid'] is False
    assert len(result['issues']) > 0


def test_strong_password():
    """Test validation of strong password"""
    validator = PasswordValidator()
    result = validator.validate("SecurePass123!")
    
    assert result['valid'] is True
    assert result['strength'] in ['medium', 'strong']
    assert len(result['issues']) == 0


def test_very_strong_password():
    """Test validation of very strong password"""
    validator = PasswordValidator()
    result = validator.validate("VerySecurePassword123!@#")
    
    assert result['valid'] is True
    assert result['strength'] == 'strong'
    assert result['score'] >= 6


def test_common_passwords():
    """Test common password detection"""
    validator = PasswordValidator()
    
    assert validator.check_common_passwords("password") is True
    assert validator.check_common_passwords("123456") is True
    assert validator.check_common_passwords("MyUniquePass123!") is False


def test_custom_min_length():
    """Test custom minimum length"""
    validator = PasswordValidator(min_length=12)
    result = validator.validate("Pass123!")
    
    assert result['valid'] is False
    assert any('12 characters' in issue for issue in result['issues'])


if __name__ == "__main__":
    test_password_validator_initialization()
    test_empty_password()
    test_weak_password()
    test_medium_password()
    test_strong_password()
    test_very_strong_password()
    test_common_passwords()
    test_custom_min_length()
    
    print("✓ All password utility tests passed!")
