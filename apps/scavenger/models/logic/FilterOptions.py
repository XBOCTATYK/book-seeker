from dataclasses import dataclass


@dataclass
class FilterOptions:
    rooms: int
    review_score: int
    oos: str
    min_price: int
    max_price: int
    currency: str

    def __str__(self):
        return f'oos={self.oos};review_score={self.review_score*10};' \
               f'price={self.currency}-{self.min_price}-{self.max_price}-1'

