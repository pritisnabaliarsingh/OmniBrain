import os

from fastapi import UploadFile, HTTPException

from app.config.settings import (
    UPLOAD_DIR,
    ALLOWED_TYPES,
    MAX_FILE_SIZE
)

from app.utils.logger import logger
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

    # Use Advanced Hybrid Pipeline
    from document_processing.pipeline.hybrid_pipeline import run_hybrid_pipeline
    pipeline_result = run_hybrid_pipeline(file_path)
    
    chunks = pipeline_result["chunks"]
    tables = pipeline_result["tables"]

    # Combine text chunks and tables for embedding
    all_text_chunks = [chunk.text for chunk in chunks]
    for table in tables:
        all_text_chunks.append(table.to_markdown())

    # Create embeddings
    embeddings = create_embeddings(all_text_chunks)

    # Create FAISS Vector Store
    create_vector_store(embeddings, all_text_chunks)

    logger.info("Vector Store Created Successfully")

    # Save Metadata to SQL Database
    from app.database.session import SessionLocal
    from app.database.crud import create_document
    from app.database.schemas import DocumentCreate

    db = SessionLocal()
    try:
        doc_data = DocumentCreate(
            filename=file.filename,
            file_type=file.content_type,
            file_size=len(content)
        )
        create_document(db, doc_data)
        logger.info("Document metadata saved to SQLite.")
    finally:
        db.close()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "chunks": len(chunks),
        "message": "PDF processed successfully."
    }