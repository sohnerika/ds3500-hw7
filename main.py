"""
Main script using extensible nlp framework
Analyzes 7 FAANG + 3 chip companies' documents across different document types
Authors: Erica Zheng, Erika Sohn, Gavin Bond
Assignment: DS3500 HW7
"""
from artificial_unintelligence import ArtificialUnintelligence
import au_parsers as aup

def main():
    """
    Load documents, generate statistics, and create visualizations
    """
    print("-- LOAD DOCUMENTS -- ")
    # Initialize the framework
    print("\nInitializing framework...")
    analyzer = ArtificialUnintelligence()

    # Load stop words
    print("\nLoading stop words...")
    analyzer.load_stop_words("data/stopwords.txt")

    # Load all 7 documents with descriptive labels
    print("\nLoading documents...")

    # 10k annual reports (3 documents)
    print("  Loading Apple 10-K 2024...")
    analyzer.load_text('data/apple_10k_2024.txt', 'Apple 10-K', parser=aup.html_like_parser)

    print("  Loading Amazon 10-K 2024...")
    analyzer.load_text('data/amazon_10k_2024.txt', 'Amazon 10-K', parser=aup.html_like_parser)

    print("  Loading AMD 10-K 2024...")
    analyzer.load_text('data/amd_10k_2024.txt', 'AMD 10-K', parser=aup.html_like_parser)

    # Earnings calls (3 documents)
    print("  Loading Apple Q4 2024 Earnings Call...")
    analyzer.load_text('data/apple_earnings_q4_2024.txt', 'Apple Earnings')

    print("  Loading Netflix Q4 2024 Earnings Call...")
    analyzer.load_text('data/netflix_earnings_q4_2024.txt', 'Netflix Earnings')

    print("  Loading NVIDIA Q4 FY2025 Earnings Call...")
    analyzer.load_text('data/nvidia_earnings_q4_2025.txt', 'NVIDIA Earnings')

    # ESG reports (2 documents)
    print("  Loading Google Environmental Report 2024...")
    analyzer.load_text('data/google_esg_2024.txt',
                       'Google ESG')

    print("  Loading Intel CSR Report 2024-25...")
    analyzer.load_text('data/intel_esg_2024_25.txt', 'Intel CSR')

    print("\nAll documents loaded successfully!")

    # Display summary statistics
    print("\n-- SUMMARY STATISTICS -- ")

    print("\nTotal words per document:")
    for label, count in sorted(analyzer.data['numwords'].items(),
                               key=lambda x: x[1], reverse=True):
        print(f"{label:25s}: {count:>8,} words")

    print("\nUnique words per document:")
    for label, count in sorted(analyzer.data['uniquewords'].items(),
                               key=lambda x: x[1], reverse=True):
        print(f"{label:25s}: {count:>8,} unique words")

    print("\nAverage word length per document:")
    for label, avg_len in sorted(analyzer.data['avg_word_len'].items(),
                                 key=lambda x: x[1], reverse=True):
        print(f"{label:25s}: {avg_len:>8.2f} characters")

    print("\nDocument type breakdown:")
    print("  10-K Reports: 3 documents (Apple, Amazon, AMD)")
    print("  Earnings Calls: 3 documents (Apple, Netflix, NVIDIA)")
    print("  ESG/CSR Reports: 2 documents (Google, Intel)")
    print("  TOTAL: 7 documents")

    # Generate visualizations
    print("\n-- GENERATING VISUALIZATIONS --")
    # Viz 1: Sankey with curated words
    print("\nGenerating Sankey diagram with curated tech/business words...")

    analyzer.wordcount_sankey()
    print("Sankey diagram generated!")

    # Viz 2: Subplots
    print("\nGenerating subplot visualization...")
    try:
        analyzer.second_visualization()
        print("Subplot visualization generated!")
    except AttributeError:
        print("second_visualization() not yet implemented...")

    # Visualization 3: Overlay
    print("\nGenerating overlay visualization...")
    try:
        analyzer.third_visualization()
        print("Overlay visualization generated!")
    except AttributeError:
        print("third_visualization() not yet implemented...")

if __name__ == "__main__":
    main()
