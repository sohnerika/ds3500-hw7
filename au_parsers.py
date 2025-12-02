
"""
An example of a custom domain-specific parser
"""

import json
from collections import Counter

def get_word_stats(words):
    """
    Core text analysis function used by all parsers.
    Takes a raw string of text and returns a standard stats dict.
    """
    wc = Counter(words)
    numwords = len(words)
    uniquewords = len(wc)
    avg_word_len = (
        sum(len(w) for w in words) / numwords if numwords > 0 else 0.0
    )
    # Pull out specific words
    return {
        "words": words,
        "wordcount": wc,
        "numwords": numwords,
        "uniquewords": uniquewords,
        "avg_word_len": avg_word_len,
    }

def json_parser(filename):
    with open(filename, "r", encoding="utf-8") as file:
        raw = json.load(file)
    text = raw["text"]

    return text






