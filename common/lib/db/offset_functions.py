from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.model.db.BaseDto import BaseDto


def find_element_with_minimal_id_more_than_current(sess: Session, dto: Type[BaseDto], current: int):
    additional_search_statement = select(dto)\
        .where(dto.id >= current)\
        .order_by(dto.id)\
        .limit(1)
    raw_data_db_result = sess.execute(additional_search_statement)

    return raw_data_db_result.one_or_none()
