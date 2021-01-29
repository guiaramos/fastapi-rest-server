from typing import Optional

from fastapi import APIRouter, HTTPException, status
from firebase_admin import auth
from pydantic import BaseModel, EmailStr

# create users router
router = APIRouter()


# UserIn describes the schema of User input
class UserIn(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


# UserInDB describes the schema of User in DB
class UserInDB(BaseModel):
    uid: str
    provider_id: str
    email: str
    display_name: Optional[str]
    photo_url: Optional[str]
    phone_number: Optional[str]


# save_user_to_db saves user on firebase
def save_user_to_firebase(user: UserIn):
    try:
        fire_user = auth.create_user(email=user.email, password=user.password)
    except auth.EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{"msg": str(e)}])

    return UserInDB(uid=fire_user.uid, provider_id=fire_user.provider_id, email=fire_user.email,
                    display_name=fire_user.display_name, photo_url=fire_user.photo_url,
                    phone_number=fire_user.phone_number)


@router.post("/users/", tags=["users"], response_model=UserInDB)
async def create_user(user: UserIn):
    # check if the confirm password matches with the password
    if user.password != user.password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords not match")

    return save_user_to_firebase(user)
