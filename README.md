# TCC — Acidentes em Rodovias Federais com Machine Learning

Projeto de Trabalho de Conclusão de Curso desenvolvido por **Amanda Thiel Lopes**, com coorientação de **Rafaela da Silva**, com foco em Análise de Dados e Ciência de Dados aplicadas aos acidentes registrados nas rodovias federais brasileiras.

## Objetivo

Analisar os fatores associados à gravidade dos acidentes registrados pela Polícia Rodoviária Federal (PRF) e avaliar técnicas de Machine Learning para classificar acidentes graves ou fatais.

## Período e base

- Período analisado: **2020 a 2025**
- Fonte: **Dados Abertos da Polícia Rodoviária Federal (PRF)**
- Unidade de análise: acidentes agrupados por ocorrência
- Base consolidada: **406.209 acidentes**
- Variáveis originais: **31**
- Base tratada (Silver): **55 variáveis**
- IDs duplicados: **0**

> Os arquivos brutos da PRF não são versionados neste repositório. O notebook de coleta reproduz o download e a consolidação a partir da fonte pública.

## Variável alvo

Foi criada a variável binária `acidente_grave`:

- **0 — Não grave:** sem vítima gravemente ferida ou fatal
- **1 — Grave/fatal:** pelo menos um ferido grave ou uma vítima fatal

Distribuição na base completa:

| Classe | Ocorrências | Participação |
|---|---:|---:|
| Não grave | 291.900 | 71,86% |
| Grave/fatal | 114.309 | 28,14% |

## Pipeline do projeto

1. Coleta e integração dos dados da PRF
2. Auditoria de qualidade
3. Tratamento e engenharia de atributos
4. Análise Exploratória de Dados (EDA)
5. Testes estatísticos: Qui-quadrado e V de Cramér
6. Experimentos de Machine Learning
7. Comparação entre Regressão Logística, Random Forest e XGBoost
8. Ajuste de threshold com foco no F2-score
9. Interpretabilidade com Feature Importance e SHAP
10. Teste temporal final em 2025

## Principais achados

- Atropelamento de pedestre: **67,93%** de acidentes graves
- Colisão frontal: **62,67%**
- Pista simples: **33,52%**
- Plena noite: **32,38%**
- Taxa geral de acidentes graves: **28,14%**

## Análise estatística

| Variável | V de Cramér | Intensidade |
|---|---:|---|
| Tipo de acidente | 0,316 | Forte |
| Causa do acidente* | 0,261 | Moderada |
| Rodovia (BR) | 0,134 | Fraca |
| UF | 0,132 | Fraca |
| Tipo de pista | 0,118 | Fraca |
| Hora | 0,077 | Muito fraca |
| Fase do dia | 0,075 | Muito fraca |

\* A causa do acidente foi analisada entre 2021 e 2025 devido à mudança de taxonomia identificada nos registros de 2020.

## Machine Learning

Foram avaliados:

- Regressão Logística
- Random Forest
- XGBoost

### Validação temporal

- Treino inicial: **2020–2023**
- Validação: **2024**
- Teste final: **2025**

O conjunto de 2025 permaneceu bloqueado até a definição do algoritmo, dos hiperparâmetros e do threshold.

### Modelo selecionado

**XGBoost**, com threshold **0,28**, selecionado na validação de 2024 por maximizar o **F2-score**.

## Resultado final — teste de 2025

| Métrica | Resultado |
|---|---:|
| Accuracy | 37,54% |
| Precision | 30,76% |
| Recall | **96,78%** |
| F1-score | 46,68% |
| F2-score | **67,71%** |
| ROC-AUC | **0,714** |
| PR-AUC | **0,529** |

### Matriz de confusão — 2025

|  | Previsto não grave | Previsto grave |
|---|---:|---:|
| Real não grave | 7.391 | 44.645 |
| Real grave | **660** | **19.833** |

Dos **20.493 acidentes realmente graves em 2025**, o modelo identificou corretamente **19.833 (96,78%)**.

O threshold baixo aumenta a sensibilidade, mas também eleva o número de falsos positivos. Portanto, o modelo deve ser interpretado como um experimento acadêmico de classificação e não como uma ferramenta operacional pronta.

## Interpretabilidade

Foram utilizadas:

- Feature Importance do XGBoost
- SHAP

Os resultados indicaram que **tipo de acidente**, **rodovia federal** e **UF** formam o principal conjunto de variáveis discriminantes do modelo.

## Estrutura do repositório

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
├── outputs/
│   ├── auditoria/
│   ├── eda/
│   ├── estatistica/
│   ├── modelos/
│   ├── interpretabilidade/
│   └── modelo_final/
└── figures/
```

## Ordem de execução dos notebooks

```text
01_coleta_integracao.ipynb
02_auditoria_qualidade.ipynb
03_tratamento_base.ipynb
04_analise_exploratoria.ipynb
05_associacoes_estatisticas.ipynb
06_experimentos_machine_learning.ipynb
07_comparacao_modelos.ipynb
08_interpretabilidade_xgboost.ipynb
09_interpretabilidade_shap.ipynb
10_teste_final_2025.ipynb
```

## Tecnologias

Python, Pandas, NumPy, SciPy, Matplotlib, Scikit-learn, XGBoost, SHAP, PyArrow, Joblib e Jupyter/Google Colab.

## Reprodução

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

Depois execute os notebooks na ordem indicada. O primeiro notebook realiza a coleta dos arquivos públicos da PRF e gera a base consolidada localmente.

## Observações metodológicas

- Variáveis de consequência como `mortos`, `feridos_graves`, `feridos`, `ilesos` e `classificacao_acidente` não foram utilizadas como preditoras, evitando data leakage.
- A variável `causa_acidente` foi preservada para análise, mas não integrou o primeiro conjunto de modelos devido à mudança de taxonomia entre 2020 e 2021.
- O threshold final foi definido antes da abertura do teste de 2025.
- Os resultados representam associações presentes nos registros históricos e não relações de causalidade.

## Autoria

**Denis Dorneles**  
Engenharia da Computação — UniFECAF

**Coorientadora:** Rafaela da Silva
