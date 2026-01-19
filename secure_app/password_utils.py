"""
Password utilities for SecureApp
"""
import re
from typing import Dict, List


class PasswordValidator:
    """Validate password strength and security requirements"""
    
    def __init__(self, min_length: int = 8):
        self.min_length = min_length
    
    def validate(self, password: str) -> Dict[str, any]:
        """
        Validate password strength
        
        Args:
            password: The password to validate
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'valid': True,
            'score': 0,
            'issues': []
        }
        
        if not password:
            results['valid'] = False
            results['issues'].append('Password cannot be empty')
            return results
        
        # Check minimum length
        if len(password) < self.min_length:
            results['valid'] = False
            results['issues'].append(f'Password must be at least {self.min_length} characters')
        else:
            results['score'] += 1
        
        # Check for uppercase letters
        if not re.search(r'[A-Z]', password):
            results['valid'] = False
            results['issues'].append('Password must contain at least one uppercase letter')
        else:
            results['score'] += 1
        
        # Check for lowercase letters
        if not re.search(r'[a-z]', password):
            results['valid'] = False
            results['issues'].append('Password must contain at least one lowercase letter')
        else:
            results['score'] += 1
        
        # Check for digits
        if not re.search(r'\d', password):
            results['valid'] = False
            results['issues'].append('Password must contain at least one digit')
        else:
            results['score'] += 1
        
        # Check for special characters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            results['valid'] = False
            results['issues'].append('Password must contain at least one special character')
        else:
            results['score'] += 1
        
        # Additional strength checks
        if len(password) >= 12:
            results['score'] += 1
        
        if len(password) >= 16:
            results['score'] += 1
        
        # Determine strength level
        if results['score'] >= 6:
            results['strength'] = 'strong'
        elif results['score'] >= 4:
            results['strength'] = 'medium'
        else:
            results['strength'] = 'weak'
        
        return results
    
    def check_common_passwords(self, password: str) -> bool:
        """
        Check if password is in common password list
        
        Args:
            password: The password to check
            
        Returns:
            True if password is common, False otherwise
        """
        common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
            'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
            'bailey', 'passw0rd', 'shadow', '123123', '654321'
        ]
        return password.lower() in common_passwords
