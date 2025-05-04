import asyncio

import streamlit as st
from agents import Agent, set_tracing_disabled

from chatter.agents.joker import joker_agent
from chatter.agents.utils import process_events, run_streamed
from chatter.settings import DEBUG
from chatter.utils import get_event_loop, initialize_state

set_tracing_disabled(True)

if DEBUG:
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("openai.agents").setLevel(logging.DEBUG)

# emojis
AVATARS = {
    "assistant": "🤖",
    "user": "👤",
    "tool": "🛠️",
}


def render_message(message, streaming=False, container=None):
    content = message["content"]

    role = message["role"]
    avatar_role = role
    if content.startswith("Tool"):
        avatar_role = "tool"

    if container:
        with container:
            st.markdown(content)
    else:
        with st.chat_message(role, avatar=AVATARS.get(avatar_role)):
            container = st.container()
            with container:
                st.markdown(message["content"])
    return container


def render_chat_messages(messages):
    previous_role = None
    container = None
    for message in messages:
        role = message["role"]
        if role != previous_role:
            # Render the message with a different avatar
            container = render_message(message)
        else:
            # Render the message with the same avatar
            container = render_message(message, container=container)
        previous_role = role


def sync_stream(
    stream_gen,
    messages: list = None,
):
    loop = asyncio.get_event_loop()
    while True:
        with st.spinner("Waiting for response..."):
            task = anext(stream_gen, None)
            if task is None:
                break
            message = loop.run_until_complete(task)
            if message is None:
                break
        print(message)
        messages.append(message)
        yield message


def main():
    print("[bold blue]STARTING[/bold blue]")
    st.set_page_config(page_title="Agent Runner", page_icon=":robot_face:")
    st.title("Agent Runner")
    st.caption(
        "This is a simple agent runner. It runs an agent and displays the output."
    )
    agent: Agent = initialize_state("agent", joker_agent())
    messages: list = initialize_state("messages", [])

    render_chat_messages(messages)

    prompt = st.chat_input("What do you want the agent to do?", accept_file=True)

    if prompt and prompt.text:
        # files = prompt.files
        # st.write(files)
        prompt_text = prompt.text

        # Add user message to history and display it
        message = {"role": "user", "content": prompt_text}
        messages.append(message)
        render_message(message)

        # Run the agent
        loop = get_event_loop()
        events_stream = loop.run_until_complete(run_streamed(agent, prompt_text))
        events_stream = process_events(events_stream)

        # Display the result
        stream_gen = sync_stream(events_stream, messages=messages)
        render_chat_messages(stream_gen)


if __name__ == "__main__":
    from rich import print

    main()
