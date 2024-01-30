from pydantic import BaseModel
from datetime import datetime
from .user import UserResponseSchema

class BasePostSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePostSchema(BasePostSchema):
    pass

class UpdatePostSchema(BasePostSchema):
    title: str | None = None
    content: str | None = None

class BasePostResponseSchema(BasePostSchema):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponseSchema
    class Config:
        from_attributes = True

class PostResponseSchema(BaseModel):
    Post: BasePostResponseSchema
    votes: int
    class Config:
        from_attributes = True