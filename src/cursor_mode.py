from enum import Enum


class CursorMode(Enum):
    SELECT = 1
    CUE = 2
    ANNOTATE = 3  # future
    OFFSET = 4
