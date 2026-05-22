import streamlit as st
from styles import inject_css

st.set_page_config(
    page_title="Diagnóstico Médico",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
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

pg = st.navigation([
    st.Page("pages/inicio.py",          title="Início",             default=True),
    st.Page("pages/diagnostico.py",     title="Diagnóstico"),
    st.Page("pages/guia_referencia.py", title="Guia de Referência"),
])
pg.run()
