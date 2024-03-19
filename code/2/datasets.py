import os
import soundfile
import librosa
import glob
import tqdm
import numpy as np



from demucs.separate import demucs_separator

# Function to extract vocals from audio files
def extract_vocals(songs_path, vocals_path):
    ctr = 0 
    model = "mdx_extra_q"
    for audio_file in tqdm.tqdm(os.listdir(songs_path)):
        separator = demucs_separator(model)
        audio_path = os.path.join(songs_path, audio_file)
        estimates = separator.separate(audio_path)
        vocals = estimates['vocals']
        vocal_name = f"vocal_{ctr}.wav"
        song_name = os.path.splitext(audio_file)[0]
        vocals.write(os.path.join(vocals_path, vocal_name))
        ctr += 1

# Function to split audio files at silences and remove silence
class Slicer:
    def __init__(self,
                 sr: int,
                 threshold: float = -40.,
                 min_length: int = 5000,
                 min_interval: int = 300,
                 hop_size: int = 20,
                 max_sil_kept: int = 5000):
        # Constructor code...

    def _apply_slice(self, waveform, begin, end):
        # Method code...

    def slice(self, waveform):
        # Method code...

def remove_silence_and_split(vocals_path, non_silence_audio):
    if not os.path.exists(non_silence_audio):
        os.makedirs(non_silence_audio)

    for audio_path in os.listdir(vocals_path):
        # Extract vocals from audio
        audio_path = os.path.join(vocals_path, audio_path)
        if len(os.path.basename(audio_path).split(".")) == 1: 
            continue
        audio_name = os.path.basename(audio_path).split(".")[0]
        audio, sr = librosa.load(audio_path, sr=None, mono=False) 
        slicer = Slicer(
            sr=sr,
            threshold=-25,
            min_length=7000,
            min_interval=600,
            hop_size=15,
            max_sil_kept=700
        )
        chunks = slicer.slice(audio)
        for i, chunk in enumerate(chunks):
            if len(chunk.shape) > 1:
                chunk = chunk.T  # Swap axes if the audio is stereo.
            soundfile.write(os.path.join(non_silence_audio,f'{audio_name}_{i}.wav'), chunk, sr)  

def split_audio_into_clips(non_silence_audio, min_length=6):
    sliced_dir = "/content/drive/MyDrive/sliced/"
    if not os.path.exists(sliced_dir):
        os.makedirs(sliced_dir)

    print(f"Slicing audios to clips of {min_length} seconds")
    cnt = 0
    for file in tqdm(os.listdir(non_silence_audio)):
        if file.endswith('.wav'):        
            audio_name = file.split('.')[0]
            audio_path = os.path.join(non_silence_audio, file)
            audio, sr = librosa.load(audio_path)

            min_samples = int(min_length * sr)

            segments = []
            segment_start = 0
            while segment_start + min_samples < len(audio):
                segment_end = segment_start + min_samples
                segments.append(audio[segment_start:segment_end])
                segment_start = segment_end

            for i, segment in enumerate(segments):
                segment_path = os.path.join(sliced_dir,f'segments_{audio_name}_{cnt}.wav')
                cnt += 1
                soundfile.write(segment_path, segment, sr)

# Set paths
songs_path = "/content/drive/MyDrive/songs"
vocals_path = "/content/drive/MyDrive/vocals"
non_silence_audio = "/content/drive/MyDrive/non_silenced/"

# Extract vocals
extract_vocals(songs_path, vocals_path)

# Remove silence and split audio
remove_silence_and_split(vocals_path, non_silence_audio)

# Split audio into clips
split_audio_into_clips(non_silence_audio, min_length=6)
