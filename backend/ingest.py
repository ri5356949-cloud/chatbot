from pathlib import Path
import os
import faiss
import pickle
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "docs"
INDEX_PATH = BASE_DIR / "data" / "index.faiss"
STORE_PATH = BASE_DIR / "data" / "store.pkl"

print("DATA_PATH =", DATA_PATH)
print("Exists =", DATA_PATH.exists())

load_dotenv(BASE_DIR / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_docs():
    texts = []
    for file in DATA_PATH.iterdir():
        if file.suffix == ".pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
    return texts

def load_docs():
    texts = []

    for file in DATA_PATH.iterdir():

        # PDF files
        if file.suffix.lower() == ".pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)

        # TXT files
        elif file.suffix.lower() == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                texts.append(f.read())

    return texts


def create_index():
    texts = load_docs()
    if not texts:
        raise ValueError("No text found in PDFs")

    embeddings = []
    for text in texts:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding
        embeddings.append(emb)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings).astype("float32"))

    with open(STORE_PATH, "wb") as f:
        pickle.dump(texts, f)

    faiss.write_index(index, str(INDEX_PATH))

if __name__ == "__main__":
    create_index()

print("Index created successfully")

