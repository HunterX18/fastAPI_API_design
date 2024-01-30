from typing import List, Annotated, Optional
from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy import func
from app.models.models import UserModel, PostModel, VoteModel
from app.schemas.post import CreatePostSchema, BasePostResponseSchema, PostResponseSchema, UpdatePostSchema
from app.db.database import db_dependency
from app.utils.oauth import get_current_user

PostRouter = APIRouter(prefix="/posts", tags=["Posts"])

@PostRouter.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponseSchema])
def getAllPosts(db: db_dependency, limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    posts = (
        db.query(PostModel, func.count(VoteModel.post_id).label("Votes"))
        .outerjoin(VoteModel, PostModel.id == VoteModel.post_id)
        .group_by(PostModel.id)
        .filter(PostModel.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # pydantic could not convert posts to List[PostResponseSchema] for some reason, so converting manually
    return [{"Post": post[0], "votes": post[1]} for post in posts]


@PostRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=BasePostResponseSchema)
def createPost(post: CreatePostSchema, db: db_dependency, current_user: Annotated[UserModel, Depends(get_current_user)]):
    new_post = PostModel(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

@PostRouter.get("/{id}", status_code=status.HTTP_200_OK, response_model=BasePostResponseSchema)
def getPost(id: int, db: db_dependency):
    post = (
            db.query(PostModel, func.count(VoteModel.post_id).label("Votes"))
            .outerjoin(VoteModel, PostModel.id == VoteModel.post_id)
            .group_by(PostModel.id)
            .filter(PostModel.id == id)
            .first()
    ) 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    # pydantic could not convert posts to List[PostResponseSchema] for some reason, so converting manually
    return { 'Post': post[0], "votes": post[1] }


@PostRouter.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=BasePostResponseSchema)
def updatePost(id: int, post: UpdatePostSchema, db: db_dependency, current_user: Annotated[UserModel, Depends(get_current_user)]):
    db_post = db.query(PostModel).filter(PostModel.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised")

    update_post = post.model_dump(exclude_unset=True)
    for key, val in update_post.items():
        setattr(db_post, key, val)

    db.commit()
    db.refresh(db_post)
    return db_post


@PostRouter.delete("/{id}")
def deletePost(id: int, db: db_dependency, current_user: Annotated[UserModel, Depends(get_current_user)]):
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised")

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)