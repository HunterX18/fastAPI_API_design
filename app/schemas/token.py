from pydantic import BaseModel
from typing import Optional

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    id: Optional[int] = None
