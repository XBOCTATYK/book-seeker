from dataclasses import dataclass
from typing import Optional


@dataclass
class FilterOptions:
    rooms: Optional[int]
    review_score: Optional[int]
    oos: Optional[str]
    min_price: Optional[int]
    max_price: Optional[int]
    currency: Optional[str]

    def __str__(self):
        return f'oos={self.oos};review_score={self.review_score*10};' \
               f'price={self.currency}-{self.min_price}-{self.max_price}-1'

