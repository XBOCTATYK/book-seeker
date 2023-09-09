from deepmerge import always_merger
from configlib.formatters.ConfigFormatter import ConfigFormatter


class ConfigService:
    merged_config = {}

    def __init__(self, *config_formatters: ConfigFormatter):
        for formatter in config_formatters:
            always_merger.merge(self.merged_config, formatter.get_config())

    def config(self) -> dict:
        return self.merged_config
