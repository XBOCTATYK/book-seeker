from abc import ABC, abstractmethod

from apps.event_bus.lib.EventFetcher import EventFetcher
from apps.event_bus.model.Event import Event
from apps.event_bus.services.PollManager import PollManager


class BaseConsumer(ABC):
    _topic: str
    _poll_manager: PollManager
    _event_fetcher: EventFetcher

    def __init__(self,
                 topic: str,
                 poll_manager: PollManager,
                 event_fetcher: EventFetcher
                 ):
        self._topic = topic
        self._poll_manager = poll_manager
        self._event_fetcher = event_fetcher

        self._poll_event()

    @abstractmethod
    def on_event(self, event: Event):
        pass

    def _on_event(self):
        for event in self._event_fetcher.fetch_events():
            if event.topic != self._topic:
                continue

            self.on_event(event)

    def _poll_event(self):
        self._poll_manager.add_handler(self.on_event)
