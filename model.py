"""
model.py — Shared model logic, constants, and utilities for LinguAI.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import streamlit as st

NUM_LABELS = 18
CSV_PATH = "lingua_diagnostico.csv"

# ── Category definitions (raw values for the model) ──────────────────────────
CATEGORIES = {
    "cor_lingua":               ['normal', 'palida', 'purpura', 'vermelha'],
    "cor_saburra":              ['amarela', 'branca', 'sem_saburra'],
    "espessura_saburra":        ['ausente', 'fina', 'grossa'],
    "lingua_inchada":           ['nao', 'sim'],
    "sexo":                     ['feminino', 'masculino'],
    "energia":                  ['baixa', 'muito_baixa', 'normal'],
    "sensacao_termica":         ['calor', 'frio', 'normal'],
    "digestao":                 ['alterada', 'lenta', 'normal', 'obstipacao'],
    "stress_ansiedade":         ['ausente', 'elevado', 'moderado'],
    "humor":                    ['agitado', 'deprimido', 'estavel'],
    "sintomas_respiratorios":   ['nenhum', 'presente'],
    "memoria":                  ['alterada', 'normal'],
    "queda_cabelo":             ['nao', 'sim'],
    "periodo_menstrual":        ['irregular', 'nao_aplicavel', 'regular'],
}

# ── Display labels (proper Portuguese with accents/caps) ─────────────────────
DISPLAY_LABELS = {
    "cor_lingua": {
        'normal':   'Normal',
        'palida':   'Pálida',
        'purpura':  'Púrpura',
        'vermelha': 'Vermelha',
    },
    "cor_saburra": {
        'amarela':     'Amarela',
        'branca':      'Branca',
        'sem_saburra': 'Sem saburra',
    },
    "espessura_saburra": {
        'ausente': 'Ausente',
        'fina':    'Fina',
        'grossa':  'Grossa',
    },
    "lingua_inchada": {
        'nao': 'Não',
        'sim': 'Sim',
    },
    "sexo": {
        'feminino':  'Feminino',
        'masculino': 'Masculino',
    },
    "energia": {
        'normal':      'Normal',
        'baixa':       'Baixa',
        'muito_baixa': 'Muito baixa',
    },
    "sensacao_termica": {
        'normal': 'Normal',
        'frio':   'Frio',
        'calor':  'Calor',
    },
    "digestao": {
        'normal':      'Normal',
        'lenta':       'Lenta',
        'alterada':    'Alterada',
        'obstipacao':  'Obstipação',
    },
    "stress_ansiedade": {
        'ausente':  'Ausente',
        'moderado': 'Moderado',
        'elevado':  'Elevado',
    },
    "humor": {
        'estavel':   'Estável',
        'agitado':   'Agitado',
        'deprimido': 'Deprimido',
    },
    "sintomas_respiratorios": {
        'nenhum':   'Nenhum',
        'presente': 'Presente',
    },
    "memoria": {
        'normal':  'Normal',
        'alterada': 'Alterada',
    },
    "queda_cabelo": {
        'nao': 'Não',
        'sim': 'Sim',
    },
    "periodo_menstrual": {
        'regular':       'Regular',
        'irregular':     'Irregular',
        'nao_aplicavel': 'Não aplicável',
    },
}

# ── Tongue reference image mapping ────────────────────────────────────────────
TONGUE_IMAGES = {
    "cor_lingua": {
        'normal':   'images/língua-normal.jpg',
        'palida':   'images/língua-pálida2.jpg',
        'purpura':  'images/língua-púrpura3.jpg',
        'vermelha': 'images/língua-vermelha2.jpg',
    },
    "cor_saburra": {
        'amarela':     'images/língua-capa-amarela-fina2.jpg',
        'branca':      'images/língua-capa-branca-fina.jpg',
        'sem_saburra': 'images/língua-sem-capa2.jpg',
    },
    "espessura_saburra": {
        'ausente': 'images/língua-sem-capa2.jpg',
        'fina':    'images/língua-capa-branca-fina.jpg',
        'grossa':  'images/língua-capa-amarela-grossa2.jpg',
    },
    "lingua_inchada": {
        'nao': 'images/língua-normal2.jpg',
        'sim': 'images/língua-inchada2.jpg',
    },
}

# ── Condition descriptions ────────────────────────────────────────────────────
CONDITION_DESCRIPTIONS = {
    'resfriado':                    'Resfriado comum — infeção viral das vias aéreas superiores.',
    'gripe':                        'Gripe — infeção viral sistémica com febre e mal-estar.',
    'infeccao':                     'Infeção — presença de agente infecioso no organismo.',
    'inflamacao':                   'Inflamação — resposta imunológica com calor e vermelhidão.',
    'alteracoes_gastrointestinais': 'Alterações gastrointestinais — perturbações do sistema digestivo.',
    'acumulacao_mucosidades':       'Acumulação de mucosidades — excesso de muco nos sistemas respiratório/digestivo.',
    'debilidade_digestiva':         'Debilidade digestiva — fraqueza do sistema digestivo.',
    'metabolismo_lento':            'Metabolismo lento — redução da taxa metabólica basal.',
    'deficit_nutricional_anemia':   'Défice nutricional / Anemia — carência de nutrientes essenciais.',
    'hiperatividade_ansiedade':     'Hiperatividade / Ansiedade — excesso de atividade mental e nervosismo.',
    'estagnacao_energia_sangue':    'Estagnação de energia e sangue — bloqueio na circulação energética.',
    'depressao_stress':             'Depressão / Stress — perturbação emocional com abatimento.',
    'obstipacao':                   'Obstipação — dificuldade na evacuação intestinal.',
    'menopausa':                    'Menopausa — transição hormonal feminina.',
    'debilidade_estomago':          'Debilidade do estômago — fraqueza da função gástrica.',
    'excessos_alimentares':         'Excessos alimentares — consumo alimentar excessivo.',
    'processo_cronico':             'Processo crónico — condição de longa duração.',
    'condicao_normal':              'Condição normal — sem patologia identificada.',
}


def get_format_func(category):
    """Return a format function for selectbox display labels."""
    labels = DISPLAY_LABELS.get(category, {})
    return lambda x, _labels=labels: _labels.get(x, x.replace('_', ' ').capitalize())


# ── Model loading & training ─────────────────────────────────────────────────
@st.cache_resource
def load_and_train_model():
    """Load CSV data, encode features, and train a Random Forest classifier."""
    df = pd.read_csv(CSV_PATH)

    feature_cols = df.columns[:-NUM_LABELS].tolist()
    label_cols   = df.columns[-NUM_LABELS:].tolist()

    y = df[label_cols].values

    encoders = {}
    for col, classes in CATEGORIES.items():
        le = LabelEncoder()
        le.fit(classes)
        encoders[col] = le
        df[col] = le.transform(df[col])

    x = df[feature_cols].copy().values

    model = RandomForestClassifier(
        n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
    )
    model.fit(x, y)

    return model, encoders, feature_cols, label_cols


# ── Prediction ────────────────────────────────────────────────────────────────
def predict_diagnosis(model, encoders, feature_cols, label_cols, raw_input):
    """Run prediction and return (diagnostics_list, sorted_probabilities)."""
    final_input = []
    for col in feature_cols:
        val = raw_input[col]
        if col in encoders:
            encoded_val = encoders[col].transform([val])[0]
            final_input.append(encoded_val)
        else:
            final_input.append(val)

    X_input    = np.array([final_input])
    prediction = model.predict(X_input)[0]
    proba      = model.predict_proba(X_input)

    diagnosticos = [label_cols[i] for i, pred in enumerate(prediction) if pred == 1]

    probs = []
    for i, label in enumerate(label_cols):
        p = proba[i][0][1] if proba[i].shape[1] > 1 else 0
        probs.append((label, p))

    probs.sort(key=lambda x: x[1], reverse=True)

    return diagnosticos, probs
