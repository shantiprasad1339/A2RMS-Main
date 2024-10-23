from mongoengine import Document, StringField, IntField,  BooleanField
from pydantic import BaseModel

class RolesTable(Document):
    name = StringField(required=True)
    powerValue = IntField(required=True)

class RolesModel(BaseModel):
    name : str
    powerValue : int