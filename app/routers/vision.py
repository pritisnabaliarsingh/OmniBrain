from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.llm_service import ask_image_question
from app.utils.logger import logger


router = APIRouter(tags=["Vision"])


# --------------------------------------------------
# 1. IMAGE UPLOAD / INFORMATION ENDPOINT
# --------------------------------------------------
@router.post("/vision")
async def vision_upload(file: UploadFile = File(...)):

    try:
        # Validate image
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid image file."
            )

        # Read image
        image_bytes = await file.read()

        # Check empty image
        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        logger.info(
            f"Vision image received: {file.filename} "
            f"({file.content_type}, {len(image_bytes)} bytes)"
        )

        # IMPORTANT:
        # This endpoint does NOT call Gemini.
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(image_bytes),
            "message": "Image received successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"Vision image upload failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Vision image upload failed: {str(e)}"
        )


# --------------------------------------------------
# 2. IMAGE ANALYSIS ENDPOINT
# --------------------------------------------------
@router.post("/vision/analyze")
async def vision_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):

    try:
        # Validate image
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid image file."
            )

        # Validate question
        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        # Read image
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        logger.info(
            f"Vision question received: {question}"
        )

        logger.info(
            f"Vision image received: {file.filename} "
            f"({file.content_type}, {len(image_bytes)} bytes)"
        )

        # Send image to Gemini
        answer = ask_image_question(
            image_bytes=image_bytes,
            mime_type=file.content_type,
            question=question
        )

        logger.info(
            f"Vision question answered successfully: {file.filename}"
        )

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "question": question,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.error(
            f"Vision question failed: {str(e)}"
        )

        # Gemini quota error
        if "429" in str(e) or "quota" in str(e).lower():
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later."
            )

        raise HTTPException(
            status_code=500,
            detail=f"Vision question failed: {str(e)}"
        )