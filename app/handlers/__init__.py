from fastapi import APIRouter
from app.handlers.blockchain.api import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/bc", tags=["blockchain"])


@router.get("/")
async def api_root():
    return {"ping": "pong"}
