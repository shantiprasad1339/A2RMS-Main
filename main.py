from fastapi import FastAPI, Form,  FastAPI, File, UploadFile, HTTPException
from mongoengine import connect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from Awards.routes import awardsroute
from leaveapplication.model.leaveapplicationmodel import LeaveApplicationCreate, LeaveTable
from Notice.route import Noticeroutes
from assetsissue.model.assetmodel import AssetTable
app = FastAPI()
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from employe.models.employemodel import Employeetablecreate, EmployeTable
from shiftmanegment.model.shiftmodel import ShiftTablecreate, ShiftTable
import json
from datetime import datetime, timedelta
from starlette.middleware.cors import CORSMiddleware
from attendance.routes import attendanceroute
from assetsissue.routes import assetroutes
import io
import os
from boto3 import client
import uuid
from fastapi import FastAPI, Form,  FastAPI, File, UploadFile, HTTPException
from mongoengine import connect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
app = FastAPI()
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from employe.models.employemodel import Employeetablecreate, EmployeTable
from shiftmanegment.model.shiftmodel import ShiftTablecreate, ShiftTable
import json
from datetime import datetime, timedelta
from starlette.middleware.cors import CORSMiddleware
from attendance.routes import attendanceroute
from assetsissue.routes import assetroutes
import io
import os
from typing import Optional
from boto3 import client
import uuid
from pydantic import BaseModel
from attendance.model.attendancemodel import AttendanceTable
from login.route import loginroute
from leaveapplication.route import leaveapplicationroute
from bson import ObjectId
app.add_middleware(
    CORSMiddleware,  # Add the middleware class here
    allow_origins=["*"],  # Allows all origins, replace with specific origins as needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

connect('A2rms', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/A2rms")   
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/login")
async def loginpage( username: str = Form(...), password: str = Form(...)):
    if username == "admin":
        if password == "admin": 
            return RedirectResponse(url="/home")

@app.get("/", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/attendanceReport", response_class=HTMLResponse)
async def attendanceReport(request: Request):
    return templates.TemplateResponse("attendanceReport.html", {"request": request})

@app.get("/leaveApplications", response_class=HTMLResponse)
async def leaveApplications(request: Request):
    return templates.TemplateResponse("leaveApplications.html", {"request": request})
@app.get("/balanceReport", response_class=HTMLResponse)
async def balanceReport(request: Request):
    return templates.TemplateResponse("balanceReport.html", {"request": request})
@app.get("/changepassword", response_class=HTMLResponse)
async def changepassword(request: Request):
    return templates.TemplateResponse("changepassword.html", {"request": request})
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
@app.get("/holidays", response_class=HTMLResponse)
async def holidays(request: Request):
    return templates.TemplateResponse("holidays.html", {"request": request})

@app.get("/leaveReport", response_class=HTMLResponse)
async def leaveReport(request: Request):
    return templates.TemplateResponse("leaveReport.html", {"request": request})
@app.get("/markAttendance/{userid}", response_class=HTMLResponse)
async def markAttendance(request: Request, userid: str):
    findata = AttendanceTable.objects(userid=userid).all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    data = {
        "data": fromjson
    }
    return templates.TemplateResponse("markAttendance.html", {"request": request, **data})
@app.get("/Noticeboard", response_class=HTMLResponse)
async def Noticeboard(request: Request):
    return templates.TemplateResponse("Noticeboard.html", {"request": request})
@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})






@app.get("/awards", response_class=HTMLResponse)
async def awards(request: Request):
    return templates.TemplateResponse("awards.html", {"request": request})

@app.get("/addemployee", response_class=HTMLResponse)
async def addemployee(request: Request):
    return templates.TemplateResponse("addEmployee.html", {"request": request})

@app.get("/perticulerstaff", response_class=HTMLResponse)
async def perticulerUser(request: Request):
    return templates.TemplateResponse("userdetail.html", {"request": request})

@app.get("/addstaff", response_class=HTMLResponse)
async def perticulerUser(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})
def upload_image_to_space(file_content: bytes, filename: str):
    spaces_access_key = 'DO009G8J4HEUMUWVJ4Q4' 
    spaces_secret_key = '+w9XGrS/zvMX6Z4mIk+cMkMTh2LtBApvYb8TfBWHOqs'
    spaces_endpoint_url = 'https://work-pool.blr1.digitaloceanspaces.com'
    spaces_bucket_name = 'socialMedia_songs'

    random_filename = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1]  

    random_filename_with_extension = f"{random_filename}{file_extension}"

    s3 = client('s3',
                 
                region_name='blr1',
                endpoint_url=spaces_endpoint_url,
                aws_access_key_id=spaces_access_key,
                aws_secret_access_key=spaces_secret_key, )

    file_content_stream = io.BytesIO(file_content)

    s3.upload_fileobj(file_content_stream, spaces_bucket_name, random_filename_with_extension,  ExtraArgs={'ACL': 'public-read'})

    return f"{spaces_endpoint_url}/{spaces_bucket_name}/{random_filename_with_extension}"

