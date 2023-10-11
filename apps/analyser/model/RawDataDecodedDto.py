from dataclasses import dataclass


@dataclass
class RawDataDecodedDto:
    id: int
    data: dict
    writer: str
    datetime: str
