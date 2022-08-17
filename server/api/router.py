from fastapi import APIRouter

from server.api.v1 import v1_router

router = APIRouter()
router.include_router(v1_router)
