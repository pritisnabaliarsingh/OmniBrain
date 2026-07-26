import time
import streamlit as st

from utils.api import upload_pdf


def render_upload():

    st.subheader("📄 Upload Document")
    st.caption("Upload a PDF to start chatting with your documents.")

    if "uploading" not in st.session_state:
        st.session_state.uploading = False

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_file:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Size",
                f"{uploaded_file.size/(1024*1024):.2f} MB"
            )

        with col2:
            st.metric(
                "Type",
                "PDF"
            )

        st.info(uploaded_file.name)

        if st.button(
            "Upload",
            use_container_width=True,
            disabled=st.session_state.uploading
        ):

            st.session_state.uploading = True

            with st.spinner("Uploading..."):

                response = upload_pdf(uploaded_file)

            st.session_state.uploading = False

            if response is None:

                st.error("Backend Offline")

            elif response.status_code == 200:

                data = response.json()

                st.session_state.current_document = {
                    "filename": data["filename"],
                    "content_type": data["content_type"],
                    "size": data["size"],
                    "status": "Ready for Chat ✅"
                }

                progress = st.progress(0)

                for i in range(101):

                    progress.progress(i)

                    time.sleep(0.01)

                st.success("Document uploaded successfully!")

            else:

                st.error("Upload Failed")

    doc = st.session_state.get("current_document")

    if doc is not None:

        st.markdown("---")

        st.subheader("Current Document")

        st.write(f"**📄 {doc['filename']}**")

        st.caption(doc["status"])

        st.write(f"Type : {doc['content_type']}")

        st.write(f"Size : {doc['size']:,} bytes")

        if st.button(
            "Remove Document",
            use_container_width=True
        ):

            st.session_state.current_document = None
            st.rerun()