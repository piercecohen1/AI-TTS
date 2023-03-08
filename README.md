# AI-TTS
AI to read the news, among other things.

AI TTS using [ElevenLabs API](https://api.elevenlabs.io/docs)

# Requirements
You will first need to install the required libraries. You can install them using pip with the following command:
`pip3 install -r requirements.txt`


# Usage
The program can be run with the following arguments:

`TTS.py [-h] [-a | -s] [-f FILE] [-v VOICE_ID] [-t TEXT] [--AI] [--gear] [--business] [--culture] [--science] [--security]`


# Arguments

  ```
  -h, --help                            show this help message and exit
  
  -a, --audio                           Use /v1/text-to-speech API endpoint
  
  -s, --stream                          Use /v1/text-to-speech/{voice_id}/stream API endpoint
  
  -f FILE, --file FILE                  Text file to convert to speech
  
  -v VOICE_ID, --voice-id VOICE_ID      Voice ID to use for the conversion
  
  -t TEXT, --text TEXT                  Text to convert to speech
    
  --AI                                  Read the latest AI news

  --gear                                Read the latest gear news

  --business                            Read the latest business news

  --culture                             Read the latest culture news

  --science                             Read the latest science news

  --security                            Read the latest security news
  
  -o OUTPUT, --output OUTPUT            May be used --audio/-a only. The name of the audio file to be created. If not specified, defaults to "output.wav"

  ```

The `--voice-id` argument is optional and will default to the ID EXAVITQu4vr4xnSDxMaL if one is not specified. See the [/v1/voices endpoint](https://api.elevenlabs.io/docs#/voices/Get_voices_v1_voices_get) for a list of all available voices.

The API key should be set as an environment variable named API_KEY.

The program will convert either the text passed in with the `-t` argument or the text in the file passed in with the `-f` argument.

# Examples
To convert the text in input.txt to speech using the pNInz6obpgDQGcFmaJgB voice ID, run the following command:

`python3 TTS.py -a -f input.txt --voice-id pNInz6obpgDQGcFmaJgB`

To directly input a string to convert to speech:

`python3 TTS.py -a --text "This is an example block of text"`

To fetch the latest AI news and read it using text to speech, run one of the following commands.

To generate an audio file with the default name audio.wav:

`python3 TTS.py -a --AI`

To generate an audio file with a custom name:

`python3 TTS.py -a --AI -o AI_news.wav`

To stream the audio only:

`python3 TTS.py -s --AI`

# Limitations

The program requires a valid Elevenlabs API key. You can get one for free by registering [here](https://elevenlabs.io).


