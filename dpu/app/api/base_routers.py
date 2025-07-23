from fastapi import APIRouter, Depends

from app.api.cloud_router import cloud_router
from app.api.duck_router import duck_router
from app.modules.authentication.authentication_dep import AuthenticationManager

api_v1_router = APIRouter(prefix="/api/v1",
                          tags=["v1"],
                          dependencies = [Depends(AuthenticationManager())]
                          )

api_v1_router.include_router(cloud_router)
api_v1_router.include_router(duck_router)