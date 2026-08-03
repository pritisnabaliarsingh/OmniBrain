from fastapi import HTTPException

from app.utils.logger import logger

from app.services.embedding_service import create_embeddings
from app.services.vector_store import search


def ask_rag(request):

    try:

        if not request.question.strip():

            logger.warning("Empty question received.")

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        logger.info(f"Question received: {request.question}")

        query_embedding = create_embeddings([request.question])

        results = search(query_embedding[0])

        answer = results[0]

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