@app.post("/api/v1/upload")
async def uploadimage( image: UploadFile = File(...), ):
    file_content = await image.read()

    imagepath = upload_image_to_space(file_content, image.filename)
    return {
        "message":"file added",
        "data":imagepath,
        "status":True
    }

@app.post("/api/v1/addstaff")
async def addStaff(body: Employeetablecreate):
    data = EmployeTable(**body.dict())
    data.save()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"Staff Added",
        "data": fromjson,
        "status":True 
    }
    
@app.post("/abcds")
async def abcd(body: ShiftTablecreate):
    userid = body.userid
    user_details = fetch_user_details(userid)

    if user_details:
        current_time = datetime.now()
        shift_in_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        shift_out_time = datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)

        if not shift_in_time or not shift_out_time:
            return {"message": "User shift details are incomplete.", "status": False}

        if body.note.lower() == "intime":
            if current_time < shift_in_time:
                note = f"User logged in early at {current_time}."
            elif current_time > shift_in_time + timedelta(minutes=30):
                note = f"User logged in late at {current_time}. Half day."
            elif current_time > shift_in_time:
                note = f"User logged in late at {current_time}. Late by {(current_time - shift_in_time).seconds // 60} minutes."
            else:
                note = f"User logged in on time at {current_time}."

            data = ShiftTable(userid=userid, note=note, intime=current_time)
        elif body.note.lower() == "outtime":
            if current_time < shift_out_time:
                time_difference = shift_out_time - current_time
                
                if current_time < datetime.now().replace(hour=13, minute=30):
                    note = f"User logged out early at {current_time}. Full leave due to before half day logout."
                elif time_difference > timedelta(hours=1):
                    note = f"User logged out early at {current_time}. Half day due to early logout."
                else:
                    note = f"User logged out early at {current_time}."
                
            else:
                note = f"User logged out on time at {current_time}."

            data = ShiftTable(userid=userid, note=note, outtime=current_time)
            


 




            if current_time < shift_out_time:
                time_difference = shift_out_time - current_time
                
                if time_difference <= timedelta(hours=1):
                    note = f"User logged out early at {current_time}."
                else:
                    note = f"User logged out early at {current_time}. Half day due to early logout."
            else:
                note = f"User logged out on time at {current_time}."

            data = ShiftTable(userid=userid, note=note, outtime=current_time)

        elif body.note.lower() == "startbreak":
            if not data.startbreak or len(data.startbreak) < 2:
                data.startbreak.append(current_time)
                note = f"User started break at {current_time}."
            else:
                return {"message": "Break limit reached. Only two breaks allowed.", "status": False}

        elif body.note.lower() == "endbreak":
            if data.startbreak and (len(data.endbreak) < len(data.startbreak)):
                last_break_start = data.startbreak[-1]
                break_duration = current_time - last_break_start

                if break_duration > timedelta(minutes=20):
                    note = f"User exceeded break time by {break_duration.seconds // 60} minutes. Half day."
                else:
                    note = f"User ended break at {current_time} after {break_duration.seconds // 60} minutes."

                data.endbreak.append(current_time)
            else:
                return {"message": "No break started to end or breaks already ended.", "status": False}

            # Check total break time
            total_break_time = sum([(end - start).seconds for start, end in zip(data.startbreak, data.endbreak)])
            if total_break_time > 20 * 60:
                note += " Total break time exceeded 20 minutes. Half day."

        else:
            return {"message": "Invalid note provided. Use 'intime', 'outtime', 'startbreak', or 'endbreak'.", "status": False}

        # Save data to MongoDB
        data.note = note
        data.save()
        tojson = data.to_json()
        fromjson = json.loads(tojson)

        return {
            "message": "Shift data processed successfully",
            "data": fromjson,
            "status": True
        }
    else:
        return {"message": "User not found", "status": False}

