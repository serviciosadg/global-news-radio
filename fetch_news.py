import json
import re
import urllib.request
import urllib.parse
import feedparser
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def extract_thumbnail(entry):
    if 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
        return entry.media_thumbnail[0].get('url', '')
    if 'media_content' in entry and len(entry.media_content) > 0:
        for m in entry.media_content:
            if m.get('url') and ('image' in m.get('type', 'image') or m.get('url', '').endswith(('.jpg', '.png', '.webp', '.jpeg'))):
                return m.get('url')
    summary = entry.get('summary', '') or entry.get('description', '')
    match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
    if match:
        return match.group(1)
    return ''

def fetch_feed_with_timeout(url, timeout=5):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            return feedparser.parse(content)
    except Exception as e:
        print(f"Skipping feed due to timeout/error ({url}): {e}")
        return None

def main():
    try:
        with open('feeds.json', 'r') as f:
            sources = json.load(f)
    except FileNotFoundError:
        sources = []

    grouped_articles = []

    for source in sources:
        print(f"Fetching {source['name']}...")
        parsed = fetch_feed_with_timeout(source['url'], timeout=5)
        if parsed and hasattr(parsed, 'entries'):
            source_list = []
            for entry in parsed.entries[:4]:
                source_list.append({
                    'source': source['name'],
                    'category': source['category'],
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', '#'),
                    'thumbnail': extract_thumbnail(entry),
                    'published': entry.get('published', datetime.utcnow().isoformat())
                })
            if source_list:
                grouped_articles.append(source_list)

    # Interleave sources evenly
    mixed_articles = []
    for i in range(4):
        for group in grouped_articles:
            if i < len(group):
                mixed_articles.append(group[i])

    with open('latest_news.json', 'w') as f:
        json.dump(mixed_articles, f, indent=4)

    print(f"Successfully saved {len(mixed_articles)} items.")

if __name__ == '__main__':
    main()
