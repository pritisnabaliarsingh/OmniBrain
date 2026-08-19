from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.models import Base
from backend.database.crud import (
    create_document,
    get_document,
    update_document_status
)


def test_document_crud():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    document = create_document(
        db,
        filename="test.pdf",
        file_size=1000,
        status="Pending"
    )

    assert document.filename == "test.pdf"

    found = get_document(db, document.id)
    assert found is not None

    updated = update_document_status(
        db,
        document.id,
        "Processed"
    )

    assert updated.status == "Processed"

    db.close()
