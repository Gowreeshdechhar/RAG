# app.py
import streamlit as st
import arxiv
import wikipedia
import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from urllib.parse import urlparse, parse_qs

from rag_utils import (
    get_wikipedia_content,
    get_arxiv_content,
    get_news_article,
    get_youtube_transcript,
    search_web,
    extract_text_from_pdf,
    build_faiss_index,
    retrieve_relevant_chunks,
    generate_response,
    summarize_text
)

st.set_page_config(page_title="SynthRAG Chat", layout="wide")
st.title("🤖 SynthRAG - ChatGPT-like Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

@st.cache_resource
def load_models():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    generator = pipeline("text-generation", model="gpt2", max_length=300)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return embedder, generator, summarizer

embedder, rag_model, summarizer = load_models()

source = st.sidebar.selectbox("Choose a source", [
    "Wikipedia", "arXiv", "PDF Upload", "News Article", "YouTube Video", "Web Search"])

# Handle PDF upload
if source == "PDF Upload":
    uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        pdf_chunks = [pdf_text[i:i+1000] for i in range(0, len(pdf_text), 1000)]
        pdf_index, pdf_embeddings = build_faiss_index(pdf_chunks, embedder)
    else:
        pdf_chunks = []
        pdf_index = None
else:
    uploaded_pdf = None

# Chat input
user_input = st.chat_input("Ask something...")

if user_input is not None and user_input.strip() != "":
    st.session_state.history.append({"user": user_input})
    st.rerun()


if len(st.session_state.history) > 0 and "answer" not in st.session_state.history[-1]:
    latest_question = st.session_state.history[-1]["user"]

    if source == "Wikipedia":
        raw_context = get_wikipedia_content(latest_question.split()[0])
    elif source == "arXiv":
        raw_context = get_arxiv_content(latest_question)
    elif source == "News Article":
        raw_context = get_news_article(latest_question)
    elif source == "YouTube Video":
        parsed_url = urlparse(latest_question)
        video_id = parse_qs(parsed_url.query).get("v", [""])[0] if "youtube" in latest_question else latest_question
        raw_context = get_youtube_transcript(video_id)
    elif source == "Web Search":
        raw_context = search_web(latest_question)
    elif source == "PDF Upload" and uploaded_pdf:
        relevant = retrieve_relevant_chunks(latest_question, pdf_chunks, pdf_embeddings, embedder)
        raw_context = "\n".join(relevant)
    else:
        raw_context = "[No valid source selected.]"

    summarized_context = summarize_text(raw_context, summarizer)
    prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
    answer = generate_response(prompt, rag_model)
    st.session_state.history[-1]["answer"] = answer

# Show history
for msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(msg["user"])
    if "answer" in msg:
        with st.chat_message("assistant"):
            st.markdown(msg["answer"])
