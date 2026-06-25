# src/components/sidebar.py
import streamlit as st
from typing import Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile


def render_sidebar(
    api_healthy: bool,
    upload_status: Optional[str] = None,
) -> Optional[UploadedFile]:
    """
    Renders the sidebar with API health, file uploader, and upload status.
    
    Args:
        api_healthy: Boolean indicating if the backend API is reachable.
        upload_status: Optional status message from the last upload attempt.
        
    Returns:
        The uploaded PDF file object, or None if no file is uploaded.
    """
    with st.sidebar:
        st.image(
            "https://img.icons8.com/fluency/96/000000/artificial-intelligence.png",
            width=80,
        )
        st.title("🧠 LexiFlow Studio")
        st.caption("Multi‑Agent RAG Orchestrator")

        # ------------------------------------------------------------
        # API Health Status
        # ------------------------------------------------------------
        st.markdown("---")
        st.subheader("🔌 System Status")
        if api_healthy:
            st.success("✅ Backend online")
        else:
            st.error("❌ Backend unreachable")
            st.caption("Ensure the LexiFlow API is running and `API_BASE_URL` is correct.")

        # ------------------------------------------------------------
        # File Uploader (The Sensory Input)
        # ------------------------------------------------------------
        st.markdown("---")
        st.subheader("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload a PDF document",
            type=["pdf"],
            label_visibility="collapsed",
            help="Supports PDF files up to 200MB",
        )

        # ------------------------------------------------------------
        # Upload Status Feedback
        # ------------------------------------------------------------
        if upload_status:
            st.info(f"📌 {upload_status}")

        st.markdown("---")
        st.caption("v0.1.0 · Built with Streamlit")

    return uploaded_file