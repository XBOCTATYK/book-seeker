from sqlalchemy import Connection
from sqlalchemy.dialects.postgresql import insert

from apps.notifier.models.db.TgUserDto import TgUserDto


def insert_default_user(connection: Connection):
        insert_statement = insert(TgUserDto).values([{'tg_id': 0, 'is_active': True}])\
            .on_conflict_do_nothing()
        connection.execute(insert_statement)

        return True
