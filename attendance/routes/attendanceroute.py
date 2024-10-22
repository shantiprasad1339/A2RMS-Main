from fastapi import FastAPI, APIRouter
from attendance.model.attendancemodel import AttendanceTable
from employe.models.employemodel import EmployeTable
from bson import ObjectId
from datetime import datetime
import json



router = APIRouter()
def timecheker(time, userid):
    findUser = EmployeTable.objects.get(id=ObjectId(userid))
    if time < findUser.Intime or findUser.Outtime <= time:
        if(time >= findUser.halfdaytime):
            return "HD" 
        elif (time<=findUser.halfdaytime):
            return "P Late"
        else:
            return "P"
    
@router.get("/api/v1/checkin-update/{userid}/date")
async def updateAttendance(userid: str):
    today = datetime.now().date()
    findata = AttendanceTable.objects(userid=f"{userid}", date=f"{today}").first()
    if findata:
        now = datetime.now()
        mark = ""
        formatted_time = now.strftime("%H:%S")
        findUser = EmployeTable.objects.get(id=ObjectId(userid))
        if f"{formatted_time}" < findUser.Intime or findUser.Outtime <= f"{formatted_time}":
            if(f"{formatted_time}" >= findUser.halfdaytime):
               mark = "HD" 
            elif (f"{formatted_time}"<=findUser.halfdaytime):
               mark = "P Late"
            else:
               mark =  "P"
        findata.mark = mark
        findata.save()
        return {
            "message":"Attendance marked",
            "status":True
        }
    else:
        now = datetime.now()
        formatted_time = now.strftime("%H:%S")
        mark = ""
        findUser = EmployeTable.objects.get(id=ObjectId(userid))
        if f"{formatted_time}" < findUser.Intime or findUser.Outtime <= f"{formatted_time}":
            if(f"{formatted_time}" >= findUser.halfdaytime):
               mark = "HD" 
            elif (f"{formatted_time}"<=findUser.halfdaytime):
               mark = "P Late"
            else:
               mark =  "P"
        
        saveData = AttendanceTable(
            userid = f"{userid}",
            mark = mark,
            date = f"{today}"
        )
        saveData.save()
        return {
            "message":"Attendance marked",
            "status":True
        }
           
           





@router.get("/api/v1/get-attendance/{userid}")
async def getAttendance(userid: str):
    findata = AttendanceTable.objects(userid=userid).all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "meessage":"here is your attendance",
        "data": fromjson,
        "status":True
    }