from typing import Annotated
from pydantic import BaseModel, Field

class VoteSchema(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]