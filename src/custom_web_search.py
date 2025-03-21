import os
import json
import asyncio
import requests
from typing import Dict, Any, Optional, List
from agents import Agent, Runner
from agents.tool import function_tool
from agents.run_context import RunContextWrapper
from agents import set_default_openai_key
from dotenv import load_dotenv

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)
# google_webs_earch_apikey = os.getenv("GOOGLE_WEB_SEARCH_APIKEY")
# google_webs_earch_cx = os.getenv("GOOGLE_WEB_SEARCH_CX")

@function_tool(
    name_override="google_web_search",  # Custom name 
    description_override="Search Google for up-to-date information",  # Custom description
)
def google_search(
    ctx: RunContextWrapper,
    query: str,
    num_results: Optional[int] = None
) -> dict:
    """
    Search the web using Google Search API.
    
    Args:
        ctx: The run context
        query: The search query
        num_results: Number of search results to return (optional)
        
    Returns:
        The search results as a dictionary
    """
    api_key = os.getenv("GOOGLE_WEB_SEARCH_APIKEY")
    cx = os.getenv("GOOGLE_WEB_SEARCH_CX")
    base_url = "https://www.googleapis.com/customsearch/v1"

    # Use a default value for num_results if not provided
    if num_results is None:
        num_results = 5
    
    search_params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": min(num_results, 10)  # Google API limits to 10 results per request
    }
    
    try:
        response = requests.get(base_url, params=search_params)
        response.raise_for_status()
        search_results = response.json()
        
        # Format results for the agent
        formatted_results = []
        if "items" in search_results:
            for item in search_results["items"]:
                formatted_results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })

        return {
            "query": query,
            "results": formatted_results
        }
    except Exception as e:
        return {"error": str(e)}

async def main():
    agent = Agent(
        name="Web searcher",
        instructions="You are a Google search agent.",
        tools=[
            google_search,
        ],
    )
    # Use the agent's result class
    # https://github.com/openai/openai-agents-python/blob/main/src/agents/result.py
    result = await Runner.run(agent, "What are the latest developments in AI?")
    print(result.final_output)

# Example usage
if __name__ == "__main__":    
    asyncio.run(main())
