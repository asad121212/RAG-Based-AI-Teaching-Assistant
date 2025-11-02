import requests
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


def inference(prompt):
    r=requests.post("http://localhost:11434/api/generate",json={
            # "model":"deepseek-r1",
            "model":"llama3.2",
            "prompt":prompt,
            "stream": False
    })

    response=r.json()
    return response


df=joblib.load("embeddings.joblib")
incoming_query=input("Enter your query: ")
query_embedding=create_embedding([incoming_query])[0]

#find the most similar chunk from existing embeddings
similarities=cosine_similarity(np.vstack(df['embedding']),[query_embedding]).flatten()
# print(similarities)

top_result=30
max_idx=similarities.argsort()[::-1][0:top_result]
# print("max idx:",max_idx)

new_df=df.loc[max_idx]

# print(new_df[['number','title','text']])

prompt=f'''
I am teaching web development using django framework. Here are the video subtitle chunk containing video title, video number, start time, end time and text at that time:

{new_df[['title','number','start','end','text']].to_json(orient='records')}

--------------------------------------------------------------------

{incoming_query}
User asked this question related to the above video chunks, you have to answer in a human way (dont mention the above format its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, politely say that you are designed to answer only web development using django framework related questions.
'''

# for index,item in new_df.iterrows():
#     print(f"Number: {item['number']}, Text : {item['text']}, Title: {item['title']}, index: {index}, start: {item['start']}, end: {item['end']}")

with open("prompt.txt","w") as f:
    f.write(prompt)

print("Thinking...")
response=inference(prompt)
print("Response:",response['response'])

with open("response.txt","w") as f:
    f.write(response['response'])
