import argparse
import io
import os
import sys
import subprocess
import requests
import pygame
import xml.etree.ElementTree as ET

def play_audio(voice_id, api_key, text, endpoint, audio_file_name):
    """Plays audio by making a TTS API request.

    Args:
    voice_id: The ID of the voice to use.
    api_key: The API key to authenticate the request.
    text: The text to convert to speech.
    endpoint: The TTS API endpoint to use.
    audio_file_name: The name of the audio file to be created
    """

    api_endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    if endpoint == "stream":
        api_endpoint += "/stream"

    headers = {
        "xi-api-key": api_key
    }
    data = {
        "text": text
    }

    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        if endpoint == "stream":
            pygame.init()
            sound = pygame.mixer.Sound(io.BytesIO(response.content))
            sound.play()
            while pygame.mixer.get_busy():
                pygame.time.wait(100)
        else:
            with open(audio_file_name, "wb") as f:
                f.write(response.content)
            subprocess.call(["afplay", audio_file_name])
    else:
        print(f"Error: {response.text}")

def get_news_by_category(category):
    """Returns the news for the given category by parsing an RSS feed.

    Args:
    category: The name of the category to retrieve news for.

    Returns:
    The concatenated titles and descriptions of the news articles.
    """
    categories = {
        "ai": "https://www.wired.com/feed/tag/ai/latest/rss",
        "gear": "https://www.wired.com/feed/category/gear/latest/rss",
        "business": "https://www.wired.com/feed/category/business/latest/rss",
        "culture": "https://www.wired.com/feed/category/culture/latest/rss",
        "science": "https://www.wired.com/feed/category/science/latest/rss",
        "security": "https://www.wired.com/feed/category/security/latest/rss",
    }
    url = categories.get(category)
    if not url:
        return None

    response = requests.get(url)
    root = ET.fromstring(response.content)
    news_articles = root.findall(".//item")
    text = ""
    for article in news_articles:
        title = article.find("title").text
        description = article.find("description").text
        text += f"{title}\n{description}\n\n"

    return text

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--voice-id", help="The ID of the voice to use")
group = parser.add_mutually_exclusive_group()
group.add_argument("--ai", help="Read the latest AI news", action="store_const", dest="category", const="ai")
group.add_argument("--gear", help="Read the latest gear news", action="store_const", dest="category", const="gear")
group.add_argument("--business", help="Read the latest business news", action="store_const", dest="category", const="business")
group.add_argument("--culture", help="Read the latest culture news", action="store_const", dest="category", const="culture")
group.add_argument("--science", help="Read the latest science news", action="store_const", dest="category", const="science")
group.add_argument("--security", help="Read the latest security news", action="store_const", dest="category", const="security")
parser.add_argument("-t", "--text", help="The text to convert to speech")
parser.add_argument("-f", "--file", help="Text file to convert to speech")

group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument("-a", "--audio", help="Use /v1/text-to-speech API endpoint", action="store_const", dest="endpoint", const="audio")
group2.add_argument("-s", "--stream", help="Use /v1/text-to-speech/{voice_id}/stream API endpoint", action="store_const", dest="endpoint", const="stream")

if "--audio" in sys.argv or "-a" in sys.argv:
    parser.add_argument("-o", "--output", help="The name of the audio file to be created")

args = parser.parse_args()

api_key = os.environ.get("API_KEY")

if api_key is None:
    print("Error: API_KEY environment variable not set")
    sys.exit(1)

voice_id = args.voice_id or "EXAVITQu4vr4xnSDxMaL"
endpoint = args.endpoint
audio_file_name = args.output if args.output else "audio.wav"

if args.category:
    text = get_news_by_category(args.category)
elif args.text:
    text = args.text
elif args.file:
    with open(args.file, "r") as f:
        text = f.read()
else:
    text = "This is an example text to speech conversion."

try:
    play_audio(voice_id, api_key, text, endpoint, audio_file_name)
except KeyboardInterrupt:
    print("\nExiting the program...")
    sys.exit(0)