def fetch_user_details(userid):
    # Mock function to simulate fetching user details from MongoDB
    # Replace this with your actual MongoDB query logic
    return {
        "userid": userid,
        "intimeshift": datetime(2024, 8, 23, 10, 0),  # Example shift start time (10:00 AM)
        "outtimeshift": datetime(2024, 8, 23, 18, 0)  # Example shift end time (6:00 PM)
    }
app.include_router(assetroutes.router, tags=["AssetRouts"])
app.include_router(attendanceroute.router, tags=["attendance / Shift"])



app.add_middleware(
    CORSMiddleware,  # Add the middleware class here
    allow_origins=["*"],  # Allows all origins, replace with specific origins as needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

connect('A2rms', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/A2rms")   
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/login")
async def loginpage( username: str = Form(...), password: str = Form(...)):
    if username == "admin":
        if password == "admin": 
            return RedirectResponse(url="/home")

@app.get("/", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/attendanceReport", response_class=HTMLResponse)
async def attendanceReport(request: Request):
    return templates.TemplateResponse("attendanceReport.html", {"request": request})

@app.get("/leaveApplications", response_class=HTMLResponse)
async def leaveApplications(request: Request):
    return templates.TemplateResponse("leaveApplications.html", {"request": request})
@app.get("/balanceReport", response_class=HTMLResponse)
async def balanceReport(request: Request):
    return templates.TemplateResponse("balanceReport.html", {"request": request})
@app.get("/changepassword", response_class=HTMLResponse)
async def changepassword(request: Request):
    return templates.TemplateResponse("changepassword.html", {"request": request})
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
@app.get("/holidays", response_class=HTMLResponse)
async def holidays(request: Request):
    return templates.TemplateResponse("holidays.html", {"request": request})

@app.get("/Leavebalance", response_class=HTMLResponse)
async def Leavebalance(request: Request):
    employes = EmployeTable.objects.all()
    finalList = []
    finalData = {
        "data": finalList
    }

    for employe in employes:
        print(ObjectId(employe.id))
        allleaves = LeaveTable.objects(user_id=str(ObjectId(employe.id))).all()
        if allleaves:
            totaldays = 0 
            totalapplided = 0
            
            for leave in allleaves:
                totalapplided = totalapplided + leave.total_days
                if leave.status == "approved":
                    totaldays = totaldays + leave.total_days

                    
                
            row = {
                "name": f"{employe.Firstname} {employe.Lastname}",
                "totalapproveddays": totaldays,
                "appliedLeaved": totalapplided,
                "balance": 0 if totaldays > 0 else 1 
                 }
            finalList.append(row)
        else:
            print("not found")
                

    print(finalData)
    return templates.TemplateResponse("Leavebalance.html", {"request": request, **finalData})

@app.get("/leaveReport", response_class=HTMLResponse)
async def leaveReport(request: Request):
    return templates.TemplateResponse("leaveReport.html", {"request": request})
@app.get("/markAttendance", response_class=HTMLResponse)
async def markAttendance(request: Request):
    return templates.TemplateResponse("markAttendance.html", {"request": request})
@app.get("/Noticeboard", response_class=HTMLResponse)
async def Noticeboard(request: Request):
    return templates.TemplateResponse("Noticeboard.html", {"request": request})

@app.get("/assests", response_class=HTMLResponse)
async def Assests(request: Request):
    findata = AssetTable.objects.all()
    enriched_data = []  # List to hold asset data with employee names

    # Loop through each asset in findata
    for asset in findata:
        asset_json = json.loads(asset.to_json())  # Convert asset to JSON
        # Query the EmployeTable using the userid from AssetTable
        employee = EmployeTable.objects(id=asset.userid).first()
        
        if employee:
            asset_json['employee_name'] = employee.Firstname  # Add employee's first name to the asset data
        else:
            asset_json['employee_name'] = 'Unknown'  # Handle cases where no employee is found
        
        enriched_data.append(asset_json)  # Add the enriched data to the list

    data = {
        "data": enriched_data
    }

    # Render the template with the enriched data
    return templates.TemplateResponse("assest-issue.html", {"request": request, **data})






@app.get("/awards", response_class=HTMLResponse)
async def awards(request: Request):
    return templates.TemplateResponse("awards.html", {"request": request})



@app.get("/perticulerstaff", response_class=HTMLResponse)
async def perticulerUser(request: Request):
    return templates.TemplateResponse("userdetail.html", {"request": request})

@app.get("/addstaff", response_class=HTMLResponse)
async def perticulerUser(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})
def upload_image_to_space(file_content: bytes, filename: str):
    spaces_access_key = 'DO009G8J4HEUMUWVJ4Q4'
    spaces_secret_key = '+w9XGrS/zvMX6Z4mIk+cMkMTh2LtBApvYb8TfBWHOqs'
    spaces_endpoint_url = 'https://work-pool.blr1.digitaloceanspaces.com'
    spaces_bucket_name = 'socialMedia_songs'

    # Generate a random filename using UUID
    # Generate a random filename using UUID
    random_filename = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1]  # Extract file extension from the original filename

    random_filename_with_extension = f"{random_filename}{file_extension}"

    s3 = client('s3',
                 
                region_name='blr1',
                endpoint_url=spaces_endpoint_url,
                aws_access_key_id=spaces_access_key,
                aws_secret_access_key=spaces_secret_key, )

    # Create a BytesIO object to read file conte nt from memory
    file_content_stream = io.BytesIO(file_content)

    s3.upload_fileobj(file_content_stream, spaces_bucket_name, random_filename_with_extension,  ExtraArgs={'ACL': 'public-read'})

    return f"{spaces_endpoint_url}/{spaces_bucket_name}/{random_filename_with_extension}"

@app.post("/api/v1/upload")
async def uploadimage( image: UploadFile = File(...), ):
    file_content = await image.read()

    # Call the upload function with the random filename and the original file extension
    imagepath = upload_image_to_space(file_content, image.filename)
    return {
        "message":"file added",
        "data":imagepath,
        "status":True
    }

@app.post("/api/v1/addstaff")
async def addStaff(body: Employeetablecreate):
    data = EmployeTable(**body.dict())
    data.save()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"Staff Added",
        "data": fromjson,
        "status":True 
    }
    
