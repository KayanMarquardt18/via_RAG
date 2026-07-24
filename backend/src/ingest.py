from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

print("Carregando modelo de embeddings...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

client = chromadb.HttpClient(
    host="chroma-production-45c8.up.railway.app",
    port=443,
    ssl=True
)

collection = client.get_or_create_collection(
    name="nasa_docs"
)

DATA_FOLDER = Path("data/docs")

total_chunks = 0

for arquivo in DATA_FOLDER.glob("*.txt"):

    print(f"\nProcessando: {arquivo.name}")

    with open(arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    chunks = texto.split("--------------------------------------------------")

    for i, chunk in enumerate(chunks):

        chunk = chunk.strip()

        if len(chunk) < 50:
            continue

        embedding = model.encode(chunk).tolist()

        chunk_id = f"{arquivo.stem}_{i}"

        collection.upsert(
            ids=[chunk_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source": arquivo.name
            }]
        )

        total_chunks += 1

print("\n================================")
print(f"Chunks processados: {total_chunks}")
print("================================")