import streamlit as st
from utils.api import upload_pdf


def render_upload():
    st.error("THIS IS MY UPLOAD PAGE")
    st.header("📄 Upload PDF")
    if "uploading" not in st.session_state:
        st.session_state.uploading = False

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success("PDF Selected Successfully")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Size",
                f"{uploaded_file.size/(1024*1024):.2f} MB"
            )

        with col2:
            st.metric(
                "Format",
                "PDF"
            )

        st.write("**Filename:**", uploaded_file.name)

        upload_clicked = st.button(
            "Upload PDF",
            use_container_width=True,
            disabled=st.session_state.uploading
        )

        if upload_clicked:

            st.session_state.uploading = True

            with st.spinner("Uploading PDF..."):

                response = upload_pdf(uploaded_file)

            if response is None:

                st.error("❌ Unable to connect to the backend.")

            elif response.status_code == 200:

                data = response.json()

                st.success("✅ PDF uploaded successfully!")
                st.session_state.current_document = {
                    "filename": data["filename"],
                    "content_type": data["content_type"],
                    "size": data["size"],
                    "status": "Ready for Chat ✅"
                }

                progress = st.progress(0)

                status = st.empty()

                import time

                status.info("📤 Upload Complete")
                progress.progress(25)
                time.sleep(0.6)

                status.info("📄 Processing PDF...")
                progress.progress(50)
                time.sleep(0.8)

                status.info("📝 Extracting Text...")
                progress.progress(75)
                time.sleep(0.8)

                status.success("🤖 Ready for Chat!")
                progress.progress(100)

                st.markdown("### 📄 Upload Details")

                st.write(f"**Filename:** {data['filename']}")
                st.write(f"**Content Type:** {data['content_type']}")
                st.write(f"**Size:** {data['size']} bytes")

    if "current_document" in st.session_state:

            doc = st.session_state.current_document

            st.markdown("---")
            st.subheader("📄 Current Document")

            st.write(f"**Filename:** {doc['filename']}")
            st.write(f"**Type:** {doc['content_type']}")
            st.write(f"**Size:** {doc['size']} bytes")

            st.success(doc["status"])

            if st.button("🗑️ Remove Current Document"):

                del st.session_state.current_document
                st.rerun()        