from pydantic import BaseModel, Field, ConfigDict


class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal: str = Field(..., description="Natural language goal")
    max_steps: int = Field(5, ge=1, le=20, description="Maximum steps to decompose into")


class ExecuteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_request: PlanRequest
