import time
import keyboard 
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "Pointboat" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

#inserisci qua come vuoi che ti risponda
FIRST_SYSTEM_MESSAGE = {"role": "system", "content":
    "Sei Giovanni Battista Turchi, un professore all' ITT Enea Mattei di Sondrio, Insegni le materie di Sistemi e Reti e TPSIT, hai scritto vari libri tra cui Reti da Pesca (tratta di sistemi e reti). Vuoi che i tuoi  studenti imparino e migliorino, guida una alfa romeo giulia, suoni la chitarra e fai il pane"
    }
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)



    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    print("[green]\n!!!!!!!\nFINITO DIALOGO.\nPRONTO PER IL PROSSIMO\n!!!!!!!\n")
    
