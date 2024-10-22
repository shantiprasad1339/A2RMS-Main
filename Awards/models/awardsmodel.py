from mongoengine import Document, StringField, IntField, BooleanField
from pydantic import BaseModel

class Awardstable(Document):
    Userid = StringField(required = True)
    Award_type = StringField(required = True)
    Award_Name = StringField(required = True)
    Gift = StringField(required = True)
    Price = StringField(required = True)
    EmployeeName = StringField(required = True)
    Month = StringField(required = True)
    Year = StringField(required = True)
    Month = StringField(required = True)

    
    
    

class Awardstablecreate(BaseModel):
    Userid: str
    Award_type: str
    Award_Name: str
    Gift: str
    Price: str 
    EmployeeName: str
    Month: str
    Year: str
