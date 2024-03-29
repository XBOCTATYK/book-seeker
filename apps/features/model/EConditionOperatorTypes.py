from enum import Enum


class EConditionOperatorTypes(Enum):
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS = 'LESS'
    LESS_OR_EQUAL = 'LESS_OR_EQUAL'
    GREATER = 'GREATER'
    GREATER_OR_EQUAL = 'GREATER_OR_EQUAL'
    IN = 'IN'
    NOT_IN = 'NOT_IN'
    CONTAINS = 'CONTAINS'
    NOT_CONTAINS = 'NOT_CONTAINS'
    STARTS_WITH = 'STARTS_WITH'
    NOT_STARTS_WITH = 'NOT_STARTS_WITH'
    ENDS_WITH = 'ENDS_WITH'
    NOT_ENDS_WITH = 'NOT_ENDS_WITH'
    IS_NULL = 'IS_NULL'
    NOT_IS_NULL = 'NOT_IS_NULL'
