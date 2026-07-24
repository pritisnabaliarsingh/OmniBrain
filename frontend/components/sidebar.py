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
    st.sidebar.markdown("---")

    backend_status = "🟢 Online"

    st.sidebar.write(f"**Backend:** {backend_status}")

    if st.sidebar.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.sidebar.markdown("---")
    st.sidebar.info("Week 1 Prototype")