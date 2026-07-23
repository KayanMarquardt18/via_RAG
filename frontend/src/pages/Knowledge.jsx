import { useState } from "react";
import { perguntarRAG } from "../services/api";

const TEMAS = [
  "Estrelas e nucleossíntese", "Galáxias e Via Láctea", "Buracos negros",
  "Núcleos Galácticos Ativos (AGN)", "Exoplanetas", "Supernovas",
  "Matéria escura", "Sistema Solar", "Ondas gravitacionais", "Big Bang",
  "Telescópios espaciais", "Relatividade", "A Lua", "Missões da NASA",
];

export default function Knowledge() {
  const [historico, setHistorico] = useState([]);
  const [pergunta, setPergunta] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!pergunta.trim() || carregando) return;

    const perguntaAtual = pergunta;
    const idUser = crypto.randomUUID();
    setHistorico((h) => [...h, { id: idUser, autor: "user", texto: perguntaAtual }]);
    setPergunta("");
    setCarregando(true);

    try {
      // converte "ia" → "assistant" pro formato da API OpenAI
      const historicoFormatado = historico.map((msg) => ({
        autor: msg.autor === "ia" ? "assistant" : msg.autor,
        texto: msg.texto,
      }));

      const data = await perguntarRAG(perguntaAtual, historicoFormatado);
      setHistorico((h) => [
        ...h,
        { id: crypto.randomUUID(), autor: "ia", texto: data.resposta },
      ]);
    } catch {
      setHistorico((h) => [
        ...h,
        {
          id: crypto.randomUUID(),
          autor: "erro",
          texto: "Não consegui falar com o backend. Confirme se a API está no ar.",
        },
      ]);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="page knowledge-page">
      <span className="eyebrow">Base de conhecimento</span>
      <h1>Pergunte sobre o cosmos</h1>
      <p className="lede">
        As respostas vêm exclusivamente de uma base de textos sobre astronomia.
        Fora desse escopo, o sistema diz que não encontrou a informação.
      </p>

      <details className="ajuda-pesquisa" open>
        <summary>O que está dentro da base de conhecimento?</summary>
        <div className="temas-grid">
          {TEMAS.map((t) => (
            <span key={t} className="tema-chip">{t}</span>
          ))}
        </div>
      </details>

      <div className="panel chat-window">
        <div className="chat-log">
          {historico.length === 0 && (
            <p className="chat-empty">
              Experimente: "O que são AGN?" ou "Como o universo começou?"
            </p>
          )}
          {historico.map((msg) => (
            <div key={msg.id} className={`chat-bubble chat-bubble--${msg.autor}`}>
              {msg.texto}
            </div>
          ))}
          {carregando && (
            <div className="chat-bubble chat-bubble--ia chat-bubble--loading">
              buscando na base…
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            placeholder="O que são AGN?"
            value={pergunta}
            onChange={(e) => setPergunta(e.target.value)}
            disabled={carregando}
          />
          <button type="submit" disabled={carregando}>
            {carregando ? (<><span className="spinner" />Buscando</>) : "Perguntar"}
          </button>
        </form>
      </div>
    </div>
  );
}