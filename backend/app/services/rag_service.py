from typing import Any, Dict

from fastapi import HTTPException

from app.services.embedding_service import create_embeddings
from app.services.llm_service import generate_answer
from app.services.vector_store import search
from app.utils.logger import logger


def ask_rag(request):
    try:
        # Validate question
        if not request.question.strip():
            logger.warning("Empty question received.")
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        logger.info(f"Question received: {request.question}")

        # Create embedding for the user's question
        query_embedding = create_embeddings([request.question])

        # Search similar chunks from FAISS
        results = search(query_embedding[0])
        context = "\n".join(results)

        # LangGraph imports
        from langgraph.graph import END, StateGraph

        from app.services.llm_service import USE_GEMINI, client

        def decide_route(state: Dict[str, Any]) -> str:
            """Decide whether to use document context or direct answering."""
            if state["context"]:
                return "search_agent"

            return "direct_answer_agent"

        def generate_with_retry(prompt: str) -> str:
            """Generate a Gemini response with retry handling."""
            import time

            for attempt in range(4):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                    )
                    return response.text

                except Exception as e:
                    error_message = str(e)

                    if (
                        "503" in error_message
                        or "429" in error_message
                        or "quota" in error_message.lower()
                    ):
                        if attempt < 3:
                            time.sleep(2**attempt)
                            continue

                    raise

            raise RuntimeError("Failed to generate response.")

        def search_agent(state: Dict[str, Any]) -> Dict[str, Any]:
            """Answer using retrieved document context."""
            prompt = (
                "Use the context to answer the question.\n\n"
                f"Context:\n{state['context']}\n\n"
                f"Question:\n{state['question']}\n\n"
                "Answer:"
            )

            if USE_GEMINI:
                answer = generate_with_retry(prompt)
            else:
                answer = generate_answer(
                    state["question"],
                    state["context"],
                )

            state["answer"] = answer
            return state

        def direct_answer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
            """Answer directly without document context."""
            prompt = (
                "Answer the user's question directly:\n\n"
                f"{state['question']}\n\n"
                "Answer:"
            )

            if USE_GEMINI:
                answer = generate_with_retry(prompt)
            else:
                answer = generate_answer(
                    state["question"],
                    "",
                )

            state["answer"] = answer
            return state

        def guardrail_agent(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            Check the generated answer for obvious toxicity
            or severe irrelevance.
            """
            prompt = f"""
You are a response quality checker for a document-question-answering system.

Evaluate the generated answer using these rules:

1. APPROVED if the answer reasonably addresses the user's question.
2. APPROVED if the answer summarizes, explains, extracts, or describes
   information from the uploaded document.
3. APPROVED if the document contains personal, educational, employment,
   application, financial, or other ordinary document information.
4. REJECTED only if the answer contains clearly harmful/toxic content
   or is completely unrelated to the user's question.
5. Do not reject an answer simply because the document contains
   sensitive-looking or personal information.

Return ONLY one word:

APPROVED

or

REJECTED

Question:
{state['question']}

Answer:
{state['answer']}
"""

            if USE_GEMINI:
                eval_result = generate_with_retry(prompt).strip().upper()
            else:
                eval_result = "APPROVED"

            if eval_result == "REJECTED":
                logger.warning(
                    "Guardrail rejected response for question: "
                    f"{state['question']}"
                )

                state["answer"] = (
                    "I couldn't provide that answer because the generated "
                    "response failed the safety/quality check."
                )

            return state

        # Build LangGraph workflow
        workflow = StateGraph(dict)

        workflow.add_node("search_agent", search_agent)
        workflow.add_node("direct_answer_agent", direct_answer_agent)
        workflow.add_node("guardrail_agent", guardrail_agent)

        workflow.set_conditional_entry_point(
            decide_route,
            {
                "search_agent": "search_agent",
                "direct_answer_agent": "direct_answer_agent",
            },
        )

        workflow.add_edge("search_agent", "guardrail_agent")
        workflow.add_edge("direct_answer_agent", "guardrail_agent")
        workflow.add_edge("guardrail_agent", END)

        app = workflow.compile()

        # Run the graph
        initial_state = {
            "question": request.question,
            "context": context,
            "answer": "",
        }

        final_state = app.invoke(initial_state)

        return {
            "question": request.question,
            "answer": final_state["answer"],
        }

    except HTTPException:
        raise

    except Exception as e:
        error_message = str(e)

        logger.error(f"RAG Error: {error_message}")

        # Gemini quota / rate-limit error
        if "429" in error_message or "quota" in error_message.lower():
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later.",
            )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )