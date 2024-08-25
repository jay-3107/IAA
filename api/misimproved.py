import faiss
import numpy as np
import subprocess
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
import textwrap
import re 
import requests
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize models
model_name = "google/flan-t5-large"
tokenizer = T5Tokenizer.from_pretrained(model_name,legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name)
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')  # Updated to use all-MiniLM-L6-v2

# FAISS index
dimension = 384  # Dimension of embeddings for all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)  # L2 distance
metadata_store = {}  # Dictionary to store metadata

# Personality responses
greetings = ["Hi there!", "Hello!", "Hey!", "Good to see you!", "Nice to meet you!"]
farewells = ["Goodbye!", "See you later!", "Take care!", "See you soon!", "Bye now!"]
polite_responses = ["Please", "Thank you", "You're welcome", "Sure thing", "Absolutely"]

# Helper functions
def chunk_text(text, max_chunk_size=1000):
    return textwrap.wrap(text, max_chunk_size, break_long_words=False, replace_whitespace=False)

def fetch_with_curl(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        print(f"Error fetching URL: {url} - {str(e)}")
        return None

def get_embeddings(texts):
    return sentence_model.encode(texts)

def fetch_website_content(url):
    page_content = fetch_with_curl(url)  # Use curl to fetch content
    if not page_content:
        return None
    soup = BeautifulSoup(page_content, 'html.parser')
    content = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
    #content = soup.get_text(separator='\n', strip=True)  
    
    #data cleaning
    content = content.lower()
    content = re.sub(r'\s+', ' ', content) #remove extra whitespace
    
    # Save content to file
    # filename = "file1.txt"
    # with open(filename, "w", encoding="utf-8") as file:
    #     file.write(content)
    #     file.close()
    # print(f"Content saved to {filename}")
    
    with open("AboutIAA.txt", "r") as file:
        content2 = file.read()
    
    #Chunk the content
    chunks = chunk_text(content2)
    
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
    input_text = f"question: {question} context: {context}"
    input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=max_length).input_ids
    outputs = model.generate(input_ids, max_length=500)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def rag_qa(url, question):
#Fetch website content
    if url and url != '':
        content = fetch_website_content(url)
    else:
        content = None
    # Retrieve relevant chunks
    if content:
        relevant_chunks = retrieve_relevant_chunks(question)
    else:
        relevant_chunks = []

    # Concatenate relevant chunks and ensure it fits the model's max length
    context = ' '.join(relevant_chunks)
    if len(tokenizer.encode(context)) > 512:
        context = tokenizer.decode(tokenizer.encode(context)[:512], skip_special_tokens=True)

    # Generate the answer
    answer = generate_answer(question, context)

    # Add personality to the response
    if answer and re.search(r'^[a-zA-Z].*[a-zA-Z]$', question):
        if question.lower() in ['hi', 'hello', 'how are you']:
            answer = np.random.choice(greetings) + ' ' + answer
        elif question.lower() in ['bye', 'goodbye', 'see you later']:
            answer = np.random.choice(farewells) + ' ' + answer
        elif any(polite_phrase in question.lower() for polite_phrase in polite_responses):
            answer = answer + ' ' + np.random.choice(polite_responses)

    return answer

def is_command(question):
    command_keywords = ['hi', 'hello', 'how are you', 'bye', 'goodbye', 'see you later', 'thank you', 'thanks']
    for keyword in command_keywords:
        if keyword in question.lower():
            return True
    
    return False

#Flask route for answering questions
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    #url = data.get("url")
    url = "https://en.wikipedia.org/wiki/Airports_Authority_of_India"
    question = data.get("message")
    print(f"Question:{question}, URL:{url}")
    
    if not question:
        return jsonify({"error": "Please provide a question."}), 400

    # Handle command questions
    if is_command(question):
        if 'thank' in question.lower():
            return jsonify({"answer": np.random.choice(polite_responses)})
        else:
            return jsonify({"answer": np.random.choice(greetings)})

    # Handle non-command questions
    try:
        answer = rag_qa(url, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)