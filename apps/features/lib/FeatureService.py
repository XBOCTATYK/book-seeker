from apps.features.services.respositories.ConditionRepository import ConditionRepository


class FeatureService:
    _condition_repository = None

    def __init__(
            self,
            condition_repository: ConditionRepository
    ):
        self._condition_repository = condition_repository

    def get_feature_by_params(self, **kwargs):
        list_of_conditions = self._condition_repository.get_by_type(kwargs['condition_type'])

