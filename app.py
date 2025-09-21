import os
import sys
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

agent = Agent(
    name="アシスタント",
    instructions="あなたは役に立つアシスタントです。",
)

result = Runner.run_sync(
    agent,
    "プログラミングに関する俳句を書いてください。",
)

print(result.final_output)
