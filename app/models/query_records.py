from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class QueryRecord(Base):
    __tablename__ = "query_records"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    queried_at = Column(DateTime(timezone=True), server_default=func.now())
