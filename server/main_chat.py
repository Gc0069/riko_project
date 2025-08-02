from pathlib import Path
import time
import uuid
import os

from process.asr_func.asr_push_to_talk import record_and_transcribe
from process.llm_funcs.llm_scr import llm_response
from process.tts_func.elevenlabs_tts import elevenlabs_gen, play_audio

print('\n========= Starting Chat... ================\n')

while True:
    audio_dir = Path("audio")
    audio_dir.mkdir(parents=True, exist_ok=True)

    output_wav_path = audio_dir / "conversation.wav"

    user_text = record_and_transcribe(output_wav_path)

    llm_reply = llm_response(user_text)

    uid = uuid.uuid4().hex
    response_path = audio_dir / f"output_{uid}.wav"

    tts_path = elevenlabs_gen(llm_reply, response_path)

    if tts_path:
        play_audio(tts_path)

    # Clean up
    for f in audio_dir.glob("*.wav"):
        f.unlink()
        
