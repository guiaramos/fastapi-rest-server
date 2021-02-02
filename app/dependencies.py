from fastapi import HTTPException, status, Request
from jose import jwt, JWTError

from .env import COOKIE_ACCESS_KEY, SECRET_KEY, ALGORITHM
from .models import token as token_models

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="user not authenticated",
)


def get_token_data(token: str):
    # check if the token is found
    if not token:
        raise credentials_exception

    # check if token is valid
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        _id = payload.get('id')

        if _id is None:
            raise credentials_exception

        token_data = token_models.TokenData(id=_id)

        return token_data

    except JWTError:
        raise credentials_exception


# get_token_cookie should return the token received on headers cookies
async def get_token_cookie(request: Request):
    cookies = request.cookies
    # check if the cookie is sent
    if not cookies:
        raise credentials_exception

    token = cookies[COOKIE_ACCESS_KEY]
    token_data = get_token_data(token)

    return token_data
