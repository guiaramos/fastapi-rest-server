from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext

from ..models import users as user_models
from ..repositories.mongo import users as user_repo

# create users router
router = APIRouter()

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


@router.post("/users/", tags=["users"], response_model=user_models.User)
async def create_user(user: user_models.UserIn):
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

    # creates the user on db
    created_user = user_repo.create_one(user_db)

    return user_models.User(**created_user.dict())
