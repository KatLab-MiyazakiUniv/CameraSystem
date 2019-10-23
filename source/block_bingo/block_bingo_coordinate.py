"""
    @file   block_bingo_coordinate.py
    @author T.Miyaji
    @brief  ブロックビンゴ攻略に使用するブロックサークルおよび交点サークルの座標を提供する。
"""
from enum import Enum, auto

# TODO Colorクラスは他のファイルにもあるので、統合する
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

class BlockCirclesCoordinate():
    """
    ブロックサークルの座標を表すクラス
    """
    def __init__(self, is_left, bonus):
        """
        ブロックサークルの座標と色を設定する。

        Parameters
        ----------
        is_left : bool
            Lコースかどうか
        bonus : int
            ボーナスサークルのブロックサークル番号
        """
        # ブロックサークルの座標を辞書に登録する
        self.block_circles = { 1: (0, 0), 2: (0, 1), 3: (0, 2),
                               4: (1, 0),            5: (1, 2),
                               6: (2, 0), 7: (2, 1), 8: (2, 2)}
        # ブロックサークルの色を登録する
        if is_left:
            self.block_circle_color = [Color.YELLOW, Color.GREEN, Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN, Color.RED, Color.BLUE]
        else:
            self.block_circle_color = [Color.RED, Color.GREEN, Color.YELLOW, Color.YELLOW, Color.BLUE, Color.BLUE, Color.RED, Color.GREEN]
        # ブロックが設置されていないブロックサークルの座標を登録する
        self.open = [i+1 for i in range(8)]
        # ボーナスサークルの座標を登録する
        self.bonus = self.get(bonus)
    

    def get(self, circle_number):
        """
        ブロックサークル番号に関連するサークルの座標を返す。
        
        Parameters
        ----------
        circle_number : int
            ブロックサークル番号
        """
        
        if circle_number < 1 or 8 < circle_number:
            raise ValueError('Block circle number is invalid!')
        return self.block_circles[circle_number]
