from sqlalchemy import Connection, select
from sqlalchemy.dialects.postgresql import insert

from apps.analyser.models.db.CleanDataParamsDictionaryDto import CleanDataParamsDictionaryDto
from apps.analyser.models.db.ParamWeightDto import ParamWeightDto


def insert_weights(connection: Connection):
    ids_select_statement = select(CleanDataParamsDictionaryDto)
    ids_select_db_result = connection.execute(ids_select_statement).all()
    ids = list(map(lambda x: [x[0], x[1]], ids_select_db_result))

    values_to_insert = list(map(
        lambda x: {'param_name': x[0], 'weight_value': 0},
        ids
    ))

    insert_params_statement = insert(ParamWeightDto)\
        .values(values_to_insert)\
        .on_conflict_do_nothing()
    connection.execute(insert_params_statement)
