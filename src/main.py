from flask import Flask, request, jsonify
import librosa
import numpy as np
import serial
import time
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/upload", methods=["POST"])
def upload_song():
    file = request.files["file"]
    time_signature = request.form.get("time_signature", "4/4")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Begin beat detection logic
    try:
        numerator, denominator = map(int, time_signature.split("/"))

        print(f"Processing file: {file_path}")
        audio, sr = librosa.load(file_path)
        tempo_arr = librosa.beat.tempo(y=audio, sr=sr)
        tempo = float(tempo_arr[0])
        print(f"Detected BPM: {round(tempo)}")

        # Start serial communication
        try:
            ser = serial.Serial("COM6", 115200)
        except Exception as e:
            return jsonify({"error": f"Could not open COM6: {str(e)}"}), 500

        beat_interval = 60.0 / tempo
        beat_count = 0
        start_time = time.time()

        print("Starting beat signal loop. Press Ctrl+C to stop.")
        while True:
            elapsed = time.time() - start_time
            if beat_count % numerator == 0:
                print(f"[{elapsed:.2f}s] SAM")
                ser.write(b"S")
            elif beat_count % numerator == numerator // 2:
                print(f"[{elapsed:.2f}s] KHALI")
                ser.write(b"K")
            else:
                print(f"[{elapsed:.2f}s] Beat")
                ser.write(b"B")

            beat_count += 1
            time.sleep(beat_interval)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Beat detection started"}), 200


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
