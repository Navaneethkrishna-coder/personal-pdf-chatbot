
def create_chunks(pages, chunk_size=500, overlap=100):
    chunks = []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "page": page["page"],
                    "text": chunk_text.strip()
                })

            start += chunk_size - overlap

    return chunks
