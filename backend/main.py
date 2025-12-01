from datetime import datetime
from fastapi import FastAPI
from scripts.vector_store import load_index, search
from scripts.groq_client import groq_llm
from scripts.db import conversations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading FAISS index...")
load_index()

@app.post("/ask")
async def ask(payload: dict):
    query = payload["query"]

    context_chunks = search(query)
    context = "\n\n".join(context_chunks)

    prompt = f"""
        Use the context below to answer accurately.

        Context:
        {context}

        Question: {query}
        Answer:
        """

    answer = groq_llm(prompt)

    conversations.insert_one({"query": query, "answer": answer, "date_time": datetime.now()})
    return {"response": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port = 8000)