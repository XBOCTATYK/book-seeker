from functools import reduce


def serialize_persons_count(count: int):
    reduce(lambda acc, x: acc + ',' + x, ['A'] * count)
