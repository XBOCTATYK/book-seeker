from typing import Callable


def make_filter_for_map(key: str, fn: Callable[[dict], bool]) -> Callable[[dict], bool]:
    return lambda x: fn(x[key]) if key in x and x[key] is not None else False
