import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate(model: str, prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=180,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("response", "").strip()
