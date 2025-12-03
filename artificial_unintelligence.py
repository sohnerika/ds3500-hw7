"""
Custom domain-specific parser
Authors: Erica Zheng, Erika Sohn, Gavin Bond
Assignment: DS3500 HW7
"""

from collections import Counter, defaultdict
import au_parsers as aup
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import re

pio.renderers.default = "browser"


class ArtificialUnintelligence:

    def __init__(self):
        """ Constructor to initialize state """

        # Extracted text data from files
        self.data = defaultdict(dict)
        self.stop_words = set()

    def load_stop_words(self, stopfile):
        """Load a stop word list from a file (one word per line) """
        with open(stopfile, "r", encoding="utf-8") as f:
            self.stop_words = {line.strip().lower() for line in f if
                               line.strip()}

    def preprocess(self, text):
        """
        Super aggressive preprocessing to remove ALL HTML/CSS/formatting artifacts
        """
        # Remove all HTML tags and formatting
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'&[a-z]+;', ' ', text)
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'http\S+|www\.\S+', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        words = text.split()

        # Remove stop words
        if self.stop_words:
            words = [w for w in words if w not in self.stop_words]

        # Filter out very short words
        words = [w for w in words if len(w) >= 3]

        # HTML/CSS formatting artifacts list
        formatting_artifacts = {
            'div', 'span', 'table', 'tbody', 'thead', 'tfoot', 'tr', 'td', 'th',
            'ul', 'ol', 'li', 'br', 'hr', 'img', 'href', 'src', 'alt',
            'html', 'head', 'body', 'title', 'meta', 'link', 'script', 'style',
            'form', 'input', 'button', 'select', 'option', 'textarea',

            'class', 'name', 'type', 'value', 'width', 'height', 'border',
            'colspan', 'rowspan', 'align', 'valign', 'bgcolor', 'color',
            'cellpadding', 'cellspacing', 'background', 'margin', 'padding',

            'font', 'size', 'weight', 'family', 'bold', 'italic', 'underline',
            'text', 'left', 'right', 'center', 'top', 'bottom', 'middle',
            'vertical', 'horizontal', 'position', 'display', 'float', 'clear',

            'px', 'pt', 'em', 'rem', 'vh', 'vw', 'pct', 'percent',

            'nbsp', 'amp', 'lt', 'gt', 'quot', 'apos',

            'pdf', 'xml', 'xbrl', 'htm', 'html', 'json', 'csv', 'txt',
            'iso', 'utf', 'ascii', 'unicode',

            'rgb', 'rgba', 'hex', 'url', 'none', 'auto', 'inherit',
            'hidden', 'visible', 'inline', 'block', 'flex', 'grid'
        }

        # Filter out all formatting artifacts
        words = [w for w in words if w not in formatting_artifacts]

        return words


    @staticmethod
    def default_parser(filename):
        """ For processing txt files """
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
        return text

    def load_text(self, filename, label=None, parser=None):
        """ Register a text document with the framework.
         Extract and store data to be used later in our visualizations """
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
        """

        # Step 1: get wordcount data: dict[label -> Counter]
        if "wordcount" not in self.data:
            print("No wordcount data available. Did you load any texts?")
            return

        wordcounts = self.data["wordcount"]  # {label: Counter(...)}
        doc_labels = list(wordcounts.keys())

        # Step 2: decide which words to include
        if word_list is not None:
            # Use caller to caller provided word list
            selected_words = [
                w for w in word_list
                if not self.stop_words or w not in self.stop_words
            ]
        else:
            # Build union of top words from each document (excl stop words)
            selected_set = set()
            for label, wc in wordcounts.items():
                for w, _c in wc.most_common(k):
                    if not self.stop_words or w not in self.stop_words:
                        selected_set.add(w)
            selected_words = sorted(selected_set)

        if not selected_words:
            print("No words selected for Sankey (maybe all filtered out).")
            return

        # Step 3: build node labels
        word_labels = selected_words
        node_labels = doc_labels + word_labels

        # Map each label to a node index
        label_to_index = {lab: i for i, lab in enumerate(node_labels)}

        # Step 4: build link lists (src, targ, val)
        src = []
        targ = []
        val = []

        for doc in doc_labels:
            wc = wordcounts[doc]
            for w in word_labels:
                count = wc.get(w, 0)
                if count > 0:
                    src.append(label_to_index[doc])  # text node index
                    targ.append(label_to_index[w])  # word node index
                    val.append(count)  # word count

        if not src:
            print("No non-zero counts for the selected words.")
            return

        # Step 5: create Sankey figure
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=node_labels,
                pad=40,
                thickness=20,
            ),
            link=dict(
                source=src,
                target=targ,
                value=val,
            )
        )])

        fig.update_layout(
            title_text="Text-to-Word Sankey Diagram",
            font_size=10
        )
        fig.show()

    def second_visualization(self):
        """
        Viz 2: Subplots showing sentiment analysis for each document
        Creates a grid of bar charts showing positive vs negative word counts
        """

        # Get data
        doc_labels = list(self.data['positive_words'].keys())
        num_docs = len(doc_labels)

        # Calculate grid dimensions
        cols = int(np.ceil(np.sqrt(num_docs)))
        rows = int(np.ceil(num_docs / cols))

        # Create figure with subplots
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
        fig.suptitle(
            'Sentiment Analysis: Positive vs Negative Words by Document',
            fontsize=16, fontweight='bold', y=0.998)

        # Flatten axes arr for easier iteration
        if num_docs == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        # Create a subplot for each document
        for idx, label in enumerate(doc_labels):
            ax = axes[idx]

            # Get sentiment counts
            pos_count = self.data['positive_words'][label]
            neg_count = self.data['negative_words'][label]
            total_words = self.data['numwords'][label]

            # Calculate percentages
            pos_pct = (pos_count / total_words * 100) if total_words > 0 else 0
            neg_pct = (neg_count / total_words * 100) if total_words > 0 else 0

            # Create bar chart
            categories = ['Positive', 'Negative']
            counts = [pos_count, neg_count]
            colors = ['#2ecc71', '#e74c3c']  # Green = positive, red = negative

            # Add count labels on bars
            bars = ax.bar(categories, counts, color=colors, alpha=0.7,
                          edgecolor='black', linewidth=1.5,
                          label=categories)  # Add labels for legend

            for bar, count, pct in zip(bars, counts, [pos_pct, neg_pct]):
                height = bar.get_height()

            ax.set_title(label, fontsize=11, fontweight='bold', pad=10)
            ax.set_ylabel('Word Count', fontsize=10)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)

            # Add legend
            if idx == 0:
                ax.legend(loc='upper left', fontsize=9, framealpha=0.9)

            ax.text(0.98, 0.98, f'Total: {total_words:,} words',
                    transform=ax.transAxes, fontsize=8,
                    verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='lightblue',
                              alpha=0.9))

        for idx in range(num_docs, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        plt.savefig('sentiment_analysis.png', dpi=300,
                    bbox_inches='tight')  # Add this line
        plt.show()

    def third_visualization(self):
        """
        Viz 3: Overlay plot comparing all documents
        Single plot with multiple metrics overlaid for comparison
        """
        # Get document labels
        doc_labels = list(self.data['numwords'].keys())

        # Create figure with secondary y axis
        fig, ax1 = plt.subplots(figsize=(14, 8))

        # X axis positions
        x_pos = np.arange(len(doc_labels))
        bar_width = 0.25

        # Data to plot
        total_words = [self.data['numwords'][label] for label in doc_labels]
        unique_words = [self.data['uniquewords'][label] for label in doc_labels]
        avg_word_len = [self.data['avg_word_len'][label] for label in
                        doc_labels]

        # Plot bars for total and unique words on primary y axis
        bars1 = ax1.bar(x_pos - bar_width, total_words, bar_width,
                        label='Total Words', color='#3498db', alpha=0.8,
                        edgecolor='black')
        bars2 = ax1.bar(x_pos, unique_words, bar_width,
                        label='Unique Words', color='#9b59b6', alpha=0.8,
                        edgecolor='black')

        ax1.set_xlabel('Document', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Word Count', fontsize=12, fontweight='bold',
                       color='black')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(doc_labels, rotation=45, ha='right')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.set_axisbelow(True)

        # Create secondary y axis for avg word length
        ax2 = ax1.twinx()
        line = ax2.plot(x_pos + bar_width, avg_word_len,
                        color='#e74c3c', marker='o', linewidth=2, markersize=8,
                        label='Avg Word Length', linestyle='--')
        ax2.set_ylabel('Average Word Length (characters)', fontsize=12,
                       fontweight='bold', color='black')  # Changed to black
        ax2.tick_params(axis='y', labelcolor='black')  # Changed to black

        # Add value labels online
        for i, (x, y) in enumerate(zip(x_pos + bar_width, avg_word_len)):
            ax2.text(x, y, f'{y:.1f}', ha='center', va='bottom',
                     fontsize=9, fontweight='bold', color='#e74c3c')

        plt.title('Document Comparison: Word Statistics Overlay',
                  fontsize=16, fontweight='bold', pad=20)

        # Combined legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2,
                   loc='upper left', fontsize=10, framealpha=0.9)

        plt.tight_layout()
        plt.savefig('word_statistics_overlay.png', dpi=300,
                    bbox_inches='tight')  # Add this line
        plt.show()