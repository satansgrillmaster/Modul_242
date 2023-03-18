from enum import Enum


class QueryMethod(Enum):
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4


class Table(Enum):
    TASK_LOG = "task_log"
    HALO_RING_CONFIG = "halo_ring_config"
    LED_COLOR = "led_color"

