from flask import Flask, request, jsonify
import pinecone
from uuid import uuid4
import requests
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer
import textwrap

# Initialize Flask app
app = Flask(__name__)

# Pinecone setup (as provided by you)
pinecone_client = pinecone.Pinecone(
    api_key="d3010d8c-2b72-4117-ae08-69596bcf7997",
    environment="us-east-1"
)
index_name = "rag-chatbot"

# Connect to the index
index = pinecone_client.Index(index_name)

# Initialize models
model_name = "google/flan-t5-large"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
sentence_model = SentenceTransformer('all-mpnet-base-v2')

# Helper functions
def chunk_text(text, max_chunk_size=1000):
    return textwrap.wrap(text, max_chunk_size, break_long_words=False, replace_whitespace=False)


#trying some things as iaa website is giving me a 403 error(anti bot mechanism)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
def fetch_website_content(url):
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    #content = ' '.join([p.get_text() for p in soup.find_all('p')])
    content = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
    chunks = chunk_text(content)
    
    # Upsert data to Pinecone
    batch_size = 500
    to_upsert = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        embeddings = get_embeddings(batch)
        to_upsert.extend([(str(uuid4()), embedding.tolist(), {"content": chunk, "url": url})
                          for embedding, chunk in zip(embeddings, batch)])
    index.upsert(vectors=to_upsert)
    
    return chunks

def get_embeddings(texts):
    return sentence_model.encode(texts)

def retrieve_relevant_chunks(query, url, top_k=10):
    query_embedding = get_embeddings([query])[0]
    results = index.query(
        vector=query_embedding.tolist(),
        filter={"url": url},
        top_k=top_k,
        include_metadata=True
    )
    return [match.metadata['content'] for match in results.matches]

def generate_answer(question, context, max_length=512):
    input_text = f"question: {question} context: {context}"
    input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=max_length).input_ids
    outputs = model.generate(input_ids, max_length=500)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def rag_qa(url, question):
    # Fetch website content
    fetch_website_content(url)
    
    # Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(question, url)
    
    # Concatenate relevant chunks and ensure it fits the model's max length
    context = ' '.join(relevant_chunks)
    # If context is too long, truncate it
    if len(tokenizer.encode(context)) > 512:
        context = tokenizer.decode(tokenizer.encode(context)[:512], skip_special_tokens=True)
    
    # Generate the answer
    answer = generate_answer(question, context)
    
    return answer

# Flask route for answering questions
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    url = "https://www.iaa.edu.in/home"
    question = data.get("message")
    
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
