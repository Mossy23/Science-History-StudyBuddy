# Science & History Study Buddy AI

A student-focused study assistant for **science and history**. Upload course materials, ask questions, and create practice flashcards or quizzes. The assistant retrieves relevant passages from the uploaded files and asks a local Ollama model to explain them.

## Features

- Science, History, or combined study mode
- Upload PDF, TXT, and DOCX course materials
- Search uploaded material using TF-IDF keyword relevance
- Ask questions and view the passages used to form an answer
- Generate practice flashcards and multiple-choice quizzes
- Run the language model locally through Ollama

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running
- A model downloaded in Ollama (the default is `gemma3:1b`)

## Setup on macOS

Open Terminal and move into this project folder:

```bash
cd Science-History-StudyBuddy
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the default Ollama model:

```bash
ollama pull gemma3:1b
```

Start the app:

```bash
streamlit run app.py
```

If you already have a different Ollama model installed, enter its exact name in the app's sidebar. You can see installed models with:

```bash
ollama list
```

## How to use it

1. Upload course PDFs, text files, or Word documents in the sidebar.
2. Put `science` or `history` in the filename to categorize the document automatically. Otherwise it is categorized as Uncategorized and can be searched in either subject mode.
3. Select Science, History, or Both.
4. Ask a question in Study Chat, or use the Flashcards and Practice Quiz tabs.
5. Expand the source list under a chat answer to inspect the passages retrieved from your materials.

## Example

Upload a history document named `history_industrial_revolution.pdf`, select **History**, and ask:

> What factors helped Britain industrialize first?

The app searches the uploaded document, sends the best matching passages to Ollama, and displays an explanation plus the source filename and page/section labels.

The actual response depends on the contents of the uploaded file and the Ollama model you choose.

## How it works

**Input → processing → output**

1. A student uploads a document or enters a question.
2. The app extracts text from the document and divides it into short sections.
3. TF-IDF ranks the sections most related to the question.
4. The selected passages are sent to Ollama with instructions to stay grounded in the material.
5. The app displays the generated explanation and the passages used.

## Current limitations

- This is a starter prototype, not a finished educational product.
- Retrieval uses TF-IDF keyword matching, not semantic/vector search. It may miss relevant passages when different words are used.
- PDF text extraction may not work well on scanned/image-only PDFs.
- Subject categorization is based on filenames. Uncategorized files can appear in either subject search.
- The app does not independently verify whether a source document is accurate or unbiased.
- The model can still misunderstand or misstate information. Check important answers against course materials.
- Uploaded files are held in the current Streamlit session; this starter does not provide permanent accounts or cloud storage.
- Flashcards and quiz questions are AI-generated drafts and should be reviewed.

## Evaluation checklist

Before using this as a final-project prototype, test it with a small set of questions and record the actual results.

| Test | What to check | Result |
|---|---|---|
| Science question with evidence in a file | Is the answer supported by the retrieved passage? | To be tested |
| History question with evidence in a file | Does it explain the event accurately? | To be tested |
| Question not covered by uploaded files | Does it admit the material is insufficient? | To be tested |
| Ambiguous question | Does it ask for clarification or explain uncertainty? | To be tested |
| Flashcards and quiz | Are the generated facts supported by the documents? | To be tested |

Do not report planned tests as completed results. Record real examples, including incorrect or unsupported answers.

## Responsible use

This tool is intended to support learning, not replace teachers, textbooks, or original research. It may reproduce errors or bias in uploaded materials and may generate incorrect explanations. Students should verify important claims, check cited passages, avoid uploading private or sensitive information, and follow course rules about AI use.

## Project structure

```text
Science-History-StudyBuddy/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── config.py
│   ├── documents.py
│   ├── ollama_client.py
│   └── study_tools.py
└── tests/
    └── test_documents.py
```

## Future improvements

- Semantic search with embeddings and a vector database
- Better source citations with page numbers and highlighted excerpts
- User-selectable difficulty and answer length
- Saved study sets and quiz scores
- More robust tests for factual accuracy, source relevance, bias, and uncertainty
