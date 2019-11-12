"""
    @file   Color.py
    @author T.Miyaji
    @brief  カメラシステムで用いる色を定義する。
"""
from enum import Enum, auto

class Color(Enum):
    """
    ブロック、ブロックサークルまたは交点サークルの色。
    """
    NONE = auto()   # ブロックが置かれていない状態を表現するために用いる
    RED = auto()
    BLUE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLACK = auto()
    WHITE = auto()