import streamlit as st
from src.config import APP_TITLE, DEFAULT_MODEL
from src.documents import add_uploaded_documents, search_documents, list_documents, clear_documents
from src.ollama_client import generate
from src.study_tools import make_flashcards, make_quiz

st.set_page_config(page_title=APP_TITLE, page_icon="📚", layout="wide")
st.title("📚 Science & History Study Buddy")
st.caption("A study assistant that answers from your course materials and shows where its information came from.")

with st.sidebar:
    st.header("Settings")
    subject = st.selectbox("Study area", ["Science", "History", "Both"])
    model = st.text_input("Ollama model", value=DEFAULT_MODEL, help="Use a model already installed in Ollama, e.g. gemma3:1b.")
    st.markdown("---")
    st.subheader("Add study materials")
    uploaded = st.file_uploader("Upload PDF, TXT, or DOCX files", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    if st.button("Add materials", disabled=not uploaded, use_container_width=True):
        with st.spinner("Reading and indexing your files..."):
            count, messages = add_uploaded_documents(uploaded)
        st.success(f"Added {count} text section(s).")
        for message in messages:
            st.caption(message)
    docs = list_documents()
    st.caption(f"Indexed sections: {len(docs)}")
    if st.button("Clear indexed materials", use_container_width=True):
        clear_documents()
        st.rerun()

chat_tab, cards_tab, quiz_tab, guide_tab = st.tabs(["💬 Study chat", "🗂️ Flashcards", "📝 Practice quiz", "ℹ️ How to use"])

with chat_tab:
    st.subheader("Ask a study question")
    question = st.text_area("Your question", placeholder="Example: What were the main causes of the Industrial Revolution?", height=100)
    if st.button("Get an explanation", type="primary", key="ask"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            matches = search_documents(question, subject=subject, limit=5)
            if not matches:
                st.warning("I couldn't find relevant material in your uploaded documents. Add course notes or documents, then try again.")
            else:
                context = "\n\n".join(
                    f"[Source {i+1}: {m['source']} | {m['subject']} | section {m['section']}]\n{m['text']}"
                    for i, m in enumerate(matches)
                )
                prompt = f"""You are a careful study tutor for science and history.
Answer the student's question using ONLY the supplied study material.
If the material does not contain enough evidence, say so clearly. Do not invent citations.
Explain in student-friendly language. End with a short 'Check your understanding' question.
Student's selected subject: {subject}
Question: {question}

STUDY MATERIAL:
{context}
"""
                with st.spinner("Reading your materials and preparing an explanation..."):
                    try:
                        answer = generate(model, prompt)
                        st.markdown("### Explanation")
                        st.markdown(answer)
                        st.markdown("### Sources used")
                        for i, match in enumerate(matches, start=1):
                            with st.expander(f"[{i}] {match['source']} — {match['subject']}, section {match['section']}"):
                                st.write(match["text"])
                    except Exception as exc:
                        st.error(f"Could not reach Ollama: {exc}")
                        st.info("Make sure Ollama is running and the selected model is installed. See the README.")

with cards_tab:
    st.subheader("Create flashcards from your materials")
    topic_cards = st.text_input("Topic (optional)", placeholder="e.g. cell structure or World War I")
    if st.button("Generate flashcards", type="primary"):
        query = topic_cards.strip() or ("science history study material" if subject == "Both" else subject)
        matches = search_documents(query, subject=subject, limit=6)
        if not matches:
            st.warning("Upload study materials before generating flashcards.")
        else:
            prompt = "Create 5 concise study flashcards from ONLY the material below. Format each as **Q:** ... then **A:** ... . Do not add facts not present in the material.\n\n" + "\n\n".join(m["text"] for m in matches)
            try:
                with st.spinner("Making flashcards..."):
                    st.markdown(generate(model, prompt))
                st.caption("Review the source documents to verify each card.")
            except Exception as exc:
                st.error(f"Could not reach Ollama: {exc}")

with quiz_tab:
    st.subheader("Practice with a short quiz")
    quiz_topic = st.text_input("Quiz topic (optional)", placeholder="e.g. photosynthesis or the Civil Rights Movement")
    if st.button("Create practice quiz", type="primary"):
        query = quiz_topic.strip() or ("science history study material" if subject == "Both" else subject)
        matches = search_documents(query, subject=subject, limit=6)
        if not matches:
            st.warning("Upload study materials before creating a quiz.")
        else:
            prompt = """Create 5 multiple-choice practice questions using ONLY the supplied material.
For each question provide A-D choices, the correct answer, and a one-sentence explanation.
Do not make up details. Put the answer key after all questions.

MATERIAL:
""" + "\n\n".join(m["text"] for m in matches)
            try:
                with st.spinner("Creating your quiz..."):
                    st.markdown(generate(model, prompt))
                st.caption("This is practice material, not a graded assessment.")
            except Exception as exc:
                st.error(f"Could not reach Ollama: {exc}")

with guide_tab:
    st.subheader("Getting started")
    st.markdown("""
1. Install and start [Ollama](https://ollama.com/).
2. Download a model in Terminal, for example `ollama pull gemma3:1b`.
3. Run `streamlit run app.py` from this project folder.
4. Upload your science or history notes as PDF, TXT, or DOCX.
5. Choose a subject and ask a question, create flashcards, or make a practice quiz.

**Important:** This starter version searches uploaded documents using keyword matching (TF-IDF) and asks Ollama to explain the retrieved passages. It is not a replacement for class instruction. Always verify important information against your course materials.
""")
