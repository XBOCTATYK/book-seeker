from collections import namedtuple
from urllib.parse import urlunparse, urlencode

Components = namedtuple(
    typename='Components',
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)


def create_url(host,
               path,
               query,
               scheme='https',
               url='',
               anchor=None):
    return urlunparse(
        Components(
            scheme=scheme,
            netloc=host,
            query=urlencode(query),
            path=path,
            url=url,
            fragment=anchor
        )
    )


class UrlCreator:
    pass
