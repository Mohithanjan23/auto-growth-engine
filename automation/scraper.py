import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
from datetime import datetime
import os

# --- CONFIGURATION ---
TARGET_URL = "https://thehackernews.com/"
HTML_TEMPLATE_PATH = "../website/index.html" 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # Professional labeling logic
    if polarity < -0.1:
        return "status-critical", "CRITICAL THREAT"
    elif polarity > 0.1:
        return "status-success", "POSITIVE UPDATE"
    else:
        return "status-neutral", "GENERAL INFO"

def fetch_cyber_news():
    print(f"Connecting to {TARGET_URL}...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        articles = soup.find_all('h2', class_='home-title', limit=9)
        
        for item in articles:
            title = item.get_text(strip=True)
            parent = item.find_parent('a')
            link = parent['href'] if parent else "#"
            css_class, label = analyze_sentiment(title)
            
            news_items.append({
                'title': title,
                'link': link,
                'css_class': css_class,
                'label': label,
                'date': datetime.now().strftime("%b %d, %Y")
            })
        return news_items
    except Exception as e:
        print(f"Error: {e}")
        return []

def update_website(data):
    print("Updating system dashboard...")
    
    html_content = ""
    for item in data:
        html_content += f"""
        <article class="report-card">
            <div class="card-header">
                <span class="status-badge {item['css_class']}">{item['label']}</span>
                <span class="report-date">{item['date']}</span>
            </div>
            <h3 class="report-title">
                <a href="{item['link']}" target="_blank">{item['title']}</a>
            </h3>
            <div class="card-footer">
                <a href="{item['link']}" target="_blank" class="read-more">Read Full Report &rarr;</a>
            </div>
        </article>
        """

    try:
        with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as file:
            template = file.read()
            
        soup = BeautifulSoup(template, "html.parser")
        feed_container = soup.find(id="feed-container")
        
        if feed_container:
            feed_container.clear()
            feed_container.append(BeautifulSoup(html_content, 'html.parser'))
            
            with open(HTML_TEMPLATE_PATH, "w", encoding="utf-8") as file:
                file.write(str(soup.prettify()))
            print("Dashboard updated successfully.")
        else:
            print("Target container ID 'feed-container' not found.")

    except FileNotFoundError:
        print(f"Template file not found at: {HTML_TEMPLATE_PATH}")

if __name__ == "__main__":
    data = fetch_cyber_news()
    if data:
        update_website(data)