import streamlit as st
from utils.api import check_health


def render_sidebar():

    health = check_health()

    st.sidebar.markdown("# 🧠 OmniBrain")
    st.sidebar.caption("Enterprise AI Workspace")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Workspace")

    doc = st.session_state.get("current_document")

    if doc is None:

        st.sidebar.info("No document uploaded")

    else:

        st.sidebar.write(f"**📄 {doc['filename']}**")
        st.sidebar.caption(doc["status"])

    st.sidebar.markdown("---")

    st.sidebar.subheader("Navigation")

    st.sidebar.radio(
        "",
        [
            "📄 Upload",
            "💬 Chat",
            "📚 History",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Backend")

    if health.get("status") == "healthy":

        st.sidebar.success("🟢 Connected")

    else:

        st.sidebar.error("🔴 Offline")

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    st.sidebar.caption("OmniBrain v2")