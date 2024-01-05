from dataclasses import dataclass

from DateTime import DateTime


@dataclass
class Event:
    topic: str
    type: str
    data: dict
    created_at: DateTime
