# Add a few more agents
from agents import Agent, Runner
from agents import set_default_openai_key
from dotenv import load_dotenv
import os

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. "
    "Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. "
    "Explain your reasoning at each step and include examples",
)

# Define your handoffs
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)

# Run the agent orchestration
async def main():
    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)

# Run the main function
import asyncio
asyncio.run(main())
# Output:
# The capital of France is Paris.   