import requests
import json
import yaml
import os

with open('character_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

API_KEY = config['CHUTES_API_KEY']
MODEL = config['CHUTES_MODEL']
HISTORY_FILE = config['history_file']

SYSTEM_PROMPT = [
    {
        "role": "system",
        "content": config['presets']['default']['system_prompt']
    }
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return SYSTEM_PROMPT

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_riko_response(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 1.0
    }

    response = requests.post(
        "https://chroma.chutes.ai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print("Error from Chutes:", response.text)
        return "Sorry senpai, I couldn't think of anything!"

    return response.json()["choices"][0]["message"]["content"]

def llm_response(user_input):
    messages = load_history()

    messages.append({
        "role": "user",
        "content": user_input
    })

    reply = get_riko_response(messages)

    messages.append({
        "role": "assistant",
        "content": reply
    })

    save_history(messages)
    return reply
    
