# abstract app class
class AbstractApp:
    _config: dict = None

    def __init__(self, config: dict):
        self._config = config

    def start(self):
        print('App started!')
