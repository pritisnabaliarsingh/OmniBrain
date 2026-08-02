import os

from fastapi import UploadFile, HTTPException

from app.config.settings import (
    UPLOAD_DIR,
    ALLOWED_TYPES,
    MAX_FILE_SIZE
)

from app.utils.logger import logger


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

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    if len(content) == 0:
        logger.warning(f"Empty file uploaded: {file.filename}")

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(content) > MAX_FILE_SIZE:
        logger.warning(
            f"Large file rejected: {file.filename}"
        )

        raise HTTPException(
            status_code=400,
            detail="Uploaded file exceeds maximum allowed size of 10 MB."
        )

    logger.info(
        f"File uploaded successfully: {file.filename}"
    )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "stored_path": file_path,
        "message": "File Uploaded Successfully and stored."
    }