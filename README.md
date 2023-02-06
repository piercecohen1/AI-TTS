# AI-TTS
AI TTS using [ElevenLabs API](https://api.elevenlabs.io/docs)

# Usage
The program can be run with the following arguments:

`text_to_voice.py [-h] [-a | -s] [-f FILE] [-v VOICE_ID] [-t TEXT] [--news]`


# Arguments

  ```
  -h, --help                            show this help message and exit
  
  -a, --audio                           Use /v1/text-to-speech API endpoint
  
  -s, --stream                          Use /v1/text-to-speech/{voice_id}/stream API endpoint
  
  -f FILE, --file FILE                  Text file to convert to speech
  
  -v VOICE_ID, --voice-id VOICE_ID      Voice ID to use for the conversion
  
  -t TEXT, --text TEXT                  Text to convert to speech
  
  --news                                Fetch the latest AI news and read it aloud (must specify -a or -s)

  ```
  
The `--voice-id` argument is optional and will default to the ID EXAVITQu4vr4xnSDxMaL if one is not specified. See the [/v1/voices endpoint](https://api.elevenlabs.io/docs#/voices/Get_voices_v1_voices_get) for a list of all available voices.

The API key should be set as an environment variable named API_KEY.

The program will convert either the text passed in with the -t argument or the text in the file passed in with the -f argument.

# Example
To convert the text in input.txt to speech using the pNInz6obpgDQGcFmaJgB voice ID, run the following command:

`python3 TTS.py --audio -f input.txt --voice-id pNInz6obpgDQGcFmaJgB`

To fetch the latest AI news and read it using text to speech, run one of the following commands.

To generate an audio file:

`python3 TTS.py -a --news`

To stream the audio only:

`python3 TTS.py -s --news`

# Limitations

The program requires a valid Elevenlabs API key. You can get one for free by registering [here](https://elevenlabs.io).


