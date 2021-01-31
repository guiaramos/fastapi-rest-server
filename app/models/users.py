import datetime
from typing import Optional

from bson.objectid import ObjectId, InvalidId
from pydantic import BaseModel, EmailStr, Field, BaseConfig


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed


# OID is a map from bson obj id to str
class OID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("not a valid ObjectId")

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
class User(MongoModel):
    id: Optional[OID] = Field()
    email: EmailStr
    name: str
    display_name: Optional[str]
    photo_url: Optional[str]
    phone_number: Optional[str]


# UserInDB describes the schema of User in DB
class UserInDB(MongoModel):
    id: Optional[OID] = Field()
    email: str
    hashed_password: str
    name: str
    display_name: Optional[str]
    photo_url: Optional[str]
    phone_number: Optional[str]
