from typing import TypedDict


class CleanDataEstimationResult(TypedDict):
    estimate: float
    param_set: dict


class CleanDataEstimate(TypedDict):
    id: int
    estimate_result: CleanDataEstimationResult
