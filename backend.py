# backend.py
import os
import fitz  # PyMuPDF
from veryfi import Client

VERYFI_CLIENT_ID = os.getenv("VERYFI_CLIENT_ID")
VERYFI_CLIENT_SECRET = os.getenv("VERYFI_CLIENT_SECRET")
VERYFI_USERNAME = os.getenv("VERYFI_USERNAME")
VERYFI_API_KEY = os.getenv("VERYFI_API_KEY")

client = Client(VERYFI_CLIENT_ID, VERYFI_CLIENT_SECRET, VERYFI_USERNAME, VERYFI_API_KEY)


def remove_logo_field(obj):
    if isinstance(obj, dict):
        return {k: remove_logo_field(v) for k, v in obj.items() if k != "logo"}
    elif isinstance(obj, list):
        return [remove_logo_field(item) for item in obj]
    return obj


def split_pdf(input_pdf_path, chunk_size=3):
    doc = fitz.open(input_pdf_path)
    chunks = []
    for i in range(0, len(doc), chunk_size):
        subdoc = fitz.open()
        for j in range(i, min(i + chunk_size, len(doc))):
            subdoc.insert_pdf(doc, from_page=j, to_page=j)
        chunk_path = f"{input_pdf_path}_chunk_{i//chunk_size}.pdf"
        subdoc.save(chunk_path)
        subdoc.close()
        chunks.append(chunk_path)
    doc.close()
    return chunks


def process_invoice_pdf(pdf_path):
    all_cleaned_data = []
    full_ocr_text = ""

    chunks = split_pdf(pdf_path, chunk_size=3)
    for chunk_path in chunks:
        response = client.process_document(chunk_path, ["Invoices"])
        cleaned = {
            k: v for k, v in response.items()
            if k not in ["meta", "img_thumbnail_url", "img_url", "pdf_url"]
        }
        cleaned = remove_logo_field(cleaned)
        all_cleaned_data.append(cleaned)

        text_output = cleaned.get("ocr_text", "")
        full_ocr_text += text_output + "\n\n"

    return {
        "invoices": all_cleaned_data,
        "combined_ocr_text": full_ocr_text.strip()
    }
