import sys
import json
import joblib
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

def embed_text(text):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": [text]
    })
    return r.json()["embeddings"][0]

def run_chat(query, embeddings_path):

    df = joblib.load(embeddings_path)

    query_embedding = embed_text(query)

    similarities = cosine_similarity(
        np.vstack(df["embedding"]), 
        [query_embedding]
    ).flatten()

    top_k = 5
    idxs = similarities.argsort()[::-1][:top_k]
    top_df = df.iloc[idxs]

    chunks = []
    for _, row in top_df.iterrows():
        chunks.append({
            "title": row["title"],
            "start": row["start"],
            "end": row["end"],
            "text": row["text"]
        })

    return json.dumps({"chunks": chunks})

if __name__ == "__main__":
    query = sys.argv[1]
    embeddings = sys.argv[2]
    print(run_chat(query, embeddings))
