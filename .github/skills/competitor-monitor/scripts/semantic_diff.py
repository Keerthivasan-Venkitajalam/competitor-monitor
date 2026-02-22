"""
Semantic diffing engine for competitor intelligence.
Uses sentence-transformers to calculate cosine similarity between text embeddings.
Validates: Requirements 4.1, 4.2, 4.5
"""

import json
import sys
from typing import Optional

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError as e:
    print(json.dumps({"error": f"Missing dependency: {e}"}))
    sys.exit(1)


class SemanticDiffer:
    """Performs semantic diffing using sentence embeddings."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the semantic differ.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text: str) -> list[float]:
        """
        Embed a text string into a vector.
        
        Args:
            text: Text to embed
            
        Returns:
            List of embedding values
        """
        embedding = self.model.encode([text])[0]
        return embedding.tolist()
    
    def calculate_similarity(self, text1: str, text2: str) -> dict:
        """
        Calculate cosine similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Dictionary with similarity percentage and embeddings
        """
        # Embed both texts
        embeddings = self.model.encode([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        # Convert to percentage (0-100)
        similarity_percentage = ((similarity + 1) / 2) * 100
        
        # Classify based on threshold (0.80 = 80%)
        threshold = 0.80
        is_strategic_shift = similarity < threshold
        
        return {
            "similarity_percentage": round(float(similarity_percentage), 2),
            "cosine_similarity": round(float(similarity), 4),
            "threshold": float(threshold),
            "shift_classification": "Strategic_Shift" if bool(is_strategic_shift) else "minor_update",
            "is_strategic_shift": bool(is_strategic_shift),
            "text1_embedding": [float(x) for x in embeddings[0].tolist()],
            "text2_embedding": [float(x) for x in embeddings[1].tolist()],
        }
    
    def diff_texts(self, current_text: str, historical_text: str) -> dict:
        """
        Perform semantic diffing between current and historical text.
        
        Args:
            current_text: Current text content
            historical_text: Historical text content
            
        Returns:
            Dictionary with diff results
        """
        return self.calculate_similarity(current_text, historical_text)


def main():
    """Main entry point for the semantic diffing CLI."""
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: python semantic_diff.py <current_text_file> <historical_text_file>"}))
        sys.exit(1)
    
    current_file = sys.argv[1]
    historical_file = sys.argv[2]
    
    try:
        # Read text files
        with open(current_file, 'r', encoding='utf-8') as f:
            current_text = f.read()
        
        with open(historical_file, 'r', encoding='utf-8') as f:
            historical_text = f.read()
        
        # Perform semantic diffing
        differ = SemanticDiffer()
        result = differ.diff_texts(current_text, historical_text)
        
        # Output JSON result
        print(json.dumps(result, indent=2))
        
    except FileNotFoundError as e:
        print(json.dumps({"error": f"File not found: {e}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Error during diffing: {e}"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
