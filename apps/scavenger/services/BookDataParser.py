import urllib3

from apps.scavenger.config.BookDataParserConfig import BookDataParserConfig
from datasource.rest.UrlCreator import create_url


class BookDataParser:
    _config: BookDataParserConfig = None
    _last_result = None

    def __init__(self, config: BookDataParserConfig):
        self._config = config

    def fetch(self):
        self._last_result = urllib3.request(
            url=self._create_url(),
            method='GET',
            headers={'Content-Type': 'application/json'},
            decode_content=True
        )

    def _create_url(self):
        return create_url(
            host=self._config['baseUrl'],
            path=self._config['optionsUrl'],
            query={}
        )


