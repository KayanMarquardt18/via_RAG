import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

print("Carregando modelo multilíngue...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_collection("nasa_docs")

# Pega os documentos (texto puro) do agn.txt -- não usamos os embeddings
# salvos no Chroma, porque esses foram gerados com o modelo antigo.
# Vamos gerar embeddings NOVOS, na hora, só pra esse teste.
dados = collection.get(
    where={"source": "agn.txt"},
    include=["documents"]
)

pergunta = "o que são AGN?"
embedding_pergunta = model.encode(pergunta)

resultados = []

for doc in dados["documents"]:
    embedding_doc = model.encode(doc)

    distancia = np.linalg.norm(embedding_pergunta - embedding_doc)

    primeira_linha = doc.strip().split("\n")[0]
    resultados.append((distancia, primeira_linha))

resultados.sort(key=lambda x: x[0])

print(f"\nRanking (modelo multilíngue) para: '{pergunta}'\n")
for posicao, (distancia, identificador) in enumerate(resultados, start=1):
    print(f"{posicao}º lugar | distância: {distancia:.4f} | {identificador}")