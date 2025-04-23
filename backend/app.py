from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import BertTokenizerFast
from model import model, config
from processor import batch_process

app = FastAPI()

# 1) Configure o CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "app://-/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Setup do modelo e tokenizer
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.load_state_dict(torch.load("model/model.pt", map_location=DEVICE))
model.to(DEVICE).eval()

tokenizer = BertTokenizerFast.from_pretrained(
    "bert-base-multilingual-cased", vocab_size=config.vocab_size
)

# 3) Rotas da API
class TextReq(BaseModel):
    text: str

@app.post("/api/single")
def single(req: TextReq):
    enc = tokenizer(req.text, return_tensors="pt", truncation=True, padding=True)
    logits = model(**enc.to(DEVICE)).logits
    idx = torch.argmax(logits, dim=1).item()
    return {"sentiment": ["neg", "neu", "pos"][idx]}

@app.post("/api/batch")
def batch(file: UploadFile = File(...)):
    path = f"temp/{file.filename}"
    open(path, "wb").write(file.file.read())
    out = batch_process(path, lambda t: single(TextReq(text=t))["sentiment"])
    return {"file": out}

@app.post("/api/train")
def train(file: UploadFile = File(...)):
    path = f"temp/{file.filename}"
    open(path, "wb").write(file.file.read())
    try:
        from train import train_model
        train_model(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "treinamento concluído"}

# 4) Por último: monte o frontend estático
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
