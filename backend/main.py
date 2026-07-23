from src.ml_predict import load_model, prepare_input, predict
from src.rag_engine import get_rag_explanation


# =========================================
# 1. CONFIGURAÇÃO DO SISTEMA
# =========================================

MODEL_PATH = "models/galaxy_model.pkl"


# =========================================
# 2. PIPELINE PRINCIPAL
# =========================================

def run_system(model, features):
    """
    Executa o fluxo completo:
    ML → RAG → resposta final
    """

    # 1. preparar entrada
    input_df = prepare_input(features)

    # 2. previsão do modelo
    prediction, probabilities = predict(model, input_df)

    # 3. explicação via RAG
    explanation = get_rag_explanation(prediction, features)

    return prediction, probabilities, explanation


# =========================================
# 3. OUTPUT FORMATADO
# =========================================

def show_result(model, prediction, probabilities, explanation):
    print("\n====================================")
    print("🔭 SISTEMA HÍBRIDO DE ASTRONOMIA")
    print("   (ML + RAG INTEGRADO)")
    print("====================================")

    print(f"\n🧠 Classe prevista: {prediction}")

    print("\n📊 Probabilidades:")

    for cls, prob in zip(model.classes_, probabilities):
        print(f"  {cls}: {prob:.4f}")

    print("\n📚 Explicação (RAG):")
    print(explanation)

    print("\n====================================\n")


# =========================================
# 4. MAIN
# =========================================

def main():
    # carregar modelo ML
    model = load_model(MODEL_PATH)

    print("\nSistema iniciado. Digite valores ou 'sair'.")
    print("Formato: u g r i z redshift\n")

    while True:
        user_input = input("Input: ")

        if user_input.lower() == "sair":
            print("Encerrando sistema...")
            break

        try:
            # converter input string → lista de floats
            features = list(map(float, user_input.split()))

            if len(features) != 6:
                print("❌ Erro: você deve inserir 6 valores.")
                continue

            # rodar sistema completo
            prediction, probs, explanation = run_system(model, features)

            # mostrar resultado
            show_result(model, prediction, probs, explanation)

        except ValueError:
            print("❌ Erro: digite apenas números separados por espaço.")


# =========================================
# EXECUÇÃO
# =========================================

if __name__ == "__main__":
    main()