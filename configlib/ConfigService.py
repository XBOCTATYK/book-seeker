from deepmerge import always_merger
from configlib.formatters.ConfigFormatter import ConfigFormatter


class ConfigService:
    _merged_config = {}
    _data_transformers = []

    def __init__(self, *config_formatters: ConfigFormatter):
        for formatter in config_formatters:
            current_config = formatter.get_config()
            finalized_config = self._apply_transformers(current_config)

            always_merger.merge(self._merged_config, finalized_config)

    def config(self) -> dict:
        return self._merged_config

    def extend(self, config_extension: dict):
        always_merger.merge(self._merged_config, config_extension)
        return self._merged_config

    def _apply_transformers(self, config: dict) -> dict:
        return config
