import pandas as pd
from pathlib import Path

print("Carregando dataset...")

DATASET = Path("data/galaxydt.csv")

df = pd.read_csv(DATASET)

print("\n========================================")
print("DATASET CARREGADO")
print("========================================")

print(f"\nLinhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")

print("\nColunas:")
print(df.columns.tolist())

print("\n========================================")
print("PRIMEIRAS 5 LINHAS")
print("========================================")

print(df.head())

print("\n========================================")
print("TIPOS DAS COLUNAS")
print("========================================")

print(df.dtypes)

print("\n========================================")
print("VALORES NULOS")
print("========================================")

print(df.isnull().sum())

print("\n========================================")
print("DISTRIBUIÇÃO DAS CLASSES")
print("========================================")

print(df["class"].value_counts())

print("\n========================================")
print("ESTATÍSTICAS NUMÉRICAS")
print("========================================")

print(df.describe())