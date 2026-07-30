from sqlalchemy.orm import Session
from .models import Document
from .models import ChatHistory

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
    from .models import ChatHistory


def create_chat_history(db, document_id, question, answer):
    history = ChatHistory(
        document_id=document_id,
        user_question=question,
        ai_answer=answer
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def get_chat_history(db, document_id):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.document_id == document_id)
        .all()
    )


def delete_chat_history(db, history_id):
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.id == history_id)
        .first()
    )

    if history:
        db.delete(history)
        db.commit()

    return history
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
