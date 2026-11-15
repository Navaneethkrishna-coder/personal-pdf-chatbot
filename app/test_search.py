
from embedder import Embedder
from vector_store import VectorStore

# 1. Initialize embedding model
embedder = Embedder()

# 2. Initialize ChromaDB
store = VectorStore()

# 3. Ask a question
question = "Which cloud and DevOps technologies do I know?"

print("\nUser Question:")
print(question)

# 4. Convert question into embedding
query_embedding = embedder.model.encode(question)

# 5. Search relevant chunks
results = store.search(
    query_embedding,
    n_results=3
)

# 6. Display retrieved information
print("\nRelevant PDF Information:\n")

if results and results["documents"]:
    for i, document in enumerate(results["documents"][0]):

        print(f"Result {i + 1}:")
        print(document)

        print("Metadata:", results["metadatas"][0][i])
        print("Distance:", results["distances"][0][i])

        print("-" * 50)
else:
    print("No relevant information found.")
