

import os
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.embedder import Embedder
from app.vector_store import VectorStore
from app.gemini_service import GeminiService
from app.pdf_reader import extract_text
from app.chunker import create_chunks


app = FastAPI(
    title="Personal PDF Chatbot API",
    description="Ask questions about your PDF documents",
    version="1.1.0"
)

embedder = Embedder()
store = VectorStore()
gemini = GeminiService()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Personal PDF Chatbot API is running!"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    safe_filename = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_filename

    try:
        content = await file.read(MAX_FILE_SIZE + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty"
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF size must not exceed 10 MB"
            )

        # Save the uploaded PDF
        with file_path.open("wb") as buffer:
            buffer.write(content)

        # Extract PDF text
        pages = extract_text(str(file_path))

        if not any(page["text"].strip() for page in pages):
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF"
            )

        # Create chunks
        chunks = create_chunks(pages)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not create text chunks from this PDF"
            )

        # Generate embeddings
        embeddings = embedder.generate_embeddings(chunks)

        # Store chunks in ChromaDB
        document_id = store.add_chunks(
            chunks,
            embeddings,
            source=safe_filename
        )

        return {
            "message": "PDF uploaded and processed successfully",
            "filename": safe_filename,
            "document_id": document_id,
            "pages": len(pages),
            "chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="PDF processing failed"
        ) from e

    finally:
        await file.close()


@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        query_embedding = embedder.model.encode(question)

        results = store.search(
            query_embedding,
            n_results=6
        )

        if not results or not results["documents"][0]:
            return {
                "question": question,
                "answer": "No relevant information found in your PDFs.",
                "sources": []
            }

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n\n".join(documents)

        answer = (
             "I found the following relevant information in your PDFs:\n\n"
             + "\n\n".join(documents[:3])
        )

        sources = [
             {
                 "filename": metadata.get("source", "Unknown PDF"),
                 "page": metadata.get("page", "Unknown"),
                 "text": document
            }
            for document, metadata in zip(documents, metadatas)
        ]
        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
                status_code=500,
                detail="Chatbot processing failed"
        ) from e
