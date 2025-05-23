import librosa
import numpy as np
import serial
import time

# Initialize serial connection to M5StickC
ser = serial.Serial("COM6", 115200)  # Replace COM6 if needed

# Ask for song path
song_path = input("Enter song file path (e.g., song.mp3): ")
time_signature_input = input("Enter time signature (e.g., 3/4, 4/4, 7/8): ")

numerator, denominator = map(int, time_signature_input.split("/"))

# Load the song
audio, sr = librosa.load(song_path)
tempo_arr = librosa.beat.tempo(y=audio, sr=sr)
tempo = float(tempo_arr[0])  # extract scalar
print(f"Detected BPM: {round(tempo)}")

# Beat timing
beat_interval = 60.0 / tempo  # in seconds

# For simulation: start marking beats
beat_count = 0
start_time = time.time()

try:
    while True:
        elapsed = time.time() - start_time

        # Determine Sam / Khali
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
