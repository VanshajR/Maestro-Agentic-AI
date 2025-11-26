from typing import Any
import asyncio
import logging

from ..models.request_models import ExecuteRequest
from ..models.response_models import (
    ExecuteResponse,
    IntermediateResult,
    TimelineEntry,
)
from .planner import planner
from .llm import llm_provider
from ..tools import web_fetch, github_search, pdf_extract, web_search, summarize


# Ensure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("executor")

class Executor:
    async def execute(self, req: ExecuteRequest) -> ExecuteResponse:
        try:
            # 1. Generate the plan
            plan_resp = await planner.create_plan(req.plan_request)
            
            intermediate: list[IntermediateResult] = []
            timeline: list[TimelineEntry] = []
            loop = asyncio.get_running_loop()

            # 2. Execute each step
            for step in plan_resp.steps:
                desc = step.description
                tool_name = self.select_tool(desc)
                
                logger.info(f"Executing Step {step.id}: {desc} | Tool: {tool_name}")
                start = loop.time()
                
                result_data = None
                try:
                    if tool_name == "web_fetch":
                        result_data = await web_fetch.fetch(desc)
                    elif tool_name == "github_search":
                        result_data = await github_search.search(desc)
                    elif tool_name == "pdf_extract":
                        result_data = await pdf_extract.extract(desc)
                    elif tool_name == "web_search":
                        result_data = await web_search.search(desc)
                    else:
                        result_data = await summarize.summarize_text(desc)
                except Exception as tool_error:
                    logger.error(f"Tool {tool_name} failed: {tool_error}")
                    # Instead of crashing, record the error so the agent can continue or report it
                    result_data = {"error": f"Tool execution failed: {str(tool_error)}"}
                
                end = loop.time()

                timeline.append(TimelineEntry(step_id=step.id, tool=tool_name, duration=end - start))
                intermediate.append(IntermediateResult(step=step, result=result_data))

            # 3. Synthesize results
            # SAFETY: Truncate individual results to avoid sending massive text blobs to the LLM
            # We limit each step's output to 2000 characters for the final prompt.
            result_blobs = []
            for item in intermediate:
                # Convert result to string and strictly limit its length
                content_str = str(item.result)
                if len(content_str) > 2000:
                    content_str = content_str[:2000] + "...[truncated]"
                result_blobs.append(f"Step {item.step.id} ({item.step.description}) => {content_str}")

            result_blob = "\n".join(result_blobs)
            
            # Final safety check: Ensure total prompt size is within reasonable limits (e.g. ~25k chars)
            if len(result_blob) > 25000:
                result_blob = result_blob[:25000] + "\n[...Total output truncated due to length safety...]"

            merged_summary = await llm_provider.complete(
                "Combine the following agent execution outputs into a concise report:\n" + result_blob
            )

            return ExecuteResponse(
                plan=plan_resp.plan,
                intermediate=intermediate,
                final_summary=merged_summary,
                timeline=timeline,
            )
        except Exception as executor_error:
            logger.error(f"Executor failed: {executor_error}")
            raise executor_error

    def select_tool(self, description: str) -> str:
        d = description.lower()
        if "github" in d or "repo" in d:
            return "github_search"
        if d.startswith("fetch") or d.startswith("open") or d.startswith("visit") or "http" in d:
            return "web_fetch"
        if d.endswith(".pdf") or "pdf" in d:
            return "pdf_extract"
        if "search" in d or "google" in d or "serp" in d:
            return "web_search"
        return "summarize"


# Export the instance for usage in router.py
executor = Executor()