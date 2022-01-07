from datetime import datetime
from typing import List
from pprint import pprint

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status

from models.comment import Comment, CommentCreate

router = APIRouter()

from core.db import engine


def pagination(skip: int = 0, limit: int = 10):
    return {
        'skip': skip,
        'limit': limit
    }


@router.get("", response_model=List[Comment],
            status_code=status.HTTP_200_OK)
async def get_comments_api(pagination=Depends(pagination)):
    cursor = await engine.find(Comment, skip=pagination['skip'], limit=pagination['limit'])
    return jsonable_encoder(cursor)


@router.get("/{comment_id}", response_model=Comment,
            status_code=status.HTTP_200_OK)
async def get_comment_detail_api(comment_id: str):
    comment = await Comment.find_by_id(comment_id)
    if comment:
        return comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment Not Found")


@router.post("/add-comment", response_model=Comment,
             status_code=status.HTTP_201_CREATED)
async def add_comment_api(model: CommentCreate):
    comment = Comment(created_by=model.name, content=model.content)
    await engine.save(comment)
    return comment


@router.post("/add-reply", response_model=Comment,
             status_code=status.HTTP_201_CREATED)
async def add_reply_api(comment_id: str, model: CommentCreate):
    print(Comment)
    comment =  await Comment.find_by_id(comment_id)
    
    if comment:
        reply = Comment(created_by=model.name, content=model.content)
        await engine.save(reply)
        print(reply)
        comment.add_reply(reply.id)
        await engine.save(comment)
        return reply

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment Not Found")


@router.put("/add-reputation", response_model=Comment,
             status_code=status.HTTP_200_OK)
async def add_reputation_api(comment_id: str, count: int):
    comment = await Comment.find_by_id(comment_id) 
    
    if comment:
        comment.add_reputation(count)
        await comment.save()
        return comment

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment Not Found")


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_api(comment_id: str):
    comment = await Comment.find_by_id(comment_id)
    parents = await engine.find(Comment, { 'replies':  ObjectId(comment_id)  })
    

    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment Not Found")

    await engine.delete(comment)
    for field in parents:
        field.replies.remove(ObjectId (comment_id))
        await engine.save(field)
    
