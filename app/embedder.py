
from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embeddings(self, chunks):

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        return embeddings


if __name__ == "__main__":
    print("Embedding model is ready!")
