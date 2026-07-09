import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI

print("Carregando modelo de embeddings...")
embed_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

print("Conectando ao ChromaDB...")
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_collection("nasa_docs")

# Conecta no LM Studio como se fosse a API da OpenAI,
# só trocando a base_url pro nosso servidor local.
llm_client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # qualquer valor funciona aqui, o LM Studio não valida
)


def buscar_contexto(pergunta, n_results=3):
    embedding_pergunta = embed_model.encode(pergunta).tolist()

    resultado = collection.query(
        query_embeddings=[embedding_pergunta],
        n_results=n_results
    )

    documentos = resultado["documents"][0]
    metadados = resultado["metadatas"][0]

    return documentos, metadados


def montar_prompt(pergunta, chunks):
    contexto = "\n\n---\n\n".join(chunks)

    prompt = f"""Você é um assistente especializado em astronomia.
Responda à pergunta do usuário usando APENAS as informações do contexto abaixo.

Regras:
1. Se o contexto contiver a resposta, responda de forma clara e completa.
2. Se o contexto NÃO contiver a resposta direta, mas tiver informações relacionadas,
   explique o que você encontrou de relacionado e deixe claro que não é uma resposta exata.
3. Se o contexto não tiver nada relacionado ao tema da pergunta, diga:
   "Não encontrei essa informação na base de dados disponível."
4. Nunca invente informações que não estejam no contexto.
5. Fale como se estivesse explicando para alguém que não é especialista, mas sem perder a precisão científica.
6. Se apresente como um assistente de astronomia, e não como um modelo de linguagem, fale de maneira intrigante e envolvente, despertando a curiosidade do usuário.
7. Priorize respostas concisas, mas completas. Se a resposta for longa, divida em parágrafos curtos.
8. Quando o assunto for amplo, sugira novas perguntas relacionadas — mas
   APENAS sobre tópicos que você sabe estarem disponíveis no contexto/base
   de dados fornecida (ex: estrutura, classificação, quasares, blazares,
   discos de acreção). Nunca sugira explorar um tópico que não esteja
   coberto pela sua base de conhecimento atual.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

RESPOSTA:"""

    return prompt


def gerar_resposta(pergunta):
    chunks, metadados = buscar_contexto(pergunta)
    prompt = montar_prompt(pergunta, chunks)

    resposta = llm_client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    texto_resposta = resposta.choices[0].message.content

    # Extrai os nomes de arquivo únicos usados como fonte
    fontes = sorted(set(m["source"] for m in metadados))

    return texto_resposta, fontes


if __name__ == "__main__":
    while True:
        pergunta = input("\nPergunta: ")

        if pergunta.lower() == "sair":
            break

        print("\nBuscando contexto e gerando resposta...\n")

        resposta, fontes = gerar_resposta(pergunta)

        print("RESPOSTA:")
        print(resposta)
        print(f"\n📚 Fontes consultadas: {', '.join(fontes)}")