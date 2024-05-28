from elevenlabs import generate, stream, set_api_key, voices, play, save
import time
import os

# Imposta direttamente la chiave API qui
api_key = '56bbb95057d4bb83109c76a8ba166d05'
set_api_key(api_key)

class ElevenLabsManager:

    def __init__(self):
        # CALLING voices() IS NECESSARY TO INSTANTIATE 11LABS FOR SOME REASON
        self.all_voices = voices()
        print(f"\nAll ElevenLabs voices: \n{self.all_voices}\n")

    # Convert text to speech, then save it to file. Returns the file path
    def text_to_audio(self, input_text, voice, save_as_wave=True, subdirectory=""):
        if voice not in [v.name for v in self.all_voices]:
            raise ValueError(f"Voice '{voice}' not found. Available voices: {[v.name for v in self.all_voices]}")
        
        audio_saved = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v2"
        )
        if save_as_wave:
          file_name = f"___Msg{str(hash(input_text))}.wav"
        else:
          file_name = f"___Msg{str(hash(input_text))}.mp3"
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_saved, tts_file)
        return tts_file

    # Convert text to speech, then play it out loud
    def text_to_audio_played(self, input_text, voice):
        if voice not in [v.name for v in self.all_voices]:
            raise ValueError(f"Voice '{voice}' not found. Available voices: {[v.name for v in self.all_voices]}")
        
        audio = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v2"
        )
        play(audio)

    # Convert text to speech, then stream it out loud (don't need to wait for full speech to finish)
    def text_to_audio_streamed(self, input_text, voice):
        if voice not in [v.name for v in self.all_voices]:
            raise ValueError(f"Voice '{voice}' not found. Available voices: {[v.name for v in self.all_voices]}")
        
        audio_stream = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v2",
          stream=True
        )
        stream(audio_stream)
