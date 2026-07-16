import streamlit as st

from components.sidebar import render_sidebar
from components.upload import render_upload
from components.chat import render_chat

# Page configuration
st.set_page_config(
    page_title="OmniBrain",
    page_icon="🧠",
    layout="wide"
)

# Sidebar
render_sidebar()

# Main page
st.title("🧠 OmniBrain")
st.subheader("Enterprise Multi-Agent AI Assistant")

st.markdown("---")

# Upload section
render_upload()

st.markdown("---")

# Chat section
render_chat()