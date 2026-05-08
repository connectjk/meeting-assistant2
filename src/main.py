"""Entry point for meeting-assistant2."""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from .agent_runtime import run_agent


def main() -> None:
    print("Starting meeting-assistant2...")
    asyncio.run(run_agent())


if __name__ == "__main__":
    main()
