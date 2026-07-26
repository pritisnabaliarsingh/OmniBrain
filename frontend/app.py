import streamlit as st

from components.sidebar import render_sidebar
from components.upload import render_upload
from components.chat import render_chat

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="OmniBrain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# LOAD CSS
# ----------------------------------------------------

with open("styles/styles.css", encoding="utf-8") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_document" not in st.session_state:
    st.session_state.current_document = None

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

render_sidebar()

# ----------------------------------------------------
# HERO
# ----------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🧠 OmniBrain</h1>

<p>
Enterprise Multi-Agent Document Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# DASHBOARD
# ----------------------------------------------------

left, right = st.columns([1, 2], gap="large")

# ---------------- LEFT ---------------- #

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    render_upload()

    st.markdown("</div>", unsafe_allow_html=True)

    doc = st.session_state.get("current_document")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📚 Workspace")

    if doc is None:

        st.info("No document uploaded yet.")

    else:

        st.success(doc["status"])

        st.write(f"**📄 {doc['filename']}**")

        st.caption(doc["content_type"])

        st.write(f"Size : {doc['size']:,} bytes")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RIGHT ---------------- #

with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🤖 AI Assistant")

    render_chat()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.markdown("---")

st.caption(
    "OmniBrain • Enterprise Multi-Agent Document Intelligence Platform"
)