# AI-TTS
AI TTS using [ElevenLabs API](https://api.elevenlabs.io/docs)

## Requirements
Python 3
Requests
Pygame
Usage
The program can be run with the following arguments:

usage: `text_to_voice.py [-h] [-a | -s] [-f FILE] --voice-id VOICE_ID [-t TEXT]`

optional arguments:
  `-h`, `--help`            show this help message and exit
  `-a`, `--audio`           Use /v1/text-to-speech API endpoint
  `-s`, `--stream`          Use /v1/text-to-speech/{voice_id}/stream API endpoint
  `-f FILE`, `--file FILE`  Text file to convert to speech
  `--voice-id VOICE_ID`   Voice ID to use
  `-t TEXT, --text TEXT`  Text to convert to speech
  
The `--voice-id` argument is optional and will default to the ID EXAVITQu4vr4xnSDxMaL if one is not specified. See the [/v1/voices endpoint](https://api.elevenlabs.io/docs#/voices/Get_voices_v1_voices_get) for a list of all available voices.

The API key should be set as an environment variable named API_KEY.

The program will convert either the text passed in with the -t argument or the text in the file passed in with the -f argument.

Example
To convert the text in input.txt to speech using the pNInz6obpgDQGcFmaJgB voice ID, run the following command:

`python3 TTS.py --audio -f input.txt --voice-id pNInz6obpgDQGcFmaJgB`
Limitations
The program requires a valid API key and a valid voice ID to run. The program is also limited by the capabilities of the Eleven Labs Text-to-Speech API.




