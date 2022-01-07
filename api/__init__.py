from fastapi import APIRouter

from .comment_api import router as post_router

router = APIRouter()

router.include_router(prefix="/comments", router=post_router, tags=['Comments'])
