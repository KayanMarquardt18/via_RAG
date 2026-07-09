import { useState } from "react";
import { classificarObjeto } from "../services/api";

const CAMPOS = [
  { nome: "u", label: "u — ultravioleta", faixa: "~355 nm" },
  { nome: "g", label: "g — verde/azul", faixa: "~469 nm" },
  { nome: "r", label: "r — vermelho", faixa: "~617 nm" },
  { nome: "i", label: "i — infravermelho próx.", faixa: "~748 nm" },
  { nome: "z", label: "z — infravermelho", faixa: "~893 nm" },
  { nome: "redshift", label: "redshift (z)", faixa: "desvio espectral" },
];

const QUIZ = [
  {
    id: 1,
    descricao: "Objeto brilhante próximo, magnitudes decrescentes suavemente",
    valores: { u: 18.12, g: 17.34, r: 17.02, i: 16.85, z: 16.74, redshift: 0.0001 },
    resposta: "STAR",
    dica: "Redshift quase zero = objeto na nossa galáxia. Magnitudes graduais = estrela fria.",
  },
  {
    id: 2,
    descricao: "Objeto distante com brilho moderado e redshift médio",
    valores: { u: 19.84, g: 18.12, r: 17.45, i: 17.10, z: 16.89, redshift: 0.12 },
    resposta: "GALAXY",
    dica: "Redshift moderado = fora da Via Láctea. Queda suave de brilho = galáxia típica.",
  },
  {
    id: 3,
    descricao: "Objeto extremamente distante com magnitudes quase planas",
    valores: { u: 18.56, g: 18.73, r: 18.90, i: 18.76, z: 18.45, redshift: 1.42 },
    resposta: "QSO",
    dica: "Redshift alto = bilhões de anos-luz. Magnitudes planas = emissão intensa do disco de acreção.",
  },
  {
    id: 4,
    descricao: "Objeto muito brilhante, extremamente próximo",
    valores: { u: 14.20, g: 13.88, r: 13.65, i: 13.52, z: 13.44, redshift: 0.00003 },
    resposta: "STAR",
    dica: "Magnitudes muito baixas (mais brilhante) + redshift ≈ 0 = estrela próxima e luminosa.",
  },
  {
    id: 5,
    descricao: "Objeto com emissão ultravioleta intensa e redshift elevado",
    valores: { u: 17.20, g: 17.85, r: 18.10, i: 17.95, z: 17.60, redshift: 2.18 },
    resposta: "QSO",
    dica: "U mais brilhante que g/r + redshift > 2 = quasar distante com emissão UV forte.",
  },
];

