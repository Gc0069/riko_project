import os
import sounddevice as sd
import soundfile as sf
import requests
import yaml

with open("character_config.yaml", "r") as f:
    config = yaml.safe_load(f)

DEEPGRAM_API_KEY = config["deepgram_api_key"]
LANGUAGE = config["deepgram_language"]

def record_and_transcribe(output_file="recording.wav", samplerate=44100):
    if os.path.exists(output_file):
        os.remove(output_file)

    print("Press ENTER to start recording...")
    input()
    print("🔴 Recording... Press ENTER to stop")

    recording = sd.rec(int(60 * samplerate), samplerate=samplerate, channels=1, dtype='float64')
    input()
    sd.stop()

    print("⏹️ Saving audio...")
    sf.write(output_file, recording, samplerate)

    print("🎯 Transcribing with Deepgram...")

    with open(output_file, 'rb') as f:
        response = requests.post(
            "https://api.deepgram.com/v1/listen",
            headers={
                "Authorization": f"Token {DEEPGRAM_API_KEY}"
            },
            params={
                "language": LANGUAGE
            },
            data=f
        )

    if response.status_code != 200:
        print("Error from Deepgram:", response.text)
        return ""

    transcription = response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
    print(f"Transcription: {transcription}")
    return transcription.strip()
    
