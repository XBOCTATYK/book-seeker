from dataclasses import dataclass

from common.lib.to_str import to_str


@dataclass
@to_str
class RawDataDecodedDto:
    id: int
    data: dict
    writer: str
    datetime: str
