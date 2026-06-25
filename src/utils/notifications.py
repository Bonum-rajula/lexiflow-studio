# src/utils/notifications.py
import streamlit as st
from typing import Optional


def show_toast(
    message: str,
    severity: str = "info",
    duration: Optional[float] = None,
) -> None:
    """
    Display a toast notification with a specific severity level.
    
    Args:
        message: The notification text.
        severity: One of "info", "success", "warning", "error".
        duration: How long to show the toast (default: 3s for info, 5s for errors).
    """
    duration = duration or (5.0 if severity == "error" else 3.0)
    st.toast(message, icon=_get_icon(severity))
    st.caption(message)  # fallback for readers


def _get_icon(severity: str) -> str:
    """Return an appropriate emoji icon for the severity level."""
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
    }
    return icons.get(severity, "ℹ️")