export default function Predictor() {
  const [aba, setAba] = useState("classificar");
  const [valores, setValores] = useState({ u: "", g: "", r: "", i: "", z: "", redshift: "" });
  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);
  const [caderneta, setCaderneta] = useState([]);
  const [revelados, setRevelados] = useState({});
  const [chutes, setChutes] = useState({});

  function handleChange(e) {
    const { name, value } = e.target;
    setValores((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErro(null);
    setCarregando(true);
    setResultado(null);
    try {
      const dados = Object.fromEntries(
        Object.entries(valores).map(([k, v]) => [k, parseFloat(v)])
      );
      const resposta = await classificarObjeto(dados);
      setResultado(resposta);
      setCaderneta((prev) => [
        {
          id: Date.now(),
          data: new Date().toLocaleString("pt-BR"),
          valores: dados,
          classe: resposta.prediction,
          prob: Math.max(...Object.values(resposta.probabilities)) * 100,
        },
        ...prev,
      ]);
    } catch {
      setErro("Não consegui falar com o backend. Confirme se a API está no ar.");
    } finally {
      setCarregando(false);
    }
  }

  function revelar(id) {
    setRevelados((prev) => ({ ...prev, [id]: true }));
  }

  function chutar(id, classe) {
    setChutes((prev) => ({ ...prev, [id]: classe }));
  }

  function preencherClassificador(vals) {
    setValores(Object.fromEntries(Object.entries(vals).map(([k, v]) => [k, String(v)])));
    setAba("classificar");
  }

  const ABAS = { classificar: "Classificar", guia: "Guia ugriz", treino: "Treino", caderneta: "Caderneta" };

  return (
    <div className="page predictor-page">
      <span className="eyebrow">Classificador fotométrico</span>
      <h1>O que é esse objeto?</h1>

      <div className="predictor-tabs">
        {Object.entries(ABAS).map(([key, label]) => (
          <button
            key={key}
            className={`tab-btn ${aba === key ? "tab-btn--active" : ""}`}
            onClick={() => setAba(key)}
          >
            {label}
          </button>
        ))}
      </div>

      {/* ABA CLASSIFICAR */}
      {aba === "classificar" && (
        <>
          <p className="lede">
            Insira as magnitudes <code>u, g, r, i, z</code> e o redshift de um objeto do catálogo SDSS.
          </p>
          <form onSubmit={handleSubmit} className="panel predictor-form">
            <div className="field-grid">
              {CAMPOS.map((campo) => (
                <label key={campo.nome} className="field">
                  <span className="field-label">{campo.label}</span>
                  <input
                    type="number"
                    step="any"
                    name={campo.nome}
                    value={valores[campo.nome]}
                    onChange={handleChange}
                    placeholder={campo.faixa}
                    required
                  />
                </label>
              ))}
            </div>
            <button type="submit" disabled={carregando}>
              {carregando ? (<><span className="spinner" />Classificando</>) : "Classificar objeto"}
            </button>
          </form>

          {erro && <p className="erro">{erro}</p>}

          {resultado && (
            <div className="panel resultado">
              <span className="eyebrow">Resultado</span>
              <h2>{resultado.prediction}</h2>
              <div className="prob-bars">
                {Object.entries(resultado.probabilities).map(([classe, prob]) => (
                  <div key={classe} className="prob-row">
                    <span>{classe}</span>
                    <div className="prob-track">
                      <div className="prob-fill" style={{ width: `${prob * 100}%` }} />
                    </div>
                    <span>{(prob * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
              <h3>Por que esse resultado?</h3>
              <p>{resultado.explanation}</p>
            </div>
          )}

          <details className="ajuda-pesquisa">
            <summary>Onde encontro esses valores para testar?</summary>
            <p>
              Pesquise objetos reais no{" "}
              <a href="https://skyserver.sdss.org" target="_blank" rel="noreferrer">SDSS SkyServer</a>{" "}
              — busque um objeto e procure a tabela <code>PhotoObj</code> com as magnitudes e o redshift.
            </p>
          </details>
        </>
      )}

      {/* ABA GUIA */}
      {aba === "guia" && (
        <div className="guia-content">
          <div className="panel guia-block">
            <span className="eyebrow">O sistema SDSS</span>
            <h2>De onde vêm esses dados?</h2>
            <p>
              O <strong>Sloan Digital Sky Survey (SDSS)</strong> é um dos maiores levantamentos astronômicos
              já realizados, iniciado em 2000 pelo Apache Point Observatory no Novo México (EUA). Ele catalogou
              centenas de milhões de objetos celestes medindo seu brilho em cinco filtros de cor e calculando
              sua distância via redshift.
            </p>
            <p>
              O dataset usado neste projeto contém <strong>10.000 objetos reais do SDSS</strong>, cada um já
              classificado por astrônomos, que serviram de base para treinar o modelo de Machine Learning.
            </p>
          </div>

          <div className="panel guia-block">
            <span className="eyebrow">Os cinco filtros</span>
            <h2>O que são u, g, r, i, z?</h2>
            <p>
              Cada letra representa um filtro de cor pelo qual o telescópio mede o brilho do objeto.
              Quanto <strong>menor o número</strong>, mais brilhante o objeto naquela faixa.
            </p>
            <div className="filtros-grid">
              {[
                { letra: "u", nome: "Ultravioleta", nm: "~355 nm", desc: "Detecta objetos muito quentes, como estrelas jovens e quasares com emissão UV intensa." },
                { letra: "g", nome: "Verde/azul", nm: "~469 nm", desc: "Luz visível azul-esverdeada. Boa para diferenciar tipos de estrelas pela temperatura." },
                { letra: "r", nome: "Vermelho", nm: "~617 nm", desc: "Luz visível vermelha. Estrelas frias emitem proporcionalmente mais nessa faixa." },
                { letra: "i", nome: "Infravermelho próx.", nm: "~748 nm", desc: "Penetra poeira interestelar. Revela objetos em regiões de formação estelar." },
                { letra: "z", nome: "Infravermelho", nm: "~893 nm", desc: "Faixa mais longa. Útil para objetos muito distantes com brilho deslocado pelo redshift." },
              ].map((f) => (
                <div key={f.letra} className="filtro-card panel">
                  <div className="filtro-letra">{f.letra}</div>
                  <div className="filtro-info">
                    <strong>{f.nome}</strong>
                    <span className="filtro-nm">{f.nm}</span>
                    <p>{f.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="panel guia-block">
            <span className="eyebrow">Distância cósmica</span>
            <h2>O que é redshift?</h2>
            <p>
              Redshift mede o quanto a luz de um objeto foi "esticada" enquanto viajava pelo universo em expansão.
              Quanto mais distante o objeto, maior o redshift.
            </p>
            <div className="redshift-escala">
              <div className="rs-item">
                <span className="rs-val">~0</span>
                <span className="rs-label">Estrela (Via Láctea)</span>
              </div>
              <div className="rs-arrow">→</div>
              <div className="rs-item">
                <span className="rs-val">0.05–0.5</span>
                <span className="rs-label">Galáxia próxima/média</span>
              </div>
              <div className="rs-arrow">→</div>
              <div className="rs-item">
                <span className="rs-val">&gt; 0.5</span>
                <span className="rs-label">Quasar distante</span>
              </div>
            </div>
          </div>

          <div className="panel guia-block">
            <span className="eyebrow">Como pesquisar</span>
            <h2>Encontrando objetos reais</h2>
            <p>
              Acesse o{" "}
              <a href="https://skyserver.sdss.org/dr18/SearchTools/IQS" target="_blank" rel="noreferrer">
                SDSS SkyServer Image Query
              </a>{" "}
              e busque por coordenadas ou nome de objetos. Na ficha do objeto, procure pela tabela{" "}
              <code>PhotoObj</code> para as magnitudes e <code>specObj</code> para o redshift.
            </p>
          </div>
        </div>
      )}

      {/* ABA TREINO */}
      {aba === "treino" && (
        <div className="treino-content">
          <p className="lede">
            Tente adivinhar a classe de cada objeto antes de revelar a resposta.
            Depois, clique em "Testar no classificador" para comparar com o modelo.
          </p>
          {QUIZ.map((q) => {
            const revelado = revelados[q.id];
            const chute = chutes[q.id];
            const acertou = chute === q.resposta;

            return (
              <div key={q.id} className="panel quiz-card">
                <span className="eyebrow">Objeto {q.id}</span>
                <p className="quiz-desc">{q.descricao}</p>

                <div className="quiz-valores">
                  {Object.entries(q.valores).map(([k, v]) => (
                    <div key={k} className="quiz-val">
                      <span className="quiz-key">{k}</span>
                      <span className="quiz-num">{v}</span>
                    </div>
                  ))}
                </div>

                {!chute && (
                  <div className="quiz-chute-btns">
                    <p style={{ color: "var(--text-dim)", fontSize: "0.88rem", marginBottom: 10 }}>
                      Qual é a sua resposta?
                    </p>
                    {["STAR", "GALAXY", "QSO"].map((c) => (
                      <button key={c} className="quiz-chute-btn" onClick={() => chutar(q.id, c)}>
                        {c}
                      </button>
                    ))}
                  </div>
                )}

                {chute && !revelado && (
                  <div className="quiz-resultado-chute">
                    <p>Sua resposta: <strong>{chute}</strong></p>
                    <button className="quiz-revelar-btn" onClick={() => revelar(q.id)}>
                      Revelar resposta
                    </button>
                  </div>
                )}

                {revelado && (
                  <div className={`quiz-gabarito ${acertou ? "quiz-gabarito--acerto" : "quiz-gabarito--erro"}`}>
                    <p>{acertou ? "Acertou!" : "Errou!"} A resposta é <strong>{q.resposta}</strong></p>
                    <p className="quiz-dica">{q.dica}</p>
                    <button className="quiz-testar-btn" onClick={() => preencherClassificador(q.valores)}>
                      Testar no classificador
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* ABA CADERNETA */}
      {aba === "caderneta" && (
        <div className="caderneta-content">
          <p className="lede">Histórico automático das classificações feitas nesta sessão.</p>
          {caderneta.length === 0 ? (
            <div className="panel caderneta-vazia">
              <p>Nenhuma classificação ainda. Vá para a aba Classificar e faça sua primeira consulta.</p>
            </div>
          ) : (
            <>
              <button className="caderneta-limpar" onClick={() => setCaderneta([])}>
                Limpar histórico
              </button>
              <div className="caderneta-lista">
                {caderneta.map((item) => (
                  <div key={item.id} className="panel caderneta-item">
                    <div className="caderneta-header">
                      <span className={`caderneta-classe caderneta-classe--${item.classe.toLowerCase()}`}>
                        {item.classe}
                      </span>
                      <span className="caderneta-data">{item.data}</span>
                      <span className="caderneta-conf">{item.prob.toFixed(1)}% confiança</span>
                    </div>
                    <div className="caderneta-vals">
                      {Object.entries(item.valores).map(([k, v]) => (
                        <span key={k} className="caderneta-val">
                          <strong>{k}</strong> {v}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}