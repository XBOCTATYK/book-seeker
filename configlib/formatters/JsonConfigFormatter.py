import json
from configlib.readers.FileConfigReader import FileConfigReader
from configlib.formatters.ConfigFormatter import ConfigFormatter
from configlib.readers.ConfigReader import ConfigReader


class JsonConfigFormatter(ConfigFormatter):
    reader: ConfigReader = FileConfigReader('/config')
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
