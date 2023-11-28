from typing import TypedDict


class AppConfig(TypedDict):
    token: str
    poll_interval: int
