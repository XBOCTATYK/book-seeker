from enum import Enum


class ECleanDataStatus(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    PROCESSED = 'PROCESSED'
    UNKNOWN = 'UNKNOWN'
