from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import Optional
from leaveapplication.model.leaveapplicationmodel import LeaveApplicationCreate, LeaveTable
import json
from typing import List

app = FastAPI()
router = APIRouter()

# Pydantic model for the request body
class LeaveApplicationCreate(BaseModel):
    leave_category: str
    leave_type: str
    user_id: str
    date: str
    reason: Optional[str] = None
    applied_on: Optional[str] = None
    total_days: Optional[int] = 1

@app.post("/api/v1/apply_leave")
async def apply_leave(body: LeaveApplicationCreate):
    # Create a new leave document in MongoDB using the provided data
    leave = LeaveTable(
        leave_category=body.leave_category,
        leave_type=body.leave_type,
        user_id=body.user_id,
        date=body.date,
        reason=body.reason,
        applied_on=body.applied_on,
        total_days=body.total_days
    )
    
    leave.save()  # Save the leave to the MongoDB database
    
    # Convert the MongoEngine document to a dictionary
    leave_data = json.loads(leave.to_json())
    
    return {
        "message": "Leave Applied Successfully",
        "data": leave_data,
        "status": True
    }
