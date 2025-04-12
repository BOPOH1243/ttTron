from datetime import datetime
from pydantic import BaseModel

class QueryRecordBase(BaseModel):
    address: str

class QueryRecordCreate(QueryRecordBase):
    pass

class QueryRecordResponse(QueryRecordBase):
    id: int
    queried_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True 

class QueryRecordsListResponse(BaseModel):
    records: list[QueryRecordResponse]
    total: int
    page: int
    size: int
