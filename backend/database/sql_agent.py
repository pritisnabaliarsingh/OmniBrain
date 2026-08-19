from sqlalchemy.orm import Session
from .models import Document


def query_documents(db: Session, status: str = None):
    query = db.query(Document)

    if status:
        query = query.filter(Document.status == status)

    return query.all()


def get_document_count(db: Session):
    return db.query(Document).count()
