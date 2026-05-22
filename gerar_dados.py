"""
Gerador de Dados Sintéticos - Diagnóstico de Língua (Medicina Chinesa)
=======================================================================
Gera 2000 entradas baseadas nas regras clínicas do especialista.

As probabilidades são INTENCIONALMENTE imperfeitas para simular dados reais:
- Cada padrão tem ruído configurável
- Features podem ocasionalmente não corresponder ao padrão esperado
- Isso torna o problema interessante para um modelo de ML

Estrutura do CSV:
  X (features de entrada): 17 colunas
  Y (labels de saída):     18 colunas (diagnósticos)
"""

import random
import csv
import os

N_AMOSTRAS = 2000
FICHEIRO_SAIDA = "lingua_diagnostico.csv"

PROB_FEATURE_AUSENTE = 0.15
PROB_FEATURE_EXTRA = 0.08
PROB_LABEL_AUSENTE = 0.12
PROB_LABEL_EXTRA = 0.07

PESOS_PADROES = {
    1:  0.06,  # Pálida, s branca fina
    2:  0.05,  # Pálida, s branca grossa
    3:  0.04,  # Pálida, s amarela grossa
    4:  0.05,  # Pálida, sem saburra
    5:  0.04,  # Pálida, s amarela fina
    6:  0.06,  # Vermelha, s branca fina
    7:  0.05,  # Vermelha, s branca grossa
    8:  0.05,  # Vermelha, sem saburra
    9:  0.04,  # Vermelha, s amarela fina
    10: 0.04,  # Vermelha, s amarela grossa
    11: 0.04,  # Púrpura, s branca fina
    12: 0.04,  # Púrpura, s branca grossa
    13: 0.04,  # Púrpura, sem saburra
    14: 0.03,  # Púrpura, s amarela fina
    15: 0.03,  # Púrpura, s amarela grossa
    16: 0.09,  # Normal, s branca fina
    17: 0.07,  # Normal, s branca grossa
    18: 0.06,  # Normal, s amarela fina
    19: 0.06,  # Normal, s amarela grossa
    20: 0.06,  # Normal, sem saburra
}

COLUNAS_X = [
    "cor_lingua",
    "cor_saburra",
    "espessura_saburra",
    "lingua_inchada",
    "idade",
    "sexo",
    "energia",
    "sensacao_termica",
    "digestao",
    "stress_ansiedade",
    "humor",
    "sintomas_respiratorios",
    "temperatura_corporal",
    "horas_sono",
    "memoria",
    "queda_cabelo",
    "periodo_menstrual",
]

COLUNAS_Y = [
    "resfriado",
    "gripe",
    "infeccao",
    "inflamacao",
    "alteracoes_gastrointestinais",
    "acumulacao_mucosidades",
    "debilidade_digestiva",
    "metabolismo_lento",
    "deficit_nutricional_anemia",
    "hiperatividade_ansiedade",
    "estagnacao_energia_sangue",
    "depressao_stress",
    "obstipacao",
    "menopausa",
    "debilidade_estomago",
    "excessos_alimentares",
    "processo_cronico",
    "condicao_normal",
]