@app.post("/abcds")
async def abcd(body: ShiftTablecreate):
    userid = body.userid
    user_details = fetch_user_details(userid)

    if user_details:
        current_time = datetime.now()
        shift_in_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        shift_out_time = datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)

        if not shift_in_time or not shift_out_time:
            return {"message": "User shift details are incomplete.", "status": False}

        if body.note.lower() == "intime":
            # Check if user is logging in
            if current_time < shift_in_time:
                note = f"User logged in early at {current_time}."
            elif current_time > shift_in_time + timedelta(minutes=30):
                note = f"User logged in late at {current_time}. Half day."
            elif current_time > shift_in_time:
                note = f"User logged in late at {current_time}. Late by {(current_time - shift_in_time).seconds // 60} minutes."
            else:
                note = f"User logged in on time at {current_time}."

            data = ShiftTable(userid=userid, note=note, intime=current_time)
        elif body.note.lower() == "outtime":
            # Check if user is logging out
            if current_time < shift_out_time:
                time_difference = shift_out_time - current_time
                
                if current_time < datetime.now().replace(hour=13, minute=30):
                    note = f"User logged out early at {current_time}. Full leave due to before half day logout."
                elif time_difference > timedelta(hours=1):
                    note = f"User logged out early at {current_time}. Half day due to early logout."
                else:
                    note = f"User logged out early at {current_time}."
                
            else:
                note = f"User logged out on time at {current_time}."

            data = ShiftTable(userid=userid, note=note, outtime=current_time)
            


 




            # Check if user is logging out
            if current_time < shift_out_time:
                time_difference = shift_out_time - current_time
                
                if time_difference <= timedelta(hours=1):
                    note = f"User logged out early at {current_time}."
                else:
                    note = f"User logged out early at {current_time}. Half day due to early logout."
            else:
                note = f"User logged out on time at {current_time}."

            data = ShiftTable(userid=userid, note=note, outtime=current_time)

        elif body.note.lower() == "startbreak":
            # User starts a break
            if not data.startbreak or len(data.startbreak) < 2:
                # If no breaks have been taken or only one break has been taken
                data.startbreak.append(current_time)
                note = f"User started break at {current_time}."
            else:
                return {"message": "Break limit reached. Only two breaks allowed.", "status": False}

        elif body.note.lower() == "endbreak":
            # User ends a break
            if data.startbreak and (len(data.endbreak) < len(data.startbreak)):
                # Ensure a break has been started and there's a start without an end
                last_break_start = data.startbreak[-1]
                break_duration = current_time - last_break_start

                if break_duration > timedelta(minutes=20):
                    note = f"User exceeded break time by {break_duration.seconds // 60} minutes. Half day."
                else:
                    note = f"User ended break at {current_time} after {break_duration.seconds // 60} minutes."

                data.endbreak.append(current_time)
            else:
                return {"message": "No break started to end or breaks already ended.", "status": False}

            # Check total break time
            total_break_time = sum([(end - start).seconds for start, end in zip(data.startbreak, data.endbreak)])
            if total_break_time > 20 * 60:
                note += " Total break time exceeded 20 minutes. Half day."

        else:
            return {"message": "Invalid note provided. Use 'intime', 'outtime', 'startbreak', or 'endbreak'.", "status": False}

        # Save data to MongoDB
        data.note = note
        data.save()
        tojson = data.to_json()
        fromjson = json.loads(tojson)

        return {
            "message": "Shift data processed successfully",
            "data": fromjson,
            "status": True
        }
    else:
        return {"message": "User not found", "status": False}

