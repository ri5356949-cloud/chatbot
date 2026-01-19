import os
import pickle
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv()
client = OpenAI()

DATA_PATH = Path("data/docs")


def load_docs():
    texts = []

    for file in DATA_PATH.iterdir():
        # TXT files
        if file.suffix.lower() == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                texts.append(f.read())

    return texts


def create_index():
    texts = load_docs()   # ✅ THIS WAS MISSING

    if not texts:
        raise ValueError("No documents found in data/docs")

    documents = []
    embeddings = []

    for text in texts:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        emb = np.array(response.data[0].embedding)

        documents.append(text)
        embeddings.append(emb)

    with open("data/store.pkl", "wb") as f:
        pickle.dump((documents, embeddings), f)

    print("Index created successfully (without FAISS)")


if __name__ == "__main__":
    print("DATA_PATH =", DATA_PATH)
    print("Exists =", DATA_PATH.exists())
    create_index()