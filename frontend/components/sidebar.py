import streamlit as st

def render_sidebar():
    st.sidebar.title("🧠 OmniBrain")

    st.sidebar.markdown("## Navigation")
    st.sidebar.markdown("---")

    st.sidebar.metric(
        "Documents",
        0
    )

    st.sidebar.metric(
        "Messages",
        len(st.session_state.get("messages", []))
    )

    st.sidebar.radio(
        "Menu",
        [
            "🏠 Home",
            "📄 Documents",
            "💬 Chat",
            "🕒 History",
            "⚙️ Settings"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.sidebar.markdown("---")
    st.sidebar.info("Week 1 Prototype")