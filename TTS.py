import argparse
import os
from elevenlabs import set_api_key, generate, play, stream, voices, VoiceSettings, save
import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
import sys

def list_voices():
    available_voices = voices()
    for voice in available_voices.voices:
        print(f"Voice ID: {voice.voice_id}, Name: {voice.name}, Category: {voice.category}")

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

# Get ElevenLabs API key from environment variable
api_key = os.environ.get("ELEVENLABS_API_KEY")

if api_key is None:
    print("Error: API_KEY environment variable not set")
    sys.exit(1)

set_api_key(api_key)

# Setup argparse for CLI
parser = argparse.ArgumentParser()
group1 = parser.add_mutually_exclusive_group(required=True)
group1.add_argument("-a", "--audio", help="Use /v1/text-to-speech API endpoint", action="store_const", dest="endpoint", const="audio")
group1.add_argument("-s", "--stream", help="Use /v1/text-to-speech/{voice_id}/stream API endpoint", action="store_const", dest="endpoint", const="stream")
group1.add_argument("--get-voices", help="Retrieve the available voices", action="store_true")

parser.add_argument("-v", "--voice-id", help="Voice ID to use for the conversion")

group2 = parser.add_mutually_exclusive_group(required=False)
group2.add_argument("-t", "--text", help="Text to convert to speech")
group2.add_argument("-f", "--file", help="Text file to convert to speech")
group2.add_argument("-u", "--url", help="BETA: URL of article to convert to speech")
group2.add_argument("--ai", help="Read the latest AI news", action="store_const", dest="category", const="ai")
group2.add_argument("--gear", help="Read the latest gear news", action="store_const", dest="category", const="gear")
group2.add_argument("--business", help="Read the latest business news", action="store_const", dest="category", const="business")
group2.add_argument("--culture", help="Read the latest culture news", action="store_const", dest="category", const="culture")
group2.add_argument("--science", help="Read the latest science news", action="store_const", dest="category", const="science")
group2.add_argument("--security", help="Read the latest security news", action="store_const", dest="category", const="security")

parser.add_argument("-m", "--model", help="ElevenLabs model to use", default="eleven_turbo_v2")
parser.add_argument("-o", "--output", help="Output to a .wav file", dest="output", required=False)

args = parser.parse_args()

api_key = os.environ.get("ELEVENLABS_API_KEY")

if api_key is None:
    print("Error: API_KEY environment variable not set")
    sys.exit(1)

args = parser.parse_args()

# Check that some text input was provided
if (args.endpoint in ['audio', 'stream']) and not (args.text or args.file or args.url or args.category):
    print("Error: No text input provided. Please specify text, file, URL, or news category.")
    sys.exit(1)

# Check for the --get-voices argument first
if args.get_voices:
    list_voices()
    sys.exit(0)

# Determine the text to be converted
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

# Prepare arguments for text-to-speech generation
generate_args = {"text": text, "model": args.model}
if args.voice_id:
    generate_args["voice"] = args.voice_id

# Handle audio streaming
if args.endpoint == "stream":
    audio_stream = generate(stream=True, **generate_args)
    audio_bytes = stream(audio_stream)
    if args.output:
        save(audio_bytes, args.output)

# Handle audio generation and saving
elif args.endpoint == "audio":
    audio = generate(**generate_args)
    if args.output:
        save(audio, args.output)

else:
    print("Error: Invalid or missing arguments.")
    sys.exit(1)