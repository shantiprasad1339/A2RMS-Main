from fastapi import FastAPI, APIRouter, HTTPException
from Awards.models.awardsmodel import Awardstable, Awardstablecreate
from bson import ObjectId
from datetime import datetime
import json
router = APIRouter()


@router.post("/api/v1/award")
async def create_award(body: Awardstablecreate):
    # Create a new award entry using the validated data from the request body
    savedata = Awardstable(
        Userid=body.Userid,
        Award_type=body.Award_type,
        Award_Name=body.Award_Name,
        Gift=body.Gift,
        Price=body.Price,
        EmployeeName=body.EmployeeName,
        Month=body.Month,
        Year=body.Year
    )
    
    # Save the data to the database
    savedata.save()
    
    # Convert the saved document to JSON format
    tojson = savedata.to_json()
    fromjson = json.loads(tojson)
    
    # Return a response with the saved data
    return {
        "message": "Award data saved successfully",
        "data": fromjson,
        "status": True
    }
@router.get("/api/v1/award/{userid}")
async def get_awards_by_userid(userid: str):
    # Query the database to find all awards for the given Userid
    awards = Awardstable.objects(Userid=userid)

    if not awards:
        raise HTTPException(status_code=404, detail="No awards found for this user.")

    # Convert the query result to JSON format
    awards_json = json.loads(awards.to_json())

    # Return the data in a response
    return {
        "message": f"Awards for user {userid}",
        "data": awards_json,
        "status": True
    }