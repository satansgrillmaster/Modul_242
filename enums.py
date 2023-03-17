from enum import Enum


class QueryMethod(Enum):
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4


class Table(Enum):
    LOG = "task_log"

