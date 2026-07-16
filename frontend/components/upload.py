import streamlit as st

def render_upload():

    st.header("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success("File Selected")

        st.write(f"📄 {uploaded_file.name}")

        st.write(
            f"Size : {uploaded_file.size/(1024*1024):.2f} MB"
        )

        if st.button("Upload"):

            st.info(
                "Backend upload will be connected later."
            )