from fastapi import APIRouter
from fastapi.responses import JSONResponse 
from roles.models.rolesmodel import RolesModel, RolesTable
import json
router = APIRouter()

@router.post("/api/v1/create-role")
async def createRoles(body: RolesModel):
    saveData = RolesTable(**body.dict())
    saveData.save()
    tojson = saveData.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"Role added",
        "data": fromjson,
        "status": True
    }

@router.get("/api/v1/get-roles-all")
async def getAllRoles():
    data = RolesTable.objects.all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Here is all roles",
        "data": fromjson,
        "status": True
    }