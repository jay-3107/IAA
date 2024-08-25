import faiss
import numpy as np
import subprocess
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer, TextIteratorStreamer
import textwrap
import threading
import uvicorn
from typing import List, Dict
from threading import Thread

# Initialize FastAPI app
app = FastAPI()

# Initialize models
model_name = "google/flan-t5-large"
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS index
dimension = 384
index = faiss.IndexFlatL2(dimension)
metadata_store: Dict[int, Dict] = {}

# Thread-local storage
thread_local = threading.local()

def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    return textwrap.wrap(text, max_chunk_size, break_long_words=False, replace_whitespace=False)

def fetch_with_curl(url: str) -> str:
    command = [
        'curl', '-L', '-X', 'GET', url,
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Curl failed: {result.stderr}")
    
    return result.stdout

def get_embeddings(texts: List[str]) -> np.ndarray:
    return sentence_model.encode(texts)

def fetch_website_content(url: str) -> List[str]:
    page_content = fetch_with_curl(url)
    soup = BeautifulSoup(page_content, 'html.parser')
    content = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
    
    with open("AboutIAA.txt", "r") as file:
        content2 = file.read()
    
    chunks = chunk_text(content2)
    
    for chunk in chunks:
        embedding = get_embeddings([chunk])[0]
        index.add(np.array([embedding]))
        metadata_store[len(metadata_store)] = {"content": chunk, "url": url}
    
    return chunks

def retrieve_relevant_chunks(query: str, top_k: int = 10) -> List[str]:
    query_embedding = get_embeddings([query])[0]
    distances, indices = index.search(np.array([query_embedding]), top_k)
    results = [metadata_store[idx]['content'] for idx in indices[0]]
    return results

def generate_answer(question: str, context: str, max_length: int = 512):
    input_text = f"question: {question} context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=max_length)
    
    streamer = TextIteratorStreamer(tokenizer)
    
    generation_kwargs = dict(
        inputs=inputs.input_ids,
        max_length=500,
        num_beams=4,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    
    thread = Thread(target=model.generate, kwargs=dict(**generation_kwargs, streamer=streamer))
    thread.start()
    
    for text in streamer:
        yield text

def rag_qa(url: str, question: str):
    if not hasattr(thread_local, 'content_fetched'):
        fetch_website_content(url)
        thread_local.content_fetched = True
    
    relevant_chunks = retrieve_relevant_chunks(question)
    context = ' '.join(relevant_chunks)
    if len(tokenizer.encode(context)) > 512:
        context = tokenizer.decode(tokenizer.encode(context)[:512], skip_special_tokens=True)
    
    for token in generate_answer(question, context):
        yield token

class QuestionRequest(BaseModel):
    url: str
    message: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    if not request.url or not request.message:
        raise HTTPException(status_code=400, detail="Please provide a URL and a question.")
    
    try:
        return StreamingResponse(rag_qa(request.url, request.message), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)