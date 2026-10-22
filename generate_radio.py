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

    # Unbiased news script intro with a sponsorship opportunity mention
    script = (
        "Welcome to your global hourly news update, brought to you by our proud sponsor. "
        "Here are the top unbiased headlines from around the world. "
    )
    
    for article in articles[:5]:
        script += f"From {article['source']}: {article['title']}. "

    script += "This concludes our current update. Stay tuned for more."

    print("Generating AI voice broadcast...")
    asyncio.run(text_to_speech(script))
    print("Broadcast audio generated successfully!")

if __name__ == '__main__':
    main()