import streamlit as st

# Page configuration
st.set_page_config(
    page_title="OmniBrain",
    page_icon="🧠",
    layout="wide"
)

# Title
st.title("🧠 OmniBrain")

# Description
st.write("Enterprise Multi-Agent AI Research Assistant")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.write("🏠 Home")
st.sidebar.write("📄 Documents")
st.sidebar.write("🕒 History")
st.sidebar.write("⚙️ Settings")

# Main Section
st.header("Upload PDF")

st.info("PDF upload functionality will be added soon.")

st.divider()

# Chat Section
st.header("Chat")

question = st.text_input("Ask a question")

if st.button("Send"):
    st.warning("Backend is not connected yet.")