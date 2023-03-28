from sqlalchemy import Column, ForeignKey, Integer, String

from src.app.database.base import BaseModel


class Books(BaseModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(String, ForeignKey("authors.id"))
    total_count = Column(Integer)
    available_count = Column(Integer)
