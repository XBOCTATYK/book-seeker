from sqlalchemy import insert, Connection

from apps.analyser.db_migrations.dictionaries import migration_dictionaries
from apps.analyser.models.db.ParamWeightDto import ParamWeightDto


def insert_weights(connection: Connection):
    values_to_insert = list(map(
        lambda x: {'param_name': x, 'weight_value': 0},
        migration_dictionaries['clean_data_params_dictionary']
    ))
    insert_params_statement = insert(ParamWeightDto).values(values_to_insert)
    connection.execute(insert_params_statement)
