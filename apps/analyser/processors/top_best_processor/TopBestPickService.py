from typing import List

from apps.analyser.models.CleanDataEstimations import CleanDataEstimate
from apps.analyser.models.db.CleanDataDto import CleanDataDto
from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.services.SummarizeGoodsService import SummarizeGoodsService
from apps.transit_data_app.repositories.FilteredDataRepository import FilteredDataRepository


class TopBestPickService(AbstractProcessor):
    _summarize_goods_service: SummarizeGoodsService
    _filtered_data_repository: FilteredDataRepository

    def __init__(
            self,
            summarize_goods_service: SummarizeGoodsService,
            filtered_data_repository: FilteredDataRepository
    ):
        self._summarize_goods_service = summarize_goods_service
        self._filtered_data_repository = filtered_data_repository

    def pick_and_save_top_options(self, values: List[CleanDataDto], count: int) -> List[CleanDataDto]:
        if len(values) == 0:
            return values

        scores: List[CleanDataEstimate] = list(map(
            lambda clean_data_item: CleanDataEstimate(
                id=clean_data_item.id,
                estimate_result=self._get_estimate(clean_data_item)
            ),
            values
        ))

        sorted_by_score_item: List[CleanDataEstimate] = sorted(
            scores,
            key=lambda item: item['estimate_result']['estimate'],
            reverse=True
        )

        sorted_items_ids: List[int] = list(map(lambda item: item['id'], sorted_by_score_item))
        top_values = sorted_items_ids[0:count]
        self._filtered_data_repository.insert_filtered_data(top_values)

        return values

    def _get_estimate(self, clean_data_dto: CleanDataDto):
        return self._summarize_goods_service.summarize(
            dict(map(
                lambda clean_data_param: (clean_data_param.type, clean_data_param.value),
                clean_data_dto.param_set
            )),
        )
