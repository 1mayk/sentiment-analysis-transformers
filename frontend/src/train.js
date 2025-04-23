/**
 * Envia o arquivo CSV/Excel para treinar o modelo via API
 * @param {File} file
 * @returns {Promise<Object>} status do treinamento
 */
export async function trainModel(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("http://localhost:8000/api/train", {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error("Erro no treinamento");
  return res.json(); // { status: 'treinamento concluído' }
}
