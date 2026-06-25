# src/app.py (UPDATED)
import streamlit as st
from loguru import logger

from .core.config import settings
from .core.session_state import init_session_state, SessionKeys
from .core.styles import apply_custom_styles
from .services.api_client import APIClient
from .components import render_sidebar, render_chat_input, render_results
from .utils.notifications import show_toast


# ------------------------------------------------------------
# 1. Apply Custom Styles
# ------------------------------------------------------------
apply_custom_styles()

# ------------------------------------------------------------
# 2. Initialize Session State
# ------------------------------------------------------------
init_session_state()

# ------------------------------------------------------------
# 3. Create API Client
# ------------------------------------------------------------
api_client = APIClient(base_url=settings.api_base_url)

# ------------------------------------------------------------
# 4. Check API Health
# ------------------------------------------------------------
api_healthy = api_client.health()
was_healthy = st.session_state.get(SessionKeys.API_HEALTHY)

# Show toast if health status changed (to avoid spamming)
if api_healthy and not was_healthy:
    show_toast("✅ Backend is online", "success")
elif not api_healthy and was_healthy:
    show_toast("❌ Backend unreachable. Check API_BASE_URL.", "error")

st.session_state[SessionKeys.API_HEALTHY] = api_healthy

# ------------------------------------------------------------
# 5. Render Sidebar (File Uploader)
# ------------------------------------------------------------
uploaded_file = render_sidebar(
    api_healthy=api_healthy,
    upload_status=st.session_state.get(SessionKeys.UPLOAD_STATUS),
)

# Handle file upload
if uploaded_file is not None:
    # Prevent re-upload spam: check if the same file was just uploaded
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.get("_last_upload_key") != file_key:
        st.session_state["_last_upload_key"] = file_key
        
        with st.spinner("⏳ Uploading and ingesting document..."):
            try:
                file_bytes = uploaded_file.read()
                response = api_client.upload_pdf(file_bytes, uploaded_file.name)
                
                # Show success toast
                show_toast(f"✅ {response.message} ({response.num_chunks} chunks)", "success")
                
                st.session_state[SessionKeys.UPLOAD_STATUS] = f"✅ {response.message} ({response.num_chunks} chunks)"
                st.session_state[SessionKeys.UPLOADED_DOCS].append({
                    "filename": response.filename,
                    "chunks": response.num_chunks,
                    "status": response.status,
                })
                # Reset answer display
                st.session_state[SessionKeys.CURRENT_ANSWER] = None
                st.session_state[SessionKeys.CURRENT_CHUNKS] = []
                st.session_state[SessionKeys.CURRENT_CRITIQUE] = None
                logger.info(f"Upload success: {response.filename}")
                
            except Exception as e:
                error_msg = str(e)
                show_toast(f"❌ Upload failed: {error_msg[:100]}", "error")
                st.session_state[SessionKeys.UPLOAD_STATUS] = f"❌ Upload failed: {error_msg}"
                logger.error(f"Upload error: {e}")

# ------------------------------------------------------------
# 6. Main Area
# ------------------------------------------------------------
st.title("💬 Ask Your Document")

col1, col2 = st.columns([4, 1])
with col1:
    st.title("💬 Ask Your Document")
with col2:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state[SessionKeys.CONVERSATION] = []
        st.session_state[SessionKeys.CURRENT_ANSWER] = None
        st.session_state[SessionKeys.CURRENT_CHUNKS] = []
        st.session_state[SessionKeys.CURRENT_CRITIQUE] = None
        show_toast("🗑️ Conversation cleared", "info")
        st.rerun()

# Check if any document has been uploaded
has_document = len(st.session_state.get(SessionKeys.UPLOADED_DOCS, [])) > 0
if not has_document:
    st.info("📄 Upload a PDF document using the sidebar to get started.")
else:
    st.caption(f"📚 Active document: {st.session_state[SessionKeys.UPLOADED_DOCS][-1]['filename']}")

# Display conversation history
conversation = st.session_state.get(SessionKeys.CONVERSATION, [])
for msg in conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------------------------------------------------
# 7. Render Results (if any)
# ------------------------------------------------------------
current_answer = st.session_state.get(SessionKeys.CURRENT_ANSWER)
current_chunks = st.session_state.get(SessionKeys.CURRENT_CHUNKS, [])
current_critique = st.session_state.get(SessionKeys.CURRENT_CRITIQUE)

if has_document and (current_answer or current_chunks):
    render_results(
        chunks=current_chunks,
        critique_raw=current_critique,
        final_answer=current_answer,
    )

# ------------------------------------------------------------
# 8. Chat Input
# ------------------------------------------------------------
is_processing = st.session_state.get(SessionKeys.PROCESSING, False)
question, submitted = render_chat_input(
    disabled=is_processing or not has_document
)

if submitted and question.strip():
    st.session_state[SessionKeys.PROCESSING] = True

    # Add user message
    st.session_state[SessionKeys.CONVERSATION].append({"role": "user", "content": question})

    with st.spinner("🧠 Agents are thinking..."):
        try:
            response = api_client.ask_question(question)

            st.session_state[SessionKeys.CURRENT_ANSWER] = response.answer
            st.session_state[SessionKeys.CURRENT_CHUNKS] = []
            st.session_state[SessionKeys.CURRENT_CRITIQUE] = response.critique

            st.session_state[SessionKeys.CONVERSATION].append({
                "role": "assistant",
                "content": response.answer
            })

            # Reset error count on success
            st.session_state[SessionKeys.ERROR_COUNT] = 0
            logger.info(f"Answer generated: {response.answer[:50]}...")

        except Exception as e:
            error_msg = str(e)
            # Increment error count for backoff
            st.session_state[SessionKeys.ERROR_COUNT] = st.session_state.get(SessionKeys.ERROR_COUNT, 0) + 1
            
            # Show user-friendly error
            if "401" in error_msg or "API key" in error_msg:
                user_msg = "🔑 OpenAI API key is missing or invalid. Please check your backend configuration."
            elif "timeout" in error_msg.lower():
                user_msg = "⏱️ The agents are taking too long. Please try again."
            else:
                user_msg = f"❌ Failed to generate answer: {error_msg[:100]}"
            
            show_toast(user_msg, "error")
            st.error(user_msg)
            logger.error(f"Ask error: {e}")

    st.session_state[SessionKeys.PROCESSING] = False
    st.rerun()