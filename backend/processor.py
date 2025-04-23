import pandas as pd
from utils import read_text_file, read_pdf, read_docx


def process_file(path: str) -> str:
    ext = path.lower().split(".")[-1]
    if ext == "txt":
        return read_text_file(path)
    if ext == "pdf":
        return read_pdf(path)
    if ext == "docx":
        return read_docx(path)
    raise ValueError("Formato não suportado")


def batch_process(path: str, predict_fn):
    df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    df["sentiment"] = df["text"].apply(predict_fn)
    out = path.replace(".", "_out.")
    (
        df.to_csv(out, index=False)
        if out.endswith(".csv")
        else df.to_excel(out, index=False)
    )
    return out
