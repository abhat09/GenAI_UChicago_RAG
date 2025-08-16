from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Chroma DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_uchicago_ads", embedding_function=embedding_model)  

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.5-pro")

def RAG_pipeline_gemini(query, db, k=5):
    retriever = db.as_retriever(search_kwargs={"k": k})
    retrieved_docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    rag_prompt = f"""You are a helpful assistant. Use the following context to answer the question. Get rid of markdown stylings.

[CONTEXT]
{context}

[QUESTION]
{query}

Answer:"""

    response = model.generate_content(rag_prompt)
    sources = [doc.metadata.get('source', 'No source available') for doc in retrieved_docs]
    return response.text, sources

app = Flask(__name__)

# Configure CORS properly
CORS(app, origins=["http://localhost:3000", "http://192.168.1.158:3000", "http://127.0.0.1:3000"])

@app.route('/api/chat', methods=['OPTIONS'])
@cross_origin()
def chat_options():
    response = jsonify({'status': 'ok'})
    return response

@app.route('/api/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        print(f"Received request from: {request.origin}")
        print(f"Request headers: {dict(request.headers)}")
        
        data = request.get_json()
        user_message = data.get('message', '')
        
        print(f"User message: {user_message}")
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from RAG pipeline
        response, sources = RAG_pipeline_gemini(user_message, db)
        
        print(f"Generated response: {response[:100]}...")
        
        response = jsonify({
            'response': response,
            'sources': sources
        })
        
        return response
        
    except Exception as e:
        print(f"Error: {str(e)}")
        error_response = jsonify({'error': 'Internal server error'}), 500
        return error_response

@app.route('/api/health', methods=['GET'])
@cross_origin()
def health_check():
    response = jsonify({'status': 'healthy'})
    return response

if __name__ == '__main__':
    print("Starting UChicago ADS Chat API...")
    print("Make sure your React app is running on http://localhost:3000")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, port=5000) 