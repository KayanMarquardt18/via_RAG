import os
import requests
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

load_dotenv()  # lê o arquivo .env e carrega as variáveis

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/pipeline/feature-extraction"


def encode(texto):
    """
    Gera o embedding de um texto usando a API de Inference da Hugging Face,
    em vez de carregar o modelo localmente (economiza memória em produção).
    """
    response = requests.post(
        HF_MODEL_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": texto, "options": {"wait_for_model": True}}
    )
    response.raise_for_status()
    return response.json()


print("Conectando ao ChromaDB...")
chroma_client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "localhost"),
    port=int(os.getenv("CHROMA_PORT", "8000"))
)
collection = chroma_client.get_collection("nasa_docs")

llm_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
# Conecta na Groq como se fosse a API da OpenAI,
# só trocando a base_url e a api_key.


def buscar_contexto(pergunta, n_results=3):
    embedding_pergunta = encode(pergunta)
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
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        reasoning_effort="none"
    )
    texto_resposta = resposta.choices[0].message.content
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