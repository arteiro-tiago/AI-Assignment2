"""
app.py — LinguAI entry point.
Uses st.navigation for clean page names in sidebar.
"""

import streamlit as st
from styles import inject_css

# ── Page config (global, set once) ────────────────────────────────────────────
st.set_page_config(
    page_title="Diagnóstico Médico",
    page_icon="👅",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar branding ─────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <div style="font-size: 2rem;">👅</div>
    <div style="font-size: 1.1rem; font-weight: 700;
         background: linear-gradient(135deg, #00d4aa, #667eea);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
         background-clip: text;">Diagnóstico Médico</div>
    <div style="color: #8899a6; font-size: 0.75rem; margin-top: 0.2rem;">
        Análise pela Língua
    </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

# ── Navigation ────────────────────────────────────────────────────────────────
pg = st.navigation([
    st.Page("pages/inicio.py",          title="Início",             icon="🏠", default=True),
    st.Page("pages/diagnostico.py",     title="Diagnóstico",        icon="🩺"),
    st.Page("pages/guia_referencia.py", title="Guia de Referência",  icon="📖"),
])
pg.run()
