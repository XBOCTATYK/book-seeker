from telegram import Bot

from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.notifier.repositories.TgUserRepository import TgUserRepository
from apps.notifier.repositories.TgUserToFetchOptionsRepository import TgUserToFetchOptionsRepository
from apps.notifier.services.FilteredResultMessageFormatter import FilteredResultMessageFormatter
from apps.transit_data_app.models.db.FilteredResultDto import FilteredResultDto


class TgUsersNotifier:
    _repository: TgUserToFetchOptionsRepository
    _tg_user_repository: TgUserRepository
    _clean_data_params_dictionary: ClearingDictionary
    _filtered_result_formatter: FilteredResultMessageFormatter

    def __init__(
            self,
            repository: TgUserToFetchOptionsRepository,
            tg_user_repository: TgUserRepository,
            filtered_result_formatter: FilteredResultMessageFormatter,
    ):
        self._repository = repository
        self._tg_user_repository = tg_user_repository

        self._filtered_result_formatter = filtered_result_formatter

    async def notify(self, bot: Bot, filtered_data: list[FilteredResultDto]):
        users = self._tg_user_repository.get_all_active()

        for user in users:
            await self._send(bot, filtered_data, user)

        return filtered_data

    async def _send(self, bot: Bot, filtered_data: list[FilteredResultDto], user):
        message = self._format_message(filtered_data)

        if message is not None and message != '':
            await bot.send_message(user.tg_id, text=message)

    def _format_message(self, filtered_data: list[FilteredResultDto]) -> str:
        return self._filtered_result_formatter.format(filtered_data)


