# src/core/styles.py
import streamlit as st

def apply_custom_styles():
    """
    Inject custom CSS to brand the app with "LexiFlow Blue" and improve UX.
    """
    st.markdown(
        """
        <style>
        /* LexiFlow Brand Colors */
        :root {
            --lexi-blue: #1E88E5;
            --lexi-blue-dark: #1565C0;
            --lexi-blue-light: #64B5F6;
        }

        /* Primary buttons */
        .stButton > button {
            background-color: var(--lexi-blue) !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background-color: var(--lexi-blue-dark) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
        }
        .stButton > button:disabled {
            opacity: 0.5 !important;
            cursor: not-allowed !important;
            transform: none !important;
        }

        /* File uploader */
        .stFileUploader > div {
            border: 2px dashed var(--lexi-blue) !important;
            border-radius: 12px !important;
            background-color: rgba(30, 136, 229, 0.05) !important;
            transition: all 0.2s ease !important;
        }
        .stFileUploader > div:hover {
            background-color: rgba(30, 136, 229, 0.1) !important;
            border-color: var(--lexi-blue-dark) !important;
        }

        /* Expanders (accordion) */
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: var(--lexi-blue) !important;
            border-radius: 8px !important;
            transition: background 0.2s ease !important;
        }
        .streamlit-expanderHeader:hover {
            background-color: rgba(30, 136, 229, 0.05) !important;
        }

        /* Metrics (Critique scores) */
        .stMetric {
            background: rgba(30, 136, 229, 0.05) !important;
            border-radius: 12px !important;
            padding: 12px !important;
            border-left: 4px solid var(--lexi-blue) !important;
        }

        /* Chat messages */
        .stChatMessage {
            border-radius: 12px !important;
            padding: 16px !important;
            margin: 8px 0 !important;
        }
        .stChatMessage.user {
            background-color: rgba(30, 136, 229, 0.08) !important;
        }
        .stChatMessage.assistant {
            background-color: rgba(30, 136, 229, 0.03) !important;
            border-left: 4px solid var(--lexi-blue) !important;
        }

        /* Code blocks in answers */
        .stMarkdown pre {
            background-color: #1E1E1E !important;
            border-radius: 8px !important;
            padding: 16px !important;
            border-left: 4px solid var(--lexi-blue) !important;
        }

        /* Toast notifications - custom styling */
        .stToast {
            border-radius: 12px !important;
            border-left: 6px solid var(--lexi-blue) !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15) !important;
        }
        .stToast.error {
            border-left-color: #EF4444 !important;
        }
        .stToast.success {
            border-left-color: #22C55E !important;
        }
        .stToast.warning {
            border-left-color: #F59E0B !important;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: #0E1117 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )