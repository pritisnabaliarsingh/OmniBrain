import streamlit as st

from utils.api import check_backend


def render_sidebar():
    with st.sidebar:
        st.title("🧠🚀 OmniBrain")

        st.caption("Multi-Modal RAG Assistant")

        st.divider()

        if st.button(
            "Check Backend",
            use_container_width=True,
        ):
            success, result = check_backend()

            if success:
                st.success("Backend Online")
            else:
                st.error("Backend Offline")

        st.divider()

        st.markdown("### Features")

        st.markdown(
            """
            📄 **PDF RAG**

            Upload a PDF and ask questions about its content.

            🖼️ **Vision**

            Upload an image and ask Gemini to analyze it.

            🔌 **FastAPI Backend**

            Connected to the OmniBrain backend API.
            """
        )