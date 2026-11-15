
import pymupdf
import os


def extract_text(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = pymupdf.open(pdf_path)
    extracted_pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        extracted_pages.append({
            "page": page_number,
            "text": text
        })

    document.close()
    return extracted_pages


if __name__ == "__main__":
    pdf_path = "data/resume (1).pdf"

    pages = extract_text(pdf_path)

    print(f"Total pages extracted: {len(pages)}")

    for page in pages:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"][:500])


