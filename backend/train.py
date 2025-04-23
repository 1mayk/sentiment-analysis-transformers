import os
import torch
from datasets import load_dataset
from transformers import BertTokenizerFast, BertForSequenceClassification
from model import config

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_model(data_path, epochs=3, batch_size=16, lr=5e-5):
    # 1. Carrega tokenizer e ajusta vocab_size
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
    config.vocab_size = (
        tokenizer.vocab_size
    )  # corrige mismatch :contentReference[oaicite:11]{index=11}

    # 2. Instancia o modelo zero-shot com config corrigido
    model = BertForSequenceClassification(config)
    model.to(DEVICE)

    # 3. Carrega dados
    ds = load_dataset("csv", data_files={"train": data_path, "test": data_path})

    def tok(ex):
        return tokenizer(
            ex["text"], truncation=True, padding="max_length", max_length=128
        )

    tok_ds = ds.map(tok, batched=True)
    tok_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    loader = torch.utils.data.DataLoader(
        tok_ds["train"], batch_size=batch_size, shuffle=True
    )

    # 4. Otimizador e treinamento
    optim = torch.optim.AdamW(model.parameters(), lr=lr)
    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0
        for batch in loader:
            inputs = {k: v.to(DEVICE) for k, v in batch.items() if k != "label"}
            labels = batch["label"].to(DEVICE)
            loss = model(**inputs, labels=labels).loss
            loss.backward()
            optim.step()
            optim.zero_grad()
            total_loss += loss.item()
        print(f"Epoch {epoch}/{epochs} — loss média: {total_loss/len(loader):.4f}")

    # 5. Salva o modelo treinado
    os.makedirs("model", exist_ok=True)
    torch.save(model.state_dict(), "model/model.pt")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python train.py <caminho_para_csv>")
        sys.exit(1)
    train_model(sys.argv[1])
