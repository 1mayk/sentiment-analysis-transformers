# Sentiment Analysis Transformers

## Pré-requisitos

- Python 3.8+
- Node.js 16+
- npm 8+

---

## 1. Instalação

### Backend
```bash
cd backend
python -m venv .venv
.venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Frontend
```bash
cd ../frontend
npm install
```

### Electron (App Desktop)
```bash
cd ../electron
npm install
```

---

## 2. Modo Desenvolvimento

### Backend (API)
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

ou

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Web)
Em outro terminal:
```bash
cd frontend
npm run dev
```
Acesse: http://localhost:5173

### Electron (App Desktop)
Em outro terminal:
```bash
cd electron
npm start
```

---

## 3. Modo Produção

### Build do Frontend
```bash
cd frontend
npm run build
```

### Backend servindo o build do frontend
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000

ou

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Acesse: http://localhost:8000

---

## 4. Treinamento do Modelo

Você deve treinar o modelo usando um arquivo CSV com as colunas `text` e `label`, onde a coluna `label` deve conter os valores **ruim**, **neutro** ou **bom** (em minúsculo, sem acento). Exemplo:

```
text,label
"O atendimento foi péssimo.",ruim
"Gostei muito do produto!",bom
"O serviço foi aceitável.",neutro
```

Para treinar via terminal:
```bash
cd backend
python train.py sample_data.csv
```

Ou envie um arquivo via interface web ou desktop na seção "Treinamento".

---

## 5. Geração do Executável Desktop Único (Windows)

O objetivo é gerar um único instalador `.exe` que embarca backend, frontend e Electron. Siga os passos:

### 1. Gere o build do frontend
```bash
cd frontend
npm run build
```

### 2. Empacote o backend com PyInstaller
```bash
cd backend
pip install pyinstaller
pyinstaller --onefile app.py
```
O executável será gerado em `backend/dist/app.exe`.

### 3. Ajuste o Electron para rodar o backend empacotado
No arquivo `electron/main.js`, altere a linha:
```js
apiProcess = spawn("python", ["../backend/app.py"]);
```
para:
```js
apiProcess = spawn("../backend/dist/app.exe");
```

### 4. Gere o instalador do Electron
```bash
cd electron
npm run build
```
O instalador final estará em `electron/dist`.

> **Atenção:** O build espera um ícone em `electron/assets/app-icon.ico`. Crie essa pasta e adicione um ícone se desejar personalizar.

---

## 6. Observações
- O backend espera o modelo treinado em `backend/model/model.pt`. Se não existir, treine ou baixe um modelo antes de rodar em produção.
- Arquivos temporários e modelos não são versionados (ver `.gitignore`).
- O app desktop inicia automaticamente o backend ao abrir.
- As labels aceitas são: **ruim**, **neutro** e **bom**.

---

## 7. Estrutura do Projeto

```
backend/    # API FastAPI, modelo, treinamento
frontend/   # React + Vite (web)
electron/   # App desktop (Electron)
```

---

## 8. Dúvidas
Abra uma issue ou consulte o código para mais detalhes.
