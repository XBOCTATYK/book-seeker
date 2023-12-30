from typing import TypedDict


class BotConfig(TypedDict):
    token: str
    poll_interval: int
    user: int
