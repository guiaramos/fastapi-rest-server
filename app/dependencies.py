from typing import Optional

from fastapi import Cookie, HTTPException, status
from jose import jwt, JWTError

from .env import COOKIE_ACCESS_KEY, SECRET_KEY, ALGORITHM
from .models import token as token_models

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials",
)


# get_token_cookie should return the token received on headers cookies
async def get_token_cookie(token: Optional[str] = Cookie(COOKIE_ACCESS_KEY)):
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

    except JWTError:
        raise credentials_exception

    return token_data
