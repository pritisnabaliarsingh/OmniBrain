import streamlit as st

from utils.api import upload_pdf


def render_upload():
    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        key="pdf_uploader",
    )

    if uploaded_file is not None:
        st.info(f"Selected: {uploaded_file.name}")

        if st.button(
            "Upload PDF",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner("Uploading and processing PDF..."):
                status_code, result = upload_pdf(uploaded_file)

            if status_code == 200:
                st.success("PDF uploaded successfully!")

                st.session_state.pdf_uploaded = True
                st.session_state.pdf_filename = uploaded_file.name

                with st.expander("Upload details"):
                    st.json(result)

            else:
                st.error("PDF upload failed.")
                st.error(result.get("detail", str(result)))