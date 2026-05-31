import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Noto Sans SC', sans-serif;
        }

        .main .block-container {
            padding-top: 1.5rem;
            max-width: 920px;
        }

        .app-hero {
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 45%, #5eead4 100%);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 8px 24px rgba(15, 118, 110, 0.25);
        }
        .app-hero h1 {
            margin: 0;
            font-size: 1.6rem;
            font-weight: 700;
        }
        .app-hero p {
            margin: 0.35rem 0 0 0;
            opacity: 0.92;
            font-size: 0.95rem;
        }

        .stat-card {
            background: #f0fdfa;
            border: 1px solid #99f6e4;
            border-radius: 12px;
            padding: 0.75rem 1rem;
            text-align: center;
        }
        .stat-card strong {
            display: block;
            font-size: 1.4rem;
            color: #0f766e;
        }
        .stat-card span {
            font-size: 0.8rem;
            color: #115e59;
        }

        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #ecfeff 100%);
        }

        div[data-testid="stSidebar"] .stButton > button {
            border-radius: 10px;
        }

        .stChatMessage {
            border-radius: 12px;
        }

        div[data-testid="stChatInput"] textarea {
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="app-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
