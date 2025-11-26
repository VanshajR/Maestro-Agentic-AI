from ..models.request_models import PlanRequest
from ..models.response_models import PlanResponse, PlanStep
from .llm import llm_provider


class Planner:
    async def create_plan(self, req: PlanRequest) -> PlanResponse:
        # CRITICAL FIX: Enhanced prompt to prevent "instructional" steps.
        # We force the LLM to generate raw search queries or specific actions.
        prompt = (
            "You are the brain of an autonomous research agent. "
            "Your task is to create a concrete, mechanical execution plan. "
            f"Goal: {req.goal}\n\n"
            "RULES:\n"
            "1. Do NOT generate a 'how-to' guide for a human (e.g., never say 'Open a browser').\n"
            "2. Steps must be specific tool inputs (search queries, URLs to fetch).\n"
            "3. For GitHub, use specific queries like: 'Search GitHub for "
            "\"python web framework\" sorted by stars'.\n"
            "4. For General Info, use: 'Web search for \"latest python frameworks 2024\"'.\n"
            f"Produce up to {req.max_steps} numbered steps."
        )
        
        raw = await llm_provider.complete(prompt)
        lines = [line.strip(" -\t") for line in raw.splitlines() if line.strip()]
        steps: list[PlanStep] = []
        for idx, line in enumerate(lines[: req.max_steps], start=1):
            parts = line.split(".", 1)
            if len(parts) == 2 and parts[0].isdigit():
                content = parts[1].strip()
            else:
                content = line
            # Remove common conversational prefixes if the LLM ignores rules
            for prefix in ["Step:", "Action:", "Command:"]:
                if content.lower().startswith(prefix.lower()):
                    content = content[len(prefix):].strip()
            
            steps.append(PlanStep(id=idx, description=content))

        if not steps:
            steps.append(PlanStep(id=1, description=req.goal))

        formatted_steps = "\n".join(f"{step.id}. {step.description}" for step in steps)
        final_summary = await llm_provider.complete(f"Summarize this plan:\n{formatted_steps}")

        return PlanResponse(plan=steps, steps=steps, final_summary=final_summary)


planner = Planner()