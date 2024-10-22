from mongoengine import Document, StringField, IntField, BooleanField
from pydantic import BaseModel

class AttendanceTable(Document):
    userid = StringField(required=True)
    late = StringField(required=False)
    mark = StringField(required=True)
    date = StringField(required=True)
    