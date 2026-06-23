import json

# ----------------------------
# 1. CARREGAR DADOS
# ----------------------------
def carregar_dados():
    with open('data/black_holes.json', 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


# ----------------------------
# 2. MOSTRAR CATÁLOGO
# ----------------------------
def mostrar_catalogo(buracos_negros):
    print("\n🌌 BURACOS NEGROS DISPONÍVEIS PARA PESQUISA:\n")

    for bh in buracos_negros:
        print(f"- {bh['nome']}")


# ----------------------------
# 3. BUSCAR OBJETO
# ----------------------------
def buscar_buraco_negro(buracos_negros, nome):
    for bh in buracos_negros:
        if bh['nome'].lower() == nome.lower():
            return bh
    return None


# ----------------------------
# 4. MOSTRAR DETALHES
# ----------------------------
def mostrar_detalhes(bh):
    print("\n📡 DETALHES DO BURACO NEGRO\n")
    print(f"Nome: {bh['nome']}")
    print(f"Tipo: {bh['tipo']}")
    print(f"Galáxia: {bh['galaxia']}")
    print(f"Massa (milhões de massas solares): {bh['massa_milhoes_solares']}")
    print(f"Distância (anos-luz): {bh['distancia_anos_luz']}")
    print(f"Descrição: {bh['descricao']}")


# ----------------------------
# 5. PROGRAMA PRINCIPAL
# ----------------------------
def main():
    buracos_negros = carregar_dados()

    mostrar_catalogo(buracos_negros)

    print("\nOlá! Qual buraco negro você quer saber mais informações?")
    info = input("Digite o nome: ")

    resultado = buscar_buraco_negro(buracos_negros, info)

    if resultado:
        mostrar_detalhes(resultado)
    else:
        print("\n❌ Buraco negro não encontrado.")


# ----------------------------
# 6. EXECUÇÃO
# ----------------------------
if __name__ == "__main__":
    main()