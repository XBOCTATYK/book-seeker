from apps.notifier.models.db.TgUserToFetchOptions import TgUserToFetchOptions
from common.services.AbstractRepository import AbstractRepository
from common.services.OffsetPointerRepository import OffsetPointerRepository
from datasource.DbLikeDataSource import DbLikeDataSource


class TgUserToFetchOptionsRepository(AbstractRepository):
    _tg_user_processing_offset_repository: OffsetPointerRepository

    def __init__(self, data_source: DbLikeDataSource, tg_user_processing_offset_repository: OffsetPointerRepository):
        super().__init__(data_source)
        self._tg_user_processing_offset_repository = tg_user_processing_offset_repository
        self._tg_user_processing_offset_repository.setup_offset(TgUserToFetchOptions)
