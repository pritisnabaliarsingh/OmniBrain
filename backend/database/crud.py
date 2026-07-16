from sqlalchemy.orm import Session
from .models import Document


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
