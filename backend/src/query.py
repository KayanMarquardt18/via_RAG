import chromadb
from sentence_transformers import SentenceTransformer

print("Carregando modelo de embeddings...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

print("Conectando ao ChromaDB...")
client = chromadb.HttpClient(
    host="localhost",
    port=8000
)

collection = client.get_collection("nasa_docs")

while True:
    pergunta = input("\nPergunta: ")

    if pergunta.lower() == "sair":
        break

    embedding_pergunta = model.encode(pergunta).tolist()

    resultado = collection.query(
        query_embeddings=[embedding_pergunta],
        n_results=3
    )

    documentos = resultado["documents"][0]
    metadados = resultado["metadatas"][0]
    distancias = resultado["distances"][0]

    print("\nRESULTADOS:\n")

    for i in range(len(documentos)):
        print(f"--- Resultado {i+1} (fonte: {metadados[i]['source']} | distância: {distancias[i]:.4f}) ---")
        print(documentos[i])
        print("\n" + "=" * 50 + "\n")