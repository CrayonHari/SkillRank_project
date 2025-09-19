# db.py - database setup using SQLAlchemy

from sqlalchemy import JSON, create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Create a local SQLite database file named documents.db
engine = create_engine("sqlite:///documents.db", echo=False)

# Base class for our models
Base = declarative_base()

# Table: Document
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    predicted_type = Column(String, nullable=True)
    field_report = Column(JSON, nullable=True)
    improvement_report = Column(JSON, nullable=True)


# Create tables (if they don't exist)
Base.metadata.create_all(engine)


# Add this in db.py temporarily before SessionLocal
Base.metadata.drop_all(engine)   # WARNING: deletes existing data
Base.metadata.create_all(engine) # Recreates tables with new columns

# Session factory
SessionLocal = sessionmaker(bind=engine)
