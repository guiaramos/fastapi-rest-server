from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, status, Depends, Response
from jose import jwt
from passlib.context import CryptContext

from ..dependencies import get_token_cookie
from ..env import COOKIE_ACCESS_KEY, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.token import TokenData
from ..models.users import UserIn, UserInDB, User, OID, UserSignIn
from ..repositories.mongo import users as user_repo

# create users router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={status.HTTP_400_BAD_REQUEST: {"detail": "passwords not match"},
               status.HTTP_401_UNAUTHORIZED: {"detail": "could not validate credentials"},
               status.HTTP_404_NOT_FOUND: {"detail": "user not found"}},
)

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


# delete_access_cookie deletes the access cookie
def delete_access_cookie(response: Response):
    response.delete_cookie(key=COOKIE_ACCESS_KEY)
    return


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


# create_user_on_db creates a user on database
def create_user_on_db(user_in: UserIn, hashed_password: str, coll=Depends(user_repo.get_user_collection)) -> User:
    # creates a user for insert on db
    user_db = UserInDB(
        email=user_in.email,
        hashed_password=hashed_password,
        name=user_in.name,
        display_name=user_in.display_name,
        photo_url=user_in.photo_url,
        phone_number=user_in.phone_number
    )

    stored_user = user_repo.create_one(coll, user_db)

    return stored_user


# get_user_on_db gets te user on database
def get_user_on_db(_id: str, coll: user_repo.get_user_collection) -> User:
    store_user = user_repo.find_one(coll, _id)
    if store_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return User(**store_user.dict())


# verify_password checks if plain_password matches with the hashed_password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# authenticate_user returns the authenticated user
def authenticate_user(coll: user_repo.get_user_collection, email: str, password: str) -> Union[User, bool]:
    user = user_repo.find_one_by_email(coll, email)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return User(**user.dict())


# get_current_user returns the current user
async def get_current_user(token_data: TokenData, coll: user_repo.get_user_collection) -> User:
    _id = token_data.id
    current_user = get_user_on_db(_id, coll=coll)
    return current_user


# add_access_cookie adds the cookie to the header
def add_access_cookie(response: Response, _id: Optional[OID]):
    # creates access_token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = TokenData(id=str(_id))
    access_token = create_access_token(access_token_data.dict(), access_token_expires)

    # add cookie to header
    create_access_cookie(response, access_token, access_token_expires.seconds)


@router.post("/", response_model=User)
async def create_user(user_in: UserIn, response: Response, coll=Depends(user_repo.get_user_collection)):
    # check if the confirm password matches with the password
    if not check_confirm_password(user_in.password, user_in.password_confirm):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords not match")

    # gets the hashed password
    hashed_password = get_password_hash(user_in.password)

    # creates the user on db
    created_user = create_user_on_db(user_in, hashed_password, coll)

    # creates and add access cookie
    add_access_cookie(response, created_user.id)

    return created_user


@router.get("/me/", response_model=User)
async def get_me(coll=Depends(user_repo.get_user_collection), token_data: TokenData = Depends(get_token_cookie)):
    # return the current user
    return await get_current_user(token_data, coll)


@router.post("/sign-in/", response_model=User)
async def sign_in(user_sign_in: UserSignIn, response: Response, coll=Depends(user_repo.get_user_collection)):
    # get the information is correct
    user = authenticate_user(coll, email=user_sign_in.email, password=user_sign_in.password)

    # if the user is not authenticated send the unauthorized and delete the cookie
    if not user:
        delete_access_cookie(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # creates and add access cookie
    add_access_cookie(response, user.id)

    return user
