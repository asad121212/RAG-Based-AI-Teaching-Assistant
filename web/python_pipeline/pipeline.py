import sys
import os
from video_to_mp3 import convert_video_to_mp3
from mp3_to_json import mp3_to_json
from merge_chunks import merge_json_chunks
from embed_json import embed_json



def run_pipeline(video_path, output_dir):
    # ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(video_path))[0]

    mp3_path = os.path.join(output_dir, base + ".mp3")
    json_path = os.path.join(output_dir, base + ".json")
    merged_path = os.path.join(output_dir, base + "_merged.json")
    pickle_path = os.path.join(output_dir, base + "_embeddings.pkl")

    print("Step 1: Video to MP3")
    convert_video_to_mp3(video_path, mp3_path)

    print("Step 2: MP3 to JSON")
    mp3_to_json(mp3_path, json_path)

    print("Step 3: Merge Chunks")
    merge_json_chunks(json_path, merged_path)

    print("Step 4: Embeddings to pickle")
    embed_json(merged_path, pickle_path)

    print("Pipeline complete.")
    print("MP3:", mp3_path)
    print("JSON:", json_path)
    print("MERGED:", merged_path)
    print("EMBEDDINGS:", pickle_path)

    return pickle_path

if __name__ == "__main__":
    video = sys.argv[1]
    out = sys.argv[2]
    run_pipeline(video, out)
