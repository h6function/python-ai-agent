import gradio as gr
import os
import sys
from agents import Agent, Runner
from dotenv import load_dotenv
from typing import List


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

assistant = Agent(
    name="アシスタント",
    instructions="あなたは役に立つアシスタントです。",
)


with gr.Blocks() as app:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox()
    clear = gr.ClearButton(chatbot)
    chat_history: List[gr.ChatMessage] = []


    async def _submit_func(message: str, chat_history: List[gr.ChatMessage]):
        chat_history.append(gr.ChatMessage(
            role="user",
            content=message,
        ))

        chat_history.append(gr.ChatMessage(
            role="assistant",
            content="いま考えてるからちょっと待ってください...",
        ))

        yield "", chat_history

        result = await Runner.run(
            starting_agent=assistant,
            input=message,
        )

        chat_history[-1].content = result.final_output
        yield "", chat_history


    msg.submit(
        fn=_submit_func,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
    )


def authentication_func(username: str, password: str) -> bool:
    # TODO: Need to implement authentication
    if password != "invalid":
        return True

    return False


if __name__ == "__main__":
    app.launch(auth=authentication_func)
