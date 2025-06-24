from fastapi import APIRouter

from app.api.cloud_router import cloud_router

api_v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

api_v1_router.include_router(cloud_router)
