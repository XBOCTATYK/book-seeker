import json
from json import JSONDecoder

from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.services.DataFetcher import DataFetcher
from configlib.readers.FileTextReader import FileTextReader
from configlib.readers.Reader import Reader


class LocalFileDataFetcher(DataFetcher):
    _reader: Reader = FileTextReader('./test-example')
    _decoder: JSONDecoder = json.JSONDecoder()

    def fetch(self, fetch_options: FetchOptions) -> dict:
        text = self._reader.read('json-example.json')
        return self._decoder.decode(text)
