"""Recria os principais gráficos a partir dos CSVs versionados em outputs/.

Execute na raiz do repositório:
    python scripts/gerar_graficos.py
As imagens novas serão salvas em figures/ como arquivos SVG.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


def ler(caminho):
    return pd.read_csv(OUT / caminho)


def salvar(nome):
    plt.tight_layout()
    plt.savefig(FIG / nome, format="svg", bbox_inches="tight")
    plt.close()
    print("Gráfico salvo:", FIG / nome)


anual = ler("eda/acidentes_por_ano.csv")
plt.figure(figsize=(9, 4.5))
plt.plot(anual["ano"], anual["acidentes"], marker="o")
plt.title("Evolução dos acidentes registrados pela PRF (2020–2025)")
plt.xlabel("Ano")
plt.ylabel("Acidentes")
plt.grid(alpha=0.25)
salvar("01_evolucao_anual.svg")


tipos = ler("eda/tipo_acidente.csv")
tipos = (tipos[tipos["acidentes"] >= 500]
         .sort_values("taxa_grave", ascending=False).head(10)
         .sort_values("taxa_grave"))
plt.figure(figsize=(9, 5))
plt.barh(tipos["tipo_acidente"], tipos["taxa_grave"])
plt.xlabel("Acidentes graves (%)")
plt.title("Proporção de gravidade por tipo de acidente")
salvar("02_tipo_acidente_gravidade.svg")


cramer = ler("estatistica/associacoes_cramers_v.csv")
rotulos = {
    "tipo_acidente": "Tipo de acidente",
    "causa_acidente": "Causa do acidente",
    "br": "Rodovia (BR)",
    "uf": "Unidade da Federação",
    "tipo_pista": "Tipo de pista",
    "fase_dia": "Fase do dia",
    "condicao_metereologica": "Condição meteorológica",
    "uso_solo": "Uso do solo",
    "dia_semana": "Dia da semana",
    "hora": "Hora"
}
cramer = cramer.nlargest(10, "cramers_v").sort_values("cramers_v")
plt.figure(figsize=(9, 5))
plt.barh(cramer["variavel"].map(lambda x: rotulos.get(x, x)), cramer["cramers_v"])
plt.xlabel("V de Cramér corrigido")
plt.title("Associação das variáveis com a classe grave")
salvar("03_cramers_v.svg")


modelos = ler("modelos/comparacao_modelos_balanceados.csv")
colunas = ["recall", "f2", "roc_auc"]
ax = modelos.plot(x="modelo", y=colunas, kind="bar", figsize=(9, 4.5), rot=0)
ax.set_title("Comparação dos modelos na validação de 2024")
ax.set_xlabel("")
ax.set_ylabel("Pontuação")
ax.legend(["Recall", "F2-score", "ROC-AUC"])
salvar("04_comparacao_modelos.svg")


thresholds = ler("modelos/analise_thresholds.csv")
xgb = thresholds[thresholds["modelo"] == "XGBoost"].sort_values("threshold")
plt.figure(figsize=(9, 4.5))
plt.plot(xgb["threshold"], xgb["precision"], label="Precisão")
plt.plot(xgb["threshold"], xgb["recall"], label="Recall")
plt.axvline(0.28, ls="--", label="Limiar histórico: 0,28")
plt.xlabel("Limiar de classificação")
plt.ylabel("Pontuação")
plt.title("Precisão e recall por limiar — XGBoost")
plt.legend()
plt.grid(alpha=0.25)
salvar("05_precision_recall_threshold.svg")


plt.figure(figsize=(9, 4.5))
for nome, grupo in thresholds.groupby("modelo"):
    grupo = grupo.sort_values("threshold")
    plt.plot(grupo["threshold"], grupo["f2"], label=nome)
plt.axvline(0.28, ls="--", label="Limiar histórico: 0,28")
plt.xlabel("Limiar de classificação")
plt.ylabel("F2-score")
plt.title("F2-score por limiar — validação de 2024")
plt.legend()
plt.grid(alpha=0.25)
salvar("06_f2_por_threshold.svg")


shap = ler("interpretabilidade/shap_importance.csv").nlargest(15, "mean_abs_shap")
shap["nome"] = (shap["feature"]
    .str.replace(r"^(categoricas|numericas)__", "", regex=True)
    .str.replace("tipo_acidente_", "Tipo de acidente — ", regex=False)
    .str.replace("br_categoria_", "BR — ", regex=False)
    .str.replace("uf_", "UF — ", regex=False)
    .str.replace("veiculos", "Número de veículos", regex=False))
shap = shap.sort_values("mean_abs_shap")
plt.figure(figsize=(11, 6))
plt.barh(shap["nome"], shap["mean_abs_shap"])
plt.xlabel("Impacto médio absoluto (SHAP)")
plt.title("15 características de maior importância global")
salvar("07_shap_top15.svg")

print("Visualizações geradas a partir dos CSVs; nenhuma nova modelagem foi executada.")
