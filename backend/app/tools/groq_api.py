import os
import httpx
import logging
from typing import Optional

logger = logging.getLogger("groq_api")

def summarize_query(query: str, max_length: int = 256) -> Optional[str]:
    """
    Use the Groq API to summarize or shorten a query to the specified max length.

    Args:
        query (str): The original query to be shortened.
        max_length (int): The maximum length of the shortened query.

    Returns:
        Optional[str]: The shortened query, or None if the API call fails.
    """
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("Groq API key is missing. Please set the GROQ_API_KEY environment variable.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",  # Updated to a valid model
        "messages": [
            {"role": "system", "content": "Shorten the following query to be concise and under the specified character limit."},
            {"role": "user", "content": f"Query: {query}\nMax Length: {max_length}"}
        ],
        "max_tokens": 100
    }

    try:
        response = httpx.post(api_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        shortened_query = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if len(shortened_query) > max_length:
            shortened_query = shortened_query[:max_length]
        return shortened_query
    except Exception as e:
        logger.error(f"Failed to shorten query using Groq API: {e}")
        return None