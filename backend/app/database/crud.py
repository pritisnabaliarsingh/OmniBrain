from sqlalchemy.orm import Session
from .models import Document, ChatHistory, ChatSession


def create_document(db: Session, filename: str, file_size: int, status: str):
    document = Document(
        filename=filename,
        file_size=file_size,
        status=status
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()


def get_all_documents(db: Session):
    return db.query(Document).all()


def update_document_status(db: Session, document_id: int, status: str):
    document = get_document(db, document_id)

    if document:
        document.status = status
        db.commit()
        db.refresh(document)

    return document


def delete_document(db: Session, document_id: int):
    document = get_document(db, document_id)

    if document:
        db.delete(document)
        db.commit()

    return document
def create_chat_history(db: Session, document_id: int, question: str, answer: str):
    history = ChatHistory(
        document_id=document_id,
        user_question=question,
        ai_answer=answer
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_chat_history(db: Session, document_id: int):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.document_id == document_id)
        .all()
    )


def delete_chat_history(db: Session, history_id: int):
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.id == history_id)
        .first()
    )

    if history:
        db.delete(history)
        db.commit()

    return history


def create_chat_session(db: Session, document_id: int):
    session = ChatSession(document_id=document_id)

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_chat_session(db: Session, session_id: str):
    return (
        db.query(ChatSession)
        .filter(ChatSession.session_id == session_id)
        .first()
    )
def get_documents_by_status(db: Session, status: str):
    return db.query(Document).filter(Document.status == status).all()
def get_document_metadata(db: Session, document_id: int):
    document = get_document(db, document_id)

    if document:
        return {
            "id": document.id,
            "filename": document.filename,
            "file_size": document.file_size,
            "status": document.status
        }

    return None
