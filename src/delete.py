import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)

# Apaga a coleção inteira (todos os chunks, embeddings e metadados)
client.delete_collection("nasa_docs")

print("Coleção 'nasa_docs' apagada.")