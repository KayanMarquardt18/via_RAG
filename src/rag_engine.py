from src.generate import buscar_contexto, montar_prompt, llm_client


def get_rag_explanation(class_name):
    """
    Recebe saída do ML e gera explicação científica
    """

    pergunta = f"O que é um objeto do tipo {class_name} na astronomia?"

    chunks, metadados = buscar_contexto(pergunta)

    prompt = montar_prompt(pergunta, chunks)

    resposta = llm_client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return resposta.choices[0].message.content