"""
Data Loss Prevention (DLP) Engine
Detects and redacts sensitive information

Patterns:
- API Keys (OpenAI, AWS, etc.)
- Credit Cards (Luhn validation)
- PII (Email, Phone, SSN)
- JWT Tokens
- Private Keys
"""

import re
import logging
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class DLPMode(str, Enum):
    """DLP action modes"""
    MASK = "mask"      # Replace with ***
    BLOCK = "block"    # Reject request
    SHADOW_LOG = "shadow_log"  # Log but allow


class DLPPattern:
    """Pattern definition for sensitive data"""
    
    def __init__(self, name: str, pattern: str, replacement: str = "***"):
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.replacement = replacement
    
    def find(self, text: str):
        """Find matches in text"""
        return self.pattern.finditer(text)
    
    def redact(self, text: str) -> str:
        """Redact matches in text"""
        return self.pattern.sub(self.replacement, text)


class DLPEngine:
    """
    Data Loss Prevention engine
    
    MVP Implementation:
    - Regex-based pattern matching (fast, <5ms)
    - Luhn validation for credit cards
    - Entropy check for random strings
    
    Future (v2):
    - ML-based detection
    - Custom patterns per team
    - Contextual analysis
    """
    
    def __init__(self):
        self.patterns = self._init_patterns()
        self.mode = DLPMode.MASK
    
    def _init_patterns(self) -> dict[str, DLPPattern]:
        """Initialize detection patterns"""
        return {
            # API Keys
            "openai_key": DLPPattern(
                "OpenAI API Key",
                r"sk-[A-Za-z0-9]{20,}",
                "sk-****"
            ),
            "aws_key": DLPPattern(
                "AWS Access Key",
                r"AKIA[0-9A-Z]{16}",
                "AKIA****"
            ),
            "aws_secret": DLPPattern(
                "AWS Secret Key",
                r"aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}",
                "aws_secret_access_key=****"
            ),
            "github_token": DLPPattern(
                "GitHub Token",
                r"ghp_[A-Za-z0-9_]{36,255}",
                "ghp_****"
            ),
            
            # Credit Cards
            "credit_card": DLPPattern(
                "Credit Card",
                r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
                "****-****-****-****"
            ),
            
            # PII
            "email": DLPPattern(
                "Email Address",
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "***@***.***"
            ),
            "phone": DLPPattern(
                "Phone Number",
                r"\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b",
                "***-***-****"
            ),
            "ssn": DLPPattern(
                "Social Security Number",
                r"\b\d{3}-\d{2}-\d{4}\b",
                "***-**-****"
            ),
            
            # Tokens
            "jwt": DLPPattern(
                "JWT Token",
                r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
                "eyJ****"
            ),
            "bearer_token": DLPPattern(
                "Bearer Token",
                r"Bearer\s+[A-Za-z0-9._-]+",
                "Bearer ****"
            ),
            
            # Private Keys
            "private_key": DLPPattern(
                "Private Key",
                r"-----BEGIN (?:RSA |DSA |EC )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |DSA |EC )?PRIVATE KEY-----",
                "-----BEGIN PRIVATE KEY-----****-----END PRIVATE KEY-----"
            ),
        }
    
    def redact(
        self,
        text: str,
        mode: Optional[str] = None,
        return_matches: bool = False
    ) -> Optional[str]:
        """
        Redact sensitive information from text
        
        Args:
            text: Text to redact
            mode: DLP mode (mask, block, shadow_log)
            return_matches: If True, return list of matches instead of redacted text
        
        Returns:
            Redacted text, None if blocked, or list of matches
        """
        mode = mode or self.mode
        
        if not text:
            return text
        
        matches = []
        redacted = text
        
        # Find all matches
        for pattern_name, pattern in self.patterns.items():
            for match in pattern.find(text):
                matches.append({
                    "type": pattern_name,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })
                
                # Redact in text
                redacted = pattern.redact(redacted)
        
        if return_matches:
            return matches
        
        # Handle based on mode
        if mode == DLPMode.BLOCK and matches:
            logger.warning(f"DLP blocked request: {len(matches)} sensitive items found")
            return None
        
        if mode == DLPMode.SHADOW_LOG and matches:
            logger.info(f"DLP shadow log: {len(matches)} sensitive items found")
            # Still return redacted text
        
        return redacted
    
    def validate_credit_card(self, card_number: str) -> bool:
        """
        Validate credit card using Luhn algorithm
        
        Returns True if valid credit card number
        """
        # Remove non-digits
        digits = re.sub(r"\D", "", card_number)
        
        if len(digits) < 13 or len(digits) > 19:
            return False
        
        # Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        return total % 10 == 0
    
    def calculate_entropy(self, text: str) -> float:
        """
        Calculate Shannon entropy of text
        
        High entropy (>4.0) suggests random/encrypted data
        """
        if not text:
            return 0.0
        
        import math
        
        # Count character frequencies
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        for count in freq.values():
            p = count / len(text)
            entropy -= p * math.log2(p)
        
        return entropy
    
    def is_likely_secret(self, text: str) -> bool:
        """
        Heuristic: Check if text is likely a secret
        
        Secrets typically have:
        - High entropy (>3.5)
        - Mix of upper/lower/digits
        - No common words
        """
        if len(text) < 20:
            return False
        
        entropy = self.calculate_entropy(text)
        if entropy < 3.5:
            return False
        
        # Check for mix of character types
        has_upper = any(c.isupper() for c in text)
        has_lower = any(c.islower() for c in text)
        has_digit = any(c.isdigit() for c in text)
        has_special = any(not c.isalnum() for c in text)
        
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        
        return char_types >= 3


# Singleton instance
dlp_engine = DLPEngine()
