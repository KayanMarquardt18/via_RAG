import joblib
import pandas as pd
from pathlib import Path

# =========================================
# 1. CARREGAR MODELO
# =========================================

MODEL_PATH = Path("models/galaxy_model.pkl")

FEATURES = ["u", "g", "r", "i", "z", "redshift"]

def load_model(path):
    print("Carregando modelo...")
    model = joblib.load(path)
    print("Modelo carregado com sucesso!")
    return model


# =========================================
# 2. PREPARAR INPUT (CORRIGIDO)
# =========================================

def prepare_input(values):
    """
    values: lista com [u, g, r, i, z, redshift]
    """

    if len(values) != len(FEATURES):
        raise ValueError(f"Esperado {len(FEATURES)} valores: {FEATURES}")

    df = pd.DataFrame([values], columns=FEATURES)
    return df


# =========================================
# 3. PREVISÃO
# =========================================

def predict(model, input_df):
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    return prediction, probabilities


# =========================================
# 4. MOSTRAR RESULTADO
# =========================================

def show_result(model, prediction, probabilities):
    print("\n=================================")
    print("RESULTADO DA PREVISÃO")
    print("=================================")

    print(f"Classe prevista: {prediction}")

    print("\nProbabilidades:")

    for cls, prob in zip(model.classes_, probabilities):
        print(f"{cls}: {prob:.4f}")


# =========================================
# 5. MAIN
# =========================================

def main():
    model = load_model(MODEL_PATH)

    # EXEMPLO (tu pode trocar livremente)
    sample = [18.1, 17.2, 16.8, 16.5, 16.3, 0.45]

    input_df = prepare_input(sample)

    prediction, probs = predict(model, input_df)

    show_result(model, prediction, probs)


# =========================================
# EXECUÇÃO
# =========================================

if __name__ == "__main__":
    main()
    