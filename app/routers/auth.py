from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import db_dependency
from app.schemas.token import TokenSchema
from app.models.models import UserModel
from app.utils.password import verify
from app.utils.oauth import create_access_token

AuthRouter = APIRouter(tags=["Authentication"])

@AuthRouter.post("/login", response_model=TokenSchema)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = db.query(UserModel).filter(UserModel.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")    

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    

