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


class MessageOutput(BaseModel):
    '''
    This is the actual agent's output type.
    '''
    response: str


# Add an input guardrail agent
class TranslateOutput(BaseModel):
    is_translate: bool
    reasoning: str


input_guardrail_agent = Agent(
    name="Input Guardrail check",
    instructions="Check if the user is asking about translation, return is_translate=True or False otherwise.",
    output_type=TranslateOutput,
)

async def translation_guardrail(ctx, agent, input_data):
    result = await Runner.run(input_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(TranslateOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_translate,
    )


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

# Add the agents as tools
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    output_type=MessageOutput,
)

chinese_agent = Agent(
    name="Chinese agent",
    instructions="You translate the user's message to Chinese",
    output_type=MessageOutput,
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        chinese_agent.as_tool(
            tool_name="translate_to_chinese",
            tool_description="Translate the user's message to Chinese",
        ),
    ],
    input_guardrails=[
        InputGuardrail(guardrail_function=translation_guardrail),
    ],
    output_guardrails=[response_guardrail],
    output_type=MessageOutput,
)

async def main():
    try:
        result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Chinese.")
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print(">>> Input guardrail tripped! It's not translation task.")
    except OutputGuardrailTripwireTriggered:
        print(">>> Output guardrail tripped! The output is too long.")

if __name__ == "__main__":
    asyncio.run(main())