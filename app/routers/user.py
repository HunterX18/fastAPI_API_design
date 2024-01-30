from fastapi import APIRouter, HTTPException, status
from app.models.models import UserModel

from app.schemas.user import CreateUserSchema, UserResponseSchema
from app.db.database import db_dependency
from app.utils.password import hash_password

UserRouter = APIRouter(prefix='/users', tags=["Users"])

@UserRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user(user: CreateUserSchema, db: db_dependency):

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@UserRouter.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def get_user(id: int, db: db_dependency):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} not found')

    return user