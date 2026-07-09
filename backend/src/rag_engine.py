from src.generate import buscar_contexto, llm_client


def get_rag_explanation(class_name):
    pergunta = f"O que é um objeto do tipo {class_name} na astronomia?"
    return _consultar_rag(pergunta, historico=[])


def ask_knowledge(pergunta_usuario, historico=None):
    return _consultar_rag(pergunta_usuario, historico=historico or [])


def _consultar_rag(pergunta, historico):
    # Se a pergunta for curta e houver histórico, enriquece a query
    # combinando com a última pergunta do usuário
    query_busca = pergunta
    if historico and len(pergunta.split()) <= 6:
        ultima_pergunta = next(
            (m["texto"] for m in reversed(historico) if m["autor"] == "user"),
            None
        )
        if ultima_pergunta:
            query_busca = f"{ultima_pergunta} {pergunta}"

    chunks, _ = buscar_contexto(query_busca)
    contexto = "\n\n---\n\n".join(chunks)

    primeira_mensagem = f"""Você é um assistente de astronomia. Responda APENAS com base no contexto abaixo.
Se não encontrar a informação, diga claramente. Nunca invente.

CONTEXTO:
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
    # instrução + contexto juntos na primeira mensagem do user
    primeira_mensagem = f"""Você é um assistente de astronomia. Responda APENAS com base no contexto abaixo.
Se não encontrar a informação, diga claramente. Nunca invente.

CONTEXTO:
{contexto}

PERGUNTA: {pergunta}"""

    # se não tem histórico, manda só a pergunta com contexto
    if not historico:
        mensagens = [{"role": "user", "content": primeira_mensagem}]
    else:
        # histórico anterior + nova pergunta com contexto novo
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

    system_prompt = f"""Você é um assistente especializado em astronomia.
Responda usando APENAS as informações do contexto abaixo.

Regras:
1. Se o contexto contiver a resposta, responda de forma clara e completa.
2. Se o contexto NÃO contiver a resposta direta, mas tiver informações relacionadas,
   explique o que encontrou e deixe claro que não é uma resposta exata.
3. Se o contexto não tiver nada relacionado, diga:
   "Não encontrei essa informação na base de dados disponível."
4. Nunca invente informações fora do contexto.
5. Fale de forma envolvente e científica, despertando curiosidade.
6. Respostas concisas, divididas em parágrafos curtos quando necessário.
7. Quando o assunto for amplo, sugira novas perguntas — mas apenas sobre tópicos
   cobertos pelo contexto ou base de conhecimento disponível.

CONTEXTO ASTRONÔMICO:
{contexto}"""

    # Monta as mensagens: system + histórico anterior + pergunta atual
    mensagens = [{"role": "system", "content": system_prompt}]

    for msg in historico:
        mensagens.append({"role": msg["autor"], "content": msg["texto"]})

    mensagens.append({"role": "user", "content": pergunta})

    resposta = llm_client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=mensagens,
        temperature=0.3
    )

    return resposta.choices[0].message.content