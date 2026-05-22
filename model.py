import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import shap

NUM_LABELS = 18
CSV_PATH = "lingua_diagnostico.csv"

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

# labels em portugues
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

# imagens das linguas
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

# descrições das condiçoes 
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
    labels = DISPLAY_LABELS.get(category, {})
    return lambda x, _labels=labels: _labels.get(x, x.replace('_', ' ').capitalize())


# handle do modelo
@st.cache_resource
def load_and_train_model():
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

    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(x, y)
    
    # shap explainer criado aqui para ser guardado com o modelo
    shap_explainer = shap.TreeExplainer(model)

    return model, encoders, feature_cols, label_cols, shap_explainer


# ── SHAP Explainer ────────────────────────────────────────────────────────────
# The explainer is now created in load_and_train_model and returned directly


def get_shap_contributions(explainer, model, encoders, feature_cols, label_cols, raw_input, diagnosis_label):
    """
    Calculate top 5 SHAP feature contributions for a specific diagnosis.
    Returns list of (feature_display, abs_contribution) tuples sorted by magnitude.
    """
    # inputs
    final_input = []
    for col in feature_cols:
        val = raw_input[col]
        if col in encoders:
            encoded_val = encoders[col].transform([val])[0]
            final_input.append(encoded_val)
        else:
            final_input.append(val)
    
    X_input = np.array([final_input])
    
    shap_values = explainer.shap_values(X_input)
    
    label_index = label_cols.index(diagnosis_label)
    
    contributions = []
    for i, feature in enumerate(feature_cols):
        contribution = shap_values[0, i, label_index]
        contributions.append((feature, contribution))
    
    contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    top_contributions = contributions[:5]
    
    result = []
    for feature, contrib in top_contributions:
        display_name = feature.replace('_', ' ').capitalize()
        result.append((display_name, contrib))
    
    return result

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

    X_input = np.array([final_input])
    prediction = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)

    diagnosticos = [label_cols[i] for i, pred in enumerate(prediction) if pred == 1]

    probs = []
    for i, label in enumerate(label_cols):
        p = proba[i][0][1] if proba[i].shape[1] > 1 else 0
        probs.append((label, p))

    probs.sort(key=lambda x: x[1], reverse=True)

    return diagnosticos, probs
