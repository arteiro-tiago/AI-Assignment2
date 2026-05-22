import streamlit as st


def get_base_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .hero-container {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-radius: 16px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 212, 170, 0.08) 0%, transparent 70%);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4aa, #667eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        position: relative;
    }

    .hero-subtitle {
        color: #8899a6;
        font-size: 1.1rem;
        font-weight: 300;
        line-height: 1.6;
        position: relative;
    }

    .glass-card {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 212, 170, 0.3);
    }

    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 0.5rem;
    }

    .card-text {
        color: #8899a6;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .stat-card {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.2rem 1.5rem;
        text-align: center;
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4aa, #667eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-label {
        color: #8899a6;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #fafafa;
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(0, 212, 170, 0.3);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .form-section {
        background: rgba(17, 25, 40, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .form-section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #00d4aa;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .result-positive {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
    }

    .result-negative {
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }

    .prob-bar-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        height: 30px;
        margin: 0.3rem 0;
        overflow: hidden;
        position: relative;
    }

    .prob-bar {
        height: 100%;
        border-radius: 8px;
        display: flex;
        align-items: center;
        padding-left: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
        transition: width 0.6s ease;
        min-width: 45px;
    }

    .prob-bar.high {
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
    }

    .prob-bar.medium {
        background: linear-gradient(90deg, #ffa726, #f7971e);
    }

    .prob-bar.low {
        background: linear-gradient(90deg, #00d4aa, #00b894);
    }

    .prob-label {
        color: #ccc;
        font-size: 0.88rem;
        margin-bottom: 0.2rem;
        font-weight: 500;
    }

    .badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-success {
        background: rgba(0, 212, 170, 0.15);
        color: #00d4aa;
        border: 1px solid rgba(0, 212, 170, 0.3);
    }

    .badge-warning {
        background: rgba(255, 167, 38, 0.15);
        color: #ffa726;
        border: 1px solid rgba(255, 167, 38, 0.3);
    }

    .badge-danger {
        background: rgba(255, 107, 107, 0.15);
        color: #ff6b6b;
        border: 1px solid rgba(255, 107, 107, 0.3);
    }

    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 170, 0.3), transparent);
        margin: 2rem 0;
    }

    .footer {
        text-align: center;
        color: #556;
        font-size: 0.8rem;
        padding: 2rem 0 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 3rem;
    }

    .ref-image-label {
        color: #ccc;
        font-size: 0.8rem;
        margin-top: 0.4rem;
        font-weight: 500;
        text-align: center;
    }

    .stSelectbox label, .stNumberInput label, .stSlider label {
        color: #ccc !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #00d4aa !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #8899a6 !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00d4aa, #00b894) !important;
        border: none !important;
        color: #0e1117 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.7rem 2rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3) !important;
    }

    .streamlit-expanderHeader {
        background: rgba(17, 25, 40, 0.5) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        color: #fafafa !important;
        font-weight: 500 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(17, 25, 40, 0.5);
        border-radius: 8px 8px 0 0;
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: #8899a6;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 212, 170, 0.1) !important;
        border-color: rgba(0, 212, 170, 0.3) !important;
        color: #00d4aa !important;
    }

    </style>
    """


def inject_css():
    """Inject the shared CSS into the current Streamlit page."""
    st.markdown(get_base_css(), unsafe_allow_html=True)
