import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="page home-page">

      <section className="hero">
        <span className="eyebrow">via_RAG · observatório de dados</span>
        <h1 className="hero-title">
          Duas formas de IA, <br />
          conhecimento e análise juntos.
        </h1>
        <p className="hero-lede">
          Um lado entende perguntas em português sobre astronomia. O outro,
          reconhece padrões em luz e distância para classificar objetos reais
          do catálogo SDSS.
        </p>

        <div className="hero-actions">
          <Link to="/knowledge" className="btn btn-primary">
            Perguntar sobre o cosmos
          </Link>
          <Link to="/predictor" className="btn btn-ghost">
            Classificar um objeto
          </Link>
        </div>
      </section>

      <section className="hero-grid">
        <div className="panel hero-card">
          <span className="eyebrow">Conhecimento</span>
          <h3>Busca semântica + geração</h3>
          <p>
            +20 textos sobre estrelas, galáxias, buracos negros e
            relatividade, vetorizados num banco de dados e consultados por um
            modelo de linguagem rodando localmente.
          </p>
        </div>
        <div className="panel hero-card">
          <span className="eyebrow">Classificador</span>
          <h3>Random Forest sobre dados reais</h3>
          <p>
            10.000 objetos do Sloan Digital Sky Survey treinaram um modelo que
            reconhece estrelas, galáxias e quasares a partir de magnitudes e
            redshift.
          </p>
        </div>
      </section>

    </div>
  );
}