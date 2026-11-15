import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)

        self.models = [
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite"
        ]

    def generate_answer(self, question, context):

        prompt = f"""
You are a helpful Personal PDF Assistant.

Answer the user's question using ONLY the information
provided in the PDF context below.

If the answer is not available in the context,
say: "I could not find this information in your PDF."

Do not invent information.

PDF CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

        last_error = None

        for model in self.models:
            for attempt in range(2):
                try:
                    print(f"Trying Gemini model: {model}")

                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if response.text:
                        print(f"Successfully generated answer using {model}")
                        return response.text

                    raise RuntimeError("Gemini returned an empty response")

                except Exception as e:
                    last_error = e
                    print(
                        f"Model {model}, attempt {attempt + 1} failed: "
                        f"{type(e).__name__}: {e}"
                    )

                    if attempt == 0:
                        time.sleep(2)

        raise RuntimeError(
            "All configured Gemini models failed. Check the backend logs."
        ) from last_error


if __name__ == "__main__":
    print("Gemini service initialized successfully!")
