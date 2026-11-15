

import chromadb
from uuid import uuid4


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="personal_pdf"
        )

    def add_chunks(self, chunks, embeddings, source="resume.pdf"):

        if not chunks:
            raise ValueError("No text chunks to store")

        document_id = str(uuid4())

        documents = [chunk["text"] for chunk in chunks]

        ids = [
            f"{document_id}_chunk_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "source": source,
                "document_id": document_id,
                "chunk_index": i,
                "page": chunk["page"]
            }
            for i, chunk in enumerate(chunks)
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(f"Stored {len(chunks)} chunks from {source}")

        return document_id

    def search(self, query_embedding, n_results=3):

        total = self.collection.count()

        if total == 0:
            return None

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(n_results, total),
            include=["documents", "metadatas", "distances"]
        )

        return results

    def get_count(self):
        return self.collection.count()


if __name__ == "__main__":
    store = VectorStore()
    print("Current document count:", store.get_count())

