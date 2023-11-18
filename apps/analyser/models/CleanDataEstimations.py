from typing import TypedDict, List

from apps.analyser.models.db.CleanDataParamDto import CleanDataParamDto


class CleanDataEstimationResult(TypedDict):
    estimate: float
    param_set: dict


class CleanDataEstimate(TypedDict):
    id: int
    estimate_result: CleanDataEstimationResult
