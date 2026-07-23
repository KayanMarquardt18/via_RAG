from src.generate import buscar_contexto

if __name__ == "__main__":
    pergunta = "o que é buraco negro"
    docs, meta = buscar_contexto(pergunta)
    print(f"\nPergunta: {pergunta}\n")
    for i, (doc, m) in enumerate(zip(docs, meta)):
        print(f"--- Chunk {i+1} (fonte: {m['source']}) ---")
        print(doc[:200], "...\n")