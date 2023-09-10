import json
from configlib.readers.FileTextReader import FileTextReader
from configlib.formatters.ConfigFormatter import ConfigFormatter
from configlib.readers.Reader import Reader


class JsonConfigFormatter(ConfigFormatter):
    reader: Reader = FileTextReader('/config')
    decoder = json.JSONDecoder()
    parsed_config: dict = None

    FILE_FORMAT = '.json'

    def __init__(self, config_name):
        super().__init__()
        try:
            config_str = self.reader.read(config_name + self.FILE_FORMAT)
            self.parsed_config = self.decoder.decode(config_str)
        except FileNotFoundError:
            self.parsed_config = {}

    def get_config(self) -> dict:
        return self.parsed_config
