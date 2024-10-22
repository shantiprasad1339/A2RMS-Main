from fastapi import FastAPI, APIRouter
from assetsissue.model.assetmodel import AssetModel, AssetTable
from employe.models.employemodel import Employeetablecreate, EmployeTable
from bson import ObjectId
from datetime import datetime
import json
router = APIRouter()


@router.post("/api/v1/asset-add")
async def assetAd(body: AssetModel):
    current_date = datetime.now().date()
    listofcount = AssetTable.objects.all()
    count = len(listofcount)
    findUser = EmployeTable.objects.get(id=ObjectId(body.userid))
    savedata = AssetTable(
        assetId = f"{findUser.Prefix}-{count}",
        asset_cretDate = f"{current_date}",
        userid = body.userid,
        assetname = body.assetname,
        assetmodel = body.assetmodel,
        handoverCrt = "N/A"
        
    )
    
    savedata.save()
    tojson = savedata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": f"Asset Isssue Succes to {findUser.Firstname} {findUser.Lastname}",
        "data": fromjson,
        "status": True
    }
    
    
@router.get("/api/v1/get-users-asset/{userid}")
async def usersAssets(userid: str):
    findata = AssetTable.objects(userid=userid).all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message":"here is your all assets",
        "data":fromjson,
        "status": True
    }