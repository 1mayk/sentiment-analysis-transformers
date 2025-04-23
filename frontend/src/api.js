const BASE = "http://localhost:8000/api";

/** Análise de texto único */
export async function analyze(text) {
  const res = await fetch(`${BASE}/single`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return res.json();
}

/** Processamento batch CSV/Excel */
export async function batch(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/batch`, {
    method: "POST",
    body: form,
  });
  return res.json();
}
