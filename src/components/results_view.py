# src/components/results_view.py
import json
import streamlit as st
from typing import List, Dict, Any, Optional


def render_results(
    chunks: List[Dict[str, Any]],
    critique_raw: Optional[str],
    final_answer: Optional[str],
) -> None:
    """
    Renders the multi‑agent output in three organised sections.
    
    Args:
        chunks: List of retrieved chunks (each with "text", "metadata", "score").
        critique_raw: JSON string from the Critic agent.
        final_answer: The final synthesised answer (Markdown).
    """
    if not chunks and not final_answer:
        st.info("💡 No results to display yet. Upload a PDF and ask a question.")
        return

    # ------------------------------------------------------------
    # Section 1: Retrieved Chunks (Expanded by default)
    # ------------------------------------------------------------
    with st.expander("📚 Retrieved Chunks", expanded=True):
        if not chunks:
            st.warning("No chunks were retrieved.")
        else:
            for idx, chunk in enumerate(chunks, 1):
                metadata = chunk.get("metadata", {})
                page = metadata.get("page", "N/A")
                source = metadata.get("source", "Unknown")
                score = chunk.get("score", 0.0)

                # Display metadata in a small chip
                st.markdown(
                    f"**Chunk {idx}** · 📄 `{source}` · Page `{page}` · "
                    f"🔹 Similarity `{score:.3f}`"
                )
                st.markdown(f"```text\n{chunk['text'][:600]}{'...' if len(chunk['text']) > 600 else ''}\n```")
                st.divider()

    # ------------------------------------------------------------
    # Section 2: Critique (Collapsed by default)
    # ------------------------------------------------------------
    with st.expander("🧐 Critic's Evaluation", expanded=False):
        if not critique_raw:
            st.caption("No critique available.")
        else:
            try:
                critique = json.loads(critique_raw)
                score = critique.get("relevance_score", 0.0)
                risk = critique.get("hallucination_risk", "Unknown")
                feedback = critique.get("feedback", "")
                missing_info = critique.get("missing_info", [])

                # Display key metrics in a nice grid
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Relevance Score", f"{score:.2f}")
                with col2:
                    st.metric("Hallucination Risk", risk)
                with col3:
                    st.metric("Missing Info", len(missing_info))

                st.markdown("**Feedback:**")
                st.info(feedback)

                if missing_info:
                    st.markdown("**Topics missing from context:**")
                    for item in missing_info:
                        st.markdown(f"- {item}")
            except json.JSONDecodeError:
                st.warning("Critique data is malformed. Raw output:")
                st.code(critique_raw, language="json")

    # ------------------------------------------------------------
    # Section 3: Final Answer (Expanded by default)
    # ------------------------------------------------------------
    with st.expander("📝 Final Answer", expanded=True):
        if final_answer:
            st.markdown(final_answer)
        else:
            st.caption("No answer generated yet.")