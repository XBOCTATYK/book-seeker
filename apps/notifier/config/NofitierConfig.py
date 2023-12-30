from typing import TypedDict

from apps.notifier.config.BotConfig import BotConfig


class NotifierConfig(TypedDict):
    bot: BotConfig
    web: dict
    db: dict
