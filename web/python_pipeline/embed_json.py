import requests
import json
import sys
import pandas as pd
import numpy as np

def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={"model": "bge-m3", "input": text_list}
    )
    return r.json()["embeddings"]

def embed_json(input_json_path, output_pickle_path):
    with open(input_json_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    texts = [chunk["text"] for chunk in content["chunks"]]
    print("Generating embeddings for", len(texts), "chunks...")

    embeddings = create_embedding(texts)

    # attach embeddings
    for i, chunk in enumerate(content["chunks"]):
        chunk["embedding"] = embeddings[i]
        chunk["chunk_id"] = i

    df = pd.DataFrame.from_records(content["chunks"])

    # Save to joblib
    import joblib
    joblib.dump(df, output_pickle_path)

    print("Embeddings saved to", output_pickle_path)

if __name__ == "__main__":
    input_json = sys.argv[1]
    output_pickle = sys.argv[2]
    embed_json(input_json, output_pickle)
