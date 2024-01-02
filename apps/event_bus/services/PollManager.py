from abc import ABC
from typing import Callable, Any

PollHandler = Callable[[Any], None]


class PollManager(ABC):
    _poll_handlers = []

    def __init__(self, poll_handlers: list[PollHandler]):
        self._poll_handlers = poll_handlers

    def start(self):
        pass

    def stop(self):
        pass

    def add_handler(self, handler: PollHandler):
        self._poll_handlers.append(handler)
