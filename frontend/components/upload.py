import time
import streamlit as st

from utils.api import upload_pdf


def render_upload():

    st.markdown("## 📄 Upload Document")
    st.caption("Upload a PDF and prepare it for AI-powered conversations.")

    if "uploading" not in st.session_state:
        st.session_state.uploading = False

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        st.success("✅ File Selected")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "📦 Size",
                f"{uploaded_file.size/(1024*1024):.2f} MB"
            )

        with c2:

            st.metric(
                "📄 Type",
                "PDF"
            )

        st.markdown(f"**Filename**  \n{uploaded_file.name}")

        if st.button(
            "🚀 Upload & Process",
            use_container_width=True,
            disabled=st.session_state.uploading
        ):

            st.session_state.uploading = True

            with st.spinner("Processing document..."):

                response = upload_pdf(uploaded_file)

            st.session_state.uploading = False

            if response is None:

                st.error("Backend is not reachable.")

            elif response.status_code == 200:

                data = response.json()

                st.session_state.current_document = {

                    "filename": data["filename"],
                    "content_type": data["content_type"],
                    "size": data["size"],
                    "status": "Ready for Chat 🚀"

                }

                progress = st.progress(0)

                steps = [

                    "Uploading...",
                    "Processing...",
                    "Extracting Text...",
                    "Creating Embeddings...",
                    "Ready!"

                ]

                status = st.empty()

                for i, step in enumerate(steps):

                    status.info(step)

                    progress.progress((i + 1) * 20)

                    time.sleep(0.45)

                status.success("Document Ready ✅")
                time.sleep(1)
                st.rerun()

    doc = st.session_state.get("current_document")

    if doc:

        st.markdown("---")

        st.subheader("📚 Current Workspace")

        c1, c2 = st.columns([4, 1])

        with c1:

            st.success(doc["status"])

            st.write(f"**📄 {doc['filename']}**")

            st.caption(doc["content_type"])

            st.write(f"**Size:** {doc['size']:,} bytes")

        with c2:

            if st.button(
                "🗑 Remove",
                use_container_width=True
            ):

                st.session_state.current_document = None
                st.rerun()