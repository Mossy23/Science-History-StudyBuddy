from src.documents import _chunks

def test_chunks_returns_text_sections():
    chunks = _chunks("one two three four five", max_words=3, overlap=1)
    assert chunks
    assert chunks[0] == "one two three"
    assert "five" in chunks[-1]
