from .db import SessionLocal
from .models import Document

def seed_database():
    db = SessionLocal()

    sample_documents = [
        Document(
            filename="AI_Research.pdf",
            file_size=204800,
            status="Processed"
        ),
        Document(
            filename="Project_Report.pdf",
            file_size=512000,
            status="Pending"
        ),
        Document(
            filename="User_Guide.pdf",
            file_size=102400,
            status="Processed"
        )
    ]

    db.add_all(sample_documents)
    db.commit()
    db.close()

    print("Sample data inserted successfully!")

if __name__ == "__main__":
    seed_database()
