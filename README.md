# AI-TTS

AI TTS using [ElevenLabs API](https://api.elevenlabs.io/docs)

# Requirements
You will first need to install the required libraries. You can install them using pip with the following command:
`pip3 install -r requirements.txt`

For an isolated environment (recommended), create and activate a virtual environment using:

```
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
pip3 install -r requirements.txt
```

To use the program, you need to supply your ElevenLabs API key. You can obtain an API key by registering [here](https://elevenlabs.io). After obtaining your API key, you should set it as an environment variable named ELEVENLABS_API_KEY. 

**Follow these steps to set the ELEVENLABS_API_KEY environment variable persistently (recommended):**

- On Linux or macOS:
  1. Open a terminal window.
  2. Open your `.zshrc` file with your favorite text editor. For example: `nano ~/.zshrc`
  3. Add the following line at the end of the file: `export ELEVENLABS_API_KEY=your_api_key_here`
  4. Make sure to replace `your_api_key_here` with your actual API key.
  5. Save the changes and exit the text editor.
  6. Run `source ~/.zshrc` in the terminal to load the changes.

- On Windows:
  1. Right-click on the Computer icon and select Properties.
  2. Click on the Advanced system settings link.
  3. In the System Properties window, click on the Advanced tab.
  4. Click on the Environment Variables button.
  5. In the System Variables section, click on the New button.
  6. In the New System Variable window, enter `ELEVENLABS_API_KEY` for the Variable name and your actual API key for the Variable value.
  7. Click OK to save the changes, and then click OK on the Environment Variables and System Properties windows.
  8. Close and reopen any Command Prompt or PowerShell windows for the changes to take effect.


Alternatively, you can set the ELEVENLABS_API_KEY environment variable temporarily, for the current session only, as follows:

- On Linux or macOS:
  1. Open a terminal window.
  2. Run the following command: `export ELEVENLABS_API_KEY=your_api_key_here`
  3. Make sure to replace `your_api_key_here` with your actual API key.

- On Windows:
  1. Open a Command Prompt or PowerShell window.
  2. Run the following command: `setx ELEVENLABS_API_KEY "your_api_key_here"`
  3. Make sure to replace `your_api_key_here` with your actual API key.
  4. Close and reopen the Command Prompt or PowerShell window for the change to take effect.


Once the ELEVENLABS_API_KEY environment variable is set, you can run the program as described in the Usage section below.


# Usage


```
TTS.py [-h] (-a | -s | --get-voices) [-v VOICE_ID]
[-t TEXT | -f FILE | -u URL | --ai | --gear | --business | --culture | --science | --security]
[-m MODEL] [-o OUTPUT]
```


# Arguments

  ```
  -h, --help                            show this help message and exit
  
  -a, --audio                           Use /v1/text-to-speech API endpoint

  -s, --stream                          Use /v1/text-to-speech/{voice_id}/stream API endpoint

  --get-voices                          Retrieve the available voices

  -v VOICE_ID, --voice-id VOICE_ID      Voice ID to use for the conversion
  
  -t TEXT, --text TEXT                  Text to convert to speech

  -f FILE, --file FILE                  Text file to convert to speech
  
  -u URL, --url URL                     BETA: URL of article to convert to speech
        
  --ai                                  Read the latest AI news

  --gear                                Read the latest gear news

  --business                            Read the latest business news

  --culture                             Read the latest culture news

  --science                             Read the latest science news

  --security                            Read the latest security news
  
  -m MODEL, --model MODEL               ElevenLabs model to use

  -o OUTPUT, --output OUTPUT            Output to a .wav file

  ```

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

