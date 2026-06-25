import chromadb

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

    resultado = collection.query(
        query_texts=[pergunta],
        n_results=3
    )

    print("\nRESULTADOS:\n")

    for doc in resultado["documents"][0]:
        print(doc)
        print("\n" + "=" * 50 + "\n")