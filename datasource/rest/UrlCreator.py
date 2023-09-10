from collections import namedtuple
from urllib.parse import urlunparse, urlencode

Components = namedtuple(
    typename='Components',
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)


def create_url(host,
               path,
               query: dict,
               scheme='https',
               anchor=None):
    return urlunparse(
        Components(
            scheme=scheme,
            netloc=host,
            query=urlencode(query, True, '', 'utf-8'),
            path='',
            url=path,
            fragment=anchor
        )
    )


class UrlCreator:
    pass
