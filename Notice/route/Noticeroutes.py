from fastapi import FastAPI, APIRouter, HTTPException
from Notice.models.Noticemodel import Noticetable, Noticetablecreate

import json
router = APIRouter()


@router.post("/api/v1/notice")
async def create_notice(body: Noticetablecreate):
    savedata = Noticetable(
        Userid=body.Userid,
        Title=body.Title,
        Description=body.Description,
        Attachments=body.Attachments,
        Date=body.Date,
        Issuedby=body.Issuedby,

    )
    
    savedata.save()
    
    tojson = savedata.to_json()
    fromjson = json.loads(tojson)
    
    return {
        "message": "Notice data saved successfully",
        "data": fromjson,
        "status": True
    }
@router.get("/api/v1/notice/{userid}")
async def get_notice_by_userid(userid: str):
    awards = Noticetable.objects(Userid=userid)

    if not awards:
        raise HTTPException(status_code=404, detail="No awards found for this user.")

    awards_json = json.loads(awards.to_json())

    return {
        "message": f"Notices for user {userid}",
        "data": awards_json,
        "status": True
    }