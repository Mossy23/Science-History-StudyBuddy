import os

APP_TITLE = "Science & History Study Buddy"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
DATA_DIR = os.getenv("STUDY_BUDDY_DATA", "data")
