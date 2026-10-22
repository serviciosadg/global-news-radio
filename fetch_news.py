import json
import feedparser
from datetime import datetime

def main():
    try:
        with open('feeds.json', 'r') as f:
            sources = json.load(f)
    except FileNotFoundError:
        sources = []

    all_articles = []

    for source in sources:
        print(f"Fetching {source['name']}...")
        parsed = feedparser.parse(source['url'])
        
        for entry in parsed.entries[:5]: 
            all_articles.append({
                'source': source['name'],
                'category': source['category'],
                'title': entry.get('title'),
                'link': entry.get('link'),
                'published': entry.get('published', str(datetime.utcnow()))
            })

    with open('latest_news.json', 'w') as f:
        json.dump(all_articles, f, indent=4)
    
    print(f"Successfully fetched {len(all_articles)} articles.")

if __name__ == '__main__':
    main()