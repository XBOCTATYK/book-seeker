# abstract
class ConfigFormatter:
    config = {}

    def get_config(self) -> dict:
        raise NotImplementedError("ConfigFormatter is abstract!")
