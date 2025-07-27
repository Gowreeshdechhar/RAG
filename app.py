import subprocess
import os
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
    "Wikipedia", "arXiv", "PDF Upload", "News Article", "YouTube Video (Summarized)", "Web Search"])

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
st.sidebar.markdown("---")
if st.sidebar.button("🎮 Turn On Hand and Voice Command"):
    script_path = os.path.join(os.getcwd(), "hand_voice_control.py")
    try:
        subprocess.Popen(["python", script_path], shell=True)
        st.sidebar.success("🟢 Hand & Voice Control Activated")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to run hand_voice_control.py: {e}")

user_input = st.chat_input("Ask something...")

if user_input is not None and user_input.strip() != "":
    st.session_state.history.append({"user": user_input})
    st.rerun()

if len(st.session_state.history) > 0 and "answer" not in st.session_state.history[-1]:
    latest_question = st.session_state.history[-1]["user"]

    if source == "Wikipedia":
        raw_context = get_wikipedia_content(latest_question.split()[0])
        summarized_context = summarize_text(raw_context, summarizer)
        prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
    elif source == "arXiv":
        raw_context = get_arxiv_content(latest_question)
        summarized_context = summarize_text(raw_context, summarizer)
        prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
    elif source == "News Article":
        raw_context = get_news_article(latest_question)
        summarized_context = summarize_text(raw_context, summarizer)
        prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
    elif source == "YouTube Video (Summarized)":
        # Extract video ID from URL
        parsed_url = urlparse(latest_question)
        video_id = None
        if "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
            if "youtu.be" in parsed_url.netloc:
                video_id = parsed_url.path.lstrip("/")
            elif "youtube.com" in parsed_url.netloc:
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get("v", [None])[0]
        
        # Fallback: treat input as video ID if no valid URL
        if not video_id or len(video_id) != 11:
            video_id = latest_question.strip() if len(latest_question.strip()) == 11 else None

        if video_id:
            raw_context = get_youtube_transcript(video_id)
            if "Error" not in raw_context:
                summarized_context = summarize_text(raw_context, summarizer)
                prompt = f"Summary of YouTube video: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
            else:
                summarized_context = f"No transcript available for video ID: {video_id}"
                prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
                st.error(summarized_context)
        else:
            summarized_context = "Invalid YouTube URL or video ID. Please provide a valid YouTube link or 11-character video ID."
            prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
            st.error(summarized_context)
    elif source == "Web Search":
        raw_context = search_web(latest_question)
        summarized_context = summarize_text(raw_context, summarizer)
        prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
    elif source == "PDF Upload" and uploaded_pdf:
        relevant = retrieve_relevant_chunks(latest_question, pdf_chunks, pdf_embeddings, embedder)
        raw_context = "\n".join(relevant)
        summarized_context = summarize_text(raw_context, summarizer)
        prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
    else:
        raw_context = "[No valid source selected.]"
        summarized_context = raw_context
        prompt = f"Context: {summarized_context}\n\nQuestion: {latest_question}\nAnswer:"
        st.error(summarized_context)

    answer = generate_response(prompt, rag_model)
    st.session_state.history[-1]["answer"] = answer

# Show history
for msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(msg["user"])
    if "answer" in msg:
        with st.chat_message("assistant"):
            st.markdown(msg["answer"])