from agents import Agent, Runner
from agents import set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish")

result = Runner.run_sync(spanish_agent, "Say 'Hello Wolrd' in Spanish")
print(result.final_output)
# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
