from fastapi import APIRouter, HTTPException
from fastapi import status
from ..models.request_models import PlanRequest, ExecuteRequest
from ..models.response_models import PlanResponse, ExecuteResponse
from .planner import planner
from .executor import executor

router = APIRouter()


@router.post("/plan", response_model=PlanResponse)
async def create_plan(req: PlanRequest):
    try:
        return await planner.create_plan(req)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/execute", response_model=ExecuteResponse)
async def execute(req: ExecuteRequest):
    try:
        return await executor.execute(req)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
