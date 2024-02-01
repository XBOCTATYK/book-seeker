from apps.AbstractApp import AbstractApp
from apps.features.db_migrations.FeaturesAppMigrationScheme import FeatureAppMigrationScheme
from apps.features.lib.FeatureService import FeatureService
from apps.features.model.EConditionOperatorTypes import EConditionOperatorTypes
from apps.features.model.EConditionTypes import EConditionTypes
from apps.features.services.dictionaries.ConditionOperatorDictionary import ConditionOperatorDictionary
from apps.features.services.dictionaries.ConditionTypeDictionary import ConditionTypeDictionary
from apps.features.services.respositories.ConditionRepository import ConditionRepository
from common.db_migrations.AbstractMigrationScheme import AbstractMigrationScheme
from common.services.DbDictionary import DbDictionary
from datasource.DbLikeDataSource import DbLikeDataSource
from datasource.providers.PostgresDataProvider import PostgresDataProvider


class FeaturesApp(AbstractApp):
    _config = {}
    _data_source: DbLikeDataSource = None
    _condition_type_dictionary: DbDictionary = None
    _condition_operator_dictionary: DbDictionary = None
    _condition_repository = None
    _feature_service = None

    def __init__(self, config: dict):
        super().__init__(config)
        self._config = config

    def start(self):
        db_config = self._config['db']

        self._data_source = DbLikeDataSource(PostgresDataProvider(db_config))
        self._condition_type_dictionary = ConditionTypeDictionary(self._data_source)
        self._condition_operator_dictionary = ConditionOperatorDictionary(self._data_source)
        self._condition_repository = ConditionRepository(
            self._data_source,
            self._condition_type_dictionary,
            self._condition_operator_dictionary
        )
        self._feature_service = FeatureService(self._condition_repository)

        self._run_app()

    def _run_app(self):
        self._feature_service.get_feature_by_params(
            condition_type=EConditionTypes.PLATFORM,
            condition_operator=EConditionOperatorTypes.EQUAL,
        )

    def stop(self):
        pass

    def exports(self) -> dict:
        return {}

    def start_migrations(self) -> AbstractMigrationScheme:
        return FeatureAppMigrationScheme()
