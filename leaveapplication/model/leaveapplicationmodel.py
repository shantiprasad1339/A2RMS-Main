from pydantic import BaseModel
from typing import Optional
from mongoengine import Document, StringField, IntField

# MongoEngine Document
class LeaveTable(Document):
    leave_category = StringField(required=True)
    leave_type = StringField(required=True)
    user_id = StringField(required=True)
    date = StringField(required=True)
    reason = StringField(required=True)
    applied_on = StringField(required=True)
    total_days = IntField(required=True)
    status = StringField(required=True)


# Pydantic model for request validation
class LeaveApplicationCreate(BaseModel):
    leave_category: str
    leave_type: str
    user_id: str
    date: str
    reason: Optional[str] = None
    applied_on: Optional[str] = None
    total_days: Optional[int] = 1
    status:str

# Pydantic model for response
class LeaveApplicationResponse(BaseModel):
    leave_category: str
    leave_type: str
    user_id: str
    date: str
    reason: Optional[str] = None
    applied_on: Optional[str] = None
    total_days: Optional[int]
    status:str

    # Convert MongoDB object to Pydantic model
    @classmethod
    def from_mongo(cls, document: LeaveTable):
        return cls(
            leave_category=document.leave_category,
            leave_type=document.leave_type,
            user_id=document.user_id,
            date=document.date,
            reason=document.reason,
            applied_on=document.applied_on,
            total_days=document.total_days,
            status=document.status,
        )
