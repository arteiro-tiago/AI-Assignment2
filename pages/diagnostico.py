"""Diagnóstico — Formulário com referências visuais inline."""

import streamlit as st
import pandas as pd
import numpy as np
import os

from model import (
    load_and_train_model, predict_diagnosis,
    CATEGORIES, DISPLAY_LABELS, TONGUE_IMAGES,
    CONDITION_DESCRIPTIONS, get_format_func,
    get_shap_contributions,
)

# carregar o modelo
model, encoders, feature_cols, label_cols, shap_explainer = load_and_train_model()



def tongue_field(label, cat_key, default):
    """Render reference images in a row, then a selectbox below."""
    st.markdown(f"**{label}**")
    images = TONGUE_IMAGES[cat_key]
    cols = st.columns(len(images))
    for i, (opt, img_path) in enumerate(images.items()):
        with cols[i]:
            if os.path.exists(img_path):
                st.image(
                    img_path,
                    caption=DISPLAY_LABELS[cat_key][opt],
                    width='stretch',
                )
    return st.selectbox(
        label, CATEGORIES[cat_key],
        format_func=get_format_func(cat_key),
        index=CATEGORIES[cat_key].index(default),
        key=f"sel_{cat_key}",
        label_visibility="collapsed",
    )


# header
st.markdown("""
<div class="hero-container" style="padding: 2rem;">
    <div class="hero-title" style="font-size: 2rem;">Diagnóstico</div>
    <div class="hero-subtitle">
        Preencha os dados do paciente e as características observadas na língua.
    </div>
</div>
""", unsafe_allow_html=True)

input_data = {}

