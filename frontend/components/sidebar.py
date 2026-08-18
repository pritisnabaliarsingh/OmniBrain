import streamlit as st
from utils.api import check_health


def render_sidebar():

    health = check_health()

    st.sidebar.markdown(
        """
        <div style="text-align:center;padding:12px 0 25px 0;">
            <h1 style="margin-bottom:0;">🧠 OmniBrain</h1>
            <p style="opacity:.7;margin-top:5px;">
                Enterprise AI Workspace
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    # ---------------- Workspace ---------------- #

    st.sidebar.subheader("📁 Workspace")

    doc = st.session_state.get("current_document")

    if doc is None:

        st.sidebar.info("No active document")

    else:

        st.sidebar.success("Ready for Chat")

        st.sidebar.markdown(f"**📄 {doc['filename']}**")

        st.sidebar.caption(doc["content_type"])

        st.sidebar.caption(f"{doc['size']:,} bytes")

    st.sidebar.markdown("---")

    # ---------------- Stats ---------------- #

    st.sidebar.subheader("📊 Statistics")

    col1, col2 = st.sidebar.columns(2)

    with col1:

        st.metric(
            "Docs",
            1 if doc else 0
        )

    with col2:

        st.metric(
            "Chats",
            len(st.session_state.get("messages", []))
        )

    st.sidebar.markdown("---")

    # ---------------- Navigation ---------------- #

    st.sidebar.subheader("🧭 Navigation")

    st.sidebar.radio(
        "",
        [
            "🏠 Dashboard",
            "📄 Documents",
            "💬 Chat",
            "🕒 History",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    # ---------------- Backend ---------------- #

    st.sidebar.subheader("⚡ Backend")

    if health.get("status") == "healthy":

        st.sidebar.success("🟢 FastAPI Connected")

    else:

        st.sidebar.error("🔴 Backend Offline")

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🗑 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    st.sidebar.markdown(
        "<center><small>OmniBrain v0.1</small></center>",
        unsafe_allow_html=True,
    )