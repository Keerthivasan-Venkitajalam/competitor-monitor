"""
Browser automation module for competitor website scraping.
Uses Playwright to navigate to URLs, wait for DOM rendering, and extract text content.
Validates: Requirements 2.1, 2.2, 2.3
"""

import asyncio
import random
import time
from typing import Optional
from playwright.async_api import async_playwright


class CompetitorBrowser:
    """Handles autonomous web browsing for competitor intelligence gathering."""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """
        Initialize the browser controller.
        
        Args:
            headless: Whether to run browser in headless mode
            timeout: Timeout in milliseconds for page operations
        """
        self.headless = headless
        self.timeout = timeout
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
    
    async def extract_text_from_url(self, url: str) -> Optional[str]:
        """
        Navigate to a URL and extract visible text content from the DOM.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Extracted text content or None if extraction failed
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            page.set_default_timeout(self.timeout)
            
            try:
                # Navigate to URL with wait for DOM content
                await page.goto(url, wait_until='domcontentloaded')
                
                # Wait for any dynamic content to load
                await page.wait_for_load_state('networkidle')
                
                # Add random delay to avoid detection
                await asyncio.sleep(random.uniform(1, 3))
                
                # Extract visible text content
                text_content = await page.evaluate('''() => {
                    // Remove script and style elements
                    const elements = document.querySelectorAll('script, style, noscript');
                    elements.forEach(el => el.remove());
                    
                    // Get body text
                    const body = document.body;
                    if (!body) return '';
                    
                    // Get all text nodes
                    const walker = document.createTreeWalker(
                        body,
                        NodeFilter.SHOW_TEXT,
                        null
                    );
                    
                    const texts = [];
                    let node;
                    while (node = walker.nextNode()) {
                        // Filter out whitespace-only text nodes
                        const text = node.textContent.trim();
                        if (text.length > 0) {
                            texts.push(text);
                        }
                    }
                    
                    return texts.join('\\n');
                }''')
                
                await browser.close()
                return text_content if text_content else None
                
            except Exception as e:
                print(f"Error extracting text from {url}: {str(e)}")
                try:
                    await browser.close()
                except:
                    pass
                return None
    
    async def extract_text_with_defense_bypass(self, url: str) -> Optional[str]:
        """
        Extract text with basic web defense bypass techniques.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Extracted text content or None if extraction failed
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport={'width': 1920, 'height': 1080},
                java_script_enabled=True
            )
            
            page = await context.new_page()
            page.set_default_timeout(self.timeout)
            
            try:
                # Navigate with multiple wait strategies
                await page.goto(url, wait_until='domcontentloaded')
                await page.wait_for_load_state('networkidle')
                
                # Add random delays between operations
                await asyncio.sleep(random.uniform(2, 4))
                
                # Scroll to trigger lazy loading
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(random.uniform(1, 2))
                
                # Extract text content
                text_content = await page.evaluate('''() => {
                    // Remove script, style, and noscript elements
                    const elements = document.querySelectorAll('script, style, noscript');
                    elements.forEach(el => el.remove());
                    
                    // Get body text
                    const body = document.body;
                    if (!body) return '';
                    
                    // Get all text nodes
                    const walker = document.createTreeWalker(
                        body,
                        NodeFilter.SHOW_TEXT,
                        null
                    );
                    
                    const texts = [];
                    let node;
                    while (node = walker.nextNode()) {
                        const text = node.textContent.trim();
                        if (text.length > 0) {
                            texts.push(text);
                        }
                    }
                    
                    return texts.join('\\n');
                }''')
                
                await browser.close()
                return text_content if text_content else None
                
            except Exception as e:
                print(f"Error with defense bypass for {url}: {str(e)}")
                try:
                    await browser.close()
                except:
                    pass
                return None


async def scrape_competitor(url: str, use_defense_bypass: bool = True) -> Optional[str]:
    """
    Convenience function to scrape a competitor's website.
    
    Args:
        url: The URL to scrape
        use_defense_bypass: Whether to use defense bypass techniques
        
    Returns:
        Extracted text content or None if extraction failed
    """
    browser = CompetitorBrowser()
    
    if use_defense_bypass:
        return await browser.extract_text_with_defense_bypass(url)
    else:
        return await browser.extract_text_from_url(url)


if __name__ == '__main__':
    # Test the browser module
    async def test():
        test_url = "https://example.com"
        print(f"Testing browser automation on {test_url}...")
        
        result = await scrape_competitor(test_url)
        if result:
            print(f"Successfully extracted {len(result)} characters")
            print(f"First 200 chars: {result[:200]}...")
        else:
            print("Failed to extract content")
    
    asyncio.run(test())
