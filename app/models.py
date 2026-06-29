from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    document_type = Column(String, nullable=True)
    status = Column(String, default="pending")
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    raw_text = Column(Text, nullable=True)
    failure_reason = Column(Text, nullable=True)

class Extraction(Base):
    __tablename__ = "extractions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    document_type = Column(String, nullable=True)
    extracted_fields = Column(Text, nullable=True)  # JSON string
    anomalies = Column(Text, nullable=True)          # JSON string
    confidence = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())