
from pdf_reader import extract_text
from chunker import create_chunks

# Extract PDF text
pages = extract_text("data/resume (1).pdf")

# Split extracted text into chunks
chunks = create_chunks(
    pages,
    chunk_size=500,
    overlap=100
)

# Display results
print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print("Source page:", chunk["page"])
    print("Text:", chunk["text"])
