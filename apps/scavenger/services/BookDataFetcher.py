from functools import reduce
from urllib.parse import unquote
from deepmerge import always_merger

import urllib3

from apps.scavenger.config.BookDataParserConfig import BookDataParserConfig
from apps.scavenger.models.dto import MarkersRequestDto
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.mappers.filter_options_mapper import FilterOptionsSerializer
from apps.scavenger.models.serializers.coordinates_serializers import map_view_box_to_string
from apps.scavenger.models.serializers.date_time_serializers import serialize_date_time
from apps.scavenger.models.serializers.persons_serializer import serialize_persons_count
from apps.scavenger.services.DataFetcher import DataFetcher
from datasource.rest.UrlUtils import UrlUtils


class BookDataFetcher(DataFetcher):
    _url_utils: UrlUtils
    _filter_options_serializer: FilterOptionsSerializer
    _config: BookDataParserConfig = None
    _book_config: dict = None
    _secret_headers: dict = {}
    _last_result = None

    def __init__(self, url_utils: UrlUtils, filter_options_serializer: FilterOptionsSerializer,
                 config: BookDataParserConfig, book_config: dict, secret_headers: dict):
        self._url_utils = url_utils
        self._config = config
        self._book_config = book_config
        self._secret_headers = secret_headers
        self._filter_options_serializer = filter_options_serializer

    def fetch(self, fetch_options: FetchOptions):
        url = unquote(self._create_url(fetch_options))
        headers = self._get_headers()

        print(url)

        # raise Exception('uuu')
        self._last_result = urllib3.request(
            url=url,
            method='GET',
            headers=headers,
            decode_content=True
        )

        print(self._last_result.status)

        return self._last_result.json()

    def _create_url(self, fetch_options: FetchOptions):
        query_params = self._get_query_params(fetch_options)

        return self._url_utils.create_url(
            host=self._config['baseUrl'],
            path=self._config['optionsUrl'],
            query=query_params
        )

    def _get_query_params(self, fetch_options: FetchOptions) -> MarkersRequestDto:
        return {
            'dest_type': 'city',
            'ref': 'searchresults',
            'limit': 2,
            'lang': 'en-gb',
            'checkin': serialize_date_time(fetch_options.checkin),
            'checkout': serialize_date_time(fetch_options.checkout),
            'room1': serialize_persons_count(fetch_options.persons),
            'maps_opened': 1,
            'sr_countrycode': 'th',  # TODO: заменить
            'spr': 1,
            'currency': fetch_options.currency,
            'nflt': self._filter_options_serializer.serialize(fetch_options.filter),
            'order': 'popularity',
            'ltfd_excl': f';BBOX={map_view_box_to_string(fetch_options.map_box)}',
        }

    def _get_headers(self) -> dict:
        return always_merger.merge({
            'content-typ': 'application/json; utf-8',
            'authority': self._book_config['authority'],
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'cookie': 'bkng_sso_session=eyJib29raW5nX2dsb2JhbCI6W3sibG9naW5faGludCI6IkFHTzVObVdmRW9lc3NsL2tUN0FnbFA0U0cyZ210Zk8wSHR2OStEY2I5blEifV19; bkng_sso_ses=eyJib29raW5nX2dsb2JhbCI6W3siaCI6IkFHTzVObVdmRW9lc3NsL2tUN0FnbFA0U0cyZ210Zk8wSHR2OStEY2I5blEifV19; _pxhd=0mnETSTRVT%2FLQNZsl3c28G4zxVq3v6Encs-aFkhiAhz%2F3dcti7bZG0B5yImwCh1riE34TU1aMYiae6po%2FPozgQ%3D%3D%3ARE-Kwi10A2f0hUFZvDl8Qyczxdx-ZAx3SSDMk79iZbTnE53lnDdYGzQ4BKbi0Q8CWi7edOuAR6IerjhRjAfLWCyzxO0xb1xNXoRO3e6iv10%3D; pcm_consent=analytical%3Dfalse%26countryCode%3DRU%26consentedAt%3D2023-09-15T21%3A10%3A26.282Z%26expiresAt%3D2024-03-13T21%3A10%3A26.282Z%26implicit%3Dtrue%26marketing%3Dfalse%26regionCode%3DMOW%26regulation%3Dgdpr%26legacyRegulation%3Dgdpr; bkng_sso_auth=CAIQsOnuTRqUAU30Aj4XykN+xyjw6qYQ01GtsrAITB2Cc5QyBEaVECHoG7uAG8JzYpc9C8DDrRbg8x3wbBvblgIWzJKxSPU8lzfK2sfxZrTuZe4KrXiHp8bWj6KxZlrzaI+LE8kvSIh54pBX30rXdPWm+kDYesfYia2NvS2Uxm1BgGOHtlUKTW3+zMdvW9abfmfOhI2FGBN/TZvrL/0=; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbmlZgMctCRAZYcE%2FYie%2FrcXkdPIFx%2B78syDQUbLXUBFhXoM8OMHjPLElGY6xNY6iW8oYvsiZAcD7zqn7D6WkUeBQL%2FTNi1q%2FKI7NEZlmxDLHtOisWr1zO34yW1b%2FQe96iFqsHKJJk0L7ZoPbU19LMDlaF%2BDbwk5TcNV1Yvqe20okHPfhAXVE8%2Bvr%2FVju883QaGBcI9E37SaV86eQDLF8NpDBzjWZmFBvd',
            'referer': self._book_config['referrer'],
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }, self._secret_headers)
