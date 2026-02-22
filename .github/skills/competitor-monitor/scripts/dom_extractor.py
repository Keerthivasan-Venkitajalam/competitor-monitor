"""
DOM text extraction utilities for competitor scraping.
Parses HTML and extracts visible text content, excluding scripts, styles, and hidden elements.
Validates: Requirements 2.3
"""

import re
from typing import Optional


class DOMTextExtractor:
    """Extracts visible text content from HTML DOM."""
    
    # Tags to exclude from text extraction
    EXCLUDED_TAGS = {'script', 'style', 'noscript', 'meta', 'head', 'title', 'link', 'br'}
    
    # CSS selectors for hidden elements
    HIDDEN_SELECTORS = [
        '[style*="display: none"]',
        '[style*="display:none"]',
        '[class*="hidden"]',
        '[aria-hidden="true"]',
        '[data-hidden="true"]',
    ]
    
    def __init__(self):
        """Initialize the DOM text extractor."""
        self.text_nodes = []
    
    def extract_text(self, html_content: str) -> str:
        """
        Extract visible text content from HTML.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Extracted text content
        """
        # Remove script and style elements
        html = self._remove_excluded_tags(html_content)
        
        # Remove hidden elements
        html = self._remove_hidden_elements(html)
        
        # Extract text
        text = self._html_to_text(html)
        
        # Clean up text
        text = self._clean_text(text)
        
        return text
    
    def _remove_excluded_tags(self, html: str) -> str:
        """Remove script, style, and other excluded tags."""
        # Remove script tags and their content
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove style tags and their content
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove noscript tags
        html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        return html
    
    def _remove_hidden_elements(self, html: str) -> str:
        """Remove hidden elements from HTML."""
        # Remove elements with display: none
        html = re.sub(r'<[^>]*style="[^"]*display:\s*none[^"]*"[^>]*>.*?</[^>]+>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<[^>]*style=\'[^\']*display:\s*none[^\']*\'[^>]*>.*?</[^>]+>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove elements with hidden class
        html = re.sub(r'<[^>]*class="[^"]*hidden[^"]*"[^>]*>.*?</[^>]+>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<[^>]*class=\'[^\']*hidden[^\']*\'[^>]*>.*?</[^>]+>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove elements with aria-hidden="true"
        html = re.sub(r'<[^>]*aria-hidden="true"[^>]*>.*?</[^>]+>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        return html
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html)
        
        # Replace HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean up extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        
        # Filter empty lines
        lines = [line for line in lines if line]
        
        # Join lines
        text = '\n'.join(lines)
        
        # Remove excessive newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def extract_text_nodes(self, html_content: str) -> list[str]:
        """
        Extract all visible text nodes from HTML.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            List of text nodes
        """
        # Remove excluded tags
        html = self._remove_excluded_tags(html_content)
        
        # Remove hidden elements
        html = self._remove_hidden_elements(html)
        
        # Extract text nodes
        text = self._html_to_text(html)
        text = self._clean_text(text)
        
        # Split into individual text nodes
        nodes = [node.strip() for node in text.split('\n') if node.strip()]
        
        return nodes
    
    def get_text_statistics(self, html_content: str) -> dict:
        """
        Get statistics about extracted text.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Dictionary with text statistics
        """
        text = self.extract_text(html_content)
        
        return {
            'total_characters': len(text),
            'total_words': len(text.split()),
            'total_lines': len(text.split('\n')),
            'average_word_length': sum(len(word) for word in text.split()) / max(len(text.split()), 1),
            'average_line_length': sum(len(line) for line in text.split('\n')) / max(len(text.split('\n')), 1),
        }


def extract_text_from_html(html_content: str) -> str:
    """
    Convenience function to extract text from HTML.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        Extracted text content
    """
    extractor = DOMTextExtractor()
    return extractor.extract_text(html_content)


def extract_text_nodes_from_html(html_content: str) -> list[str]:
    """
    Convenience function to extract text nodes from HTML.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        List of text nodes
    """
    extractor = DOMTextExtractor()
    return extractor.extract_text_nodes(html_content)


if __name__ == '__main__':
    # Test the DOM extractor
    test_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <style>body { color: black; }</style>
    </head>
    <body>
        <h1>Welcome to Our Site</h1>
        <p>This is a paragraph with <strong>bold text</strong>.</p>
        <script>alert("This should be removed");</script>
        <div class="hidden">This is hidden</div>
        <div style="display: none">This is also hidden</div>
        <p>Another paragraph with <em>italic text</em>.</p>
        <nav>
            <a href="/home">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </nav>
        <footer>
            <p>Copyright 2024</p>
        </footer>
    </body>
    </html>
    '''
    
    extractor = DOMTextExtractor()
    
    print("DOM Text Extractor Test")
    print("=" * 40)
    
    print("\nOriginal HTML:")
    print(test_html[:200] + "...")
    
    print("\nExtracted Text:")
    text = extractor.extract_text(test_html)
    print(text)
    
    print("\nText Statistics:")
    stats = extractor.get_text_statistics(test_html)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nText Nodes:")
    nodes = extractor.extract_text_nodes(test_html)
    for i, node in enumerate(nodes, 1):
        print(f"  {i}. {node}")
