
from pdf_reader import extract_text
from chunker import create_chunks
from embedder import Embedder
from vector_store import VectorStore

# 1. Extract PDF text
pdf_path = "data/resume (1).pdf"
pages = extract_text(pdf_path)

# 2. Create chunks
chunks = create_chunks(pages)

# 3. Generate embeddings
embedder = Embedder()
embeddings = embedder.generate_embeddings(chunks)

# 4. Initialize vector database
store = VectorStore()

# 5. Store chunks and embeddings
store.add_chunks(chunks, embeddings)

# 6. Verify storage
print("Total stored chunks:", store.get_count())
