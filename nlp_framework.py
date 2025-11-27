"""
Main class with all methods
"""
import re
from collections import Counter
import plotly.graph_objects as go #dash creation

class TextAnalyzer:
    """ Reusable framework for text analysis """
    def __init__(self):
        """ Initialize text analyzer """
        self.data = { # nested dict allows for easier data access
            'word_counts': {},
            'total_words': {},
            'cleaned_text': {} # {label: {word: count}}
        }

    def load_stop_words(self, stopfile):
        """ Load stop words like "a", "is", "the" from file """
        with open(stopfile, 'r', encoding = 'utf-8') as f:
            for line in f:
                self.stop_words.add(set(line.strip().lower()))

    def load_text(self, filename, label=None, parser=None):
        """ Register txt file with library """

        # Read file
        if label is None: # if label does not exist
            label = str(filename.split("/")[-1].replace(".txt", "").strip())

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()

        except FileNotFoundError:
            print(f"File {filename }not found: please check file path.")

        # Parse file
        if parser: # if parser exists
            text = parser(text)

    def _preprocess(self, text):
        """ Private helper method
        Input: ONE string
        Output: cleaned text
        """

    def count_words(self, text):
        """ Open file and count words """
        with open()

        total_words = {}
        for label, v in data[word_counts]:




