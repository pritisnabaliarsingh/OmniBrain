from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, index=True) 
    uploaded_at = Column(DateTime, default=datetime.utcnow, index=True)
    file_size = Column(Integer)
    status = Column(String(50), index=True)
    chunks = relationship("Chunk", back_populates="document")
    history = relationship("ChatHistory", back_populates="document")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    chunk_text = Column(Text)
    chunk_number = Column(Integer)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
   document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    user_question = Column(Text)
    ai_answer = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    document = relationship("Document", back_populates="history")
