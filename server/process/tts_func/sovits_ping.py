import requests
import soundfile as sf
import sounddevice as sd
import yaml

with open('character_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

API_KEY = config['elevenlabs_api_key']
VOICE_ID = config['elevenlabs_voice_id']
MODEL_ID = config['elevenlabs_model_id']
SETTINGS = config['elevenlabs_settings']

def play_audio(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()

def elevenlabs_gen(text, output_path="output.wav"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": SETTINGS["stability"],
            "similarity_boost": SETTINGS["similarity_boost"],
            "style": SETTINGS["style"],
            "use_speaker_boost": SETTINGS["use_speaker_boost"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("Error from ElevenLabs:", response.text)
        return None

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
    
