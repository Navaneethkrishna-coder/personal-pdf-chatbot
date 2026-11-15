
from embedder import Embedder
from vector_store import VectorStore
from gemini_service import GeminiService

# 1. Initialize components
embedder = Embedder()
store = VectorStore()
gemini = GeminiService()

# 2. Ask a question
question = "Which cloud and DevOps technologies do I know?"

print("\nQuestion:", question)

# 3. Convert question into embedding
query_embedding = embedder.model.encode(question)

# 4. Retrieve relevant PDF chunks
results = store.search(query_embedding, n_results=3)

if not results or not results["documents"][0]:
    print("No relevant PDF information found.")

else:

    # 5. Prepare context
    context = "\n\n".join(results["documents"][0])

    # 6. Generate answer using Gemini
    answer = gemini.generate_answer(question, context)

    print("\nChatbot Answer:\n")
    print(answer)
