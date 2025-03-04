import os
import faiss
import numpy as np
from pathlib import Path
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("MISTRAIL_API_KEY")
CHUNK_SIZE = 2048
INDEX_FILE_PATH = "app/models/faiss_index.index"
CV_FILE_PATH = "app/models/cv.txt"
EMBEDDINGS_MODEL = "mistral-embed"
LLM_MODEL = "ministral-3b-latest"

client = Mistral(API_KEY=API_KEY)

text = open(CV_FILE_PATH, "r").read()
chunks = [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


def get_text_embedding(input):
    embeddings_batch_response = client.embeddings.create(
        model=EMBEDDINGS_MODEL, inputs=input
    )
    return embeddings_batch_response.data[0].embedding


if Path.exists(INDEX_FILE_PATH):
    index = faiss.read_index(INDEX_FILE_PATH)
else:
    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])
    d = text_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(text_embeddings)
    faiss.write_index(index, INDEX_FILE_PATH)

question = "Quel âge a Pascal ?"
question_embeddings = np.array([get_text_embedding(question)])

D, I = index.search(question_embeddings, k=2)
retrieved_chunk = [chunks[i] for i in I.tolist()[0]]

prompt = f"""
Context information is below.
---------------------
{retrieved_chunk}
---------------------
Given the context information and not prior knowledge, answer the query. Do not answer any other questions not related to the given information context.
Query: {question}
Answer:
"""


def run_mistral(user_message, model=LLM_MODEL):
    messages = [{"role": "user", "content": user_message}]
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
        temperature=0,
    )
    return chat_response.choices[0].message.content


print(run_mistral(prompt))
