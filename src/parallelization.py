import os
import asyncio

from agents import Agent, ItemHelpers, Runner, trace
from agents import set_default_openai_key
from dotenv import load_dotenv
# from agents import enable_verbose_stdout_logging

# enable_verbose_stdout_logging()

load_dotenv()
openai_apikey = os.getenv("OPENAI_APIKEY")
set_default_openai_key(openai_apikey)

"""
This example shows the parallelization pattern. We run the agent three times in parallel, and pick
the best result.
"""

msg_reply_agent = Agent(
    model="gpt-4o-mini",
    name="msg_reply_agent",
    instructions="You reply the user's question in 50 words or less, be concise, relevant and polite.",
)

msg_picker = Agent(
    model="gpt-4o-mini",
    name="msg_picker",
    instructions="You pick the best reply from the given options, choose the one that is most concise, relevant and polite.",
)


async def main():
    msg = input("Hi! What is your question?\n\n") # Hi! I want to know what is LLM and AI agent?

    # Ensure the entire workflow is a single trace
    with trace("Parallel massage reply agent"):
        res_1, res_2, res_3 = await asyncio.gather(
            Runner.run(
                msg_reply_agent,
                msg,
            ),
            Runner.run(
                msg_reply_agent,
                msg,
            ),
            Runner.run(
                msg_reply_agent,
                msg,
            ),
        )

        outputs = [
            ItemHelpers.text_message_outputs(res_1.new_items),
            ItemHelpers.text_message_outputs(res_2.new_items),
            ItemHelpers.text_message_outputs(res_3.new_items),
        ]

        all_replies = "\n\n".join(outputs)
        print(f"\n\Reply:\n\n{all_replies}")

        best_translation = await Runner.run(
            msg_picker,
            f"Input: {msg}\n\nReplies:\n{all_replies}",
        )

    print("\n\n-----")

    print(f"Best reply: {best_translation.final_output}")


if __name__ == "__main__":
    asyncio.run(main())