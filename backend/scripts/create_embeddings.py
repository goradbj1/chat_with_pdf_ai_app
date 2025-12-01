import os
from pdf_loader import load_pdf, split_text
from vector_store import build_vector_store, load_index

PDF_FOLDER = "data/"

def process_pdfs():
    print("Loading existing FAISS index (if available)...")
    load_index()

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in /pdfs folder!")
        return

    for pdf in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf)
        print(f"\nProcessing PDF: {pdf_path}")

        text = load_pdf(pdf_path)
        chunks = split_text(text)

        print(f" - Extracted {len(chunks)} chunks")
        print(" - Updating vector store...")

        build_vector_store(chunks)

    print("\nAll PDFs processed successfully!")
    print("Persistent FAISS index updated.")

if __name__ == "__main__":
    process_pdfs()