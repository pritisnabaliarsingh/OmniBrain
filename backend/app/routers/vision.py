import base64

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from google import genai

from app.config.settings import GEMINI_API_KEY


router = APIRouter(
    prefix="/vision",
    tags=["Vision"]
)


# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


@router.get("/health")
def vision_health():
    return {
        "status": "ok",
        "service": "vision"
    }


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    # Validate image
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )

    # Read uploaded image
    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty"
        )

    try:
        # Convert image to base64
        image_data = base64.b64encode(contents).decode("utf-8")

        # Send image + question to Gemini
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {
                    "type": "image",
                    "data": image_data,
                    "mime_type": file.content_type
                },
                {
                    "type": "text",
                    "text": question
                }
            ]
        )

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(contents),
            "question": question,
            "answer": interaction.output_text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini image analysis failed: {str(e)}"
        )