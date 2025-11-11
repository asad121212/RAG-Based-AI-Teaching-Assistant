import json
import sys
import math
import os

def merge_json_chunks(input_json_path, output_json_path, n=5):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data["chunks"]
    merged = []
    total = len(chunks)
    groups = math.ceil(total / n)

    for i in range(groups):
        start = i * n
        end = min((i + 1) * n, total)

        group = chunks[start:end]

        merged.append({
            "number": group[0]["number"],
            "title": group[0]["title"],
            "start": group[0]["start"],
            "end": group[-1]["end"],
            "text": " ".join([c["text"] for c in group])
        })

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({"chunks": merged, "text": data["text"]}, f, indent=4)

    print("Merged JSON saved:", output_json_path)

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    merge_json_chunks(input_path, output_path)
