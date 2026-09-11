"""
Exercise 5: Part 4 - Mini-Project Implementation
CLI Text Processing & Word Statistics Tool.
Demonstrates structured OOP concepts, explicit error handling, and type safety.
"""

import sys
import re
from typing import Dict, List, Tuple


class TextAnalyzer:
    """Encapsulates text processing, tokenization, and statistical metrics."""
    
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self._tokens = self._tokenize()

    def _tokenize(self) -> List[str]:
        # Extract lowercase alphanumeric words
        return re.findall(r'\b\w+\b', self.raw_text.lower())

    def word_count(self) -> int:
        return len(self._tokens)

    def unique_word_count(self) -> int:
        return len(set(self._tokens))

    def word_frequencies(self) -> Dict[str, int]:
        freqs: Dict[str, int] = {}
        for token in self._tokens:
            freqs[token] = freqs.get(token, 0) + 1
        return freqs

    def top_words(self, limit: int = 5) -> List[Tuple[str, int]]:
        freqs = self.word_frequencies()
        sorted_freqs = sorted(freqs.items(), key=lambda item: item[1], reverse=True)
        return sorted_freqs[:limit]


def run_analysis(text_sample: str):
    print("=" * 50)
    print("TEXT PROCESSING & ANALYSIS REPORT")
    print("=" * 50)
    analyzer = TextAnalyzer(text_sample)
    print(f"Total Word Count:  {analyzer.word_count()}")
    print(f"Unique Words:      {analyzer.unique_word_count()}")
    print("\nTop 5 Most Frequent Words:")
    for word, count in analyzer.top_words(5):
        print(f"  - {word}: {count}")
    print("=" * 50)


if __name__ == "__main__":
    sample = """
    FastAPI is a modern, fast web framework for building APIs with Python.
    Python is versatile, readable, and powerful. FastAPI makes Python web development
    fast, effective, and enjoyable for developers worldwide.
    """
    run_analysis(sample)
