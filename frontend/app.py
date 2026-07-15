import streamlit as st

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="OmniBrain",
    page_icon="🧠",
    layout="wide"
)

# ---------------- Sidebar ----------------
st.sidebar.title("🧠 OmniBrain")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "",
    ["🏠 Home", "📄 Documents", "🕒 History", "⚙️ Settings"]
)

st.sidebar.markdown("---")
st.sidebar.info("Frontend Prototype - Week 1")

# ---------------- Main Page ----------------
st.title("🧠 OmniBrain")
st.subheader("Enterprise Multi-Agent AI Assistant")

st.write("Upload a corporate report or financial PDF to begin.")

st.markdown("---")

# ---------------- Upload Section ----------------
st.header("📄 Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    size = uploaded_file.size / (1024 * 1024)

    st.success("File Selected Successfully!")

    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**File Size:** {size:.2f} MB")

    if st.button("Upload"):
        st.info("Backend integration coming soon...")

st.markdown("---")

# ---------------- Chat Section ----------------
st.header("💬 Chat")

question = st.text_input(
    "Ask a question about the uploaded document"
)

if st.button("Send"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.info("AI response will appear here after backend integration.")