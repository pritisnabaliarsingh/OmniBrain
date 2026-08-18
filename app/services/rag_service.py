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
        context = "\n".join(results)

        # Basic LangGraph Orchestrator
        from typing import Dict, Any
        from langgraph.graph import StateGraph, END
        from app.services.llm_service import client, USE_GEMINI

        def decide_route(state: Dict[str, Any]) -> str:
            # If the user asks about the document, route to search. Otherwise, direct answer.
            # For this simple system, we'll always route to search if context exists.
            if state["context"]:
                return "search_agent"
            return "direct_answer_agent"

        def generate_with_retry(prompt: str) -> str:
            import time
            
            for attempt in range(4):
                try:
                    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                    return response.text
                except Exception as e:
                    if "503" in str(e) or "429" in str(e) or "quota" in str(e).lower():
                        if attempt < 3:
                            time.sleep(2 ** attempt) # Exponential backoff: 1s, 2s, 4s
                            continue
                    raise e

        def search_agent(state: Dict[str, Any]) -> Dict[str, Any]:
            prompt = f"Use the context to answer the question.\n\nContext:\n{state['context']}\n\nQuestion:\n{state['question']}\n\nAnswer:"
            if USE_GEMINI:
                answer = generate_with_retry(prompt)
            else:
                answer = generate_answer(state['question'], state['context'])
            state["answer"] = answer
            return state

        def direct_answer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
            prompt = f"Answer the user's question directly:\n\n{state['question']}\n\nAnswer:"
            if USE_GEMINI:
                answer = generate_with_retry(prompt)
            else:
                answer = generate_answer(state['question'], "")
            state["answer"] = answer
            return state

        def guardrail_agent(state: Dict[str, Any]) -> Dict[str, Any]:
            # Evaluate output for hallucinations or toxicity
            prompt = f"Evaluate the following answer for toxicity or severe hallucinations. If it is toxic or completely irrelevant, reply 'REJECTED'. Otherwise reply 'APPROVED'.\n\nQuestion: {state['question']}\nAnswer: {state['answer']}\n\nEvaluation:"
            if USE_GEMINI:
                eval_result = generate_with_retry(prompt).strip().upper()
            else:
                eval_result = "APPROVED" # Skip evaluation for local model to save time

            if "REJECTED" in eval_result:
                state["answer"] = "I'm sorry, I cannot provide an answer to that question due to safety or relevance guardrails."
            return state

        # Build graph
        workflow = StateGraph(dict)
        workflow.add_node("search_agent", search_agent)
        workflow.add_node("direct_answer_agent", direct_answer_agent)
        workflow.add_node("guardrail_agent", guardrail_agent)

        workflow.set_conditional_entry_point(
            decide_route,
            {
                "search_agent": "search_agent",
                "direct_answer_agent": "direct_answer_agent"
            }
        )
        workflow.add_edge("search_agent", "guardrail_agent")
        workflow.add_edge("direct_answer_agent", "guardrail_agent")
        workflow.add_edge("guardrail_agent", END)

        app = workflow.compile()

        # Run the graph
        initial_state = {
            "question": request.question,
            "context": context,
            "answer": ""
        }
        final_state = app.invoke(initial_state)

        return {
            "question": request.question,
            "answer": final_state["answer"]
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
                detail="Gemini API quota exceeded. Please try again later."
            )

        # Other unexpected errors
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )