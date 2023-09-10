from urllib.parse import unquote
from deepmerge import always_merger

import urllib3

from apps.scavenger.config.BookDataParserConfig import BookDataParserConfig
from apps.scavenger.models.dto import MarkersRequestDto
from apps.scavenger.models.logic.FetchOptions import FetchOptions
from apps.scavenger.models.serializers.coordinates_serializers import map_view_box_to_string
from apps.scavenger.models.serializers.date_time_serializers import format_date_time
from datasource.rest.UrlCreator import create_url


class BookDataFetcher:
    _config: BookDataParserConfig = None
    _book_config: dict = None
    _secret_headers: dict = {}
    _last_result = None

    def __init__(self, config: BookDataParserConfig, book_config: dict, secret_headers: dict):
        self._config = config
        self._book_config = book_config
        self._secret_headers = secret_headers

    def fetch(self, fetch_options: FetchOptions):
        headers = self._set_headers()

        print(headers)

        raise Exception('uuu')

        self._last_result = urllib3.request(
            url=unquote(self._create_url(fetch_options)),
            method='GET',
            headers=headers,
            decode_content=True
        )

        print(self._last_result.status)

        return self._last_result.json()

    def _create_url(self, fetch_options: FetchOptions):
        query_params = self._set_query_params(fetch_options)
        print(query_params)

        return create_url(
            host=self._config['baseUrl'],
            path=self._config['optionsUrl'],
            query=query_params
        )

    def _set_query_params(self, fetch_options: FetchOptions) -> MarkersRequestDto:
        return {
            'dest_type': 'city',
            'ref': 'searchresults',
            'limit': 100,
            'lang': 'en-gb',
            'checkin': format_date_time(fetch_options.checkin),
            'checkout': format_date_time(fetch_options.checkout),
            'room1': 'A,A',
            'maps_opened': 1,
            'sr_countrycode': 'th',  # TODO: заменить
            'spr': 1,
            'currency': fetch_options.currency,
            'nflt': str(fetch_options.filter),
            'order': 'popularity',
            'ltfd_excl': f';BBOX={map_view_box_to_string(fetch_options.map_box)}',
        }

    def _set_headers(self) -> dict:
        return always_merger.merge({
            'content-typ': 'application/json; utf-8',
            'authority': self._book_config['authority'],
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'cookie': 'px_init=0; cors_js=1; bkng_sso_session=eyJib29raW5nX2dsb2JhbCI6W3sibG9naW5faGludCI6IkFHTzVObVdmRW9lc3NsL2tUN0FnbFA0U0cyZ210Zk8wSHR2OStEY2I5blEifV19; bkng_sso_ses=eyJib29raW5nX2dsb2JhbCI6W3siaCI6IkFHTzVObVdmRW9lc3NsL2tUN0FnbFA0U0cyZ210Zk8wSHR2OStEY2I5blEifV19; pcm_consent=consentedAt%3D2023-09-07T17%3A30%3A05.992Z%26countryCode%3DRU%26expiresAt%3D2024-03-05T17%3A30%3A05.992Z%26implicit%3Dfalse%26regionCode%3DMOW%26regulation%3Dgdpr%26legacyRegulation%3Dgdpr%26consentId%3D00000000-0000-0000-0000-000000000000%26analytical%3Dfalse%26marketing%3Dfalse; _pxvid=827c23d1-4da2-11ee-9b2f-f53331510dcc; _pxhd=E8CbtCVFdKkc7qufP7Ucw1Kjw19n1QELBvjW-t7z4l1Vd5D%2FGRVfZmsuYgRf%2FC%2F-9Wo8uj1zphDyvvwW%2FvoaxA%3D%3D%3AfE2faxinNVFXfHug1BdpFXdA76%2Fj1LKjbA%2FE8lnVICeNmrOIq37ywBXAM8nUBHc4TzrC1kcdJi5g0M1SeBjuJQUUg0aB05e00QpXnKxRHcY%3D; bkng_sso_auth=CAIQsOnuTRqUAV81EgeipRhY3XN1daafKiJ0CUqCoIRRZipy0p1XR0o3Pj5nLHVqi1uiouBvCTNOvc226TFJgbwnp7l1DNPqTAsD9OUMMDXWTPCUE/m6+ufWq8Q8QY00GcUkcGhrJl0JCMsX73ACTe7Ug9wevYk/laRjjV7mNzQ4uME3PhCQkhQtBbq4KAlwD580wKnDasqoE3zZ+IE=; lastSeen=1694356874830; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLb9qg0InA%2FFDczAXbuPf2yEvbw5CHcnMQlXIQWsBDDk8PuIy88V21ukqk%2FDYVrn9hBi2YpEwArar1sb%2BVXda9PHdoAb8BGHg87QvvGAZM05j4gwSdhmJQurNwMq2dsMOsV3heUA5p0SSG2jecPmRE8uZaHK1if7k414fTzT%2F3SY%2BBnPdMba08o1mzyhKSNZbpTxnMH20SJHrd%2B0hBASxJPHv3%2BTTyYDu93; _pxhd=E8CbtCVFdKkc7qufP7Ucw1Kjw19n1QELBvjW-t7z4l1Vd5D%2FGRVfZmsuYgRf%2FC%2F-9Wo8uj1zphDyvvwW%2FvoaxA%3D%3D%3AfE2faxinNVFXfHug1BdpFXdA76%2Fj1LKjbA%2FE8lnVICeNmrOIq37ywBXAM8nUBHc4TzrC1kcdJi5g0M1SeBjuJQUUg0aB05e00QpXnKxRHcY%3D; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLb9qg0InA%2FFDckk34WD6CBo6y1GD13sluMk%2B9NWHfRMuK0qkXlzITZKJ9BN%2F6zSaI%2BmzKp%2FdV1jbCihPZCLVVlQd439U%2FxeXV5tGVpNoz2KofFqV8xVWBJTC%2FtDT%2FEzbzD4Jskjj2RLeSB454fHvrxJpbQhXWldXja1EGgyLnLz2reqCyPCM9DyYqoXPLtRV8wG6UqlmaKK7WMqRCHLaKc0dvbgZ%2FRcRg7; bkng_sso_auth=CAIQsOnuTRqUATQnagTvZuDibQLveuJFuMBujv6auNanQePuD521ZRAtEHG9/dxrCRqNIL3Yn6jUQr/LykEVRTv/lIHf+N0lSavpHKo3UYxCTiqAokQt/escIHud46aHBhOdRV6f8rx54XglvdsuhoQfH+noXk5xnvjbOmlSqliFYqE/yxTEwCL/jr6zmyjMu1Xpvv2PY3A+2w+Mx80=',
            'referer': self._book_config['referrer'],
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }, self._secret_headers)
