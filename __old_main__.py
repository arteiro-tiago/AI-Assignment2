import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import shap
# print(shap.__version__) -> 0.51.0

NUM_LABELS = 18

df = pd.read_csv("lingua_diagnostico.csv")

feature_cols = df.columns[:-NUM_LABELS].tolist() 
label_cols = df.columns[-NUM_LABELS:].tolist()

x = df[feature_cols].copy().values
y = df[label_cols].values

categorical_cols = [
    "cor_lingua", "cor_saburra", "espessura_saburra", "lingua_inchada",
    "sexo", "energia", "sensacao_termica", "digestao",
    "stress_ansiedade", "humor", "sintomas_respiratorios",
    "memoria", "queda_cabelo", "periodo_menstrual"
]


encoders = {}
categories = {
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

# trransformar as categorias em numeros
for col, classes in categories.items():
    le = LabelEncoder()
    le.fit(classes)
    encoders[col] = le
    df[col] = le.transform(df[col])

x = df[feature_cols].copy().values


np.random.seed(42)
indices = np.random.permutation(len(x))
# dividir os dados (as features e as labels) 70% treino e 20% teste
split = int(len(x) * 0.8)
train_idx, test_idx = indices[:split], indices[split:]

x_train, x_test = x[train_idx], x[test_idx]
y_train, y_test = y[train_idx], y[test_idx]
 
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
model.fit(x_train, y_train)
explainer = shap.TreeExplainer(model)

# avaliação rápida
y_pred = model.predict(x_test)
print("=" * 50)
print("AVALIAÇÃO DO MODELO (test set 20%)")
print("=" * 50)
for i, label in enumerate(label_cols):
    acc = np.mean(y_pred[:, i] == y_test[:, i])
    print(f"  {label:<35} acc: {acc:.2f}")
 

def convertInput(raw_input):
    final = []
    for col in feature_cols:
        val = raw_input[col]
        if col in encoders:
            val = encoders[col].transform([val])[0]
        final.append(val)
    return np.array([final])
 
 
def predict(raw_input: dict):
    X_input = convertInput(raw_input)
    prediction = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)
 
    print("DIAGNÓSTICO")
    diagnosticos = []
    for i, label in enumerate(label_cols):
        if prediction[i] == 1:
            diagnosticos.append(label)
 
    if diagnosticos:
        for d in diagnosticos:
            print(f" - {d}")
    else:
        print("  Nenhum diagnóstico identificado.")
 
    print("\nPROBABILIDADES (todas as labels)")
    print("-" * 50)

    probs = []
    for i, label in enumerate(label_cols):
        p = proba[i][0][1] if proba[i].shape[1] > 1 else 0
        probs.append((label, p))

    probs.sort(key=lambda x: x[1], reverse=True)

    for label, p in probs:
        if p > 0.25:
            print(f"  {label:<35} {p:.2f}")



def explain_prediction(raw_input):

    X_input = convertInput(raw_input)

    shap_values = explainer.shap_values(X_input)

    prediction = model.predict(X_input)[0]

    print("\nEXPLICAÇÕES SHAP")
    print("=" * 60)

    for label_index, label in enumerate(label_cols):

        if prediction[label_index] == 1:

            print(f"\nDiagnóstico: {label}")

            contributions = []

            for i, feature in enumerate(feature_cols):

                value = shap_values[0, i, label_index]

                contributions.append((feature, value))

            contributions.sort(key=lambda x: abs(x[1]), reverse=True)

            for feature, value in contributions[:5]:

                direction = "↑ aumenta" if value > 0 else "↓ diminui"

                print(f"  {feature:<25} {direction} ({value:.3f})")


def plot_shap(raw_input, label_index=0):

    X_input = convertInput(raw_input)

    shap_values = explainer.shap_values(X_input)

    explanation = shap.Explanation(
        values=shap_values[0, :, label_index],
        base_values=explainer.expected_value[label_index],
        data=X_input[0],
        feature_names=feature_cols
    )

    shap.plots.waterfall(explanation)
    

input_teste = {
    "cor_lingua":            "normal",    # palida | vermelha | purpura | normal
    "cor_saburra":           "sem_saburra",     # branca | amarela | sem_saburra
    "espessura_saburra":     "ausente",      # fina | grossa | ausente
    "lingua_inchada":        "nao",         # nao | sim
    "idade":                 20,            # inteiro 18-90
    "sexo":                  "masculino",   # masculino | feminino
    "energia":               "normal",      # normal | baixa | muito_baixa
    "sensacao_termica":      "normal",       # normal | frio | calor
    "digestao":              "normal",  # normal | lenta | alterada | obstipacao
    "stress_ansiedade":      "ausente",     # ausente | moderado | elevado
    "humor":                 "estavel",     # estavel | agitado | deprimido
    "sintomas_respiratorios":"nenhum",      # nenhum | presente
    "temperatura_corporal":  36.0,          # float 36.0-40.5
    "horas_sono":            7.0,           # float 3.0-10.0
    "memoria":               "normal",      # normal | alterada
    "queda_cabelo":          "nao",         # nao | sim
    "periodo_menstrual":     "nao_aplicavel" # regular | irregular | nao_aplicavel
}


shap_values_train = explainer.shap_values(x_train)

label_index = 0

shap.summary_plot(
    shap_values_train[:, :, label_index],
    x_train,
    feature_names=feature_cols
)

predict(input_teste)
explain_prediction(input_teste)
plot_shap(input_teste, label_index=0)