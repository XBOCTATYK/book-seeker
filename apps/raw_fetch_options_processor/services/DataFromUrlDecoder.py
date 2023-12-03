from urllib.parse import urlsplit, parse_qs, SplitResult

from common.services.Decoder import Decoder, T


class DataFromUrlDecoder(Decoder):
    def decode(self, target: str) -> T:
        data: SplitResult = urlsplit(target)
        qs = parse_qs(data.query)
        result = dict(map(lambda item: (item[0], item[1][0]), qs.items()))

        return result
