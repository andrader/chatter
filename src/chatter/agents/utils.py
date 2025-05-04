import asyncio
from typing import AsyncGenerator, AsyncIterator

import agents
from agents import Agent, ItemHelpers, Runner, StreamEvent
from rich import print


async def process_events(events_stream: AsyncGenerator) -> AsyncGenerator:
    while True:
        event = await anext(events_stream, None)
        if event is None:
            break
        content = None

        if event.type == "raw_response_event":
            if event.data.type == "response.output_text.delta":
                # print("[bold blue]STREAMMING EVENTS[/bold blue]")
                # content_stream = stream_response(events_stream)
                continue

        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
            # yield dict(role="assistant", content=f"Agent updated: {event.new_agent.name}")

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                content = f"Tool `{event.item.raw_item.name}` was called"
            elif event.item.type == "tool_call_output_item":
                content = f"Tool output: {event.item.output}"
            elif event.item.type == "message_output_item":
                # continue
                ItemHelpers.tool_call_output_item
                content = ItemHelpers.text_message_output(event.item)
            else:
                content = f"* Unknown item type: {event}"

        if content is not None:
            yield dict(role="assistant", content=content)


async def stream_response(events_stream) -> AsyncGenerator:
    print("[bold blue]INSIDE STREAMING RESPONSE[/bold blue]")
    # yield from result.stream_events() while type is not response.content_part.done
    while True:
        await asyncio.sleep(0.5)
        event = await anext(events_stream, None)
        if event is None:
            break
        if event.type == "raw_response_event":
            if event.data.type == "response.output_text.delta":
                yield event.data.delta
                continue
            elif event.data.type == "response.content_part.added":
                continue
            elif event.data.type == "response.output_text.done":
                break
            else:
                break
        else:
            break


async def run_streamed(
    agent: Agent, prompt: str, **kwargs
) -> AsyncIterator[StreamEvent]:
    try:
        return Runner.run_streamed(agent, input=prompt, **kwargs).stream_events()
    except agents.ModelBehaviorError as e:
        raise e
    except agents.MaxTurnsExceeded as e:
        raise e
