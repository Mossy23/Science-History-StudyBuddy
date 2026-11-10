from pathlib import Path
import io
import re
import streamlit as st
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _extract(upload):
    name = upload.name
    suffix = Path(name).suffix.lower()
    raw = upload.getvalue()
    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(raw))
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    if suffix == ".docx":
        doc = Document(io.BytesIO(raw))
        text = "\n".join(p.text for p in doc.paragraphs)
        return [(1, text)]
    if suffix == ".txt":
        return [(1, raw.decode("utf-8", errors="replace"))]
    raise ValueError(f"Unsupported file type: {suffix}")

def _chunks(text, max_words=180, overlap=30):
    words = re.sub(r"\s+", " ", text).split()
    if not words:
        return []
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks

def add_uploaded_documents(uploads):
    records = st.session_state.setdefault("study_documents", [])
    messages, added = [], 0
    for upload in uploads:
        subject = "Science" if "science" in upload.name.lower() else ("History" if "history" in upload.name.lower() else "Uncategorized")
        try:
            pages = _extract(upload)
            for page_number, text in pages:
                for section_number, chunk in enumerate(_chunks(text), start=1):
                    records.append({
                        "source": upload.name,
                        "subject": subject,
                        "section": f"{page_number}.{section_number}",
                        "text": chunk,
                    })
                    added += 1
            messages.append(f"{upload.name}: categorized as {subject}. Rename files to include 'science' or 'history' to help categorize them.")
        except Exception as exc:
            messages.append(f"{upload.name}: couldn't read file ({exc}).")
    return added, messages

def list_documents():
    return st.session_state.get("study_documents", [])

def clear_documents():
    st.session_state["study_documents"] = []

def search_documents(query, subject="Both", limit=5):
    records = list_documents()
    if subject in ("Science", "History"):
        records = [r for r in records if r["subject"] in (subject, "Uncategorized")]
    if not records or not query.strip():
        return []
    corpus = [r["text"] for r in records]
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(corpus + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    except ValueError:
        return []
    ranked = sorted(zip(scores, records), key=lambda item: item[0], reverse=True)
    return [record for score, record in ranked[:limit] if score > 0]
