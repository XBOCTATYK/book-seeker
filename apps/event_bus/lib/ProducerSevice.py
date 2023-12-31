from datasource.DbLikeDataSource import DbLikeDataSource


class ProducerService:
    _config: dict
    _topic: str
    _data_source: DbLikeDataSource

    def __init__(self, config: dict, data_source: DbLikeDataSource, topic: str):
        self._config = config
        self._data_source = data_source
        self._topic = topic

    def produce(self, message: str):
        pass
