from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, default='')
    content = Column(Text, nullable=False, default='')
    tags = Column(String(500), nullable=False, default='')  # 逗号分隔
    ai_notes = Column(Text, nullable=True)
    ai_mindmap = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
