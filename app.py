import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Now genai will pick up the API key automatically from the environment

# Load your Chroma DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_uchicago_ads", embedding_function=embedding_model)  

# Initialize Gemini model once
model = genai.GenerativeModel("models/gemini-2.5-pro")

def RAG_pipeline_gemini(query, db, k=5):
    retriever = db.as_retriever(search_kwargs={"k": k})
    retrieved_docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    rag_prompt = f"""You are a helpful assistant. Use the following context to answer the question.

[CONTEXT]
{context}

[QUESTION]
{query}

Answer:"""

    response = model.generate_content(rag_prompt)

    sources = [doc.metadata.get('source', 'No source available') for doc in retrieved_docs]

    return response.text, sources

# Streamlit UI
st.title("UChicago ADS RAG Chatbot with Gemini")

if 'history' not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question about UChicago ADS:")

if st.button("Send") and query:
    with st.spinner("Generating answer..."):
        answer, sources = RAG_pipeline_gemini(query, db)
        st.session_state.history.append((query, answer, sources))

if st.session_state.history:
    for i, (q, a, s) in enumerate(reversed(st.session_state.history)):
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {a}")
        st.markdown(f"**Sources:**")
        for src in s:
            st.markdown(f"- {src}")
        st.markdown("---")