PADROES = {
    1: {
        "nome": "Pálida, saburra branca fina",
        "x": {
            "cor_lingua": "palida",
            "cor_saburra": "branca",
            "espessura_saburra": "fina",
            "energia": "baixa",
            "sensacao_termica": "frio",
            "digestao": "lenta",
            "temperatura_corporal_tipo": "baixa",
        },
        "y": ["debilidade_digestiva", "metabolismo_lento", "resfriado"],
    },
    2: {
        "nome": "Pálida, saburra branca grossa",
        "x": {
            "cor_lingua": "palida",
            "cor_saburra": "branca",
            "espessura_saburra": "grossa",
            "energia": "baixa",
            "sensacao_termica": "frio",
            "digestao": "alterada",
            "temperatura_corporal_tipo": "baixa",
        },
        "y": ["debilidade_digestiva", "metabolismo_lento", "acumulacao_mucosidades", "alteracoes_gastrointestinais"],
    },
    3: {
        "nome": "Pálida, saburra amarela grossa",
        "x": {
            "cor_lingua": "palida",
            "cor_saburra": "amarela",
            "espessura_saburra": "grossa",
            "energia": "baixa",
            "digestao": "alterada",
        },
        "y": ["debilidade_digestiva", "acumulacao_mucosidades", "alteracoes_gastrointestinais", "infeccao"],
    },
    4: {
        "nome": "Pálida, sem saburra",
        "x": {
            "cor_lingua": "palida",
            "cor_saburra": "sem_saburra",
            "espessura_saburra": "ausente",
            "energia": "baixa",
            "memoria": "alterada",
            "queda_cabelo": "sim",
        },
        "y": ["deficit_nutricional_anemia"],
    },
    5: {
        "nome": "Pálida, saburra amarela fina",
        "x": {
            "cor_lingua": "palida",
            "cor_saburra": "amarela",
            "espessura_saburra": "fina",
            "energia": "baixa",
            "sintomas_respiratorios": "presente",
            "temperatura_corporal_tipo": "alta",
        },
        "y": ["gripe", "debilidade_digestiva", "inflamacao"],
    },
    6: {
        "nome": "Vermelha, saburra branca fina",
        "x": {
            "cor_lingua": "vermelha",
            "cor_saburra": "branca",
            "espessura_saburra": "fina",
            "stress_ansiedade": "elevado",
            "humor": "agitado",
            "sintomas_respiratorios": "presente",
        },
        "y": ["hiperatividade_ansiedade", "gripe", "inflamacao"],
    },
    7: {
        "nome": "Vermelha, saburra branca grossa",
        "x": {
            "cor_lingua": "vermelha",
            "cor_saburra": "branca",
            "espessura_saburra": "grossa",
            "stress_ansiedade": "elevado",
            "digestao": "alterada",
        },
        "y": ["hiperatividade_ansiedade", "acumulacao_mucosidades", "alteracoes_gastrointestinais", "infeccao"],
    },
    8: {
        "nome": "Vermelha, sem saburra",
        "x": {
            "cor_lingua": "vermelha",
            "cor_saburra": "sem_saburra",
            "espessura_saburra": "ausente",
            "stress_ansiedade": "elevado",
            "horas_sono_tipo": "pouco",
            "queda_cabelo": "sim",
        },
        "y": ["hiperatividade_ansiedade", "deficit_nutricional_anemia", "menopausa"],
    },
    9: {
        "nome": "Vermelha, saburra amarela fina",
        "x": {
            "cor_lingua": "vermelha",
            "cor_saburra": "amarela",
            "espessura_saburra": "fina",
            "stress_ansiedade": "elevado",
            "sintomas_respiratorios": "presente",
            "temperatura_corporal_tipo": "alta",
        },
        "y": ["gripe", "hiperatividade_ansiedade", "inflamacao", "infeccao"],
    },
    10: {
        "nome": "Vermelha, saburra amarela grossa",
        "x": {
            "cor_lingua": "vermelha",
            "cor_saburra": "amarela",
            "espessura_saburra": "grossa",
            "stress_ansiedade": "elevado",
            "digestao": "obstipacao",
            "humor": "agitado",
        },
        "y": ["hiperatividade_ansiedade", "acumulacao_mucosidades", "inflamacao", "infeccao", "alteracoes_gastrointestinais", "obstipacao"],
    },
    11: {
        "nome": "Púrpura, saburra branca fina",
        "x": {
            "cor_lingua": "purpura",
            "cor_saburra": "branca",
            "espessura_saburra": "fina",
            "humor": "deprimido",
            "stress_ansiedade": "elevado",
            "periodo_menstrual": "irregular",
        },
        "y": ["estagnacao_energia_sangue", "depressao_stress"],
    },
    12: {
        "nome": "Púrpura, saburra branca grossa",
        "x": {
            "cor_lingua": "purpura",
            "cor_saburra": "branca",
            "espessura_saburra": "grossa",
            "humor": "deprimido",
            "digestao": "alterada",
        },
        "y": ["estagnacao_energia_sangue", "acumulacao_mucosidades"],
    },
    13: {
        "nome": "Púrpura, sem saburra",
        "x": {
            "cor_lingua": "purpura",
            "cor_saburra": "sem_saburra",
            "espessura_saburra": "ausente",
            "humor": "deprimido",
            "queda_cabelo": "sim",
            "periodo_menstrual": "irregular",
        },
        "y": ["estagnacao_energia_sangue", "deficit_nutricional_anemia", "processo_cronico"],
    },
    14: {
        "nome": "Púrpura, saburra amarela fina",
        "x": {
            "cor_lingua": "purpura",
            "cor_saburra": "amarela",
            "espessura_saburra": "fina",
            "humor": "agitado",
            "stress_ansiedade": "elevado",
        },
        "y": ["estagnacao_energia_sangue", "hiperatividade_ansiedade"],
    },
    15: {
        "nome": "Púrpura, saburra amarela grossa",
        "x": {
            "cor_lingua": "purpura",
            "cor_saburra": "amarela",
            "espessura_saburra": "grossa",
            "digestao": "alterada",
            "humor": "deprimido",
        },
        "y": ["estagnacao_energia_sangue", "acumulacao_mucosidades", "alteracoes_gastrointestinais"],
    },
    16: {
        "nome": "Normal, saburra branca fina",
        "x": {
            "cor_lingua": "normal",
            "cor_saburra": "branca",
            "espessura_saburra": "fina",
            "energia": "normal",
            "digestao": "normal",
        },
        "y": ["condicao_normal", "resfriado"],
    },
    17: {
        "nome": "Normal, saburra branca grossa",
        "x": {
            "cor_lingua": "normal",
            "cor_saburra": "branca",
            "espessura_saburra": "grossa",
            "digestao": "alterada",
        },
        "y": ["alteracoes_gastrointestinais", "acumulacao_mucosidades", "excessos_alimentares"],
    },
    18: {
        "nome": "Normal, saburra amarela fina",
        "x": {
            "cor_lingua": "normal",
            "cor_saburra": "amarela",
            "espessura_saburra": "fina",
            "humor": "agitado",
            "sintomas_respiratorios": "presente",
            "temperatura_corporal_tipo": "alta",
        },
        "y": ["gripe", "hiperatividade_ansiedade"],
    },
    19: {
        "nome": "Normal, saburra amarela grossa",
        "x": {
            "cor_lingua": "normal",
            "cor_saburra": "amarela",
            "espessura_saburra": "grossa",
            "digestao": "alterada",
        },
        "y": ["alteracoes_gastrointestinais", "acumulacao_mucosidades"],
    },
    20: {
        "nome": "Normal, sem saburra",
        "x": {
            "cor_lingua": "normal",
            "cor_saburra": "sem_saburra",
            "espessura_saburra": "ausente",
            "digestao": "lenta",
            "energia": "baixa",
        },
        "y": ["debilidade_estomago"],
    },
}