def fetch_user_details(userid):
    # Mock function to simulate fetching user details from MongoDB
    # Replace this with your actual MongoDB query logic
    return {
        "userid": userid,
        "intimeshift": datetime(2024, 8, 23, 10, 0),  # Example shift start time (10:00 AM)
        "outtimeshift": datetime(2024, 8, 23, 18, 0)  # Example shift end time (6:00 PM)
    }



class LeaveApplicationCreate(BaseModel):
    leave_category: str
    leave_type: str
    user_id: str
    date: str
    reason: Optional[str] = None
    applied_on: Optional[str] = None
    total_days: Optional[int] = 1
    status:str

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
        total_days=body.total_days,
        status=body.status,
    )
    
    leave.save()  # Save the leave to the MongoDB database
    
    # Convert the MongoEngine document to a dictionary
    leave_data = json.loads(leave.to_json())
    
    return {
        "message": "Leave Applied Successfully",
        "data": leave_data,
        "status": True
    }

@app.get("/api/v1/leave-get/{userid}")
async def getleaves(userid: str):
    findata = LeaveTable.objects(user_id=userid).all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"here is your all leaves",
        "data":fromjson,
        "status": True
    }
@app.get("/api/v1/total-leave-get")
async def totalleaves():
    findata = LeaveTable.objects.all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"here is your all leaves",
        "data":fromjson,
        "status": True
    }




app.include_router(assetroutes.router, tags=["AssetRouts"])
app.include_router(attendanceroute.router, tags=["attendance / Shift"])
app.include_router(loginroute.router, tags=["Login"])
app.include_router(Noticeroutes.router, tags=["Notice"])
app.include_router(awardsroute.router, tags=["Awards"])






