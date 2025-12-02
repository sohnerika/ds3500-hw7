from collections import Counter, defaultdict
import au_parsers as aup
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"

class ArtificialUnintelligence:

    def __init__(self):
        """ Constructor to initialize state """

        # Extracted text data from files
        self.data = defaultdict(dict)
        self.stop_words = set()

    def load_stop_words(self, stopfile):
        """Load a stop word list from a file (one word per line)."""
        with open(stopfile, "r", encoding="utf-8") as f:
            self.stop_words = {line.strip().lower() for line in f if line.strip()}

    def preprocess(self, text):
        """Default preprocessing: lowercasing, splitting, stop-word removal."""
        text = text.lower()
        words = text.split()

        if self.stop_words:
            words = [w for w in words if w not in self.stop_words]

        return words

    @staticmethod
    def default_parser(filename):
        """ For processing plain text files (.txt) """
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
        return text

    def load_text(self, filename, label=None, parser=None):
        """ Register a text document with the framework.
         Extract and store data to be used later in our visualizations. """
        if parser is None:
            raw_text = ArtificialUnintelligence.default_parser(filename)
        else:
            raw_text = parser(filename)
        # Preprocess raw text after parsing
        words = self.preprocess(raw_text)
        # Pulls wanted stats from words
        results = aup.get_word_stats(words)
        # Use filename for the label if none is provided
        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def wordcount_sankey(self, word_list=None, k=5):
        """
         Map each text to words using a Sankey diagram, where the thickness of the line
        # is the number of times that word occurs in the text. Users can specify a particular
        # set of words, or the words can be the union of the k most common words across
        # each text file (excluding stop words)
        """
        # 1) Get wordcount data: dict[label -> Counter]
        if "wordcount" not in self.data:
            print("No wordcount data available. Did you load any texts?")
            return

        wordcounts = self.data["wordcount"]  # {label: Counter(...)}
        doc_labels = list(wordcounts.keys())

        # 2) Decide which words to include
        if word_list is not None:
            # Use caller-provided word list, respecting stop words if any
            selected_words = [
                w for w in word_list
                if not self.stop_words or w not in self.stop_words
            ]
        else:
            # Build union of top-k words from each document (excluding stop words)
            selected_set = set()
            for label, wc in wordcounts.items():
                for w, _c in wc.most_common(k):
                    if not self.stop_words or w not in self.stop_words:
                        selected_set.add(w)
            selected_words = sorted(selected_set)

        if not selected_words:
            print("No words selected for Sankey (maybe all filtered out).")
            return

        # 3) Build node labels: first all documents, then all selected words
        word_labels = selected_words
        node_labels = doc_labels + word_labels

        # Map each label to a node index
        label_to_index = {lab: i for i, lab in enumerate(node_labels)}

        # 4) Build link lists (source, target, value)
        sources = []
        targets = []
        values = []

        for doc in doc_labels:
            wc = wordcounts[doc]
            for w in word_labels:
                count = wc.get(w, 0)
                if count > 0:
                    sources.append(label_to_index[doc])  # text node index
                    targets.append(label_to_index[w])  # word node index
                    values.append(count)  # word count

        if not sources:
            print("No non-zero counts for the selected words.")
            return

        # 5) Create Sankey figure
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=node_labels,
                pad=40,
                thickness=20,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
            )
        )])

        fig.update_layout(
            title_text="Text-to-Word Sankey Diagram",
            font_size=10
        )
        fig.show()
