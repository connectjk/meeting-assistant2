"""Agent runtime – setup and run loop for meeting-assistant2."""

import os
from openai import AzureOpenAI


SYSTEM_PROMPT = """\
A meeting assistant agent that joins virtual meetings, transcribes conversations in real time, extracts action items, assigns owners, sends follow-up summaries, and schedules follow-up meetings when required.
"""


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-06-01",
    )


async def run_agent() -> None:
    client = _get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Agent ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            messages=messages,
        )

        assistant_msg = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_msg})
        print(f"Agent: {assistant_msg}")
