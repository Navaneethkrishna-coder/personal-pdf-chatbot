
from pdf_reader import extract_text
from chunker import create_chunks
from embedder import Embedder

# Step 1: Extract PDF text
pdf_path = "data/resume (1).pdf"

pages = extract_text(pdf_path)

# Step 2: Split text into chunks
chunks = create_chunks(pages)

print("Total chunks:", len(chunks))

# Step 3: Generate embeddings
embedder = Embedder()

embeddings = embedder.generate_embeddings(chunks)

# Step 4: Display results
print("\nEmbedding generation completed!")

print("Total embeddings:", len(embeddings))
print("Embedding dimensions:", embeddings.shape)

print("\nFirst chunk:")
print(chunks[0]["text"])

print("\nFirst embedding:")
print(embeddings[0][:10])
