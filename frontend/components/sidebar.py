import streamlit as st


def render_sidebar():

    st.sidebar.title("🧠 OmniBrain")

    st.sidebar.markdown("## Navigation")
    st.sidebar.markdown("---")

    # Current document information
    if "current_document" in st.session_state:

        doc = st.session_state.current_document

        st.sidebar.success("📄 Document Loaded")

        st.sidebar.write(f"**Name:** {doc['filename']}")
        st.sidebar.write(f"**Size:** {doc['size']} bytes")
        st.sidebar.write(f"**Status:** {doc['status']}")

    else:

        st.sidebar.warning("📄 No document uploaded")

    st.sidebar.metric(
        "💬 Messages",
        len(st.session_state.get("messages", []))
    )

    st.sidebar.markdown("---")

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

    backend_status = "🟢 Online"

    st.sidebar.write(f"**Backend:** {backend_status}")

    st.sidebar.markdown("---")

    st.sidebar.subheader("⚡ Quick Actions")

    if st.sidebar.button("🗑 Remove Current Document"):

        if "current_document" in st.session_state:

            del st.session_state.current_document

            st.sidebar.success("Document removed.")

            st.rerun()

    if st.sidebar.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.sidebar.success("Chat cleared.")

    st.sidebar.markdown("---")

    with st.sidebar.expander("ℹ️ About OmniBrain"):

        st.write(
            """
OmniBrain is a Multi-Modal RAG platform that allows users to upload
PDF documents and interact with them using AI-powered chat.
            """
        )

    st.sidebar.markdown("---")

    st.sidebar.info("Week 1 Prototype")