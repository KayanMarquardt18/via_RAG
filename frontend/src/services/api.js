const API_URL = "http://localhost:8001";

export async function classificarObjeto(dados) {
  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  if (!response.ok) throw new Error("Erro ao classificar objeto");
  return response.json();
}

export async function perguntarRAG(pergunta, historico = []) {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pergunta, historico }),
  });
  if (!response.ok) throw new Error("Erro ao buscar resposta");
  return response.json();
}