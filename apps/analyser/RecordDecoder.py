import json
from json import JSONDecoder

from common.services.Decoder import Decoder


class RecordDecoder(Decoder):
    _decoder: JSONDecoder = json.JSONDecoder()

    def decode(self, record: str) -> dict:
        result = self._decoder.decode(record)
        print(result)
        return result


