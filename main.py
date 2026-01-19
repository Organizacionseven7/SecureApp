#!/usr/bin/env python3
"""
SecureApp - Security Utility Application
Main CLI interface
"""
import sys
from secure_app.password_utils import PasswordValidator
from secure_app.sanitizer import InputSanitizer
from secure_app.encryption import EncryptionManager
from secure_app.auth import AuthManager


def print_banner():
    """Print application banner"""
    print("=" * 50)
    print("  SecureApp - Security Utility Application")
    print("  Version 0.1.0")
    print("=" * 50)
    print()


def test_password_validation():
    """Test password validation functionality"""
    print("\n--- Password Validation Test ---")
    validator = PasswordValidator()
    
    test_passwords = [
        "weak",
        "Password123",
        "SecurePass123!",
        "VerySecurePassword123!@#"
    ]
    
    for pwd in test_passwords:
        result = validator.validate(pwd)
        print(f"\nPassword: {pwd}")
        print(f"Valid: {result['valid']}")
        print(f"Strength: {result.get('strength', 'N/A')}")
        print(f"Score: {result['score']}/7")
        if result['issues']:
            print(f"Issues: {', '.join(result['issues'])}")
        
        is_common = validator.check_common_passwords(pwd)
        if is_common:
            print("⚠️  WARNING: This is a common password!")


def test_input_sanitization():
    """Test input sanitization functionality"""
    print("\n\n--- Input Sanitization Test ---")
    sanitizer = InputSanitizer()
    
    # Test HTML sanitization
    html_input = "<script>alert('XSS')</script>Hello"
    sanitized = sanitizer.sanitize_html(html_input)
    print(f"\nHTML Input: {html_input}")
    print(f"Sanitized: {sanitized}")
    
    # Test filename sanitization
    filename = "../../etc/passwd"
    sanitized = sanitizer.sanitize_filename(filename)
    print(f"\nFilename: {filename}")
    print(f"Sanitized: {sanitized}")
    
    # Test email validation
    emails = ["test@example.com", "invalid.email", "user@domain.co.uk"]
    print("\nEmail Validation:")
    for email in emails:
        is_valid = sanitizer.validate_email(email)
        print(f"  {email}: {'✓ Valid' if is_valid else '✗ Invalid'}")


def test_encryption():
    """Test encryption functionality"""
    print("\n\n--- Encryption Test ---")
    manager = EncryptionManager()
    
    # Generate key
    key = manager.generate_key()
    print(f"Generated Key: {key[:20]}... (truncated)")
    
    manager.set_key(key)
    
    # Test encryption/decryption
    original_text = "This is a secret message!"
    encrypted = manager.encrypt(original_text)
    decrypted = manager.decrypt(encrypted)
    
    print(f"\nOriginal: {original_text}")
    print(f"Encrypted: {encrypted[:40]}... (truncated)")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {'✓ Yes' if original_text == decrypted else '✗ No'}")
    
    # Test password hashing
    password = "MySecurePassword123!"
    hashed = manager.hash_password(password)
    print(f"\nPassword: {password}")
    print(f"Hashed: {hashed[:30]}... (truncated)")
    
    # Verify password
    is_valid = manager.verify_password(password, hashed)
    print(f"Verification: {'✓ Match' if is_valid else '✗ No Match'}")
    
    wrong_password = "WrongPassword"
    is_valid = manager.verify_password(wrong_password, hashed)
    print(f"Wrong password: {'✓ Match' if is_valid else '✗ No Match'}")


def test_authentication():
    """Test authentication functionality"""
    print("\n\n--- Authentication Test ---")
    auth = AuthManager()
    
    # Generate token
    token = auth.generate_token()
    print(f"Generated Token: {token[:20]}... (truncated)")
    
    # Create session
    user_id = "user123"
    session_token = auth.create_session(user_id)
    print(f"\nSession created for user: {user_id}")
    print(f"Session Token: {session_token[:20]}... (truncated)")
    
    # Validate session
    is_valid = auth.validate_session(user_id, session_token)
    print(f"Session Validation: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Generate 2FA code
    code = auth.generate_secure_code()
    print(f"\n2FA Code: {code}")


def main():
    """Main application entry point"""
    print_banner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python main.py [--help]")
        print("\nThis application demonstrates various security utilities:")
        print("  - Password validation and strength checking")
        print("  - Input sanitization (HTML, SQL, filenames)")
        print("  - Encryption and decryption")
        print("  - Password hashing and verification")
        print("  - Authentication token generation")
        print("  - Session management")
        return
    
    try:
        test_password_validation()
        test_input_sanitization()
        test_encryption()
        test_authentication()
        
        print("\n\n" + "=" * 50)
        print("All security tests completed successfully! ✓")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
