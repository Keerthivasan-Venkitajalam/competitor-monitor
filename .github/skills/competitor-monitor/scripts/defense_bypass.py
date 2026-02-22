"""
Web defense bypass utilities for competitor scraping.
Implements user agent rotation, random delays, and basic CAPTCHA detection.
Validates: Requirements 2.4
"""

import random
import time
from typing import Optional


class DefenseBypass:
    """Handles basic web defense bypass techniques."""
    
    def __init__(self):
        """Initialize defense bypass with common user agents."""
        self.user_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Safari on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            # Firefox on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            # Chrome on Linux
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Edge on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        ]
        
        # Common browser fingerprints for rotation
        self.browser_fingerprints = [
            {
                'platform': 'Win32',
                'language': 'en-US',
                'vendor': 'Google Inc.',
                'platform': 'Win32'
            },
            {
                'platform': 'MacIntel',
                'language': 'en-US',
                'vendor': 'Apple Inc.',
                'platform': 'MacIntel'
            },
            {
                'platform': 'Linux x86_64',
                'language': 'en-US',
                'vendor': '',
                'platform': 'Linux x86_64'
            }
        ]
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent from the list."""
        return random.choice(self.user_agents)
    
    def get_random_fingerprint(self) -> dict:
        """Get a random browser fingerprint."""
        return random.choice(self.browser_fingerprints)
    
    def get_random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> float:
        """
        Get a random delay between operations to avoid detection.
        
        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
            
        Returns:
            Random delay in seconds
        """
        return random.uniform(min_seconds, max_seconds)
    
    def add_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """
        Add a random delay to avoid detection.
        
        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = self.get_random_delay(min_seconds, max_seconds)
        time.sleep(delay)
    
    def rotate_headers(self, base_headers: Optional[dict] = None) -> dict:
        """
        Rotate HTTP headers to avoid detection.
        
        Args:
            base_headers: Base headers to extend
            
        Returns:
            Rotated headers dictionary
        """
        headers = base_headers or {}
        
        # Add random user agent
        headers['User-Agent'] = self.get_random_user_agent()
        
        # Add common headers
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Accept-Language'] = 'en-US,en;q=0.5'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['Sec-Fetch-Dest'] = 'document'
        headers['Sec-Fetch-Mode'] = 'navigate'
        headers['Sec-Fetch-Site'] = 'none'
        headers['Sec-Fetch-User'] = '?1'
        
        return headers
    
    def detect_captcha(self, html_content: str) -> bool:
        """
        Detect if a page contains CAPTCHA elements.
        
        Args:
            html_content: HTML content to analyze
            
        Returns:
            True if CAPTCHA is detected, False otherwise
        """
        captcha_indicators = [
            'recaptcha',
            'captcha',
            'g-recaptcha',
            'hcaptcha',
            'cf-turnstile',
            'challenge-form',
            'verify',
            'I am not a robot',
            'Enter the characters you see',
        ]
        
        content_lower = html_content.lower()
        return any(indicator in content_lower for indicator in captcha_indicators)
    
    def get_rotation_strategy(self, attempt_number: int) -> dict:
        """
        Get rotation strategy based on attempt number.
        
        Args:
            attempt_number: Current attempt number
            
        Returns:
            Strategy configuration dictionary
        """
        # Increase delays on subsequent attempts
        base_delay = 2.0 + (attempt_number * 1.5)
        
        return {
            'user_agent': self.get_random_user_agent(),
            'delay_before': self.get_random_delay(base_delay, base_delay + 2),
            'delay_after': self.get_random_delay(1.0, 2.0),
            'fingerprint': self.get_random_fingerprint()
        }


def create_defense_bypass_config() -> dict:
    """
    Create a configuration for defense bypass.
    
    Returns:
        Configuration dictionary with all bypass settings
    """
    bypass = DefenseBypass()
    
    return {
        'user_agents': bypass.user_agents,
        'browser_fingerprints': bypass.browser_fingerprints,
        'default_delay_range': (1.0, 3.0),
        'captcha_indicators': [
            'recaptcha',
            'captcha',
            'g-recaptcha',
            'hcaptcha',
            'cf-turnstile',
        ]
    }


if __name__ == '__main__':
    # Test the defense bypass module
    bypass = DefenseBypass()
    
    print("Defense Bypass Test")
    print("=" * 40)
    
    print("\nRandom User Agents:")
    for i in range(3):
        print(f"  {i+1}. {bypass.get_random_user_agent()}")
    
    print("\nRandom Delays:")
    for i in range(3):
        print(f"  {i+1}. {bypass.get_random_delay():.2f} seconds")
    
    print("\nHeaders Rotation:")
    headers = bypass.rotate_headers()
    for key, value in headers.items():
        if key == 'User-Agent':
            print(f"  {key}: {value[:50]}...")
        else:
            print(f"  {key}: {value}")
    
    print("\nCAPTCHA Detection Test:")
    test_html = '<div class="g-recaptcha">test</div>'
    print(f"  HTML contains CAPTCHA: {bypass.detect_captcha(test_html)}")
    
    test_html_clean = '<div class="content">test</div>'
    print(f"  Clean HTML contains CAPTCHA: {bypass.detect_captcha(test_html_clean)}")
    
    print("\nRotation Strategy:")
    for attempt in [1, 2, 3]:
        strategy = bypass.get_rotation_strategy(attempt)
        print(f"  Attempt {attempt}: delay={strategy['delay_before']:.2f}s")
