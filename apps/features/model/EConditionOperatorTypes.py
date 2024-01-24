from enum import Enum


class EConditionOperatorTypes(Enum):
    EQUAL = 0
    NOT_EQUAL = 1
    LESS = 2
    LESS_OR_EQUAL = 3
    GREATER = 4
    GREATER_OR_EQUAL = 5
    IN = 6
    NOT_IN = 7
    CONTAINS = 8
    NOT_CONTAINS = 9
    STARTS_WITH = 10
    NOT_STARTS_WITH = 11
    ENDS_WITH = 12
    NOT_ENDS_WITH = 13
    IS_NULL = 14
    NOT_IS_NULL = 15
