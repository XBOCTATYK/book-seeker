class DataProvider:
    name = 'abstract'

    def get_name(self):
        return self.name

    def connect(self):
        return None

    def disconnect(self):
        return None

    def get_connection(self):
        return None
