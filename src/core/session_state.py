# src/core/session_state.py (UPDATED)
import streamlit as st
from typing import List, Dict, Any, Optional


class SessionKeys:
    """Centralised keys for st.session_state."""
    CONVERSATION = "conversation_history"
    UPLOADED_DOCS = "uploaded_documents"
    PROCESSING = "processing"
    UPLOAD_STATUS = "upload_status"
    API_HEALTHY = "api_healthy"
    CURRENT_ANSWER = "current_answer"
    CURRENT_CHUNKS = "current_chunks"
    CURRENT_CRITIQUE = "current_critique"
    # NEW: Toast & error states
    LAST_TOAST = "last_toast"          # Avoid duplicate toasts on rerun
    ERROR_COUNT = "error_count"        # Track consecutive errors


def init_session_state():
    """Initialize all session state variables with default values."""
    if SessionKeys.CONVERSATION not in st.session_state:
        st.session_state[SessionKeys.CONVERSATION] = []
    if SessionKeys.UPLOADED_DOCS not in st.session_state:
        st.session_state[SessionKeys.UPLOADED_DOCS] = []
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
    if SessionKeys.LAST_TOAST not in st.session_state:
        st.session_state[SessionKeys.LAST_TOAST] = None
    if SessionKeys.ERROR_COUNT not in st.session_state:
        st.session_state[SessionKeys.ERROR_COUNT] = 0