from agents import Agent

from chatter.llm import get_client
from chatter.tools.how_many_jokes import how_many_jokes


def joker_agent():
    client = get_client()

    agent = Agent(
        name="Joker",
        model=client,
        instructions="First state the use intent. If the user wants jokes, first call the `how_many_jokes` tool, then tell that many jokes different from past jokes. If the user wants to tell a joke, first ask for the joke, then tell it. If the user wants to hear a joke, first call the `how_many_jokes` tool, then tell that many jokes different from past jokes.",
        tools=[how_many_jokes],
    )
    return agent
