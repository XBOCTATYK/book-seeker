from typing import TypedDict


class FilterOptions(TypedDict):
    min_price: str
    max_price: str
    rooms: int
    review_score: float
    currency: str
