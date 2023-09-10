from deepmerge import always_merger
from configlib.formatters.ConfigFormatter import ConfigFormatter


class ConfigService:
    _merged_config = {}

    def __init__(self, *config_formatters: ConfigFormatter):
        for formatter in config_formatters:
            always_merger.merge(self._merged_config, formatter.get_config())

    def config(self) -> dict:
        return self._merged_config

    def extend(self, config_extension: dict):
        always_merger.merge(self._merged_config, config_extension)
        return self._merged_config
