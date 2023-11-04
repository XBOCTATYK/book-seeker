from urllib.parse import urlsplit

from common.services.Decoder import Decoder, T


class DataFromUrlDecoder(Decoder):
    def decode(self, target: str) -> T:
        data = urlsplit(target)

