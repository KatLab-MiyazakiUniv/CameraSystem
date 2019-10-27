"""
    @file   block_bingo_coordinate.py
    @author T.Miyaji
    @brief  ブロックビンゴ攻略に使用するブロックサークルおよび交点サークルの座標を提供する。
"""
from enum import Enum, auto
import numpy as np

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
    def __init__(self, is_left, bonus, color):
        """
        ブロックサークルの座標と色を設定する。

        Parameters
        ----------
        is_left : bool
            Lコースかどうか
        bonus : int
            ボーナスサークルのブロックサークル番号
        color : int
            カラーブロックが置かれたサークルのブロックサークル番号
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
        # ボーナスサークルのブロックサークル番号を登録する
        self.bonus_circle = bonus
        # カラーブロックが置かれたサークルのブロックサークル番号を登録する
        self.color_circle = color
    

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

    
    def colors(self, candidate):
        """
        ブロックを設置するブロックサークルの番号から、サークルの色を返す。

        candidate : list
            ブロックビンゴを成立するためのブロックサークル番号のリスト
        """
        return [self.block_circle_color[number-1] for number in candidate]


class CrossCirclesCoordinate():
    """
    交点サークルの座標を表すクラス。
    """
    def __init__(self):
        """
        交点サークルの座標を登録する。
        """
        # 交点サークルの座標を表す4x4行列を作成する(配列の要素は、配置されたブロックの色を表す)
        self.cross_circles = np.full((4, 4), Color.NONE)
        # 初期位置としてブロックが置かれている交点サークルの座標をリスト化する
        self.open = [(0,0), (1,1), (0,2), (1,3), (2,0), (3,1), (2,2), (3,3)]
    

    def color(self, coordinate):
        """
        指定した交点サークルの座標に置かれているブロックの色を取得する。

        Parameters
        ----------
        coordinate : tuple
            交点サークルの座標
        """
        return self.cross_circles[coordinate[0], coordinate[1]]


    def set_block_color(self, coordinate, color):
        """
        指定した交点サークルの座標に置かれたブロックの色を設定する。

        Parameters
        ----------
        coordinate : tuple
            交点サークルの座標
        color : Color
            配置ブロックの色
        """
        if coordinate[0] < 0 or 3 < coordinate[0]:
            raise ValueError('x-coordinate of cross circles is invalid!')
        if coordinate[1] < 0 or 3 < coordinate[1]:
            raise ValueError('y-coordinate of cross circles is invalid!')
        
        self.cross_circles[coordinate[0], coordinate[1]] = color
    

    def goal_node(self, current, block_circle):
        """
        設置するブロックサークル番号の周辺にある交点サークルのうち、走行体に最も近い距離にある座標を返す。

        Parameters
        ----------
        current : tuple
            走行体の現在地
        block_circle : tuple
            ブロックサークルの座標
        """
        # ブロックサークルの周辺にある4つの交点サークルの座標を取得する
        coordinates = [block_circle,
                       (block_circle[0], block_circle[1]+1),
                       (block_circle[0]+1, block_circle[1]),
                       (block_circle[0]+1, block_circle[1]+1)]
        # ブロックが置かれた交点サークルの座標を取り除く
        coordinates = list(set(coordinates) - set(self.open))
        # 交点サークルの座標と現在地の距離を計算する
        distance = list(map(lambda x: abs(x[0]-current[0]) + abs(x[1]-current[1]), coordinates))

        return coordinates[distance.index(min(distance))]


    def move_block(self, coordinate):
        """
        交点サークルからブロックを取得して移動したことをデータ構造に登録する。

        Parameters
        ----------
        coordinate : tuple
            交点サークルの座標
        """
        # 引数の交点サークルの座標に置いてあるブロックの色をNONEに設定する
        self.set_block_color(coordinate, Color.NONE)
        # openリストから削除する
        self.open.remove(coordinate)