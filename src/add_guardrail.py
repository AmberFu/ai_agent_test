import os
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner
from agents import set_default_openai_key
from agents import InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from agents import output_guardrail, RunContextWrapper, OutputGuardrailTripwireTriggered

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)

# Add an input guardrail agent
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str


input_guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(input_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )


class MessageOutput(BaseModel):
    '''
    This is the actual agent's output type.
    '''
    response: str


# Add an output guardrail agent
class ShortOutput(BaseModel):
    '''
    This is the guardrail's output type.
    '''
    is_short: bool
    reasoning: str


output_guardrail_agent = Agent(
    name="Output Guardrail check",
    instructions="Check if the response less than 50 words, return is_short=True or False otherwise.",
    output_type=ShortOutput,
)

@output_guardrail
async def response_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output.response, context=ctx.context)
    output_word_count = len(output.response.split())

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = output_word_count > 50 or not result.final_output.is_short,
    )

# Add agents
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. "
    "Explain your reasoning at each step and include examples",
    output_guardrails=[response_guardrail],
    output_type=MessageOutput,
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. "
    "Explain important events and context clearly.",
    output_guardrails=[response_guardrail],
    output_type=MessageOutput,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
    output_guardrails=[response_guardrail],
    output_type=MessageOutput,
)

async def main():
    try:
        result = await Runner.run(triage_agent, "who was the first president of the united states?")
        print(result.final_output)

        result = await Runner.run(triage_agent, "what is life")
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print(">>> Input guardrail tripped! It's not homework.")
    except OutputGuardrailTripwireTriggered:
        print(">>> Output guardrail tripped! The output is too long.")

if __name__ == "__main__":
    asyncio.run(main())
