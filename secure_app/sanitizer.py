"""
Input sanitization utilities for SecureApp
"""
import html
import re
from typing import Optional


class InputSanitizer:
    """Sanitize user inputs to prevent security vulnerabilities"""
    
    @staticmethod
    def sanitize_html(input_text: str) -> str:
        """
        Sanitize HTML to prevent XSS attacks
        
        Args:
            input_text: The text to sanitize
            
        Returns:
            Sanitized text
        """
        if not input_text:
            return ""
        return html.escape(input_text)
    
    @staticmethod
    def sanitize_sql(input_text: str) -> str:
        """
        Sanitize input to help prevent SQL injection
        
        ⚠️ IMPORTANT: This is NOT a replacement for parameterized queries!
        ALWAYS use parameterized queries (prepared statements) as your primary
        defense against SQL injection. This function provides only a weak
        additional layer of protection and can be bypassed by determined attackers.
        
        Args:
            input_text: The text to sanitize
            
        Returns:
            Sanitized text
        """
        if not input_text:
            return ""
        
        # Remove dangerous SQL keywords and characters
        dangerous_patterns = [
            r'(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b)',
            r'(--|;|\/\*|\*\/)',
            r"('|\"|`)"
        ]
        
        sanitized = input_text
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent directory traversal attacks
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename
        """
        if not filename:
            return ""
        
        # Remove path separators and parent directory references
        sanitized = filename.replace('..', '').replace('/', '').replace('\\', '')
        
        # Remove any non-alphanumeric characters except dot, dash, and underscore
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', sanitized)
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: The email to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def sanitize_path(path: str) -> Optional[str]:
        """
        Sanitize file path to prevent directory traversal
        
        Args:
            path: The path to sanitize
            
        Returns:
            Sanitized path or None if path is invalid
        """
        if not path:
            return None
        
        # Normalize path and check for traversal attempts
        if '..' in path or path.startswith('/'):
            return None
        
        return path.replace('\\', '/')
