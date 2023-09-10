import os.path
import os
from configlib.readers.Reader import Reader


class FileTextReader(Reader):
    config_base_path = None
    config_str = None

    def __init__(self, config_dir):
        super().__init__()
        self.config_base_path = os.path.normpath(os.getcwd() + config_dir)

    def read(self, config_name: str) -> str:
        path = os.path.normpath(self.config_base_path + '/' + config_name)
        file = open(path, 'r')
        config_str = file.read()
        file.close()
        return config_str

