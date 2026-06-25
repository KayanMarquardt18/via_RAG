import pandas as pd

df = pd.read_csv("data/galaxydt.csv")

print("✔ CSV carregado com sucesso")
print("Linhas:", len(df))
print("\nPreview:")
print(df.head())