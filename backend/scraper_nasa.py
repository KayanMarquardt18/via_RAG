"""
Scraper robusto para extração de conteúdo da NASA (Black Holes) voltado para RAG.

Melhorias em relação à versão original:
- Tratamento de erros de rede (timeout, status code, exceções de conexão)
- Extração de mais elementos relevantes (parágrafos, listas, títulos)
- Filtro de "lixo" mais seguro (baseado em estrutura/posição, não em palavras-chave soltas)
- Chunking com overlap (melhora recuperação semântica em RAG)
- Saída em JSON (estruturado, com metadados) + TXT (legível por humanos)
- Logging informativo de cada etapa
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import json
import time
from datetime import datetime, timezone


URL = "https://science.nasa.gov/universe/black-holes/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# =====================================================
# 1. REQUISIÇÃO HTTP COM RETRY
# =====================================================
def buscar_html(url, tentativas=3, timeout=15):
    """Busca o HTML da página com retry e tratamento de erros."""
    ultimo_erro = None

    for tentativa in range(1, tentativas + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            return r.text
        except requests.exceptions.RequestException as e:
            ultimo_erro = e
            print(f"⚠️  Tentativa {tentativa}/{tentativas} falhou: {e}")
            if tentativa < tentativas:
                time.sleep(2 * tentativa)  # backoff progressivo

    raise RuntimeError(f"Não foi possível acessar {url}. Último erro: {ultimo_erro}")


# =====================================================
# 2. LIMPEZA DE TEXTO
# =====================================================
# Linhas que costumam ser puro "boilerplate" de navegação/rodapé,
# usadas como texto EXATO (não substring), para não descartar
# parágrafos legítimos que apenas mencionam essas palavras.
LIXO_EXATO = {
    "nasa", "universe", "stars", "galaxies", "exoplanets",
    "explore", "about", "home", "share", "related",
    "follow", "read more", "search", "menu", "skip to main content",
}


def limpar_texto(t, min_chars=40):
    if not t:
        return None

    t = re.sub(r'\s+', ' ', t).strip()

    if len(t) < min_chars:
        return None

    # Só descarta se o texto INTEIRO (normalizado) for boilerplate,
    # não se a palavra aparecer dentro de uma frase maior.
    if t.lower().strip(" .") in LIXO_EXATO:
        return None

    return t


# =====================================================
# 3. EXTRAÇÃO DE CONTEÚDO
# =====================================================
def extrair_conteudo(html):
    """
    Extrai parágrafos, itens de lista e títulos do corpo principal.
    Retorna lista de dicts: {"tipo": "paragrafo"|"item_lista"|"titulo", "texto": str}
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove elementos que quase nunca têm conteúdo útil para RAG
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "form", "button"]):
        tag.decompose()

    # Tenta focar no conteúdo principal, se existir uma tag <main> ou <article>
    container = soup.find("main") or soup.find("article") or soup

    elementos = []
    seen = set()

    for tag in container.find_all(["p", "li", "h1", "h2", "h3"]):
        bruto = tag.get_text(separator=" ", strip=True)
        texto = limpar_texto(bruto)

        if not texto or texto in seen:
            continue

        seen.add(texto)

        if tag.name in ("h1", "h2", "h3"):
            tipo = "titulo"
        elif tag.name == "li":
            tipo = "item_lista"
        else:
            tipo = "paragrafo"

        elementos.append({"tipo": tipo, "texto": texto})

    return elementos


# =====================================================
# 4. CHUNKING COM OVERLAP
# =====================================================
def criar_chunks(elementos, max_chars=900, min_chars=200, overlap_chars=150):
    """
    Agrupa elementos em chunks coerentes, com overlap entre chunks
    consecutivos para preservar contexto nas bordas (importante para RAG).
    """
    if not elementos:
        return []

    chunks = []
    atual = ""
    fontes_atual = []  # guarda quais tipos de elemento compõem o chunk

    def fechar_chunk():
        nonlocal atual, fontes_atual
        texto_final = atual.strip()
        if len(texto_final) >= min_chars:
            chunks.append({
                "texto": texto_final,
                "tem_titulo": "titulo" in fontes_atual,
                "n_elementos": len(fontes_atual),
            })

    for el in elementos:
        texto = el["texto"]

        if len(texto) < 15:
            continue

        candidato = (atual + " " + texto).strip() if atual else texto

        if len(candidato) <= max_chars:
            atual = candidato
            fontes_atual.append(el["tipo"])
        else:
            fechar_chunk()

            # overlap: pega o final do chunk anterior para iniciar o próximo
            overlap = atual[-overlap_chars:] if len(atual) > overlap_chars else atual
            atual = (overlap + " " + texto).strip()
            fontes_atual = [el["tipo"]]

    fechar_chunk()

    return chunks


# =====================================================
# 5. SALVAR DATASET (JSON + TXT)
# =====================================================
def salvar_dataset(chunks, nome_base, url_origem, saida_dir="data/docs"):
    os.makedirs(saida_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()

    # --- JSON estruturado (ideal para indexar em RAG) ---
    registros = []
    for i, c in enumerate(chunks):
        registros.append({
            "id": f"{nome_base}_{i+1:04d}",
            "source_url": url_origem,
            "scraped_at": timestamp,
            "chunk_index": i + 1,
            "total_chunks": len(chunks),
            "char_count": len(c["texto"]),
            "has_title_context": c["tem_titulo"],
            "text": c["texto"],
        })

    caminho_json = os.path.join(saida_dir, f"{nome_base}.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

    # --- TXT legível (útil para revisão humana) ---
    caminho_txt = os.path.join(saida_dir, f"{nome_base}.txt")
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("NASA DATASET - BLACK HOLES (CLEAN RAG FORMAT)\n")
        f.write(f"Fonte: {url_origem}\n")
        f.write(f"Coletado em: {timestamp}\n")
        f.write("=" * 60 + "\n\n")

        for reg in registros:
            f.write(f"\n[CHUNK {reg['chunk_index']}/{reg['total_chunks']}] ")
            f.write(f"(id={reg['id']}, chars={reg['char_count']})\n")
            f.write("-" * 50 + "\n")
            f.write(reg["text"] + "\n")
            f.write("-" * 50 + "\n")

    print(f"✅ Dataset salvo em:\n   - {caminho_json}\n   - {caminho_txt}")
    print(f"📦 Total de chunks: {len(chunks)}")

    return caminho_json, caminho_txt


# =====================================================
# 6. PIPELINE PRINCIPAL
# =====================================================
def main():
    print(f"🌐 Buscando conteúdo de: {URL}")
    html = buscar_html(URL)

    print("🧹 Extraindo e limpando conteúdo...")
    elementos = extrair_conteudo(html)
    print(f"   {len(elementos)} elementos de texto extraídos.")

    if not elementos:
        print("⚠️  Nenhum conteúdo extraído. Verifique se o site mudou de estrutura "
              "ou se o acesso está sendo bloqueado.")
        return

    print("✂️  Criando chunks (com overlap)...")
    chunks = criar_chunks(elementos)

    if not chunks:
        print("⚠️  Nenhum chunk válido foi gerado (conteúdo insuficiente).")
        return

    salvar_dataset(chunks, "nasa_black_holes_clean", URL)


if __name__ == "__main__":
    main()