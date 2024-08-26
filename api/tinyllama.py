import faiss
import numpy as np
import subprocess
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import textwrap
import re
import torch

# Initialize Flask app
app = Flask(__name__)

# Initialize models
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')  # Updated to use all-MiniLM-L6-v2

# FAISS index
dimension = 384  # Dimension of embeddings for all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)  # L2 distance
metadata_store = {}  # Dictionary to store metadata

# Helper functions
def chunk_text(text, max_chunk_size=1000):
    return textwrap.wrap(text, max_chunk_size, break_long_words=False, replace_whitespace=False)


def fetch_with_curl(url):
    command = [
        'curl', '-L', '-X', 'GET', url,
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Curl failed: {result.stderr}")
    
    return result.stdout


def get_embeddings(texts):
    return sentence_model.encode(texts)


def fetch_website_content(url):
    page_content = fetch_with_curl(url)  # Use curl to fetch content
    soup = BeautifulSoup(page_content, 'html.parser')
    content = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
    
    chunks = chunk_text(content)
    
    # Upsert data to FAISS
    for chunk in chunks:
        embedding = get_embeddings([chunk])[0]
        index.add(np.array([embedding]))
        metadata_store[len(metadata_store)] = {"content": chunk, "url": url}
    
    return chunks


def retrieve_relevant_chunks(query, top_k=10):
    query_embedding = get_embeddings([query])[0]
    distances, indices = index.search(np.array([query_embedding]), top_k)
    results = [metadata_store[idx]['content'] for idx in indices[0]]
    return results


def generate_answer(question, context, max_length=512):
    # Use chat template for conversation
    messages = [{context}]
    
    # Format the conversation with the chat template
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Generate the answer using TinyLlama
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    return outputs[0]["generated_text"]


def rag_qa(url, question):
    # Fetch website content
    fetch_website_content(url)
    
    # Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(question)
    
    # Concatenate relevant chunks and ensure it fits the model's max length
    context = ' '.join(relevant_chunks)
    if len(pipe.tokenizer.encode(context)) > 512:
        context = pipe.tokenizer.decode(pipe.tokenizer.encode(context)[:512], skip_special_tokens=True)
    
    # Generate the answer
    answer = generate_answer(question, context)
    
    return answer


# Flask route for answering questions
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    url = data.get("url")
    #url = "https://en.wikipedia.org/wiki/Airports_Authority_of_India"
    question = data.get("message")
    print("Question: ", question)
    
    if not url or not question:
        return jsonify({"error": "Please provide a question."}), 400
    
    try:
        answer = rag_qa(url, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)
