from typing import Dict

TOOLS: Dict[str, str] = {
    "web_fetch": "app.tools.web_fetch",
    "github_search": "app.tools.github_search",
    "pdf_extract": "app.tools.pdf_extract",
    "web_search": "app.tools.web_search",
    "summarize": "app.tools.summarize",
}


def list_tools():
    return list(TOOLS.keys())
