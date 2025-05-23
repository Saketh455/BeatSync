import librosa
import numpy as np
import serial
import time
import requests
import os
from urllib.parse import urlparse

# Initialize serial connection to M5StickC
ser = serial.Serial("COM6", 115200)  # Replace COM6 if needed

# Ask for song input
song_input = input("Enter song file path or URL: ").strip()
time_signature_input = input("Enter time signature (e.g., 3/4, 4/4, 7/8): ")
numerator, denominator = map(int, time_signature_input.split("/"))

# Determine if input is a URL or a file path
if song_input.startswith("http://") or song_input.startswith("https://"):
    print("Downloading audio file from URL...")
    response = requests.get(song_input, stream=True)

    parsed_url = urlparse(song_input)
    filename = os.path.basename(parsed_url.path)
    if not filename.endswith((".mp3", ".wav", ".ogg", ".flac")):
        filename += ".mp3"  # Default to mp3 if extension is missing

    temp_file = f"temp_{filename}"

    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    song_path = temp_file
else:
    song_path = song_input

# Load the song
print("Loading audio...")
audio, sr = librosa.load(song_path)
tempo_arr = librosa.beat.tempo(y=audio, sr=sr)
tempo = float(tempo_arr[0])  # Extract scalar
print(f"Detected BPM: {round(tempo)}")

# Beat timing
beat_interval = 60.0 / tempo  # in seconds

# Beat simulation
beat_count = 0
start_time = time.time()

try:
    while True:
        elapsed = time.time() - start_time

        # Determine beat type
        if beat_count % numerator == 0:
            print(f"[{elapsed:.2f}s] SAM")
            ser.write(b"S")  # Send S for SAM
        elif beat_count % numerator == numerator // 2:
            print(f"[{elapsed:.2f}s] KHALI")
            ser.write(b"K")  # Send K for KHALI
        else:
            print(f"[{elapsed:.2f}s] Beat")
            ser.write(b"B")  # Send B for normal beat

        beat_count += 1
        time.sleep(beat_interval)

except KeyboardInterrupt:
    print("\nStopped.")
    ser.close()
    if "temp_file" in locals() and os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"Deleted temporary file: {temp_file}")
