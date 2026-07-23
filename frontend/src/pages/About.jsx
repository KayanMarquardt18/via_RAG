export default function About() {
  return (
    <div className="page about-page">

      <section className="about-hero">
        <span className="eyebrow">Sobre o projeto</span>
        <h1>ViaRAG</h1>
        <p className="about-lede">
          Um sistema híbrido de astronomia, construído para aprender — na prática —
          como busca semântica, geração de linguagem e aprendizado de máquina
          funcionam por dentro.
        </p>
      </section>

      <section className="panel about-block">
        <span className="eyebrow">O criador</span>
        <h2>Kayan Marquardt</h2>
        <p>
          Sou do Rio Grande do Sul, trabalho com Análise de Dados e Customer
          Success, e curso Ciência de Dados. O ViaRAG nasceu de uma curiosidade
          simples: entender de verdade como sistemas de IA funcionam por dentro,
          em vez de só usá-los prontos.
        </p>
        <p>
          Escolhi astronomia como tema porque é um assunto que me fascina e
          porque dados científicos têm qualidade e estrutura ótimas para testar
          recuperação de informação e classificação — dois pilares deste projeto.
        </p>
        <div className="about-links">
          <a href="https://github.com/KayanMarquardt18/via_RAG" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a href="https://www.linkedin.com/in/kayan-marquardt-806a87305/" target="_blank" rel="noreferrer">
            LinkedIn
          </a>
        </div>
      </section>

      <section className="panel about-block">
        <span className="eyebrow">Como funciona — RAG</span>
        <h2>O que é a aba Conhecimento</h2>
        <p>
          RAG significa <em>Retrieval-Augmented Generation</em> — geração de
          texto aumentada por busca. Funciona em três etapas:
        </p>
        <ol className="about-steps">
          <li>
            Sua pergunta é transformada em um vetor numérico que representa seu
            significado (um <em>embedding</em>).
          </li>
          <li>
            Esse vetor é comparado a uma base de textos sobre astronomia
            (galáxias, buracos negros, exoplanetas, relatividade e outros temas)
            previamente vetorizada num banco de dados vetorial.
          </li>
          <li>
            Os trechos mais relevantes encontrados são entregues a um modelo de
            linguagem, que escreve a resposta final <strong>com base apenas
            nesses trechos</strong>.
          </li>
        </ol>
        <p>
          Isso significa que a aba Conhecimento só responde bem perguntas sobre
          os temas presentes na base (estrelas, galáxias, buracos negros, AGN,
          exoplanetas, sistema solar, relatividade, matéria escura, ondas
          gravitacionais e correlatos). Perguntas fora desse escopo tendem a
          receber uma resposta honesta de que a informação não foi encontrada,
          em vez de uma resposta inventada.
        </p>
      </section>

      <section className="panel about-block">
        <span className="eyebrow">Como funciona — Machine Learning</span>
        <h2>O que é a aba Classificador</h2>
        <p>
          O Classificador não busca texto — ele reconhece padrões numéricos. Foi
          treinado com um modelo Random Forest sobre 10.000 objetos catalogados
          pelo Sloan Digital Sky Survey (SDSS), cada um já identificado como
          estrela, galáxia ou quasar.
        </p>
        <p>
          A partir de seis números — as magnitudes <code>u, g, r, i, z</code> e o{" "}
          <code>redshift</code> de um objeto — o modelo aprendeu a associar
          combinações desses valores ao tipo de objeto observado, da mesma forma
          que astrônomos usam índices de cor e desvio espectral para classificar
          objetos reais.
        </p>
        <p>
          Diferente do RAG, ele não "sabe" nada sobre o assunto em texto — ele só
          reconhece um padrão estatístico aprendido a partir de exemplos reais, e
          devolve uma probabilidade para cada classe possível.
        </p>
      </section>

      <section className="panel about-block about-block--quiet">
        <span className="eyebrow">Em resumo</span>
        <p>
          RAG responde <strong>perguntas em linguagem natural</strong> dentro de
          um tema coberto pela base de conhecimento. ML classifica{" "}
          <strong>dados numéricos</strong> dentro do que foi observado no
          treinamento. São duas formas diferentes de IA, e este projeto existe
          justamente para mostrar como elas se complementam.
        </p>
      </section>

    </div>
  );
}