import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)

collection = client.get_collection("nasa_docs")

result = collection.get()

ids = result["ids"]

print("Total de chunks:", len(ids))
print("IDs únicos:", len(set(ids)))

if len(ids) != len(set(ids)):
    print("⚠️ DUPLICAÇÃO DETECTADA")
else:
    print("✔ Sem duplicação")