import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
            "model":"bge-m3",
            "input":text_list
    })

    embedding=r.json()['embeddings']
    return embedding

jsons=os.listdir("merged_jsons")
all_chunks=[]
chunk_id=0
for json_file in jsons:
    with open(f"merged_jsons/{json_file}","r") as f:
        content=json.load(f)
    print(f"Processing {json_file} for embeddings...")
    embeddings=create_embedding([chunk['text'] for chunk in content['chunks']])   

    for i,chunk in enumerate(content['chunks']):
        chunk['embedding']=embeddings[i]
        chunk['chunk_id']=chunk_id
        chunk_id+=1
        all_chunks.append(chunk)
        

df=pd.DataFrame.from_records(all_chunks)
# Save dataframe with embeddings for future use
joblib.dump(df,"embeddings.joblib")


