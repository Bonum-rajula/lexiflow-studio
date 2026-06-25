# src/components/chat_input.py
import streamlit as st


def render_chat_input(disabled: bool = False) -> tuple[str, bool]:
    """
    Renders the question input area and the send button.
    
    Args:
        disabled: Whether the input and button should be disabled (e.g., during processing).
        
    Returns:
        A tuple: (question_text, is_submitted)
        - question_text: The text entered by the user.
        - is_submitted: True if the "Send" button was clicked this cycle.
    """
    with st.container():
        # Custom CSS to make the text area larger and more prominent
        st.markdown(
            """
            <style>
            .stTextArea textarea {
                font-size: 1.1rem;
                min-height: 120px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        question = st.text_area(
            "Ask a question about the document",
            placeholder="e.g., What does Section 3.2 say about data retention?",
            label_visibility="collapsed",
            disabled=disabled,
            key="question_input",  # Consistent key for state
        )

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            submitted = st.button(
                "🚀 Send",
                type="primary",
                use_container_width=True,
                disabled=disabled or not question.strip(),
            )

        return question, submitted