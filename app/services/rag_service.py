from fastapi import HTTPException

from app.services.llm_service import generate_answer
from app.services.embedding_service import create_embeddings
from app.services.vector_store import search
from app.utils.logger import logger


def ask_rag(request):
    try:
        # Validate question
        if not request.question.strip():
            logger.warning("Empty question received.")

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        logger.info(f"Question received: {request.question}")

        # Create embedding for the user's question
        query_embedding = create_embeddings([request.question])

        # Search similar chunks from FAISS
        results = search(query_embedding[0])

        # Convert retrieved chunks into context
        context = "\n".join(results)

        # Generate answer using Gemini
        answer = generate_answer(
            request.question,
            context
        )

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