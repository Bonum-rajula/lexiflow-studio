# src/app.py
import streamlit as st
from loguru import logger

from .core.config import settings
from .core.session_state import init_session_state, SessionKeys
from .services.api_client import APIClient
from .components import render_sidebar, render_chat_input, render_results


# ------------------------------------------------------------
# 1. Initialize Session State
# ------------------------------------------------------------
init_session_state()

# ------------------------------------------------------------
# 2. Create API Client
# ------------------------------------------------------------
api_client = APIClient(base_url=settings.api_base_url)

# ------------------------------------------------------------
# 3. Check API Health and Update State
# ------------------------------------------------------------
api_healthy = api_client.health()
st.session_state[SessionKeys.API_HEALTHY] = api_healthy

# ------------------------------------------------------------
# 4. Render Sidebar (File Uploader)
# ------------------------------------------------------------
uploaded_file = render_sidebar(
    api_healthy=api_healthy,
    upload_status=st.session_state.get(SessionKeys.UPLOAD_STATUS),
)

# Handle file upload
if uploaded_file is not None:
    # Prevent re-upload if the same file is already uploaded (optional)
    # For simplicity, we upload every time the user selects a file.
    with st.spinner("Uploading and ingesting document..."):
        try:
            file_bytes = uploaded_file.read()
            response = api_client.upload_pdf(file_bytes, uploaded_file.name)
            st.session_state[SessionKeys.UPLOAD_STATUS] = f"✅ {response.message} ({response.num_chunks} chunks)"
            # Store document info
            st.session_state[SessionKeys.UPLOADED_DOCS].append({
                "filename": response.filename,
                "chunks": response.num_chunks,
                "status": response.status,
            })
            # Reset answer display when new document is uploaded
            st.session_state[SessionKeys.CURRENT_ANSWER] = None
            st.session_state[SessionKeys.CURRENT_CHUNKS] = []
            st.session_state[SessionKeys.CURRENT_CRITIQUE] = None
            logger.info(f"Upload success: {response.filename}")
        except Exception as e:
            st.session_state[SessionKeys.UPLOAD_STATUS] = f"❌ Upload failed: {str(e)}"
            logger.error(f"Upload error: {e}")

# ------------------------------------------------------------
# 5. Main Area: Conversation & Input
# ------------------------------------------------------------
st.title("💬 Ask Your Document")

# Display conversation history (past Q&A)
conversation = st.session_state.get(SessionKeys.CONVERSATION, [])
for msg in conversation:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ------------------------------------------------------------
# 6. Render Results of the Latest Answer (if any)
# ------------------------------------------------------------
current_answer = st.session_state.get(SessionKeys.CURRENT_ANSWER)
current_chunks = st.session_state.get(SessionKeys.CURRENT_CHUNKS, [])
current_critique = st.session_state.get(SessionKeys.CURRENT_CRITIQUE)

if current_answer or current_chunks:
    render_results(
        chunks=current_chunks,
        critique_raw=current_critique,
        final_answer=current_answer,
    )

# ------------------------------------------------------------
# 7. Chat Input (Bottom)
# ------------------------------------------------------------
question, submitted = render_chat_input(
    disabled=st.session_state.get(SessionKeys.PROCESSING, False)
)

if submitted and question.strip():
    # Set processing flag to disable input
    st.session_state[SessionKeys.PROCESSING] = True

    # Add user question to conversation
    st.session_state[SessionKeys.CONVERSATION].append({"role": "user", "content": question})

    # Call API
    with st.spinner("🧠 Agents are thinking..."):
        try:
            response = api_client.ask_question(question)

            # Store the results in session state for display
            st.session_state[SessionKeys.CURRENT_ANSWER] = response.answer
            st.session_state[SessionKeys.CURRENT_CHUNKS] = []  # We don't have chunks from the API response (needs backend change)
            # For now, we don't have chunks in the response, but we can store critique
            st.session_state[SessionKeys.CURRENT_CRITIQUE] = response.critique

            # Append assistant answer to conversation history
            st.session_state[SessionKeys.CONVERSATION].append({
                "role": "assistant",
                "content": response.answer
            })

            logger.info(f"Answer generated: {response.answer[:50]}...")

        except Exception as e:
            st.error(f"❌ Failed to get answer: {str(e)}")
            logger.error(f"Ask error: {e}")

    # Clear processing flag
    st.session_state[SessionKeys.PROCESSING] = False

    # Rerun to refresh the UI with new state
    st.rerun()