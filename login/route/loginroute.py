from fastapi import FastAPI, APIRouter, HTTPException
from employe.models.employemodel import EmployeTable
from bson import ObjectId
import json
from pydantic import BaseModel



router = APIRouter()
class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/api/v1/login")
async def login(login_data: LoginRequest):
    try:
        # Query the EmployeTable to find a match for email and password (phonenumber)
        employee = EmployeTable.objects(Office_email=login_data.email, Phone=login_data.password).first()

        if not employee:
            # Raise an error if no matching employee is found
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Convert the employee object to JSON
        employee_json = json.loads(employee.to_json())

        # Return the full employee data in the response
        return {
            "message": "Login successful",
            "data": employee_json,
            "status": True
        }

    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=str(e))