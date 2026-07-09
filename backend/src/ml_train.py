import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# =========================================
# 1. CARREGAMENTO DO DATASET
# =========================================

DATASET_PATH = Path("data/galaxydt.csv")

def load_data(path: Path) -> pd.DataFrame:
    print("Carregando dataset...")
    df = pd.read_csv(path)
    print(f"Dataset carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df


# =========================================
# 2. PREPARAÇÃO DOS DADOS
# =========================================

def prepare_data(df: pd.DataFrame):
    features = ["u", "g", "r", "i", "z", "redshift"]

    X = df[features]
    y = df["class"]

    print("\nDistribuição das classes:")
    print(y.value_counts())

    return X, y


# =========================================
# 3. SPLIT TREINO / TESTE
# =========================================

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\nSplit concluído:")
    print(f"Treino: {X_train.shape[0]} amostras")
    print(f"Teste: {X_test.shape[0]} amostras")

    return X_train, X_test, y_train, y_test


# =========================================
# 4. TREINAMENTO DO MODELO
# =========================================

def train_model(X_train, y_train):
    print("\nTreinando modelo Random Forest...")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("Modelo treinado com sucesso!")
    return model


# =========================================
# 5. AVALIAÇÃO
# =========================================

def evaluate_model(model, X_test, y_test):
    print("\nAvaliando modelo...")

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


# =========================================
# 6. SALVAR MODELO
# =========================================

def save_model(model, path="models/galaxy_model.pkl"):
    Path("models").mkdir(exist_ok=True)

    joblib.dump(model, path)
    print(f"\nModelo salvo em: {path}")


# =========================================
# MAIN
# =========================================

def main():
    df = load_data(DATASET_PATH)

    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = split_data(X, y)

    model = train_model(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    save_model(model)


if __name__ == "__main__":
    main()