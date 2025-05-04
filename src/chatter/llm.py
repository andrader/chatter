import functools

from agents.extensions.models.litellm_model import LitellmModel
from litellm import _turn_on_debug as turn_on_llmlit_debug

from chatter.settings import API_KEY, DEBUG, MODEL

if DEBUG:
    turn_on_llmlit_debug()


@functools.lru_cache(maxsize=1)
def get_client():
    client = LitellmModel(model=MODEL, api_key=API_KEY)
    return client