DEFAULTS_X = {
    "cor_lingua":             "normal",
    "cor_saburra":            "branca",
    "espessura_saburra":      "fina",
    "lingua_inchada":         "nao",
    "energia":                "normal",
    "sensacao_termica":       "normal",
    "digestao":               "normal",
    "stress_ansiedade":       "ausente",
    "humor":                  "estavel",
    "sintomas_respiratorios": "nenhum",
    "memoria":                "normal",
    "queda_cabelo":           "nao",
}

def ruido_feature(valor_esperado, prob_ausente=PROB_FEATURE_AUSENTE):
    if random.random() < prob_ausente:
        return False
    return True

def gerar_amostra(padrao_id):
    padrão = PADROES[padrao_id]
    x_esperado = padrão["x"]
    y_esperado = padrão["y"]

    x = {}

    # 1. Gerar os dados demográficos base
    x["idade"] = random.randint(18, 85)
    x["sexo"] = random.choice(["masculino", "feminino"])
    
    # Se a língua for associada a marcas dentais/inchaço nas notas
    if padrao_id in [1, 2, 20] or random.random() < 0.12:
        x["lingua_inchada"] = "sim"
    else:
        x["lingua_inchada"] = "nao"

    if x["sexo"] == "feminino":
        if x["idade"] >= 50:
            x["periodo_menstrual"] = "nao_aplicavel"
        else:
            x["periodo_menstrual"] = random.choices(["regular", "irregular"], weights=[0.75, 0.25], k=1)[0]
    else:
        x["periodo_menstrual"] = "nao_aplicavel"

    # 2. Aplicar os valores clínicos esperados com base no padrão (com ruído)
    for col, val in x_esperado.items():
        if col not in ["temperatura_corporal_tipo", "horas_sono_tipo"]:
            if ruido_feature(val):
                x[col] = val

    # 3. Preencher o resto com os valores padrão padrão (DEFAULTS_X) caso não tenham sido atribuídos
    for col in COLUNAS_X:
        if col not in x and col not in ["idade", "sexo", "horas_sono", "temperatura_corporal", "periodo_menstrual"]:
            x[col] = DEFAULTS_X.get(col, "normal")

    # 4. Inserir ruído probabilístico de features extra (atribuições aleatórias adicionais)
    for col in COLUNAS_X:
        if col not in x_esperado and col not in ["idade", "sexo", "horas_sono", "temperatura_corporal", "lingua_inchada", "periodo_menstrual", "cor_lingua", "cor_saburra", "espessura_saburra"]:
            if random.random() < PROB_FEATURE_EXTRA:
                opcoes = {
                    "energia":              ["baixa", "muito_baixa", "normal"],
                    "sensacao_termica":     ["frio", "normal", "calor"],
                    "digestao":             ["lenta", "normal", "alterada", "obstipacao"],
                    "stress_ansiedade":     ["ausente", "moderado", "elevado"],
                    "humor":                ["estavel", "deprimido", "agitado"],
                    "memoria":              ["normal", "alterada"],
                    "sintomas_respiratorios": ["nenhum", "presente"],
                    "queda_cabelo":         ["nao", "sim"],
                }
                if col in opcoes:
                    x[col] = random.choice(opcoes[col])

    # 5. Lógica para gerar os dados numéricos de Horas de Sono (Floats Reais)
    if "horas_sono_tipo" in x_esperado and x_esperado["horas_sono_tipo"] == "pouco":
        if ruido_feature("pouco"):
            x["horas_sono"] = round(random.uniform(3.0, 5.9), 1)
        else:
            x["horas_sono"] = round(random.uniform(6.0, 8.5), 1)
    else:
        # Se a língua for vermelha sem capa, a recomendação é dormir 7-8h, geramos em torno disso
        if x.get("cor_lingua") == "vermelha" and x.get("cor_saburra") == "sem_saburra":
            x["horas_sono"] = round(random.uniform(5.0, 9.0), 1)
        else:
            x["horas_sono"] = round(random.uniform(4.0, 10.0), 1)

    # 6. Lógica para gerar os dados numéricos de Temperatura Corporal (Floats Reais)
    if "temperatura_corporal_tipo" in x_esperado:
        tipo_temp = x_esperado["temperatura_corporal_tipo"]
        if ruido_feature(tipo_temp):
            if tipo_temp == "alta":
                x["temperatura_corporal"] = round(random.uniform(37.5, 40.0), 1)
            elif tipo_temp == "baixa":
                x["temperatura_corporal"] = round(random.uniform(36.0, 36.5), 1)
        else:
            x["temperatura_corporal"] = round(random.uniform(36.5, 37.4), 1)
    else:
        if x.get("cor_lingua") == "vermelha" or x.get("cor_saburra") == "amarela":
            x["temperatura_corporal"] = round(random.uniform(36.8, 39.5), 1)
        else:
            x["temperatura_corporal"] = round(random.uniform(36.1, 37.4), 1)

    # Ajuste de consistência para idade avançada (vinculado a língua vermelha sem capa nas notas)
    if padrao_id == 8 and random.random() < 0.70:
        x["idade"] = random.randint(60, 85)

    # 7. Geração de outputs Y (Labels)
    y = {col: 0 for col in COLUNAS_Y}

    for label in y_esperado:
        if random.random() >= PROB_LABEL_AUSENTE:
            y[label] = 1

    for label in COLUNAS_Y:
        if y[label] == 0 and random.random() < PROB_LABEL_EXTRA:
            y[label] = 1

    return x, y


def gerar_dataset(n=N_AMOSTRAS):
    ids = list(PESOS_PADROES.keys())
    pesos = [PESOS_PADROES[i] for i in ids]
    total = sum(pesos)
    pesos_norm = [p / total for p in pesos]

    amostras = []
    for _ in range(n):
        padrao_id = random.choices(ids, weights=pesos_norm, k=1)[0]
        x, y = gerar_amostra(padrao_id)
        amostras.append({**x, **y})

    return amostras


if __name__ == "__main__":
    random.seed(42)

    print(f"A gerar {N_AMOSTRAS} amostras em conformidade clínica...")
    dados = gerar_dataset(N_AMOSTRAS)

    caminho = os.path.join(os.path.dirname(__file__), FICHEIRO_SAIDA)
    colunas = COLUNAS_X + COLUNAS_Y

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)
    print(f"Sucesso! Dados guardados corretamente em '{FICHEIRO_SAIDA}'.")