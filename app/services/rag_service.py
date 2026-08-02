from fastapi import HTTPException

from app.utils.logger import logger


def ask_rag(request):

    try:

        if not request.question.strip():

            logger.warning("Empty question received.")

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        logger.info(f"Question received: {request.question}")

        answer = "This is a sample response from OmniBrain."

        return {
            "question": request.question,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.error(f"Unexpected Error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )