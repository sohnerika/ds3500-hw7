from artificial_unintelligence import ArtificialUnintelligence
import au_parsers as aup
import pprint as pp

def main():
    tt = ArtificialUnintelligence()

    tt.load_stop_words("data/stopwords.txt")
    tt.load_text('data/appl_10k_2023.txt', 'A')
    tt.load_text('data/apple_earnings_q4_2024.txt', 'B')

    pp.pprint(tt.data)

    # Option A: use union of top-k words from each text
    tt.wordcount_sankey(k=5)

main()

