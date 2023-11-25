from telegram import Bot

from apps.notifier.repositories.TgUserToFetchOptionsRepository import TgUserToFetchOptionsRepository


class TgUsersNotifier:
    _repository: TgUserToFetchOptionsRepository

    def __init__(self, repository: TgUserToFetchOptionsRepository):
        self._repository = repository

    def notify(self, bot: Bot):
        pass
