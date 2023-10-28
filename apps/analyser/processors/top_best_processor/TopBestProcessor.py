from typing import List

from apps.analyser.processors.AbstractProcessor import AbstractProcessor
from apps.analyser.services.SummarizeGoodsService import SummarizeGoodsService


class TopBestProcessor(AbstractProcessor):
    _summarize_goods_service: SummarizeGoodsService

    def __init__(self, summarize_goods_service: SummarizeGoodsService):
        self._summarize_goods_service = summarize_goods_service

    def process(self, values: List[dict]):
        scores = self._summarize_goods_service.summarize_all(values)

        print(scores)
