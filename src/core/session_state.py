# src/core/session_state.py
import streamlit as st
from typing import List, Dict, Any, Optional


class SessionKeys:
    """Centralised keys for st.session_state."""
    CONVERSATION = "conversation_history"
    UPLOADED_DOCS = "uploaded_documents"
    PROCESSING = "processing"
    UPLOAD_STATUS = "upload_status"
    API_HEALTHY = "api_healthy"
    CURRENT_ANSWER = "current_answer"      # Store the last answer for display
    CURRENT_CHUNKS = "current_chunks"
    CURRENT_CRITIQUE = "current_critique"


def init_session_state():
    """Initialize all session state variables with default values."""
    if SessionKeys.CONVERSATION not in st.session_state:
        st.session_state[SessionKeys.CONVERSATION] = []  # list of {"role": "user"/"assistant", "content": str}
    if SessionKeys.UPLOADED_DOCS not in st.session_state:
        st.session_state[SessionKeys.UPLOADED_DOCS] = []  # list of dicts with filename, chunks, etc.
    if SessionKeys.PROCESSING not in st.session_state:
        st.session_state[SessionKeys.PROCESSING] = False
    if SessionKeys.UPLOAD_STATUS not in st.session_state:
        st.session_state[SessionKeys.UPLOAD_STATUS] = None
    if SessionKeys.API_HEALTHY not in st.session_state:
        st.session_state[SessionKeys.API_HEALTHY] = False
    if SessionKeys.CURRENT_ANSWER not in st.session_state:
        st.session_state[SessionKeys.CURRENT_ANSWER] = None
    if SessionKeys.CURRENT_CHUNKS not in st.session_state:
        st.session_state[SessionKeys.CURRENT_CHUNKS] = []
    if SessionKeys.CURRENT_CRITIQUE not in st.session_state:
        st.session_state[SessionKeys.CURRENT_CRITIQUE] = None