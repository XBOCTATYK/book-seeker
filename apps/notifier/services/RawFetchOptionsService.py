from apps.raw_fetch_options_processor.model.db.RawFetchOptionsDto import RawFetchOptionsDto
from apps.raw_fetch_options_processor.repositories.RawFetchOptionsRepository import RawFetchOptionsRepository


class RawFetchOptionsService:
    _raw_fetch_options_repository: RawFetchOptionsRepository = None

    def __init__(self, raw_fetch_options_repository: RawFetchOptionsRepository):
        self._raw_fetch_options_repository = raw_fetch_options_repository

    def save_raw_fetch_options(self, raw_fetch_option_url: str):
        raw_fetch_options_dto = RawFetchOptionsDto(url=raw_fetch_option_url, status='NEW')
        rest = self._raw_fetch_options_repository.save(raw_fetch_options_dto)
        print(rest)
