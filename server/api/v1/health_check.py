from fastapi import APIRouter

from server.enums.status_enum import StatusEnum
from server.schemas.status_schema import StatusSchema

router = APIRouter()


@router.get("/health-check/", response_model=StatusSchema)
async def get_health_check_status():
    """Get health check status"""
    return {"status": StatusEnum.success.value}
