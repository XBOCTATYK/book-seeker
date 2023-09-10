# abstract
class Reader:
    read_str: str = ''

    def read(self, name: str) -> str:
        raise NotImplementedError("ConfigReader is an abstract class!")
