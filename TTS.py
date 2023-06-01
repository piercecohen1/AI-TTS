import argparse
import io
import os
import sys
import subprocess
import requests
import xml.etree.ElementTree as ET
import sys
from bs4 import BeautifulSoup
import re
import json
from tabulate import tabulate
# Supress unncessary pygame prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def is_tool(name):
    """Check whether `name` is on PATH."""

    from shutil import which

    return which(name) is not None

def get_voices(api_key):
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        voices = data["voices"]
        table_data = [
            [
                voice["voice_id"],
                voice["name"],
                voice["category"],
            ]
            for voice in voices
        ]
        print(tabulate(table_data, headers=["Voice ID", "Name", "Category"]))
    else:
        print(f"Error: {response.text}")




def url_to_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article = soup.find('article')

    # Remove unnecessary sections
    for section in article.find_all(['aside', 'header', 'footer', 'figure', 'figcaption', 'nav', 'script']):
        section.decompose()

    # Remove hyperlinks and images from the article
    for link in article.find_all('a'):
        link.decompose()
    for img in article.find_all('img'):
        img.decompose()

    # Extract the text from the article
    text = article.get_text(separator=' ')

    # Remove unwanted characters and normalize whitespace
    text = re.sub(r'[\n]+', '\n', text)
    text = re.sub(r'[/;:]', '', text)
    text = re.sub(r'\d{4}', '', text)
    text = re.sub(r'[\n]*\w*Comments[\n]*', '', text)
    text = re.sub(r'(\n\s*)+\n+', '\n\n', text).strip()
    text = re.sub(r' +', ' ', text)
    text = re.sub(r' ?([.,?!])', r'\1', text)

    # Remove other unwanted patterns
    text = re.sub(r'Listen\s+\d+\s+min.*Share', '', text)
    text = re.sub(r'Most Popular', '', text)
    text = re.sub(r'From our sponsor', '', text)

    return text

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
            pygame.init() # To use a custom sound device, use pygame.mixer.init(devicename='name_of_device') here
            sound = pygame.mixer.Sound(io.BytesIO(response.content))
            sound.play()
            while pygame.mixer.get_busy():
                pygame.time.wait(100)
        else:
            with open(audio_file_name, "wb") as f:
                f.write(response.content)
            if os.name == 'nt':  # If on Windows, use Windows Media Player
                subprocess.call(["wmplayer", "/play", "/close", audio_file_name])
            elif sys.platform == 'darwin': # If on Mac, use afplay
                subprocess.call(["afplay", audio_file_name])
            elif sys.platform == 'linux': # If on Linux, use aplay
                subprocess.call(["mpv", audio_file_name])
            else:
                print(f"Unsupported platform: {os.name}")
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

# Check if required playback tools on linux are installed
if sys.platform == 'linux' and not is_tool('mpv'):
    print("\n'mpv' is not installed. Please install it to continue.\n")
    print("\033[1m    sudo apt install mpv\n\033[0m")
    sys.exit(1)

parser = argparse.ArgumentParser()
group1 = parser.add_mutually_exclusive_group(required=True)
group1.add_argument("-a", "--audio", help="Use /v1/text-to-speech API endpoint", action="store_const", dest="endpoint", const="audio")
group1.add_argument("-s", "--stream", help="Use /v1/text-to-speech/{voice_id}/stream API endpoint", action="store_const", dest="endpoint", const="stream")
group1.add_argument("--get-voices", help="Retrieve the available voices", action="store_true")

parser.add_argument("-v", "--voice-id", help="The ID of the voice to use")

group2 = parser.add_mutually_exclusive_group(required=False)
group2.add_argument("-t", "--text", help="The text to convert to speech")
group2.add_argument("-f", "--file", help="Text file to convert to speech")
group2.add_argument("-u", "--url", help="BETA: URL of article to convert to speech")
group2.add_argument("--ai", help="Read the latest AI news", action="store_const", dest="category", const="ai")
group2.add_argument("--gear", help="Read the latest gear news", action="store_const", dest="category", const="gear")
group2.add_argument("--business", help="Read the latest business news", action="store_const", dest="category", const="business")
group2.add_argument("--culture", help="Read the latest culture news", action="store_const", dest="category", const="culture")
group2.add_argument("--science", help="Read the latest science news", action="store_const", dest="category", const="science")
group2.add_argument("--security", help="Read the latest security news", action="store_const", dest="category", const="security")

parser.add_argument("-o", "--output", help="May be used --audio/-a only. The name of the audio file to be created. If not specified, defaults to output.wav", dest="output", required=False)

args = parser.parse_args()

api_key = os.environ.get("ELEVENLABS_API_KEY")

if api_key is None:
    print("Error: API_KEY environment variable not set")
    sys.exit(1)

voice_id = args.voice_id or "EXAVITQu4vr4xnSDxMaL"
endpoint = args.endpoint

if args.get_voices:
    get_voices(api_key)
else:
    voice_id = args.voice_id or "EXAVITQu4vr4xnSDxMaL"
    endpoint = args.endpoint

if args.category:
    text = get_news_by_category(args.category)
elif args.text:
    text = args.text
elif args.file:
    with open(args.file, "r") as f:
        text = f.read()
elif args.url:
    text = url_to_text(args.url)
else:
    text = "This is an example text to speech conversion."

try:
    if not args.get_voices:
        if args.endpoint == "stream":
            if args.output:
                raise Exception("Error: -s and -o cannot be used together")
            audio_file_name = None
        elif args.endpoint == "audio":
            audio_file_name = args.output if args.output else "output.wav"
        else:
            audio_file_name = None

        play_audio(voice_id, api_key, text, endpoint, audio_file_name)

except Exception as e:
    print(e)
    sys.exit(1)

except KeyboardInterrupt:
    print("\nExiting the program...")
    sys.exit(0)
