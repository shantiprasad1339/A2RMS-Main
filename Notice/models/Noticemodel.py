from mongoengine import Document, StringField, IntField, BooleanField
from pydantic import BaseModel

class Noticetable(Document):
    Userid = StringField(required = True)
    Title = StringField(required = True)
    Description = StringField(required = True)
    Attachments = StringField(required = True)
    Date = StringField(required = True)
    Issuedby = StringField(required = True)
   

    
    
    

class Noticetablecreate(BaseModel):
    Userid: str
    Title: str
    Description: str
    Attachments: str 
    Issuedby: str
    Date: str
  
