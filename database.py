from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Note model
class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)


# Summary model - stores AI-generated summaries
class SummaryDB(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    summary_text = Column(Text, nullable=False)
    note_count = Column(Integer, nullable=False)  # How many notes were summarized
    timestamp = Column(DateTime, default=datetime.now)


# Create tables
Base.metadata.create_all(bind=engine)
