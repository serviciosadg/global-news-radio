import asyncio
import json
import edge_tts

VOICE = "en-US-ChristopherNeural"
OUTPUT_FILE = "news_broadcast.mp3"

async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def main():
    try:
        with open('latest_news.json', 'r') as f:
            articles = json.load(f)
    except FileNotFoundError:
        articles = []

    script = (
        "Welcome to AlexDiaz Global Radio. Here is the latest update, "
        "bringing you unfiltered perspectives from East, West, and the Global South. "
        "Want your brand or business featured on this broadcast and pinned to our live feed? "
        "Click the Advertise button at the top of our page to sponsor AlexDiaz Global Radio. "
    )

    history_items = [a for a in articles if a.get('category') in ('History', 'ArchiveVault')]
    news_items = [a for a in articles if a.get('category') not in ('History', 'ArchiveVault')]

    if history_items:
        script += "First, from our Archive Vault and On This Day feature: "
        for item in history_items:
            script += f"From {item['source']}: {item['title']}. "

    script += "Now, here are the latest headlines across global news: "

    for article in news_items[:8]:
        script += f"Reporting from {article['source']}: {article['title']}. "

    script += (
        "That concludes this latest update on AlexDiaz Global Radio. "
        "Remember, sponsorship slots are open now. Click Advertise on our page to partner with us. "
        "Sign up to receive updates in your email inbox."
    )

    print("Generating AI voice broadcast...")
    asyncio.run(text_to_speech(script))
    print("Broadcast audio generated successfully!")

if __name__ == '__main__':
    main()
