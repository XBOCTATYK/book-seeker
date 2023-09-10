from collections import namedtuple
from urllib.parse import urlunparse, urlencode


class UrlUtils:
    Components = namedtuple(
        typename='Components',
        field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
    )

    def create_url(self, host: str, path: str, query: dict, scheme: str = 'https', anchor: str = None):
        return urlunparse(
            self.Components(
                scheme=scheme,
                netloc=host,
                query=urlencode(query, True, '', 'utf-8'),
                path='',
                url=path,
                fragment=anchor
            )
        )
