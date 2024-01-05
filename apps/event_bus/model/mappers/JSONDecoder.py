import json

from common.services.Decoder import Decoder


class JSONDecoder(Decoder):
    _decoder = json.JSONDecoder()

    def decode(self, target: str) -> dict:
        return self._decoder.decode(target)
