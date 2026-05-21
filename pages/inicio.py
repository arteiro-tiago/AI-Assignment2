"""Início — Home Page."""

import streamlit as st
import pandas as pd

from model import load_and_train_model, CSV_PATH

# ── Load model (cached) ──────────────────────────────────────────────────────
model, encoders, feature_cols, label_cols = load_and_train_model()
df = pd.read_csv(CSV_PATH)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-container">
    <div class="hero-title">👅 Diagnóstico Médico</div>
    <div style="font-size: 1.3rem; color: #e0e0e0; font-weight: 400;
         margin-bottom: 1rem; position: relative;">
        Sistema de Apoio ao Diagnóstico pela Língua
    </div>
    <div class="hero-subtitle">
        Prova de Conceito — <strong style="color: #00d4aa;">Inteligência
        Artificial</strong>, FEUP 2025/2026.<br>
        Sistema de Machine Learning para sugerir diagnósticos a partir das
        características da língua, baseado na
        <strong style="color: #667eea;">Medicina Tradicional Chinesa</strong>.
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STATS
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{len(label_cols)}</div>
        <div class="stat-label">Condições</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">100</div>
        <div class="stat-label">Árvores (RF)</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{len(feature_cols)}</div>
        <div class="stat-label">Features</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{len(df):,}</div>
        <div class="stat-label">Amostras</div>
    </div>""", unsafe_allow_html=True)
