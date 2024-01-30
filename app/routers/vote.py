
from typing import List, Annotated, Optional
from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.models.models import UserModel, VoteModel, PostModel
from app.schemas.vote import VoteSchema
from app.db.database import db_dependency
from app.utils.oauth import get_current_user

VoteRouter = APIRouter(prefix="/vote", tags=["Votes"])

@VoteRouter.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteSchema, db: db_dependency, current_user: Annotated[UserModel, Depends(get_current_user)]):

    post = db.query(PostModel).filter(PostModel.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")

    found_vote = db.query(VoteModel).filter(VoteModel.post_id == vote.post_id, VoteModel.user_id == current_user.id).first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = VoteModel(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return { "message": "vote successfully added "}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote not found")
        db.delete(found_vote)
        db.commit()
        return { "message": "vote successfully deleted" }