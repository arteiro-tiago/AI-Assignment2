"""Guia de Referência Visual — Galeria de imagens da língua."""

import streamlit as st
import os

IMAGE_DIR = "images"

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-container" style="padding: 2rem;">
    <div class="hero-title" style="font-size: 2rem;">Guia de Referência Visual</div>
    <div class="hero-subtitle">
        Galeria de imagens de referência da língua, organizadas por categoria.
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  GALLERY DATA
# ══════════════════════════════════════════════════════════════════════════════
GALLERY = {
    "Cor da Língua": {
        "description": (
            "A cor da língua é um dos indicadores mais importantes. "
            "Uma língua saudável apresenta cor rosada uniforme."
        ),
        "items": [
            {
                "image": "língua-normal.jpg",
                "title": "Normal",
                "description": "Cor rosada uniforme, boa circulação sanguínea.",
                "badge": "Normal",
                "badge_type": "success",
            },
            {
                "image": "língua-pálida2.jpg",
                "title": "Pálida",
                "description": "Pode indicar deficiência de sangue ou frio interno.",
                "badge": "Atenção",
                "badge_type": "warning",
            },
            {
                "image": "língua-púrpura3.jpg",
                "title": "Púrpura",
                "description": "Estagnação de sangue e energia, problemas circulatórios.",
                "badge": "Atenção",
                "badge_type": "warning",
            },
            {
                "image": "língua-vermelha2.jpg",
                "title": "Vermelha",
                "description": "Calor interno, inflamação ou processos infeciosos.",
                "badge": "Alerta",
                "badge_type": "danger",
            },
        ],
    },
    "Saburra (Revestimento)": {
        "description": (
            "A saburra é o revestimento da superfície da língua. "
            "Cor e espessura indicam o estado digestivo e energético."
        ),
        "items": [
            {
                "image": "língua-capa-branca-fina.jpg",
                "title": "Branca Fina",
                "description": "Condição de frio ou fase inicial de infeção.",
                "badge": "Normal",
                "badge_type": "success",
            },
            {
                "image": "língua-capa-amarela-fina2.jpg",
                "title": "Amarela Fina",
                "description": "Calor interno moderado ou inflamação leve.",
                "badge": "Calor",
                "badge_type": "warning",
            },
            {
                "image": "língua-capa-amarela-grossa2.jpg",
                "title": "Amarela Grossa",
                "description": "Calor interno significativo, possível infeção.",
                "badge": "Alerta",
                "badge_type": "danger",
            },
            {
                "image": "língua-sem-capa2.jpg",
                "title": "Sem Saburra",
                "description": "Deficiência de Yin ou desidratação.",
                "badge": "Atenção",
                "badge_type": "warning",
            },
        ],
    },
    "Forma e Textura": {
        "description": (
            "A forma e textura revelam o estado dos órgãos internos "
            "e a retenção de líquidos."
        ),
        "items": [
            {
                "image": "língua-normal2.jpg",
                "title": "Normal",
                "description": "Tamanho proporcional, bordos lisos, textura uniforme.",
                "badge": "Normal",
                "badge_type": "success",
            },
            {
                "image": "língua-inchada2.jpg",
                "title": "Inchada",
                "description": "Retenção de líquidos ou deficiência do Baço.",
                "badge": "Atenção",
                "badge_type": "warning",
            },
            {
                "image": "língua-fissurada.jpg",
                "title": "Fissurada",
                "description": "Deficiência de Yin, calor crónico ou desidratação.",
                "badge": "Atenção",
                "badge_type": "warning",
            },
            {
                "image": "língua-pintas_vermelhas.jpg",
                "title": "Pintas Vermelhas",
                "description": "Calor nos órgãos ou processos inflamatórios.",
                "badge": "Alerta",
                "badge_type": "danger",
            },
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  RENDER GALLERY
# ══════════════════════════════════════════════════════════════════════════════
for category_name, category_data in GALLERY.items():
    st.markdown(
        f'<div class="section-header">{category_name}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"""
    <div style="color: #8899a6; margin-bottom: 1.5rem; font-size: 0.95rem;
         line-height: 1.6;">
        {category_data['description']}
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(category_data['items']))

    for i, item in enumerate(category_data['items']):
        with cols[i]:
            img_path = os.path.join(IMAGE_DIR, item['image'])
            if os.path.exists(img_path):
                st.image(img_path, width='stretch')

            badge_html = (
                f'<span class="badge badge-{item["badge_type"]}">'
                f'{item["badge"]}</span>'
            )

            st.markdown(f"""
            <div style="padding: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between;
                     align-items: center; margin-bottom: 0.3rem;">
                    <span style="font-weight: 600; color: #fafafa;
                          font-size: 0.95rem;">{item['title']}</span>
                    {badge_html}
                </div>
                <div style="color: #8899a6; font-size: 0.82rem;
                     line-height: 1.4;">
                    {item['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

