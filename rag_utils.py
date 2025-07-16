# rag_utils.py
import arxiv
import wikipedia
import fitz
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from newspaper import Article
from youtube_transcript_api import YouTubeTranscriptApi
from duckduckgo_search import DDGS

def get_wikipedia_content(topic):
    try:
        return wikipedia.page(topic).content
    except Exception as e:
        return f"Error fetching Wikipedia content: {str(e)}"

def get_arxiv_content(query):
    try:
        search = arxiv.Search(query=query, max_results=3)
        summaries = [result.summary for result in search.results()]
        return "\n\n".join(summaries)
    except Exception as e:
        return f"Error fetching ArXiv content: {str(e)}"

def get_news_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error fetching news article: {str(e)}"

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error fetching YouTube transcript: {str(e)}"

def search_web(query, max_results=3):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
            return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Error performing web search: {str(e)}"

def extract_text_from_pdf(pdf):
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def build_faiss_index(docs, embedder):
    embeddings = embedder.encode(docs, convert_to_tensor=False)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, embeddings

def retrieve_relevant_chunks(query, docs, embeddings, embedder, k=3):
    query_vec = embedder.encode([query])[0]
    index = faiss.IndexFlatL2(len(query_vec))
    index.add(np.array(embeddings))
    distances, indices = index.search(np.array([query_vec]), k)
    return [docs[i] for i in indices[0]]

def generate_response(prompt, model):
    result = model(prompt, max_new_tokens=150)[0]["generated_text"]
    return result.replace(prompt, "").strip()

def summarize_text(text, summarizer, max_chunk_length=1000):
    if len(text) < max_chunk_length:
        return summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    
    chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = [summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)
