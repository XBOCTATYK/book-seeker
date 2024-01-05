from typing import TypedDict


class PollManagerConfig(TypedDict):
    poll_interval: int
    max_workers: int
