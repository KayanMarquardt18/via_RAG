from src.generate import buscar_contexto, llm_client


def get_rag_explanation(class_name, valores=None):
    """
    Gera uma explicação para o resultado de uma predição do classificador ML.
    Diferente do chat geral: aqui já sabemos a resposta (veio do modelo),
    então o LLM nunca deve recusar — só conectar os dados ao contexto.
    """
    query_busca = f"características de {class_name.lower()} magnitudes fotometria redshift"
    chunks, _ = buscar_contexto(query_busca)
    contexto = "\n\n---\n\n".join(chunks)

    valores_txt = ""
    if valores:
        valores_txt = f"\nValores fotométricos do objeto: {valores}\n"

    prompt = f"""Você é ViaBot, um assistente de astronomia batendo um papo casual sobre o resultado
de um classificador de Machine Learning.

Um modelo já analisou os dados fotométricos de um objeto e concluiu que ele é do tipo: {class_name}
{valores_txt}
Use as informações abaixo para explicar de forma natural e conversada por que um objeto com essas
características costuma ser classificado como {class_name}.

Regras:
1. Nunca cite "o contexto" ou "as informações fornecidas" — fale como se você já soubesse,
   sem mencionar de onde veio o conhecimento.
2. Nunca diga que não existe a inform. Sempre construa uma explicação, conectando
   os conceitos disponíveis com a classificação {class_name}, mesmo que não haja um termo técnico exato, porém nunca invente fatos ou números que não estejam no contexto, apenas leve o usuário a pesquisar por outros temas que você possui.
3. Se houver valores fotométricos, relacione-os com a explicação de forma natural.
4. Fale como quem está contando algo interessante pra um amigo curioso — tom leve, envolvente,
   frases curtas. Nada de linguagem de relatório.
5. Seja conciso: 2 a 4 frases, direto ao ponto.

INFORMAÇÕES DISPONÍVEIS:
{contexto}

EXPLICAÇÃO:"""

    resposta = llm_client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return resposta.choices[0].message.content


def ask_knowledge(pergunta_usuario, historico=None):
    return _consultar_rag(pergunta_usuario, historico=historico or [])


def _consultar_rag(pergunta, historico):
    query_busca = pergunta

    PALAVRAS_REFERENCIA = {
        "esse", "essa", "esses", "essas", "isso", "disso", "dele", "dela",
        "deles", "delas", "ele", "ela", "nele", "nela", "aí", "então"
    }

    palavras_pergunta = set(pergunta.lower().replace("?", "").split())
    parece_continuacao = bool(palavras_pergunta & PALAVRAS_REFERENCIA)

    if historico and parece_continuacao:
        ultima_pergunta = next(
            (m["texto"] for m in reversed(historico) if m["autor"] == "user"),
            None
        )
        if ultima_pergunta:
            query_busca = f"{ultima_pergunta} {pergunta}"

    chunks, _ = buscar_contexto(query_busca)
    contexto = "\n\n---\n\n".join(chunks)

    apresentacao = ""
    if not historico:
        apresentacao = """Essa é a primeira mensagem da conversa. Comece se apresentando rapidamente
como ViaBot, um assistente de astronomia — só uma frase curta e simpática, tipo "Oi, eu sou o ViaBot!" —
e emende direto na resposta da pergunta, sem enrolar.

"""

    primeira_mensagem = f"""Você é ViaBot, um assistente de astronomia batendo papo com alguém curioso
sobre o universo. Responda com base nas informações abaixo, mas de forma natural e conversada —
como se estivesse explicando pra um amigo, não escrevendo um relatório.

{apresentacao}Regras:
Regras:
1. Nunca cite "o contexto" ou "as informações fornecidas" — fale a informação diretamente,
   como se você já soubesse, sem mencionar de onde veio.
2. Baseie sua resposta ESTRITAMENTE nas informações disponíveis abaixo. Não adicione fatos,
   números, datas ou detalhes que não estejam explicitamente ali, mesmo que pareçam plausíveis.
3. Se a informação disponível não cobrir a pergunta, diga isso de forma simples e direta, tipo
   "Essa eu não sei te dizer com certeza" — nunca complete a lacuna com conhecimento próprio.
4. Use frases curtas e diretas, tom leve e curioso — pode soltar a linguagem um pouco,
   sem perder precisão científica.
5. Continue naturalmente a conversa, sem repetir estruturas formais a cada resposta.
INFORMAÇÕES DISPONÍVEIS:
{contexto}

PERGUNTA: {pergunta}"""

    if not historico:
        mensagens = [{"role": "user", "content": primeira_mensagem}]
    else:
        mensagens = []
        for msg in historico:
            role = "assistant" if msg["autor"] == "ia" else "user"
            mensagens.append({"role": role, "content": msg["texto"]})
        mensagens.append({"role": "user", "content": primeira_mensagem})

    resposta = llm_client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=mensagens,
        temperature=0.3
    )

    return resposta.choices[0].message.content