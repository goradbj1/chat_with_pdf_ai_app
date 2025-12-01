import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "vector_db/faiss_index.bin"
DOC_PATH = "vector_db/documents.pkl"

index = None
documents = []
dimension = 384  # embedding size


def save_index():
    if index is None:
        return

    faiss.write_index(index, INDEX_PATH)

    with open(DOC_PATH, "wb") as f:
        pickle.dump(documents, f)

    print("Saved FAISS index & documents to disk.")


def load_index():
    global index, documents

    if os.path.exists(INDEX_PATH) and os.path.exists(DOC_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(DOC_PATH, "rb") as f:
            documents = pickle.load(f)
        print("Loaded persistent vector DB.")
        return True

    print("No existing FAISS index found.")
    return False


def build_vector_store(chunks):
    global index, documents

    embeddings = model.encode(chunks).astype("float32")

    if index is None:
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        documents = chunks
    else:
        index.add(embeddings)
        documents.extend(chunks)

    save_index()

def search(query, k=3):
    """Search the FAISS index and return top matched text chunks"""
    global index, documents

    if index is None:
        raise ValueError("FAISS index not loaded. Did you run create_embeddings.py?")

    q_emb = model.encode([query]).astype("float32")

    distances, indices = index.search(q_emb, k)

    results = []
    for idx in indices[0]:
        results.append(documents[idx])

    return results