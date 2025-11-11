import whisper
import json
import sys
import os

model = whisper.load_model("large-v2")

def mp3_to_json(mp3_path, json_output_path):
    print("Transcribing:", mp3_path)

    filename = os.path.basename(mp3_path)
    parts = filename.split("_")

    number = parts[0] if len(parts) > 1 else "0"
    title = parts[1].replace(".mp3", "") if len(parts) > 1 else filename

    result = model.transcribe(
        audio=mp3_path,
        language="hi",
        task="translate",
        word_timestamps=False
    )

    chunks = []
    for seg in result["segments"]:
        chunks.append({
            "number": number,
            "title": title,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })

    output = {
        "chunks": chunks,
        "text": result["text"]
    }

    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("JSON written:", json_output_path)

if __name__ == "__main__":
    mp3_path = sys.argv[1]
    json_output_path = sys.argv[2]
    mp3_to_json(mp3_path, json_output_path)
