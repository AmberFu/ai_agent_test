import os
import asyncio
import requests
from agents import Agent, Runner, WebSearchTool, trace
from agents import set_default_openai_key
from dotenv import load_dotenv

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)
# google_webs_earch_apikey = os.getenv("GOOGLE_WEB_SEARCH_APIKEY")
# google_webs_earch_cx = os.getenv("GOOGLE_WEB_SEARCH_CX")


async def main():
    agent = Agent(
        name="Web searcher",
        instructions="You are a apartment searching agent.",
        tools=[
            WebSearchTool(
                # https://platform.openai.com/docs/guides/tools-web-search#user-location
                user_location={
                    "type": "approximate",
                    "country": "TW", 
                    "city": "Taichung",
                    # "region": "London",
                    })],
    )

    with trace("Web search example"):
        result = await Runner.run(
            agent,
            "search the web for 'best movie on 2025'",
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
