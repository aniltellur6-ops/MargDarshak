import io
from pypdf import PdfReader
from docx import Document

def parse_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")
    return text

def parse_docx(file_bytes: bytes) -> str:
    text = ""
    try:
        doc = Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")
    return text

def parse_document(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return parse_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        return parse_docx(file_bytes)
    elif filename.lower().endswith(".txt"):
        return file_bytes.decode("utf-8")
    else:
        raise ValueError(f"Unsupported file format for {filename}")
