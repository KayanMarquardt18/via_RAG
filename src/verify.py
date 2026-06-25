import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)

colecoes = client.list_collections()
print("Coleções existentes:", colecoes)