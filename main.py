import pandas as pd
import matplotlib.pyplot as plt

# =============== Carrega os Dados do Kaggle ===============
df = pd.read_csv("Space_Corrected.csv")

# =============== Nomeando as Colunas do .CSV ===============
df = df.rename(columns={" Rocket": "Rocket"})
df["Rocket"] = pd.to_numeric(df["Rocket"], errors="coerce")
df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce", utc=True)
df["Year"] = df["Datum"].dt.year

# =============== Ano de lançamento do Foguete ===============
freq_year = df["Year"].dropna().astype(int).value_counts().sort_index().reset_index()
freq_year.columns = ["Ano", "Frequencia"]
freq_year["Frequencia_Relativa_%"] = (freq_year["Frequencia"] / freq_year["Frequencia"].sum() * 100).round(2)
freq_year["Frequencia_Acumulada"] = freq_year["Frequencia"].cumsum()

# =============== Custo dos Foguetes ===============
classes = pd.cut(df["Rocket"].dropna(), bins=8)
freq_rocket = classes.value_counts().sort_index().reset_index()
freq_rocket.columns = ["Classe_Rocket_USD_mi", "Frequencia"]
freq_rocket["Frequencia_Relativa_%"] = (freq_rocket["Frequencia"] / freq_rocket["Frequencia"].sum() * 100).round(2)
freq_rocket["Frequencia_Acumulada"] = freq_rocket["Frequencia"].cumsum()
freq_rocket["Classe_Rocket_USD_mi"] = freq_rocket["Classe_Rocket_USD_mi"].astype(str)

# =============== Grafico de lançamento de Foguete Por Ano ===============

plt.figure(figsize=(10, 5))
plt.plot(freq_year["Ano"], freq_year["Frequencia"], marker="o", color="blue", label="Lançamentos")
plt.title("Quantidade de Lançamentos por Ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("grafico_lancamentos_por_ano.png", dpi=150)
plt.close()


# =============== Custo de Cada Foguete ===============
plt.figure(figsize=(10, 5))
plt.hist(df["Rocket"].dropna(), bins=15, color="orange", edgecolor="black", label="Custo")
plt.title("Distribuição do Custo dos Foguetes (USD milhões)")
plt.xlabel("Custo do Foguete (USD milhões)")
plt.ylabel("Frequência")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_distribuicao_custo_foguete.png", dpi=150)
plt.close()

# =============== Analise Variada ===============
def resumo_estatistico(serie, nome):
    s = serie.dropna()
    moda = s.mode().iloc[0] if not s.mode().empty else None
    return {
        "Variavel": nome,
        "Media": s.mean(),
        "Mediana": s.median(),
        "Moda": moda,
        "Maximo": s.max(),
        "Minimo": s.min(),
        "Amplitude": s.max() - s.min(),
        "Variancia": s.var(),
        "Desvio_Padrao": s.std(),
        "Q1": s.quantile(0.25),
        "Q2": s.quantile(0.50),
        "Q3": s.quantile(0.75),
    }


estat_year = resumo_estatistico(df["Year"], "Year")
estat_rocket = resumo_estatistico(df["Rocket"], "Rocket")

estatisticas = pd.DataFrame([estat_year, estat_rocket]).round(4)

# =============== Sprint ===============
print("\nBASE ESCOLHIDA:")

print("TABELA DE FREQUÊNCIA - VARIÁVEL DISCRETA (Year):")
print(freq_year.to_string(index=False))

print("\nTABELA DE FREQUÊNCIA - VARIÁVEL CONTÍNUA (Rocket):")
print(freq_rocket.to_string(index=False))

print("\nESTATÍSTICA DESCRITIVA (Year e Rocket):")
print(estatisticas.to_string(index=False))

print("\nInterpretação rápida:")
print(f"- Year: média={estat_year['Media']:.2f}, mediana={estat_year['Mediana']:.2f}, moda={estat_year['Moda']:.2f}")
print(f"- Rocket: média={estat_rocket['Media']:.2f}, mediana={estat_rocket['Mediana']:.2f}, desvio padrão={estat_rocket['Desvio_Padrao']:.2f}")
print("- Conclusão: há grande variação nos custos dos foguetes.")

print("\nPronto! Valores exibidos no Run.")
