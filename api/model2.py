import faiss   #used to search for embeddings
import numpy as np #used to store embeddings
import subprocess #used to run curl command
from bs4 import BeautifulSoup #used to parse html content
from flask import Flask, request, jsonify #used to create API
from uuid import uuid4 #used to generate unique ids
from sentence_transformers import SentenceTransformer #used to encode text
from transformers import T5ForConditionalGeneration, T5Tokenizer #used to generate answers
import textwrap #used to chunk text
import re  #used for data cleaning

# Initialize Flask app
app = Flask(__name__)

# Initialize models
model_name = "google/flan-t5-large" 
tokenizer = T5Tokenizer.from_pretrained(model_name,legacy=False) #Used to tokenize text(for t5 model)
model = T5ForConditionalGeneration.from_pretrained(model_name) #Used to generate answers
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')   #a machine learning model that transformes sentences to dense vector representations

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
    #content = soup.get_text(separator='\n', strip=True)  
    
    #data cleaning
    #content = content.lower()
    #content = re.sub(r'\s+', ' ', content) #remove extra whitespace
    
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
    # Fetch website content
    fetch_website_content(url)
    
    # Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(question)
    
    # Concatenate relevant chunks and ensure it fits the model's max length
    context = ' '.join(relevant_chunks)
    if len(tokenizer.encode(context)) > 512:
        context = tokenizer.decode(tokenizer.encode(context)[:512], skip_special_tokens=True)
    
    # Generate the answer
    answer = generate_answer(question, context)
    
    return answer


# Flask route for answering questions
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    url = data.get("url")
    question = data.get("message")
    print(f"Question:{question}, URL:{url}")
    
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
