import pandas as pd
from collections import Counter
import re

# Configuration
CSV_FILE = "security_trends.csv"

def get_top_keywords():
    print("--- Keyword Intelligence Started ---")
    
    try:
        # Load the data we scraped
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            print("No data found. Run scraper.py first.")
            return

        # Combine all headlines into one giant string
        text = " ".join(df['Headline'].astype(str).tolist()).lower()
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        # Split into words
        words = text.split()
        
        # Filter out boring words (stopwords)
        stopwords = set(['the', 'a', 'an', 'to', 'for', 'in', 'on', 'of', 'and', 'is', 'with', 'new', 'how'])
        filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Count frequency
        counts = Counter(filtered_words)
        top_10 = counts.most_common(10)
        
        print("\n Top Trending Keywords:")
        print("-------------------------")
        for word, count in top_10:
            print(f"{word.ljust(15)} : {count} mentions")
            
        print("\n Recommendation: Write an article about:", top_10[0][0].upper())

    except FileNotFoundError:
        print(f" Could not find {CSV_FILE}. Run scraper.py first!")

if __name__ == "__main__":
    get_top_keywords()