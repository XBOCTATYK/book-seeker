# abstract app class
class AbstractApp:
    _config: dict = None
    _is_started: bool = False

    def __init__(self, config: dict):
        self._config = config

    def start(self):
        self._is_started = True
        print('App started!')

    def stop(self):
        self._is_started = False
        print('App stopped!')
