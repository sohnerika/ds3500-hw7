"""
Custom domain-specific parser and simple sentiment analysis
Authors: Erica Zheng, Erika Sohn, Gavin Bond
Assignment: DS3500 HW7
"""

import json
from collections import Counter
import re

# Sentiment word lists
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'best', 'positive', 'success', 'successful',
    'growth', 'strong', 'better', 'improve', 'improved', 'innovation',
    'innovative',
    'opportunity', 'achieve', 'achieved', 'win', 'winning', 'excited',
    'exciting',
    'love', 'amazing', 'fantastic', 'wonderful', 'outstanding', 'exceptional',
    'thrilled', 'confident', 'optimistic', 'proud', 'pleased', 'delighted',
    'advance', 'advanced', 'breakthrough', 'record', 'increase', 'increased',
    'efficient', 'effective', 'quality', 'reliable', 'superior', 'leading',
    'momentum', 'robust', 'healthy', 'accelerate', 'expanding', 'enhance'
}

NEGATIVE_WORDS = {
    'bad', 'poor', 'negative', 'decline', 'declined', 'decrease', 'decreased',
    'loss', 'lost', 'fail', 'failed', 'failure', 'weak', 'weakness', 'worse',
    'difficult', 'challenge', 'challenging', 'problem', 'issue', 'risk',
    'risks',
    'concern', 'concerns', 'uncertain', 'uncertainty', 'adversely', 'adverse',
    'lower', 'reduce', 'reduced', 'constraint', 'constrained', 'limited',
    'delay', 'delayed', 'disruption', 'disrupt', 'shortage', 'volatile',
    'competition', 'competitive', 'threat', 'pressure', 'downturn', 'crisis',
    'conflict', 'litigation', 'regulatory', 'compliance', 'violation'
}


def get_word_stats(words):
    """
    Core text analysis function used by all parsers.
    Takes a list of words and returns a standard stats dict.
    """
    wc = Counter(words)
    numwords = len(words)
    uniquewords = len(wc)
    avg_word_len = (
        sum(len(w) for w in words) / numwords if numwords > 0 else 0.0
    )

    # Calculate sentiment
    positive_count = sum(1 for w in words if w in POSITIVE_WORDS)
    negative_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    # Calculate sentiment score
    sentiment_score = (positive_count - negative_count) / numwords if numwords > 0 else 0.0

    return {
        "words": words,
        "wordcount": wc,
        "numwords": numwords,
        "uniquewords": uniquewords,
        "avg_word_len": avg_word_len,
        "positive_words": positive_count,
        "negative_words": negative_count,
        "sentiment_score": sentiment_score
    }


def json_parser(filename):
    """
    Custom parser for JSON files with 'text' field
    """
    with open(filename, "r", encoding="utf-8") as file:
        raw = json.load(file)
    text = raw["text"]
    return text

def html_like_parser(filename):
    """
    Custom parser for HTML-ish or SEC filings with CSS code.
    Returns cleaned plain text.
    """
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove script and style blocks
    text = re.sub(r'<script.*?>.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove ALL HTML tags
    text = re.sub(r'<[^>]*>', ' ', text)

    # Remove inline attributes: key="...", key='...', key=value
    text = re.sub(r'\b\w+\s*=\s*(".*?"|\'.*?\'|\S+)', ' ', text)

    # Remove punctuation that causes weird tokens
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()







