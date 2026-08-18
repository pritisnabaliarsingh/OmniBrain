import os

from fastapi import UploadFile, HTTPException

from app.config.settings import (
    UPLOAD_DIR,
    ALLOWED_TYPES,
    MAX_FILE_SIZE
)

from app.utils.logger import logger
from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text
from app.services.embedding_service import create_embeddings
from app.services.vector_store import create_vector_store


async def save_pdf(file: UploadFile):

    if file.content_type not in ALLOWED_TYPES:
        logger.warning(
            f"Invalid file type uploaded: {file.filename} ({file.content_type})"
        )

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file exceeds maximum allowed size."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    logger.info(f"File uploaded successfully: {file.filename}")

    # Read PDF
    text = read_pdf(file_path)

    # Split into chunks
    chunks = split_text(text)

    # Create embeddings
    embeddings = create_embeddings(chunks)

    # Create FAISS Vector Store
    create_vector_store(embeddings, chunks)

    logger.info("Vector Store Created Successfully")

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "PDF processed successfully."
    }