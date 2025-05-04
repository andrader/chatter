import json
import os
import time


# Function to generate a title for the conversation
def generate_title(messages):
    if len(messages) < 2:  # Need at least one exchange
        return f"Conversation-{time.strftime('%Y%m%d-%H%M%S')}"
    # Simple title generation based on the first user message
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:30].strip()
            return f"{title}-{time.strftime('%Y%m%d-%H%M%S')}"
    return f"Conversation-{time.strftime('%Y%m%d-%H%M%S')}"


# Function to save conversation to JSON
def save_conversation(messages, title):
    os.makedirs("conversations", exist_ok=True)
    filename = f"conversations/{title.replace(' ', '_')}.json"
    with open(filename, "w") as f:
        json.dump(messages, f, indent=2)
    return filename


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = {}

    def add_child(self, key, child_node):
        self.children[key] = child_node

    def get_child(self, key):
        return self.children.get(key)

    def traverse(self):
        nodes = [self]
        while nodes:
            current = nodes.pop(0)
            print(current.data)
            nodes.extend(current.children.values())


def initialize_state(key, default=None, default_factory=None):
    """Initialize a session state variable if it doesn't exist."""
    import streamlit as st

    if key not in st.session_state:
        if default_factory is not None:
            st.session_state[key] = default_factory()
        else:
            st.session_state[key] = default
    return st.session_state[key]


def get_event_loop():
    import asyncio

    try:
        # First try to get the running loop
        loop = asyncio.get_running_loop()
        print("Using existing event loop.")
    except RuntimeError:
        print("No running loop found, creating a new one.")
        # If no event loop exists, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop
