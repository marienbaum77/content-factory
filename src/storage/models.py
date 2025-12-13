from sqlalchemy import Column, String, Integer, DateTime, func
from .db import Base

class ProcessedUrl(Base):
    __tablename__ = "processed_urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True) # unique=True - защита от дублей
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())