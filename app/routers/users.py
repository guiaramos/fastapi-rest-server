from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Response
from jose import jwt
from passlib.context import CryptContext
from pymongo import errors

from ..models import users as user_models, token as token_models
from ..repositories.mongo import users as user_repo

# create users router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={status.HTTP_400_BAD_REQUEST: {"detail": "passwords not match"}},
)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "0a19e92911da2a0d3a5088d3cafc978cf3089ab966c1c5c2b37ac70981c19ee6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_ACCESS_KEY = "todo.access-token"

# pwd_context create a crypto context for hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# check_confirm_password checks if the password has been confirmed by the user
def check_confirm_password(pass1: str, pass2: str):
    if pass1 != pass2:
        return False
    return True


# get_password_hash return the hashed assword
def get_password_hash(password: str):
    return pwd_context.hash(password)


# create_access_token creates a access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


# create_access_cookie send cookie with the response
def create_access_cookie(response: Response, value: str, max_age: int):
    response.set_cookie(
        key=COOKIE_ACCESS_KEY,
        value=value,  # access_token
        # domain='localhost' must be set for production,
        max_age=max_age,  # lifetime of the cookie, should match with the cookie
        # secure=True,  # can be sent on https only, must be set for production
        httponly=True  # javascript cant access the cookie
    )
    return


@router.post("/", response_model=user_models.User)
async def create_user(user: user_models.UserIn, response: Response, coll=Depends(user_repo.get_user_collection)):
    # check if the confirm password matches with the password
    if not check_confirm_password(user.password, user.password_confirm):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords not match")

    # gets the hashed password
    hashed_password = get_password_hash(user.password)

    # creates a user for insert on db
    user_db = user_models.UserInDB(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        display_name=user.display_name,
        photo_url=user.photo_url,
        phone_number=user.phone_number
    )

    try:
        # creates the user on db
        created_user = user_repo.create_one(coll, user_db)

        # creates access_token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data = token_models.TokenData(id=created_user.id)
        access_token = create_access_token(access_token_data.dict(), access_token_expires)

        # add cookie to header
        create_access_cookie(response, access_token, access_token_expires.seconds)

        return user_models.User(**created_user.dict())

    except errors.DuplicateKeyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[e.details])