#informações gerais
st.markdown(
    '<div class="form-section-title">Informação Geral</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)
with c1:
    input_data['idade'] = st.number_input(
        "Idade", min_value=1, max_value=120, value=30)
    input_data['temperatura_corporal'] = st.slider(
        "Temperatura Corporal (°C)", 35.0, 41.0, 36.5, 0.1)
with c2:
    input_data['sexo'] = st.selectbox(
        "Sexo", CATEGORIES['sexo'],
        format_func=get_format_func('sexo'),
        index=CATEGORIES['sexo'].index('masculino'))
    input_data['horas_sono'] = st.slider(
        "Horas de Sono", 0.0, 16.0, 8.0, 0.5)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# características da língua

st.markdown(
    '<div class="form-section-title">Características da Língua</div>',
    unsafe_allow_html=True,
)

input_data['cor_lingua'] = tongue_field("Cor da Língua", 'cor_lingua', 'normal')

input_data['cor_saburra'] = tongue_field("Cor da Saburra", 'cor_saburra', 'sem_saburra')

input_data['espessura_saburra'] = tongue_field("Espessura da Saburra", 'espessura_saburra', 'ausente')

input_data['lingua_inchada'] = tongue_field("Língua Inchada", 'lingua_inchada', 'nao')

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# outros simtomas e estilo de vida
st.markdown(
    '<div class="form-section-title">Sintomas e Estilo de Vida</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)
with c1:
    input_data['energia'] = st.selectbox(
        "Nível de Energia", CATEGORIES['energia'],
        format_func=get_format_func('energia'),
        index=CATEGORIES['energia'].index('normal'))
    input_data['digestao'] = st.selectbox(
        "Digestão", CATEGORIES['digestao'],
        format_func=get_format_func('digestao'),
        index=CATEGORIES['digestao'].index('normal'))
    input_data['humor'] = st.selectbox(
        "Humor", CATEGORIES['humor'],
        format_func=get_format_func('humor'),
        index=CATEGORIES['humor'].index('estavel'))
    input_data['memoria'] = st.selectbox(
        "Memória", CATEGORIES['memoria'],
        format_func=get_format_func('memoria'),
        index=CATEGORIES['memoria'].index('normal'))
with c2:
    input_data['sensacao_termica'] = st.selectbox(
        "Sensação Térmica", CATEGORIES['sensacao_termica'],
        format_func=get_format_func('sensacao_termica'),
        index=CATEGORIES['sensacao_termica'].index('normal'))
    input_data['stress_ansiedade'] = st.selectbox(
        "Stress / Ansiedade", CATEGORIES['stress_ansiedade'],
        format_func=get_format_func('stress_ansiedade'),
        index=CATEGORIES['stress_ansiedade'].index('ausente'))
    input_data['sintomas_respiratorios'] = st.selectbox(
        "Sintomas Respiratórios", CATEGORIES['sintomas_respiratorios'],
        format_func=get_format_func('sintomas_respiratorios'),
        index=CATEGORIES['sintomas_respiratorios'].index('nenhum'))
    input_data['queda_cabelo'] = st.selectbox(
        "Queda de Cabelo", CATEGORIES['queda_cabelo'],
        format_func=get_format_func('queda_cabelo'),
        index=CATEGORIES['queda_cabelo'].index('nao'))

# condição especial para mulheres por causa do periodo menstrual
if input_data['sexo'] == 'feminino':
    input_data['periodo_menstrual'] = st.selectbox(
        "Período Menstrual",
        ['regular', 'irregular', 'nao_aplicavel'],
        format_func=get_format_func('periodo_menstrual'))
else:
    input_data['periodo_menstrual'] = 'nao_aplicavel'

# diagnóstico
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

if st.button("Realizar Diagnóstico", type="primary", use_container_width=True):
    with st.spinner('A analisar…'):
        diagnosticos, probs = predict_diagnosis(
            model, encoders, feature_cols, label_cols, input_data
        )

    # resultado
    st.markdown('<div class="section-header">Resultado</div>',unsafe_allow_html=True)

    if diagnosticos:
        st.markdown("""
        <div class="result-positive">
            <div style="font-weight: 600; color: #ff6b6b;">
                Condições sugeridas:
            </div>
        </div>
        """, unsafe_allow_html=True)

        for d in diagnosticos:
            formatted = d.replace('_', ' ').capitalize()
            desc = CONDITION_DESCRIPTIONS.get(d, '')
            st.markdown(f"""
            <div class="glass-card"
                 style="padding: 1rem; border-left: 3px solid #ff6b6b;">
                <div style="font-weight: 600; color: #fafafa;">{formatted}</div>
                <div style="color: #8899a6; font-size: 0.85rem; margin-top: 0.3rem;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-negative">
            <div style="font-weight: 600; color: #00d4aa;">
                Nenhuma condição anómala identificada.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # probabilidades dos resultados
    st.markdown('<div class="section-header">Probabilidades</div>',unsafe_allow_html=True)

    display_probs = [(label, p) for label, p in probs if p > 0.05]

    if display_probs:
        for label, p in display_probs:
            formatted = label.replace('_', ' ').capitalize()
            pct = p * 100
            bar_class = "high" if p > 0.6 else ("medium" if p > 0.3 else "low")

            st.markdown(f"""
            <div style="margin-bottom: 0.8rem;">
                <div class="prob-label">{formatted}</div>
                <div class="prob-bar-container">
                    <div class="prob-bar {bar_class}"
                         style="width: {max(pct, 8)}%;">
                        {pct:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Nenhuma probabilidade significativa (> 5%) encontrada.")

    # contribuições do SHAP 
    st.markdown('<div class="custom-divider"></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-header">Análise de Características (SHAP)</div>',unsafe_allow_html=True)

    if diagnosticos:
        for diagnosis in diagnosticos:
            formatted_diagnosis = diagnosis.replace('_', ' ').capitalize()
            
            st.markdown(f"""
            <div style="margin-top: 1.5rem; margin-bottom: 1rem;">
                <div class="prob-label">{formatted_diagnosis}</div>
            </div>
            """, unsafe_allow_html=True)
            
            contributions = get_shap_contributions(
                shap_explainer, model, encoders, feature_cols, label_cols,
                input_data, diagnosis
            )
            
            if contributions:
                for feature, shap_value in contributions:
                    direction = "aumenta" if shap_value > 0 else "diminui"
                    abs_value = abs(shap_value)
                    
                    if contributions:
                        max_shap = 0
                        for _, v in contributions:
                            abs_v = abs(v)
                            if abs_v > max_shap:
                                max_shap = abs_v
                    else:
                        max_shap = 1

                    if max_shap > 0:
                        bar_width = (abs_value / max_shap) * 100
                        if bar_width > 100:
                            bar_width = 100
                    else:
                        bar_width = 0

                    if shap_value > 0:
                        bar_color = "#ff6b6b"
                    else:
                        bar_color = "#667eea"
                        
                    st.markdown(f"""
                    <div style="margin-bottom: 0.8rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                            <span class="prob-label" style="font-size: 0.9rem;">{feature}</span>
                            <span style="color: #8899a6; font-size: 0.85rem;">{direction}</span>
                        </div>
                        <div class="prob-bar-container">
                            <div style="width: {max(bar_width, 5)}%; background: {bar_color}; 
                                        padding: 0.4rem; color: white; text-align: right; 
                                        font-size: 0.8rem; border-radius: 3px;">
                                {abs_value:.3f}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma análise de características.")

