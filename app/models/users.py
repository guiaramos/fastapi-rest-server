from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


# PyObjectId is a map from bjson obj id to strs
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('invalid ObjectId')

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


# UserIn describes the schema of User input
class UserIn(BaseModel):
    email: EmailStr
    name: str
    password: str
    password_confirm: str
    display_name: Optional[str]
    photo_url: Optional[str]
    phone_number: Optional[str]


# User describes the schema of User output
class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    display_name: Optional[str]
    photo_url: Optional[str]
    phone_number: Optional[str]


# UserInDB describes the schema of User in DB
class UserInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    hashed_password: str
    name: str
    display_name: Optional[str]
    photo_url: Optional[str]
    phone_number: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
