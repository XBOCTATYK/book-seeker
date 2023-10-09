import json
from json import JSONDecoder

from common.services.Decoder import Decoder


class RecordDecoder(Decoder):
    _decoder: JSONDecoder = json.JSONDecoder()

    def decode(self, record: str) -> dict:
        return self._decoder.decode(record)


