import requests
import pygame
import argparse
import io
import os
import sys
import subprocess
import xml.etree.ElementTree as ET

def play_audio(voice_id, api_key, text, endpoint):
    # Construct the API endpoint
    api_endpoint = "https://api.elevenlabs.io/v1/text-to-speech"
    if endpoint == "stream":
        api_endpoint += f"/{voice_id}/stream"
    else:
        api_endpoint += f"/{voice_id}"

    headers = {
        "xi-api-key": api_key
    }
    data = {
        "text": text
    }

    # Make the API request
    response = requests.post(api_endpoint, headers=headers, json=data)

    # If the request was successful
    if response.status_code == 200:
        # If the endpoint is for the audio stream
        if endpoint == "stream":
            # Initialize pygame
            pygame.init()
            # Load the audio stream into memory
            sound = pygame.mixer.Sound(io.BytesIO(response.content))
            # Play the audio stream
            sound.play()
            # Wait for the audio stream to finish playing
            while pygame.mixer.get_busy():
                pygame.time.wait(100)
        else:
            # Write the audio file to disk
            with open("audio.wav", "wb") as f:
                f.write(response.content)
            # Play the audio file
            subprocess.call(["afplay", "audio.wav"])
    else:
        # If the request was not successful, print the error
        print("Error:", response.text)

def get_news_from_rss(url):
    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the XML content of the response
    root = ET.fromstring(response.content)

    # Find all the news articles in the XML
    news_articles = root.findall(".//item")

    # Concatenate the titles and descriptions of the news articles
    text = ""
    for article in news_articles:
        title = article.find("title").text
        description = article.find("description").text
        text += f"{title}\n{description}\n\n"

    return text

# Set up the argument parser
parser = argparse.ArgumentParser()

# Specify the voice ID to use for the TTS
parser.add_argument("-v", "--voice-id", required=False, help="The ID of the voice to use")

# Specify a string of text to convert to speech
parser.add_argument("-t", "--text", help="The text to convert to speech")

# Mutually exclusive arguments
group = parser.add_mutually_exclusive_group()

# AI argument to read from AI RSS feed
group.add_argument("--AI", help="Read the latest AI news", action="store_true")

# Gear argument to read from gear RSS feed
group.add_argument("--gear", help="Read the latest gear news", action="store_true")

# Gear argument to read from gear RSS feed
group.add_argument("--business", help="Read the latest business news", action="store_true")

# Culture argument to read from culture RSS feed
group.add_argument("--culture", help="Read the latest culture news", action="store_true")

# Science argument to read from science RSS feed
group.add_argument("--science", help="Read the latest science news", action="store_true")

# Security argument to read from security RSS feed
group.add_argument("--security", help="Read the latest security news", action="store_true")

# Mutually exclusive arguments
group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument("-a", "--audio", help="Use /v1/text-to-speech API endpoint", action="store_true")
group2.add_argument("-s", "--stream", help="Use /v1/text-to-speech/{voice_id}/stream API endpoint", action="store_true")

# Add the optional file argument
parser.add_argument("-f", "--file", help="Text file to convert to speech")

# Parse the arguments
args = parser.parse_args()

# Get the API key from environment variable
api_key = os.environ.get("API_KEY")
if api_key is None:
    print("Error: API_KEY environment variable not set")
    sys.exit(1)

# Determine which endpoint to use
if args.stream:
    endpoint = "stream"
else:
    endpoint = "audio"

# Default voice ID to use
voice_id = "EXAVITQu4vr4xnSDxMaL"

# Change the default if the --voice-id argument is specified
if args.voice_id:
    voice_id = args.voice_id

# Determine if the --AI argument was specified
if args.AI:
    # URL of the news website's AI RSS feed
    url = "https://www.wired.com/feed/tag/ai/latest/rss"

    # Get the news from the RSS feed
    text = get_news_from_rss(url)

    try:
        # Call the play_audio function
        play_audio(voice_id, api_key, text, endpoint)

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit(0)

# Determine if the --gear argument was specified
elif args.gear:
    # URL of the news website's gear RSS feed
    url = "https://www.wired.com/feed/category/gear/latest/rss"

    # Get the news from the RSS feed
    text = get_news_from_rss(url)

    try:
        # Call the play_audio function
        play_audio(voice_id, api_key, text, endpoint)

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit(0)

elif args.business:
    # URL of the news website's business RSS feed
    url = "https://www.wired.com/feed/category/business/latest/rss"

    # Get the news from the RSS feed
    text = get_news_from_rss(url)

    try:
        # Call the play_audio function
        play_audio(voice_id, api_key, text, endpoint)

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit(0)

elif args.culture:
    # URL of the news website's culture RSS feed
    url = "https://www.wired.com/feed/category/culture/latest/rss"

    # Get the news from the RSS feed
    text = get_news_from_rss(url)

    try:
        # Call the play_audio function
        play_audio(voice_id, api_key, text, endpoint)

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit(0)

elif args.science:
    # URL of the news website's science RSS feed
    url = "https://www.wired.com/feed/category/science/latest/rss"

    # Get the news from the RSS feed
    text = get_news_from_rss(url)

    try:
        # Call the play_audio function
        play_audio(voice_id, api_key, text, endpoint)

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit(0)

elif args.security:
    # URL of the news website's security RSS feed
    url = "https://www.wired.com/feed/category/security/latest/rss"

    # Get the news from the RSS feed
    text = get_news_from_rss(url)

    try:
        # Call the play_audio function
        play_audio(voice_id, api_key, text, endpoint)

    except KeyboardInterrupt:
        print("\nExiting the program...")
        sys.exit(0)

# Determine if the --text argument was specified
elif args.text:
    text = args.text

# Determine if a text file was passed in
elif args.file:
    with open(args.file, "r") as f:
        text = f.read()

else:
    text = "This is an example text to speech conversion."

try:
    # Call the play_audio function
    play_audio(voice_id, api_key, text, endpoint)

except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit(0)