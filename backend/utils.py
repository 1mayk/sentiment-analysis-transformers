from pdfminer.high_level import extract_text
from docx import Document


def read_text_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_pdf(path):
    return extract_text(path)


def read_docx(path):
    return "\n".join(p.text for p in Document(path).paragraphs)
