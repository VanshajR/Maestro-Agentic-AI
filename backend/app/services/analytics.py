from typing import Any
import statistics


def simple_stats(durations: list[float]) -> dict[str, Any]:
    if not durations:
        return {"count": 0}
    return {"count": len(durations), "mean": statistics.mean(durations), "max": max(durations), "min": min(durations)}
