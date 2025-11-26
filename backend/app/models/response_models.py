from typing import Any

from pydantic import BaseModel, ConfigDict


class PlanStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    description: str


class IntermediateResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step: PlanStep
    result: dict[str, Any]


class TimelineEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: int
    tool: str
    duration: float


class PlanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan: list[PlanStep]
    steps: list[PlanStep]
    final_summary: str


class ExecuteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan: list[PlanStep]
    intermediate: list[IntermediateResult]
    final_summary: str
    timeline: list[TimelineEntry]
