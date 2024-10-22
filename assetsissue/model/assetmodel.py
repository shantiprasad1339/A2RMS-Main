from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class AssetTable(Document):
    assetId = StringField(required=True)
    asset_cretDate = StringField(required=True)
    userid = StringField(required=True)
    assetname = StringField(required=True)
    assetmodel = StringField(required=True)
    handoverCrt = StringField(required=True)
    
    

class AssetModel(BaseModel):

    userid : str
    assetname : str
    assetmodel : str
