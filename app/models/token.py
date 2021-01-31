from typing import Optional

from pydantic import BaseModel


# Token represents a token schema
class Token(BaseModel):
    access_token: str
    token_type: str


# TokenData represents a token data schema
class TokenData(BaseModel):
    id: Optional[str] = None
