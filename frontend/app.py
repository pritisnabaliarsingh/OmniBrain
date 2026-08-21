import streamlit as st

from components.chat import render_chat
from components.sidebar import render_sidebar
from components.upload import render_upload
from components.vision import render_vision


st.set_page_config(
    page_title="OmniBrain",
    page_icon="🧠",
    layout="wide",
)


render_sidebar()


st.title("🧠 OmniBrain")
st.caption("Multi-Modal RAG Assistant")


pdf_tab, vision_tab = st.tabs(
    [
        "📄 PDF Assistant",
        "🖼️ Image Analysis",
    ]
)


with pdf_tab:
    st.header("PDF Assistant")

    upload_col, chat_col = st.columns(
        [1, 1],
        gap="large",
    )

    with upload_col:
        render_upload()

    with chat_col:
        render_chat()


with vision_tab:
    st.header("Image Analysis")

    render_vision()