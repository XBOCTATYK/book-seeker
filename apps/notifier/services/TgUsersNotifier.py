import asyncio
from functools import reduce

from telegram import Bot

from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto
from apps.analyser.models.dictionaries.ClearingDictionary import ClearingDictionary
from apps.notifier.repositories.TgUserRepository import TgUserRepository
from apps.notifier.repositories.TgUserToFetchOptionsRepository import TgUserToFetchOptionsRepository
from apps.transit_data_app.models.db.FilteredResultDto import FilteredResultDto
from common.lib.also import also


class TgUsersNotifier:
    _repository: TgUserToFetchOptionsRepository
    _tg_user_repository: TgUserRepository
    _clean_data_params_dictionary: ClearingDictionary
    _dict_id: int = None
    _config = {}

    def __init__(
            self,
            repository: TgUserToFetchOptionsRepository,
            tg_user_repository: TgUserRepository,
            clean_data_params_dictionary: ClearingDictionary,
            config: dict
    ):
        self._repository = repository
        self._tg_user_repository = tg_user_repository
        self._clean_data_params_dictionary = clean_data_params_dictionary
        self._dict_id = self._clean_data_params_dictionary.select_by_id('b_url')
        self._config = config

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
        result_list = reduce(self._format_url, filtered_data, [])
        return '\n ===== \n'.join(str(x) for x in result_list)

    def _format_url(self, acc: list, item):
        next_val = self._find_url(item.clean_data.param_set)
        return also(acc, lambda x: acc.append(self._config['baseUrl'] + next_val + '\n' + '=====' + '\n'))

    def _find_url(self, param_set: list[CleanDataParamDto]) -> str:
        result = next(x for x in param_set if x.type == self._dict_id)
        return result.value if result is not None else ''
